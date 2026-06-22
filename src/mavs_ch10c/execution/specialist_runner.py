"""Shared empirical specialist outputs for Phase 2 systems."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from mavs_ch10c import console
from mavs_ch10c.execution.dataset_builder import PartitionBundle
from mavs_ch10c.execution.repeated_training import FittedSpecialist
from mavs_ch10c.verification.hash_utils import sha256_json


@dataclass(frozen=True)
class SpecialistOutputBundle:
    bundle_id: str
    dataset_id: str
    run_mode: str
    execution_seed: int
    split_schedule_id: str
    initialization_schedule_id: str
    specialist_composition_id: str
    specialist_ids: tuple[str, ...]
    row_ids: np.ndarray
    row_hashes: tuple[str, ...]
    labels: np.ndarray
    probabilities: np.ndarray
    supports: np.ndarray
    validation_probabilities: np.ndarray
    validation_labels: np.ndarray
    benchmark_partition_hash: str
    fit_record_hash: str
    specialist_output_hash: str
    probability_matrix_hash: str
    label_hash: str
    checkpoint_hashes: dict[str, str]


def build_specialist_output_bundle(
    run_mode: str,
    execution_seed: int,
    initialization_schedule_id: str,
    specialist_composition_id: str,
    partition_bundle: PartitionBundle,
    fitted_specialists: list[FittedSpecialist],
) -> SpecialistOutputBundle:
    """Build the identical specialist-output bundle consumed by all five systems."""

    # console.log: phase2 empirical specialist output bundle build begins.
    console.log(
        "phase2.specialist_runner.bundle.start "
        f"dataset={partition_bundle.dataset_id} composition={specialist_composition_id}"
    )
    benchmark = partition_bundle.benchmark
    specialist_ids = tuple(fit.record.specialist_id for fit in fitted_specialists)
    probabilities = np.column_stack(
        [fit.benchmark_probabilities for fit in fitted_specialists]
    )
    supports = np.column_stack([fit.benchmark_supports for fit in fitted_specialists])
    validation_probabilities = np.column_stack(
        [fit.validation_probabilities for fit in fitted_specialists]
    )
    fit_record_hash = sha256_json([fit.record.__dict__ for fit in fitted_specialists])
    probability_matrix_hash = _hash_array(probabilities)
    payload = {
        "dataset_id": partition_bundle.dataset_id,
        "run_mode": run_mode,
        "execution_seed": execution_seed,
        "split_schedule_id": partition_bundle.split_schedule_id,
        "initialization_schedule_id": initialization_schedule_id,
        "specialist_composition_id": specialist_composition_id,
        "specialist_ids": list(specialist_ids),
        "benchmark_partition_hash": benchmark.row_hash,
        "fit_record_hash": fit_record_hash,
        "probability_matrix_hash": probability_matrix_hash,
    }
    bundle = SpecialistOutputBundle(
        bundle_id=sha256_json(payload)[:24],
        dataset_id=partition_bundle.dataset_id,
        run_mode=run_mode,
        execution_seed=int(execution_seed),
        split_schedule_id=partition_bundle.split_schedule_id,
        initialization_schedule_id=initialization_schedule_id,
        specialist_composition_id=specialist_composition_id,
        specialist_ids=specialist_ids,
        row_ids=benchmark.row_ids,
        row_hashes=benchmark.row_hashes,
        labels=benchmark.y,
        probabilities=probabilities,
        supports=supports,
        validation_probabilities=validation_probabilities,
        validation_labels=partition_bundle.splits["validation"].y,
        benchmark_partition_hash=benchmark.row_hash,
        fit_record_hash=fit_record_hash,
        specialist_output_hash=sha256_json(payload),
        probability_matrix_hash=probability_matrix_hash,
        label_hash=benchmark.label_hash,
        checkpoint_hashes={
            fit.record.specialist_id: fit.record.checkpoint_hash
            for fit in fitted_specialists
        },
    )
    # console.log: phase2 empirical specialist output bundle build completed.
    console.log(
        "phase2.specialist_runner.bundle.complete "
        f"bundle={bundle.bundle_id} rows={len(bundle.labels)} specialists={len(bundle.specialist_ids)}"
    )
    return bundle


def _hash_array(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.shape).encode("utf-8"))
    digest.update(str(contiguous.dtype).encode("utf-8"))
    digest.update(contiguous.tobytes())
    return digest.hexdigest()
