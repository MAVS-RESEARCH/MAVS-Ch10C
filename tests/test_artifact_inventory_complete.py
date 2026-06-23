from __future__ import annotations

from pathlib import Path

from mavs_ch10c.verification.final_verification import REQUIRED_INVENTORY_CATEGORIES
from mavs_ch10c.verification.hash_utils import load_json_config


def test_artifact_inventory_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    inventory = load_json_config(repo_root / "results" / "reports" / "artifact_inventory.json")

    assert inventory["status"] == "pass"
    assert inventory["entry_count"] > 0
    assert inventory["missing_required_artifacts"] == []
    assert inventory["missing_required_categories"] == []
    for category in REQUIRED_INVENTORY_CATEGORIES:
        assert inventory["category_counts"][category] > 0

