from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.execution.controller import import_foundation


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Chapter 10A/10B foundations")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase1 import foundation script begins.
    console.log(f"phase1.script.import_foundation.start repo_root={repo_root}")
    import_foundation(repo_root, sys.argv)
    # console.log: phase1 import foundation script completed.
    console.log("phase1.script.import_foundation.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
