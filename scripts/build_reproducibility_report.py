from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.reporting.reproducibility_report import build_reproducibility_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase 5 reproducibility report")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase5 reproducibility report script begins.
    console.log(f"phase5.script.build_reproducibility_report.start repo_root={repo_root}")
    build_reproducibility_report(repo_root)
    # console.log: phase5 reproducibility report script completed.
    console.log("phase5.script.build_reproducibility_report.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
