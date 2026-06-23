"""Phase 5 reproducibility report generator."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.reporting import BASELINE_SYSTEMS, GOVERNANCE_SYSTEMS, PURE_MAVS_SYSTEM
from mavs_ch10c.reporting.artifact_manifest import build_reproducibility_manifest
from mavs_ch10c.reporting.figures import build_stability_figures
from mavs_ch10c.reporting.tables import build_report_tables
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file


def load_report_config(repo_root: Path, config_path: Path | None = None) -> dict[str, Any]:
    """Load the JSON-formatted Phase 5 report config."""

    path = config_path or repo_root / "configs" / "reports" / "reproducibility_report.yaml"
    return load_json_config(path)


def build_reproducibility_report(
    repo_root: Path,
    config_path: Path | None = None,
) -> dict[str, Any]:
    """Build report tables, figures, Markdown report, and artifact manifest."""

    # console.log: phase5 reproducibility report build begins.
    console.log("phase5.report.build.start")
    config = load_report_config(repo_root, config_path)
    tables = build_report_tables(repo_root, config)
    figures = build_stability_figures(repo_root, config, tables)
    report_text = _render_report(repo_root, config, tables)
    report_path = repo_root / config["output_paths"]["report"]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    manifest = build_reproducibility_manifest(repo_root, config)
    _validate_report_claims(repo_root, config, report_text)
    result = {
        "report_path": str(report_path),
        "report_hash": sha256_file(report_path),
        "manifest_path": str(repo_root / config["output_paths"]["artifact_manifest"]),
        "manifest_hash": manifest["reproducibility_artifact_manifest_hash"],
        "figure_count": len(figures),
        "variance_table_rows": len(tables["variance_tables"]),
        "stability_table_rows": len(tables["stability_tables"]),
        "delta_table_rows": len(tables["reproducibility_system_deltas"]),
    }
    # console.log: phase5 reproducibility report build completed.
    console.log(
        "phase5.report.build.complete "
        f"report_hash={result['report_hash']} manifest_hash={result['manifest_hash']}"
    )
    return result


def _render_report(
    repo_root: Path,
    config: dict[str, Any],
    tables: dict[str, list[dict[str, Any]]],
) -> str:
    # console.log: phase5 reproducibility report render begins.
    console.log("phase5.report.render.start")
    summary = _analysis_summary(repo_root, config, tables)
    report = "\n".join(
        [
            "# MAVS Chapter 10C Reproducibility Report",
            "",
            "## Source Authority",
            (
                "This report is generated from the Phase 1-4 artifacts declared in "
                "`configs/reports/reproducibility_report.yaml`. The primary local source "
                "context is `C:\\Users\\Saif malik\\Downloads\\Mavs.pdf`; the implementation "
                "contract is `WorkPlan.md`; and the implementation audit log is `Path.md`."
            ),
            "",
            "## Methodology",
            (
                "The report consumes frozen Phase 4 metric artifacts only. It does not train "
                "models, tune hyperparameters, modify governance policy, or use training, "
                "validation, or calibration diagnostics as final evidence."
            ),
            "",
            "## Imported Chapter 10A and 10B Foundation",
            (
                f"Chapter 10A commit `{summary['ch10a_commit']}` supplies datasets, model "
                "families, system semantics, and frozen governance hashes. Chapter 10B commit "
                f"`{summary['ch10b_commit']}` supplies artifact hashing and verification "
                "patterns. Both imports are referenced through "
                "`results/foundation_import/foundation_import_manifest.json`."
            ),
            "",
            "## Frozen Governance Policy",
            (
                "Pure MAVS-GC and Veto MAVS are treated as governance systems. Governance "
                "trace stability is evaluated only from trace fields already emitted by the "
                "frozen Phase 2 execution corpus and aligned in the Phase 3 variance rows."
            ),
            "",
            "## Repeated Execution Matrix",
            (
                f"Locked evidence covers {summary['locked_variance_rows']} variance rows; "
                f"audit evidence covers {summary['audit_variance_rows']} variance rows. "
                f"The locked corpus contains {summary['locked_model_fits']} model fits; "
                f"the audit corpus contains {summary['audit_model_fits']} model fits."
            ),
            "",
            "## Independent Benchmark Design",
            (
                "The locked and audit benchmark partitions are disjoint from train, "
                "validation, and calibration partitions. Audit seeds and schedules are "
                "independent from locked seeds and schedules. The report identifies locked "
                "and audit results separately in every generated table."
            ),
            "",
            "## Anti-Overfitting Controls",
            (
                "Metric definitions were frozen before report generation. The Phase 4 metric "
                "manifest records `training_performed=false`, "
                "`metric_definitions_selected_from_audit=false`, and "
                "`metrics_read_only_frozen_variance_datasets=true`. Positive, negative, and "
                "mixed outcomes are preserved in `results/reports/reproducibility_system_deltas.csv`."
            ),
            "",
            "## Results",
            _results_markdown(summary),
            "",
            "## Claim Register",
            _claim_register_markdown(summary),
            "",
            "## Limitations",
            (
                "The evidence is bounded to the four configured datasets, the five configured "
                "systems, the declared seed/split/init/composition matrix, and the empirical "
                "working-frame caps recorded in Phase 2 manifests. Chapter 10C evidence here "
                "does not evaluate corruption stress. Wider intervals, lower stability, and "
                "negative correctness deltas remain part of the final evidence."
            ),
            "",
            "## Final Answer to Chapter 10C",
            _final_answer(summary),
            "",
        ]
    )
    # console.log: phase5 reproducibility report render completed.
    console.log(f"phase5.report.render.complete claims={len(summary['claims'])}")
    return report


def _analysis_summary(
    repo_root: Path,
    config: dict[str, Any],
    tables: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    foundation = load_json_config(repo_root / config["input_paths"]["foundation_manifest"])
    locked_corpus = load_json_config(repo_root / config["input_paths"]["locked_corpus_manifest"])
    audit_corpus = load_json_config(repo_root / config["input_paths"]["audit_corpus_manifest"])
    variance_manifest = load_json_config(repo_root / config["input_paths"]["variance_manifest"])
    metric_manifest = load_json_config(repo_root / config["input_paths"]["metric_manifest"])
    variance_counts = _compare_pure_against_baselines(
        tables["variance_tables"], value_field="sample_variance", lower_is_better=True
    )
    ci_counts = _compare_pure_against_baselines(
        tables["variance_tables"], value_field="confidence_interval_width", lower_is_better=True
    )
    prediction_counts = _compare_pure_against_baselines(
        [
            row
            for row in tables["stability_tables"]
            if row["metric_name"] == "prediction_stability"
        ],
        value_field="reported_value",
        lower_is_better=False,
    )
    decision_counts = _compare_pure_against_baselines(
        [
            row
            for row in tables["stability_tables"]
            if row["metric_name"] == "decision_stability"
        ],
        value_field="reported_value",
        lower_is_better=False,
    )
    trace_counts = _compare_pure_against_veto_trace(tables["stability_tables"])
    delta_counts = Counter(
        row["direction_vs_baseline"] for row in tables["reproducibility_system_deltas"]
    )
    claims = _claims(
        variance_counts,
        ci_counts,
        prediction_counts,
        decision_counts,
        trace_counts,
        delta_counts,
    )
    return {
        "ch10a_commit": foundation["ch10a"]["commit"],
        "ch10b_commit": foundation["ch10b"]["commit"],
        "locked_variance_rows": variance_manifest["locked"]["variance_row_count"],
        "audit_variance_rows": variance_manifest["audit"]["variance_row_count"],
        "locked_model_fits": locked_corpus["model_fit_count"],
        "audit_model_fits": audit_corpus["model_fit_count"],
        "metric_manifest_hash": metric_manifest["reproducibility_metric_manifest_hash"],
        "source_variance_manifest_hash": metric_manifest["source_variance_manifest_hash"],
        "variance_counts": variance_counts,
        "ci_counts": ci_counts,
        "prediction_counts": prediction_counts,
        "decision_counts": decision_counts,
        "trace_counts": trace_counts,
        "delta_counts": dict(delta_counts),
        "locked_audit_consistency": metric_manifest["locked_audit_consistency"],
        "claims": claims,
    }


def _compare_pure_against_baselines(
    rows: list[dict[str, Any]],
    value_field: str,
    lower_is_better: bool,
) -> dict[str, Any]:
    by_key: dict[tuple[str, str, str, str, str], dict[str, dict[str, Any]]] = {}
    for row in rows:
        metric_key = row.get("metric_name", "")
        key = (
            row["run_mode"],
            row["dataset_id"],
            row["specialist_composition_id"],
            metric_key,
            row.get("compared_metric", ""),
        )
        by_key.setdefault(key, {})[row["system_id"]] = row
    counts = Counter()
    datasets: set[str] = set()
    baselines: set[str] = set()
    total = 0
    for key, systems in by_key.items():
        pure = systems.get(PURE_MAVS_SYSTEM)
        if not pure:
            continue
        pure_value = _to_float(pure.get(value_field, ""))
        if pure_value is None:
            continue
        for baseline in BASELINE_SYSTEMS:
            baseline_row = systems.get(baseline)
            if not baseline_row:
                continue
            baseline_value = _to_float(baseline_row.get(value_field, ""))
            if baseline_value is None:
                continue
            relation = _relation(pure_value, baseline_value, lower_is_better)
            counts[relation] += 1
            total += 1
            if relation == "better":
                datasets.add(key[1])
                baselines.add(baseline)
    return {
        "better": counts["better"],
        "neutral": counts["neutral"],
        "worse": counts["worse"],
        "total": total,
        "supporting_dataset_count": len(datasets),
        "supporting_baseline_count": len(baselines),
    }


def _compare_pure_against_veto_trace(rows: list[dict[str, Any]]) -> dict[str, Any]:
    trace_rows = [row for row in rows if row["metric_name"] == "trace_stability"]
    by_key: dict[tuple[str, str, str, str], dict[str, dict[str, Any]]] = {}
    for row in trace_rows:
        key = (
            row["run_mode"],
            row["dataset_id"],
            row["specialist_composition_id"],
            row["trace_field"],
        )
        by_key.setdefault(key, {})[row["system_id"]] = row
    counts = Counter()
    total = 0
    for systems in by_key.values():
        pure = systems.get(PURE_MAVS_SYSTEM)
        veto = systems.get("veto_mavs")
        if not pure or not veto:
            continue
        pure_value = _to_float(pure["reported_value"])
        veto_value = _to_float(veto["reported_value"])
        if pure_value is None or veto_value is None:
            continue
        counts[_relation(pure_value, veto_value, lower_is_better=False)] += 1
        total += 1
    return {
        "better": counts["better"],
        "neutral": counts["neutral"],
        "worse": counts["worse"],
        "total": total,
    }


def _claims(
    variance_counts: dict[str, Any],
    ci_counts: dict[str, Any],
    prediction_counts: dict[str, Any],
    decision_counts: dict[str, Any],
    trace_counts: dict[str, Any],
    delta_counts: Counter[str],
) -> list[dict[str, str]]:
    return [
        {
            "id": "C1",
            "claim": (
                "Pure MAVS-GC shows lower variance in "
                f"{variance_counts['better']}/{variance_counts['total']} paired comparisons."
            ),
            "classification": _support_label(variance_counts),
            "evidence": (
                "`results/reports/variance_tables.csv`; "
                "`results/figures/accuracy_variance_by_system.png`; "
                "`results/figures/f1_variance_by_system.png`"
            ),
        },
        {
            "id": "C2",
            "claim": (
                "Pure MAVS-GC shows higher prediction stability in "
                f"{prediction_counts['better']}/{prediction_counts['total']} comparisons."
            ),
            "classification": _support_label(prediction_counts),
            "evidence": (
                "`results/reports/stability_tables.csv`; "
                "`results/figures/prediction_stability_by_system.png`"
            ),
        },
        {
            "id": "C3",
            "claim": (
                "Pure MAVS-GC shows higher final decision stability in "
                f"{decision_counts['better']}/{decision_counts['total']} comparisons."
            ),
            "classification": _support_label(decision_counts),
            "evidence": (
                "`results/reports/stability_tables.csv`; "
                "`results/figures/decision_stability_by_system.png`"
            ),
        },
        {
            "id": "C4",
            "claim": (
                "Pure MAVS-GC trace similarity is higher than Veto MAVS in "
                f"{trace_counts['better']}/{trace_counts['total']} governance trace comparisons."
            ),
            "classification": _support_label(trace_counts),
            "evidence": (
                "`results/reports/stability_tables.csv`; "
                "`results/figures/trace_stability_by_system.png`"
            ),
        },
        {
            "id": "C5",
            "claim": (
                "Pure MAVS-GC has narrower confidence intervals in "
                f"{ci_counts['better']}/{ci_counts['total']} comparisons."
            ),
            "classification": _support_label(ci_counts),
            "evidence": (
                "`results/reports/variance_tables.csv`; "
                "`results/figures/confidence_interval_widths.png`"
            ),
        },
        {
            "id": "C6",
            "claim": (
                "Correctness deltas are mixed: "
                f"{delta_counts.get('pure_mavs_higher', 0)} higher, "
                f"{_neutral_delta_count(delta_counts)} neutral, "
                f"{delta_counts.get('pure_mavs_lower', 0)} lower."
            ),
            "classification": "mixed_tradeoff",
            "evidence": "`results/reports/reproducibility_system_deltas.csv`",
        },
        {
            "id": "C7",
            "claim": "Locked and audit evidence use matching metric families, systems, and baselines.",
            "classification": "supported_artifact_scope",
            "evidence": (
                "`results/stability_metrics/reproducibility_metric_manifest.json`; "
                "`results/reports/reproducibility_artifact_manifest.json`"
            ),
        },
    ]


def _results_markdown(summary: dict[str, Any]) -> str:
    variance = summary["variance_counts"]
    prediction = summary["prediction_counts"]
    decision = summary["decision_counts"]
    trace = summary["trace_counts"]
    ci = summary["ci_counts"]
    delta = summary["delta_counts"]
    return "\n".join(
        [
            (
                f"- Variance: Pure MAVS-GC is lower in {variance['better']} of "
                f"{variance['total']} paired variance comparisons."
            ),
            (
                f"- Prediction stability: Pure MAVS-GC is higher in {prediction['better']} "
                f"of {prediction['total']} paired comparisons."
            ),
            (
                f"- Decision stability: Pure MAVS-GC is higher in {decision['better']} "
                f"of {decision['total']} paired comparisons."
            ),
            (
                f"- Governance traces: Pure MAVS-GC trace similarity is higher than Veto "
                f"MAVS in {trace['better']} of {trace['total']} trace-field comparisons."
            ),
            (
                f"- Confidence intervals: Pure MAVS-GC is narrower in {ci['better']} of "
                f"{ci['total']} interval-width comparisons."
            ),
            (
                "- Correctness deltas: "
                f"{delta.get('pure_mavs_higher', 0)} higher, "
                f"{_neutral_delta_count(delta)} neutral, "
                f"{delta.get('pure_mavs_lower', 0)} lower."
            ),
        ]
    )


def _claim_register_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "| Claim ID | Claim | Classification | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    for claim in summary["claims"]:
        lines.append(
            f"| {claim['id']} | {claim['claim']} | {claim['classification']} | "
            f"{claim['evidence']} |"
        )
    return "\n".join(lines)


def _final_answer(summary: dict[str, Any]) -> str:
    variance = summary["variance_counts"]
    prediction = summary["prediction_counts"]
    decision = summary["decision_counts"]
    if (
        variance["better"] > variance["worse"]
        and prediction["better"] > prediction["worse"]
        and decision["better"] > decision["worse"]
    ):
        return (
            "The Phase 5 evidence supports a bounded, artifact-scoped conclusion that Pure "
            "MAVS-GC can improve parts of reproducibility under the configured repeated "
            "matrix, but the result remains mixed because correctness deltas and interval "
            "widths include negative and neutral cases."
        )
    return (
        "The Phase 5 evidence does not support an unconditional reproducibility advantage "
        "for Pure MAVS-GC. The supported conclusion is mixed and artifact-scoped: some "
        "variance and stability comparisons improve, while other comparisons are neutral "
        "or worse and must remain part of the final record."
    )


def _validate_report_claims(repo_root: Path, config: dict[str, Any], text: str) -> None:
    claim_lines = [
        line
        for line in text.splitlines()
        if line.startswith("| C") and len(line) > 3 and line[3].isdigit()
    ]
    if len(claim_lines) < 7:
        raise RuntimeError(f"Expected at least 7 claim rows, found {len(claim_lines)}")
    for line in claim_lines:
        artifacts = [part.split("`", 1)[0] for part in line.split("`")[1::2]]
        if not artifacts:
            raise RuntimeError(f"Claim lacks artifact references: {line}")
        for artifact in artifacts:
            if artifact.startswith("results/") and not (repo_root / artifact).exists():
                raise RuntimeError(f"Claim references missing artifact: {artifact}")
    for figure_path in config["figure_paths"].values():
        path = repo_root / figure_path
        if not path.exists() or path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError(f"Invalid required PNG figure: {path}")


def _relation(left: float, right: float, lower_is_better: bool) -> str:
    tolerance = 1e-12
    if abs(left - right) <= tolerance:
        return "neutral"
    if lower_is_better:
        return "better" if left < right else "worse"
    return "better" if left > right else "worse"


def _support_label(counts: dict[str, Any]) -> str:
    if counts["total"] == 0:
        return "unsupported_no_rows"
    if counts["better"] > counts["worse"]:
        return "mixed_positive"
    if counts["better"] == counts["worse"]:
        return "mixed_neutral"
    return "mixed_negative"


def _neutral_delta_count(delta_counts: dict[str, Any]) -> int:
    return int(delta_counts.get("pure_mavs_equal", 0)) + int(delta_counts.get("neutral", 0)) + int(
        delta_counts.get("no_change", 0)
    )


def _to_float(value: str) -> float | None:
    if value == "":
        return None
    return float(value)
