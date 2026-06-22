from __future__ import annotations

import csv
import json
from pathlib import Path

from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset


def test_static_weighted_ensemble_uses_imported_frozen_config_policy() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_variance_benchmark_dataset(repo_root)
    manifest = json.loads(
        (repo_root / "results" / "variance_benchmarks" / "variance_dataset_manifest.json").read_text()
    )
    assert manifest["static_weight_policy"] == "imported_frozen_ch10a_config"

    rows = _read_rows(repo_root / "results" / "variance_benchmarks" / "locked_variance_rows.csv")
    static_rows = [row for row in rows if row["system_id"] == "static_weighted_ensemble"]
    assert len(static_rows) == 64800
    assert all(row["system_config_hash"] for row in static_rows)
    assert all(row["source_backend"] == "empirical_sklearn_repeated_training" for row in static_rows)
    assert all(row["empirical_prediction_available"] == "true" for row in static_rows)

    delta_rows = _read_rows(repo_root / "results" / "variance_benchmarks" / "system_delta_rows.csv")
    assert any(row["baseline_system_id"] == "static_weighted_ensemble" for row in delta_rows)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
