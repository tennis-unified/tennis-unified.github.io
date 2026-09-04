# launch_taichi.ps1 — start the Taichi Health and Finance Intranet on port 8767
# as a fully-detached process via WMI Win32_Process.Create.
#
# The standalone Taichi paths don't contain spaces, but every argument is quoted
# defensively to match the rest of the launcher's behavior and avoid future
# breakage if the directory is ever moved to a path with spaces.

$ErrorActionPreference = 'Stop'

$py       = 'C:\Users\Phamd\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe'
$server   = 'D:\Taichi-Health-Finance\Intranet\serve.py'
$docroot  = 'D:\Taichi-Health-Finance\Intranet\docs'
$port     = 8767
$url      = 'http://localhost:8767/'

# Sanity checks
foreach ($path in @($py, $server, $docroot)) {
  if (-not (Test-Path $path)) {
    Write-Host "FATAL: missing path: $path"
    exit 1
  }
}

# Kill any leftover process on this port
$existing = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
  Write-Host "Port $port already bound by PID $($existing.OwningProcess) - killing it"
  Stop-Process -Id $existing.OwningProcess -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 500
}

# Build CommandLine with all path-like args quoted
function Quote-If-Spaces { param([string]$s) if ($s -match '\s') { "`"$s`"" } else { $s } }
$cmdLine = "$(Quote-If-Spaces $py) $(Quote-If-Spaces $server) --port $port --directory $(Quote-If-Spaces $docroot)"
Write-Host "Launching: $cmdLine"

$proc = Invoke-WmiMethod -Path 'Win32_Process' -Name Create -ArgumentList $cmdLine -ErrorAction Stop
if ($proc.ReturnValue -ne 0) {
  Write-Host "WMI Create failed (ReturnValue=$($proc.ReturnValue))"
  exit 1
}
Write-Host "PID: $($proc.ProcessId)"

# Wait up to 15s for the port to bind.
# Use BOTH Get-NetTCPConnection and netstat fallback — on some Windows sessions
# Get-NetTCPConnection returns null transiently, causing a false-negative that
# makes us incorrectly report "did not bind" even though the server is fine.
$deadline = (Get-Date).AddSeconds(15)
$bound = $false
while ((Get-Date) -lt $deadline) {
  $ownerPid = $null
  $c = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
  if ($c) { $ownerPid = $c.OwningProcess }
  if (-not $ownerPid) {
    # Fallback: parse netstat -ano
    $line = netstat -ano 2>$null | Select-String ":${port}\s+.*LISTENING" | Select-Object -First 1
    if ($line) {
      $tokens = ($line -split '\s+') | Where-Object { $_ -ne '' }
      # netstat columns: Proto LocalAddress ForeignAddress State PID
      $ownerPid = $tokens[-1]
    }
  }
  if ($ownerPid) {
    $bound = $true
    Write-Host "Port $port bound by PID $ownerPid"
    break
  }
  Start-Sleep -Seconds 1
}

if (-not $bound) {
  Write-Host "WARNING: server did not bind within 15s."
  $stillAlive = Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.ProcessId)" -ErrorAction SilentlyContinue
  if ($stillAlive) {
    Write-Host "        PID $($proc.ProcessId) is still running but not listening on $port."
  } else {
    Write-Host "        PID $($proc.ProcessId) died. Check serve.py / directory contents."
  }
  exit 1
}

Write-Host ""
Write-Host "Taichi server running at $url"
exit 0
