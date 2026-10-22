"""Delete all data and reseed the fictional demo story.

Usage (from repo root):  backend/.venv/bin/python scripts/reset_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.db.seed import reset  # noqa: E402
from app.db.session import init_engine, session_scope  # noqa: E402

if __name__ == "__main__":
    init_engine()
    with session_scope() as s:
        reset(s)
    print("Demo data reset.")
