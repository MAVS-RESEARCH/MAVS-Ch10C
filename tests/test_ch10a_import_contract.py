from __future__ import annotations

from pathlib import Path

from mavs_ch10c.execution.controller import import_foundation


def test_ch10a_import_contract() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = import_foundation(repo_root, ["pytest", "test_ch10a_import_contract"])
    ch10a = manifest["ch10a"]

    assert ch10a["status"] == "pass"
    assert set(ch10a["datasets"]) == {
        "breast_cancer_wisconsin",
        "adult_income",
        "credit_card_fraud",
        "bank_marketing",
    }
    assert set(ch10a["specialists"]) == {
        "random_forest",
        "gradient_boosted_trees",
        "mlp",
    }
    assert set(ch10a["systems"]) == {
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
        "pure_mavs_gc",
    }
    assert len(ch10a["governance_hashes"]) == 6
    assert all(len(value) == 64 for value in ch10a["governance_hashes"].values())
