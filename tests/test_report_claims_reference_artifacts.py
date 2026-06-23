from __future__ import annotations

import re
from pathlib import Path

from mavs_ch10c.reporting.reproducibility_report import build_reproducibility_report


def test_report_claims_reference_artifacts() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_reproducibility_report(repo_root)
    report = (repo_root / "results" / "reports" / "reproducibility_report.md").read_text(
        encoding="utf-8"
    )

    assert "## Claim Register" in report
    assert "## Final Answer to Chapter 10C" in report
    claim_lines = [line for line in report.splitlines() if re.match(r"^\| C\d+ \|", line)]
    assert len(claim_lines) >= 7
    for line in claim_lines:
        artifact_paths = re.findall(r"`(results/[^`]+)`", line)
        assert artifact_paths, line
        for artifact_path in artifact_paths:
            assert (repo_root / artifact_path).exists(), artifact_path
    forbidden_claims = [
        "proves robustness under corruption",
        "universal superiority",
        "cross-domain validity",
        "governance learning",
    ]
    lowered = report.lower()
    for phrase in forbidden_claims:
        assert phrase not in lowered
