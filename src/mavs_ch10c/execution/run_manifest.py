"""Run manifest writer for Phase 1 commands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import write_json


def write_run_manifest(path: Path, manifest: dict[str, Any]) -> str:
    """Write a deterministic run manifest and return its SHA-256 hash."""

    # console.log: phase1 run manifest write begins.
    console.log(f"phase1.run_manifest.write.start path={path}")
    manifest_hash = write_json(path, manifest)
    # console.log: phase1 run manifest write completed.
    console.log(f"phase1.run_manifest.write.complete hash={manifest_hash}")
    return manifest_hash
