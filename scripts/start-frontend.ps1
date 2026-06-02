param(
    [string]$HostAddress = '127.0.0.1',
    [int]$Port = 5173
)

$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\common.ps1"

$projectRoot = Get-MonettoProjectRoot
$frontendRoot = Join-Path $projectRoot 'monettoF'
$npm = Get-MonettoNpm

if (Test-MonettoPortListening -Port $Port) {
    Write-Host "Frontend ya esta escuchando en http://$HostAddress`:$Port"
    return
}

Set-Location $frontendRoot

$viteCommand = Join-Path $frontendRoot 'node_modules\.bin\vite.cmd'
if (-not (Test-Path $viteCommand)) {
    Write-Host "Instalando dependencias del frontend..."
    & $npm install
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo npm install."
    }
}

Write-Host "Frontend listo:"
Write-Host "  App: http://$HostAddress`:$Port"
Write-Host ""
Write-Host "Para detenerlo: Ctrl+C"

& $npm run dev -- --host $HostAddress --port $Port
