#!/usr/bin/env bash
set -e

if [ ! -d venv ]; then
  echo "venv not found. Run setup_env.sh first" >&2
  exit 1
fi

. venv/bin/activate
pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing
