# Setup Python Environment Script (PowerShell)
# Checks Python version, creates virtual environment, and installs dependencies

Write-Host "=== Python Environment Setup ===" -ForegroundColor Cyan

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $majorVersion = [int]$Matches[1]
        $minorVersion = [int]$Matches[2]
        
        if (($majorVersion -eq 3) -and ($minorVersion -ge 8)) {
            Write-Host "✓ Python 3.8+ detected" -ForegroundColor Green
        } else {
            Write-Host "✗ Python 3.8+ required. Found: Python $majorVersion.$minorVersion" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Removing old environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

python -m venv venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling production dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Production dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install production dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "`nInstalling development dependencies..." -ForegroundColor Yellow
pip install -r requirements-dev.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Development dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install development dependencies" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "✓ Python environment ready" -ForegroundColor Green
Write-Host "`nTo activate the environment manually, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`nTo run tests, execute:" -ForegroundColor Yellow
Write-Host "  .\run_tests.ps1" -ForegroundColor White
