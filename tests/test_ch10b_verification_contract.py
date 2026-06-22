from __future__ import annotations

from pathlib import Path

from mavs_ch10c.execution.controller import import_foundation


def test_ch10b_verification_contract() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = import_foundation(repo_root, ["pytest", "test_ch10b_verification_contract"])
    ch10b = manifest["ch10b"]

    assert ch10b["status"] == "pass"
    assert len(ch10b["verification_utility_hashes"]) >= 8
    expected_suffixes = {
        "verification/hash_utils.py",
        "verification/artifact_inventory.py",
        "verification/release_gate.py",
        "verification/import_audit.py",
        "stress/run_manifest.py",
        "scripts/hash_artifacts.py",
        "scripts/verify_artifacts.py",
        "scripts/reproduce_all.py",
    }
    observed = set(ch10b["verification_utility_hashes"])
    for suffix in expected_suffixes:
        assert any(path.endswith(suffix) for path in observed)
    assert all(len(value) == 64 for value in ch10b["verification_utility_hashes"].values())
