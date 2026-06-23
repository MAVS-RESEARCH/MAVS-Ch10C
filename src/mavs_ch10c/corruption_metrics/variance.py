"""Phase 6 corruption variance table builder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.corruption_metrics import VARIANCE_METRIC_TO_SOURCE
from mavs_ch10c.verification.hash_utils import sha256_json

VARIANCE_FIELDS = [
    "table_row_id",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "corruption_family",
    "corruption_level",
    "metric_name",
    "compared_metric",
    "mean_metric_value",
    "sample_variance",
    "standard_deviation",
    "source_run_count",
    "benchmark_row_count",
    "clean_anchor",
    "clean_anchor_source",
    "source_corruption_manifest_hash",
    "source_corruption_artifact_hash",
]


def build_corruption_variance_rows(
    repo_root: Path,
    config: dict[str, Any],
    summary_rows: list[dict[str, Any]],
    manifest_hash: str,
) -> list[dict[str, Any]]:
    """Build long-form Phase 6 variance rows."""

    # console.log: phase6 corruption variance table build begins.
    console.log("phase6.variance.build.start")
    clean_anchors = _load_phase5_variance_anchors(repo_root, config)
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        for metric_name, source_metric in VARIANCE_METRIC_TO_SOURCE.items():
            row = _variance_row(summary, metric_name, source_metric, manifest_hash)
            if float(summary["corruption_level"]) == 0.0 and metric_name in {
                "accuracy_variance",
                "f1_variance",
            }:
                anchor = clean_anchors.get(
                    (
                        summary["run_mode"],
                        summary["dataset_id"],
                        summary["system_id"],
                        summary["specialist_composition_id"],
                        metric_name,
                    )
                )
                if anchor:
                    row["mean_metric_value"] = anchor["mean_metric_value"]
                    row["sample_variance"] = anchor["sample_variance"]
                    row["standard_deviation"] = anchor["standard_deviation"]
                    row["clean_anchor_source"] = config["source_manifests"][
                        "phase5_clean_variance_table"
                    ]
            row["table_row_id"] = sha256_json(row)[:24]
            rows.append(row)
    _validate_variance_rows(config, rows)
    # console.log: phase6 corruption variance table build completed.
    console.log(f"phase6.variance.build.complete rows={len(rows)}")
    return sorted(rows, key=lambda row: tuple(str(row[field]) for field in VARIANCE_FIELDS[1:]))


def _variance_row(
    summary: dict[str, Any],
    metric_name: str,
    source_metric: str,
    manifest_hash: str,
) -> dict[str, Any]:
    return {
        "run_mode": summary["run_mode"],
        "dataset_id": summary["dataset_id"],
        "system_id": summary["system_id"],
        "specialist_composition_id": summary["specialist_composition_id"],
        "corruption_family": summary["corruption_family"],
        "corruption_level": summary["corruption_level"],
        "metric_name": metric_name,
        "compared_metric": source_metric,
        "mean_metric_value": summary[f"{source_metric}_mean"],
        "sample_variance": summary[f"{source_metric}_variance"],
        "standard_deviation": summary[f"{source_metric}_standard_deviation"],
        "source_run_count": summary["source_run_count"],
        "benchmark_row_count": summary["benchmark_row_count"],
        "clean_anchor": summary["clean_anchor"],
        "clean_anchor_source": "",
        "source_corruption_manifest_hash": manifest_hash,
        "source_corruption_artifact_hash": summary["corruption_summary_hash"],
    }


def _load_phase5_variance_anchors(
    repo_root: Path,
    config: dict[str, Any],
) -> dict[tuple[str, str, str, str, str], dict[str, str]]:
    # console.log: phase6 Phase 5 variance clean-anchor loading begins.
    console.log("phase6.variance.clean_anchor.start")
    path = repo_root / config["source_manifests"]["phase5_clean_variance_table"]
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    anchors: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for row in frame.to_dict("records"):
        anchors[
            (
                row["run_mode"],
                row["dataset_id"],
                row["system_id"],
                row["specialist_composition_id"],
                row["metric_name"],
            )
        ] = row
    # console.log: phase6 Phase 5 variance clean-anchor loading completed.
    console.log(f"phase6.variance.clean_anchor.complete rows={len(anchors)}")
    return anchors


def _validate_variance_rows(config: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    # console.log: phase6 corruption variance coverage validation begins.
    console.log("phase6.variance.coverage.start")
    expected = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["variance_metrics"])
    )
    if len(rows) != expected:
        raise RuntimeError(f"Phase 6 variance row count mismatch: {len(rows)} != {expected}")
    observed_metrics = {row["metric_name"] for row in rows}
    if observed_metrics != set(config["variance_metrics"]):
        raise RuntimeError(f"Phase 6 variance metric coverage mismatch: {observed_metrics}")
    # console.log: phase6 corruption variance coverage validation completed.
    console.log(f"phase6.variance.coverage.complete rows={len(rows)}")

