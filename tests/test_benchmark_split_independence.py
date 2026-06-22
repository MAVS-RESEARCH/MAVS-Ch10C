from __future__ import annotations

from mavs_ch10c.execution.dataset_builder import build_partition_bundle


def test_locked_and_audit_benchmark_hashes_are_independent() -> None:
    locked = build_partition_bundle(
        "credit_card_fraud", "locked", "locked_split_03", 31003
    )
    audit = build_partition_bundle("credit_card_fraud", "audit", "audit_split_01", 32001)

    assert locked.locked_benchmark_hash is not None
    assert audit.audit_benchmark_hash is not None
    assert locked.locked_benchmark_hash != audit.audit_benchmark_hash
    assert audit.audit_benchmark_hash != audit.train_hash
    assert audit.audit_benchmark_hash != audit.validation_hash
    assert audit.audit_benchmark_hash != audit.calibration_hash
