"""Phase 4 reproducibility metric aggregation and artifact writing."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.evaluation import BASELINE_SYSTEMS, REQUIRED_METRIC_FAMILIES
from mavs_ch10c.evaluation.agreement import build_run_to_run_agreement_rows
from mavs_ch10c.evaluation.confidence_intervals import build_confidence_interval_rows
from mavs_ch10c.evaluation.stability import (
    build_consensus_stability_rows,
    build_decision_stability_rows,
    build_prediction_stability_rows,
)
from mavs_ch10c.evaluation.trace_stability import build_trace_stability_rows
from mavs_ch10c.evaluation.variance import (
    build_execution_unit_metrics,
    build_metric_variance_rows,
)
from mavs_ch10c.verification.hash_utils import (
    load_json_config,
    sha256_file,
    sha256_json,
    write_json,
)

METRIC_CODE_PATHS = [
    "src/mavs_ch10c/evaluation/__init__.py",
    "src/mavs_ch10c/evaluation/variance.py",
    "src/mavs_ch10c/evaluation/stability.py",
    "src/mavs_ch10c/evaluation/agreement.py",
    "src/mavs_ch10c/evaluation/confidence_intervals.py",
    "src/mavs_ch10c/evaluation/trace_stability.py",
    "src/mavs_ch10c/evaluation/aggregation.py",
    "scripts/build_reproducibility_metrics.py",
    "scripts/build_stability_tables.py",
    "configs/experiments/reproducibility_metrics.yaml",
]

METRIC_ROW_FIELDS = [
    "metric_row_id",
    "metric_family",
    "metric_name",
    "aggregation_grain",
    "run_mode",
    "dataset_id",
    "system_id",
    "baseline_system_id",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
    "trace_field",
    "agreement_target",
    "compared_metric",
    "row_count",
    "repetition_unit_count",
    "observation_count",
    "pair_count",
    "row_alignment_group_count",
    "mean_value",
    "sample_variance",
    "standard_deviation",
    "standard_error",
    "confidence_level",
    "confidence_method",
    "confidence_interval_width",
    "ci_width_comparison_to_pure",
    "binary_pairwise_agreement",
    "decision_pairwise_agreement",
    "probability_pairwise_stability",
    "mean_abs_probability_difference",
    "consensus_applicability",
    "consensus_field",
    "consensus_pairwise_stability",
    "score_probability_pairwise_stability",
    "mean_row_level_variance",
    "field_exact_repeat_rate",
    "exact_trace_hash_repeat_rate",
    "normalized_trace_distance_mean",
    "normalized_trace_similarity",
    "kappa_agreement",
    "expected_agreement",
    "zero_division_policy",
    "pure_mavs_reference_value",
    "baseline_value",
    "delta_value",
    "direction_vs_baseline",
    "metric_definition_version",
    "source_input_hash",
    "source_backend",
]

REQUIRED_ARTIFACTS = {
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
}


def build_reproducibility_metrics(
    repo_root: Path,
    config_path: Path | None = None,
    command_line: list[str] | None = None,
) -> dict[str, Any]:
    """Build all Phase 4 reproducibility metric artifacts."""

    # console.log: phase4 reproducibility metric build begins.
    console.log("phase4.aggregation.build.start")
    config_path = config_path or repo_root / "configs" / "experiments" / "reproducibility_metrics.yaml"
    command_line = command_line or []
    config = load_json_config(config_path)
    output_dir = repo_root / str(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    variance_manifest = _load_frozen_variance_manifest(repo_root, config)
    metric_code_hashes = _metric_code_hashes(repo_root)
    existing_manifest = _load_existing_metric_manifest_if_valid(
        repo_root, output_dir, config_path, config, variance_manifest, metric_code_hashes
    )
    if existing_manifest is not None:
        # console.log: phase4 reproducibility metric cache hit.
        console.log(
            "phase4.aggregation.build.cache_hit "
            f"hash={existing_manifest['reproducibility_metric_manifest_hash']}"
        )
        return existing_manifest

    locked_rows = _load_variance_rows(repo_root, "locked")
    audit_rows = _load_variance_rows(repo_root, "audit")
    delta_rows = _load_delta_rows(repo_root)
    source_input_hash = variance_manifest["variance_dataset_manifest_hash"]
    locked_tables = _build_mode_metric_tables(locked_rows, config, source_input_hash)
    audit_tables = _build_mode_metric_tables(audit_rows, config, source_input_hash)
    paired_rows = _build_paired_comparison_rows(
        delta_rows,
        config["metric_definition_version"],
        source_input_hash,
    )

    locked_metric_rows = _with_definition_version(
        _mode_rows(locked_tables) + [row for row in paired_rows if row["run_mode"] == "locked"],
        config["metric_definition_version"],
    )
    audit_metric_rows = _with_definition_version(
        _mode_rows(audit_tables) + [row for row in paired_rows if row["run_mode"] == "audit"],
        config["metric_definition_version"],
    )
    table_rows = {
        "locked_metric_rows": locked_metric_rows,
        "audit_metric_rows": audit_metric_rows,
        "accuracy_variance": _with_definition_version(
            locked_tables["accuracy_variance"] + audit_tables["accuracy_variance"],
            config["metric_definition_version"],
        ),
        "f1_variance": _with_definition_version(
            locked_tables["f1_variance"] + audit_tables["f1_variance"],
            config["metric_definition_version"],
        ),
        "prediction_stability": _with_definition_version(
            locked_tables["prediction_stability"] + audit_tables["prediction_stability"],
            config["metric_definition_version"],
        ),
        "decision_stability": _with_definition_version(
            locked_tables["decision_stability"] + audit_tables["decision_stability"],
            config["metric_definition_version"],
        ),
        "consensus_stability": _with_definition_version(
            locked_tables["consensus_stability"] + audit_tables["consensus_stability"],
            config["metric_definition_version"],
        ),
        "trace_stability": _with_definition_version(
            locked_tables["trace_stability"] + audit_tables["trace_stability"],
            config["metric_definition_version"],
        ),
        "run_to_run_agreement": _with_definition_version(
            locked_tables["run_to_run_agreement"] + audit_tables["run_to_run_agreement"],
            config["metric_definition_version"],
        ),
        "confidence_interval_widths": _with_definition_version(
            locked_tables["confidence_interval_width"] + audit_tables["confidence_interval_width"],
            config["metric_definition_version"],
        ),
    }
    for artifact_name, rows in table_rows.items():
        _write_metric_csv(output_dir / REQUIRED_ARTIFACTS[artifact_name], rows)

    artifact_hashes = {
        artifact_name: sha256_file(output_dir / filename)
        for artifact_name, filename in REQUIRED_ARTIFACTS.items()
    }
    manifest = _build_metric_manifest(
        repo_root,
        config_path,
        config,
        command_line,
        variance_manifest,
        metric_code_hashes,
        artifact_hashes,
        table_rows,
    )
    manifest_hash = write_json(output_dir / "reproducibility_metric_manifest.json", manifest)
    manifest["reproducibility_metric_manifest_hash"] = manifest_hash
    write_json(output_dir / "reproducibility_metric_manifest.json", manifest)
    # console.log: phase4 reproducibility metric build completed.
    console.log(
        "phase4.aggregation.build.complete "
        f"locked_rows={len(locked_metric_rows)} audit_rows={len(audit_metric_rows)} "
        f"hash={manifest['reproducibility_metric_manifest_hash']}"
    )
    return manifest


def _build_mode_metric_tables(
    rows: pd.DataFrame,
    config: dict[str, Any],
    source_input_hash: str,
) -> dict[str, list[dict[str, Any]]]:
    # console.log: phase4 per-mode metric table build begins.
    console.log(f"phase4.aggregation.mode_tables.start mode={rows['run_mode'].iloc[0]}")
    execution_units = build_execution_unit_metrics(rows, config["zero_division_policy"])
    tables = {
        "accuracy_variance": build_metric_variance_rows(
            execution_units,
            "accuracy",
            "accuracy_variance",
            config["zero_division_policy"],
            source_input_hash,
        ),
        "f1_variance": build_metric_variance_rows(
            execution_units,
            "f1",
            "f1_variance",
            config["zero_division_policy"],
            source_input_hash,
        ),
        "prediction_stability": build_prediction_stability_rows(rows, source_input_hash),
        "decision_stability": build_decision_stability_rows(rows, source_input_hash),
        "consensus_stability": build_consensus_stability_rows(rows, source_input_hash),
        "trace_stability": build_trace_stability_rows(rows, source_input_hash),
        "run_to_run_agreement": build_run_to_run_agreement_rows(rows, source_input_hash),
        "confidence_interval_width": build_confidence_interval_rows(
            execution_units,
            confidence_level=float(config["confidence_level"]),
            z_value=float(config["z_value"]),
            zero_division_policy=config["zero_division_policy"],
            source_input_hash=source_input_hash,
        ),
    }
    # console.log: phase4 per-mode metric table build completed.
    console.log(f"phase4.aggregation.mode_tables.complete mode={rows['run_mode'].iloc[0]}")
    return tables


def _mode_rows(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family in REQUIRED_METRIC_FAMILIES:
        rows.extend(tables[family])
    return rows


def _build_paired_comparison_rows(
    delta_rows: pd.DataFrame,
    metric_definition_version: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    # console.log: phase4 paired Pure MAVS baseline comparison build begins.
    console.log("phase4.aggregation.paired_comparisons.start")
    working = delta_rows.copy()
    for column in ["probability_delta", "decision_delta", "confidence_delta", "correctness_delta"]:
        working[column] = pd.to_numeric(working[column])
    outputs: list[dict[str, Any]] = []
    for group_columns, grain in [
        (
            [
                "run_mode",
                "dataset_id",
                "baseline_system_id",
                "split_schedule_id",
                "initialization_schedule_id",
                "specialist_composition_id",
            ],
            "dataset_baseline_split_init_composition",
        ),
        (
            ["run_mode", "dataset_id", "baseline_system_id", "specialist_composition_id"],
            "dataset_baseline_composition",
        ),
    ]:
        for key, group in working.groupby(group_columns, dropna=False):
            values = key if isinstance(key, tuple) else (key,)
            payload = {
                "run_mode": "",
                "dataset_id": "",
                "system_id": "pure_mavs_gc",
                "baseline_system_id": "",
                "split_schedule_id": "all",
                "initialization_schedule_id": "all",
                "specialist_composition_id": "",
            }
            for column, value in zip(group_columns, values):
                payload[column] = str(value)
            mean_correctness_delta = float(group["correctness_delta"].mean())
            mean_probability_delta = float(group["probability_delta"].mean())
            payload.update(
                {
                    "metric_family": "paired_pure_mavs_baseline",
                    "metric_name": "paired_pure_mavs_gc_vs_baseline",
                    "aggregation_grain": grain,
                    "row_count": int(len(group)),
                    "mean_value": mean_correctness_delta,
                    "baseline_value": str(payload["baseline_system_id"]),
                    "delta_value": mean_correctness_delta,
                    "mean_abs_probability_difference": abs(mean_probability_delta),
                    "decision_pairwise_agreement": 1.0 - float((group["decision_delta"].abs() > 0).mean()),
                    "direction_vs_baseline": _delta_direction(mean_correctness_delta),
                    "metric_definition_version": metric_definition_version,
                    "source_input_hash": source_input_hash,
                    "source_backend": "empirical_sklearn_repeated_training",
                }
            )
            payload["metric_row_id"] = _metric_row_id(payload)
            outputs.append(payload)
    # console.log: phase4 paired Pure MAVS baseline comparison build completed.
    console.log(f"phase4.aggregation.paired_comparisons.complete rows={len(outputs)}")
    return outputs


def _delta_direction(delta: float) -> str:
    if abs(delta) <= 1e-12:
        return "neutral"
    return "pure_mavs_higher" if delta > 0.0 else "pure_mavs_lower"


def _build_metric_manifest(
    repo_root: Path,
    config_path: Path,
    config: dict[str, Any],
    command_line: list[str],
    variance_manifest: dict[str, Any],
    metric_code_hashes: dict[str, str],
    artifact_hashes: dict[str, str],
    table_rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    locked_metric_rows = table_rows["locked_metric_rows"]
    audit_metric_rows = table_rows["audit_metric_rows"]
    paired_rows = [
        row
        for row in locked_metric_rows + audit_metric_rows
        if row.get("metric_family") == "paired_pure_mavs_baseline"
    ]
    manifest = {
        "status": "pass",
        "phase": "phase4_reproducibility_metrics",
        "metric_definition_version": config["metric_definition_version"],
        "source_variance_manifest_hash": variance_manifest["variance_dataset_manifest_hash"],
        "source_variance_artifact_hashes": variance_manifest["artifact_hashes"],
        "metrics_read_only_frozen_variance_datasets": True,
        "training_performed": False,
        "audit_metric_definitions_frozen": config["audit_metric_definitions_frozen"],
        "metric_definitions_selected_from_audit": False,
        "preserve_negative_neutral_mixed_results": config["preserve_negative_neutral_mixed_results"],
        "confidence_interval_method": config["confidence_interval_method"],
        "confidence_level": float(config["confidence_level"]),
        "z_value": float(config["z_value"]),
        "bootstrap_seed": config["bootstrap_seed"],
        "zero_division_policy": config["zero_division_policy"],
        "config_hash": sha256_file(config_path),
        "metric_code_hashes": metric_code_hashes,
        "artifact_hashes": artifact_hashes,
        "locked_metric_row_count": len(locked_metric_rows),
        "audit_metric_row_count": len(audit_metric_rows),
        "table_row_counts": {name: len(rows) for name, rows in table_rows.items()},
        "required_metric_families": REQUIRED_METRIC_FAMILIES,
        "paired_pure_mavs_baselines": BASELINE_SYSTEMS,
        "paired_pure_mavs_baseline_row_count": len(paired_rows),
        "locked_audit_consistency": _locked_audit_consistency(locked_metric_rows, audit_metric_rows),
        "variance_coverage": {
            "locked": variance_manifest["locked"],
            "audit": variance_manifest["audit"],
        },
        "command_line": command_line,
        "output_dir": str(repo_root / str(config["output_dir"])),
    }
    return manifest


def _locked_audit_consistency(
    locked_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    locked_families = {row["metric_family"] for row in locked_rows}
    audit_families = {row["metric_family"] for row in audit_rows}
    locked_systems = {row["system_id"] for row in locked_rows if row.get("system_id")}
    audit_systems = {row["system_id"] for row in audit_rows if row.get("system_id")}
    locked_baselines = {row["baseline_system_id"] for row in locked_rows if row.get("baseline_system_id")}
    audit_baselines = {row["baseline_system_id"] for row in audit_rows if row.get("baseline_system_id")}
    return {
        "metric_families_match": locked_families == audit_families,
        "systems_match": locked_systems == audit_systems,
        "paired_baselines_match": locked_baselines == audit_baselines,
        "locked_metric_families": sorted(locked_families),
        "audit_metric_families": sorted(audit_families),
        "locked_systems": sorted(locked_systems),
        "audit_systems": sorted(audit_systems),
        "locked_paired_baselines": sorted(locked_baselines),
        "audit_paired_baselines": sorted(audit_baselines),
    }


def _load_frozen_variance_manifest(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    # console.log: phase4 frozen variance manifest load begins.
    console.log("phase4.aggregation.variance_manifest.start")
    manifest_path = repo_root / str(config["source_variance_manifest_path"])
    manifest = load_json_config(manifest_path)
    if manifest.get("status") != "pass":
        raise RuntimeError("Phase 4 requires a passing Phase 3 variance manifest")
    if manifest.get("trace_fields_available_for_phase4") is not True:
        raise RuntimeError("Phase 4 requires Phase 3 variance rows with trace fields")
    expected_files = {
        "locked_variance_rows": repo_root / "results" / "variance_benchmarks" / "locked_variance_rows.csv",
        "audit_variance_rows": repo_root / "results" / "variance_benchmarks" / "audit_variance_rows.csv",
        "system_delta_rows": repo_root / "results" / "variance_benchmarks" / "system_delta_rows.csv",
    }
    for label, path in expected_files.items():
        if manifest["artifact_hashes"].get(label) != sha256_file(path):
            raise RuntimeError(f"Frozen variance artifact hash mismatch: {label}")
    # console.log: phase4 frozen variance manifest load completed.
    console.log(
        "phase4.aggregation.variance_manifest.complete "
        f"hash={manifest['variance_dataset_manifest_hash']}"
    )
    return manifest


def _load_existing_metric_manifest_if_valid(
    repo_root: Path,
    output_dir: Path,
    config_path: Path,
    config: dict[str, Any],
    variance_manifest: dict[str, Any],
    metric_code_hashes: dict[str, str],
) -> dict[str, Any] | None:
    manifest_path = output_dir / "reproducibility_metric_manifest.json"
    if not manifest_path.exists():
        return None
    try:
        manifest = load_json_config(manifest_path)
    except Exception:
        return None
    if manifest.get("status") != "pass":
        return None
    if manifest.get("metric_definition_version") != config["metric_definition_version"]:
        return None
    if manifest.get("config_hash") != sha256_file(config_path):
        return None
    if manifest.get("source_variance_manifest_hash") != variance_manifest["variance_dataset_manifest_hash"]:
        return None
    if manifest.get("metric_code_hashes") != metric_code_hashes:
        return None
    artifact_hashes = manifest.get("artifact_hashes", {})
    if set(artifact_hashes) != set(REQUIRED_ARTIFACTS):
        return None
    for artifact_name, filename in REQUIRED_ARTIFACTS.items():
        path = output_dir / filename
        if not path.exists() or artifact_hashes.get(artifact_name) != sha256_file(path):
            return None
    return manifest


def _load_variance_rows(repo_root: Path, run_mode: str) -> pd.DataFrame:
    # console.log: phase4 variance row load begins.
    console.log(f"phase4.aggregation.variance_rows.start mode={run_mode}")
    path = repo_root / "results" / "variance_benchmarks" / f"{run_mode}_variance_rows.csv"
    rows = pd.read_csv(path, dtype=str)
    if rows.empty:
        raise RuntimeError(f"Phase 4 cannot consume empty variance rows: {path}")
    # console.log: phase4 variance row load completed.
    console.log(f"phase4.aggregation.variance_rows.complete mode={run_mode} rows={len(rows)}")
    return rows


def _load_delta_rows(repo_root: Path) -> pd.DataFrame:
    # console.log: phase4 system delta row load begins.
    console.log("phase4.aggregation.delta_rows.start")
    path = repo_root / "results" / "variance_benchmarks" / "system_delta_rows.csv"
    rows = pd.read_csv(path, dtype=str)
    if rows.empty:
        raise RuntimeError(f"Phase 4 cannot consume empty delta rows: {path}")
    # console.log: phase4 system delta row load completed.
    console.log(f"phase4.aggregation.delta_rows.complete rows={len(rows)}")
    return rows


def _write_metric_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    # console.log: phase4 metric CSV write begins.
    console.log(f"phase4.aggregation.csv_write.start path={path} rows={len(rows)}")
    if not rows:
        raise RuntimeError(f"Cannot write empty Phase 4 metric table: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=METRIC_ROW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in METRIC_ROW_FIELDS})
    # console.log: phase4 metric CSV write completed.
    console.log(f"phase4.aggregation.csv_write.complete path={path}")


def _metric_code_hashes(repo_root: Path) -> dict[str, str]:
    return {relative_path: sha256_file(repo_root / relative_path) for relative_path in METRIC_CODE_PATHS}


def _with_definition_version(
    rows: list[dict[str, Any]], metric_definition_version: str
) -> list[dict[str, Any]]:
    for row in rows:
        row["metric_definition_version"] = metric_definition_version
    return rows


def _metric_row_id(payload: dict[str, Any]) -> str:
    return sha256_json(
        {
            "metric_family": payload["metric_family"],
            "metric_name": payload["metric_name"],
            "aggregation_grain": payload["aggregation_grain"],
            "run_mode": payload["run_mode"],
            "dataset_id": payload["dataset_id"],
            "system_id": payload["system_id"],
            "baseline_system_id": payload["baseline_system_id"],
            "split_schedule_id": payload["split_schedule_id"],
            "initialization_schedule_id": payload["initialization_schedule_id"],
            "specialist_composition_id": payload["specialist_composition_id"],
        }
    )[:24]
