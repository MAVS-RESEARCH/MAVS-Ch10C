from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def test_system_schedule_alignment() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_variance_benchmark_dataset(repo_root)

    for mode, expected_groups in [("locked", 64800), ("audit", 25920)]:
        rows = _read_rows(
            repo_root / "results" / "variance_benchmarks" / f"{mode}_variance_rows.csv"
        )
        groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            key = (
                row["dataset_id"],
                row["run_mode"],
                row["execution_seed"],
                row["split_schedule_id"],
                row["initialization_schedule_id"],
                row["specialist_composition_id"],
                row["row_id"],
                row["label_hash"],
            )
            groups[key].append(row)
        assert len(groups) == expected_groups
        for group in groups.values():
            assert {row["system_id"] for row in group} == {
                "single_model",
                "mean_ensemble",
                "static_weighted_ensemble",
                "veto_mavs",
                "pure_mavs_gc",
            }


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
