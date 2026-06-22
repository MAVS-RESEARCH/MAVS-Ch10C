"""Command line interface for MAVS Chapter 10C Phase 1."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mavs_ch10c import console
from mavs_ch10c.execution.controller import (
    build_and_write_repetition_grid,
    import_foundation,
)
from mavs_ch10c.execution.corpus_writer import run_repetition_corpus
from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MAVS Chapter 10C utilities")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "import-foundation",
        help="Locate and validate Chapter 10A and Chapter 10B foundations",
    )

    grid_parser = subparsers.add_parser(
        "build-repetition-grid",
        help="Build the Phase 1 repetition grid",
    )
    grid_parser.add_argument(
        "--run-mode",
        choices=["locked", "audit", "all"],
        default="all",
        help="Run mode to expand",
    )
    corpus_parser = subparsers.add_parser(
        "run-repetition-corpus",
        help="Run a Phase 2 locked or audit repeated-execution corpus",
    )
    corpus_parser.add_argument(
        "--config",
        required=True,
        help="Phase 2 corpus experiment config path",
    )
    corpus_parser.add_argument(
        "--execution-mode",
        choices=["manifest", "final"],
        default="manifest",
        help="Corpus execution mode",
    )
    subparsers.add_parser(
        "build-variance-benchmark-dataset",
        help="Build the Phase 3 variance benchmark dataset",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    command_line = sys.argv if argv is None else ["mavs-ch10c", *argv]

    # console.log: phase1 CLI dispatch begins.
    console.log(f"phase1.cli.dispatch command={args.command} repo_root={repo_root}")
    if args.command == "import-foundation":
        import_foundation(repo_root, command_line)
    elif args.command == "build-repetition-grid":
        build_and_write_repetition_grid(repo_root, args.run_mode, command_line)
    elif args.command == "run-repetition-corpus":
        run_repetition_corpus(
            repo_root,
            (repo_root / args.config).resolve(),
            args.execution_mode,
            command_line,
        )
    elif args.command == "build-variance-benchmark-dataset":
        build_variance_benchmark_dataset(repo_root)
    else:
        raise ValueError(f"Unhandled command: {args.command}")
    # console.log: phase1 CLI dispatch completed.
    console.log(f"phase1.cli.dispatch.complete command={args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
