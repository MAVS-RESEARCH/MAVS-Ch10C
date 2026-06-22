"""Governance trace stability definitions for Phase 4."""

from __future__ import annotations

import ast
import json
from collections import defaultdict
from math import comb
from typing import Any

import numpy as np
import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.evaluation import GOVERNANCE_SYSTEMS
from mavs_ch10c.evaluation.stability import (
    ROW_ALIGNMENT_COLUMNS,
    mean_pairwise_abs_difference,
)
from mavs_ch10c.evaluation.variance import (
    DETAILED_GROUP_COLUMNS,
    SUMMARY_GROUP_COLUMNS,
    _base_group_payload,
)
from mavs_ch10c.verification.hash_utils import sha256_json

TRACE_FIELDS = [
    "s",
    "r",
    "z",
    "a",
    "w",
    "m",
    "theta",
    "R",
    "hard_veto",
    "decision",
]


def build_trace_stability_rows(
    rows: pd.DataFrame, source_input_hash: str
) -> list[dict[str, Any]]:
    """Compute governance trace field variance and repeat-rate metrics."""

    # console.log: phase4 trace stability build begins.
    console.log("phase4.trace_stability.build.start")
    governance_rows = rows[rows["system_id"].isin(GOVERNANCE_SYSTEMS)].copy()
    output: list[dict[str, Any]] = []
    for trace_field in TRACE_FIELDS:
        scalar_column = f"trace_{trace_field}_scalar"
        canonical_column = f"trace_{trace_field}_canonical"
        scalar_values: list[float] = []
        canonical_values: list[str] = []
        for raw_value in governance_rows[f"trace_{trace_field}"].tolist():
            scalar, canonical = _trace_scalar_and_canonical(raw_value)
            scalar_values.append(scalar)
            canonical_values.append(canonical)
        governance_rows[scalar_column] = scalar_values
        governance_rows[canonical_column] = canonical_values
        for group_columns, grain in [
            (DETAILED_GROUP_COLUMNS, "dataset_system_split_init_composition"),
            (SUMMARY_GROUP_COLUMNS, "dataset_system_composition"),
        ]:
            output.extend(
                _trace_field_for_group(
                    governance_rows,
                    group_columns,
                    grain,
                    trace_field,
                    scalar_column,
                    canonical_column,
                    source_input_hash,
                )
            )
    # console.log: phase4 trace stability build completed.
    console.log(f"phase4.trace_stability.build.complete rows={len(output)}")
    return output


def _trace_field_for_group(
    rows: pd.DataFrame,
    group_columns: list[str],
    aggregation_grain: str,
    trace_field: str,
    scalar_column: str,
    canonical_column: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    accumulators: dict[tuple[Any, ...], dict[str, float]] = defaultdict(
        lambda: {
            "row_alignment_group_count": 0.0,
            "observation_count": 0.0,
            "pair_count": 0.0,
            "field_exact_pairs": 0.0,
            "trace_hash_exact_pairs": 0.0,
            "distance_sum": 0.0,
            "variance_sum": 0.0,
            "variance_count": 0.0,
        }
    )
    grouped = rows.groupby(group_columns + ROW_ALIGNMENT_COLUMNS, dropna=False)
    for key, group in grouped:
        scalar_values = group[scalar_column].astype(float).tolist()
        canonical_values = group[canonical_column].astype(str).tolist()
        trace_hash_values = group["trace_hash"].astype(str).tolist()
        if len(scalar_values) < 2:
            continue
        group_key = tuple(key[: len(group_columns)])
        mean_abs_diff, pair_count = mean_pairwise_abs_difference(scalar_values)
        acc = accumulators[group_key]
        acc["row_alignment_group_count"] += 1
        acc["observation_count"] += len(scalar_values)
        acc["pair_count"] += pair_count
        acc["field_exact_pairs"] += _exact_repeat_pairs(canonical_values)
        acc["trace_hash_exact_pairs"] += _exact_repeat_pairs(trace_hash_values)
        acc["distance_sum"] += mean_abs_diff * pair_count
        acc["variance_sum"] += float(np.var(scalar_values, ddof=1))
        acc["variance_count"] += 1
    output: list[dict[str, Any]] = []
    for key, acc in accumulators.items():
        pair_count = acc["pair_count"]
        distance = acc["distance_sum"] / pair_count if pair_count else 0.0
        payload = _base_group_payload(group_columns, key)
        payload.update(
            {
                "metric_family": "trace_stability",
                "metric_name": "trace_stability",
                "aggregation_grain": aggregation_grain,
                "trace_field": trace_field,
                "row_alignment_group_count": int(acc["row_alignment_group_count"]),
                "observation_count": int(acc["observation_count"]),
                "pair_count": int(pair_count),
                "field_exact_repeat_rate": acc["field_exact_pairs"] / pair_count if pair_count else 0.0,
                "exact_trace_hash_repeat_rate": acc["trace_hash_exact_pairs"] / pair_count if pair_count else 0.0,
                "normalized_trace_distance_mean": distance,
                "normalized_trace_similarity": 1.0 - distance,
                "sample_variance": acc["variance_sum"] / acc["variance_count"] if acc["variance_count"] else 0.0,
                "source_input_hash": source_input_hash,
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
        payload["metric_row_id"] = sha256_json(
            {
                "metric_family": payload["metric_family"],
                "trace_field": trace_field,
                "aggregation_grain": payload["aggregation_grain"],
                "run_mode": payload["run_mode"],
                "dataset_id": payload["dataset_id"],
                "system_id": payload["system_id"],
                "split_schedule_id": payload["split_schedule_id"],
                "initialization_schedule_id": payload["initialization_schedule_id"],
                "specialist_composition_id": payload["specialist_composition_id"],
            }
        )[:24]
        output.append(payload)
    return output


def _trace_scalar_and_canonical(raw_value: Any) -> tuple[float, str]:
    text = "" if raw_value is None else str(raw_value)
    if not text or text == "nan":
        return 0.0, ""
    try:
        parsed = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        parsed = text
    canonical = json.dumps(parsed, sort_keys=True, ensure_ascii=True)
    if isinstance(parsed, dict):
        numbers = [
            float(value)
            for value in parsed.values()
            if isinstance(value, (bool, int, float))
        ]
        return (float(np.mean(numbers)) if numbers else 0.0), canonical
    if isinstance(parsed, bool):
        return (1.0 if parsed else 0.0), canonical
    try:
        return float(parsed), canonical
    except (TypeError, ValueError):
        if text.lower() == "true":
            return 1.0, canonical
        if text.lower() == "false":
            return 0.0, canonical
        return 0.0, canonical


def _exact_repeat_pairs(values: list[str]) -> int:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return sum(comb(count, 2) for count in counts.values() if count >= 2)
