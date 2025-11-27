param([string]$python = "python")
.\venv\Scripts\Activate
.\venv\Scripts\python.exe -m pytest tests -v
