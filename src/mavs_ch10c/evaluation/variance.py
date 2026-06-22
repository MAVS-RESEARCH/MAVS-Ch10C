"""Accuracy and F1 variance definitions for Phase 4."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import sha256_json

RUN_UNIT_COLUMNS = [
    "run_mode",
    "dataset_id",
    "system_id",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
    "execution_seed",
    "run_id",
]

SUMMARY_GROUP_COLUMNS = [
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
]

DETAILED_GROUP_COLUMNS = [
    "run_mode",
    "dataset_id",
    "system_id",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
]


def build_execution_unit_metrics(
    rows: pd.DataFrame, zero_division_policy: str
) -> pd.DataFrame:
    """Compute run-level accuracy and F1 from row-level variance records."""

    # console.log: phase4 execution-unit metric computation begins.
    console.log(f"phase4.variance.execution_units.start rows={len(rows)}")
    numeric = rows.copy()
    for column in ["correctness", "f1_tp", "f1_fp", "f1_fn", "f1_tn"]:
        numeric[column] = pd.to_numeric(numeric[column])
    grouped = numeric.groupby(RUN_UNIT_COLUMNS, dropna=False).agg(
        row_count=("variance_row_id", "count"),
        correct_count=("correctness", "sum"),
        tp=("f1_tp", "sum"),
        fp=("f1_fp", "sum"),
        fn=("f1_fn", "sum"),
        tn=("f1_tn", "sum"),
    )
    grouped = grouped.reset_index()
    grouped["accuracy"] = grouped["correct_count"] / grouped["row_count"]
    denominator = (2.0 * grouped["tp"]) + grouped["fp"] + grouped["fn"]
    grouped["f1"] = np.where(
        denominator > 0.0,
        (2.0 * grouped["tp"]) / denominator,
        0.0,
    )
    grouped["zero_division_policy"] = zero_division_policy
    # console.log: phase4 execution-unit metric computation completed.
    console.log(f"phase4.variance.execution_units.complete units={len(grouped)}")
    return grouped


def build_metric_variance_rows(
    execution_units: pd.DataFrame,
    metric_column: str,
    metric_family: str,
    zero_division_policy: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    """Build sample variance rows for detailed and summary grains."""

    # console.log: phase4 metric variance build begins.
    console.log(f"phase4.variance.metric_rows.start metric={metric_family}")
    rows: list[dict[str, Any]] = []
    rows.extend(
        _variance_for_group(
            execution_units,
            DETAILED_GROUP_COLUMNS,
            metric_column,
            metric_family,
            "dataset_system_split_init_composition",
            zero_division_policy,
            source_input_hash,
        )
    )
    rows.extend(
        _variance_for_group(
            execution_units,
            SUMMARY_GROUP_COLUMNS,
            metric_column,
            metric_family,
            "dataset_system_composition",
            zero_division_policy,
            source_input_hash,
        )
    )
    # console.log: phase4 metric variance build completed.
    console.log(f"phase4.variance.metric_rows.complete metric={metric_family} rows={len(rows)}")
    return rows


def _variance_for_group(
    execution_units: pd.DataFrame,
    group_columns: list[str],
    metric_column: str,
    metric_family: str,
    aggregation_grain: str,
    zero_division_policy: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for key, group in execution_units.groupby(group_columns, dropna=False):
        values = group[metric_column].astype(float).to_numpy()
        count = int(len(values))
        variance = float(np.var(values, ddof=1)) if count > 1 else 0.0
        std = float(np.sqrt(variance))
        payload = _base_group_payload(group_columns, key)
        payload.update(
            {
                "metric_family": metric_family,
                "metric_name": metric_family,
                "aggregation_grain": aggregation_grain,
                "compared_metric": metric_column,
                "repetition_unit_count": count,
                "row_count": int(group["row_count"].sum()),
                "mean_value": float(np.mean(values)) if count else 0.0,
                "sample_variance": variance,
                "standard_deviation": std,
                "zero_division_policy": zero_division_policy,
                "source_input_hash": source_input_hash,
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
        payload["metric_row_id"] = sha256_json(
            {
                "metric_family": payload["metric_family"],
                "aggregation_grain": payload["aggregation_grain"],
                "run_mode": payload["run_mode"],
                "dataset_id": payload["dataset_id"],
                "system_id": payload["system_id"],
                "split_schedule_id": payload["split_schedule_id"],
                "initialization_schedule_id": payload["initialization_schedule_id"],
                "specialist_composition_id": payload["specialist_composition_id"],
            }
        )[:24]
        results.append(payload)
    return results


def _base_group_payload(group_columns: list[str], key: Any) -> dict[str, Any]:
    values = key if isinstance(key, tuple) else (key,)
    payload = {
        "run_mode": "",
        "dataset_id": "",
        "system_id": "",
        "split_schedule_id": "all",
        "initialization_schedule_id": "all",
        "specialist_composition_id": "",
    }
    for column, value in zip(group_columns, values):
        payload[column] = str(value)
    return payload
