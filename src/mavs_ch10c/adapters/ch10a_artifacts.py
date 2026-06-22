"""Validation of the completed Chapter 10A foundation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_source import SourceResolution
from mavs_ch10c.adapters.ch10a_systems import assert_contract_matches
from mavs_ch10c.verification.hash_utils import hash_relative_files, load_json_config


def _require_files(source_root: Path, relative_paths: list[str]) -> list[str]:
    missing = [path for path in relative_paths if not (source_root / path).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required Chapter 10A files: {missing}")
    return relative_paths


def validate_ch10a_foundation(
    repo_root: Path, source: SourceResolution, config_path: Path
) -> dict[str, Any]:
    """Validate Chapter 10A source contracts and immutable governance files."""

    # console.log: phase1 Chapter 10A validation begins.
    console.log(f"phase1.ch10a.validate.start path={source.path}")
    config = load_json_config(config_path)
    assert_contract_matches(config)

    dataset_config_paths = [
        f"configs/datasets/{dataset_id}.yaml"
        for dataset_id in config["required_datasets"]
    ]
    model_config_paths = [
        f"configs/models/{specialist_id}.yaml"
        for specialist_id in config["required_specialists"]
    ]
    system_config_paths = [
        f"configs/systems/{system_id}.yaml"
        for system_id in config["required_systems"]
    ]
    required_paths = (
        dataset_config_paths
        + model_config_paths
        + system_config_paths
        + config["governance_files"]
        + config["protocol_files"]
        + config["report_files"]
    )

    _require_files(source.path, required_paths)
    governance_hashes = hash_relative_files(source.path, config["governance_files"])
    system_config_hashes = hash_relative_files(source.path, system_config_paths)
    dataset_config_hashes = hash_relative_files(source.path, dataset_config_paths)
    specialist_config_hashes = hash_relative_files(source.path, model_config_paths)
    protocol_hashes = hash_relative_files(source.path, config["protocol_files"])
    report_hashes = hash_relative_files(source.path, config["report_files"])

    manifest = {
        "source_id": source.source_id,
        "source_path": str(source.path),
        "source_origin": source.origin,
        "repo_url": source.repo_url,
        "commit": source.commit,
        "datasets": config["required_datasets"],
        "specialists": config["required_specialists"],
        "systems": config["required_systems"],
        "dataset_config_hashes": dataset_config_hashes,
        "specialist_config_hashes": specialist_config_hashes,
        "system_config_hashes": system_config_hashes,
        "governance_hashes": governance_hashes,
        "protocol_hashes": protocol_hashes,
        "report_hashes": report_hashes,
        "status": "pass",
    }
    # console.log: phase1 Chapter 10A validation completed.
    console.log(
        "phase1.ch10a.validate.complete "
        f"datasets={len(config['required_datasets'])} systems={len(config['required_systems'])}"
    )
    return manifest
