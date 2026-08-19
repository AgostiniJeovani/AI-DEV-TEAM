[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$CheckOnly,
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceAgents = Join-Path $repoRoot "agents"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$codexAgents = Join-Path $codexHome "agents"

function Get-NormalizedPath([string]$PathValue) {
    return [System.IO.Path]::GetFullPath($PathValue).TrimEnd("\")
}

if (-not (Test-Path -LiteralPath $sourceAgents -PathType Container)) {
    throw "Agent source directory not found: $sourceAgents"
}

if (-not (Test-Path -LiteralPath $codexHome -PathType Container)) {
    if ($CheckOnly) {
        throw "Codex directory not found: $codexHome"
    }
    New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
}

$sourceFullPath = Get-NormalizedPath $sourceAgents
$destinationItem = Get-Item -LiteralPath $codexAgents -Force -ErrorAction SilentlyContinue

if ($null -ne $destinationItem) {
    if ($destinationItem.LinkType -ne "Junction") {
        throw "Destination already exists and is not a junction: $codexAgents. No files were changed."
    }

    $targetValue = @($destinationItem.Target)[0]
    $targetFullPath = Get-NormalizedPath $targetValue
    if ($targetFullPath -ne $sourceFullPath) {
        throw "Existing junction points to '$targetFullPath', but '$sourceFullPath' was expected. No files were changed."
    }

    Write-Output "Junction already configured: $codexAgents -> $sourceAgents"
}
elseif ($CheckOnly) {
    throw "Junction not found: $codexAgents"
}
else {
    if ($PSCmdlet.ShouldProcess($codexAgents, "Criar junction para $sourceAgents")) {
        New-Item -ItemType Junction -Path $codexAgents -Target $sourceAgents | Out-Null
        Write-Output "Junction created: $codexAgents -> $sourceAgents"
    }
}

if (-not $SkipValidation) {
    $validator = Join-Path $PSScriptRoot "validate-agents.py"
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $python) {
        Write-Warning "Python not found; the junction was checked, but TOML validation was not run."
    }
    else {
        & $python.Source $validator
        if ($LASTEXITCODE -ne 0) {
            throw "Agent validation failed with exit code $LASTEXITCODE."
        }
    }
}
