from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase 3 variance benchmark dataset")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase3 variance benchmark script begins.
    console.log(f"phase3.script.build_variance_benchmark.start repo_root={repo_root}")
    build_variance_benchmark_dataset(repo_root)
    # console.log: phase3 variance benchmark script completed.
    console.log("phase3.script.build_variance_benchmark.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
