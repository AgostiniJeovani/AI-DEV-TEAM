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
    throw "Diretório fonte de agentes não encontrado: $sourceAgents"
}

if (-not (Test-Path -LiteralPath $codexHome -PathType Container)) {
    if ($CheckOnly) {
        throw "Diretório do Codex não encontrado: $codexHome"
    }
    New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
}

$sourceFullPath = Get-NormalizedPath $sourceAgents
$destinationItem = Get-Item -LiteralPath $codexAgents -Force -ErrorAction SilentlyContinue

if ($null -ne $destinationItem) {
    if ($destinationItem.LinkType -ne "Junction") {
        throw "Destino já existe e não é uma junction: $codexAgents. Nenhum arquivo foi alterado."
    }

    $targetValue = @($destinationItem.Target)[0]
    $targetFullPath = Get-NormalizedPath $targetValue
    if ($targetFullPath -ne $sourceFullPath) {
        throw "Junction existente aponta para '$targetFullPath', mas o esperado é '$sourceFullPath'. Nenhum arquivo foi alterado."
    }

    Write-Output "Junction já configurada: $codexAgents -> $sourceAgents"
}
elseif ($CheckOnly) {
    throw "Junction não encontrada: $codexAgents"
}
else {
    if ($PSCmdlet.ShouldProcess($codexAgents, "Criar junction para $sourceAgents")) {
        New-Item -ItemType Junction -Path $codexAgents -Target $sourceAgents | Out-Null
        Write-Output "Junction criada: $codexAgents -> $sourceAgents"
    }
}

if (-not $SkipValidation) {
    $validator = Join-Path $PSScriptRoot "validate-agents.py"
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $python) {
        Write-Warning "Python não encontrado; a junction foi verificada, mas a validação TOML não foi executada."
    }
    else {
        & $python.Source $validator
        if ($LASTEXITCODE -ne 0) {
            throw "A validação dos agentes falhou com código $LASTEXITCODE."
        }
    }
}

