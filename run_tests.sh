#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  echo "Virtual environment not found. Run ./setup_env.sh first." >&2
  exit 1
fi

source .venv/bin/activate

pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
