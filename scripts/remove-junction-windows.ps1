[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceAgents = [System.IO.Path]::GetFullPath((Join-Path $repoRoot "agents")).TrimEnd("\")
$sourceSkills = Join-Path $repoRoot "skills"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$codexAgents = Join-Path $codexHome "agents"
$codexSkills = Join-Path $codexHome "skills"

function Get-NormalizedPath([string]$PathValue) {
    return [System.IO.Path]::GetFullPath($PathValue).TrimEnd("\")
}

function Get-VerifiedJunction([string]$Destination, [string]$Source, [string]$Label) {
    $item = Get-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return $null
    }
    if ($item.LinkType -ne "Junction") {
        throw "$Label exists but is not a junction. No files were removed: $Destination"
    }
    $targetValue = @($item.Target)[0]
    if ((Get-NormalizedPath $targetValue) -ne (Get-NormalizedPath $Source)) {
        throw "$Label points to '$targetValue', not '$Source'. No files were removed."
    }
    return $item
}

$agentJunction = Get-VerifiedJunction $codexAgents $sourceAgents "Agent destination"
$skillJunctions = @()
if (Test-Path -LiteralPath $sourceSkills -PathType Container) {
    foreach ($skillSource in Get-ChildItem -LiteralPath $sourceSkills -Directory) {
        if (Test-Path -LiteralPath (Join-Path $skillSource.FullName "SKILL.md") -PathType Leaf) {
            $destination = Join-Path $codexSkills $skillSource.Name
            $item = Get-VerifiedJunction $destination $skillSource.FullName "Skill destination '$($skillSource.Name)'"
            if ($null -ne $item) {
                $skillJunctions += $item
            }
        }
    }
}

if ($null -eq $agentJunction -and $skillJunctions.Count -eq 0) {
    Write-Output "No AI-DEV-TEAM junctions found."
    exit 0
}

if ($CheckOnly) {
    if ($null -ne $agentJunction) {
        Write-Output "Compatible agent junction found: $codexAgents -> $sourceAgents"
    }
    foreach ($skillJunction in $skillJunctions) {
        Write-Output "Compatible skill junction found: $($skillJunction.FullName)"
    }
    exit 0
}

# Targets are verified before removal. Removing a junction leaves its source
# directory and every unrelated personal skill intact.
if ($null -ne $agentJunction -and $PSCmdlet.ShouldProcess($codexAgents, "Remove only the verified AI-DEV-TEAM agent junction")) {
    Remove-Item -LiteralPath $codexAgents
    Write-Output "Agent junction removed. Repository files were preserved."
}
foreach ($skillJunction in $skillJunctions) {
    if ($PSCmdlet.ShouldProcess($skillJunction.FullName, "Remove only the verified AI-DEV-TEAM skill junction")) {
        Remove-Item -LiteralPath $skillJunction.FullName
        Write-Output "Skill junction removed: $($skillJunction.FullName)"
    }
}
