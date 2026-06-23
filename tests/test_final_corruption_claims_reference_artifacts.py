from __future__ import annotations

from pathlib import Path

import pandas as pd


def test_final_corruption_claims_reference_artifacts() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ledger = pd.read_csv(
        repo_root / "results" / "reports" / "corruption_claim_support_ledger.csv",
        dtype=str,
    )

    assert len(ledger) == 10
    assert set(ledger["claim_id"].astype(int)) == set(range(1, 11))
    for row in ledger.to_dict("records"):
        paths = [row["primary_artifact"]] + [
            path.strip() for path in str(row["supporting_artifacts"]).split(";") if path.strip()
        ]
        for path in paths:
            assert (repo_root / path).exists()

