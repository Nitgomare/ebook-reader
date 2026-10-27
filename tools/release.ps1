<#
.SYNOPSIS
  科研知识学习中心一键发布：构建校验 → 认证测试 → 提交推送 → 部署 Cloudflare Pages → 核对部署结果。

.DESCRIPTION
  本项目不是 GitHub 与 Cloudflare 自动联动的站点：推送只更新仓库，线上只有执行
  `wrangler pages deploy dist` 才会变化。本脚本把这条固定流水线固化下来，避免漏步骤。

  步骤：
    1. 前置检查：当天 CHANGELOG 条目、Python/Node/npx 可用、Git 远程。
    2. 构建：清掉 dist 内只读属性后执行 manage.py check（构建 + 内容校验）。
    3. 认证测试：node --test tools/worker-auth.test.mjs。
    4. 提交：只暂存明确范围内的文件（不使用 git add .），提交后推送。
    5. 部署：wrangler pages deploy dist，凭证取自环境变量或令牌文件，不写入任何文件。
    6. 核对：确认最新部署为 Production/main，Source 等于本次提交，并检查未登录跳转登录页。

.PARAMETER Message
  提交信息。省略时使用 "发布：YYYY-MM-DD 更新"。

.PARAMETER TokenFile
  存放 Cloudflare API Token 的文本文件（单行）。默认依次尝试
  $env:CLOUDFLARE_API_TOKEN、$env:CF_TOKEN_FILE、D:\Userdata\Desktop\.cloudflare_api_token、
  $HOME\Desktop\.cloudflare_api_token。令牌只注入当前进程环境，不打印、不落盘。

.PARAMETER AccountId
  Cloudflare 账户 ID。默认取 $env:CLOUDFLARE_ACCOUNT_ID，否则读 .wrangler/cache/wrangler-account.json。

.PARAMETER Yes
  跳过提交前的确认提示（用于非交互执行）。

.PARAMETER DryRun
  只打印将要执行的命令与当前状态，不做构建、提交、推送或部署。

.PARAMETER SkipBuild
  复用现有 dist（仍会做认证测试与后续步骤）。谨慎使用，脚本不校验 dist 是否最新。

.PARAMETER NoPush
  提交但不推送。

.PARAMETER NoDeploy
  构建、测试、提交、推送，但不部署。

.EXAMPLE
  .\tools\release.ps1 -Message "新增《机械原理（第四版）》"

.EXAMPLE
  .\tools\release.ps1 -DryRun

.NOTES
  绝不使用 git add .、git reset --hard、git clean -fd、force push。
  工作区中的 PRD.md、tmp/、notebook-preview/ 等草稿不纳入提交范围。
  传入 -Message 时避免使用中文引号“”，PowerShell 会将其当作字符串分隔符，
  导致提交信息被截断；脚本会在提交后比对实际提交说明并给出提示。
#>
[CmdletBinding()]
param(
  [string]$Message,
  [string]$TokenFile,
  [string]$AccountId,
  [switch]$Yes,
  [switch]$DryRun,
  [switch]$SkipBuild,
  [switch]$NoPush,
  [switch]$NoDeploy
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}

$ProjectName = 'research-knowledge-hub'
$Branch = 'main'
$Wrangler = 'wrangler@4.37.0'

# 只提交这些范围；不包含 tmp/、notebook-preview/、PRD.md 等草稿材料。
$IncludePaths = @(
  'CHANGELOG.md', 'README.md', 'books.json', 'build.py', 'manage.py', 'verify.py',
  'public', 'content', 'tools', 'resource-inventory', 'dist'
)

function Write-Step($text) { Write-Host ""; Write-Host "== $text" -ForegroundColor Cyan }
function Write-Ok($text) { Write-Host "   $text" -ForegroundColor Green }
function Write-Warn2($text) { Write-Host "   $text" -ForegroundColor Yellow }
function Fail($text) { Write-Host ""; Write-Host "!! $text" -ForegroundColor Red; exit 1 }

function Invoke-Native {
  param([string]$Exe, [string[]]$Arguments, [switch]$AllowFail)
  Write-Host "   > $Exe $($Arguments -join ' ')" -ForegroundColor DarkGray
  & $Exe @Arguments
  $code = $LASTEXITCODE
  if ($code -ne 0 -and -not $AllowFail) { Fail "命令失败（退出码 $code）：$Exe $($Arguments -join ' ')" }
  return $code
}

# ---------- 定位仓库 ----------
$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root 'manage.py'))) { Fail "未找到项目根目录（缺少 manage.py）：$Root" }
Set-Location $Root
Write-Step "项目根目录：$Root"

$Python = if (Test-Path (Join-Path (Split-Path -Parent $Root) '.venv\Scripts\python.exe')) {
  Join-Path (Split-Path -Parent $Root) '.venv\Scripts\python.exe'
} elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { $null }
if (-not $Python) { Fail '未找到 Python（需要 ../.venv/Scripts/python.exe 或 PATH 中的 python）' }

$Today = Get-Date -Format 'yyyy-MM-dd'
if (-not $Message) { $Message = "发布：$Today 更新" }

# ---------- 前置检查 ----------
Write-Step '前置检查'

if (-not (Select-String -Path (Join-Path $Root 'CHANGELOG.md') -Pattern "^## $Today" -Quiet)) {
  Fail "CHANGELOG.md 缺少当天条目（^## $Today）。请先按「新增 / 优化 / 修复 / 部署」补写，再发布。"
}
Write-Ok "CHANGELOG 含当天条目：## $Today"

$dirty = @(& git status --porcelain)
Write-Ok ("工作区变更条目：{0}" -f $dirty.Count)

function Test-InScope {
  param([string]$Path)
  if ($Path -like 'dist/*') { return $true }
  foreach ($inc in $IncludePaths) {
    if ($Path -eq $inc -or $Path -like "$inc/*") { return $true }
  }
  return $false
}

$untrackedOutside = @($dirty | Where-Object { $_ -like '?? *' } |
  Where-Object { -not (Test-InScope ($_.Substring(3).Trim('"'))) })
if ($untrackedOutside.Count -gt 0) {
  Write-Warn2 '以下未跟踪文件不在提交范围内（保持原样，不提交）：'
  $untrackedOutside | Select-Object -First 10 | ForEach-Object { Write-Warn2 "  $($_.Substring(3))" }
}

$HeadBefore = (& git rev-parse --short HEAD).Trim()
Write-Ok "当前 HEAD：$HeadBefore"

if ($DryRun) {
  Write-Step 'DryRun：以下步骤将被执行，本次不做任何改动'
  Write-Host "   1) 清除 dist 只读属性：Get-ChildItem dist -Recurse -File -Attributes ReadOnly"
  Write-Host "   2) 构建校验：$Python -X utf8 manage.py check"
  Write-Host "   3) 认证测试：node --test tools/worker-auth.test.mjs"
  Write-Host "   4) 提交：git add -A -- $($IncludePaths -join ' ')"
  Write-Host "      提交信息：$Message"
  if (-not $NoPush) { Write-Host "   5) 推送：git push origin $Branch" }
  if (-not $NoDeploy) { Write-Host "   6) 部署：npx --yes $Wrangler pages deploy dist --project-name $ProjectName --branch $Branch --commit-dirty=true" }
  Write-Host "   7) 核对：wrangler pages deployment list / 未登录跳转检查"
  exit 0
}

# ---------- 构建 ----------
if (-not $SkipBuild) {
  Write-Step '清除 dist 内只读属性（Windows 上只读文件会导致重建失败）'
  $readonly = @(Get-ChildItem -Path (Join-Path $Root 'dist') -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.IsReadOnly })
  if ($readonly.Count -gt 0) {
    $readonly | ForEach-Object { $_.IsReadOnly = $false }
    Write-Ok ("已清除 {0} 个只读文件" -f $readonly.Count)
  } else { Write-Ok '无需处理' }

  Write-Step '构建与内容校验'
  Invoke-Native $Python @('-X', 'utf8', 'manage.py', 'check') | Out-Null
  Write-Ok '构建校验通过'
} else {
  Write-Warn2 '按参数跳过构建，将部署现有 dist'
}

# ---------- 认证测试 ----------
Write-Step '认证与访问控制测试'
if (Get-Command node -ErrorAction SilentlyContinue) {
  Invoke-Native 'node' @('--test', 'tools/worker-auth.test.mjs') | Out-Null
  Write-Ok '认证测试通过'
} else {
  Write-Warn2 '未找到 node，跳过认证测试'
}

# ---------- 提交 ----------
Write-Step '暂存变更（仅明确范围）'
& git add -A -- $IncludePaths
if ($LASTEXITCODE -ne 0) { Fail 'git add 失败' }
$staged = @(& git diff --cached --name-only)
Write-Ok ("暂存文件数：{0}" -f $staged.Count)

if ($staged.Count -eq 0) {
  Write-Warn2 '没有需要提交的变更，继续部署现有 dist'
} else {
  if (-not $Yes) {
    Write-Host ""
    Write-Host "  提交信息：$Message"
    $answer = Read-Host '  确认提交并推送到 GitHub？(y/N)'
    if ($answer -notmatch '^[Yy]') { Fail '已取消（未提交）。' }
  }
  Invoke-Native 'git' @('-c', 'core.quotepath=false', 'commit', '-q', '-m', $Message) | Out-Null
  Write-Ok '提交完成'
  $actualSubject = (& git log -1 --format=%s).Trim()
  if ($actualSubject -ne $Message) {
    Write-Warn2 "提交说明与预期不一致（实际：$actualSubject）"
    Write-Warn2 '若因引号被 shell 截断，可在下一次提交中补充说明。'
  }

  if (-not $NoPush) {
    Write-Step '推送到 GitHub'
    $env:GIT_TERMINAL_PROMPT = '0'
    $pushCode = Invoke-Native 'git' @('push', 'origin', $Branch) -AllowFail
    if ($pushCode -ne 0) {
      Fail "推送被拒绝：远端可能有新提交。请手动执行 git fetch 后合并，禁止 force push。"
    }
    Write-Ok '推送完成'
  } else { Write-Warn2 '按参数跳过推送（仓库与线上将不一致）' }
}

$HeadAfter = (& git rev-parse --short HEAD).Trim()

if ($NoDeploy) {
  Write-Step '按参数跳过部署'
  Write-Ok "提交：$HeadAfter　（仅仓库已更新，线上未变化）"
  exit 0
}

# ---------- 部署 ----------
Write-Step '解析 Cloudflare 凭证'

$token = $env:CLOUDFLARE_API_TOKEN
if (-not $token) {
  $candidates = @()
  if ($env:CF_TOKEN_FILE) { $candidates += $env:CF_TOKEN_FILE }
  if ($TokenFile) { $candidates += $TokenFile }
  $candidates += 'D:\Userdata\Desktop\.cloudflare_api_token'
  $candidates += (Join-Path $HOME 'Desktop\.cloudflare_api_token')
  foreach ($c in $candidates) {
    if ($c -and (Test-Path $c)) { $token = (Get-Content -Raw -Path $c).Trim(); if ($token) { Write-Ok "令牌来源：$c"; break } }
  }
}
if (-not $token) { Fail '未找到 Cloudflare API Token：请设置 $env:CLOUDFLARE_API_TOKEN，或用 -TokenFile 指定文件。' }
if ($token.Length -lt 20) { Fail 'Cloudflare API Token 长度异常，请检查令牌文件。' }

if (-not $AccountId) {
  $AccountId = $env:CLOUDFLARE_ACCOUNT_ID
  if (-not $AccountId) {
    $accountCache = Join-Path $Root '.wrangler\cache\wrangler-account.json'
    if (-not (Test-Path $accountCache)) { $accountCache = Join-Path $HOME 'AppData\Roaming\xdg.config\.wrangler\config\..\..\.wrangler-account.json' }
    if (Test-Path $accountCache) {
      try { $AccountId = (Get-Content -Raw -Path $accountCache | ConvertFrom-Json).account.id } catch {}
    }
  }
}
if (-not $AccountId) { Fail '未找到 Cloudflare 账户 ID：请设置 $env:CLOUDFLARE_ACCOUNT_ID。' }
Write-Ok "账户 ID：$AccountId"

$env:CLOUDFLARE_API_TOKEN = $token
$env:CLOUDFLARE_ACCOUNT_ID = $AccountId
$env:CI = 'true'

Write-Step "部署 dist 到 Cloudflare Pages（项目 $ProjectName / 分支 $Branch）"
$deployLog = Join-Path ([IO.Path]::GetTempPath()) ("pages-deploy-{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
$deployOutput = & npx --yes $Wrangler pages deploy dist --project-name $ProjectName --branch $Branch --commit-dirty=true 2>&1
$deployCode = $LASTEXITCODE
$deployOutput | Set-Content -Path $deployLog -Encoding utf8
$deployOutput | Select-Object -Last 8 | ForEach-Object { Write-Host "   $_" }
if ($deployCode -ne 0) { Fail "部署失败（退出码 $deployCode），完整日志：$deployLog" }
Write-Ok '部署命令执行成功'

# ---------- 核对 ----------
Write-Step '核对最新部署记录'
$listOutput = & npx --yes $Wrangler pages deployment list --project-name $ProjectName 2>&1
$deployId = $null; $source = $null; $envCol = $null; $branchCol = $null
foreach ($line in $listOutput) {
  if ($line -notmatch '│') { continue }
  $cells = @(($line -replace '^\s*│', '' -replace '│\s*$', '') -split '│' | ForEach-Object { $_.Trim() })
  if ($cells.Count -ge 4 -and $cells[0] -match '^[0-9a-f]{8}-[0-9a-f]{4}-') {
    $deployId = $cells[0]; $envCol = $cells[1]; $branchCol = $cells[2]; $source = $cells[3]
    break
  }
}
if (-not $deployId) { Write-Warn2 "无法解析部署列表，请手动核对：$deployLog"; exit 0 }
Write-Ok "部署编号：$deployId"
Write-Ok "Environment：$envCol　Branch：$branchCol　Source：$source"

if ($envCol -ne 'Production') { Fail "最新部署不是 Production（$envCol），请检查 --branch 参数。" }
if ($branchCol -ne $Branch) { Fail "最新部署分支不是 $Branch（$branchCol）。" }
if ($source -and $source -ne '-' -and $HeadAfter -notlike "$source*") {
  Write-Warn2 "部署 Source（$source）与本次提交（$HeadAfter）不一致，请确认是否夹带未提交改动。"
}

Write-Step '检查未登录访问是否仍被拦截'
$headers = @()
if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
  $headers = @(& curl.exe -s -o NUL -D - --max-redirs 0 --max-time 25 "https://$ProjectName.pages.dev/" 2>&1)
}
$statusLine = $headers | Where-Object { $_ -match '^HTTP/' } | Select-Object -First 1
$locLine = $headers | Where-Object { $_ -match '^(?i)location:' } | Select-Object -First 1
if ($statusLine -match ' 30[1237]' -and $locLine -match '__auth/login') {
  Write-Ok "未登录访问跳转登录页（$($locLine -replace '^(?i)location:\s*','')）"
} elseif ($statusLine -match ' 200') {
  Write-Warn2 '未登录访问返回 200：请人工确认是否出现登录页，访问控制可能被削弱。'
} elseif ($statusLine) {
  Write-Warn2 "未登录访问返回：$($statusLine.Trim())，请人工核对。"
} else {
  Write-Warn2 '无法探测线上状态（curl 不可用或网络受限）。'
}

Write-Step '发布完成'
Write-Ok "提交：$HeadAfter　部署：$deployId"
Write-Ok "生产站：https://$ProjectName.pages.dev/"
Write-Warn2 '别忘了在 CHANGELOG 的当天条目中记录本次部署编号（若尚未写入）。'
