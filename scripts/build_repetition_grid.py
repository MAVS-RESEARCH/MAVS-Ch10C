from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.execution.controller import build_and_write_repetition_grid


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Chapter 10C repetition grid")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument(
        "--run-mode",
        choices=["locked", "audit", "all"],
        default="all",
        help="Run mode to expand",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase1 build repetition grid script begins.
    console.log(
        f"phase1.script.build_repetition_grid.start repo_root={repo_root} run_mode={args.run_mode}"
    )
    build_and_write_repetition_grid(repo_root, args.run_mode, sys.argv)
    # console.log: phase1 build repetition grid script completed.
    console.log("phase1.script.build_repetition_grid.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
