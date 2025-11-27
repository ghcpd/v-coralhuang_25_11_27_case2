# Setup environment script for Windows PowerShell
# Checks Python 3.8+, creates venv, and installs dependencies

param(
    [switch]$NoActivate = $false
)

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Agent Tools Refactoring - Environment Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion"

# Verify Python 3.8+
try {
    $versionCheck = python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.8 or higher is required"
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python version check passed" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel > $null 2>&1
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host "✓ Production dependencies installed" -ForegroundColor Green

Write-Host "Installing dev dependencies..." -ForegroundColor Yellow
pip install -q -r requirements-dev.txt
Write-Host "✓ Development dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✓ Environment setup completed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "To run tests, use:" -ForegroundColor Yellow
Write-Host "  .\run_tests.ps1" -ForegroundColor Cyan
Write-Host ""
