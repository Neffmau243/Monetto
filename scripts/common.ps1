$ErrorActionPreference = 'Stop'

function Get-MonettoProjectRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

function Add-MonettoPathPart {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathPart
    )

    $parts = @()
    if ($env:Path) {
        $parts = $env:Path -split ';' | Where-Object { $_ -and $_.Trim() }
    }

    if ($parts -notcontains $PathPart) {
        $env:Path = ($PathPart, $env:Path) -join ';'
    }
}

function Repair-MonettoNodePath {
    $nodeDir = 'C:\Program Files\nodejs'
    $npmPath = Join-Path $nodeDir 'npm.cmd'

    if (-not (Test-Path $npmPath)) {
        return $false
    }

    Add-MonettoPathPart -PathPart $nodeDir

    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $userParts = @()
    if ($userPath) {
        $userParts = $userPath -split ';' | Where-Object { $_ -and $_.Trim() }
    }

    if ($userParts -notcontains $nodeDir) {
        try {
            $newUserPath = ($userParts + $nodeDir) -join ';'
            [Environment]::SetEnvironmentVariable('Path', $newUserPath, 'User')
            Write-Host "Node agregado al PATH de usuario: $nodeDir"
        }
        catch {
            Write-Warning "No pude guardar Node en el PATH de usuario, pero lo active para esta ventana."
        }
    }

    return $true
}

function Get-MonettoNpm {
    [void](Repair-MonettoNodePath)

    $npmCommand = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($npmCommand) {
        return $npmCommand.Source
    }

    $fallback = 'C:\Program Files\nodejs\npm.cmd'
    if (Test-Path $fallback) {
        return $fallback
    }

    throw "No encontre npm. Instala Node.js LTS desde https://nodejs.org y vuelve a abrir la terminal."
}

function Test-MonettoPortListening {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port
    )

    try {
        $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    }
    catch {
        $connection = $null
    }

    return [bool]$connection
}
