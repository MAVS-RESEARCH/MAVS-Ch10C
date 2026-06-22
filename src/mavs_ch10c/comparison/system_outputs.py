"""Normalize Phase 2 empirical system outputs into Phase 3 variance rows."""

from __future__ import annotations

from typing import Any

from mavs_ch10c import console
from mavs_ch10c.comparison.alignment import alignment_key_hash
from mavs_ch10c.execution.system_runner import GOVERNANCE_SYSTEMS
from mavs_ch10c.verification.hash_utils import sha256_json

TRACE_FIELD_COLUMNS = [
    "trace_s",
    "trace_r",
    "trace_z",
    "trace_a",
    "trace_w",
    "trace_m",
    "trace_theta",
    "trace_R",
    "trace_hard_veto",
    "trace_decision",
]


def normalize_system_output(row: dict[str, Any]) -> dict[str, Any]:
    """Map a row-level prediction to common empirical comparison fields."""

    # console.log: phase3 empirical system output normalization begins.
    console.log(
        "phase3.system_outputs.normalize.start "
        f"system={row['system_id']} repetition={row['repetition_id']} row={row['row_id']}"
    )
    normalized = {
        "variance_row_id": sha256_json(
            {
                "run_id": row["run_id"],
                "system_id": row["system_id"],
                "row_hash": row["row_hash"],
            }
        )[:24],
        "alignment_group_hash": alignment_key_hash(row),
        "row_id": row["row_id"],
        "row_hash": row["row_hash"],
        "dataset_id": row["dataset_id"],
        "run_mode": row["run_mode"],
        "execution_seed": row["execution_seed"],
        "split_schedule_id": row["split_schedule_id"],
        "initialization_schedule_id": row["initialization_schedule_id"],
        "specialist_composition_id": row["specialist_composition_id"],
        "system_id": row["system_id"],
        "specialist_ids": row["specialist_ids"],
        "label": row["label"],
        "label_hash": row["label_hash"],
        "probability_score": row["probability_score"],
        "binary_decision": row["binary_decision"],
        "confidence": row["confidence"],
        "correctness": row["correctness"],
        "f1_tp": row["f1_tp"],
        "f1_fp": row["f1_fp"],
        "f1_fn": row["f1_fn"],
        "f1_tn": row["f1_tn"],
        "rejection_acceptance": row["rejection_acceptance"],
        "trace_hash": row["trace_hash"],
        "trace_schema_hash": row["trace_schema_hash"],
        "trace_s": row.get("trace_s", ""),
        "trace_r": row.get("trace_r", ""),
        "trace_z": row.get("trace_z", ""),
        "trace_a": row.get("trace_a", ""),
        "trace_w": row.get("trace_w", ""),
        "trace_m": row.get("trace_m", ""),
        "trace_theta": row.get("trace_theta", ""),
        "trace_R": row.get("trace_R", ""),
        "trace_hard_veto": row.get("trace_hard_veto", ""),
        "trace_decision": row.get("trace_decision", ""),
        "governance_trace_complete": str(row["system_id"] in GOVERNANCE_SYSTEMS),
        "run_id": row["run_id"],
        "repetition_id": row["repetition_id"],
        "system_config_hash": row["system_config_hash"],
        "specialist_output_hash": row["specialist_output_hash"],
        "probability_matrix_hash": row["probability_matrix_hash"],
        "empirical_prediction_available": "true",
        "source_backend": "empirical_sklearn_repeated_training",
    }
    if row["system_id"] in GOVERNANCE_SYSTEMS and not row["trace_hash"]:
        raise ValueError(f"Governance trace hash missing for row: {row['prediction_row_id']}")
    # console.log: phase3 empirical system output normalization completed.
    console.log(f"phase3.system_outputs.normalize.complete row={normalized['variance_row_id']}")
    return normalized
