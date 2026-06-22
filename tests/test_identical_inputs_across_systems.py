from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def test_identical_inputs_across_systems() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_variance_benchmark_dataset(repo_root)

    for mode in ["locked", "audit"]:
        path = repo_root / "results" / "variance_benchmarks" / f"{mode}_variance_rows.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = [dict(row) for row in csv.DictReader(handle)]
        groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            groups[row["alignment_group_hash"]].append(row)
        for group in groups.values():
            assert len({row["specialist_output_hash"] for row in group}) == 1
            assert len({row["probability_matrix_hash"] for row in group}) == 1
            assert len({row["row_hash"] for row in group}) == 1
            assert len({row["label_hash"] for row in group}) == 1
            assert len({row["label"] for row in group}) == 1
