from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10c.execution.controller import import_foundation


def test_no_local_governance_algorithm_package_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    assert not (repo_root / "src" / "mavs_ch10c" / "governance").exists()


def test_import_manifest_freezes_upstream_governance_files() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    import_foundation(repo_root, ["pytest", "test_no_algorithmic_governance_modification"])
    manifest_path = repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    expected_files = {
        "src/mavs_ch10a/governance/diagnostics.py",
        "src/mavs_ch10a/governance/severity.py",
        "src/mavs_ch10a/governance/rebalancer.py",
        "src/mavs_ch10a/governance/organs.py",
        "src/mavs_ch10a/governance/policy.py",
        "src/mavs_ch10a/governance/trace.py",
    }
    assert set(manifest["governance_hashes"]) == expected_files
