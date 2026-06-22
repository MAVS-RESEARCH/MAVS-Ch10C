from __future__ import annotations

from pathlib import Path

from mavs_ch10c.repeatability.seed_registry import load_seed_registry


def test_seed_registry_complete_and_disjoint() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    registry = load_seed_registry(
        repo_root / "configs" / "reproducibility" / "seed_registry.yaml"
    )

    assert len(registry["locked_execution_seeds"]) == 30
    assert len(registry["audit_execution_seeds"]) == 20
    assert len(registry["shadow_verification_seeds"]) >= 2
    assert len(registry["split_seeds"]) == 8
    assert len(registry["initialization_seeds"]) == 3

    namespaces = [
        registry["locked_execution_seeds"],
        registry["audit_execution_seeds"],
        registry["shadow_verification_seeds"],
        registry["split_seeds"],
        registry["initialization_seeds"],
    ]
    all_seeds = [seed for namespace in namespaces for seed in namespace]
    assert len(all_seeds) == len(set(all_seeds))
