$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\common.ps1"

$projectRoot = Get-MonettoProjectRoot
$backendScript = Join-Path $PSScriptRoot 'start-backend.ps1'
$frontendScript = Join-Path $PSScriptRoot 'start-frontend.ps1'
$powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
if (-not (Test-Path $powershell)) {
    $powershell = (Get-Command powershell.exe -ErrorAction Stop).Source
}

[void](Repair-MonettoNodePath)

Start-Process -FilePath $powershell `
    -ArgumentList "-NoExit -NoProfile -ExecutionPolicy Bypass -File `"$backendScript`"" `
    -WorkingDirectory $projectRoot

Start-Process -FilePath $powershell `
    -ArgumentList "-NoExit -NoProfile -ExecutionPolicy Bypass -File `"$frontendScript`"" `
    -WorkingDirectory $projectRoot

Write-Host "Monetto se esta levantando en dos ventanas:"
Write-Host "  Backend:  http://127.0.0.1:8000/docs"
Write-Host "  Frontend: http://127.0.0.1:5173"
Write-Host ""
Write-Host "Si una ventana dice que el puerto ya esta en uso, ese servicio ya estaba arriba."
