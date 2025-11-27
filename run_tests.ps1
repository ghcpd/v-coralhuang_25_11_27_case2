# Run tests with coverage reporting for Windows PowerShell
# Usage: .\run_tests.ps1

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Running Agent Tools Tests" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

Write-Host "Running pytest with coverage..." -ForegroundColor Yellow
Write-Host ""

pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing --cov-report=html

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Test execution completed" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Coverage report generated in: htmlcov\index.html" -ForegroundColor Green
Write-Host ""
