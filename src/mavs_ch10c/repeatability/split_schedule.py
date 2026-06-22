"""Split schedule loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_json


def load_split_schedules(path: Path, split_seeds: set[int]) -> list[dict[str, Any]]:
    # console.log: phase1 split schedule load begins.
    console.log(f"phase1.split_schedules.load path={path}")
    payload = load_json_config(path)
    schedules = list(payload.get("split_schedules", []))
    validate_split_schedules(schedules, split_seeds)
    return schedules


def validate_split_schedules(
    schedules: list[dict[str, Any]], split_seeds: set[int]
) -> None:
    # console.log: phase1 split schedule validation begins.
    console.log("phase1.split_schedules.validate.start")
    if not schedules:
        raise ValueError("No split schedules configured")
    ids = [schedule["id"] for schedule in schedules]
    if len(ids) != len(set(ids)):
        raise ValueError("Split schedule ids must be unique")
    for schedule in schedules:
        seed = schedule.get("seed")
        if seed not in split_seeds:
            raise ValueError(f"Split schedule seed is not registered: {schedule}")
        total = (
            schedule["train_fraction"]
            + schedule["validation_fraction"]
            + schedule["calibration_fraction"]
            + schedule["benchmark_fraction"]
        )
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Split fractions must sum to 1.0: {schedule}")
        if schedule["run_mode"] not in {"locked", "audit"}:
            raise ValueError(f"Invalid split run mode: {schedule}")
    # console.log: phase1 split schedule validation completed.
    console.log(f"phase1.split_schedules.validate.complete count={len(schedules)}")


def split_schedules_hash(schedules: list[dict[str, Any]]) -> str:
    return sha256_json(schedules)
