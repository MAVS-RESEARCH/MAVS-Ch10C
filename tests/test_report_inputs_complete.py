from __future__ import annotations

from pathlib import Path

from mavs_ch10c.reporting.reproducibility_report import load_report_config


def test_report_inputs_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_report_config(repo_root)

    for path in config["input_paths"].values():
        assert (repo_root / path).exists(), path
    assert config["analysis_rules"]["require_artifact_reference_for_every_claim"] is True
    assert config["analysis_rules"]["fail_if_expected_rows_or_figures_missing"] is True
    assert config["expected"]["baselines"] == [
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
    ]
    assert config["expected"]["governance_systems"] == ["pure_mavs_gc", "veto_mavs"]
