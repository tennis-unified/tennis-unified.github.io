# launch_3_intranets.ps1 — start 3 detached web servers for the local intranet bundle:
#   8765  Tennis Knowledge Gap Intranet     (python -m http.server, MkDocs site)
#   8766  Tennis-Unified Library            (Range-aware serve.py with TP-Archive-Site)
#   8767  Taichi Health and Finance        (Range-aware serve.py with Intranet/docs)
#
# All servers are spawned via WMI Win32_Process.Create so they're fully detached
# from any parent console. The launcher script can exit immediately and the
# server processes survive.
#
# IMPORTANT: Every path that contains a space ("Github Repos", "New Tennis
# Knowledge\Tennis Knowledge") MUST be wrapped in literal double-quotes in the
# CommandLine. Otherwise python's argparse / serve.py's argparse will split the
# path on the space and fail with "unrecognized arguments".

$ErrorActionPreference = 'Stop'

$py = 'C:\Users\Phamd\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe'

$servers = @(
  @{
    Name      = 'Tennis Knowledge Gap Intranet'
    Port      = 8765
    Exe       = $py
    PreArgs   = @('-m', 'http.server', '8765')
    PostArgs  = @('--directory', 'D:\Github Repos\research-intranet\site')
    UrlRoot   = 'http://localhost:8765/'
  },
  @{
    Name      = 'Tennis-Unified Library'
    Port      = 8766
    Exe       = $py
    PreArgs   = @('D:\New Tennis Knowledge\Tennis Knowledge\Tennis-Unified\serve.py', '--port', '8766')
    PostArgs  = @('--directory', 'D:\New Tennis Knowledge\Tennis Knowledge\Tennis-Unified')
    UrlRoot   = 'http://localhost:8766/TP-Archive-Site/'
  },
  @{
    Name      = 'Taichi Health and Finance Intranet'
    Port      = 8767
    Exe       = $py
    PreArgs   = @('D:\Taichi-Health-Finance\Intranet\serve.py', '--port', '8767')
    PostArgs  = @('--directory', 'D:\Taichi-Health-Finance\Intranet\docs')
    UrlRoot   = 'http://localhost:8767/'
  }
)

# Sanity checks
if (-not (Test-Path $py)) {
  Write-Host "FATAL: python not found at $py"
  exit 1
}

# Build the CommandLine for one server, quoting anything that contains a space
function Quote-If-Spaces { param([string]$s) if ($s -match '\s') { "`"$s`"" } else { $s } }
function Format-CmdLine {
  param([string]$Exe, [string[]]$PreArgs, [string[]]$PostArgs)
  $parts = @()
  $parts += Quote-If-Spaces $Exe
  foreach ($a in $PreArgs) { $parts += Quote-If-Spaces $a }
  foreach ($a in $PostArgs) { $parts += Quote-If-Spaces $a }
  return ($parts -join ' ')
}

# Get-NetTCPConnection returns null transiently on some Windows sessions; fall
# back to netstat -ano parsing for robustness.
function Get-PortOwner {
  param([int]$Port)
  $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  if ($conn) { return $conn.OwningProcess }
  $line = netstat -ano 2>$null | Select-String ":${Port}\s+.*LISTENING" | Select-Object -First 1
  if ($line) {
    $tokens = ($line -split '\s+') | Where-Object { $_ -ne '' }
    return $tokens[-1]
  }
  return $null
}

# Kill any leftover process on these ports
foreach ($port in 8765, 8766, 8767) {
  $owner = Get-PortOwner -Port $port
  if ($owner) {
    Write-Host "Port $port already bound by PID $owner - killing it"
    Stop-Process -Id $owner -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
  }
}

# Launch each server via WMI
$launched = @()
foreach ($s in $servers) {
  $cmdLine = Format-CmdLine -Exe $s.Exe -PreArgs $s.PreArgs -PostArgs $s.PostArgs
  Write-Host "[$($s.Port)] $($s.Name)"
  Write-Host "        CMD: $cmdLine"
  $proc = Invoke-WmiMethod -Path 'Win32_Process' -Name Create -ArgumentList $cmdLine -ErrorAction Stop
  if ($proc.ReturnValue -ne 0) {
    Write-Host "        FAILED: WMI Create returned $($proc.ReturnValue)"
    exit 1
  }
  Write-Host "        PID: $($proc.ProcessId)"
  $launched += [pscustomobject]@{
    Name    = $s.Name
    Port    = $s.Port
    UrlRoot = $s.UrlRoot
    PID     = $proc.ProcessId
  }
}

# Wait up to 20s for each port to bind.
# Get-PortOwner (defined above) uses BOTH Get-NetTCPConnection and a netstat
# fallback — on some Windows sessions Get-NetTCPConnection returns null
# transiently, causing false-negatives.
$deadline = (Get-Date).AddSeconds(20)
$bound = @{}
while ((Get-Date) -lt $deadline) {
  foreach ($s in $launched) {
    if (-not $bound[$s.Port]) {
      $owner = Get-PortOwner -Port $s.Port
      if ($owner) {
        $bound[$s.Port] = $owner
        Write-Host "        Port $($s.Port) bound by PID $owner"
      }
    }
  }
  if ($bound.Count -eq $launched.Count) { break }
  Start-Sleep -Seconds 1
}

# Report final state
$failed = @()
foreach ($s in $launched) {
  if (-not $bound[$s.Port]) {
    $failed += $s
    Write-Host "        $($s.Port) ($($s.Name)): NOT BOUND"
  }
}
if ($failed.Count -gt 0) {
  Write-Host ""
  Write-Host "WARNING: $($failed.Count) server(s) failed to bind within 20s."
  Write-Host "         Servers that DID bind are still running."
  exit 1
}

Write-Host ""
Write-Host "All 3 intranets are running:"
foreach ($s in $launched) {
  Write-Host "  $($s.Port)  $($s.Name)"
  Write-Host "         $($s.UrlRoot)"
}
exit 0
