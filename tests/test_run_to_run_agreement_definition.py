from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics


def test_run_to_run_agreement_definition() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_metrics(repo_root)
    rows = _read_rows(repo_root / "results" / "stability_metrics" / "run_to_run_agreement.csv")

    assert rows
    assert {row["agreement_target"] for row in rows} == {"decision", "correctness"}
    assert all(0.0 <= float(row["binary_pairwise_agreement"]) <= 1.0 for row in rows)
    for row in rows:
        if row["kappa_agreement"]:
            assert -1.0 <= float(row["kappa_agreement"]) <= 1.0


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
