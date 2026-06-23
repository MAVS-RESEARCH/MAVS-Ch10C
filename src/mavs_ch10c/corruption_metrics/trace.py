"""Phase 6 corruption trace-stability table builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import sha256_json

TRACE_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "corruption_family",
    "corruption_level",
    "trace_field",
    "trace_stability",
    "trace_stability_variance",
    "source_run_count",
    "clean_anchor",
    "clean_anchor_source",
    "source_corruption_manifest_hash",
    "source_corruption_artifact_hash",
]


def build_corruption_trace_rows(
    repo_root: Path,
    config: dict[str, Any],
    trace_rows: list[dict[str, Any]],
    manifest_hash: str,
) -> list[dict[str, Any]]:
    """Build Phase 6 trace stability rows."""

    # console.log: phase6 corruption trace table build begins.
    console.log("phase6.trace.build.start")
    clean_anchors = _load_phase5_trace_anchors(repo_root, config)
    rows: list[dict[str, Any]] = []
    for source in trace_rows:
        row = {
            "run_mode": source["run_mode"],
            "dataset_id": source["dataset_id"],
            "system_id": source["system_id"],
            "specialist_composition_id": source["specialist_composition_id"],
            "corruption_family": source["corruption_family"],
            "corruption_level": source["corruption_level"],
            "trace_field": source["trace_field"],
            "trace_stability": source["trace_stability"],
            "trace_stability_variance": source["trace_stability_variance"],
            "source_run_count": source["source_run_count"],
            "clean_anchor": source["clean_anchor"],
            "clean_anchor_source": "",
            "source_corruption_manifest_hash": manifest_hash,
            "source_corruption_artifact_hash": source["trace_row_hash"],
        }
        if float(source["corruption_level"]) == 0.0:
            anchor = clean_anchors.get(
                (
                    source["run_mode"],
                    source["dataset_id"],
                    source["system_id"],
                    source["specialist_composition_id"],
                    source["trace_field"],
                )
            )
            if anchor is not None:
                row["trace_stability"] = anchor
                row["clean_anchor_source"] = config["source_manifests"][
                    "phase5_clean_stability_table"
                ]
        row["table_row_id"] = sha256_json(row)[:24]
        rows.append(row)
    _validate_trace_rows(config, rows)
    # console.log: phase6 corruption trace table build completed.
    console.log(f"phase6.trace.build.complete rows={len(rows)}")
    return sorted(rows, key=lambda row: tuple(str(row[field]) for field in TRACE_FIELDS[1:]))


def _load_phase5_trace_anchors(
    repo_root: Path,
    config: dict[str, Any],
) -> dict[tuple[str, str, str, str, str], str]:
    # console.log: phase6 Phase 5 trace clean-anchor loading begins.
    console.log("phase6.trace.clean_anchor.start")
    path = repo_root / config["source_manifests"]["phase5_clean_stability_table"]
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame = frame[frame["metric_name"] == "trace_stability"].copy()
    anchors: dict[tuple[str, str, str, str, str], str] = {}
    for row in frame.to_dict("records"):
        anchors[
            (
                row["run_mode"],
                row["dataset_id"],
                row["system_id"],
                row["specialist_composition_id"],
                row["trace_field"],
            )
        ] = row["reported_value"]
    # console.log: phase6 Phase 5 trace clean-anchor loading completed.
    console.log(f"phase6.trace.clean_anchor.complete rows={len(anchors)}")
    return anchors


def _validate_trace_rows(config: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    # console.log: phase6 corruption trace coverage validation begins.
    console.log("phase6.trace.coverage.start")
    expected = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["governance_systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["trace_fields"])
    )
    if len(rows) != expected:
        raise RuntimeError(f"Phase 6 trace row count mismatch: {len(rows)} != {expected}")
    observed_fields = {row["trace_field"] for row in rows}
    if observed_fields != set(config["trace_fields"]):
        raise RuntimeError(f"Phase 6 trace field coverage mismatch: {observed_fields}")
    # console.log: phase6 corruption trace coverage validation completed.
    console.log(f"phase6.trace.coverage.complete rows={len(rows)}")

