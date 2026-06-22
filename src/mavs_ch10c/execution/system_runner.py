"""Empirical system execution for Phase 2."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from itertools import product
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, log_loss

from mavs_ch10c import console
from mavs_ch10c.execution.specialist_runner import SpecialistOutputBundle
from mavs_ch10c.verification.hash_utils import sha256_json

GOVERNANCE_SYSTEMS = {"veto_mavs", "pure_mavs_gc"}

GOVERNANCE_TRACE_FIELDS = [
    "x_id",
    "row_hash",
    "dataset_id",
    "run_mode",
    "execution_seed",
    "split_schedule_id",
    "initialization_schedule_id",
    "specialist_composition_id",
    "system_id",
    "specialist_ids",
    "s",
    "r",
    "z",
    "a",
    "w",
    "m",
    "theta",
    "R",
    "hard_veto",
    "decision",
    "label",
    "config_hash",
    "checkpoint_hashes",
    "trace_hash",
]


@dataclass(frozen=True)
class SystemExecutionRecord:
    run_id: str
    repetition_id: str
    run_mode: str
    dataset_id: str
    system_id: str
    execution_seed: int
    split_schedule_id: str
    initialization_schedule_id: str
    specialist_composition_id: str
    specialist_ids: str
    specialist_output_hash: str
    probability_matrix_hash: str
    prediction_hash: str
    decision_hash: str
    label_hash: str
    trace_hash: str
    trace_schema_hash: str
    governance_trace_complete: bool
    system_config_hash: str
    run_manifest_hash: str
    row_count: int
    accuracy: float
    f1: float


@dataclass(frozen=True)
class SystemExecutionResult:
    record: SystemExecutionRecord
    prediction_rows: list[dict[str, Any]]
    trace_rows: list[dict[str, Any]]
    frozen_run_manifest: dict[str, Any]
    run_manifest: dict[str, Any]


def run_system_from_bundle(
    unit: dict[str, Any],
    bundle: SpecialistOutputBundle,
    system_config_hashes: dict[str, str],
    system_configs: dict[str, dict[str, Any]],
    governance_config: dict[str, Any],
) -> SystemExecutionResult:
    """Execute one comparison system on shared specialist outputs."""

    # console.log: phase2 empirical system execution begins.
    console.log(
        "phase2.system_runner.execute.start "
        f"system={unit['system_id']} repetition={unit['repetition_id']}"
    )
    system_id = str(unit["system_id"])
    system_config_hash = _lookup_system_config_hash(system_id, system_config_hashes)
    frozen_run_manifest = _build_frozen_run_manifest(
        unit=unit,
        bundle=bundle,
        system_id=system_id,
        system_config_hash=system_config_hash,
        governance_config=governance_config,
    )
    probabilities, decisions, trace_payload = _execute_system(
        system_id, bundle, system_configs[system_id], governance_config
    )
    prediction_rows = _build_prediction_rows(
        unit, bundle, probabilities, decisions, trace_payload
    )
    trace_rows = trace_payload["trace_rows"]
    prediction_hash = _hash_array(probabilities)
    decision_hash = _hash_array(decisions)
    trace_hash = sha256_json(trace_rows) if trace_rows else ""
    trace_schema_hash = sha256_json(GOVERNANCE_TRACE_FIELDS) if trace_rows else ""
    base = {
        "repetition_id": unit["repetition_id"],
        "system_id": system_id,
        "specialist_output_hash": bundle.specialist_output_hash,
        "probability_matrix_hash": bundle.probability_matrix_hash,
        "prediction_hash": prediction_hash,
        "decision_hash": decision_hash,
        "label_hash": bundle.label_hash,
        "system_config_hash": system_config_hash,
    }
    run_manifest_hash = sha256_json(
        {
            **base,
            "pre_execution_manifest_hash": frozen_run_manifest["pre_execution_manifest_hash"],
            "artifact": "run_manifest",
        }
    )
    record = SystemExecutionRecord(
        run_id=sha256_json(base)[:24],
        repetition_id=str(unit["repetition_id"]),
        run_mode=str(unit["run_mode"]),
        dataset_id=str(unit["dataset_id"]),
        system_id=system_id,
        execution_seed=int(unit["execution_seed"]),
        split_schedule_id=str(unit["split_schedule_id"]),
        initialization_schedule_id=str(unit["initialization_schedule_id"]),
        specialist_composition_id=str(unit["specialist_composition_id"]),
        specialist_ids=",".join(bundle.specialist_ids),
        specialist_output_hash=bundle.specialist_output_hash,
        probability_matrix_hash=bundle.probability_matrix_hash,
        prediction_hash=prediction_hash,
        decision_hash=decision_hash,
        label_hash=bundle.label_hash,
        trace_hash=trace_hash,
        trace_schema_hash=trace_schema_hash,
        governance_trace_complete=bool(system_id in GOVERNANCE_SYSTEMS and trace_rows),
        system_config_hash=system_config_hash,
        run_manifest_hash=run_manifest_hash,
        row_count=int(len(bundle.labels)),
        accuracy=float(accuracy_score(bundle.labels, decisions)),
        f1=float(f1_score(bundle.labels, decisions, zero_division=0)),
    )
    for row in prediction_rows:
        row["trace_schema_hash"] = trace_schema_hash
        row["system_config_hash"] = system_config_hash
    run_manifest = {
        **record.__dict__,
        "checkpoint_hashes": bundle.checkpoint_hashes,
        "benchmark_partition_hash": bundle.benchmark_partition_hash,
        "pre_execution_manifest_hash": frozen_run_manifest["pre_execution_manifest_hash"],
        "final_evidence_split": bundle.run_mode,
        "training_diagnostics_are_final_evidence": False,
    }
    # console.log: phase2 empirical system execution completed.
    console.log(
        "phase2.system_runner.execute.complete "
        f"run_id={record.run_id} rows={record.row_count} f1={record.f1:.6f}"
    )
    return SystemExecutionResult(record, prediction_rows, trace_rows, frozen_run_manifest, run_manifest)


def _build_frozen_run_manifest(
    *,
    unit: dict[str, Any],
    bundle: SpecialistOutputBundle,
    system_id: str,
    system_config_hash: str,
    governance_config: dict[str, Any],
) -> dict[str, Any]:
    """Build the run manifest that is frozen before system execution."""

    manifest = {
        "manifest_type": "pre_execution_frozen_run_manifest",
        "repetition_id": str(unit["repetition_id"]),
        "run_mode": str(unit["run_mode"]),
        "dataset_id": str(unit["dataset_id"]),
        "system_id": system_id,
        "execution_seed": int(unit["execution_seed"]),
        "split_schedule_id": str(unit["split_schedule_id"]),
        "initialization_schedule_id": str(unit["initialization_schedule_id"]),
        "specialist_composition_id": str(unit["specialist_composition_id"]),
        "specialist_ids": ",".join(bundle.specialist_ids),
        "specialist_output_hash": bundle.specialist_output_hash,
        "probability_matrix_hash": bundle.probability_matrix_hash,
        "label_hash": bundle.label_hash,
        "benchmark_partition_hash": bundle.benchmark_partition_hash,
        "checkpoint_hashes": dict(bundle.checkpoint_hashes),
        "system_config_hash": system_config_hash,
        "governance_config_hash": sha256_json(governance_config),
        "training_diagnostics_are_final_evidence": False,
        "allowed_final_evidence_split": str(unit["run_mode"]),
    }
    manifest["pre_execution_manifest_hash"] = sha256_json(manifest)
    # console.log: phase2 frozen pre-execution run manifest built.
    console.log(
        "phase2.system_runner.frozen_manifest.complete "
        f"repetition={manifest['repetition_id']} system={system_id}"
    )
    return manifest


def _execute_system(
    system_id: str,
    bundle: SpecialistOutputBundle,
    system_config: dict[str, Any],
    governance_config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    threshold = float(system_config.get("decision", {}).get("probability_threshold", 0.5))
    if system_id == "single_model":
        selected_index = _select_single_model(bundle, system_config)
        probabilities = bundle.probabilities[:, selected_index]
        hard_veto = np.zeros(len(bundle.labels), dtype=bool)
        decisions = _binary_decisions(probabilities, threshold)
        traces: list[dict[str, Any]] = []
    elif system_id == "mean_ensemble":
        probabilities = np.mean(bundle.probabilities, axis=1)
        hard_veto = np.zeros(len(bundle.labels), dtype=bool)
        decisions = _binary_decisions(probabilities, threshold)
        traces = []
    elif system_id == "static_weighted_ensemble":
        weights = _fit_static_weights(bundle, system_config)
        probabilities = bundle.probabilities @ weights
        hard_veto = np.zeros(len(bundle.labels), dtype=bool)
        decisions = _binary_decisions(probabilities, threshold)
        traces = []
    elif system_id == "veto_mavs":
        probabilities, decisions, hard_veto, traces = _run_veto_mavs(
            bundle, system_config, governance_config
        )
    elif system_id == "pure_mavs_gc":
        probabilities, decisions, hard_veto, traces = _run_pure_mavs_gc(
            bundle, system_config, governance_config
        )
    else:
        raise ValueError(f"Unsupported system id: {system_id}")
    return probabilities, decisions, {
        "hard_veto": hard_veto,
        "trace_rows": traces,
    }


def _select_single_model(bundle: SpecialistOutputBundle, system_config: dict[str, Any]) -> int:
    selection = system_config.get("selection", {})
    tie_breaker = list(selection.get("tie_breaker", bundle.specialist_ids))
    best_index = 0
    best_value = None
    for model_id in tie_breaker:
        if model_id not in bundle.specialist_ids:
            continue
        index = bundle.specialist_ids.index(model_id)
        value = float(
            f1_score(
                bundle.validation_labels,
                _binary_decisions(bundle.validation_probabilities[:, index], 0.5),
                zero_division=0,
            )
        )
        if best_value is None or value > best_value:
            best_value = value
            best_index = index
    # console.log: phase2 single-model validation selection completed.
    console.log(
        "phase2.system_runner.single_model.select "
        f"model={bundle.specialist_ids[best_index]} validation_f1={best_value:.6f}"
    )
    return best_index


def _fit_static_weights(bundle: SpecialistOutputBundle, system_config: dict[str, Any]) -> np.ndarray:
    step = float(system_config.get("fit", {}).get("grid_step", 0.05))
    candidates = _simplex_grid(len(bundle.specialist_ids), step)
    best_weights = candidates[0]
    best_loss = float("inf")
    for weights in candidates:
        probabilities = np.clip(bundle.validation_probabilities @ weights, 1e-9, 1.0 - 1e-9)
        current_loss = float(
            log_loss(bundle.validation_labels, np.column_stack([1.0 - probabilities, probabilities]))
        )
        if current_loss < best_loss:
            best_loss = current_loss
            best_weights = weights
    # console.log: phase2 static weights validation fit completed.
    console.log(
        "phase2.system_runner.static_weights.fit "
        f"specialists={list(bundle.specialist_ids)} validation_log_loss={best_loss:.8f}"
    )
    return best_weights


def _run_veto_mavs(
    bundle: SpecialistOutputBundle,
    system_config: dict[str, Any],
    governance_config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[dict[str, Any]]]:
    probabilities = np.mean(bundle.probabilities, axis=1)
    diagnostics = _compute_diagnostics(bundle.probabilities, bundle.supports)
    severity = _aggregate_severity(diagnostics, governance_config["severity"])
    hard_veto = severity >= float(governance_config["policy"]["hard_veto_threshold"])
    threshold = float(system_config["decision"]["probability_threshold"])
    decisions = np.where(hard_veto, 0, _binary_decisions(probabilities, threshold)).astype(np.int8)
    consensus = 2.0 * probabilities - 1.0
    theta = np.full(len(bundle.labels), 2.0 * threshold - 1.0)
    weights = np.full_like(bundle.supports, 1.0 / bundle.supports.shape[1], dtype=np.float64)
    traces = _build_trace_rows(
        bundle, "veto_mavs", diagnostics, severity, weights, theta, consensus, hard_veto, decisions
    )
    # console.log: phase2 Veto MAVS empirical execution completed.
    console.log(f"phase2.system_runner.veto_mavs.complete hard_vetoes={int(hard_veto.sum())}")
    return probabilities, decisions, hard_veto, traces


def _run_pure_mavs_gc(
    bundle: SpecialistOutputBundle,
    system_config: dict[str, Any],
    governance_config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[dict[str, Any]]]:
    diagnostics = _compute_diagnostics(bundle.probabilities, bundle.supports)
    severity = _aggregate_severity(diagnostics, governance_config["severity"])
    weights = _compute_governed_weights(bundle.supports, severity, governance_config["rebalancer"])
    consensus = np.sum(weights * bundle.supports, axis=1)
    theta = (
        float(governance_config["policy"]["theta0"])
        + float(governance_config["policy"]["lambda"]) * severity
    )
    hard_veto = severity >= float(governance_config["policy"]["hard_veto_threshold"])
    decisions = ((consensus >= theta) & (~hard_veto)).astype(np.int8)
    probabilities = np.clip((consensus + 1.0) / 2.0, 0.0, 1.0)
    traces = _build_trace_rows(
        bundle, "pure_mavs_gc", diagnostics, severity, weights, theta, consensus, hard_veto, decisions
    )
    # console.log: phase2 Pure MAVS-GC empirical execution completed.
    console.log(f"phase2.system_runner.pure_mavs_gc.complete hard_vetoes={int(hard_veto.sum())}")
    return probabilities, decisions, hard_veto, traces


def _build_prediction_rows(
    unit: dict[str, Any],
    bundle: SpecialistOutputBundle,
    probabilities: np.ndarray,
    decisions: np.ndarray,
    trace_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    hard_veto = trace_payload["hard_veto"]
    trace_by_row = {
        str(row["row_id"]): row["trace_hash"]
        for row in trace_payload["trace_rows"]
    }
    for index, row_id in enumerate(bundle.row_ids):
        label = int(bundle.labels[index])
        decision = int(decisions[index])
        row_hash = bundle.row_hashes[index]
        rows.append(
            {
                "prediction_row_id": sha256_json(
                    {
                        "repetition_id": unit["repetition_id"],
                        "system_id": unit["system_id"],
                        "row_hash": row_hash,
                    }
                )[:24],
                "run_id": "",
                "repetition_id": unit["repetition_id"],
                "dataset_id": unit["dataset_id"],
                "run_mode": unit["run_mode"],
                "execution_seed": unit["execution_seed"],
                "split_schedule_id": unit["split_schedule_id"],
                "initialization_schedule_id": unit["initialization_schedule_id"],
                "specialist_composition_id": unit["specialist_composition_id"],
                "system_id": unit["system_id"],
                "specialist_ids": ",".join(bundle.specialist_ids),
                "row_id": str(int(row_id)),
                "row_hash": row_hash,
                "label": label,
                "probability_score": float(probabilities[index]),
                "binary_decision": decision,
                "confidence": float(abs(probabilities[index] - 0.5) * 2.0),
                "correctness": int(decision == label),
                "f1_tp": int(decision == 1 and label == 1),
                "f1_fp": int(decision == 1 and label == 0),
                "f1_fn": int(decision == 0 and label == 1),
                "f1_tn": int(decision == 0 and label == 0),
                "rejection_acceptance": "rejected" if bool(hard_veto[index]) else "accepted",
                "trace_hash": trace_by_row.get(str(int(row_id)), ""),
                "trace_schema_hash": "",
                "system_config_hash": "",
                "specialist_output_hash": bundle.specialist_output_hash,
                "probability_matrix_hash": bundle.probability_matrix_hash,
                "label_hash": bundle.label_hash,
                "empirical_prediction_available": "true",
                "source_backend": "empirical_sklearn_repeated_training",
            }
        )
    return rows


def attach_run_id(rows: list[dict[str, Any]], run_id: str) -> list[dict[str, Any]]:
    for row in rows:
        row["run_id"] = run_id
    return rows


def _build_trace_rows(
    bundle: SpecialistOutputBundle,
    system_id: str,
    diagnostics: dict[str, np.ndarray],
    severity: np.ndarray,
    weights: np.ndarray,
    theta: np.ndarray,
    consensus: np.ndarray,
    hard_veto: np.ndarray,
    decisions: np.ndarray,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    config_hash = sha256_json({"system_id": system_id, "specialists": list(bundle.specialist_ids)})
    for index, row_id in enumerate(bundle.row_ids):
        payload = {
            "row_id": str(int(row_id)),
            "row_hash": bundle.row_hashes[index],
            "dataset_id": bundle.dataset_id,
            "run_mode": bundle.run_mode,
            "execution_seed": bundle.execution_seed,
            "split_schedule_id": bundle.split_schedule_id,
            "initialization_schedule_id": bundle.initialization_schedule_id,
            "specialist_composition_id": bundle.specialist_composition_id,
            "system_id": system_id,
            "specialist_ids": list(bundle.specialist_ids),
            "s": {
                model_id: float(bundle.probabilities[index, model_index])
                for model_index, model_id in enumerate(bundle.specialist_ids)
            },
            "r": {
                model_id: float(bundle.supports[index, model_index])
                for model_index, model_id in enumerate(bundle.specialist_ids)
            },
            "z": {
                flag_name: float(values[index])
                for flag_name, values in diagnostics.items()
            },
            "a": float(severity[index]),
            "w": {
                model_id: float(weights[index, model_index])
                for model_index, model_id in enumerate(bundle.specialist_ids)
            },
            "m": 0.0,
            "theta": float(theta[index]),
            "R": float(consensus[index]),
            "hard_veto": bool(hard_veto[index]),
            "decision": int(decisions[index]),
            "label": int(bundle.labels[index]),
            "config_hash": config_hash,
            "checkpoint_hashes": dict(bundle.checkpoint_hashes),
        }
        payload["trace_hash"] = sha256_json(payload)
        rows.append(payload)
    return rows


def _compute_diagnostics(probabilities: np.ndarray, supports: np.ndarray) -> dict[str, np.ndarray]:
    clipped = np.clip(probabilities, 1e-12, 1.0 - 1e-12)
    mean_probability = np.mean(probabilities, axis=1)
    votes = probabilities >= 0.5
    positive_vote_rate = np.mean(votes, axis=1)
    majority_vote_rate = np.maximum(positive_vote_rate, 1.0 - positive_vote_rate)
    entropy = -(clipped * np.log2(clipped) + (1.0 - clipped) * np.log2(1.0 - clipped))
    return {
        "probability_spread": np.max(probabilities, axis=1) - np.min(probabilities, axis=1),
        "support_disagreement": np.std(supports, axis=1),
        "low_mean_confidence": 1.0 - np.abs(2.0 * mean_probability - 1.0),
        "vote_disagreement": 1.0 - majority_vote_rate,
        "mean_entropy": np.mean(entropy, axis=1),
    }


def _aggregate_severity(flags: dict[str, np.ndarray], severity_config: dict[str, Any]) -> np.ndarray:
    severity = np.zeros_like(next(iter(flags.values())), dtype=np.float64)
    for flag_name, values in flags.items():
        severity += float(severity_config.get("weights", {}).get(flag_name, 0.0)) * values
    return np.maximum(severity, 0.0)


def _compute_governed_weights(
    supports: np.ndarray, severity: np.ndarray, rebalancer_config: dict[str, Any]
) -> np.ndarray:
    n_rows, n_models = supports.shape
    base = np.full((n_rows, n_models), 1.0 / n_models, dtype=np.float64)
    center = np.mean(supports, axis=1, keepdims=True)
    deviation = np.abs(supports - center)
    penalty_strength = float(rebalancer_config.get("outlier_penalty_strength", 0.0))
    adjusted = base * np.maximum(0.0, 1.0 - penalty_strength * severity.reshape(-1, 1) * deviation)
    clipped = np.clip(
        adjusted,
        float(rebalancer_config.get("min_weight", 0.0)),
        float(rebalancer_config.get("max_weight", 1.0)),
    )
    return clipped / clipped.sum(axis=1, keepdims=True)


def _binary_decisions(probabilities: np.ndarray, threshold: float) -> np.ndarray:
    return (np.asarray(probabilities, dtype=np.float64) >= threshold).astype(np.int8)


def _simplex_grid(dimensions: int, step: float) -> list[np.ndarray]:
    units = int(round(1.0 / step))
    candidates: list[np.ndarray] = []
    for values in product(range(units + 1), repeat=dimensions):
        if sum(values) != units:
            continue
        candidates.append(np.asarray(values, dtype=np.float64) / units)
    return candidates


def _hash_array(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.shape).encode("utf-8"))
    digest.update(str(contiguous.dtype).encode("utf-8"))
    digest.update(contiguous.tobytes())
    return digest.hexdigest()


def _lookup_system_config_hash(system_id: str, system_config_hashes: dict[str, str]) -> str:
    suffix = f"configs/systems/{system_id}.yaml"
    for path, digest in system_config_hashes.items():
        if path.endswith(suffix):
            return digest
    raise KeyError(f"Missing frozen system config hash for system: {system_id}")
