"""Pure MAVS-GC empirical baseline-delta rows for Phase 3."""

from __future__ import annotations

from typing import Any

from mavs_ch10c import console
from mavs_ch10c.comparison import BASELINE_SYSTEMS, PURE_MAVS_SYSTEM
from mavs_ch10c.verification.hash_utils import sha256_json


def build_delta_rows(
    groups: dict[tuple[str, ...], list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    """Build row-level Pure MAVS-GC comparison rows against all baselines."""

    # console.log: phase3 empirical baseline delta build begins.
    console.log(f"phase3.baseline_deltas.build.start groups={len(groups)}")
    rows: list[dict[str, Any]] = []
    for group in groups.values():
        by_system = {row["system_id"]: row for row in group}
        pure = by_system[PURE_MAVS_SYSTEM]
        for baseline_system in BASELINE_SYSTEMS:
            baseline = by_system[baseline_system]
            delta_payload = {
                "pure_run_id": pure["run_id"],
                "baseline_run_id": baseline["run_id"],
                "baseline_system_id": baseline_system,
                "row_hash": pure["row_hash"],
                "alignment_group_hash": sha256_json(
                    {
                        "dataset_id": pure["dataset_id"],
                        "run_mode": pure["run_mode"],
                        "execution_seed": pure["execution_seed"],
                        "split_schedule_id": pure["split_schedule_id"],
                        "initialization_schedule_id": pure["initialization_schedule_id"],
                        "specialist_composition_id": pure["specialist_composition_id"],
                        "row_id": pure["row_id"],
                        "label_hash": pure["label_hash"],
                    }
                ),
            }
            rows.append(
                {
                    "delta_row_id": sha256_json(delta_payload)[:24],
                    "dataset_id": pure["dataset_id"],
                    "run_mode": pure["run_mode"],
                    "execution_seed": pure["execution_seed"],
                    "split_schedule_id": pure["split_schedule_id"],
                    "initialization_schedule_id": pure["initialization_schedule_id"],
                    "specialist_composition_id": pure["specialist_composition_id"],
                    "row_id": pure["row_id"],
                    "row_hash": pure["row_hash"],
                    "label": pure["label"],
                    "label_hash": pure["label_hash"],
                    "pure_system_id": PURE_MAVS_SYSTEM,
                    "baseline_system_id": baseline_system,
                    "pure_run_id": pure["run_id"],
                    "baseline_run_id": baseline["run_id"],
                    "same_specialist_output_hash": str(
                        pure["specialist_output_hash"]
                        == baseline["specialist_output_hash"]
                    ),
                    "same_probability_matrix_hash": str(
                        pure["probability_matrix_hash"]
                        == baseline["probability_matrix_hash"]
                    ),
                    "same_label_hash": str(pure["label_hash"] == baseline["label_hash"]),
                    "probability_delta": _float(pure["probability_score"]) - _float(baseline["probability_score"]),
                    "decision_delta": _int(pure["binary_decision"]) - _int(baseline["binary_decision"]),
                    "confidence_delta": _float(pure["confidence"]) - _float(baseline["confidence"]),
                    "correctness_delta": _int(pure["correctness"]) - _int(baseline["correctness"]),
                    "f1_tp_delta": _int(pure["f1_tp"]) - _int(baseline["f1_tp"]),
                    "f1_fp_delta": _int(pure["f1_fp"]) - _int(baseline["f1_fp"]),
                    "f1_fn_delta": _int(pure["f1_fn"]) - _int(baseline["f1_fn"]),
                    "f1_tn_delta": _int(pure["f1_tn"]) - _int(baseline["f1_tn"]),
                    "pure_rejection_acceptance": pure["rejection_acceptance"],
                    "baseline_rejection_acceptance": baseline["rejection_acceptance"],
                    "metric_delta_status": "computed_empirical_row_delta",
                }
            )
    # console.log: phase3 empirical baseline delta build completed.
    console.log(f"phase3.baseline_deltas.build.complete rows={len(rows)}")
    return rows


def _float(value: Any) -> float:
    return float(value)


def _int(value: Any) -> int:
    return int(value)
