from __future__ import annotations

from pathlib import Path

from mavs_ch10c.execution.corpus_writer import run_repetition_corpus


def test_locked_corpus_manifest_schema() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = run_repetition_corpus(
        repo_root,
        repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml",
        "manifest",
        ["pytest", "test_locked_corpus_manifest_schema"],
    )

    assert manifest["status"] == "pass"
    assert manifest["run_mode"] == "locked"
    assert manifest["execution_backend"] == "empirical_sklearn_repeated_training"
    assert manifest["empirical_prediction_available"] is True
    assert manifest["row_count"] == 36000
    assert manifest["prediction_row_count"] == 324000
    assert manifest["pre_execution_run_manifest_count"] == 36000
    assert manifest["run_manifest_count"] == 36000
    assert manifest["governance_trace_count"] == 129600
    assert manifest["model_fit_count"] == 5400
    assert len(manifest["corpus_manifest_hash"]) == 64
    assert manifest["tuning_performed"] is False
    assert manifest["final_claims_from_training_diagnostics"] is False
    assert set(manifest["artifact_hashes"]) == {
        "corpus_index",
        "predictions_index",
        "trace_index",
        "specialist_metadata",
        "frozen_run_manifests",
        "run_manifests",
    }
    assert len(manifest["experiment_config_hash"]) == 64
    assert manifest["execution_code_hashes"]
    assert manifest["foundation_source_hash_contract"]["specialist_config_hashes"]
    assert len(manifest["repetition_grid_manifest_hash"]) == 64
    assert len(manifest["seed_registry_hash"]) == 64
