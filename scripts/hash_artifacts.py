from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.verification.final_verification import build_artifact_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase 7 artifact inventory")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase7 hash-artifacts script begins.
    console.log(f"phase7.script.hash_artifacts.start repo_root={repo_root}")
    build_artifact_inventory(repo_root)
    # console.log: phase7 hash-artifacts script completed.
    console.log("phase7.script.hash_artifacts.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

