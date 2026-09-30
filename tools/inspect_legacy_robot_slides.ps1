param([Parameter(Mandatory=$true)][string]$Source)
$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path -LiteralPath $Source).Path
$auditRoot = Join-Path $PSScriptRoot '../resource-inventory/robot-technology-basics'
$app = New-Object -ComObject PowerPoint.Application
function Read-ShapeText($shape) {
    if ($shape.Type -eq 6) {
        for ($g = 1; $g -le $shape.GroupItems.Count; $g++) { Read-ShapeText $shape.GroupItems.Item($g) }
    } elseif ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
        $shape.TextFrame.TextRange.Text.Trim()
    } elseif ($shape.HasTable -eq -1) {
        for ($r = 1; $r -le $shape.Table.Rows.Count; $r++) {
            for ($c = 1; $c -le $shape.Table.Columns.Count; $c++) { $shape.Table.Cell($r,$c).Shape.TextFrame.TextRange.Text.Trim() }
        }
    }
}
try {
    $reviews = @()
    foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File -Filter '*.ppt') {
        $deck = $null
        try {
            $deck = $app.Presentations.Open($file.FullName, -1, 0, 0)
            $pages = @()
            for ($i = 1; $i -le $deck.Slides.Count; $i++) {
                $parts = @()
                foreach ($shape in $deck.Slides.Item($i).Shapes) { $parts += @(Read-ShapeText $shape) }
                $pages += (($parts -join "`n").Trim())
            }
            $digest = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $relative = $file.FullName.Substring($sourceRoot.Length + 1).Replace('\','/')
            $reviews += [PSCustomObject]@{path=$relative; id=$digest.Substring(0,16); sha256=$digest; title=$file.BaseName; pageCount=$pages.Count; pages=$pages}
            Write-Output "$relative : $($pages.Count) pages"
        } finally { if ($null -ne $deck) { $deck.Close() } }
    }
    $reviews | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $auditRoot 'legacy-ppt-review.json') -Encoding UTF8
} finally { $app.Quit() }
