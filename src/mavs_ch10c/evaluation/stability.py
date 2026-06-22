"""Prediction, decision, and consensus stability definitions for Phase 4."""

from __future__ import annotations

from collections import defaultdict
from math import comb
from typing import Any

import numpy as np
import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.evaluation import GOVERNANCE_SYSTEMS
from mavs_ch10c.evaluation.variance import (
    DETAILED_GROUP_COLUMNS,
    SUMMARY_GROUP_COLUMNS,
    _base_group_payload,
)
from mavs_ch10c.verification.hash_utils import sha256_json

ROW_ALIGNMENT_COLUMNS = ["row_id", "label_hash"]


def build_prediction_stability_rows(
    rows: pd.DataFrame, source_input_hash: str
) -> list[dict[str, Any]]:
    """Compute row-aligned predicted-label and probability stability."""

    # console.log: phase4 prediction stability build begins.
    console.log("phase4.stability.prediction.start")
    result = _binary_probability_stability(
        rows,
        metric_family="prediction_stability",
        metric_name="prediction_stability",
        binary_column="binary_decision",
        probability_column="probability_score",
        binary_output_field="binary_pairwise_agreement",
        source_input_hash=source_input_hash,
    )
    # console.log: phase4 prediction stability build completed.
    console.log(f"phase4.stability.prediction.complete rows={len(result)}")
    return result


def build_decision_stability_rows(
    rows: pd.DataFrame, source_input_hash: str
) -> list[dict[str, Any]]:
    """Compute row-aligned final accept/reject decision stability."""

    # console.log: phase4 decision stability build begins.
    console.log("phase4.stability.decision.start")
    result = _binary_probability_stability(
        rows,
        metric_family="decision_stability",
        metric_name="decision_stability",
        binary_column="binary_decision",
        probability_column="probability_score",
        binary_output_field="decision_pairwise_agreement",
        source_input_hash=source_input_hash,
    )
    # console.log: phase4 decision stability build completed.
    console.log(f"phase4.stability.decision.complete rows={len(result)}")
    return result


def build_consensus_stability_rows(
    rows: pd.DataFrame, source_input_hash: str
) -> list[dict[str, Any]]:
    """Compute MAVS consensus stability and baseline score stability."""

    # console.log: phase4 consensus stability build begins.
    console.log("phase4.stability.consensus.start")
    working = rows.copy()
    working["probability_score"] = pd.to_numeric(working["probability_score"])
    if "trace_R" not in working:
        working["trace_R"] = ""
    working["trace_R_numeric"] = pd.to_numeric(working["trace_R"], errors="coerce")
    output: list[dict[str, Any]] = []
    for group_columns, grain in [
        (DETAILED_GROUP_COLUMNS, "dataset_system_split_init_composition"),
        (SUMMARY_GROUP_COLUMNS, "dataset_system_composition"),
    ]:
        output.extend(_consensus_for_group(working, group_columns, grain, source_input_hash))
    # console.log: phase4 consensus stability build completed.
    console.log(f"phase4.stability.consensus.complete rows={len(output)}")
    return output


def pairwise_binary_agreement(values: list[int]) -> tuple[int, int, float]:
    """Return agree-pairs, total-pairs, and agreement for binary values."""

    count = len(values)
    if count < 2:
        return 0, 0, 0.0
    ones = int(sum(values))
    zeros = count - ones
    agree_pairs = comb(ones, 2) + comb(zeros, 2)
    pair_count = comb(count, 2)
    return agree_pairs, pair_count, agree_pairs / pair_count


def mean_pairwise_abs_difference(values: list[float]) -> tuple[float, int]:
    """Return mean absolute pairwise difference and pair count."""

    if len(values) < 2:
        return 0.0, 0
    ordered = np.sort(np.asarray(values, dtype=np.float64))
    count = len(ordered)
    coefficients = (2 * np.arange(count)) - count + 1
    total_abs = float(np.sum(coefficients * ordered))
    pair_count = comb(count, 2)
    return total_abs / pair_count, pair_count


def _binary_probability_stability(
    rows: pd.DataFrame,
    *,
    metric_family: str,
    metric_name: str,
    binary_column: str,
    probability_column: str,
    binary_output_field: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    working = rows.copy()
    working[binary_column] = pd.to_numeric(working[binary_column]).astype(int)
    working[probability_column] = pd.to_numeric(working[probability_column])
    output: list[dict[str, Any]] = []
    for group_columns, grain in [
        (DETAILED_GROUP_COLUMNS, "dataset_system_split_init_composition"),
        (SUMMARY_GROUP_COLUMNS, "dataset_system_composition"),
    ]:
        accumulators: dict[tuple[Any, ...], dict[str, float]] = defaultdict(
            lambda: {
                "row_alignment_group_count": 0.0,
                "observation_count": 0.0,
                "pair_count": 0.0,
                "agree_pairs": 0.0,
                "probability_abs_diff_sum": 0.0,
            }
        )
        grouped = working.groupby(group_columns + ROW_ALIGNMENT_COLUMNS, dropna=False)
        for key, group in grouped:
            group_key = tuple(key[: len(group_columns)])
            values = group[binary_column].astype(int).tolist()
            probabilities = group[probability_column].astype(float).tolist()
            agree_pairs, pair_count, _ = pairwise_binary_agreement(values)
            mean_abs_diff, probability_pair_count = mean_pairwise_abs_difference(probabilities)
            if pair_count == 0:
                continue
            acc = accumulators[group_key]
            acc["row_alignment_group_count"] += 1
            acc["observation_count"] += len(values)
            acc["pair_count"] += pair_count
            acc["agree_pairs"] += agree_pairs
            acc["probability_abs_diff_sum"] += mean_abs_diff * probability_pair_count
        for key, acc in accumulators.items():
            pair_count = acc["pair_count"]
            mean_abs_probability_difference = (
                acc["probability_abs_diff_sum"] / pair_count if pair_count else 0.0
            )
            payload = _base_group_payload(group_columns, key)
            payload.update(
                {
                    "metric_family": metric_family,
                    "metric_name": metric_name,
                    "aggregation_grain": grain,
                    "row_alignment_group_count": int(acc["row_alignment_group_count"]),
                    "observation_count": int(acc["observation_count"]),
                    "pair_count": int(pair_count),
                    binary_output_field: acc["agree_pairs"] / pair_count if pair_count else 0.0,
                    "binary_pairwise_agreement": acc["agree_pairs"] / pair_count if pair_count else 0.0,
                    "mean_abs_probability_difference": mean_abs_probability_difference,
                    "probability_pairwise_stability": 1.0 - mean_abs_probability_difference,
                    "source_input_hash": source_input_hash,
                    "source_backend": "empirical_sklearn_repeated_training",
                }
            )
            payload["metric_row_id"] = _stability_metric_id(payload)
            output.append(payload)
    return output


def _consensus_for_group(
    rows: pd.DataFrame,
    group_columns: list[str],
    aggregation_grain: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for key, group in rows.groupby(group_columns, dropna=False):
        system_id = str(group["system_id"].iloc[0])
        if system_id in GOVERNANCE_SYSTEMS:
            value_column = "trace_R_numeric"
            value_rows = group[group[value_column].notna()]
            applicability = "governance_consensus_R"
            consensus_field = "R"
        else:
            value_column = "probability_score"
            value_rows = group
            applicability = "not_applicable_baseline_probability_score"
            consensus_field = "probability_score"
        pair_count = 0
        abs_diff_sum = 0.0
        variance_values: list[float] = []
        row_group_count = 0
        for _, row_group in value_rows.groupby(ROW_ALIGNMENT_COLUMNS, dropna=False):
            values = row_group[value_column].astype(float).tolist()
            if len(values) < 2:
                continue
            row_group_count += 1
            mean_abs_diff, current_pairs = mean_pairwise_abs_difference(values)
            pair_count += current_pairs
            abs_diff_sum += mean_abs_diff * current_pairs
            variance_values.append(float(np.var(values, ddof=1)))
        mean_abs_diff = abs_diff_sum / pair_count if pair_count else 0.0
        payload = _base_group_payload(group_columns, key)
        payload.update(
            {
                "metric_family": "consensus_stability",
                "metric_name": "consensus_stability",
                "aggregation_grain": aggregation_grain,
                "consensus_applicability": applicability,
                "consensus_field": consensus_field,
                "row_alignment_group_count": row_group_count,
                "observation_count": int(len(value_rows)),
                "pair_count": int(pair_count),
                "mean_row_level_variance": float(np.mean(variance_values)) if variance_values else 0.0,
                "consensus_pairwise_stability": "" if system_id not in GOVERNANCE_SYSTEMS else 1.0 - mean_abs_diff,
                "score_probability_pairwise_stability": "" if system_id in GOVERNANCE_SYSTEMS else 1.0 - mean_abs_diff,
                "mean_abs_probability_difference": mean_abs_diff,
                "source_input_hash": source_input_hash,
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
        payload["metric_row_id"] = _stability_metric_id(payload)
        output.append(payload)
    return output


def _stability_metric_id(payload: dict[str, Any]) -> str:
    return sha256_json(
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
