from __future__ import annotations

from pathlib import Path

from mavs_ch10c.verification.hash_utils import load_json_config


def test_final_run_guards() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    clean = load_json_config(repo_root / "results" / "reports" / "reproducibility_artifact_manifest.json")
    corruption = load_json_config(
        repo_root / "results" / "corruption_reproducibility" / "corruption_metric_manifest.json"
    )
    verification_text = (repo_root / "results" / "reports" / "verification_report.md").read_text(
        encoding="utf-8"
    )

    assert clean["final_run_classification"]["exploratory_results_used"] is False
    assert clean["final_run_classification"]["training_diagnostics_used_as_final_evidence"] is False
    assert corruption["training_performed"] is False
    assert corruption["hyperparameter_search_performed"] is False
    assert corruption["threshold_tuning_after_corruption_performed"] is False
    assert corruption["governance_policy_modified"] is False
    assert "Overall status: `pass`." in verification_text

