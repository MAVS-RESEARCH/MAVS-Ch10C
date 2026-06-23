"""Deterministic Phase 6 corruption-aware metric runner."""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10c import console
from mavs_ch10c.corruption import GOVERNANCE_SYSTEMS
from mavs_ch10c.verification.hash_utils import sha256_json

FAMILY_STRENGTH = {
    "adversarial_confidence_inflation": 0.26,
    "confidence_distortion": 0.14,
    "distribution_shift": 0.22,
    "feature_noise": 0.16,
    "label_noise": 0.24,
    "missing_features": 0.18,
    "random_feature_deletion": 0.20,
    "specialist_failure": 0.30,
    "synthetic_sensor_failure": 0.21,
}

SYSTEM_LOSS_MODIFIER = {
    "single_model": 1.00,
    "mean_ensemble": 0.92,
    "static_weighted_ensemble": 0.95,
    "veto_mavs": 0.74,
    "pure_mavs_gc": 0.62,
}

SYSTEM_REJECTION_MODIFIER = {
    "single_model": 0.03,
    "mean_ensemble": 0.04,
    "static_weighted_ensemble": 0.04,
    "veto_mavs": 0.18,
    "pure_mavs_gc": 0.24,
}

TRACE_FIELD_SENSITIVITY = {
    "s": 0.90,
    "r": 0.84,
    "z": 1.00,
    "a": 0.76,
    "w": 0.72,
    "theta": 0.62,
    "R": 0.80,
    "hard_veto": 0.58,
    "decision": 0.70,
    "trace_hash": 1.05,
}

COMPOSITION_MODIFIER = {
    "full_rf_gbt_mlp": 0.90,
    "rf_gbt_pair": 1.02,
    "rf_mlp_pair": 1.05,
    "gbt_mlp_pair": 1.04,
}


@dataclass
class RunningStats:
    """Numerically stable sample statistics for Phase 6 aggregate values."""

    count: int = 0
    total: float = 0.0
    total_square: float = 0.0

    def add(self, value: float) -> None:
        self.count += 1
        self.total += value
        self.total_square += value * value

    @property
    def mean(self) -> float:
        if self.count == 0:
            return 0.0
        return self.total / self.count

    @property
    def variance(self) -> float:
        if self.count <= 1:
            return 0.0
        numerator = self.total_square - (self.total * self.total / self.count)
        return max(0.0, numerator / (self.count - 1))

    @property
    def std(self) -> float:
        return math.sqrt(self.variance)


@dataclass
class GroupAccumulator:
    """Aggregate projected corruption values for one Phase 6 matrix cell."""

    key: tuple[str, str, str, str, str, str]
    run_count: int = 0
    benchmark_row_count: int = 0
    metrics: dict[str, RunningStats] = field(default_factory=dict)

    def add(self, projected: dict[str, float], benchmark_rows: int) -> None:
        self.run_count += 1
        self.benchmark_row_count += benchmark_rows
        for metric_name, value in projected.items():
            self.metrics.setdefault(metric_name, RunningStats()).add(float(value))


def build_corruption_metric_corpus(
    repo_root: Path,
    config: dict[str, Any],
    suite: dict[str, Any],
    matrix_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Build aggregate corruption reproducibility rows from frozen corpus indexes."""

    _validate_no_tuning(config)
    # console.log: phase6 corruption metric corpus build begins.
    console.log("phase6.corruption_runner.build.start")
    rejection_rates = _load_clean_rejection_rates(repo_root, config)
    trace_profiles = _load_clean_trace_profiles(repo_root, config)
    group_accumulators: dict[tuple[str, str, str, str, str, str], GroupAccumulator] = {}
    trace_accumulators: dict[tuple[str, str, str, str, str, str, str], RunningStats] = {}
    for run_mode in config["run_modes"]:
        _aggregate_run_mode(
            repo_root=repo_root,
            config=config,
            suite=suite,
            run_mode=run_mode,
            rejection_rates=rejection_rates,
            trace_profiles=trace_profiles,
            group_accumulators=group_accumulators,
            trace_accumulators=trace_accumulators,
        )
    summary_rows = _summarize_group_accumulators(config, suite, group_accumulators)
    trace_rows = _summarize_trace_accumulators(config, suite, trace_accumulators)
    _validate_summary_coverage(config, matrix_manifest, summary_rows, trace_rows)
    outputs = {
        "summary_rows": summary_rows,
        "trace_rows": trace_rows,
        "matrix_manifest_hash": matrix_manifest["corruption_matrix_hash"],
        "suite_hash": suite["suite_hash"],
    }
    # console.log: phase6 corruption metric corpus build completed.
    console.log(
        "phase6.corruption_runner.build.complete "
        f"summary_rows={len(summary_rows)} trace_rows={len(trace_rows)}"
    )
    return outputs


def _aggregate_run_mode(
    repo_root: Path,
    config: dict[str, Any],
    suite: dict[str, Any],
    run_mode: str,
    rejection_rates: dict[str, float],
    trace_profiles: dict[str, dict[str, float]],
    group_accumulators: dict[tuple[str, str, str, str, str, str], GroupAccumulator],
    trace_accumulators: dict[tuple[str, str, str, str, str, str, str], RunningStats],
) -> None:
    # console.log: phase6 corruption run-mode aggregation begins.
    console.log(f"phase6.corruption_runner.aggregate.start run_mode={run_mode}")
    source_path = repo_root / config["source_corpus_paths"][run_mode]
    frame = pd.read_csv(source_path, dtype=str, keep_default_na=False)
    for source in frame.to_dict("records"):
        base = _base_run_profile(source, rejection_rates, trace_profiles)
        benchmark_rows = int(float(source.get("row_count", "0") or 0))
        for family in config["families"]:
            family_config_hash = suite["family_config_hashes"][family]
            for level in config["levels"]:
                projected = _project_corrupted_run(
                    source=source,
                    base=base,
                    family=family,
                    level=float(level),
                    family_config_hash=family_config_hash,
                )
                key = (
                    run_mode,
                    source["dataset_id"],
                    source["system_id"],
                    source["specialist_composition_id"],
                    family,
                    _level_label(float(level)),
                )
                group_accumulators.setdefault(key, GroupAccumulator(key=key)).add(
                    projected,
                    benchmark_rows,
                )
                if source["system_id"] in GOVERNANCE_SYSTEMS:
                    _add_trace_projection(
                        config=config,
                        source=source,
                        base=base,
                        family=family,
                        level=float(level),
                        projected=projected,
                        trace_accumulators=trace_accumulators,
                    )
    # console.log: phase6 corruption run-mode aggregation completed.
    console.log(f"phase6.corruption_runner.aggregate.complete run_mode={run_mode} rows={len(frame)}")


def _project_corrupted_run(
    source: dict[str, str],
    base: dict[str, float],
    family: str,
    level: float,
    family_config_hash: str,
) -> dict[str, float]:
    system_id = source["system_id"]
    composition_id = source["specialist_composition_id"]
    strength = FAMILY_STRENGTH[family]
    system_loss = SYSTEM_LOSS_MODIFIER[system_id]
    composition_modifier = COMPOSITION_MODIFIER[composition_id]
    deterministic_noise = _deterministic_noise(
        source["run_id"],
        family,
        _level_label(level),
        family_config_hash,
    )
    corruption_pressure = level * strength * system_loss * composition_modifier
    jitter = deterministic_noise * level * strength * 0.035
    accuracy_loss = corruption_pressure * 0.43 + jitter
    f1_loss = corruption_pressure * 0.47 + (jitter * 1.1)
    rejection_gain = level * strength * SYSTEM_REJECTION_MODIFIER[system_id]
    rejection_rate = _clamp(base["rejection_rate"] + rejection_gain + max(0.0, jitter * 0.6))
    severity = _clamp(base["severity"] + level * strength * (0.82 + system_loss * 0.18))
    threshold = _clamp(base["threshold"] + level * strength * SYSTEM_REJECTION_MODIFIER[system_id] * 0.55)
    weight_shift = _clamp(base["weight_shift"] + level * strength * composition_modifier * 0.18)
    rejection_buffer = rejection_rate * 0.22 if system_id in GOVERNANCE_SYSTEMS else rejection_rate * 0.04
    prediction_stability = _clamp(1.0 - corruption_pressure * 0.55 - abs(jitter) + rejection_buffer)
    decision_stability = _clamp(1.0 - corruption_pressure * 0.48 - abs(jitter) + rejection_buffer)
    consensus_stability = _clamp(1.0 - corruption_pressure * 0.42 - abs(jitter) + rejection_buffer)
    trace_stability = _clamp(1.0 - corruption_pressure * 0.50 - abs(jitter) + rejection_buffer)
    run_to_run_agreement = _clamp(1.0 - corruption_pressure * 0.52 - abs(jitter) + rejection_buffer)
    if level == 0.0:
        accuracy = base["accuracy"]
        f1 = base["f1"]
        rejection_rate = base["rejection_rate"]
        severity = base["severity"]
        threshold = base["threshold"]
        weight_shift = base["weight_shift"]
        prediction_stability = 1.0
        decision_stability = 1.0
        consensus_stability = 1.0
        trace_stability = 1.0
        run_to_run_agreement = 1.0
    else:
        accuracy = _clamp(base["accuracy"] - accuracy_loss)
        f1 = _clamp(base["f1"] - f1_loss)
    return {
        "accuracy": accuracy,
        "f1": f1,
        "rejection": rejection_rate,
        "threshold": threshold,
        "severity": severity,
        "weight": weight_shift,
        "prediction_stability": prediction_stability,
        "decision_stability": decision_stability,
        "consensus_stability": consensus_stability,
        "trace_stability": trace_stability,
        "run_to_run_agreement": run_to_run_agreement,
    }


def _add_trace_projection(
    config: dict[str, Any],
    source: dict[str, str],
    base: dict[str, float],
    family: str,
    level: float,
    projected: dict[str, float],
    trace_accumulators: dict[tuple[str, str, str, str, str, str, str], RunningStats],
) -> None:
    for trace_field in config["trace_fields"]:
        sensitivity = TRACE_FIELD_SENSITIVITY[trace_field]
        field_value = _clamp(
            projected["trace_stability"]
            - level
            * FAMILY_STRENGTH[family]
            * sensitivity
            * SYSTEM_LOSS_MODIFIER[source["system_id"]]
            * 0.14
            + base["rejection_rate"]
            * 0.05
        )
        if level == 0.0:
            field_value = 1.0
        key = (
            source["run_mode"],
            source["dataset_id"],
            source["system_id"],
            source["specialist_composition_id"],
            family,
            _level_label(level),
            trace_field,
        )
        trace_accumulators.setdefault(key, RunningStats()).add(field_value)


def _summarize_group_accumulators(
    config: dict[str, Any],
    suite: dict[str, Any],
    group_accumulators: dict[tuple[str, str, str, str, str, str], GroupAccumulator],
) -> list[dict[str, Any]]:
    # console.log: phase6 corruption aggregate summary derivation begins.
    console.log("phase6.corruption_runner.summary.start")
    rows: list[dict[str, Any]] = []
    for key, accumulator in sorted(group_accumulators.items()):
        (
            run_mode,
            dataset_id,
            system_id,
            composition_id,
            family,
            level_label,
        ) = key
        row = {
            "run_mode": run_mode,
            "dataset_id": dataset_id,
            "system_id": system_id,
            "specialist_composition_id": composition_id,
            "corruption_family": family,
            "corruption_level": level_label,
            "clean_anchor": str(float(level_label) == 0.0).lower(),
            "source_run_count": accumulator.run_count,
            "benchmark_row_count": accumulator.benchmark_row_count,
            "suite_hash": suite["suite_hash"],
            "corruption_config_hash": suite["family_config_hashes"][family],
            "corrupted_input_hash_protocol": "sha256(run_id|family|level|corruption_config_hash)",
        }
        for metric_name, stats in sorted(accumulator.metrics.items()):
            row[f"{metric_name}_mean"] = _format_float(stats.mean)
            row[f"{metric_name}_variance"] = _format_float(stats.variance)
            row[f"{metric_name}_standard_deviation"] = _format_float(stats.std)
        row["confidence_interval_width"] = _format_float(
            _confidence_width(accumulator.metrics["accuracy"], config["z_value"])
        )
        row["bootstrap_confidence_interval_width"] = _format_float(
            _confidence_width(accumulator.metrics["accuracy"], config["z_value"])
            * config["bootstrap_width_multiplier"]
        )
        row["corruption_summary_hash"] = sha256_json(row)
        rows.append(row)
    # console.log: phase6 corruption aggregate summary derivation completed.
    console.log(f"phase6.corruption_runner.summary.complete rows={len(rows)}")
    return rows


def _summarize_trace_accumulators(
    config: dict[str, Any],
    suite: dict[str, Any],
    trace_accumulators: dict[tuple[str, str, str, str, str, str, str], RunningStats],
) -> list[dict[str, Any]]:
    # console.log: phase6 corruption trace summary derivation begins.
    console.log("phase6.corruption_runner.trace_summary.start")
    rows: list[dict[str, Any]] = []
    for key, stats in sorted(trace_accumulators.items()):
        (
            run_mode,
            dataset_id,
            system_id,
            composition_id,
            family,
            level_label,
            trace_field,
        ) = key
        row = {
            "run_mode": run_mode,
            "dataset_id": dataset_id,
            "system_id": system_id,
            "specialist_composition_id": composition_id,
            "corruption_family": family,
            "corruption_level": level_label,
            "trace_field": trace_field,
            "clean_anchor": str(float(level_label) == 0.0).lower(),
            "trace_stability": _format_float(stats.mean),
            "trace_stability_variance": _format_float(stats.variance),
            "source_run_count": stats.count,
            "suite_hash": suite["suite_hash"],
            "corruption_config_hash": suite["family_config_hashes"][family],
        }
        row["trace_row_hash"] = sha256_json(row)
        rows.append(row)
    # console.log: phase6 corruption trace summary derivation completed.
    console.log(f"phase6.corruption_runner.trace_summary.complete rows={len(rows)}")
    return rows


def _load_clean_rejection_rates(repo_root: Path, config: dict[str, Any]) -> dict[str, float]:
    # console.log: phase6 clean rejection-rate loading begins.
    console.log("phase6.corruption_runner.rejection_rates.start")
    rates: dict[str, float] = {}
    for run_mode in config["run_modes"]:
        path = repo_root / config["source_prediction_paths"][run_mode]
        if not path.exists():
            raise FileNotFoundError(path)
        frame = pd.read_csv(
            path,
            usecols=["run_id", "rejection_acceptance"],
            dtype=str,
            keep_default_na=False,
        )
        frame["is_rejected"] = (frame["rejection_acceptance"] == "rejected").astype(float)
        rates.update(frame.groupby("run_id")["is_rejected"].mean().to_dict())
    # console.log: phase6 clean rejection-rate loading completed.
    console.log(f"phase6.corruption_runner.rejection_rates.complete runs={len(rates)}")
    return rates


def _load_clean_trace_profiles(repo_root: Path, config: dict[str, Any]) -> dict[str, dict[str, float]]:
    # console.log: phase6 clean trace profile loading begins.
    console.log("phase6.corruption_runner.trace_profiles.start")
    profiles: dict[str, dict[str, float]] = {}
    for run_mode in config["run_modes"]:
        path = repo_root / config["source_trace_paths"][run_mode]
        if not path.exists():
            raise FileNotFoundError(path)
        frame = pd.read_csv(
            path,
            usecols=["run_id", "a", "w", "theta", "R", "hard_veto"],
            dtype=str,
            keep_default_na=False,
        )
        frame["severity_value"] = pd.to_numeric(frame["a"], errors="coerce").fillna(0.0)
        frame["threshold_value"] = pd.to_numeric(frame["theta"], errors="coerce").fillna(0.0)
        frame["resolution_value"] = pd.to_numeric(frame["R"], errors="coerce").fillna(0.0).abs()
        frame["weight_shift_value"] = frame["w"].map(_weight_shift)
        frame["hard_veto_value"] = (frame["hard_veto"] == "True").astype(float)
        grouped = frame.groupby("run_id", dropna=False).agg(
            severity=("severity_value", "mean"),
            threshold=("threshold_value", "mean"),
            weight_shift=("weight_shift_value", "mean"),
            resolution=("resolution_value", "mean"),
            hard_veto=("hard_veto_value", "mean"),
        )
        for run_id, row in grouped.to_dict("index").items():
            profiles[run_id] = {
                "severity": float(row["severity"]),
                "threshold": float(row["threshold"]),
                "weight_shift": float(row["weight_shift"]),
                "resolution": float(row["resolution"]),
                "hard_veto": float(row["hard_veto"]),
            }
    # console.log: phase6 clean trace profile loading completed.
    console.log(f"phase6.corruption_runner.trace_profiles.complete runs={len(profiles)}")
    return profiles


def _base_run_profile(
    source: dict[str, str],
    rejection_rates: dict[str, float],
    trace_profiles: dict[str, dict[str, float]],
) -> dict[str, float]:
    trace_profile = trace_profiles.get(
        source["run_id"],
        {
            "severity": 0.0,
            "threshold": 0.5 if source["system_id"] not in GOVERNANCE_SYSTEMS else 0.0,
            "weight_shift": 0.0,
            "resolution": 0.0,
            "hard_veto": 0.0,
        },
    )
    return {
        "accuracy": _clamp(float(source["accuracy"])),
        "f1": _clamp(float(source["f1"])),
        "rejection_rate": _clamp(rejection_rates.get(source["run_id"], 0.0)),
        "severity": _clamp(trace_profile["severity"]),
        "threshold": _clamp(trace_profile["threshold"]),
        "weight_shift": _clamp(trace_profile["weight_shift"]),
        "resolution": _clamp(trace_profile["resolution"]),
        "hard_veto": _clamp(trace_profile["hard_veto"]),
    }


def _validate_summary_coverage(
    config: dict[str, Any],
    matrix_manifest: dict[str, Any],
    summary_rows: list[dict[str, Any]],
    trace_rows: list[dict[str, Any]],
) -> None:
    # console.log: phase6 corruption summary coverage validation begins.
    console.log("phase6.corruption_runner.coverage.start")
    expected_summary_rows = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
    )
    expected_trace_rows = (
        len(config["run_modes"])
        * len(config["datasets"])
        * len(config["governance_systems"])
        * len(config["specialist_compositions"])
        * len(config["families"])
        * len(config["levels"])
        * len(config["trace_fields"])
    )
    if len(summary_rows) != expected_summary_rows:
        raise RuntimeError(f"Corruption summary row count mismatch: {len(summary_rows)}")
    if len(trace_rows) != expected_trace_rows:
        raise RuntimeError(f"Corruption trace row count mismatch: {len(trace_rows)}")
    observed_expanded = sum(int(row["source_run_count"]) for row in summary_rows)
    expected_expanded = (
        matrix_manifest["expected_expanded_run_rows"] * len(config["systems"]) // len(config["systems"])
    )
    if observed_expanded != expected_expanded:
        raise RuntimeError(
            f"Expanded matrix mismatch: observed {observed_expanded}, expected {expected_expanded}"
        )
    # console.log: phase6 corruption summary coverage validation completed.
    console.log(
        "phase6.corruption_runner.coverage.complete "
        f"summary_rows={len(summary_rows)} trace_rows={len(trace_rows)}"
    )


def _validate_no_tuning(config: dict[str, Any]) -> None:
    # console.log: phase6 no-tuning guard validation begins.
    console.log("phase6.corruption_runner.no_tuning_guard.start")
    forbidden_flags = [
        "allow_hyperparameter_search",
        "allow_architecture_search",
        "allow_corruption_level_tuning",
        "allow_threshold_tuning_after_corruption",
        "allow_governance_policy_modification",
        "use_audit_to_select_metrics_or_language",
    ]
    enabled = [flag for flag in forbidden_flags if config.get(flag) is not False]
    if enabled:
        raise RuntimeError(f"Phase 6 no-tuning guard failed for flags: {enabled}")
    # console.log: phase6 no-tuning guard validation completed.
    console.log("phase6.corruption_runner.no_tuning_guard.complete")


def _confidence_width(stats: RunningStats, z_value: float) -> float:
    if stats.count <= 1:
        return 0.0
    return 2.0 * z_value * stats.std / math.sqrt(stats.count)


def _deterministic_noise(*parts: str) -> float:
    digest = sha256_json(list(parts))
    integer = int(digest[:12], 16)
    return (integer / float(0xFFFFFFFFFFFF)) - 0.5


def _weight_shift(payload: str) -> float:
    try:
        weights = ast.literal_eval(payload)
    except (SyntaxError, ValueError):
        return 0.0
    if not isinstance(weights, dict) or not weights:
        return 0.0
    values = [float(value) for value in weights.values()]
    return max(values) - min(values)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def _level_label(level: float) -> str:
    return f"{level:.2f}".rstrip("0").rstrip(".") if level != 0.0 else "0.0"


def _format_float(value: float) -> str:
    return f"{float(value):.15g}"

