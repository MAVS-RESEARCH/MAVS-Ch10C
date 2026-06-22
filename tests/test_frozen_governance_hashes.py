from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10c.execution.controller import import_foundation
from mavs_ch10c.verification.hash_utils import sha256_file


def test_frozen_governance_hashes_match_import_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    import_foundation(repo_root, ["pytest", "test_frozen_governance_hashes"])
    manifest_path = repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = Path(manifest["source_path"])

    for relative_path, expected_hash in manifest["governance_hashes"].items():
        assert sha256_file(source_path / relative_path) == expected_hash
