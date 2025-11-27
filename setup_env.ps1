$ErrorActionPreference = "Stop"

Write-Host "Checking Python version..."
$pythonVersionOutput = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed or not on PATH."
    exit 1
}
$versionMatches = [regex]::Match($pythonVersionOutput, "Python (\d+)\.(\d+)")
if (-not $versionMatches.Success) {
    Write-Error "Unable to parse Python version from: $pythonVersionOutput"
    exit 1
}
$major = [int]$versionMatches.Groups[1].Value
$minor = [int]$versionMatches.Groups[2].Value
if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
    Write-Error "Python 3.8+ is required. Found $major.$minor"
    exit 1
}
Write-Host "Python version OK: $major.$minor"

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
pip install --upgrade pip

Write-Host "Installing dependencies..."
pip install -r requirements-dev.txt

Write-Host "Environment setup complete."
