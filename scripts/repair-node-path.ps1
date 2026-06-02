$ErrorActionPreference = 'Stop'

. "$PSScriptRoot\common.ps1"

if (-not (Repair-MonettoNodePath)) {
    throw "No encontre Node/npm en C:\Program Files\nodejs. Instala Node.js LTS y vuelve a ejecutar este script."
}

$npm = Get-MonettoNpm
$version = & $npm --version

Write-Host "npm listo. Version: $version"
Write-Host "Abre una terminal nueva si la actual todavia no reconoce npm."
