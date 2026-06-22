from __future__ import annotations

from pathlib import Path

from mavs_ch10c.repeatability.seed_registry import load_seed_registry


def test_audit_execution_seeds_independent_from_locked_execution_seeds() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    registry = load_seed_registry(
        repo_root / "configs" / "reproducibility" / "seed_registry.yaml"
    )

    assert set(registry["locked_execution_seeds"]).isdisjoint(
        registry["audit_execution_seeds"]
    )
