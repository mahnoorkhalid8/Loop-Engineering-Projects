# Wrapper the scheduled task calls. Appends output to logs/paper-watch.log
# with a run marker (see Sky Watch's identical pattern in Project 3).
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$log = Join-Path $root "logs\paper-watch.log"
New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Add-Content -Path $log -Value "----- run at $stamp -----"
try {
    $output = python "$root\scripts\paper_watch.py" "LLM agents" 2>&1
    Add-Content -Path $log -Value $output
} catch {
    Add-Content -Path $log -Value "FAILED: $_"
}
