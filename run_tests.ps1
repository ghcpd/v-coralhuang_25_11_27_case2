# Run Tests Script (PowerShell)
# Activates virtual environment and runs pytest with coverage

Write-Host "=== Running Tests ===" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found. Please run setup_env.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Run tests with coverage
Write-Host "`nRunning tests with coverage..." -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Gray

pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing --cov-report=html

$exitCode = $LASTEXITCODE

Write-Host "`n" + ("=" * 60) -ForegroundColor Gray

if ($exitCode -eq 0) {
    Write-Host "`n✓ All tests passed!" -ForegroundColor Green
    Write-Host "`nCoverage report saved to: htmlcov/index.html" -ForegroundColor Yellow
} else {
    Write-Host "`n✗ Some tests failed" -ForegroundColor Red
    exit $exitCode
}
