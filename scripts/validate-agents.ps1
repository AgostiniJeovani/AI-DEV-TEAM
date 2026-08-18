$ErrorActionPreference = "Stop"
python (Join-Path $PSScriptRoot "validate-agents.py")
exit $LASTEXITCODE
