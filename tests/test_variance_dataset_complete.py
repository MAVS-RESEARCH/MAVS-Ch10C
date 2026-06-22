from __future__ import annotations

import csv
import json
from pathlib import Path

from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def test_variance_dataset_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = build_variance_benchmark_dataset(repo_root)

    assert manifest["status"] == "pass"
    assert manifest["source_backend"] == "empirical_sklearn_repeated_training"
    assert manifest["locked"]["row_count"] == 324000
    assert manifest["audit"]["row_count"] == 129600
    assert manifest["locked"]["aligned_group_count"] == 64800
    assert manifest["audit"]["aligned_group_count"] == 25920
    assert manifest["delta_row_count"] == 362880
    assert manifest["missing_units"] == []
    assert manifest["empirical_prediction_available"] is True
    assert len(manifest["variance_dataset_manifest_hash"]) == 64

    output_dir = repo_root / "results" / "variance_benchmarks"
    assert _row_count(output_dir / "locked_variance_rows.csv") == 324000
    assert _row_count(output_dir / "audit_variance_rows.csv") == 129600
    assert _row_count(output_dir / "system_delta_rows.csv") == 362880

    persisted = json.loads((output_dir / "variance_dataset_manifest.json").read_text())
    assert persisted["status"] == "pass"
    assert persisted["delta_row_count"] == 362880


def _row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))
