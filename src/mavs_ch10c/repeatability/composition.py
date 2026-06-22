"""Specialist composition loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_systems import REQUIRED_SPECIALISTS
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_json


def load_specialist_compositions(path: Path) -> list[dict[str, Any]]:
    # console.log: phase1 specialist composition load begins.
    console.log(f"phase1.compositions.load path={path}")
    payload = load_json_config(path)
    compositions = list(payload.get("specialist_compositions", []))
    validate_specialist_compositions(compositions)
    return compositions


def validate_specialist_compositions(compositions: list[dict[str, Any]]) -> None:
    # console.log: phase1 specialist composition validation begins.
    console.log("phase1.compositions.validate.start")
    if not compositions:
        raise ValueError("No specialist compositions configured")
    ids = [composition["id"] for composition in compositions]
    if len(ids) != len(set(ids)):
        raise ValueError("Specialist composition ids must be unique")
    required = set(REQUIRED_SPECIALISTS)
    for composition in compositions:
        specialists = set(composition.get("specialists", []))
        if not specialists:
            raise ValueError(f"Composition has no specialists: {composition}")
        unknown = specialists - required
        if unknown:
            raise ValueError(f"Composition references unknown specialists: {unknown}")
    # console.log: phase1 specialist composition validation completed.
    console.log(f"phase1.compositions.validate.complete count={len(compositions)}")


def specialist_compositions_hash(compositions: list[dict[str, Any]]) -> str:
    return sha256_json(compositions)
