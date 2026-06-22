from __future__ import annotations

import csv
import json
from pathlib import Path

from mavs_ch10c.execution.corpus_writer import run_repetition_corpus


def test_locked_and_audit_all_runs_recorded() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    locked_manifest = run_repetition_corpus(
        repo_root,
        repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml",
        "manifest",
        ["pytest", "test_locked_and_audit_all_runs_recorded", "locked"],
    )
    audit_manifest = run_repetition_corpus(
        repo_root,
        repo_root / "configs" / "experiments" / "audit_repetition_corpus.yaml",
        "manifest",
        ["pytest", "test_locked_and_audit_all_runs_recorded", "audit"],
    )

    assert locked_manifest["row_count"] == 36000
    assert audit_manifest["row_count"] == 14400
    assert locked_manifest["prediction_row_count"] == 324000
    assert audit_manifest["prediction_row_count"] == 129600
    assert audit_manifest["model_fit_count"] == 2160
    _assert_file_row_count(repo_root / "results" / "execution_corpus" / "locked", 36000, 324000)
    _assert_file_row_count(repo_root / "results" / "execution_corpus" / "audit", 14400, 129600)


def _assert_file_row_count(output_dir: Path, expected_rows: int, expected_prediction_rows: int) -> None:
    with (output_dir / "corpus_manifest.json").open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    assert manifest["row_count"] == expected_rows
    assert len(manifest["corpus_manifest_hash"]) == 64

    with (output_dir / "corpus_index.csv").open("r", encoding="utf-8", newline="") as handle:
        corpus_rows = list(csv.DictReader(handle))
    assert len(corpus_rows) == expected_rows
    with (output_dir / "predictions_index.csv").open("r", encoding="utf-8", newline="") as handle:
        prediction_rows = list(csv.DictReader(handle))
    assert len(prediction_rows) == expected_prediction_rows

    with (output_dir / "run_manifests.jsonl").open("r", encoding="utf-8") as handle:
        run_manifest_rows = [json.loads(line) for line in handle if line.strip()]
    assert len(run_manifest_rows) == expected_rows
    assert all(row["pre_execution_manifest_hash"] for row in run_manifest_rows[:50])

    with (output_dir / "frozen_run_manifests.jsonl").open("r", encoding="utf-8") as handle:
        frozen_manifest_rows = [json.loads(line) for line in handle if line.strip()]
    assert len(frozen_manifest_rows) == expected_rows
    assert all(
        row["manifest_type"] == "pre_execution_frozen_run_manifest"
        for row in frozen_manifest_rows[:50]
    )
    assert {
        row["pre_execution_manifest_hash"] for row in frozen_manifest_rows[:50]
    } == {
        row["pre_execution_manifest_hash"] for row in run_manifest_rows[:50]
    }

    for row in corpus_rows[:50]:
        same_unit_rows = [
            candidate
            for candidate in corpus_rows
            if candidate["dataset_id"] == row["dataset_id"]
            and candidate["run_mode"] == row["run_mode"]
            and candidate["execution_seed"] == row["execution_seed"]
            and candidate["split_schedule_id"] == row["split_schedule_id"]
            and candidate["initialization_schedule_id"] == row["initialization_schedule_id"]
            and candidate["specialist_composition_id"] == row["specialist_composition_id"]
        ]
        hashes = {candidate["specialist_output_hash"] for candidate in same_unit_rows}
        assert len(hashes) == 1
