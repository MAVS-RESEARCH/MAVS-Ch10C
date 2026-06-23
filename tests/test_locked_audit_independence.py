from __future__ import annotations

from pathlib import Path

import pandas as pd

from mavs_ch10c.repeatability.seed_registry import load_seed_registry


def test_locked_audit_independence() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    registry = load_seed_registry(repo_root / "configs" / "reproducibility" / "seed_registry.yaml")
    locked = pd.read_csv(
        repo_root / "results" / "execution_corpus" / "locked" / "corpus_index.csv",
        dtype=str,
        usecols=["run_mode", "execution_seed", "split_schedule_id"],
    )
    audit = pd.read_csv(
        repo_root / "results" / "execution_corpus" / "audit" / "corpus_index.csv",
        dtype=str,
        usecols=["run_mode", "execution_seed", "split_schedule_id"],
    )

    assert set(registry["locked_execution_seeds"]).isdisjoint(registry["audit_execution_seeds"])
    assert set(locked["run_mode"]) == {"locked"}
    assert set(audit["run_mode"]) == {"audit"}
    assert set(locked["execution_seed"]).isdisjoint(set(audit["execution_seed"]))
    assert set(locked["split_schedule_id"]).isdisjoint(set(audit["split_schedule_id"]))

