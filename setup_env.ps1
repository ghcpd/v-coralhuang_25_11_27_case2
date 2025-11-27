param(
    [string]$venvName = "venv"
)

Write-Host "Checking Python version..."
$py = python -c "import sys;print(sys.version_info[:3])" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python not found. Install Python 3.8+"
    exit 1
}

Write-Host "Creating virtual environment $venvName..."
python -m venv $venvName
Write-Host "Activating virtual environment and installing deps..."
& "$venvName/Scripts/Activate.ps1"; pip install -r requirements.txt; pip install -r requirements-dev.txt
Write-Host "Environment setup complete. Activate with: .\$venvName\Scripts\Activate.ps1"
