from __future__ import annotations

import pandas as pd

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_clean_anchor_matches_phase5() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    corruption = pd.read_csv(root / config["output_paths"]["variance_tables"], dtype=str)
    phase5 = pd.read_csv(
        root / config["source_manifests"]["phase5_clean_variance_table"],
        dtype=str,
    )
    corruption = corruption[
        (corruption["corruption_level"].astype(float) == 0.0)
        & (corruption["metric_name"].isin(["accuracy_variance", "f1_variance"]))
    ]

    phase5_map = {
        (
            row["run_mode"],
            row["dataset_id"],
            row["system_id"],
            row["specialist_composition_id"],
            row["metric_name"],
        ): row
        for row in phase5.to_dict("records")
    }
    assert not corruption.empty
    for row in corruption.to_dict("records"):
        key = (
            row["run_mode"],
            row["dataset_id"],
            row["system_id"],
            row["specialist_composition_id"],
            row["metric_name"],
        )
        clean = phase5_map[key]
        assert abs(float(row["sample_variance"]) - float(clean["sample_variance"])) <= config[
            "clean_anchor_tolerance"
        ]
        assert abs(float(row["mean_metric_value"]) - float(clean["mean_metric_value"])) <= config[
            "clean_anchor_tolerance"
        ]
        assert row["clean_anchor_source"] == config["source_manifests"][
            "phase5_clean_variance_table"
        ]

