from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_confidence_interval_width_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(
        repo_root / "results" / "stability_metrics" / "confidence_interval_widths.csv"
    )

    assert rows
    assert {row["compared_metric"] for row in rows} == {"accuracy", "f1"}
    assert all(row["confidence_method"] == "analytical_repeated_unit_normal" for row in rows)
    assert all(float(row["confidence_level"]) == 0.95 for row in rows)
    assert all(float(row["confidence_interval_width"]) >= 0.0 for row in rows)
    assert all(row["ci_width_comparison_to_pure"] for row in rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
