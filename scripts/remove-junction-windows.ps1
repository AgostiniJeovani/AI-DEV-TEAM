[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceAgents = [System.IO.Path]::GetFullPath((Join-Path $repoRoot "agents")).TrimEnd("\")
$codexAgents = Join-Path (Join-Path $env:USERPROFILE ".codex") "agents"
$destinationItem = Get-Item -LiteralPath $codexAgents -Force -ErrorAction SilentlyContinue

if ($null -eq $destinationItem) {
    Write-Output "Nenhuma junction encontrada em $codexAgents"
    exit 0
}

if ($destinationItem.LinkType -ne "Junction") {
    throw "O destino existe, mas não é uma junction. Nenhum arquivo foi removido: $codexAgents"
}

$targetValue = @($destinationItem.Target)[0]
$targetFullPath = [System.IO.Path]::GetFullPath($targetValue).TrimEnd("\")
if ($targetFullPath -ne $sourceAgents) {
    throw "A junction aponta para '$targetFullPath', não para '$sourceAgents'. Nenhum arquivo foi removido."
}

if ($CheckOnly) {
    Write-Output "Junction compatível encontrada: $codexAgents -> $sourceAgents"
    exit 0
}

if ($PSCmdlet.ShouldProcess($codexAgents, "Remover somente a junction")) {
    Remove-Item -LiteralPath $codexAgents
    Write-Output "Junction removida. Os arquivos fonte em $sourceAgents foram preservados."
}
