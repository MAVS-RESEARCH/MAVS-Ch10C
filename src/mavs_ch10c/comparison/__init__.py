"""Phase 3 comparison utilities for MAVS Chapter 10C."""

from __future__ import annotations

BASELINE_SYSTEMS = [
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
]

PURE_MAVS_SYSTEM = "pure_mavs_gc"

ALIGNMENT_FIELDS = [
    "dataset_id",
    "run_mode",
    "execution_seed",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
    "row_id",
    "label_hash",
]
