# PowerShell script to run tests with coverage
if (-not (Test-Path -Path .\venv)) {
    Write-Host "venv not found. Run setup_env.ps1 first" -ForegroundColor Yellow
    exit 1
}

. .\venv\Scripts\Activate
pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
