param([string]$python = "python")
Write-Host "Setting up environment and running tests..."
powershell -ExecutionPolicy Bypass -File .\setup_env.ps1 -python $python
powershell -ExecutionPolicy Bypass -File .\run_tests.ps1 -python $python
