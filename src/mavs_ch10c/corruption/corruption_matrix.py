"""Corruption-aware reproducibility matrix builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import sha256_file, sha256_json


def build_corruption_matrix_manifest(
    repo_root: Path,
    config: dict[str, Any],
    suite: dict[str, Any],
) -> dict[str, Any]:
    """Build the Phase 6 matrix manifest from frozen Phase 2 corpus indexes."""

    # console.log: phase6 corruption matrix build begins.
    console.log("phase6.corruption_matrix.build.start")
    run_mode_manifests = {}
    total_source_rows = 0
    total_expected_rows = 0
    for run_mode in config["run_modes"]:
        source_path = repo_root / config["source_corpus_paths"][run_mode]
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        frame = pd.read_csv(source_path, dtype=str, keep_default_na=False)
        coverage = _coverage_for_run_mode(frame, config, run_mode)
        expected_expanded = len(frame) * len(config["families"]) * len(config["levels"])
        run_mode_manifests[run_mode] = {
            "source_path": str(source_path),
            "source_sha256": sha256_file(source_path),
            "source_run_rows": len(frame),
            "expected_corruption_rows": expected_expanded,
            "coverage": coverage,
            "missing_units": [],
        }
        total_source_rows += len(frame)
        total_expected_rows += expected_expanded
    manifest = {
        "phase": "phase6_corruption_matrix",
        "status": "pass",
        "matrix_grain": config["summary_aggregation_grain"],
        "run_modes": config["run_modes"],
        "datasets": config["datasets"],
        "systems": config["systems"],
        "specialist_compositions": config["specialist_compositions"],
        "corruption_families": suite["families"],
        "corruption_levels": suite["levels"],
        "source_run_rows": total_source_rows,
        "expected_expanded_run_rows": total_expected_rows,
        "run_modes_detail": run_mode_manifests,
        "locked_audit_separation_preserved": True,
        "clean_anchor_level": 0.0,
        "shadow_verification_used_as_final_evidence": False,
        "suite_hash": suite["suite_hash"],
    }
    manifest["corruption_matrix_hash"] = sha256_json(manifest)
    # console.log: phase6 corruption matrix build completed.
    console.log(
        "phase6.corruption_matrix.build.complete "
        f"source_rows={total_source_rows} expected_expanded_rows={total_expected_rows}"
    )
    return manifest


def _coverage_for_run_mode(
    frame: pd.DataFrame,
    config: dict[str, Any],
    run_mode: str,
) -> dict[str, Any]:
    # console.log: phase6 corruption matrix run-mode coverage validation begins.
    console.log(f"phase6.corruption_matrix.coverage.start run_mode={run_mode}")
    required_columns = {
        "run_id",
        "dataset_id",
        "system_id",
        "execution_seed",
        "split_schedule_id",
        "initialization_schedule_id",
        "specialist_composition_id",
        "run_mode",
    }
    missing_columns = sorted(required_columns - set(frame.columns))
    if missing_columns:
        raise RuntimeError(f"Corpus index missing required columns: {missing_columns}")
    mode_frame = frame[frame["run_mode"] == run_mode].copy()
    if len(mode_frame) != len(frame):
        raise RuntimeError(f"Corpus path for {run_mode} contains mixed run modes")
    observed_datasets = sorted(mode_frame["dataset_id"].unique().tolist())
    observed_systems = sorted(mode_frame["system_id"].unique().tolist())
    observed_compositions = sorted(mode_frame["specialist_composition_id"].unique().tolist())
    if set(observed_datasets) != set(config["datasets"]):
        raise RuntimeError(f"{run_mode} dataset coverage mismatch: {observed_datasets}")
    if set(observed_systems) != set(config["systems"]):
        raise RuntimeError(f"{run_mode} system coverage mismatch: {observed_systems}")
    if set(observed_compositions) != set(config["specialist_compositions"]):
        raise RuntimeError(f"{run_mode} composition coverage mismatch: {observed_compositions}")
    grouped = mode_frame.groupby(
        [
            "dataset_id",
            "system_id",
            "specialist_composition_id",
        ],
        dropna=False,
    ).size()
    expected_per_group = grouped.iloc[0]
    if not (grouped == expected_per_group).all():
        raise RuntimeError(f"{run_mode} matrix is imbalanced before corruption expansion")
    coverage = {
        "dataset_count": len(observed_datasets),
        "system_count": len(observed_systems),
        "specialist_composition_count": len(observed_compositions),
        "execution_seed_count": int(mode_frame["execution_seed"].nunique()),
        "split_schedule_count": int(mode_frame["split_schedule_id"].nunique()),
        "initialization_schedule_count": int(
            mode_frame["initialization_schedule_id"].nunique()
        ),
        "source_rows_per_dataset_system_composition": int(expected_per_group),
        "source_rows": int(len(mode_frame)),
    }
    # console.log: phase6 corruption matrix run-mode coverage validation completed.
    console.log(
        "phase6.corruption_matrix.coverage.complete "
        f"run_mode={run_mode} rows={coverage['source_rows']}"
    )
    return coverage

