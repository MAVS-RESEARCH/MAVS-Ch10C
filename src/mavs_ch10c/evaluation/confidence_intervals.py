"""Analytical confidence interval widths for Phase 4."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.evaluation.variance import (
    DETAILED_GROUP_COLUMNS,
    SUMMARY_GROUP_COLUMNS,
    _base_group_payload,
)
from mavs_ch10c.verification.hash_utils import sha256_json


def build_confidence_interval_rows(
    execution_units: pd.DataFrame,
    *,
    confidence_level: float,
    z_value: float,
    zero_division_policy: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    """Build predeclared analytical interval widths for accuracy and F1."""

    # console.log: phase4 confidence interval build begins.
    console.log("phase4.confidence_intervals.build.start")
    rows: list[dict[str, Any]] = []
    for metric_column in ["accuracy", "f1"]:
        for group_columns, grain in [
            (DETAILED_GROUP_COLUMNS, "dataset_system_split_init_composition"),
            (SUMMARY_GROUP_COLUMNS, "dataset_system_composition"),
        ]:
            rows.extend(
                _intervals_for_group(
                    execution_units,
                    group_columns,
                    grain,
                    metric_column,
                    confidence_level,
                    z_value,
                    zero_division_policy,
                    source_input_hash,
                )
            )
    _annotate_pure_mavs_width_comparison(rows)
    # console.log: phase4 confidence interval build completed.
    console.log(f"phase4.confidence_intervals.build.complete rows={len(rows)}")
    return rows


def _intervals_for_group(
    execution_units: pd.DataFrame,
    group_columns: list[str],
    aggregation_grain: str,
    metric_column: str,
    confidence_level: float,
    z_value: float,
    zero_division_policy: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in execution_units.groupby(group_columns, dropna=False):
        values = group[metric_column].astype(float).to_numpy()
        count = int(len(values))
        sample_std = float(np.std(values, ddof=1)) if count > 1 else 0.0
        standard_error = sample_std / float(np.sqrt(count)) if count else 0.0
        width = float(2.0 * z_value * standard_error)
        payload = _base_group_payload(group_columns, key)
        payload.update(
            {
                "metric_family": "confidence_interval_width",
                "metric_name": f"{metric_column}_confidence_interval_width",
                "aggregation_grain": aggregation_grain,
                "compared_metric": metric_column,
                "repetition_unit_count": count,
                "mean_value": float(np.mean(values)) if count else 0.0,
                "standard_deviation": sample_std,
                "standard_error": standard_error,
                "confidence_level": confidence_level,
                "confidence_method": "analytical_repeated_unit_normal",
                "confidence_interval_width": width,
                "zero_division_policy": zero_division_policy,
                "source_input_hash": source_input_hash,
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
        payload["metric_row_id"] = sha256_json(
            {
                "metric_family": payload["metric_family"],
                "metric_name": payload["metric_name"],
                "aggregation_grain": payload["aggregation_grain"],
                "run_mode": payload["run_mode"],
                "dataset_id": payload["dataset_id"],
                "system_id": payload["system_id"],
                "split_schedule_id": payload["split_schedule_id"],
                "initialization_schedule_id": payload["initialization_schedule_id"],
                "specialist_composition_id": payload["specialist_composition_id"],
            }
        )[:24]
        rows.append(payload)
    return rows


def _annotate_pure_mavs_width_comparison(rows: list[dict[str, Any]]) -> None:
    pure_lookup = {
        (
            row["run_mode"],
            row["dataset_id"],
            row["split_schedule_id"],
            row["initialization_schedule_id"],
            row["specialist_composition_id"],
            row["aggregation_grain"],
            row["compared_metric"],
        ): float(row["confidence_interval_width"])
        for row in rows
        if row["system_id"] == "pure_mavs_gc"
    }
    for row in rows:
        key = (
            row["run_mode"],
            row["dataset_id"],
            row["split_schedule_id"],
            row["initialization_schedule_id"],
            row["specialist_composition_id"],
            row["aggregation_grain"],
            row["compared_metric"],
        )
        pure_width = pure_lookup.get(key)
        if pure_width is None or row["system_id"] == "pure_mavs_gc":
            row["pure_mavs_reference_value"] = "" if pure_width is None else pure_width
            row["ci_width_comparison_to_pure"] = "reference" if row["system_id"] == "pure_mavs_gc" else "not_available"
            continue
        current_width = float(row["confidence_interval_width"])
        row["pure_mavs_reference_value"] = pure_width
        if abs(current_width - pure_width) <= 1e-12:
            row["ci_width_comparison_to_pure"] = "indistinguishable"
        elif pure_width < current_width:
            row["ci_width_comparison_to_pure"] = "pure_mavs_narrower"
        else:
            row["ci_width_comparison_to_pure"] = "pure_mavs_wider"
