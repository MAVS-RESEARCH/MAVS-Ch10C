from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file


def test_metric_inputs_are_frozen() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = build_reproducibility_metrics(repo_root)
    variance_manifest = load_json_config(
        repo_root / "results" / "variance_benchmarks" / "variance_dataset_manifest.json"
    )

    assert manifest["status"] == "pass"
    assert manifest["metrics_read_only_frozen_variance_datasets"] is True
    assert manifest["training_performed"] is False
    assert manifest["metric_definitions_selected_from_audit"] is False
    assert manifest["source_variance_manifest_hash"] == variance_manifest["variance_dataset_manifest_hash"]
    assert manifest["paired_pure_mavs_baselines"] == [
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
    ]
    assert manifest["locked_audit_consistency"]["metric_families_match"] is True
    assert manifest["locked_audit_consistency"]["systems_match"] is True
    assert manifest["locked_audit_consistency"]["paired_baselines_match"] is True
    for artifact_name, digest in manifest["artifact_hashes"].items():
        filename = _artifact_filename(artifact_name)
        assert sha256_file(repo_root / "results" / "stability_metrics" / filename) == digest
    persisted = json.loads(
        (repo_root / "results" / "stability_metrics" / "reproducibility_metric_manifest.json").read_text()
    )
    assert persisted["reproducibility_metric_manifest_hash"] == manifest["reproducibility_metric_manifest_hash"]


def _artifact_filename(artifact_name: str) -> str:
    return {
        "locked_metric_rows": "locked_metric_rows.csv",
        "audit_metric_rows": "audit_metric_rows.csv",
        "accuracy_variance": "accuracy_variance.csv",
        "f1_variance": "f1_variance.csv",
        "prediction_stability": "prediction_stability.csv",
        "decision_stability": "decision_stability.csv",
        "consensus_stability": "consensus_stability.csv",
        "trace_stability": "trace_stability.csv",
        "run_to_run_agreement": "run_to_run_agreement.csv",
        "confidence_interval_widths": "confidence_interval_widths.csv",
    }[artifact_name]
