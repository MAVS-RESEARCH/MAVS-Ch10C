from __future__ import annotations

import pandas as pd

from mavs_ch10c.verification.hash_utils import load_json_config

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_matrix_complete() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    execution_manifest = load_json_config(root / config["output_paths"]["execution_manifest"])
    matrix = execution_manifest["matrix_manifest"]

    assert matrix["source_run_rows"] == 50400
    assert matrix["expected_expanded_run_rows"] == 3628800
    assert set(matrix["corruption_families"]) == set(config["families"])
    assert [float(level) for level in matrix["corruption_levels"]] == config["levels"]
    assert matrix["locked_audit_separation_preserved"] is True

    summary = pd.read_csv(root / config["output_paths"]["reproducibility_tables"])
    expected_rows = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
    )
    assert len(summary) == expected_rows
    assert set(summary["run_mode"]) == set(config["run_modes"])

