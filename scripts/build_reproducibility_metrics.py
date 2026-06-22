from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase 4 reproducibility metrics")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase4 reproducibility metric script begins.
    console.log(f"phase4.script.build_reproducibility_metrics.start repo_root={repo_root}")
    build_reproducibility_metrics(repo_root, command_line=sys.argv)
    # console.log: phase4 reproducibility metric script completed.
    console.log("phase4.script.build_reproducibility_metrics.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
