from __future__ import annotations

from pathlib import Path

from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file


def test_no_governance_source_drift() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    foundation = load_json_config(repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json")
    ch10a_root = Path(foundation["source_path"])

    for relative_path, expected_hash in foundation["governance_hashes"].items():
        assert sha256_file(ch10a_root / relative_path) == expected_hash

