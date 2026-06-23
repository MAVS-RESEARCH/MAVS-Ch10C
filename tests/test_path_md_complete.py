from __future__ import annotations

from pathlib import Path


def test_path_md_complete_for_phase7() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    text = (repo_root / "Path.md").read_text(encoding="utf-8")

    for required in [
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Phase 5",
        "Phase 6",
        "Phase 7",
        "artifact_inventory",
        "verification_report",
        "WorkPlan Compliance Check",
    ]:
        assert required in text

