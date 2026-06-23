# MAVS Chapter 10C Reproducibility Report

## Source Authority
This report is generated from the Phase 1-4 artifacts declared in `configs/reports/reproducibility_report.yaml`. The primary local source context is `C:\Users\Saif malik\Downloads\Mavs.pdf`; the implementation contract is `WorkPlan.md`; and the implementation audit log is `Path.md`.

## Methodology
The report consumes frozen Phase 4 metric artifacts only. It does not train models, tune hyperparameters, modify governance policy, or use training, validation, or calibration diagnostics as final evidence.

## Imported Chapter 10A and 10B Foundation
Chapter 10A commit `3f8ce15dac24eaefcd1379279c30f1ded5be9a0b` supplies datasets, model families, system semantics, and frozen governance hashes. Chapter 10B commit `6411af5b029de4216a5506beabd3ddf7182df4d9` supplies artifact hashing and verification patterns. Both imports are referenced through `results/foundation_import/foundation_import_manifest.json`.

## Frozen Governance Policy
Pure MAVS-GC and Veto MAVS are treated as governance systems. Governance trace stability is evaluated only from trace fields already emitted by the frozen Phase 2 execution corpus and aligned in the Phase 3 variance rows.

## Repeated Execution Matrix
Locked evidence covers 324000 variance rows; audit evidence covers 129600 variance rows. The locked corpus contains 5400 model fits; the audit corpus contains 2160 model fits.

## Independent Benchmark Design
The locked and audit benchmark partitions are disjoint from train, validation, and calibration partitions. Audit seeds and schedules are independent from locked seeds and schedules. The report identifies locked and audit results separately in every generated table.

## Anti-Overfitting Controls
Metric definitions were frozen before report generation. The Phase 4 metric manifest records `training_performed=false`, `metric_definitions_selected_from_audit=false`, and `metrics_read_only_frozen_variance_datasets=true`. Positive, negative, and mixed outcomes are preserved in `results/reports/reproducibility_system_deltas.csv`.

## Results
- Variance: Pure MAVS-GC is lower in 86 of 256 paired variance comparisons.
- Prediction stability: Pure MAVS-GC is higher in 44 of 128 paired comparisons.
- Decision stability: Pure MAVS-GC is higher in 44 of 128 paired comparisons.
- Governance traces: Pure MAVS-GC trace similarity is higher than Veto MAVS in 17 of 320 trace-field comparisons.
- Confidence intervals: Pure MAVS-GC is narrower in 86 of 256 interval-width comparisons.
- Correctness deltas: 26 higher, 11 neutral, 91 lower.

## Claim Register
| Claim ID | Claim | Classification | Evidence |
| --- | --- | --- | --- |
| C1 | Pure MAVS-GC shows lower variance in 86/256 paired comparisons. | mixed_negative | `results/reports/variance_tables.csv`; `results/figures/accuracy_variance_by_system.png`; `results/figures/f1_variance_by_system.png` |
| C2 | Pure MAVS-GC shows higher prediction stability in 44/128 comparisons. | mixed_negative | `results/reports/stability_tables.csv`; `results/figures/prediction_stability_by_system.png` |
| C3 | Pure MAVS-GC shows higher final decision stability in 44/128 comparisons. | mixed_negative | `results/reports/stability_tables.csv`; `results/figures/decision_stability_by_system.png` |
| C4 | Pure MAVS-GC trace similarity is higher than Veto MAVS in 17/320 governance trace comparisons. | mixed_negative | `results/reports/stability_tables.csv`; `results/figures/trace_stability_by_system.png` |
| C5 | Pure MAVS-GC has narrower confidence intervals in 86/256 comparisons. | mixed_negative | `results/reports/variance_tables.csv`; `results/figures/confidence_interval_widths.png` |
| C6 | Correctness deltas are mixed: 26 higher, 11 neutral, 91 lower. | mixed_tradeoff | `results/reports/reproducibility_system_deltas.csv` |
| C7 | Locked and audit evidence use matching metric families, systems, and baselines. | supported_artifact_scope | `results/stability_metrics/reproducibility_metric_manifest.json`; `results/reports/reproducibility_artifact_manifest.json` |

## Limitations
The evidence is bounded to the four configured datasets, the five configured systems, the declared seed/split/init/composition matrix, and the empirical working-frame caps recorded in Phase 2 manifests. Chapter 10C evidence here does not evaluate corruption stress. Wider intervals, lower stability, and negative correctness deltas remain part of the final evidence.

## Final Answer to Chapter 10C
The Phase 5 evidence does not support an unconditional reproducibility advantage for Pure MAVS-GC. The supported conclusion is mixed and artifact-scoped: some variance and stability comparisons improve, while other comparisons are neutral or worse and must remain part of the final record.
