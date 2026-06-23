from __future__ import annotations

from mavs_ch10c.corruption import CORRUPTION_FAMILIES, CORRUPTION_LEVELS
from mavs_ch10c.corruption.ch10b_suite import load_corruption_suite

from phase6_helpers import phase6_config, repo_root


def test_corruption_suite_import_contract() -> None:
    config = phase6_config()
    suite = load_corruption_suite(repo_root(), config)

    assert set(suite["families"]) == set(CORRUPTION_FAMILIES)
    assert [float(level) for level in suite["levels"]] == CORRUPTION_LEVELS
    assert suite["ch10b_grid_manifest_payload_hash"] == (
        "2e18454a30dc9c83b9c74af3bf432b93ea6434a88205b107238447f2677f0523"
    )
    assert suite["ch10b_manifest_definition_count"] == 2880
    assert set(suite["family_config_hashes"]) == set(CORRUPTION_FAMILIES)

