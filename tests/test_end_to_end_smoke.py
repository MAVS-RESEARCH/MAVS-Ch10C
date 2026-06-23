from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_phase7_reproduce_all_final_succeeds() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/reproduce_all.py", "--run-mode", "final"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "phase7.reproduce_all.complete" in completed.stdout

