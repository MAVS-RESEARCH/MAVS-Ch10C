"""Validation of Chapter 10B verification patterns required by Chapter 10C."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_source import SourceResolution
from mavs_ch10c.verification.hash_utils import hash_relative_files, load_json_config


def _require_files(source_root: Path, relative_paths: list[str]) -> None:
    missing = [path for path in relative_paths if not (source_root / path).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required Chapter 10B files: {missing}")


def validate_ch10b_verification(
    repo_root: Path, source: SourceResolution, config_path: Path
) -> dict[str, Any]:
    """Validate Chapter 10B hashing, inventory, and release-gate utilities."""

    # console.log: phase1 Chapter 10B verification validation begins.
    console.log(f"phase1.ch10b.validate.start path={source.path}")
    config = load_json_config(config_path)
    required_paths = config["verification_files"] + config["report_files"]
    _require_files(source.path, required_paths)

    utility_hashes = hash_relative_files(source.path, config["verification_files"])
    report_hashes = hash_relative_files(source.path, config["report_files"])
    manifest = {
        "source_id": source.source_id,
        "source_path": str(source.path),
        "source_origin": source.origin,
        "repo_url": source.repo_url,
        "commit": source.commit,
        "verification_utility_hashes": utility_hashes,
        "report_hashes": report_hashes,
        "status": "pass",
    }
    # console.log: phase1 Chapter 10B verification validation completed.
    console.log(
        "phase1.ch10b.validate.complete "
        f"verification_files={len(config['verification_files'])}"
    )
    return manifest
