#!/usr/bin/env bash
set -euo pipefail

echo "Checking Python version..."
PYTHON_BIN=${PYTHON_BIN:-python3}
VERSION=$($PYTHON_BIN --version 2>&1)
if [[ $? -ne 0 ]]; then
  echo "Python is not installed or not on PATH" >&2
  exit 1
fi
MAJOR=$(echo "$VERSION" | awk '{print $2}' | cut -d. -f1)
MINOR=$(echo "$VERSION" | awk '{print $2}' | cut -d. -f2)
if [[ $MAJOR -lt 3 || ( $MAJOR -eq 3 && $MINOR -lt 8 ) ]]; then
  echo "Python 3.8+ is required. Found $MAJOR.$MINOR" >&2
  exit 1
fi

echo "Python version OK: $MAJOR.$MINOR"

if [[ ! -d .venv ]]; then
  echo "Creating virtual environment (.venv)..."
  $PYTHON_BIN -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements-dev.txt

echo "Environment setup complete."
