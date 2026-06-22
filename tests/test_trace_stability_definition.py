from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_trace_stability_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(repo_root / "results" / "stability_metrics" / "trace_stability.csv")

    assert rows
    assert {row["system_id"] for row in rows} == {"pure_mavs_gc", "veto_mavs"}
    assert {row["trace_field"] for row in rows} == {
        "s",
        "r",
        "z",
        "a",
        "w",
        "m",
        "theta",
        "R",
        "hard_veto",
        "decision",
    }
    assert all(0.0 <= float(row["field_exact_repeat_rate"]) <= 1.0 for row in rows)
    assert all(0.0 <= float(row["exact_trace_hash_repeat_rate"]) <= 1.0 for row in rows)
    assert all(0.0 <= float(row["normalized_trace_similarity"]) <= 1.0 for row in rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
