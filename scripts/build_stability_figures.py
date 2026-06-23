from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.reporting.figures import build_stability_figures
from mavs_ch10c.reporting.reproducibility_report import load_report_config
from mavs_ch10c.reporting.tables import build_report_tables


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase 5 stability figures")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    # console.log: phase5 stability figure script begins.
    console.log(f"phase5.script.build_stability_figures.start repo_root={repo_root}")
    config = load_report_config(repo_root)
    tables = build_report_tables(repo_root, config)
    build_stability_figures(repo_root, config, tables)
    # console.log: phase5 stability figure script completed.
    console.log("phase5.script.build_stability_figures.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
