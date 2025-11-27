#!/usr/bin/env bash
set -e

python_exec=$(command -v python || true)
if [ -z "$python_exec" ]; then
  echo "Python is not found. Install Python 3.8+" >&2
  exit 1
fi

version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ $(python - <<'PY'
import sys
v = sys.version_info
print(v.major >= 3 and v.major > 3 or (v.major == 3 and v.minor >= 8))
PY
) != "True" ]]; then
  echo "Python 3.8+ required" >&2
  exit 1
fi

if [ ! -d venv ]; then
  python -m venv venv
fi

. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo "Environment setup complete. Activate venv: source venv/bin/activate"
