# Wrapper the scheduled task calls. Runs sky_watch.py and appends its
# output to logs/sky-watch.log with a run marker, so a failure or a
# forgotten run is visible later (Concept: "an unattended loop fails
# unattended too -- write a line every run").
$ErrorActionPreference = "Continue"
$env:NASA_API_KEY = "wLEJV71WX5JGpOK4PbkhaKSzHw7nVYRifzX5UWtr"
$root = Split-Path -Parent $PSScriptRoot
$log = Join-Path $root "logs\sky-watch.log"
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Add-Content -Path $log -Value "----- run at $stamp -----"
try {
    $output = python "$root\scripts\sky_watch.py" 2>&1
    Add-Content -Path $log -Value $output
} catch {
    Add-Content -Path $log -Value "FAILED: $_"
}
