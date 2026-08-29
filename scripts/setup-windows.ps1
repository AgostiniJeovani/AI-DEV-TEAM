[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$CheckOnly,
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceAgents = Join-Path $repoRoot "agents"
$sourceSkills = Join-Path $repoRoot "skills"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$codexAgents = Join-Path $codexHome "agents"
$codexSkills = Join-Path $codexHome "skills"

function Get-NormalizedPath([string]$PathValue) {
    return [System.IO.Path]::GetFullPath($PathValue).TrimEnd("\")
}

function Assert-CompatibleJunction([string]$Destination, [string]$Source, [string]$Label) {
    $item = Get-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return $false
    }
    if ($item.LinkType -ne "Junction") {
        throw "$Label already exists and is not a junction: $Destination. No files were changed."
    }
    $targetValue = @($item.Target)[0]
    if ((Get-NormalizedPath $targetValue) -ne (Get-NormalizedPath $Source)) {
        throw "$Label points to '$targetValue', but '$(Get-NormalizedPath $Source)' was expected. No files were changed."
    }
    return $true
}

if (-not (Test-Path -LiteralPath $sourceAgents -PathType Container)) {
    throw "Agent source directory not found: $sourceAgents"
}
if (-not (Test-Path -LiteralPath $sourceSkills -PathType Container)) {
    throw "Skill source directory not found: $sourceSkills"
}

$skillSources = @(Get-ChildItem -LiteralPath $sourceSkills -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") -PathType Leaf
})
if ($skillSources.Count -eq 0) {
    throw "No skill folders with SKILL.md were found in: $sourceSkills"
}

$codexSkillsItem = Get-Item -LiteralPath $codexSkills -Force -ErrorAction SilentlyContinue
if ($null -ne $codexSkillsItem -and -not $codexSkillsItem.PSIsContainer) {
    throw "Codex skills destination exists and is not a directory: $codexSkills. No files were changed."
}

if (-not (Test-Path -LiteralPath $codexHome -PathType Container)) {
    if ($CheckOnly) {
        throw "Codex directory not found: $codexHome"
    }
    if ($PSCmdlet.ShouldProcess($codexHome, "Create Codex directory")) {
        New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
    }
}

# Preflight every destination before creating anything, so a conflicting user
# folder cannot leave activation partially configured.
$agentsConfigured = Assert-CompatibleJunction $codexAgents $sourceAgents "Agent destination"
$skillConfiguration = @()
foreach ($skillSource in $skillSources) {
    $skillDestination = Join-Path $codexSkills $skillSource.Name
    $configured = Assert-CompatibleJunction $skillDestination $skillSource.FullName "Skill destination '$($skillSource.Name)'"
    $skillConfiguration += [PSCustomObject]@{
        Name = $skillSource.Name
        Source = $skillSource.FullName
        Destination = $skillDestination
        Configured = $configured
    }
}

if ($CheckOnly) {
    if (-not $agentsConfigured) {
        throw "Agent junction not found: $codexAgents"
    }
    $missingSkills = @($skillConfiguration | Where-Object { -not $_.Configured })
    if ($missingSkills.Count -gt 0) {
        throw "Skill junctions not found: $($missingSkills.Name -join ', ')"
    }
    Write-Output "Activation verified: $codexAgents -> $sourceAgents"
    foreach ($skill in $skillConfiguration) {
        Write-Output "Skill verified: $($skill.Destination) -> $($skill.Source)"
    }
}
else {
    if (-not $agentsConfigured -and $PSCmdlet.ShouldProcess($codexAgents, "Create junction for $sourceAgents")) {
        New-Item -ItemType Junction -Path $codexAgents -Target $sourceAgents | Out-Null
        Write-Output "Agent junction created: $codexAgents -> $sourceAgents"
    }
    elseif ($agentsConfigured) {
        Write-Output "Agent junction already configured: $codexAgents -> $sourceAgents"
    }

    if (-not (Test-Path -LiteralPath $codexSkills -PathType Container) -and $PSCmdlet.ShouldProcess($codexSkills, "Create Codex skills directory")) {
        New-Item -ItemType Directory -Path $codexSkills -Force | Out-Null
    }
    foreach ($skill in $skillConfiguration) {
        if (-not $skill.Configured -and $PSCmdlet.ShouldProcess($skill.Destination, "Create junction for $($skill.Source)")) {
            New-Item -ItemType Junction -Path $skill.Destination -Target $skill.Source | Out-Null
            Write-Output "Skill junction created: $($skill.Destination) -> $($skill.Source)"
        }
        elseif ($skill.Configured) {
            Write-Output "Skill junction already configured: $($skill.Destination) -> $($skill.Source)"
        }
    }
}

if (-not $SkipValidation) {
    $validator = Join-Path $PSScriptRoot "validate-agents.py"
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $python) {
        Write-Warning "Python not found; activation was checked, but catalog validation was not run."
    }
    else {
        & $python.Source $validator
        if ($LASTEXITCODE -ne 0) {
            throw "Agent validation failed with exit code $LASTEXITCODE."
        }
    }
}
