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
    Write-Output "No junction found at $codexAgents"
    exit 0
}

if ($destinationItem.LinkType -ne "Junction") {
    throw "The destination exists but is not a junction. No files were removed: $codexAgents"
}

$targetValue = @($destinationItem.Target)[0]
$targetFullPath = [System.IO.Path]::GetFullPath($targetValue).TrimEnd("\")
if ($targetFullPath -ne $sourceAgents) {
    throw "The junction points to '$targetFullPath', not '$sourceAgents'. No files were removed."
}

if ($CheckOnly) {
    Write-Output "Compatible junction found: $codexAgents -> $sourceAgents"
    exit 0
}

if ($PSCmdlet.ShouldProcess($codexAgents, "Remover somente a junction")) {
    Remove-Item -LiteralPath $codexAgents
    Write-Output "Junction removed. Source files in $sourceAgents were preserved."
}
