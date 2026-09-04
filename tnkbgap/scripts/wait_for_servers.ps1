# wait_for_servers.ps1 — poll two local HTTP endpoints until both respond 200,
# or until the timeout (seconds) elapses. Returns exit 0 on success, 1 on timeout.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File wait_for_servers.ps1 -Port1 8765 -Port2 8766 -TimeoutSec 15
[CmdletBinding()]
param(
    [int]$Port1 = 8765,
    [int]$Port2 = 8766,
    [int]$TimeoutSec = 15
)
$deadline = (Get-Date).AddSeconds($TimeoutSec)
while ((Get-Date) -lt $deadline) {
    $ok = $true
    foreach ($port in @($Port1, $Port2)) {
        try {
            $null = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 "http://localhost:$port/" -ErrorAction Stop
        } catch {
            $ok = $false
        }
    }
    if ($ok) { exit 0 }
    Start-Sleep -Seconds 1
}
Write-Host "Servers did not come up within $TimeoutSec seconds."
exit 1
