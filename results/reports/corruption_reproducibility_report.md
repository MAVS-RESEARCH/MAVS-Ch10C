# Corruption-Aware Reproducibility Report

## Scope

Phase 6 evaluates whether MAVS-GC preserves reproducibility and stability under the complete Chapter 10B corruption suite. The evidence is generated from frozen Phase 2 benchmark outputs and tied to the Phase 5 clean-condition anchor at corruption level `0.0`.

No model training, hyperparameter search, corruption-level tuning, threshold tuning, or governance-policy modification was performed in this phase.

## Imported Corruption Suite

- Suite hash: `87c98140d082c07e744e7f1374b8d8a5707ea7eea091fd84f5422426ab76c190`
- Chapter 10B grid payload hash: `2e18454a30dc9c83b9c74af3bf432b93ea6434a88205b107238447f2677f0523`
- Families: adversarial_confidence_inflation, confidence_distortion, distribution_shift, feature_noise, label_noise, missing_features, random_feature_deletion, specialist_failure, synthetic_sensor_failure
- Levels: 0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0

## Matrix Coverage

- Source run rows: 50400
- Expanded corruption run rows: 3628800
- Locked and audit evidence remain separated.
- Shadow verification is not used as final evidence.

## Research Question Answers

### RQ1. Does MAVS-GC reduce variance under corruption?

Status: `mixed`.

Pure MAVS-GC mean corrupted accuracy/F1 variance is 0.0172849; the non-Pure-MAVS comparison mean is 0.0148235.

Primary artifact: `results/reports/corruption_variance_tables.csv`.

Supporting artifacts: `results/reports/corruption_reproducibility_tables.csv; results/corruption_reproducibility/corruption_execution_manifest.json`.

### RQ2. Does MAVS-GC preserve prediction stability under corruption?

Status: `supported`.

Pure MAVS-GC mean corrupted prediction_stability is 0.971615; the non-Pure-MAVS comparison mean is 0.952713.

Primary artifact: `results/reports/corruption_stability_tables.csv`.

Supporting artifacts: `results/figures/prediction_stability_by_corruption.png`.

### RQ3. Does MAVS-GC preserve decision stability under corruption?

Status: `supported`.

Pure MAVS-GC mean corrupted decision_stability is 0.97577; the non-Pure-MAVS comparison mean is 0.958762.

Primary artifact: `results/reports/corruption_stability_tables.csv`.

Supporting artifacts: `results/figures/decision_stability_by_corruption.png`.

### RQ4. Does MAVS-GC preserve consensus stability under corruption?

Status: `supported`.

Pure MAVS-GC mean corrupted consensus_stability is 0.979332; the non-Pure-MAVS comparison mean is 0.963946.

Primary artifact: `results/reports/corruption_stability_tables.csv`.

Supporting artifacts: `results/figures/consensus_stability_by_corruption.png`.

### RQ5. Does MAVS-GC preserve trace stability under corruption?

Status: `supported`.

Pure MAVS-GC mean corrupted trace stability is 0.967976; Veto MAVS mean corrupted trace stability is 0.959693.

Primary artifact: `results/reports/corruption_trace_stability_tables.csv`.

Supporting artifacts: `results/figures/trace_stability_by_corruption.png`.

### RQ6. Which corruption families destabilize MAVS-GC most?

Status: `supported`.

The lowest mean prediction stability is observed for `specialist_failure` at 0.959872.

Primary artifact: `results/reports/corruption_reproducibility_tables.csv`.

Supporting artifacts: `results/reports/corruption_stability_tables.csv`.

### RQ7. Which corruption families destabilize baseline systems most?

Status: `supported`.

The lowest mean prediction stability is observed for `specialist_failure` at 0.927823.

Primary artifact: `results/reports/corruption_reproducibility_tables.csv`.

Supporting artifacts: `results/reports/corruption_stability_tables.csv`.

### RQ8. Does MAVS-GC maintain stability by increasing rejection?

Status: `supported`.

Pure MAVS-GC mean rejection under corruption is 0.0231708; the comparison mean is 0.00717495. Pure MAVS-GC decision stability is 0.97577; the comparison mean is 0.958762.

Primary artifact: `results/reports/corruption_reproducibility_tables.csv`.

Supporting artifacts: `results/reports/corruption_stability_tables.csv`.

### RQ9. Does specialist failure significantly affect reproducibility?

Status: `supported`.

Specialist-failure mean prediction stability is 0.9385; all other corruption families average 0.958743.

Primary artifact: `results/reports/corruption_reproducibility_tables.csv`.

Supporting artifacts: `results/reports/corruption_stability_tables.csv`.

### RQ10. Are governance-induced stability effects stronger under corruption than under clean conditions?

Status: `supported`.

Pure MAVS-GC decision-stability delta versus comparison systems is -0.00684573 at level 0.0 and 0.0170086 for levels greater than 0.0.

Primary artifact: `results/reports/corruption_stability_tables.csv`.

Supporting artifacts: `results/reports/corruption_reproducibility_tables.csv`.

## Interpretation Rules Applied

- Family-specific destabilization is reported descriptively, not as a universal claim.
- Governance contributes to reproducibility under stress.
- MAVS-GC primarily functions as a governance architecture under adverse conditions rather than as a clean-condition reproducibility optimizer.
- Specialist failure is a material reproducibility stressor.
- Stability is achieved through a caution tradeoff.

## Limitations

- Phase 6 applies the imported Chapter 10B corruption definitions to frozen Phase 2 benchmark outputs through deterministic corruption-aware projections, rather than rerunning a new hyperparameter or governance search.
- Level `0.0` is a clean anchor and is not interpreted as a stress condition.
- Positive, neutral, and mixed findings are preserved in the claim support ledger.

## Artifact References

- Execution manifest: `results/corruption_reproducibility/corruption_execution_manifest.json`
- Metric manifest: `results/corruption_reproducibility/corruption_metric_manifest.json`
- Reproducibility table: `results/reports/corruption_reproducibility_tables.csv`
- Variance table: `results/reports/corruption_variance_tables.csv`
- Stability table: `results/reports/corruption_stability_tables.csv`
- Trace stability table: `results/reports/corruption_trace_stability_tables.csv`
- Claim support ledger: `results/reports/corruption_claim_support_ledger.csv`
