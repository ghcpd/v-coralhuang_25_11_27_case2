#!/usr/bin/env bash
set -euo pipefail
venv_name=${1:-venv}
python3 -m venv "$venv_name"
source "$venv_name/bin/activate"
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo "Environment setup complete. Activate with: source $venv_name/bin/activate"
