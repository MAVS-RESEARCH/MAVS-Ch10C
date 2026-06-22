from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_prediction_stability_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(repo_root / "results" / "stability_metrics" / "prediction_stability.csv")

    assert rows
    assert {row["run_mode"] for row in rows} == {"locked", "audit"}
    assert {row["metric_family"] for row in rows} == {"prediction_stability"}
    assert all(int(row["pair_count"]) > 0 for row in rows)
    assert all(0.0 <= float(row["binary_pairwise_agreement"]) <= 1.0 for row in rows)
    assert all(0.0 <= float(row["probability_pairwise_stability"]) <= 1.0 for row in rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
