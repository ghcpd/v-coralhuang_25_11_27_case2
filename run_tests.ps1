$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    Write-Error "Virtual environment not found. Run ./setup_env.ps1 first."
    exit 1
}

Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Running pytest with coverage..."
pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
