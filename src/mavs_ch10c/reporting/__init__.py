"""Phase 5 reporting utilities for MAVS Chapter 10C."""

from __future__ import annotations

PURE_MAVS_SYSTEM = "pure_mavs_gc"

BASELINE_SYSTEMS = [
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
]

GOVERNANCE_SYSTEMS = [
    "pure_mavs_gc",
    "veto_mavs",
]

REQUIRED_REPORT_TABLES = [
    "variance_tables",
    "stability_tables",
    "reproducibility_system_deltas",
]

REQUIRED_FIGURES = [
    "accuracy_variance_by_system",
    "f1_variance_by_system",
    "prediction_stability_by_system",
    "decision_stability_by_system",
    "consensus_stability_by_system",
    "trace_stability_by_system",
    "confidence_interval_widths",
]
