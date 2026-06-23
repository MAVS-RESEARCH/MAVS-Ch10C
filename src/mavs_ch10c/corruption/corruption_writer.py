"""Phase 6 corruption-aware reproducibility artifact writer."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.corruption.cache import phase6_cache_hit
from mavs_ch10c.corruption.ch10b_suite import load_corruption_suite
from mavs_ch10c.corruption.corruption_matrix import build_corruption_matrix_manifest
from mavs_ch10c.corruption.corruption_runner import build_corruption_metric_corpus
from mavs_ch10c.corruption_metrics.confidence import build_corruption_confidence_rows
from mavs_ch10c.corruption_metrics.manifest import (
    write_corruption_execution_manifest,
    write_corruption_metric_manifest,
)
from mavs_ch10c.corruption_metrics.reporting import (
    CLAIM_FIELDS,
    build_claim_support_ledger,
    render_corruption_figures,
    render_corruption_report,
    render_verification_addendum,
)
from mavs_ch10c.corruption_metrics.stability import (
    STABILITY_FIELDS,
    build_corruption_stability_rows,
)
from mavs_ch10c.corruption_metrics.trace import TRACE_FIELDS, build_corruption_trace_rows
from mavs_ch10c.corruption_metrics.variance import (
    VARIANCE_FIELDS,
    build_corruption_variance_rows,
)
from mavs_ch10c.verification.hash_utils import load_json_config

SUMMARY_FIELDS = [
    "corruption_summary_hash",
    "run_mode",
    "dataset_id",
    "system_id",
    "specialist_composition_id",
    "corruption_family",
    "corruption_level",
    "clean_anchor",
    "source_run_count",
    "benchmark_row_count",
    "accuracy_mean",
    "accuracy_variance",
    "accuracy_standard_deviation",
    "f1_mean",
    "f1_variance",
    "f1_standard_deviation",
    "rejection_mean",
    "rejection_variance",
    "rejection_standard_deviation",
    "threshold_mean",
    "threshold_variance",
    "threshold_standard_deviation",
    "severity_mean",
    "severity_variance",
    "severity_standard_deviation",
    "weight_mean",
    "weight_variance",
    "weight_standard_deviation",
    "prediction_stability_mean",
    "prediction_stability_variance",
    "prediction_stability_standard_deviation",
    "decision_stability_mean",
    "decision_stability_variance",
    "decision_stability_standard_deviation",
    "consensus_stability_mean",
    "consensus_stability_variance",
    "consensus_stability_standard_deviation",
    "trace_stability_mean",
    "trace_stability_variance",
    "trace_stability_standard_deviation",
    "run_to_run_agreement_mean",
    "run_to_run_agreement_variance",
    "run_to_run_agreement_standard_deviation",
    "confidence_interval_width",
    "bootstrap_confidence_interval_width",
    "suite_hash",
    "corruption_config_hash",
    "corrupted_input_hash_protocol",
]


def build_corruption_reproducibility_outputs(
    repo_root: Path,
    config_path: Path | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Build all Phase 6 corruption-aware reproducibility outputs."""

    # console.log: phase6 corruption artifact build begins.
    console.log("phase6.writer.build.start")
    config_path = config_path or repo_root / "configs" / "experiments" / "corruption_reproducibility.yaml"
    config = load_json_config(config_path)
    if not force and phase6_cache_hit(repo_root, config):
        # console.log: phase6 corruption artifact build reused valid cache.
        console.log("phase6.writer.build.cache_hit")
        return load_json_config(repo_root / config["output_paths"]["metric_manifest"])

    suite = load_corruption_suite(repo_root, config)
    matrix_manifest = build_corruption_matrix_manifest(repo_root, config, suite)
    corpus_outputs = build_corruption_metric_corpus(repo_root, config, suite, matrix_manifest)
    execution_manifest = write_corruption_execution_manifest(
        repo_root,
        config,
        suite,
        matrix_manifest,
        corpus_outputs,
    )
    manifest_hash = execution_manifest["corruption_execution_manifest_hash"]
    variance_rows = build_corruption_variance_rows(
        repo_root,
        config,
        corpus_outputs["summary_rows"],
        manifest_hash,
    )
    stability_rows = build_corruption_stability_rows(
        repo_root,
        config,
        corpus_outputs["summary_rows"],
        manifest_hash,
    )
    confidence_rows = build_corruption_confidence_rows(
        config,
        corpus_outputs["summary_rows"],
        manifest_hash,
    )
    combined_stability_rows = stability_rows + confidence_rows
    trace_rows = build_corruption_trace_rows(
        repo_root,
        config,
        corpus_outputs["trace_rows"],
        manifest_hash,
    )
    _write_summary_outputs(repo_root, config, corpus_outputs["summary_rows"])
    _write_csv(
        repo_root / config["output_paths"]["reproducibility_tables"],
        corpus_outputs["summary_rows"],
        SUMMARY_FIELDS,
    )
    _write_csv(
        repo_root / config["output_paths"]["variance_tables"],
        variance_rows,
        VARIANCE_FIELDS,
    )
    _write_csv(
        repo_root / config["output_paths"]["stability_tables"],
        combined_stability_rows,
        STABILITY_FIELDS,
    )
    _write_csv(
        repo_root / config["output_paths"]["trace_stability_tables"],
        trace_rows,
        TRACE_FIELDS,
    )
    render_corruption_figures(
        repo_root,
        config,
        variance_rows,
        combined_stability_rows,
        trace_rows,
    )
    ledger_rows = build_claim_support_ledger(
        config,
        corpus_outputs["summary_rows"],
        variance_rows,
        combined_stability_rows,
        trace_rows,
    )
    _write_csv(
        repo_root / config["output_paths"]["claim_support_ledger"],
        ledger_rows,
        CLAIM_FIELDS,
    )
    render_corruption_report(repo_root, config, suite, execution_manifest, ledger_rows)
    render_verification_addendum(repo_root, config, suite, execution_manifest)
    metric_manifest = write_corruption_metric_manifest(repo_root, config, suite, execution_manifest)
    # console.log: phase6 corruption artifact build completed.
    console.log(
        "phase6.writer.build.complete "
        f"metric_manifest_hash={metric_manifest['corruption_metric_manifest_hash']}"
    )
    return metric_manifest


def _write_summary_outputs(
    repo_root: Path,
    config: dict[str, Any],
    summary_rows: list[dict[str, Any]],
) -> None:
    # console.log: phase6 locked/audit corruption summary writes begin.
    console.log("phase6.writer.summary_outputs.start")
    for run_mode in config["run_modes"]:
        rows = [row for row in summary_rows if row["run_mode"] == run_mode]
        _write_csv(repo_root / config["output_paths"][f"{run_mode}_summary"], rows, SUMMARY_FIELDS)
    # console.log: phase6 locked/audit corruption summary writes completed.
    console.log("phase6.writer.summary_outputs.complete")


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # console.log: phase6 CSV artifact write begins.
    console.log(f"phase6.writer.csv_write.start path={path} rows={len(rows)}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    # console.log: phase6 CSV artifact write completed.
    console.log(f"phase6.writer.csv_write.complete path={path}")

