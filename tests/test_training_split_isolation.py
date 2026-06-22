from __future__ import annotations

from mavs_ch10c.execution.dataset_builder import build_partition_bundle


def test_training_split_isolated_from_other_partitions() -> None:
    bundle = build_partition_bundle(
        "breast_cancer_wisconsin", "locked", "locked_split_01", 31001
    )

    assert bundle.train_hash != bundle.validation_hash
    assert bundle.train_hash != bundle.calibration_hash
    assert bundle.train_hash != bundle.locked_benchmark_hash
    assert bundle.train_count == 72
    assert bundle.validation_count == 18
    assert bundle.calibration_count == 12
    assert bundle.locked_benchmark_count == 9
    assert bundle.audit_benchmark_count == 9
    assert bundle.benchmark_count == 9
