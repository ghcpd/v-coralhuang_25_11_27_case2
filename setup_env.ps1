param([string]$python = "python")

Write-Host "Checking Python version..."
$verOut = & $python --version 2>&1
Write-Host $verOut
if ($LASTEXITCODE -ne 0) { Write-Error "Python not found"; exit 1 }

Write-Host "Creating virtual environment..."
& $python -m venv .\venv
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to create venv"; exit 1 }

Write-Host "Installing dependencies..."
.\venv\Scripts\Activate; pip install -U pip; pip install -r requirements.txt; pip install -r requirements-dev.txt

Write-Host "Done. Activate the environment with: .\venv\Scripts\Activate" 
