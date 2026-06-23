"""Phase 6 corruption-aware metric table builders."""

from __future__ import annotations

VARIANCE_METRIC_TO_SOURCE = {
    "accuracy_variance": "accuracy",
    "f1_variance": "f1",
    "rejection_variance": "rejection",
    "threshold_variance": "threshold",
    "severity_variance": "severity",
    "weight_variance": "weight",
}

STABILITY_METRICS = [
    "prediction_stability",
    "decision_stability",
    "consensus_stability",
    "trace_stability",
    "run_to_run_agreement",
]

CONFIDENCE_METRICS = [
    "confidence_interval_width",
    "bootstrap_confidence_interval_width",
]

