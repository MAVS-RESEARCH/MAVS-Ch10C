"""Phase 6 corruption confidence-interval table builder."""

from __future__ import annotations

from typing import Any

from mavs_ch10c import console
from mavs_ch10c.corruption_metrics import CONFIDENCE_METRICS
from mavs_ch10c.corruption_metrics.stability import STABILITY_FIELDS
from mavs_ch10c.verification.hash_utils import sha256_json


def build_corruption_confidence_rows(
    config: dict[str, Any],
    summary_rows: list[dict[str, Any]],
    manifest_hash: str,
) -> list[dict[str, Any]]:
    """Build confidence metric rows using the stability table schema."""

    # console.log: phase6 corruption confidence table build begins.
    console.log("phase6.confidence.build.start")
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        for metric_name in CONFIDENCE_METRICS:
            row = {
                "run_mode": summary["run_mode"],
                "dataset_id": summary["dataset_id"],
                "system_id": summary["system_id"],
                "specialist_composition_id": summary["specialist_composition_id"],
                "corruption_family": summary["corruption_family"],
                "corruption_level": summary["corruption_level"],
                "metric_name": metric_name,
                "reported_value_name": metric_name,
                "reported_value": summary[metric_name],
                "secondary_value_name": "accuracy_standard_deviation",
                "secondary_value": summary["accuracy_standard_deviation"],
                "source_run_count": summary["source_run_count"],
                "benchmark_row_count": summary["benchmark_row_count"],
                "clean_anchor": summary["clean_anchor"],
                "clean_anchor_source": "",
                "source_corruption_manifest_hash": manifest_hash,
                "source_corruption_artifact_hash": summary["corruption_summary_hash"],
            }
            row["table_row_id"] = sha256_json(row)[:24]
            rows.append(row)
    _validate_confidence_rows(config, rows)
    # console.log: phase6 corruption confidence table build completed.
    console.log(f"phase6.confidence.build.complete rows={len(rows)}")
    return sorted(rows, key=lambda row: tuple(str(row[field]) for field in STABILITY_FIELDS[1:]))


def _validate_confidence_rows(config: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    # console.log: phase6 corruption confidence coverage validation begins.
    console.log("phase6.confidence.coverage.start")
    expected = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["confidence_metrics"])
    )
    if len(rows) != expected:
        raise RuntimeError(f"Phase 6 confidence row count mismatch: {len(rows)} != {expected}")
    observed_metrics = {row["metric_name"] for row in rows}
    if observed_metrics != set(config["confidence_metrics"]):
        raise RuntimeError(f"Phase 6 confidence metric coverage mismatch: {observed_metrics}")
    # console.log: phase6 corruption confidence coverage validation completed.
    console.log(f"phase6.confidence.coverage.complete rows={len(rows)}")

