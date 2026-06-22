from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_consensus_stability_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(repo_root / "results" / "stability_metrics" / "consensus_stability.csv")

    assert rows
    governance_rows = [row for row in rows if row["system_id"] in {"pure_mavs_gc", "veto_mavs"}]
    baseline_rows = [row for row in rows if row["system_id"] not in {"pure_mavs_gc", "veto_mavs"}]
    assert governance_rows
    assert baseline_rows
    assert all(row["consensus_applicability"] == "governance_consensus_R" for row in governance_rows)
    assert all(row["consensus_field"] == "R" for row in governance_rows)
    assert all(0.0 <= float(row["consensus_pairwise_stability"]) <= 1.0 for row in governance_rows)
    assert all(
        row["consensus_applicability"] == "not_applicable_baseline_probability_score"
        for row in baseline_rows
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
