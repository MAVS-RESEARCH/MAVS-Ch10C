from __future__ import annotations

from mavs_ch10c.execution.dataset_builder import build_partition_bundle


def test_calibration_split_isolated_from_training_and_benchmark() -> None:
    bundle = build_partition_bundle("adult_income", "locked", "locked_split_02", 31002)

    assert bundle.calibration_hash != bundle.train_hash
    assert bundle.calibration_hash != bundle.validation_hash
    assert bundle.calibration_hash != bundle.locked_benchmark_hash
    assert bundle.calibration_hash != bundle.audit_benchmark_hash
