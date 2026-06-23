"""Phase 5 reproducibility table builders."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.reporting import BASELINE_SYSTEMS, PURE_MAVS_SYSTEM
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file, sha256_json

VARIANCE_TABLE_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "metric_name",
    "compared_metric",
    "mean_metric_value",
    "sample_variance",
    "standard_deviation",
    "confidence_interval_width",
    "ci_width_comparison_to_pure",
    "pure_mavs_reference_ci_width",
    "row_count",
    "repetition_unit_count",
    "source_metric_manifest_hash",
    "source_metric_artifact_hash",
]

STABILITY_TABLE_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "metric_name",
    "trace_field",
    "agreement_target",
    "reported_value_name",
    "reported_value",
    "secondary_value_name",
    "secondary_value",
    "pair_count",
    "observation_count",
    "row_alignment_group_count",
    "consensus_applicability",
    "source_metric_manifest_hash",
    "source_metric_artifact_hash",
]

DELTA_TABLE_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "baseline_system_id",
    "system_id",
    "specialist_composition_id",
    "mean_correctness_delta",
    "direction_vs_baseline",
    "decision_pairwise_agreement",
    "mean_abs_probability_difference",
    "row_count",
    "source_metric_manifest_hash",
    "source_metric_artifact_hash",
]


def build_report_tables(repo_root: Path, config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Build Phase 5 report tables from frozen Phase 4 metric artifacts."""

    # console.log: phase5 report table build begins.
    console.log("phase5.tables.build.start")
    metric_manifest = _load_metric_manifest(repo_root, config)
    variance_rows = _build_variance_rows(repo_root, config, metric_manifest)
    stability_rows = _build_stability_rows(repo_root, config, metric_manifest)
    delta_rows = _build_delta_rows(repo_root, config, metric_manifest)
    outputs = {
        "variance_tables": variance_rows,
        "stability_tables": stability_rows,
        "reproducibility_system_deltas": delta_rows,
    }
    _validate_table_coverage(outputs, config)
    for name, rows in outputs.items():
        path = repo_root / config["output_paths"][name]
        fieldnames = {
            "variance_tables": VARIANCE_TABLE_FIELDS,
            "stability_tables": STABILITY_TABLE_FIELDS,
            "reproducibility_system_deltas": DELTA_TABLE_FIELDS,
        }[name]
        _write_csv(path, rows, fieldnames)
    # console.log: phase5 report table build completed.
    console.log(
        "phase5.tables.build.complete "
        f"variance_rows={len(variance_rows)} stability_rows={len(stability_rows)} "
        f"delta_rows={len(delta_rows)}"
    )
    return outputs


def _build_variance_rows(
    repo_root: Path,
    config: dict[str, Any],
    metric_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    # console.log: phase5 variance table derivation begins.
    console.log("phase5.tables.variance.start")
    expected = config["expected"]
    summary_grain = expected["summary_aggregation_grain"]
    frames = [
        _read_metric_csv(repo_root, config, "accuracy_variance"),
        _read_metric_csv(repo_root, config, "f1_variance"),
    ]
    variance = pd.concat(frames, ignore_index=True)
    variance = variance[variance["aggregation_grain"] == summary_grain].copy()
    ci = _read_metric_csv(repo_root, config, "confidence_interval_widths")
    ci = ci[ci["aggregation_grain"] == summary_grain].copy()
    ci_map = {
        _variance_ci_key(row): row
        for row in ci.to_dict("records")
        if row["compared_metric"] in {"accuracy", "f1"}
    }
    rows: list[dict[str, Any]] = []
    for source in variance.to_dict("records"):
        ci_row = ci_map.get(_variance_ci_key(source), {})
        row = {
            "run_mode": source["run_mode"],
            "dataset_id": source["dataset_id"],
            "system_id": source["system_id"],
            "specialist_composition_id": source["specialist_composition_id"],
            "metric_name": source["metric_name"],
            "compared_metric": source["compared_metric"],
            "mean_metric_value": source["mean_value"],
            "sample_variance": source["sample_variance"],
            "standard_deviation": source["standard_deviation"],
            "confidence_interval_width": ci_row.get("confidence_interval_width", ""),
            "ci_width_comparison_to_pure": ci_row.get("ci_width_comparison_to_pure", ""),
            "pure_mavs_reference_ci_width": ci_row.get("pure_mavs_reference_value", ""),
            "row_count": source["row_count"],
            "repetition_unit_count": source["repetition_unit_count"],
            "source_metric_manifest_hash": metric_manifest["reproducibility_metric_manifest_hash"],
            "source_metric_artifact_hash": metric_manifest["artifact_hashes"][source["metric_name"]],
        }
        row["table_row_id"] = sha256_json(row)[:24]
        rows.append(row)
    rows = _sort_rows(rows, VARIANCE_TABLE_FIELDS)
    # console.log: phase5 variance table derivation completed.
    console.log(f"phase5.tables.variance.complete rows={len(rows)}")
    return rows


def _build_stability_rows(
    repo_root: Path,
    config: dict[str, Any],
    metric_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    # console.log: phase5 stability table derivation begins.
    console.log("phase5.tables.stability.start")
    expected = config["expected"]
    summary_grain = expected["summary_aggregation_grain"]
    metric_inputs = [
        "prediction_stability",
        "decision_stability",
        "consensus_stability",
        "trace_stability",
        "run_to_run_agreement",
    ]
    rows: list[dict[str, Any]] = []
    for metric_key in metric_inputs:
        frame = _read_metric_csv(repo_root, config, metric_key)
        frame = frame[frame["aggregation_grain"] == summary_grain].copy()
        for source in frame.to_dict("records"):
            value_name, value = _primary_stability_value(source)
            secondary_name, secondary_value = _secondary_stability_value(source)
            row = {
                "run_mode": source["run_mode"],
                "dataset_id": source["dataset_id"],
                "system_id": source["system_id"],
                "specialist_composition_id": source["specialist_composition_id"],
                "metric_name": source["metric_name"],
                "trace_field": source["trace_field"],
                "agreement_target": source["agreement_target"],
                "reported_value_name": value_name,
                "reported_value": value,
                "secondary_value_name": secondary_name,
                "secondary_value": secondary_value,
                "pair_count": source["pair_count"],
                "observation_count": source["observation_count"],
                "row_alignment_group_count": source["row_alignment_group_count"],
                "consensus_applicability": source["consensus_applicability"],
                "source_metric_manifest_hash": metric_manifest[
                    "reproducibility_metric_manifest_hash"
                ],
                "source_metric_artifact_hash": metric_manifest["artifact_hashes"][metric_key],
            }
            row["table_row_id"] = sha256_json(row)[:24]
            rows.append(row)
    rows = _sort_rows(rows, STABILITY_TABLE_FIELDS)
    # console.log: phase5 stability table derivation completed.
    console.log(f"phase5.tables.stability.complete rows={len(rows)}")
    return rows


def _build_delta_rows(
    repo_root: Path,
    config: dict[str, Any],
    metric_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    # console.log: phase5 system delta table derivation begins.
    console.log("phase5.tables.deltas.start")
    expected = config["expected"]
    locked = _read_metric_csv(repo_root, config, "locked_metric_rows")
    audit = _read_metric_csv(repo_root, config, "audit_metric_rows")
    deltas = pd.concat([locked, audit], ignore_index=True)
    deltas = deltas[
        (deltas["metric_name"] == "paired_pure_mavs_gc_vs_baseline")
        & (deltas["aggregation_grain"] == expected["baseline_summary_grain"])
    ].copy()
    rows: list[dict[str, Any]] = []
    for source in deltas.to_dict("records"):
        row = {
            "run_mode": source["run_mode"],
            "dataset_id": source["dataset_id"],
            "baseline_system_id": source["baseline_system_id"],
            "system_id": PURE_MAVS_SYSTEM,
            "specialist_composition_id": source["specialist_composition_id"],
            "mean_correctness_delta": source["delta_value"],
            "direction_vs_baseline": source["direction_vs_baseline"],
            "decision_pairwise_agreement": source["decision_pairwise_agreement"],
            "mean_abs_probability_difference": source["mean_abs_probability_difference"],
            "row_count": source["row_count"],
            "source_metric_manifest_hash": metric_manifest[
                "reproducibility_metric_manifest_hash"
            ],
            "source_metric_artifact_hash": metric_manifest["artifact_hashes"][
                f"{source['run_mode']}_metric_rows"
            ],
        }
        row["table_row_id"] = sha256_json(row)[:24]
        rows.append(row)
    rows = _sort_rows(rows, DELTA_TABLE_FIELDS)
    # console.log: phase5 system delta table derivation completed.
    console.log(f"phase5.tables.deltas.complete rows={len(rows)}")
    return rows


def _validate_table_coverage(
    outputs: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
) -> None:
    expected = config["expected"]
    variance = outputs["variance_tables"]
    stability = outputs["stability_tables"]
    deltas = outputs["reproducibility_system_deltas"]
    expected_variance_count = (
        len(expected["run_modes"])
        * len(expected["datasets"])
        * len(expected["systems"])
        * len(expected["specialist_compositions"])
        * len(expected["variance_metrics"])
    )
    expected_delta_count = (
        len(expected["run_modes"])
        * len(expected["datasets"])
        * len(BASELINE_SYSTEMS)
        * len(expected["specialist_compositions"])
    )
    if len(variance) != expected_variance_count:
        raise RuntimeError(
            f"Variance table row count mismatch: {len(variance)} != {expected_variance_count}"
        )
    if len(deltas) != expected_delta_count:
        raise RuntimeError(f"Delta table row count mismatch: {len(deltas)} != {expected_delta_count}")
    if not stability:
        raise RuntimeError("Stability table is empty")
    _require_values(variance, "dataset_id", expected["datasets"])
    _require_values(variance, "system_id", expected["systems"])
    _require_values(variance, "run_mode", expected["run_modes"])
    _require_values(deltas, "baseline_system_id", expected["baselines"])
    trace_rows = [row for row in stability if row["metric_name"] == "trace_stability"]
    _require_values(trace_rows, "trace_field", expected["trace_fields"])


def _load_metric_manifest(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = repo_root / config["input_paths"]["metric_manifest"]
    manifest = load_json_config(path)
    if manifest.get("status") != "pass":
        raise RuntimeError(f"Metric manifest is not pass: {path}")
    if manifest.get("training_performed") is not False:
        raise RuntimeError("Phase 5 requires Phase 4 metrics with training_performed=false")
    return manifest


def _read_metric_csv(repo_root: Path, config: dict[str, Any], key: str) -> pd.DataFrame:
    path = repo_root / config["input_paths"][key]
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # console.log: phase5 report CSV write begins.
    console.log(f"phase5.tables.csv_write.start path={path} rows={len(rows)}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    # console.log: phase5 report CSV write completed.
    console.log(f"phase5.tables.csv_write.complete path={path}")


def _variance_ci_key(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        row["run_mode"],
        row["dataset_id"],
        row["system_id"],
        row["specialist_composition_id"],
        row["compared_metric"],
    )


def _primary_stability_value(row: dict[str, Any]) -> tuple[str, str]:
    metric_name = row["metric_name"]
    if metric_name == "prediction_stability":
        return "binary_pairwise_agreement", row["binary_pairwise_agreement"]
    if metric_name == "decision_stability":
        return "decision_pairwise_agreement", row["decision_pairwise_agreement"]
    if metric_name == "consensus_stability":
        if row["consensus_pairwise_stability"]:
            return "consensus_pairwise_stability", row["consensus_pairwise_stability"]
        return "score_probability_pairwise_stability", row["score_probability_pairwise_stability"]
    if metric_name == "trace_stability":
        return "normalized_trace_similarity", row["normalized_trace_similarity"]
    if metric_name == "run_to_run_agreement":
        return "kappa_agreement", row["kappa_agreement"]
    raise ValueError(f"Unsupported stability metric: {metric_name}")


def _secondary_stability_value(row: dict[str, Any]) -> tuple[str, str]:
    metric_name = row["metric_name"]
    if metric_name in {"prediction_stability", "decision_stability", "consensus_stability"}:
        return "mean_abs_probability_difference", row["mean_abs_probability_difference"]
    if metric_name == "trace_stability":
        return "field_exact_repeat_rate", row["field_exact_repeat_rate"]
    if metric_name == "run_to_run_agreement":
        return "binary_pairwise_agreement", row["binary_pairwise_agreement"]
    return "", ""


def _require_values(rows: list[dict[str, Any]], field: str, expected_values: list[str]) -> None:
    observed = {row[field] for row in rows}
    missing = sorted(set(expected_values) - observed)
    if missing:
        raise RuntimeError(f"Missing {field} values: {missing}")


def _sort_rows(rows: list[dict[str, Any]], fieldnames: list[str]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda row: tuple(str(row.get(field, "")) for field in fieldnames[1:]))


def table_hashes(repo_root: Path, config: dict[str, Any]) -> dict[str, str]:
    """Return SHA-256 hashes for generated Phase 5 report tables."""

    return {
        name: sha256_file(repo_root / config["output_paths"][name])
        for name in [
            "variance_tables",
            "stability_tables",
            "reproducibility_system_deltas",
        ]
    }
