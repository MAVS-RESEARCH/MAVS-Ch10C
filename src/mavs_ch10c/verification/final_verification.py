"""Phase 7 final artifact inventory and release verification gates."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.corruption.corruption_writer import build_corruption_reproducibility_outputs
from mavs_ch10c.evaluation.aggregation import build_reproducibility_metrics
from mavs_ch10c.execution.corpus_writer import run_repetition_corpus
from mavs_ch10c.execution.dataset_builder import build_partition_bundle
from mavs_ch10c.repeatability.repetition_grid import build_repetition_grid
from mavs_ch10c.repeatability.seed_registry import load_seed_registry
from mavs_ch10c.reporting.reproducibility_report import build_reproducibility_report
from mavs_ch10c.comparison.variance_dataset import build_variance_benchmark_dataset
from mavs_ch10c.verification.hash_utils import (
    canonical_json,
    load_json_config,
    sha256_file,
    sha256_json,
    write_json,
)

REQUIRED_PHASE7_FILES = [
    "scripts/reproduce_all.py",
    "scripts/hash_artifacts.py",
    "scripts/verify_artifacts.py",
    "results/reports/artifact_inventory.json",
    "results/reports/verification_report.md",
    "results/reports/corruption_verification_addendum.md",
    "tests/test_end_to_end_smoke.py",
    "tests/test_artifact_inventory_complete.py",
    "tests/test_final_run_guards.py",
    "tests/test_locked_audit_independence.py",
    "tests/test_no_governance_source_drift.py",
    "tests/test_path_md_complete.py",
    "tests/test_final_corruption_artifacts_complete.py",
    "tests/test_final_corruption_claims_reference_artifacts.py",
]

REQUIRED_FINAL_ARTIFACTS = [
    "WorkPlan.md",
    "Path.md",
    "README.md",
    "pyproject.toml",
    "results/foundation_import/ch10a_import_manifest.json",
    "results/foundation_import/ch10b_import_manifest.json",
    "results/foundation_import/foundation_import_manifest.json",
    "results/run_manifests/repetition_grid.csv",
    "results/run_manifests/repetition_grid_manifest.json",
    "results/execution_corpus/locked/corpus_index.csv",
    "results/execution_corpus/locked/predictions_index.csv",
    "results/execution_corpus/locked/trace_index.csv",
    "results/execution_corpus/locked/corpus_manifest.json",
    "results/execution_corpus/locked/audit_freeze_manifest.json",
    "results/execution_corpus/audit/corpus_index.csv",
    "results/execution_corpus/audit/predictions_index.csv",
    "results/execution_corpus/audit/trace_index.csv",
    "results/execution_corpus/audit/corpus_manifest.json",
    "results/variance_benchmarks/variance_dataset_manifest.json",
    "results/stability_metrics/reproducibility_metric_manifest.json",
    "results/reports/variance_tables.csv",
    "results/reports/stability_tables.csv",
    "results/reports/reproducibility_report.md",
    "results/reports/reproducibility_artifact_manifest.json",
    "results/corruption_reproducibility/corruption_execution_manifest.json",
    "results/corruption_reproducibility/corruption_metric_manifest.json",
    "results/reports/corruption_reproducibility_tables.csv",
    "results/reports/corruption_stability_tables.csv",
    "results/reports/corruption_variance_tables.csv",
    "results/reports/corruption_trace_stability_tables.csv",
    "results/reports/corruption_claim_support_ledger.csv",
    "results/reports/corruption_reproducibility_report.md",
    "results/reports/corruption_verification_addendum.md",
]

REQUIRED_INVENTORY_CATEGORIES = [
    "configs",
    "source_files",
    "tests",
    "scripts",
    "import_manifests",
    "seed_registries",
    "split_schedules",
    "initialization_schedules",
    "composition_manifests",
    "run_manifests",
    "corpus_indexes",
    "variance_datasets",
    "metric_tables",
    "corruption_corpora",
    "corruption_metric_tables",
    "corruption_figures",
    "corruption_reports",
    "figures",
    "reports",
    "path_md",
]

REQUIRED_CLEAN_METRICS = [
    "accuracy_variance",
    "f1_variance",
    "prediction_stability",
    "decision_stability",
    "consensus_stability",
    "trace_stability",
    "run_to_run_agreement",
    "confidence_interval_width",
]

REQUIRED_CORRUPTION_METRICS = [
    "accuracy_variance",
    "f1_variance",
    "rejection_variance",
    "threshold_variance",
    "severity_variance",
    "weight_variance",
    "prediction_stability",
    "decision_stability",
    "consensus_stability",
    "trace_stability",
    "run_to_run_agreement",
    "confidence_interval_width",
    "bootstrap_confidence_interval_width",
]

GOVERNANCE_TRACE_FIELDS = [
    "row_id",
    "dataset_id",
    "run_mode",
    "execution_seed",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
    "system_id",
    "specialist_ids",
    "s",
    "r",
    "z",
    "a",
    "w",
    "m",
    "theta",
    "R",
    "hard_veto",
    "decision",
    "label",
    "config_hash",
    "checkpoint_hashes",
    "trace_hash",
]


@dataclass(frozen=True)
class VerificationCheck:
    check_id: str
    status: str
    evidence: str

    def raise_if_failed(self) -> None:
        if self.status != "pass":
            raise RuntimeError(f"{self.check_id} failed: {self.evidence}")


def reproduce_all(repo_root: Path, run_mode: str, command_line: list[str]) -> dict[str, Any]:
    """Run the Phase 7 one-command reproduction and verification sequence."""

    # console.log: phase7 one-command reproduction begins.
    console.log(f"phase7.reproduce_all.start run_mode={run_mode}")
    if run_mode != "final":
        raise ValueError("Phase 7 reproduce_all currently supports only --run-mode final")
    _validate_foundation_import(repo_root)
    _validate_repetition_grid(repo_root)
    locked_manifest = run_repetition_corpus(
        repo_root,
        repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml",
        "manifest",
        command_line,
    )
    audit_manifest = run_repetition_corpus(
        repo_root,
        repo_root / "configs" / "experiments" / "audit_repetition_corpus.yaml",
        "manifest",
        command_line,
    )
    variance_manifest = build_variance_benchmark_dataset(repo_root)
    metric_manifest = build_reproducibility_metrics(repo_root, command_line=command_line)
    report_result = build_reproducibility_report(repo_root)
    corruption_manifest = build_corruption_reproducibility_outputs(repo_root)
    inventory = build_artifact_inventory(repo_root)
    verification = verify_release_artifacts(repo_root, inventory)
    result = {
        "status": "pass",
        "run_mode": run_mode,
        "locked_corpus_manifest_hash": locked_manifest["corpus_manifest_hash"],
        "audit_corpus_manifest_hash": audit_manifest["corpus_manifest_hash"],
        "variance_dataset_manifest_hash": variance_manifest["variance_dataset_manifest_hash"],
        "metric_manifest_hash": metric_manifest["reproducibility_metric_manifest_hash"],
        "report_hash": report_result["report_hash"],
        "corruption_metric_manifest_hash": corruption_manifest["corruption_metric_manifest_hash"],
        "artifact_inventory_hash": inventory["inventory_payload_hash"],
        "verification_status": verification["overall_status"],
    }
    # console.log: phase7 one-command reproduction completed.
    console.log(
        "phase7.reproduce_all.complete "
        f"inventory_hash={result['artifact_inventory_hash']} status={result['verification_status']}"
    )
    return result


def build_artifact_inventory(repo_root: Path) -> dict[str, Any]:
    """Build the final artifact inventory required by Phase 7."""

    # console.log: phase7 artifact inventory build begins.
    console.log("phase7.inventory.build.start")
    candidate_paths = _inventory_candidate_paths(repo_root)
    entries = [_inventory_entry(repo_root, path) for path in candidate_paths]
    category_counts: dict[str, int] = {}
    for entry in entries:
        category_counts[entry["category"]] = category_counts.get(entry["category"], 0) + 1
    inventory = {
        "phase": "phase7_artifact_inventory",
        "status": "pass",
        "schema_version": "1.0",
        "entry_count": len(entries),
        "category_counts": category_counts,
        "required_categories": REQUIRED_INVENTORY_CATEGORIES,
        "missing_required_categories": [
            category
            for category in REQUIRED_INVENTORY_CATEGORIES
            if category_counts.get(category, 0) == 0
        ],
        "required_artifacts": REQUIRED_FINAL_ARTIFACTS,
        "missing_required_artifacts": [
            path for path in REQUIRED_FINAL_ARTIFACTS if not (repo_root / path).exists()
        ],
        "entries": entries,
        "self_hash_policy": "artifact_inventory.json is excluded from its own hash comparison",
    }
    if inventory["missing_required_categories"] or inventory["missing_required_artifacts"]:
        inventory["status"] = "fail"
    inventory["inventory_payload_hash"] = sha256_json(
        {key: value for key, value in inventory.items() if key != "inventory_payload_hash"}
    )
    write_json(repo_root / "results" / "reports" / "artifact_inventory.json", inventory)
    # console.log: phase7 artifact inventory build completed.
    console.log(
        "phase7.inventory.build.complete "
        f"entries={inventory['entry_count']} hash={inventory['inventory_payload_hash']}"
    )
    return inventory


def verify_release_artifacts(
    repo_root: Path,
    inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run final Phase 7 verification gates and write the verification report."""

    # console.log: phase7 release verification begins.
    console.log("phase7.verify.start")
    inventory = inventory or load_json_config(repo_root / "results" / "reports" / "artifact_inventory.json")
    checks = [
        _check_required_files(repo_root),
        _check_inventory_complete(inventory),
        _check_inventory_hashes(repo_root, inventory),
        _check_governance_source_hashes(repo_root),
        _check_seed_registry(repo_root),
        _check_locked_audit_independence(repo_root),
        _check_split_partitions(repo_root),
        _check_system_and_metric_coverage(repo_root),
        _check_governance_trace_contract(repo_root),
        _check_report_claim_references(repo_root),
        _check_corruption_coverage(repo_root),
        _check_corruption_claim_references(repo_root),
        _check_corruption_clean_anchor(repo_root),
        _check_final_run_guards(repo_root),
        _check_path_md(repo_root),
        _check_corruption_addendum(repo_root),
    ]
    overall_status = "pass" if all(check.status == "pass" for check in checks) else "fail"
    verification = {
        "phase": "phase7_final_verification",
        "overall_status": overall_status,
        "check_count": len(checks),
        "checks": [check.__dict__ for check in checks],
    }
    report = _render_verification_report(verification)
    report_path = repo_root / "results" / "reports" / "verification_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    verification["verification_report_hash"] = sha256_file(report_path)
    if overall_status != "pass":
        raise RuntimeError("Phase 7 final verification failed")
    # console.log: phase7 release verification completed.
    console.log(
        "phase7.verify.complete "
        f"status={overall_status} report_hash={verification['verification_report_hash']}"
    )
    return verification


def _validate_foundation_import(repo_root: Path) -> None:
    # console.log: phase7 foundation import validation begins.
    console.log("phase7.foundation.validate.start")
    foundation = load_json_config(repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json")
    ch10b = load_json_config(repo_root / "results" / "foundation_import" / "ch10b_import_manifest.json")
    if foundation.get("status") != "pass" or ch10b.get("status") != "pass":
        raise RuntimeError("Foundation import manifests must be pass")
    _check_governance_source_hashes(repo_root).raise_if_failed()
    # console.log: phase7 foundation import validation completed.
    console.log("phase7.foundation.validate.complete")


def _validate_repetition_grid(repo_root: Path) -> None:
    # console.log: phase7 repetition-grid validation begins.
    console.log("phase7.repetition_grid.validate.start")
    recorded = load_json_config(repo_root / "results" / "run_manifests" / "repetition_grid_manifest.json")
    computed_units = build_repetition_grid(repo_root, "all")
    if recorded.get("grid_hash") != sha256_json([unit.__dict__ for unit in computed_units]):
        raise RuntimeError("Repetition grid hash mismatch")
    if recorded.get("row_count") != len(computed_units):
        raise RuntimeError("Repetition grid row count mismatch")
    # console.log: phase7 repetition-grid validation completed.
    console.log(f"phase7.repetition_grid.validate.complete rows={len(computed_units)}")


def _inventory_candidate_paths(repo_root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for pattern in [
        "configs/**/*.yaml",
        "src/mavs_ch10c/**/*.py",
        "tests/**/*.py",
        "scripts/*.py",
        "results/foundation_import/*.json",
        "results/run_manifests/*",
        "results/execution_corpus/**/*.csv",
        "results/execution_corpus/**/*manifest.json",
        "results/variance_benchmarks/*",
        "results/stability_metrics/*",
        "results/reports/*",
        "results/figures/*",
        "results/corruption_reproducibility/**/*",
        "WorkPlan.md",
        "Path.md",
        "README.md",
        "pyproject.toml",
    ]:
        candidates.update(path for path in repo_root.glob(pattern) if path.is_file())
    candidates.discard(repo_root / "results" / "reports" / "artifact_inventory.json")
    return sorted(candidates, key=lambda path: path.as_posix())


def _inventory_entry(repo_root: Path, path: Path) -> dict[str, Any]:
    relative_path = path.relative_to(repo_root).as_posix()
    entry = {
        "path": relative_path,
        "category": _categorize(relative_path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "required": relative_path in REQUIRED_FINAL_ARTIFACTS or relative_path in REQUIRED_PHASE7_FILES,
    }
    if path.suffix == ".csv" and path.stat().st_size < 20_000_000:
        entry["row_count"] = _csv_row_count(path)
    return entry


def _categorize(relative_path: str) -> str:
    if relative_path == "Path.md":
        return "path_md"
    if relative_path.startswith("configs/reproducibility/seed_registry"):
        return "seed_registries"
    if relative_path.startswith("configs/reproducibility/split_schedules"):
        return "split_schedules"
    if relative_path.startswith("configs/reproducibility/init_schedules"):
        return "initialization_schedules"
    if relative_path.startswith("configs/reproducibility/specialist_compositions"):
        return "composition_manifests"
    if relative_path.startswith("configs/"):
        return "configs"
    if relative_path.startswith("src/"):
        return "source_files"
    if relative_path.startswith("tests/"):
        return "tests"
    if relative_path.startswith("scripts/"):
        return "scripts"
    if relative_path.startswith("results/foundation_import/"):
        return "import_manifests"
    if relative_path.startswith("results/run_manifests/"):
        return "run_manifests"
    if relative_path.startswith("results/execution_corpus/"):
        return "corpus_indexes"
    if relative_path.startswith("results/variance_benchmarks/"):
        return "variance_datasets"
    if relative_path.startswith("results/stability_metrics/") or relative_path in {
        "results/reports/variance_tables.csv",
        "results/reports/stability_tables.csv",
        "results/reports/reproducibility_system_deltas.csv",
    }:
        return "metric_tables"
    if relative_path.startswith("results/corruption_reproducibility/"):
        return "corruption_corpora"
    if relative_path.startswith("results/reports/corruption_") and relative_path.endswith(".csv"):
        return "corruption_metric_tables"
    if relative_path.startswith("results/figures/") and "_by_corruption" in relative_path:
        return "corruption_figures"
    if relative_path.startswith("results/reports/corruption_"):
        return "corruption_reports"
    if relative_path.startswith("results/figures/"):
        return "figures"
    if relative_path.startswith("results/reports/"):
        return "reports"
    return "reports"


def _csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def _check_required_files(repo_root: Path) -> VerificationCheck:
    missing = [
        path
        for path in REQUIRED_FINAL_ARTIFACTS + REQUIRED_PHASE7_FILES
        if path != "results/reports/verification_report.md" and not (repo_root / path).exists()
    ]
    return _check(
        "required_files_exist",
        not missing,
        f"missing={missing if missing else 'none'}",
    )


def _check_inventory_complete(inventory: dict[str, Any]) -> VerificationCheck:
    missing_categories = inventory.get("missing_required_categories", [])
    missing_artifacts = inventory.get("missing_required_artifacts", [])
    return _check(
        "artifact_inventory_complete",
        inventory.get("status") == "pass" and not missing_categories and not missing_artifacts,
        f"entries={inventory.get('entry_count')} missing_categories={missing_categories} missing_artifacts={missing_artifacts}",
    )


def _check_inventory_hashes(repo_root: Path, inventory: dict[str, Any]) -> VerificationCheck:
    mismatches = []
    for entry in inventory.get("entries", []):
        path = repo_root / entry["path"]
        if not path.exists() or sha256_file(path) != entry["sha256"]:
            mismatches.append(entry["path"])
    return _check("artifact_hashes_match", not mismatches, f"mismatches={mismatches if mismatches else 'none'}")


def _check_governance_source_hashes(repo_root: Path) -> VerificationCheck:
    foundation = load_json_config(repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json")
    ch10a_root = Path(foundation["source_path"])
    mismatches = []
    for relative_path, expected_hash in foundation.get("governance_hashes", {}).items():
        if sha256_file(ch10a_root / relative_path) != expected_hash:
            mismatches.append(relative_path)
    return _check("no_governance_source_drift", not mismatches, f"mismatches={mismatches if mismatches else 'none'}")


def _check_seed_registry(repo_root: Path) -> VerificationCheck:
    registry = load_seed_registry(repo_root / "configs" / "reproducibility" / "seed_registry.yaml")
    locked = set(registry["locked_execution_seeds"])
    audit = set(registry["audit_execution_seeds"])
    valid = len(locked) == 30 and len(audit) == 20 and not (locked & audit)
    return _check("seed_registry_complete", valid, f"locked={len(locked)} audit={len(audit)} overlap={len(locked & audit)}")


def _check_locked_audit_independence(repo_root: Path) -> VerificationCheck:
    locked = pd.read_csv(repo_root / "results" / "execution_corpus" / "locked" / "corpus_index.csv", dtype=str, usecols=["run_mode", "execution_seed", "split_schedule_id"])
    audit = pd.read_csv(repo_root / "results" / "execution_corpus" / "audit" / "corpus_index.csv", dtype=str, usecols=["run_mode", "execution_seed", "split_schedule_id"])
    seed_overlap = set(locked["execution_seed"]) & set(audit["execution_seed"])
    split_overlap = set(locked["split_schedule_id"]) & set(audit["split_schedule_id"])
    valid = set(locked["run_mode"]) == {"locked"} and set(audit["run_mode"]) == {"audit"} and not seed_overlap and not split_overlap
    return _check("locked_audit_independence", valid, f"seed_overlap={len(seed_overlap)} split_overlap={len(split_overlap)}")


def _check_split_partitions(repo_root: Path) -> VerificationCheck:
    datasets = ["breast_cancer_wisconsin", "adult_income", "credit_card_fraud", "bank_marketing"]
    schedules = [
        ("locked", "locked_split_01", 31001),
        ("locked", "locked_split_05", 31005),
        ("audit", "audit_split_01", 32001),
        ("audit", "audit_split_03", 32003),
    ]
    failures = []
    for dataset_id in datasets:
        for run_mode, schedule_id, seed in schedules:
            bundle = build_partition_bundle(dataset_id, run_mode, schedule_id, seed)
            hashes = [
                bundle.train_hash,
                bundle.validation_hash,
                bundle.calibration_hash,
                bundle.locked_benchmark_hash if run_mode == "locked" else bundle.audit_benchmark_hash,
            ]
            if len(set(hashes)) != len(hashes):
                failures.append(f"{dataset_id}:{run_mode}:{schedule_id}")
    return _check("split_partitions_disjoint", not failures, f"failures={failures if failures else 'none'}")


def _check_system_and_metric_coverage(repo_root: Path) -> VerificationCheck:
    variance = pd.read_csv(repo_root / "results" / "reports" / "variance_tables.csv", dtype=str)
    stability = pd.read_csv(repo_root / "results" / "reports" / "stability_tables.csv", dtype=str)
    clean_metrics = set(variance["metric_name"]) | set(stability["metric_name"])
    systems = set(variance["system_id"]) | set(stability["system_id"])
    expected_systems = {"single_model", "mean_ensemble", "static_weighted_ensemble", "veto_mavs", "pure_mavs_gc"}
    metric_names_required = set(REQUIRED_CLEAN_METRICS) - {"confidence_interval_width"}
    missing_metrics = sorted(metric_names_required - clean_metrics)
    confidence_width_present = (
        "confidence_interval_width" in variance.columns
        and variance["confidence_interval_width"].astype(str).str.len().gt(0).any()
    )
    if not confidence_width_present:
        missing_metrics.append("confidence_interval_width")
    valid = systems == expected_systems and not missing_metrics
    return _check("systems_and_metrics_complete", valid, f"systems={sorted(systems)} missing_metrics={missing_metrics}")


def _check_governance_trace_contract(repo_root: Path) -> VerificationCheck:
    trace = pd.read_csv(repo_root / "results" / "execution_corpus" / "locked" / "trace_index.csv", dtype=str, nrows=10)
    missing_columns = sorted(set(GOVERNANCE_TRACE_FIELDS) - set(trace.columns))
    valid = not missing_columns
    return _check("governance_trace_contract", valid, f"missing_columns={missing_columns if missing_columns else 'none'}")


def _check_report_claim_references(repo_root: Path) -> VerificationCheck:
    manifest = load_json_config(repo_root / "results" / "reports" / "reproducibility_artifact_manifest.json")
    policy = manifest.get("report_claim_policy", {})
    valid = (
        policy.get("every_claim_references_artifacts") is True
        and policy.get("global_superiority_claim_made") is False
        and policy.get("corruption_robustness_claim_made") is False
    )
    return _check("clean_report_claims_reference_artifacts", valid, f"policy={policy}")


def _check_corruption_coverage(repo_root: Path) -> VerificationCheck:
    config = load_json_config(repo_root / "configs" / "experiments" / "corruption_reproducibility.yaml")
    variance = pd.read_csv(repo_root / config["output_paths"]["variance_tables"], dtype=str)
    stability = pd.read_csv(repo_root / config["output_paths"]["stability_tables"], dtype=str)
    trace = pd.read_csv(repo_root / config["output_paths"]["trace_stability_tables"], dtype=str)
    observed_metrics = set(variance["metric_name"]) | set(stability["metric_name"])
    missing_metrics = sorted(set(REQUIRED_CORRUPTION_METRICS) - observed_metrics)
    families = set(variance["corruption_family"]) & set(stability["corruption_family"]) & set(trace["corruption_family"])
    levels = {float(value) for value in variance["corruption_level"].unique()}
    valid = families == set(config["families"]) and levels == set(config["levels"]) and not missing_metrics
    return _check("corruption_families_levels_metrics_complete", valid, f"families={len(families)} levels={sorted(levels)} missing_metrics={missing_metrics}")


def _check_corruption_claim_references(repo_root: Path) -> VerificationCheck:
    ledger = pd.read_csv(repo_root / "results" / "reports" / "corruption_claim_support_ledger.csv", dtype=str)
    missing_artifacts = []
    for row in ledger.to_dict("records"):
        paths = [row["primary_artifact"]] + [
            path.strip() for path in str(row["supporting_artifacts"]).split(";") if path.strip()
        ]
        missing_artifacts.extend(path for path in paths if not (repo_root / path).exists())
    valid = len(ledger) == 10 and set(ledger["claim_id"].astype(int)) == set(range(1, 11)) and not missing_artifacts
    return _check("corruption_claims_reference_artifacts", valid, f"claims={len(ledger)} missing_artifacts={missing_artifacts if missing_artifacts else 'none'}")


def _check_corruption_clean_anchor(repo_root: Path) -> VerificationCheck:
    config = load_json_config(repo_root / "configs" / "experiments" / "corruption_reproducibility.yaml")
    corruption = pd.read_csv(repo_root / config["output_paths"]["variance_tables"], dtype=str)
    phase5 = pd.read_csv(repo_root / config["source_manifests"]["phase5_clean_variance_table"], dtype=str)
    corruption = corruption[
        (corruption["corruption_level"].astype(float) == 0.0)
        & (corruption["metric_name"].isin(["accuracy_variance", "f1_variance"]))
    ]
    phase5_map = {
        (
            row["run_mode"],
            row["dataset_id"],
            row["system_id"],
            row["specialist_composition_id"],
            row["metric_name"],
        ): row
        for row in phase5.to_dict("records")
    }
    tolerance = float(config["clean_anchor_tolerance"])
    mismatches = 0
    for row in corruption.to_dict("records"):
        key = (
            row["run_mode"],
            row["dataset_id"],
            row["system_id"],
            row["specialist_composition_id"],
            row["metric_name"],
        )
        clean = phase5_map[key]
        if abs(float(row["sample_variance"]) - float(clean["sample_variance"])) > tolerance:
            mismatches += 1
    return _check("corruption_clean_anchor_matches_phase5", mismatches == 0, f"checked={len(corruption)} mismatches={mismatches}")


def _check_final_run_guards(repo_root: Path) -> VerificationCheck:
    clean_manifest = load_json_config(repo_root / "results" / "reports" / "reproducibility_artifact_manifest.json")
    corruption_manifest = load_json_config(repo_root / "results" / "corruption_reproducibility" / "corruption_metric_manifest.json")
    clean_class = clean_manifest.get("final_run_classification", {})
    valid = (
        clean_class.get("exploratory_results_used") is False
        and clean_class.get("training_diagnostics_used_as_final_evidence") is False
        and corruption_manifest.get("training_performed") is False
        and corruption_manifest.get("hyperparameter_search_performed") is False
        and corruption_manifest.get("threshold_tuning_after_corruption_performed") is False
        and corruption_manifest.get("governance_policy_modified") is False
    )
    return _check("final_run_guards", valid, f"clean_classification={clean_class}")


def _check_path_md(repo_root: Path) -> VerificationCheck:
    text = (repo_root / "Path.md").read_text(encoding="utf-8")
    required_terms = [
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Phase 5",
        "Phase 6",
        "Phase 7",
        "artifact_inventory",
        "verification_report",
        "WorkPlan Compliance Check",
        "run ids at manifest level",
        "hash",
        "Deviations and Limitations",
        "Final `python scripts/reproduce_all.py --run-mode final`: passed",
        "Full repository tests: `53 passed`",
    ]
    missing = [term for term in required_terms if term not in text]
    return _check("path_md_complete", not missing, f"missing_terms={missing if missing else 'none'}")


def _check_corruption_addendum(repo_root: Path) -> VerificationCheck:
    text = (repo_root / "results" / "reports" / "corruption_verification_addendum.md").read_text(encoding="utf-8")
    valid = "Overall status: `pass`." in text and "Missing units: none." in text
    return _check("corruption_verification_addendum_pass", valid, "overall status and missing-unit statement checked")


def _check(check_id: str, passed: bool, evidence: str) -> VerificationCheck:
    return VerificationCheck(check_id=check_id, status="pass" if passed else "fail", evidence=evidence)


def _render_verification_report(verification: dict[str, Any]) -> str:
    lines = [
        "# MAVS Chapter 10C Verification Report",
        "",
        f"Overall status: `{verification['overall_status']}`.",
        "",
        "## Verification Gates",
        "",
    ]
    for check in verification["checks"]:
        lines.extend(
            [
                f"### {check['check_id']}",
                "",
                f"Status: `{check['status']}`.",
                "",
                f"Evidence: {check['evidence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Final Evidence Policy",
            "",
            "Final clean evidence is generated from the frozen Phase 2-5 matrices. Final corruption evidence is generated from the frozen Phase 6 matrix. Smoke, exploratory, training, validation, and calibration diagnostics are not used as final evidence.",
            "",
        ]
    )
    return "\n".join(lines)
