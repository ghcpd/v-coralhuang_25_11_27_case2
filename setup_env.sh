#!/usr/bin/env bash
set -euo pipefail

PY=${1:-python3}
echo "Checking Python version"
${PY} --version

echo "Creating venv..."
${PY} -m venv venv
echo "Activating and installing dependencies..."
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo "Done. Activate the environment with: source venv/bin/activate"
