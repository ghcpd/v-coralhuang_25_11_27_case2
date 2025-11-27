import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path so `src` is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
