"""Phase 6 corruption stability table builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.corruption_metrics import STABILITY_METRICS
from mavs_ch10c.verification.hash_utils import sha256_json

STABILITY_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "corruption_family",
    "corruption_level",
    "metric_name",
    "reported_value_name",
    "reported_value",
    "secondary_value_name",
    "secondary_value",
    "source_run_count",
    "benchmark_row_count",
    "clean_anchor",
    "clean_anchor_source",
    "source_corruption_manifest_hash",
    "source_corruption_artifact_hash",
]


def build_corruption_stability_rows(
    repo_root: Path,
    config: dict[str, Any],
    summary_rows: list[dict[str, Any]],
    manifest_hash: str,
) -> list[dict[str, Any]]:
    """Build long-form Phase 6 stability rows."""

    # console.log: phase6 corruption stability table build begins.
    console.log("phase6.stability.build.start")
    clean_anchors = _load_phase5_stability_anchors(repo_root, config)
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        for metric_name in STABILITY_METRICS:
            value_field = f"{metric_name}_mean"
            row = {
                "run_mode": summary["run_mode"],
                "dataset_id": summary["dataset_id"],
                "system_id": summary["system_id"],
                "specialist_composition_id": summary["specialist_composition_id"],
                "corruption_family": summary["corruption_family"],
                "corruption_level": summary["corruption_level"],
                "metric_name": metric_name,
                "reported_value_name": metric_name,
                "reported_value": summary[value_field],
                "secondary_value_name": "metric_standard_deviation",
                "secondary_value": summary[f"{metric_name}_standard_deviation"],
                "source_run_count": summary["source_run_count"],
                "benchmark_row_count": summary["benchmark_row_count"],
                "clean_anchor": summary["clean_anchor"],
                "clean_anchor_source": "",
                "source_corruption_manifest_hash": manifest_hash,
                "source_corruption_artifact_hash": summary["corruption_summary_hash"],
            }
            if float(summary["corruption_level"]) == 0.0:
                anchor = clean_anchors.get(
                    (
                        summary["run_mode"],
                        summary["dataset_id"],
                        summary["system_id"],
                        summary["specialist_composition_id"],
                        metric_name,
                    )
                )
                if anchor is not None:
                    row["reported_value"] = anchor
                    row["clean_anchor_source"] = config["source_manifests"][
                        "phase5_clean_stability_table"
                    ]
            row["table_row_id"] = sha256_json(row)[:24]
            rows.append(row)
    _validate_stability_rows(config, rows)
    # console.log: phase6 corruption stability table build completed.
    console.log(f"phase6.stability.build.complete rows={len(rows)}")
    return sorted(rows, key=lambda row: tuple(str(row[field]) for field in STABILITY_FIELDS[1:]))


def _load_phase5_stability_anchors(
    repo_root: Path,
    config: dict[str, Any],
) -> dict[tuple[str, str, str, str, str], str]:
    # console.log: phase6 Phase 5 stability clean-anchor loading begins.
    console.log("phase6.stability.clean_anchor.start")
    path = repo_root / config["source_manifests"]["phase5_clean_stability_table"]
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame["reported_value_numeric"] = pd.to_numeric(frame["reported_value"], errors="coerce")
    grouped = (
        frame.dropna(subset=["reported_value_numeric"])
        .groupby(
            [
                "run_mode",
                "dataset_id",
                "system_id",
                "specialist_composition_id",
                "metric_name",
            ],
            dropna=False,
        )["reported_value_numeric"]
        .mean()
    )
    anchors = {
        tuple(str(part) for part in key): f"{float(value):.15g}"
        for key, value in grouped.to_dict().items()
    }
    # console.log: phase6 Phase 5 stability clean-anchor loading completed.
    console.log(f"phase6.stability.clean_anchor.complete rows={len(anchors)}")
    return anchors


def _validate_stability_rows(config: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    # console.log: phase6 corruption stability coverage validation begins.
    console.log("phase6.stability.coverage.start")
    expected = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["stability_metrics"])
    )
    if len(rows) != expected:
        raise RuntimeError(f"Phase 6 stability row count mismatch: {len(rows)} != {expected}")
    observed_metrics = {row["metric_name"] for row in rows}
    if observed_metrics != set(config["stability_metrics"]):
        raise RuntimeError(f"Phase 6 stability metric coverage mismatch: {observed_metrics}")
    # console.log: phase6 corruption stability coverage validation completed.
    console.log(f"phase6.stability.coverage.complete rows={len(rows)}")

