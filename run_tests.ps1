param(
    [string]$venvName = "venv"
)

if (-Not (Test-Path "$venvName/Scripts/Activate.ps1")) {
    Write-Error "Virtual env not found. Run .\setup_env.ps1 first."
    exit 1
}

& "$venvName/Scripts/Activate.ps1"; pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
