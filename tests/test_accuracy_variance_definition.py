from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_accuracy_variance_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(repo_root / "results" / "stability_metrics" / "accuracy_variance.csv")

    assert rows
    assert {row["run_mode"] for row in rows} == {"locked", "audit"}
    assert {row["metric_family"] for row in rows} == {"accuracy_variance"}
    assert {
        row["aggregation_grain"] for row in rows
    } == {"dataset_system_split_init_composition", "dataset_system_composition"}
    assert all(float(row["sample_variance"]) >= 0.0 for row in rows)
    assert all(float(row["standard_deviation"]) >= 0.0 for row in rows)
    assert all(0.0 <= float(row["mean_value"]) <= 1.0 for row in rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
