"""Seed registry loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_json

SEED_NAMESPACES = [
    "locked_execution_seeds",
    "audit_execution_seeds",
    "shadow_verification_seeds",
    "split_seeds",
    "initialization_seeds",
]


def load_seed_registry(path: Path) -> dict[str, Any]:
    # console.log: phase1 seed registry load begins.
    console.log(f"phase1.seeds.load path={path}")
    registry = load_json_config(path)
    validate_seed_registry(registry)
    return registry


def validate_seed_registry(registry: dict[str, Any]) -> None:
    # console.log: phase1 seed registry validation begins.
    console.log("phase1.seeds.validate.start")
    all_seen: dict[int, str] = {}
    for namespace in SEED_NAMESPACES:
        seeds = registry.get(namespace)
        if not isinstance(seeds, list) or not seeds:
            raise ValueError(f"Seed namespace is missing or empty: {namespace}")
        if len(seeds) != len(set(seeds)):
            raise ValueError(f"Duplicate seeds inside namespace: {namespace}")
        for seed in seeds:
            if not isinstance(seed, int):
                raise TypeError(f"Seed must be an integer: {namespace}={seed}")
            previous = all_seen.get(seed)
            if previous is not None:
                raise ValueError(
                    f"Seed collision across namespaces: seed={seed} {previous} {namespace}"
                )
            all_seen[seed] = namespace
    if set(registry["locked_execution_seeds"]) & set(registry["audit_execution_seeds"]):
        raise ValueError("Locked and audit execution seeds must be disjoint")
    # console.log: phase1 seed registry validation completed.
    console.log(f"phase1.seeds.validate.complete total_seeds={len(all_seen)}")


def seed_registry_hash(registry: dict[str, Any]) -> str:
    return sha256_json(registry)
