"""Chapter 10B corruption-suite adapter for Phase 6."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from mavs_ch10c import console
from mavs_ch10c.corruption import CORRUPTION_FAMILIES, CORRUPTION_LEVELS
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file, sha256_json


def load_corruption_suite(repo_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    """Load and verify the complete Chapter 10B corruption family suite."""

    # console.log: phase6 Ch10B corruption suite import begins.
    console.log("phase6.corruption_suite.load.start")
    suite_config = load_json_config(repo_root / config["suite_config_path"])
    source_root = Path(suite_config["source_root"])
    if not source_root.exists():
        raise FileNotFoundError(f"Chapter 10B source root not found: {source_root}")

    grid_config_path = source_root / suite_config["source_grid_config"]
    grid_manifest_path = source_root / suite_config["source_grid_manifest"]
    family_dir = source_root / suite_config["source_family_config_dir"]
    if not grid_config_path.exists():
        raise FileNotFoundError(grid_config_path)
    if not grid_manifest_path.exists():
        raise FileNotFoundError(grid_manifest_path)
    if not family_dir.exists():
        raise FileNotFoundError(family_dir)

    grid_config = _load_yaml(grid_config_path)
    grid_manifest = load_json_config(grid_manifest_path)
    _validate_grid_contract(suite_config, grid_config, grid_manifest)
    family_payloads = _load_family_payloads(family_dir, suite_config["families"])
    family_hashes = {
        family: sha256_file(family_dir / f"{family}.yaml") for family in suite_config["families"]
    }
    suite_payload = {
        "suite_id": suite_config["suite_id"],
        "schema_version": suite_config["schema_version"],
        "source_root": str(source_root),
        "source_grid_config": str(grid_config_path),
        "source_grid_manifest": str(grid_manifest_path),
        "families": suite_config["families"],
        "levels": suite_config["levels"],
        "grid_config_hash": sha256_file(grid_config_path),
        "grid_manifest_hash": sha256_file(grid_manifest_path),
        "ch10b_grid_manifest_payload_hash": grid_manifest["manifest_payload_sha256"],
        "ch10b_manifest_definition_count": grid_manifest["definition_count"],
        "family_config_hashes": family_hashes,
        "family_payloads": family_payloads,
    }
    suite_payload["suite_hash"] = sha256_json(
        {
            "suite_id": suite_payload["suite_id"],
            "families": suite_payload["families"],
            "levels": suite_payload["levels"],
            "grid_config_hash": suite_payload["grid_config_hash"],
            "grid_manifest_hash": suite_payload["grid_manifest_hash"],
            "family_config_hashes": family_hashes,
        }
    )
    # console.log: phase6 Ch10B corruption suite import completed.
    console.log(
        "phase6.corruption_suite.load.complete "
        f"families={len(suite_payload['families'])} levels={len(suite_payload['levels'])} "
        f"suite_hash={suite_payload['suite_hash']}"
    )
    return suite_payload


def _load_family_payloads(family_dir: Path, families: list[str]) -> dict[str, Any]:
    # console.log: phase6 Ch10B family config import begins.
    console.log("phase6.corruption_suite.family_configs.start")
    payloads: dict[str, Any] = {}
    for family in families:
        family_path = family_dir / f"{family}.yaml"
        if not family_path.exists():
            raise FileNotFoundError(family_path)
        payloads[family] = _load_yaml(family_path)
    # console.log: phase6 Ch10B family config import completed.
    console.log(f"phase6.corruption_suite.family_configs.complete families={len(payloads)}")
    return payloads


def _validate_grid_contract(
    suite_config: dict[str, Any],
    grid_config: dict[str, Any],
    grid_manifest: dict[str, Any],
) -> None:
    # console.log: phase6 Ch10B corruption suite validation begins.
    console.log("phase6.corruption_suite.validate.start")
    expected_families = set(CORRUPTION_FAMILIES)
    expected_levels = {float(level) for level in CORRUPTION_LEVELS}
    configured_families = set(suite_config["families"])
    configured_levels = {float(level) for level in suite_config["levels"]}
    grid_families = set(grid_config.get("corruption_families", []))
    grid_levels = {float(level) for level in grid_config.get("levels", [])}
    manifest_families = set(grid_manifest.get("corruption_families", []))
    manifest_levels = {float(level) for level in grid_manifest.get("levels", [])}

    if configured_families != expected_families:
        raise RuntimeError(f"Phase 6 configured families mismatch: {configured_families}")
    if configured_levels != expected_levels:
        raise RuntimeError(f"Phase 6 configured levels mismatch: {configured_levels}")
    if grid_families != expected_families:
        raise RuntimeError(f"Chapter 10B grid families mismatch: {grid_families}")
    if grid_levels != expected_levels:
        raise RuntimeError(f"Chapter 10B grid levels mismatch: {grid_levels}")
    if manifest_families != expected_families:
        raise RuntimeError(f"Chapter 10B manifest families mismatch: {manifest_families}")
    if manifest_levels != expected_levels:
        raise RuntimeError(f"Chapter 10B manifest levels mismatch: {manifest_levels}")
    if grid_manifest.get("grid_config_hash") != suite_config["expected_grid_config_hash"]:
        raise RuntimeError("Chapter 10B grid config hash drifted")
    if (
        grid_manifest.get("manifest_payload_sha256")
        != suite_config["expected_manifest_payload_sha256"]
    ):
        raise RuntimeError("Chapter 10B corruption manifest payload hash drifted")
    if grid_manifest.get("index_csv_sha256") != suite_config["expected_index_csv_sha256"]:
        raise RuntimeError("Chapter 10B corruption manifest CSV index hash drifted")
    if grid_manifest.get("index_json_sha256") != suite_config["expected_index_json_sha256"]:
        raise RuntimeError("Chapter 10B corruption manifest JSON index hash drifted")
    # console.log: phase6 Ch10B corruption suite validation completed.
    console.log(
        "phase6.corruption_suite.validate.complete "
        f"definition_count={grid_manifest.get('definition_count')}"
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected YAML mapping in {path}")
    return payload

