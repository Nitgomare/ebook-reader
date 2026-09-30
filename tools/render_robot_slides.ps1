param([string]$JobPath = "$PSScriptRoot/../resource-inventory/robot-technology-basics/render-job.json")
$ErrorActionPreference = 'Stop'
$jobs = Get-Content -LiteralPath $JobPath -Raw -Encoding UTF8 | ConvertFrom-Json
$app = New-Object -ComObject PowerPoint.Application
try {
    foreach ($job in $jobs) {
        New-Item -ItemType Directory -Path $job.destination -Force | Out-Null
        $deck = $null
        try {
            # Read-only, no presentation window; export never runs macros or linked media.
            $deck = $app.Presentations.Open($job.source, -1, 0, 0)
            for ($i = 1; $i -le $deck.Slides.Count; $i++) {
                $target = Join-Path $job.destination ('{0:0000}.jpg' -f $i)
                if (-not (Test-Path -LiteralPath $target)) {
                    $deck.Slides.Item($i).Export($target, 'JPG', 1600, [int](1600 * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth))
                }
            }
            Write-Output "$($job.id): $($deck.Slides.Count) slides"
        } finally { if ($null -ne $deck) { $deck.Close() } }
    }
} finally { $app.Quit() }
