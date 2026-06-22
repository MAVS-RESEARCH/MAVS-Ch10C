from __future__ import annotations

from pathlib import Path

from mavs_ch10c.execution.controller import build_and_write_repetition_grid
from mavs_ch10c.repeatability.repetition_grid import build_repetition_grid


def test_repetition_grid_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    units = build_repetition_grid(repo_root, run_mode="all")

    assert len(units) == 50400
    assert sum(1 for unit in units if unit.run_mode == "locked") == 36000
    assert sum(1 for unit in units if unit.run_mode == "audit") == 14400
    assert len({unit.repetition_id for unit in units}) == len(units)
    assert {unit.dataset_id for unit in units} == {
        "breast_cancer_wisconsin",
        "adult_income",
        "credit_card_fraud",
        "bank_marketing",
    }
    assert {unit.system_id for unit in units} == {
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
        "pure_mavs_gc",
    }


def test_repetition_grid_manifest_written() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = build_and_write_repetition_grid(
        repo_root, "all", ["pytest", "test_repetition_grid_manifest_written"]
    )

    assert manifest["status"] == "pass"
    assert manifest["row_count"] == 50400
    assert manifest["locked_row_count"] == 36000
    assert manifest["audit_row_count"] == 14400
    assert len(manifest["grid_hash"]) == 64
