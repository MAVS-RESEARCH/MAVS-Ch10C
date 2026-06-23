"""Phase 6 corruption-aware reproducibility support."""

from __future__ import annotations

CORRUPTION_FAMILIES = [
    "adversarial_confidence_inflation",
    "confidence_distortion",
    "distribution_shift",
    "feature_noise",
    "label_noise",
    "missing_features",
    "random_feature_deletion",
    "specialist_failure",
    "synthetic_sensor_failure",
]

CORRUPTION_LEVELS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]

GOVERNANCE_SYSTEMS = ["veto_mavs", "pure_mavs_gc"]

