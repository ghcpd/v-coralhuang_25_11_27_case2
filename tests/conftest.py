import sys
import os

# Ensure the project's src directory is importable as a package
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, ROOT)
    sys.path.insert(0, SRC)
