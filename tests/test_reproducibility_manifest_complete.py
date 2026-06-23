from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10c.reporting.reproducibility_report import build_reproducibility_report
from mavs_ch10c.verification.hash_utils import sha256_file, sha256_json


def test_reproducibility_manifest_complete() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = build_reproducibility_report(repo_root)
    manifest_path = repo_root / "results" / "reports" / "reproducibility_artifact_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    required_keys = {
        "source_document_references",
        "import_source_commits",
        "dataset_hashes",
        "split_schedule_hashes",
        "seed_registry_hashes",
        "initialization_schedule_hashes",
        "composition_hashes",
        "model_config_hashes",
        "governance_source_hashes",
        "corpus_hashes",
        "variance_dataset_hashes",
        "metric_table_hashes",
        "report_table_hashes",
        "figure_hashes",
        "report_hash",
        "reproducibility_artifact_manifest_hash",
    }
    assert required_keys <= manifest.keys()
    manifest_without_hash = dict(manifest)
    manifest_hash = manifest_without_hash.pop("reproducibility_artifact_manifest_hash")
    assert sha256_json(manifest_without_hash) == manifest_hash
    assert manifest["report_hash"] == result["report_hash"]
    assert manifest["report_hash"] == sha256_file(
        repo_root / "results" / "reports" / "reproducibility_report.md"
    )
    assert len(manifest["figure_hashes"]) == 7
    assert manifest["report_claim_policy"]["every_claim_references_artifacts"] is True
