from __future__ import annotations

import pandas as pd

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_metrics_complete() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    variance = pd.read_csv(root / config["output_paths"]["variance_tables"], dtype=str)
    stability = pd.read_csv(root / config["output_paths"]["stability_tables"], dtype=str)

    assert set(variance["metric_name"]) == set(config["variance_metrics"])
    assert set(config["stability_metrics"]).issubset(set(stability["metric_name"]))
    assert set(config["confidence_metrics"]).issubset(set(stability["metric_name"]))
    assert set(variance["corruption_family"]) == set(config["families"])
    assert set(float(level) for level in variance["corruption_level"].unique()) == set(config["levels"])
    assert set(float(level) for level in stability["corruption_level"].unique()) == set(config["levels"])
