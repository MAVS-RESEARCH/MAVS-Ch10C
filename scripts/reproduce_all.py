from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.verification.final_verification import reproduce_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 7 final reproduction and verification")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument(
        "--run-mode",
        choices=["final"],
        default="final",
        help="Phase 7 run mode",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase7 reproduce-all script begins.
    console.log(f"phase7.script.reproduce_all.start repo_root={repo_root} run_mode={args.run_mode}")
    reproduce_all(repo_root, args.run_mode, sys.argv)
    # console.log: phase7 reproduce-all script completed.
    console.log("phase7.script.reproduce_all.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

