from __future__ import annotations

import pandas as pd

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_trace_stability_complete() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    trace = pd.read_csv(root / config["output_paths"]["trace_stability_tables"])

    expected_rows = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["governance_systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["trace_fields"])
    )
    assert len(trace) == expected_rows
    assert set(trace["system_id"]) == set(config["governance_systems"])
    assert set(trace["trace_field"]) == set(config["trace_fields"])
    assert trace["trace_stability"].between(0.0, 1.0).all()

