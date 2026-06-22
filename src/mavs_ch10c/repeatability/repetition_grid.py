"""Repetition-grid expansion for Chapter 10C."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_systems import REQUIRED_DATASETS, REQUIRED_SYSTEMS
from mavs_ch10c.repeatability.composition import load_specialist_compositions
from mavs_ch10c.repeatability.init_schedule import load_initialization_schedules
from mavs_ch10c.repeatability.seed_registry import load_seed_registry, seed_registry_hash
from mavs_ch10c.repeatability.split_schedule import load_split_schedules
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_json


@dataclass(frozen=True)
class RepetitionUnit:
    repetition_id: str
    run_mode: str
    dataset_id: str
    system_id: str
    execution_seed: int
    split_schedule_id: str
    split_seed: int
    initialization_schedule_id: str
    initialization_seed: int
    specialist_composition_id: str
    specialist_ids: str


def _unit_id(fields: dict[str, Any]) -> str:
    return sha256_json(fields)[:24]


def build_repetition_grid(repo_root: Path, run_mode: str = "all") -> list[RepetitionUnit]:
    """Build system-level repetition units from frozen Phase 1 configs."""

    # console.log: phase1 repetition grid build begins.
    console.log(f"phase1.repetition_grid.build.start run_mode={run_mode}")
    config_dir = repo_root / "configs" / "reproducibility"
    seed_registry = load_seed_registry(config_dir / "seed_registry.yaml")
    split_schedules = load_split_schedules(
        config_dir / "split_schedules.yaml", set(seed_registry["split_seeds"])
    )
    init_schedules = load_initialization_schedules(
        config_dir / "init_schedules.yaml",
        set(seed_registry["initialization_seeds"]),
    )
    compositions = load_specialist_compositions(
        config_dir / "specialist_compositions.yaml"
    )
    grid_config = load_json_config(config_dir / "repetition_grid.yaml")

    requested_modes = ["locked", "audit"] if run_mode == "all" else [run_mode]
    units: list[RepetitionUnit] = []
    for mode in requested_modes:
        if mode not in grid_config["run_modes"]:
            raise ValueError(f"Unknown run mode for repetition grid: {mode}")
        mode_config = grid_config["run_modes"][mode]
        execution_seeds = seed_registry[mode_config["execution_seed_namespace"]]
        mode_splits = [
            schedule
            for schedule in split_schedules
            if schedule["run_mode"] == mode_config["split_run_mode"]
        ]
        _assert_expected_counts(mode, mode_config, execution_seeds, mode_splits, init_schedules, compositions)
        for dataset_id in REQUIRED_DATASETS:
            for system_id in REQUIRED_SYSTEMS:
                for execution_seed in execution_seeds:
                    for split_schedule in mode_splits:
                        for init_schedule in init_schedules:
                            for composition in compositions:
                                base_fields = {
                                    "run_mode": mode,
                                    "dataset_id": dataset_id,
                                    "system_id": system_id,
                                    "execution_seed": execution_seed,
                                    "split_schedule_id": split_schedule["id"],
                                    "initialization_schedule_id": init_schedule["id"],
                                    "specialist_composition_id": composition["id"],
                                }
                                units.append(
                                    RepetitionUnit(
                                        repetition_id=_unit_id(base_fields),
                                        run_mode=mode,
                                        dataset_id=dataset_id,
                                        system_id=system_id,
                                        execution_seed=execution_seed,
                                        split_schedule_id=split_schedule["id"],
                                        split_seed=split_schedule["seed"],
                                        initialization_schedule_id=init_schedule["id"],
                                        initialization_seed=init_schedule["seed"],
                                        specialist_composition_id=composition["id"],
                                        specialist_ids=",".join(composition["specialists"]),
                                    )
                                )
    # console.log: phase1 repetition grid build completed.
    console.log(f"phase1.repetition_grid.build.complete units={len(units)}")
    return units


def _assert_expected_counts(
    mode: str,
    mode_config: dict[str, Any],
    execution_seeds: list[int],
    split_schedules: list[dict[str, Any]],
    init_schedules: list[dict[str, Any]],
    compositions: list[dict[str, Any]],
) -> None:
    expectations = {
        "execution_seed": (len(execution_seeds), mode_config["expected_execution_seed_count"]),
        "split_schedule": (len(split_schedules), mode_config["expected_split_schedule_count"]),
        "initialization_schedule": (
            len(init_schedules),
            mode_config["expected_initialization_schedule_count"],
        ),
        "specialist_composition": (
            len(compositions),
            mode_config["expected_specialist_composition_count"],
        ),
    }
    for label, (actual, expected) in expectations.items():
        if actual != expected:
            raise ValueError(
                f"{mode} {label} count mismatch: actual={actual}, expected={expected}"
            )


def write_repetition_grid(path: Path, units: Iterable[RepetitionUnit]) -> int:
    """Write repetition units as CSV and return the row count."""

    rows = [asdict(unit) for unit in units]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("Cannot write an empty repetition grid")
    # console.log: phase1 repetition grid CSV write begins.
    console.log(f"phase1.repetition_grid.write.start path={path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    # console.log: phase1 repetition grid CSV write completed.
    console.log(f"phase1.repetition_grid.write.complete rows={len(rows)}")
    return len(rows)


def repetition_grid_manifest(repo_root: Path, units: list[RepetitionUnit]) -> dict[str, Any]:
    """Build a deterministic manifest for a generated repetition grid."""

    config_dir = repo_root / "configs" / "reproducibility"
    seed_registry = load_seed_registry(config_dir / "seed_registry.yaml")
    unit_rows = [asdict(unit) for unit in units]
    return {
        "status": "pass",
        "row_count": len(unit_rows),
        "locked_row_count": sum(1 for unit in units if unit.run_mode == "locked"),
        "audit_row_count": sum(1 for unit in units if unit.run_mode == "audit"),
        "dataset_count": len(REQUIRED_DATASETS),
        "system_count": len(REQUIRED_SYSTEMS),
        "seed_registry_hash": seed_registry_hash(seed_registry),
        "grid_hash": sha256_json(unit_rows),
    }
