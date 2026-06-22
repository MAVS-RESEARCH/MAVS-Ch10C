from __future__ import annotations

from pathlib import Path

import pytest

from mavs_ch10c.execution.corpus_writer import (
    ensure_audit_freeze_gate,
    ensure_final_hash_contracts,
    ensure_locked_freeze_manifest,
    ensure_no_tuning,
)
from mavs_ch10c.verification.hash_utils import load_json_config


def test_no_tuning_guard_accepts_phase2_configs() -> None:
    ensure_no_tuning(
        {
            "allow_hyperparameter_search": False,
            "allow_governance_tuning": False,
            "allow_model_family_changes": False,
            "allow_phase2_final_claims_from_training_diagnostics": False,
        }
    )


def test_no_tuning_guard_rejects_hyperparameter_search() -> None:
    with pytest.raises(ValueError):
        ensure_no_tuning(
            {
                "allow_hyperparameter_search": True,
                "allow_governance_tuning": False,
                "allow_model_family_changes": False,
                "allow_phase2_final_claims_from_training_diagnostics": False,
            }
        )


def test_final_hash_contracts_accept_frozen_inputs() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config = load_json_config(
        repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml"
    )
    ensure_final_hash_contracts(repo_root, config)


def test_audit_freeze_gate_accepts_locked_freeze_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    locked_manifest = load_json_config(
        repo_root / "results" / "execution_corpus" / "locked" / "corpus_manifest.json"
    )
    ensure_locked_freeze_manifest(repo_root, locked_manifest)
    freeze_manifest = ensure_audit_freeze_gate(repo_root)
    assert freeze_manifest["locked_pipeline_frozen"] is True
    assert freeze_manifest["metric_code_frozen"] is True
    assert freeze_manifest["report_templates_frozen"] is True
