# PowerShell script to set up Python venv and install dependencies
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed or not in PATH. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
$version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$version -lt [version]'3.8') {
    Write-Host "Python version must be 3.8 or greater. Found $version" -ForegroundColor Red
    exit 1
}

# Create venv
if (-not (Test-Path -Path .\venv)) {
    python -m venv venv
}

# Activate and install
Set-Location -Path $PWD
. .\venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
Write-Host "Environment setup complete. Activate the venv with: . .\venv\Scripts\Activate" -ForegroundColor Green
