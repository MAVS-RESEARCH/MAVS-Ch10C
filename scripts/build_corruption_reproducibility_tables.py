"""Build the Phase 6 corruption reproducibility tables."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.corruption.corruption_writer import build_corruption_reproducibility_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    # console.log: phase6 table script execution begins.
    console.log("phase6.script.tables.start")
    build_corruption_reproducibility_outputs(repo_root, force=args.force)
    # console.log: phase6 table script execution completed.
    console.log("phase6.script.tables.complete")


if __name__ == "__main__":
    main()
