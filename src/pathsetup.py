# src/pathsetup.py
# One-time bootstrap: make the repo root importable so
# `from config.settings import ...` and `from src.xxx import ...` work
# regardless of how the entry point is invoked.
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)