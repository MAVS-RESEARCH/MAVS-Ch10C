"""Phase 1 orchestration controller."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_artifacts import validate_ch10a_foundation
from mavs_ch10c.adapters.ch10a_source import resolve_source
from mavs_ch10c.adapters.ch10b_verification import validate_ch10b_verification
from mavs_ch10c.execution.environment import capture_environment
from mavs_ch10c.execution.run_manifest import write_run_manifest
from mavs_ch10c.repeatability.repetition_grid import (
    build_repetition_grid,
    repetition_grid_manifest,
    write_repetition_grid,
)
from mavs_ch10c.verification.hash_utils import write_json


def import_foundation(repo_root: Path, command_line: list[str]) -> dict[str, Any]:
    """Locate and validate Chapter 10A and 10B foundations."""

    # console.log: phase1 foundation import begins.
    console.log("phase1.foundation.import.start")
    ch10a_config = repo_root / "configs" / "ch10a_import" / "source.yaml"
    ch10b_config = repo_root / "configs" / "ch10b_import" / "source.yaml"
    ch10a_source = resolve_source(repo_root, ch10a_config)
    ch10b_source = resolve_source(repo_root, ch10b_config)
    ch10a_manifest = validate_ch10a_foundation(repo_root, ch10a_source, ch10a_config)
    ch10b_manifest = validate_ch10b_verification(repo_root, ch10b_source, ch10b_config)
    environment = capture_environment(repo_root, command_line)

    output_dir = repo_root / "results" / "foundation_import"
    ch10a_hash = write_json(output_dir / "ch10a_import_manifest.json", ch10a_manifest)
    ch10b_hash = write_json(output_dir / "ch10b_import_manifest.json", ch10b_manifest)
    foundation_manifest = {
        "status": "pass",
        "phase": "phase1_foundation_import",
        "ch10a_import_manifest_hash": ch10a_hash,
        "ch10b_import_manifest_hash": ch10b_hash,
        "ch10a": ch10a_manifest,
        "ch10b": ch10b_manifest,
        "environment": environment,
    }
    foundation_hash = write_run_manifest(
        output_dir / "foundation_import_manifest.json", foundation_manifest
    )
    foundation_manifest["foundation_import_manifest_hash"] = foundation_hash
    write_json(output_dir / "foundation_import_manifest.json", foundation_manifest)
    # console.log: phase1 foundation import completed.
    console.log(f"phase1.foundation.import.complete hash={foundation_hash}")
    return foundation_manifest


def build_and_write_repetition_grid(
    repo_root: Path, run_mode: str, command_line: list[str]
) -> dict[str, Any]:
    """Build, write, and manifest the Phase 1 repetition grid."""

    # console.log: phase1 repetition grid controller begins.
    console.log(f"phase1.repetition_grid.controller.start run_mode={run_mode}")
    units = build_repetition_grid(repo_root, run_mode=run_mode)
    output_dir = repo_root / "results" / "run_manifests"
    csv_path = output_dir / "repetition_grid.csv"
    row_count = write_repetition_grid(csv_path, units)
    manifest = repetition_grid_manifest(repo_root, units)
    manifest.update(
        {
            "phase": "phase1_repetition_grid",
            "run_mode": run_mode,
            "csv_path": str(csv_path),
            "row_count": row_count,
            "environment": capture_environment(repo_root, command_line),
        }
    )
    manifest_hash = write_run_manifest(
        output_dir / "repetition_grid_manifest.json", manifest
    )
    manifest["manifest_hash"] = manifest_hash
    write_json(output_dir / "repetition_grid_manifest.json", manifest)
    # console.log: phase1 repetition grid controller completed.
    console.log(f"phase1.repetition_grid.controller.complete hash={manifest_hash}")
    return manifest
