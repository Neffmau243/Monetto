param(
    [string]$HostAddress = '127.0.0.1',
    [int]$Port = 8000,
    [switch]$SkipMigrations
)

$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\common.ps1"

$projectRoot = Get-MonettoProjectRoot
$venvPath = Join-Path $projectRoot '.venv'
$python = Join-Path $venvPath 'Scripts\python.exe'

function New-MonettoVenv {
    $pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pythonLauncher) {
        & $pythonLauncher.Source -3.11 -m venv $venvPath
        if ($LASTEXITCODE -eq 0) {
            return
        }

        & $pythonLauncher.Source -3 -m venv $venvPath
        if ($LASTEXITCODE -eq 0) {
            return
        }
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        throw "No encontre Python. Instala Python 3.11+ y vuelve a ejecutar este script."
    }

    & $pythonCommand.Source -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "No pude crear el entorno virtual de Python."
    }
}

if (Test-MonettoPortListening -Port $Port) {
    Write-Host "Backend ya esta escuchando en http://$HostAddress`:$Port"
    Write-Host "Swagger: http://$HostAddress`:$Port/docs"
    return
}

Set-Location $projectRoot

if (-not (Test-Path $python)) {
    Write-Host "Creando entorno virtual en .venv..."
    New-MonettoVenv
}

$readyStamp = Join-Path $venvPath '.monetto-ready'
$pyproject = Join-Path $projectRoot 'pyproject.toml'
$needsInstall = -not (Test-Path $readyStamp)

& $python -m pip show uvicorn *> $null
if ($LASTEXITCODE -ne 0) {
    $needsInstall = $true
}

if ((Test-Path $readyStamp) -and (Test-Path $pyproject)) {
    if ((Get-Item $pyproject).LastWriteTimeUtc -gt (Get-Item $readyStamp).LastWriteTimeUtc) {
        $needsInstall = $true
    }
}

if ($needsInstall) {
    Write-Host "Instalando dependencias del backend..."
    & $python -m pip install -e '.[dev]'
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo la instalacion de dependencias Python."
    }
    New-Item -Path $readyStamp -ItemType File -Force | Out-Null
}

if (-not $SkipMigrations) {
    Write-Host "Aplicando migraciones..."
    & $python -m alembic upgrade head
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo alembic upgrade head. Revisa que MySQL este activo y que la base exista."
    }
}

Write-Host "Backend listo:"
Write-Host "  API:     http://$HostAddress`:$Port/api"
Write-Host "  Swagger: http://$HostAddress`:$Port/docs"
Write-Host ""
Write-Host "Para detenerlo: Ctrl+C"

& $python -m uvicorn app.main:app --reload --host $HostAddress --port $Port
