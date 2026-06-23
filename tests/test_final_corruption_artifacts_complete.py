from __future__ import annotations

from pathlib import Path

import pandas as pd

from mavs_ch10c.verification.hash_utils import load_json_config


def test_final_corruption_artifacts_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_json_config(repo_root / "configs" / "experiments" / "corruption_reproducibility.yaml")
    execution = load_json_config(repo_root / config["output_paths"]["execution_manifest"])
    metric = load_json_config(repo_root / config["output_paths"]["metric_manifest"])
    variance = pd.read_csv(repo_root / config["output_paths"]["variance_tables"], dtype=str)
    stability = pd.read_csv(repo_root / config["output_paths"]["stability_tables"], dtype=str)
    trace = pd.read_csv(repo_root / config["output_paths"]["trace_stability_tables"], dtype=str)

    assert execution["status"] == "pass"
    assert metric["status"] == "pass"
    assert execution["matrix_manifest"]["expected_expanded_run_rows"] == 3628800
    assert set(variance["corruption_family"]) == set(config["families"])
    assert set(float(value) for value in variance["corruption_level"].unique()) == set(config["levels"])
    assert set(config["confidence_metrics"]).issubset(set(stability["metric_name"]))
    assert set(trace["trace_field"]) == set(config["trace_fields"])

