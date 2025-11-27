#!/usr/bin/env bash
set -euo pipefail
venv_name=${1:-venv}
if [ ! -f "$venv_name/bin/activate" ]; then
  echo "Virtualenv not found. Run ./setup_env.sh first."
  exit 1
fi
source "$venv_name/bin/activate"
pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
