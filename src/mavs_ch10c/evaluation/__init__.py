"""Phase 4 reproducibility metric utilities for MAVS Chapter 10C."""

from __future__ import annotations

REQUIRED_METRIC_FAMILIES = [
    "accuracy_variance",
    "f1_variance",
    "prediction_stability",
    "decision_stability",
    "consensus_stability",
    "trace_stability",
    "run_to_run_agreement",
    "confidence_interval_width",
]

GOVERNANCE_SYSTEMS = ["pure_mavs_gc", "veto_mavs"]

BASELINE_SYSTEMS = [
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
]

PURE_MAVS_SYSTEM = "pure_mavs_gc"
