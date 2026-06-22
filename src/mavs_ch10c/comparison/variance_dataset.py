"""Build Phase 3 variance benchmark datasets from Phase 2 corpus outputs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.comparison.alignment import (
    coverage_summary,
    group_aligned_rows,
    load_corpus_index,
    validate_aligned_groups,
)
from mavs_ch10c.comparison.baseline_deltas import build_delta_rows
from mavs_ch10c.comparison.system_outputs import normalize_system_output
from mavs_ch10c.comparison.system_outputs import TRACE_FIELD_COLUMNS
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file, write_json


def build_variance_benchmark_dataset(repo_root: Path) -> dict[str, Any]:
    """Build locked, audit, and delta variance benchmark artifacts."""

    # console.log: phase3 variance dataset build begins.
    console.log("phase3.variance_dataset.build.start")
    output_dir = repo_root / "results" / "variance_benchmarks"
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_manifest = _load_existing_variance_manifest_if_valid(repo_root, output_dir)
    if existing_manifest is not None:
        # console.log: phase3 variance dataset cache hit.
        console.log(
            "phase3.variance_dataset.build.cache_hit "
            f"hash={existing_manifest['variance_dataset_manifest_hash']}"
        )
        return existing_manifest

    locked_result = _build_mode(repo_root, "locked", output_dir / "locked_variance_rows.csv")
    audit_result = _build_mode(repo_root, "audit", output_dir / "audit_variance_rows.csv")
    delta_rows = locked_result["delta_rows"] + audit_result["delta_rows"]
    delta_path = output_dir / "system_delta_rows.csv"
    _write_csv(delta_path, delta_rows)

    locked_path = output_dir / "locked_variance_rows.csv"
    audit_path = output_dir / "audit_variance_rows.csv"
    manifest = {
        "status": "pass",
        "phase": "phase3_variance_benchmark_dataset",
        "source_backend": "empirical_sklearn_repeated_training",
        "empirical_prediction_available": True,
        "locked": locked_result["summary"],
        "audit": audit_result["summary"],
        "delta_row_count": len(delta_rows),
        "pure_mavs_delta_baselines": [
            "single_model",
            "mean_ensemble",
            "static_weighted_ensemble",
            "veto_mavs",
        ],
        "static_weight_policy": "imported_frozen_ch10a_config",
        "trace_field_columns": TRACE_FIELD_COLUMNS,
        "trace_fields_available_for_phase4": True,
        "missing_units": [],
        "artifact_hashes": {
            "locked_variance_rows": sha256_file(locked_path),
            "audit_variance_rows": sha256_file(audit_path),
            "system_delta_rows": sha256_file(delta_path),
            "locked_corpus_manifest": load_json_config(
                repo_root / "results" / "execution_corpus" / "locked" / "corpus_manifest.json"
            )["corpus_manifest_hash"],
            "audit_corpus_manifest": load_json_config(
                repo_root / "results" / "execution_corpus" / "audit" / "corpus_manifest.json"
            )["corpus_manifest_hash"],
        },
    }
    manifest_hash = write_json(output_dir / "variance_dataset_manifest.json", manifest)
    manifest["variance_dataset_manifest_hash"] = manifest_hash
    write_json(output_dir / "variance_dataset_manifest.json", manifest)
    # console.log: phase3 variance dataset build completed.
    console.log(
        "phase3.variance_dataset.build.complete "
        f"locked={locked_result['summary']['row_count']} audit={audit_result['summary']['row_count']} deltas={len(delta_rows)}"
    )
    return manifest


def _load_existing_variance_manifest_if_valid(
    repo_root: Path, output_dir: Path
) -> dict[str, Any] | None:
    manifest_path = output_dir / "variance_dataset_manifest.json"
    locked_path = output_dir / "locked_variance_rows.csv"
    audit_path = output_dir / "audit_variance_rows.csv"
    delta_path = output_dir / "system_delta_rows.csv"
    if not all(path.exists() for path in [manifest_path, locked_path, audit_path, delta_path]):
        return None
    try:
        manifest = load_json_config(manifest_path)
    except Exception:
        return None
    if manifest.get("status") != "pass":
        return None
    if manifest.get("source_backend") != "empirical_sklearn_repeated_training":
        return None
    if manifest.get("empirical_prediction_available") is not True:
        return None
    if manifest.get("trace_fields_available_for_phase4") is not True:
        return None
    if manifest.get("trace_field_columns") != TRACE_FIELD_COLUMNS:
        return None
    if not _variance_rows_have_trace_fields(locked_path):
        return None
    if not _variance_rows_have_trace_fields(audit_path):
        return None
    try:
        locked_hash = load_json_config(
            repo_root / "results" / "execution_corpus" / "locked" / "corpus_manifest.json"
        )["corpus_manifest_hash"]
        audit_hash = load_json_config(
            repo_root / "results" / "execution_corpus" / "audit" / "corpus_manifest.json"
        )["corpus_manifest_hash"]
    except Exception:
        return None
    artifact_hashes = manifest.get("artifact_hashes", {})
    if artifact_hashes.get("locked_variance_rows") != sha256_file(locked_path):
        return None
    if artifact_hashes.get("audit_variance_rows") != sha256_file(audit_path):
        return None
    if artifact_hashes.get("system_delta_rows") != sha256_file(delta_path):
        return None
    if artifact_hashes.get("locked_corpus_manifest") != locked_hash:
        return None
    if artifact_hashes.get("audit_corpus_manifest") != audit_hash:
        return None
    return manifest


def _build_mode(repo_root: Path, run_mode: str, output_path: Path) -> dict[str, Any]:
    # console.log: phase3 per-mode variance build begins.
    console.log(f"phase3.variance_dataset.mode.start mode={run_mode}")
    corpus_path = (
        repo_root / "results" / "execution_corpus" / run_mode / "predictions_index.csv"
    )
    trace_path = repo_root / "results" / "execution_corpus" / run_mode / "trace_index.csv"
    rows = load_corpus_index(corpus_path)
    trace_rows = _load_trace_fields(trace_path)
    groups = group_aligned_rows(rows)
    validate_aligned_groups(groups)
    variance_rows = [
        normalize_system_output(_attach_trace_fields(row, trace_rows))
        for group in groups.values()
        for row in sorted(group, key=lambda item: item["system_id"])
    ]
    _write_csv(output_path, variance_rows)
    delta_rows = build_delta_rows(groups)
    summary = coverage_summary(groups)
    summary["variance_row_count"] = len(variance_rows)
    summary["delta_row_count"] = len(delta_rows)
    # console.log: phase3 per-mode variance build completed.
    console.log(
        f"phase3.variance_dataset.mode.complete mode={run_mode} rows={len(variance_rows)} deltas={len(delta_rows)}"
    )
    return {"summary": summary, "delta_rows": delta_rows}


def _load_trace_fields(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    # console.log: phase3 governance trace field load begins.
    console.log(f"phase3.variance_dataset.trace_load.start path={path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = {
            (row["run_id"], row["row_hash"]): {
                "trace_s": row["s"],
                "trace_r": row["r"],
                "trace_z": row["z"],
                "trace_a": row["a"],
                "trace_w": row["w"],
                "trace_m": row["m"],
                "trace_theta": row["theta"],
                "trace_R": row["R"],
                "trace_hard_veto": row["hard_veto"],
                "trace_decision": row["decision"],
            }
            for row in csv.DictReader(handle)
        }
    # console.log: phase3 governance trace field load completed.
    console.log(f"phase3.variance_dataset.trace_load.complete rows={len(rows)}")
    return rows


def _attach_trace_fields(
    row: dict[str, Any],
    trace_rows: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    fields = trace_rows.get((row["run_id"], row["row_hash"]))
    if fields is None:
        return {**row, **{field: "" for field in TRACE_FIELD_COLUMNS}}
    return {**row, **fields}


def _variance_rows_have_trace_fields(path: Path) -> bool:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return bool(reader.fieldnames) and set(TRACE_FIELD_COLUMNS).issubset(reader.fieldnames)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    # console.log: phase3 CSV write begins.
    console.log(f"phase3.variance_dataset.csv_write.start path={path} rows={len(rows)}")
    if not rows:
        raise ValueError(f"Cannot write empty Phase 3 CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    # console.log: phase3 CSV write completed.
    console.log(f"phase3.variance_dataset.csv_write.complete path={path}")
