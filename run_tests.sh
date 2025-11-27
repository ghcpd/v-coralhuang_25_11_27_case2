#!/usr/bin/env bash
set -euo pipefail
source venv/bin/activate
venv/bin/python -m pytest tests -v
