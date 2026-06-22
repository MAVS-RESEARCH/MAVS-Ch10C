"""Run-to-run agreement definitions for Phase 4."""

from __future__ import annotations

from collections import defaultdict
from math import comb
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.evaluation.stability import ROW_ALIGNMENT_COLUMNS, pairwise_binary_agreement
from mavs_ch10c.evaluation.variance import (
    DETAILED_GROUP_COLUMNS,
    SUMMARY_GROUP_COLUMNS,
    _base_group_payload,
)
from mavs_ch10c.verification.hash_utils import sha256_json


def build_run_to_run_agreement_rows(
    rows: pd.DataFrame, source_input_hash: str
) -> list[dict[str, Any]]:
    """Compute pairwise and kappa-style agreement for decisions and correctness."""

    # console.log: phase4 run-to-run agreement build begins.
    console.log("phase4.agreement.run_to_run.start")
    output: list[dict[str, Any]] = []
    working = rows.copy()
    for column in ["binary_decision", "correctness"]:
        working[column] = pd.to_numeric(working[column]).astype(int)
    for target, column in [
        ("decision", "binary_decision"),
        ("correctness", "correctness"),
    ]:
        for group_columns, grain in [
            (DETAILED_GROUP_COLUMNS, "dataset_system_split_init_composition"),
            (SUMMARY_GROUP_COLUMNS, "dataset_system_composition"),
        ]:
            output.extend(
                _agreement_for_group(
                    working,
                    group_columns,
                    grain,
                    target,
                    column,
                    source_input_hash,
                )
            )
    # console.log: phase4 run-to-run agreement build completed.
    console.log(f"phase4.agreement.run_to_run.complete rows={len(output)}")
    return output


def _agreement_for_group(
    rows: pd.DataFrame,
    group_columns: list[str],
    aggregation_grain: str,
    agreement_target: str,
    value_column: str,
    source_input_hash: str,
) -> list[dict[str, Any]]:
    accumulators: dict[tuple[Any, ...], dict[str, float]] = defaultdict(
        lambda: {
            "row_alignment_group_count": 0.0,
            "observation_count": 0.0,
            "pair_count": 0.0,
            "agree_pairs": 0.0,
            "ones": 0.0,
        }
    )
    grouped = rows.groupby(group_columns + ROW_ALIGNMENT_COLUMNS, dropna=False)
    for key, group in grouped:
        values = group[value_column].astype(int).tolist()
        if len(values) < 2:
            continue
        group_key = tuple(key[: len(group_columns)])
        agree_pairs, pair_count, _ = pairwise_binary_agreement(values)
        acc = accumulators[group_key]
        acc["row_alignment_group_count"] += 1
        acc["observation_count"] += len(values)
        acc["pair_count"] += pair_count
        acc["agree_pairs"] += agree_pairs
        acc["ones"] += sum(values)
    output: list[dict[str, Any]] = []
    for key, acc in accumulators.items():
        pair_count = acc["pair_count"]
        observed = acc["agree_pairs"] / pair_count if pair_count else 0.0
        p_one = acc["ones"] / acc["observation_count"] if acc["observation_count"] else 0.0
        expected = (p_one * p_one) + ((1.0 - p_one) * (1.0 - p_one))
        if 1.0 - expected <= 1e-12:
            kappa: float | str = ""
            status = "undefined_single_class_distribution"
        else:
            kappa = (observed - expected) / (1.0 - expected)
            status = "computed"
        payload = _base_group_payload(group_columns, key)
        payload.update(
            {
                "metric_family": "run_to_run_agreement",
                "metric_name": "run_to_run_agreement",
                "aggregation_grain": aggregation_grain,
                "agreement_target": agreement_target,
                "row_alignment_group_count": int(acc["row_alignment_group_count"]),
                "observation_count": int(acc["observation_count"]),
                "pair_count": int(pair_count),
                "binary_pairwise_agreement": observed,
                "kappa_agreement": kappa,
                "expected_agreement": expected,
                "zero_division_policy": status,
                "source_input_hash": source_input_hash,
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
        payload["metric_row_id"] = sha256_json(
            {
                "metric_family": payload["metric_family"],
                "agreement_target": payload["agreement_target"],
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
