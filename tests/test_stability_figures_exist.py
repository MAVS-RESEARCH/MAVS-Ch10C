from __future__ import annotations

from pathlib import Path

from mavs_ch10c.reporting.reproducibility_report import (
    build_reproducibility_report,
    load_report_config,
)


def test_stability_figures_exist() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_report(repo_root)
    config = load_report_config(repo_root)

    for figure_path in config["figure_paths"].values():
        path = repo_root / figure_path
        assert path.exists(), figure_path
        assert path.stat().st_size > 1000
        with path.open("rb") as handle:
            assert handle.read(8) == b"\x89PNG\r\n\x1a\n"
