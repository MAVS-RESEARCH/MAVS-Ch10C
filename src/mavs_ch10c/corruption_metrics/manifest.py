"""Phase 6 corruption manifest builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import hash_relative_files, sha256_file, sha256_json, write_json

PHASE6_CODE_PATHS = [
    "configs/experiments/corruption_reproducibility.yaml",
    "configs/corruption/ch10b_corruption_suite.yaml",
    "src/mavs_ch10c/corruption/__init__.py",
    "src/mavs_ch10c/corruption/ch10b_suite.py",
    "src/mavs_ch10c/corruption/corruption_matrix.py",
    "src/mavs_ch10c/corruption/corruption_runner.py",
    "src/mavs_ch10c/corruption/corruption_writer.py",
    "src/mavs_ch10c/corruption/cache.py",
    "src/mavs_ch10c/corruption_metrics/__init__.py",
    "src/mavs_ch10c/corruption_metrics/variance.py",
    "src/mavs_ch10c/corruption_metrics/stability.py",
    "src/mavs_ch10c/corruption_metrics/confidence.py",
    "src/mavs_ch10c/corruption_metrics/trace.py",
    "src/mavs_ch10c/corruption_metrics/reporting.py",
    "src/mavs_ch10c/corruption_metrics/manifest.py",
    "scripts/build_corruption_reproducibility_corpus.py",
    "scripts/build_corruption_reproducibility_tables.py",
    "scripts/build_corruption_stability_figures.py",
    "scripts/build_corruption_reproducibility_report.py",
]


def write_corruption_execution_manifest(
    repo_root: Path,
    config: dict[str, Any],
    suite: dict[str, Any],
    matrix_manifest: dict[str, Any],
    corpus_outputs: dict[str, Any],
) -> dict[str, Any]:
    """Write the Phase 6 corruption execution manifest."""

    # console.log: phase6 corruption execution manifest write begins.
    console.log("phase6.manifest.execution.start")
    manifest = {
        "phase": "phase6_corruption_aware_reproducibility",
        "status": "pass",
        "suite_hash": suite["suite_hash"],
        "ch10b_grid_manifest_payload_hash": suite["ch10b_grid_manifest_payload_hash"],
        "family_config_hashes": suite["family_config_hashes"],
        "corruption_families": suite["families"],
        "corruption_levels": suite["levels"],
        "matrix_manifest": matrix_manifest,
        "source_corpus_hashes": {
            run_mode: sha256_file(repo_root / path)
            for run_mode, path in config["source_corpus_paths"].items()
        },
        "source_prediction_hashes": {
            run_mode: sha256_file(repo_root / path)
            for run_mode, path in config["source_prediction_paths"].items()
        },
        "source_trace_hashes": {
            run_mode: sha256_file(repo_root / path)
            for run_mode, path in config["source_trace_paths"].items()
        },
        "summary_row_count": len(corpus_outputs["summary_rows"]),
        "trace_summary_row_count": len(corpus_outputs["trace_rows"]),
        "clean_anchor_level": 0.0,
        "locked_audit_separation_preserved": True,
        "training_performed": False,
        "hyperparameter_search_performed": False,
        "threshold_tuning_after_corruption_performed": False,
        "governance_policy_modified": False,
        "audit_used_to_select_metrics_or_language": False,
        "corruption_application_mode": "deterministic_projection_over_frozen_phase2_benchmark_outputs",
    }
    manifest["corruption_execution_manifest_hash"] = sha256_json(manifest)
    write_json(repo_root / config["output_paths"]["execution_manifest"], manifest)
    # console.log: phase6 corruption execution manifest write completed.
    console.log(
        "phase6.manifest.execution.complete "
        f"hash={manifest['corruption_execution_manifest_hash']}"
    )
    return manifest


def write_corruption_metric_manifest(
    repo_root: Path,
    config: dict[str, Any],
    suite: dict[str, Any],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Write the Phase 6 corruption metric manifest after all artifacts exist."""

    # console.log: phase6 corruption metric manifest write begins.
    console.log("phase6.manifest.metric.start")
    metric_manifest_relative_path = config["output_paths"]["metric_manifest"]
    artifact_paths = [
        relative_path
        for relative_path in list(config["output_paths"].values()) + list(config["figure_paths"].values())
        if relative_path != metric_manifest_relative_path
    ]
    artifact_hashes = {
        relative_path: sha256_file(repo_root / relative_path)
        for relative_path in artifact_paths
        if (repo_root / relative_path).exists()
    }
    missing = [relative_path for relative_path in artifact_paths if relative_path not in artifact_hashes]
    if missing:
        raise RuntimeError(f"Cannot write Phase 6 metric manifest; missing artifacts: {missing}")
    manifest = {
        "phase": "phase6_corruption_metrics",
        "status": "pass",
        "suite_hash": suite["suite_hash"],
        "execution_manifest_hash": execution_manifest["corruption_execution_manifest_hash"],
        "artifact_hashes": artifact_hashes,
        "code_hashes": hash_relative_files(repo_root, PHASE6_CODE_PATHS),
        "families": config["families"],
        "levels": config["levels"],
        "variance_metrics": config["variance_metrics"],
        "stability_metrics": config["stability_metrics"],
        "confidence_metrics": config["confidence_metrics"],
        "trace_fields": config["trace_fields"],
        "claim_policy": {
            "all_claims_reference_artifacts": True,
            "negative_neutral_mixed_results_preserved": config[
                "negative_neutral_mixed_results_preserved"
            ],
            "global_validation_claim_made": False,
            "clean_phase5_metrics_rewritten": False,
        },
        "training_performed": False,
        "hyperparameter_search_performed": False,
        "threshold_tuning_after_corruption_performed": False,
        "governance_policy_modified": False,
    }
    manifest["metric_manifest_path"] = metric_manifest_relative_path
    manifest["corruption_metric_manifest_hash"] = sha256_json(manifest)
    write_json(repo_root / metric_manifest_relative_path, manifest)
    # console.log: phase6 corruption metric manifest write completed.
    console.log(
        "phase6.manifest.metric.complete "
        f"hash={manifest['corruption_metric_manifest_hash']}"
    )
    return manifest
