# launch_servers.ps1 — start research-intranet (8765) and tennis-unified (8766)
# as TRULY detached, no-console, long-lived processes. They survive the parent
# .bat exiting because they're created via WMI Win32_Process.Create with no
# console association, no WindowStyle, no parent-job linkage.
#
# Tennis-Unified uses a custom Range-aware HTTP server (serve.py) so that
# HTML5 <video> tags in the Coach Video Library can seek/scrub. Python's
# stock `http.server` does NOT support Range requests and videos fail to load.

$ErrorActionPreference = 'Stop'

$py          = 'D:\Github Repos\research-intranet\.venv\Scripts\python.exe'
$researchDir = 'D:\Github Repos\research-intranet\site'
$tennisDir   = 'D:\New Tennis Knowledge\Tennis Knowledge\Tennis-Unified'
$servePy     = 'D:\New Tennis Knowledge\Tennis Knowledge\Tennis-Unified\serve.py'
$port1       = 8765
$port2       = 8766

# Sanity checks
foreach ($path in @($py, $researchDir, $tennisDir, $servePy)) {
  if (-not (Test-Path $path)) {
    Write-Host "FATAL: missing path: $path"
    exit 1
  }
}

# Build a properly-quoted CommandLine. WMI passes it as a single string to
# CreateProcess, so embedded double-quotes survive. The directory path MUST be
# wrapped in double-quotes otherwise python's argparse splits on the space in
# "Github Repos" and dies with "unrecognized arguments: Repos\...".
function Launch-Server {
  param([string]$Exe, [string]$Dir, [int]$Port, [string]$Tag, [string]$ExtraArg)
  if ($ExtraArg) {
    $cmdLine = "`"$Exe`" `"$ExtraArg`" --port $Port --directory `"$Dir`""
  } else {
    $cmdLine = "`"$Exe`" -m http.server $Port --directory `"$Dir`""
  }
  Write-Host "Launching ${Tag}: $cmdLine"
  $proc = Invoke-WmiMethod -Path 'Win32_Process' -Name Create `
              -ArgumentList $cmdLine -ErrorAction Stop
  if ($proc.ReturnValue -ne 0) {
    Write-Host "WMI Create failed for $Tag (ReturnValue=$($proc.ReturnValue))"
    return $null
  }
  return $proc.ProcessId
}

$pid1 = Launch-Server -Exe $py -Dir $researchDir -Port $port1 -Tag 'research-intranet'
$pid2 = Launch-Server -Exe $py -Dir $tennisDir   -Port $port2 -Tag 'tennis-unified' -ExtraArg $servePy

if (-not $pid1 -or -not $pid2) { exit 1 }

# Wait up to 15s for both ports to bind
$deadline = (Get-Date).AddSeconds(15)
$ok1 = $ok2 = $false
while ((Get-Date) -lt $deadline) {
  if (-not $ok1) {
    $c = Get-NetTCPConnection -LocalPort $port1 -State Listen -ErrorAction SilentlyContinue
    if ($c) { $ok1 = $true; Write-Host "Port $port1 bound (PID $($c.OwningProcess))" }
  }
  if (-not $ok2) {
    $c = Get-NetTCPConnection -LocalPort $port2 -State Listen -ErrorAction SilentlyContinue
    if ($c) { $ok2 = $true; Write-Host "Port $port2 bound (PID $($c.OwningProcess))" }
  }
  if ($ok1 -and $ok2) { break }
  Start-Sleep -Seconds 1
}

if (-not $ok1 -or -not $ok2) {
  Write-Host ""
  Write-Host "One or more servers failed to bind within 15s."
  if (-not $ok1) { Write-Host "  - port $port1 (research-intranet) NOT listening" }
  if (-not $ok2) { Write-Host "  - port $port2 (tennis-unified)    NOT listening" }
  # Check if our PIDs are still alive
  foreach ($pid in @($pid1, $pid2)) {
    if ($pid) {
      $p = Get-CimInstance Win32_Process -Filter "ProcessId=$pid" -ErrorAction SilentlyContinue
      if ($p) { Write-Host "    PID $pid still running" } else { Write-Host "    PID $pid DIED" }
    }
  }
  exit 1
}

Write-Host "Both servers up. PIDs: research=$pid1, tennis=$pid2"
exit 0
