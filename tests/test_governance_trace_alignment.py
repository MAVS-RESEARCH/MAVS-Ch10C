from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def test_governance_trace_alignment() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_variance_benchmark_dataset(repo_root)

    for mode in ["locked", "audit"]:
        path = repo_root / "results" / "variance_benchmarks" / f"{mode}_variance_rows.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = [dict(row) for row in csv.DictReader(handle)]
        governance_rows = [
            row for row in rows if row["system_id"] in {"veto_mavs", "pure_mavs_gc"}
        ]
        baseline_rows = [
            row for row in rows if row["system_id"] not in {"veto_mavs", "pure_mavs_gc"}
        ]
        assert governance_rows
        assert all(row["trace_hash"] for row in governance_rows)
        assert all(row["trace_schema_hash"] for row in governance_rows)
        assert all(row["governance_trace_complete"] == "True" for row in governance_rows)
        assert all(row["trace_hash"] == "" for row in baseline_rows)
