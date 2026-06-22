from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mavs_ch10c import console
from mavs_ch10c.execution.corpus_writer import run_repetition_corpus


def main() -> int:
    parser = argparse.ArgumentParser(description="Run locked Phase 2 repetition corpus")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument(
        "--execution-mode",
        choices=["manifest", "final"],
        default="manifest",
        help="Corpus execution mode",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    config_path = repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml"
    # console.log: phase2 locked corpus script begins.
    console.log(
        "phase2.script.run_locked_repetition_corpus.start "
        f"repo_root={repo_root} execution_mode={args.execution_mode}"
    )
    run_repetition_corpus(repo_root, config_path, args.execution_mode, sys.argv)
    # console.log: phase2 locked corpus script completed.
    console.log("phase2.script.run_locked_repetition_corpus.complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
