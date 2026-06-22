"""Initialization schedule loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_json


def load_initialization_schedules(
    path: Path, initialization_seeds: set[int]
) -> list[dict[str, Any]]:
    # console.log: phase1 initialization schedule load begins.
    console.log(f"phase1.init_schedules.load path={path}")
    payload = load_json_config(path)
    schedules = list(payload.get("initialization_schedules", []))
    validate_initialization_schedules(schedules, initialization_seeds)
    return schedules


def validate_initialization_schedules(
    schedules: list[dict[str, Any]], initialization_seeds: set[int]
) -> None:
    # console.log: phase1 initialization schedule validation begins.
    console.log("phase1.init_schedules.validate.start")
    if not schedules:
        raise ValueError("No initialization schedules configured")
    ids = [schedule["id"] for schedule in schedules]
    if len(ids) != len(set(ids)):
        raise ValueError("Initialization schedule ids must be unique")
    for schedule in schedules:
        if schedule.get("seed") not in initialization_seeds:
            raise ValueError(
                f"Initialization schedule seed is not registered: {schedule}"
            )
    # console.log: phase1 initialization schedule validation completed.
    console.log(f"phase1.init_schedules.validate.complete count={len(schedules)}")


def initialization_schedules_hash(schedules: list[dict[str, Any]]) -> str:
    return sha256_json(schedules)
