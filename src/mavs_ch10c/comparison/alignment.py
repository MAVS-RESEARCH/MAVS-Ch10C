"""Alignment checks for Phase 3 variance benchmark construction."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.adapters.ch10a_systems import REQUIRED_DATASETS, REQUIRED_SYSTEMS
from mavs_ch10c.comparison import ALIGNMENT_FIELDS
from mavs_ch10c.verification.hash_utils import sha256_json


def load_corpus_index(path: Path) -> list[dict[str, Any]]:
    """Load a Phase 2 row-level prediction index."""

    # console.log: phase3 corpus index load begins.
    console.log(f"phase3.alignment.load_corpus.start path={path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError(f"Corpus index is empty: {path}")
    # console.log: phase3 corpus index load completed.
    console.log(f"phase3.alignment.load_corpus.complete rows={len(rows)}")
    return rows


def alignment_key(row: dict[str, Any]) -> tuple[str, ...]:
    """Build the row-level alignment key for one prediction row."""

    return tuple(str(row[field]) for field in ALIGNMENT_FIELDS)


def alignment_key_hash(row: dict[str, Any]) -> str:
    return sha256_json({field: row[field] for field in ALIGNMENT_FIELDS})


def group_aligned_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, ...], list[dict[str, Any]]]:
    """Group rows by identical schedule, row id, and benchmark label provenance."""

    # console.log: phase3 alignment grouping begins.
    console.log(f"phase3.alignment.group.start rows={len(rows)}")
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(alignment_key(row), []).append(row)
    # console.log: phase3 alignment grouping completed.
    console.log(f"phase3.alignment.group.complete groups={len(groups)}")
    return groups


def validate_aligned_groups(groups: dict[tuple[str, ...], list[dict[str, Any]]]) -> None:
    """Fail on missing systems or mismatched input evidence within an aligned group."""

    # console.log: phase3 alignment validation begins.
    console.log(f"phase3.alignment.validate.start groups={len(groups)}")
    required_systems = set(REQUIRED_SYSTEMS)
    for key, group in groups.items():
        systems = {row["system_id"] for row in group}
        if systems != required_systems:
            missing = sorted(required_systems - systems)
            unexpected = sorted(systems - required_systems)
            raise ValueError(
                f"Aligned group system mismatch key={key} missing={missing} unexpected={unexpected}"
            )
        _require_single_value(group, "specialist_output_hash", key)
        _require_single_value(group, "probability_matrix_hash", key)
        _require_single_value(group, "label_hash", key)
        _require_single_value(group, "row_hash", key)
        _require_single_value(group, "label", key)
    # console.log: phase3 alignment validation completed.
    console.log("phase3.alignment.validate.complete")


def coverage_summary(groups: dict[tuple[str, ...], list[dict[str, Any]]]) -> dict[str, Any]:
    """Summarize schedule coverage for a validated alignment map."""

    # console.log: phase3 coverage summary begins.
    console.log(f"phase3.alignment.coverage.start groups={len(groups)}")
    rows = [row for group in groups.values() for row in group]
    summary = {
        "dataset_count": len({row["dataset_id"] for row in rows}),
        "system_count": len({row["system_id"] for row in rows}),
        "execution_seed_count": len({row["execution_seed"] for row in rows}),
        "split_schedule_count": len({row["split_schedule_id"] for row in rows}),
        "initialization_schedule_count": len(
            {row["initialization_schedule_id"] for row in rows}
        ),
        "specialist_composition_count": len(
            {row["specialist_composition_id"] for row in rows}
        ),
        "aligned_group_count": len(groups),
        "row_count": len(rows),
        "prediction_row_count": len(rows),
        "datasets": sorted({row["dataset_id"] for row in rows}),
        "systems": sorted({row["system_id"] for row in rows}),
    }
    if set(summary["datasets"]) != set(REQUIRED_DATASETS):
        raise ValueError(f"Dataset coverage mismatch: {summary['datasets']}")
    if set(summary["systems"]) != set(REQUIRED_SYSTEMS):
        raise ValueError(f"System coverage mismatch: {summary['systems']}")
    # console.log: phase3 coverage summary completed.
    console.log(
        "phase3.alignment.coverage.complete "
        f"groups={summary['aligned_group_count']} rows={summary['row_count']}"
    )
    return summary


def _require_single_value(
    group: list[dict[str, Any]], field: str, key: tuple[str, ...]
) -> None:
    values = {row[field] for row in group}
    if len(values) != 1:
        raise ValueError(f"Aligned group field mismatch key={key} field={field}")
