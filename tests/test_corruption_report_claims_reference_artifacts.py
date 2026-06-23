from __future__ import annotations

import pandas as pd

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_report_claims_reference_artifacts() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    ledger = pd.read_csv(root / config["output_paths"]["claim_support_ledger"], dtype=str)
    report_text = (root / config["output_paths"]["report"]).read_text(encoding="utf-8")

    assert len(ledger) == 10
    assert set(ledger["claim_id"].astype(int)) == set(range(1, 11))
    assert ledger["primary_artifact"].str.len().gt(0).all()
    assert ledger["supporting_artifacts"].str.len().gt(0).all()
    for artifact in ledger["primary_artifact"]:
        assert (root / artifact).exists()
    for claim_id in range(1, 11):
        assert f"RQ{claim_id}." in report_text

