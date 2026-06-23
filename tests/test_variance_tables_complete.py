from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.reporting.reproducibility_report import load_report_config
from mavs_ch10c.reporting.tables import build_report_tables


def test_variance_tables_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_report_config(repo_root)
    tables = build_report_tables(repo_root, config)

    variance_rows = tables["variance_tables"]
    delta_rows = tables["reproducibility_system_deltas"]
    expected = config["expected"]
    assert len(variance_rows) == (
        len(expected["run_modes"])
        * len(expected["datasets"])
        * len(expected["systems"])
        * len(expected["specialist_compositions"])
        * len(expected["variance_metrics"])
    )
    assert {row["metric_name"] for row in variance_rows} == set(expected["variance_metrics"])
    assert {row["run_mode"] for row in variance_rows} == set(expected["run_modes"])
    assert {row["baseline_system_id"] for row in delta_rows} == set(expected["baselines"])
    assert {row["direction_vs_baseline"] for row in delta_rows}

    output_path = repo_root / config["output_paths"]["variance_tables"]
    with output_path.open(newline="", encoding="utf-8") as handle:
        persisted = list(csv.DictReader(handle))
    assert len(persisted) == len(variance_rows)
