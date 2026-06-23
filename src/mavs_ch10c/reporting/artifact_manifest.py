"""Phase 5 reproducibility artifact manifest builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.reporting import REQUIRED_FIGURES, REQUIRED_REPORT_TABLES
from mavs_ch10c.reporting.figures import figure_hashes
from mavs_ch10c.reporting.tables import table_hashes
from mavs_ch10c.verification.hash_utils import (
    hash_relative_files,
    load_json_config,
    sha256_file,
    sha256_json,
    write_json,
)

REPORTING_CODE_PATHS = [
    "configs/reports/reproducibility_report.yaml",
    "src/mavs_ch10c/reporting/__init__.py",
    "src/mavs_ch10c/reporting/tables.py",
    "src/mavs_ch10c/reporting/figures.py",
    "src/mavs_ch10c/reporting/reproducibility_report.py",
    "src/mavs_ch10c/reporting/artifact_manifest.py",
    "scripts/build_variance_tables.py",
    "scripts/build_stability_figures.py",
    "scripts/build_reproducibility_report.py",
    "scripts/build_reproducibility_manifest.py",
]

LOCAL_PROTOCOL_PATHS = [
    "configs/reproducibility/seed_registry.yaml",
    "configs/reproducibility/split_schedules.yaml",
    "configs/reproducibility/init_schedules.yaml",
    "configs/reproducibility/specialist_compositions.yaml",
    "configs/reproducibility/repetition_grid.yaml",
    "configs/experiments/ch10c_reproducibility.yaml",
    "configs/experiments/locked_repetition_corpus.yaml",
    "configs/experiments/audit_repetition_corpus.yaml",
    "configs/experiments/reproducibility_metrics.yaml",
]


def build_reproducibility_manifest(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    """Build the Phase 5 reproducibility artifact manifest."""

    # console.log: phase5 reproducibility artifact manifest build begins.
    console.log("phase5.artifact_manifest.build.start")
    _require_phase5_outputs(repo_root, config)
    foundation = load_json_config(repo_root / config["input_paths"]["foundation_manifest"])
    repetition_grid = load_json_config(repo_root / config["input_paths"]["repetition_grid_manifest"])
    locked_corpus = load_json_config(repo_root / config["input_paths"]["locked_corpus_manifest"])
    audit_corpus = load_json_config(repo_root / config["input_paths"]["audit_corpus_manifest"])
    variance = load_json_config(repo_root / config["input_paths"]["variance_manifest"])
    metrics = load_json_config(repo_root / config["input_paths"]["metric_manifest"])
    report_path = repo_root / config["output_paths"]["report"]
    manifest_body = {
        "phase": "phase5_reproducibility_report",
        "status": "pass",
        "report_version": config["report_version"],
        "source_document_references": config["source_document_references"],
        "import_source_commits": {
            "ch10a": foundation["ch10a"]["commit"],
            "ch10b": foundation["ch10b"]["commit"],
        },
        "dataset_hashes": foundation["ch10a"]["dataset_config_hashes"],
        "split_schedule_hashes": {
            "local_split_schedule_config": sha256_file(
                repo_root / "configs" / "reproducibility" / "split_schedules.yaml"
            ),
            "imported_ch10a_split_protocol": foundation["ch10a"]["protocol_hashes"][
                "src/mavs_ch10a/data/splits.py"
            ],
        },
        "seed_registry_hashes": {
            "local_seed_registry_config": sha256_file(
                repo_root / "configs" / "reproducibility" / "seed_registry.yaml"
            ),
            "locked_corpus_seed_registry": locked_corpus["seed_registry_hash"],
            "audit_corpus_seed_registry": audit_corpus["seed_registry_hash"],
        },
        "initialization_schedule_hashes": {
            "local_initialization_schedule_config": sha256_file(
                repo_root / "configs" / "reproducibility" / "init_schedules.yaml"
            )
        },
        "composition_hashes": {
            "local_specialist_composition_config": sha256_file(
                repo_root / "configs" / "reproducibility" / "specialist_compositions.yaml"
            )
        },
        "model_config_hashes": foundation["ch10a"]["specialist_config_hashes"],
        "system_config_hashes": foundation["ch10a"]["system_config_hashes"],
        "governance_source_hashes": foundation["ch10a"]["governance_hashes"],
        "local_protocol_hashes": hash_relative_files(repo_root, LOCAL_PROTOCOL_PATHS),
        "corpus_hashes": {
            "repetition_grid_manifest_hash": repetition_grid["grid_hash"],
            "locked_corpus_manifest_hash": locked_corpus["corpus_manifest_hash"],
            "audit_corpus_manifest_hash": audit_corpus["corpus_manifest_hash"],
            "locked_corpus_artifacts": locked_corpus["artifact_hashes"],
            "audit_corpus_artifacts": audit_corpus["artifact_hashes"],
        },
        "variance_dataset_hashes": {
            "variance_dataset_manifest_hash": variance["variance_dataset_manifest_hash"],
            "artifact_hashes": variance["artifact_hashes"],
        },
        "metric_table_hashes": {
            "reproducibility_metric_manifest_hash": metrics[
                "reproducibility_metric_manifest_hash"
            ],
            "artifact_hashes": metrics["artifact_hashes"],
        },
        "report_table_hashes": table_hashes(repo_root, config),
        "figure_hashes": figure_hashes(repo_root, config),
        "report_hash": sha256_file(report_path),
        "reporting_code_hashes": hash_relative_files(repo_root, REPORTING_CODE_PATHS),
        "config_hash": sha256_file(repo_root / "configs" / "reports" / "reproducibility_report.yaml"),
        "analysis_rules": config["analysis_rules"],
        "final_run_classification": {
            "locked": "final_frozen_repeated_execution",
            "audit": "final_independent_audit_repeated_execution",
            "exploratory_results_used": False,
            "training_diagnostics_used_as_final_evidence": False,
        },
        "report_claim_policy": {
            "every_claim_references_artifacts": True,
            "negative_neutral_mixed_results_preserved": True,
            "global_superiority_claim_made": False,
            "corruption_robustness_claim_made": False,
        },
    }
    manifest_body["reproducibility_artifact_manifest_hash"] = sha256_json(manifest_body)
    output_path = repo_root / config["output_paths"]["artifact_manifest"]
    write_json(output_path, manifest_body)
    # console.log: phase5 reproducibility artifact manifest build completed.
    console.log(
        "phase5.artifact_manifest.build.complete "
        f"hash={manifest_body['reproducibility_artifact_manifest_hash']}"
    )
    return manifest_body


def _require_phase5_outputs(repo_root: Path, config: dict[str, Any]) -> None:
    missing: list[str] = []
    for name in REQUIRED_REPORT_TABLES:
        path = repo_root / config["output_paths"][name]
        if not path.exists():
            missing.append(str(path))
    for name in REQUIRED_FIGURES:
        path = repo_root / config["figure_paths"][name]
        if not path.exists():
            missing.append(str(path))
    report_path = repo_root / config["output_paths"]["report"]
    if not report_path.exists():
        missing.append(str(report_path))
    if missing:
        raise RuntimeError(f"Cannot build Phase 5 artifact manifest; missing outputs: {missing}")
