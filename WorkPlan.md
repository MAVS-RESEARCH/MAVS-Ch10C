# MAVS Chapter 10C WorkPlan

## Source Authority

This workplan is grounded in the source documents supplied by the user and in a local structural inspection of the completed Chapter 10A and 10B repositories.

1. `MAVS Chapter 10C-Doc.pdf`
   - Controlling document for this repository.
   - Defines Chapter 10C as the reproducibility benchmark program.
   - Requires reusing the validated Chapter 10A datasets, governance implementation, comparison systems, and benchmark foundation.
   - Requires reusing or extending the Chapter 10B artifact hashing, run manifest, environment capture, seed registry, and verification infrastructure.
   - Forbids algorithmic modifications to MAVS-GC during Chapter 10C.
   - Requires repeated execution over 20-50 seeds, multiple train/test splits, multiple specialist initialization schedules, and multiple specialist compositions.
2. `Mavs Research Bible - Chapter 10.pdf`
   - Defines Chapter 10 as the real benchmark program for MAVS.
   - Requires the same five comparison systems across Chapters 10A, 10B, and 10C.
   - Defines Chapter 10C as the reproducibility program and requires variance, stability, confidence interval width, and run-to-run agreement metrics.
   - Adds the evidence standard: results must be reproducible, statistically supported, observed across multiple datasets, observed against multiple baselines, and documented through traces and reports.
3. `Mavs.pdf`
   - Defines MAVS as a governance-first architecture.
   - Requires all specialists to speak, governed consensus, diagnostics/red flags, severity aggregation, contextual weights, optional mitigation, governed thresholds, hard veto behavior, and deterministic explanation traces.
4. `MAVS Research Bible - Chapter 10A Completion Report.pdf`
   - Confirms Chapter 10A is complete.
   - Establishes the validated dataset corpus, specialist families, comparison systems, benchmark splits, manifests, artifact hashing, governance traces, and accuracy evidence.
   - Confirms Chapter 10A did not support universal predictive-correctness superiority and therefore Chapter 10C must avoid accuracy-superiority assumptions.
5. `MAVS Research Bible - Chapter 10B Completion Report Final.pdf`, `MAVS_Chapter10B_Corrected_Final_Numbers_Report.pdf`, and `Robustness Highlights Chapter 10B.pdf`
   - Confirm Chapter 10B is complete and verified.
   - Establish the verified import, hashing, artifact inventory, trace-schema, stress-run manifest, and release verification patterns to reuse in Chapter 10C.
   - Confirm the current MAVS evidence identity: governance is strongest as failure-management, robustness, and safety-oriented behavior, not universal accuracy maximization.

If documents differ in detail, this plan uses the stricter or more complete requirement unless it would move Chapter 10C into later research chapters. Chapter 10C must answer the reproducibility question; positive, negative, and mixed outcomes are all acceptable.

## Mission

Chapter 10C answers one research question:

**Does MAVS-GC reduce experimental variance relative to traditional aggregation systems?**

The objective is not to improve MAVS-GC, tune governance, redesign specialists, or obtain state-of-the-art scores. The objective is to measure whether frozen governance produces lower run-to-run variance, higher prediction stability, higher decision stability, higher consensus stability, higher trace stability, narrower confidence intervals, and stronger run-to-run agreement than aggregation-only systems under repeated execution.

## Scope Boundary

In scope:

- Importing the completed Chapter 10A benchmark corpus:
  - Breast Cancer Wisconsin
  - Adult Income
  - Credit Card Fraud
  - Bank Marketing
- Reusing the Chapter 10A specialist families:
  - Random Forest
  - Gradient Boosted Trees
  - MLP
- Reusing the Chapter 10A comparison systems:
  - Single Model
  - Mean Ensemble
  - Static Weighted Ensemble
  - Veto MAVS
  - Pure MAVS-GC
- Reusing the Chapter 10A MAVS-GC governance implementation without algorithmic modification.
- Reusing and extending Chapter 10B verification concepts:
  - artifact hashing
  - run manifests
  - environment capture
  - seed registry
  - artifact inventory
  - release verification
- Repeated execution under:
  - 20-50 execution seeds
  - multiple train/test split schedules
  - multiple specialist initialization schedules
  - multiple specialist compositions
- Required Chapter 10C metrics:
  - Accuracy Variance
  - F1 Variance
  - Prediction Stability
  - Decision Stability
  - Consensus Stability
  - Trace Stability
  - Run-to-Run Agreement
  - Confidence Interval Width
- Required outputs:
  - large reproducibility corpus
  - variance benchmark dataset
  - reproducibility measurements
  - variance tables
  - stability figures
  - reproducibility report
  - artifact manifest
  - verification report

Out of scope:

- Algorithmic changes to MAVS-GC.
- Governance threshold tuning from Chapter 10C outcomes.
- Model architecture invention beyond the Chapter 10A specialist families.
- Corruption studies from Chapter 10B, except where import verification relies on Chapter 10B infrastructure.
- General intelligence, universal superiority, cross-domain validity, governance learning, self-governance, scientific discovery, or publication-level generalization claims.

## Frozen Governance Policy

Chapter 10C exists to measure reproducibility, not redesign governance.

Allowed changes:

- Adapter code around imported Chapter 10A systems.
- Repeated-training orchestration.
- Reproducibility run manifests.
- Stability and variance metrics.
- Trace comparison code.
- Reporting and verification code.

Forbidden changes:

- Changing Pure MAVS-GC decision equations.
- Changing Veto MAVS veto semantics.
- Changing governance thresholds, severity aggregation, mitigation, rebalancer behavior, or hard-veto logic after import.
- Changing baseline system semantics.
- Selecting new hyperparameters or governance coefficients from Chapter 10C results.

The implementation must store source hashes for imported Chapter 10A governance files and must fail final verification if those hashes drift without an explicit recorded upstream import update.

## Repository Contract

This repository will be a reproducible Python benchmark package. It should follow the Chapter 10A and 10B style: explicit configs, small scripts, typed source modules, tests for every invariant, generated artifacts under `results/`, and a complete implementation trail in `Path.md`.

Planned top-level structure:

```text
configs/
  ch10a_import/
  ch10b_import/
  reproducibility/
  experiments/
  reports/
external/
  ch10a/
  ch10b/
src/
  mavs_ch10c/
    adapters/
    repeatability/
    execution/
    comparison/
    evaluation/
    reporting/
    verification/
    cli.py
tests/
results/
  foundation_import/
  run_manifests/
  execution_corpus/
  variance_benchmarks/
  stability_metrics/
  figures/
  reports/
scripts/
WorkPlan.md
Path.md
```

Heavy generated artifacts should be ignored by git unless a later publication decision explicitly tracks them. Final reports, tables, figures, manifests, artifact inventories, and verification reports should be tracked when small enough.

## Default Reproducibility Matrix

The final matrix must satisfy the Chapter 10C requirement of 20-50 seeds per dataset while preserving independent audit evidence.

Default locked matrix:

```text
datasets: 4
systems: 5
execution_seeds: 30
split_schedules: 5
initialization_schedules: 3
specialist_compositions: 4
```

Minimum locked system-level evaluation cells:

```text
4 datasets * 5 systems * 30 seeds * 5 splits * 3 init schedules * 4 compositions = 36000
```

Default audit matrix:

```text
datasets: 4
systems: 5
execution_seeds: 20
split_schedules: 3
initialization_schedules: 3
specialist_compositions: 4
```

Minimum audit system-level evaluation cells:

```text
4 datasets * 5 systems * 20 seeds * 3 splits * 3 init schedules * 4 compositions = 14400
```

Default specialist compositions:

```text
full_rf_gbt_mlp
rf_gbt_pair
rf_mlp_pair
gbt_mlp_pair
```

For `single_model`, the available specialist is chosen from the active composition using predeclared validation rules only. For ensemble and governance systems, the active composition defines which specialists are allowed to speak. All active specialists must speak for every evaluated input.

If compute limits force a reduced matrix, the reduced final matrix must still include at least 20 seeds per dataset, at least 2 split schedules, at least 2 initialization schedules, and at least 2 specialist compositions. Any reduction must be recorded in `Path.md` before final execution and must be disclosed in the final report.

## Phase 1 - Repeatability Foundation and Import Controller

### Scope

Build the Chapter 10C foundation without reimplementing Chapter 10A or 10B from scratch.

This phase imports and verifies:

- Chapter 10A dataset manifests.
- Chapter 10A preprocessing and split protocols.
- Chapter 10A specialist configs.
- Chapter 10A governance implementation.
- Chapter 10A comparison system semantics.
- Chapter 10B artifact hashing, inventory, run manifest, environment capture, and verification patterns.

New deliverable:

- Reproducibility execution controller.

### Files and Directories to Create

```text
pyproject.toml
README.md
.gitignore
configs/ch10a_import/source.yaml
configs/ch10b_import/source.yaml
configs/reproducibility/seed_registry.yaml
configs/reproducibility/split_schedules.yaml
configs/reproducibility/init_schedules.yaml
configs/reproducibility/specialist_compositions.yaml
configs/reproducibility/repetition_grid.yaml
configs/experiments/ch10c_reproducibility.yaml
external/ch10a/.gitkeep
external/ch10b/.gitkeep
src/mavs_ch10c/__init__.py
src/mavs_ch10c/cli.py
src/mavs_ch10c/adapters/ch10a_source.py
src/mavs_ch10c/adapters/ch10a_artifacts.py
src/mavs_ch10c/adapters/ch10a_systems.py
src/mavs_ch10c/adapters/ch10b_verification.py
src/mavs_ch10c/repeatability/seed_registry.py
src/mavs_ch10c/repeatability/split_schedule.py
src/mavs_ch10c/repeatability/init_schedule.py
src/mavs_ch10c/repeatability/composition.py
src/mavs_ch10c/repeatability/repetition_grid.py
src/mavs_ch10c/execution/environment.py
src/mavs_ch10c/execution/run_manifest.py
src/mavs_ch10c/execution/controller.py
src/mavs_ch10c/verification/hash_utils.py
scripts/import_foundation.py
scripts/build_repetition_grid.py
results/foundation_import/.gitkeep
results/run_manifests/.gitkeep
tests/test_ch10a_import_contract.py
tests/test_ch10b_verification_contract.py
tests/test_frozen_governance_hashes.py
tests/test_seed_registry_complete.py
tests/test_repetition_grid_complete.py
tests/test_no_algorithmic_governance_modification.py
```

### Code to Produce

- A Chapter 10A source locator that can use a configured local path, an absolute path, or an artifact bundle.
- A Chapter 10B source locator for verification utilities and release-gate patterns.
- Import validators for:
  - required dataset ids
  - required specialist family ids
  - required comparison system ids
  - dataset manifests
  - preprocessing metadata
  - split-generation protocol
  - governance source hashes
  - system config hashes
  - trace schema compatibility
- A seed registry with disjoint seed namespaces:
  - locked execution seeds
  - audit execution seeds
  - shadow verification seeds
  - split seeds
  - initialization seeds
- A repetition-grid builder that expands dataset, execution seed, split schedule, initialization schedule, specialist composition, and run mode.
- An environment capture module that records:
  - operating system
  - Python version
  - dependency versions
  - git commit
  - command line
  - import source commit hashes
  - relevant environment variables
- A run manifest writer that records every execution unit before results are produced.

### Coding Approach

- Use import adapters rather than copying Chapter 10A or 10B source directly.
- Treat imported Chapter 10A governance code as immutable.
- Keep Chapter 10C orchestration separate from Chapter 10A system internals.
- Make every repeatability dimension explicit in config.
- Fail closed if an imported artifact, config, or source hash is missing or changed.

### Model Handling

No final reproducibility model training occurs in this phase. This phase only imports the validated model family definitions, dataset protocols, and system semantics that later phases will rerun under repeated conditions.

### Anti-Overfitting Controls

- The seed registry, split schedules, initialization schedules, specialist compositions, and metric definitions must be frozen before any full repeated corpus is generated.
- Locked seeds and audit seeds must be disjoint.
- Shadow verification seeds must not influence implementation choices except to expose reproducibility defects.
- Governance source hashes must be stored before Phase 2.
- If a required Chapter 10A or 10B artifact is unavailable, stop and record the blocker in `Path.md`; do not silently replace it.

### Phase 1 Acceptance Criteria

- Chapter 10A and Chapter 10B sources or artifact bundles are located.
- Required Chapter 10A datasets, systems, specialist definitions, and governance source hashes are validated.
- Required Chapter 10B hashing and verification patterns are available or locally reimplemented with equivalent tests.
- Seed registry and repetition grid are generated.
- No training command is executed.
- Tests pass for import contracts, seed completeness, frozen governance hashes, and repetition-grid completeness.
- `Path.md` records imported source paths, commits, hashes, commands, tests, blockers, and whether this phase followed the workplan.

## Phase 2 - Repeated Execution Corpus

### Scope

Generate the large reproducibility corpus required by Chapter 10C.

For every dataset:

- Run 20-50 seeds.
- Run multiple train/test splits.
- Run multiple specialist initialization schedules.
- Run multiple specialist compositions.
- Record all runs.
- Do not tune.

This phase intentionally retrains specialists under predeclared repeated conditions to measure variance. This is not model development and does not permit hyperparameter search or governance adjustment.

### Files and Directories to Create

```text
configs/experiments/locked_repetition_corpus.yaml
configs/experiments/audit_repetition_corpus.yaml
src/mavs_ch10c/execution/dataset_builder.py
src/mavs_ch10c/execution/repeated_training.py
src/mavs_ch10c/execution/specialist_runner.py
src/mavs_ch10c/execution/system_runner.py
src/mavs_ch10c/execution/corpus_writer.py
src/mavs_ch10c/execution/cache.py
scripts/run_locked_repetition_corpus.py
scripts/run_audit_repetition_corpus.py
results/execution_corpus/.gitkeep
results/execution_corpus/locked/.gitkeep
results/execution_corpus/audit/.gitkeep
tests/test_training_split_isolation.py
tests/test_calibration_split_isolation.py
tests/test_benchmark_split_independence.py
tests/test_audit_seed_independence.py
tests/test_no_tuning_guard.py
tests/test_corpus_manifest_schema.py
tests/test_all_runs_recorded.py
```

### Code to Produce

- A repeated dataset builder that creates or imports train, validation, calibration, locked test, and audit test partitions from the Chapter 10A dataset protocol for each split schedule.
- A repeated specialist trainer that uses frozen Chapter 10A model configs and varies only:
  - random seed
  - train/test split schedule
  - initialization schedule
  - active specialist composition
- A corpus runner that executes all five comparison systems on identical specialist outputs for each repetition unit.
- A corpus writer that stores:
  - predictions
  - probabilities
  - system decisions
  - labels
  - specialist metadata
  - governance traces
  - run manifests
  - artifact hashes
- A cache that permits resumable execution without changing completed artifact hashes.

### Model Specifics

Random Forest:

- Use the frozen Chapter 10A Random Forest config.
- Vary only the declared random seed and split schedule.
- Record number of trees, max depth, class weighting, feature count, training row count, checkpoint hash, and probability-output hash.
- No hyperparameter grid search is allowed.

Gradient Boosted Trees:

- Use the frozen Chapter 10A Gradient Boosted Trees config.
- Vary only the declared random seed and split schedule.
- Record learning-rate, estimator count, depth/leaves settings, training row count, checkpoint hash, and probability-output hash.
- No hyperparameter grid search is allowed.

MLP:

- Use the frozen Chapter 10A MLP config.
- Vary only the declared random seed, initialization schedule, and split schedule.
- Use training and validation partitions only for convergence/early-stopping rules already defined in Chapter 10A configs.
- Record convergence status, epoch count, loss curve hash, checkpoint hash, and probability-output hash.
- No architecture search is allowed.

Calibration:

- Use the Chapter 10A calibration method.
- Fit calibration only on the calibration partition for that repetition unit.
- Record calibration split hash and calibration object hash.

### Benchmarks Produced in This Phase

Training diagnostics:

- train and validation accuracy
- train and validation F1
- calibration error before and after calibration
- convergence metadata

Final evidence inputs:

- locked benchmark predictions and traces
- audit benchmark predictions and traces
- run manifests
- corpus indexes

Training diagnostics are never final Chapter 10C evidence. Final reproducibility evidence must come only from locked and audit benchmark partitions.

### Brutal Independent Benchmark Requirement

Every trained model must be evaluated on benchmark data entirely different from the data used to train, validate, calibrate, or select it:

- Training rows are used only for fitting specialists.
- Validation rows are used only for allowed predeclared training diagnostics or early stopping.
- Calibration rows are used only for probability calibration.
- Locked benchmark rows are disjoint from train, validation, and calibration rows.
- Audit benchmark rows are disjoint from train, validation, calibration, and locked benchmark rows.
- Audit execution seeds, split schedules, and initialization schedules are independent from locked schedules.
- No final claim may use train, validation, or calibration metrics.

### Anti-Overfitting Controls

- The runner must refuse final mode if seed registries, model configs, governance configs, or system configs are uncommitted or hash-mismatched.
- The runner must store a frozen run manifest before executing each unit.
- The runner must fail if benchmark row hashes appear in train, validation, or calibration partitions.
- If code or configs change after locked results are inspected, all affected locked and audit outputs must be invalidated or marked exploratory.
- The audit corpus must not be run until the locked corpus pipeline, metric code, and report templates are frozen.

### Phase 2 Acceptance Criteria

- Locked repeated execution corpus exists for all required datasets, systems, seeds, split schedules, initialization schedules, and specialist compositions.
- Audit repeated execution corpus exists with independent seeds and split schedules.
- Every run has a manifest and artifact hashes.
- Every system receives identical specialist outputs for the same repetition unit.
- Governance systems emit complete traces.
- Training, calibration, locked benchmark, and audit benchmark isolation tests pass.
- `Path.md` records commands, run ids, model fit counts, corpus row counts, output paths, hashes, failed/retried runs, and workplan compliance.

## Phase 3 - Governance Comparison and Variance Benchmark Dataset

### Scope

Build the variance benchmark dataset comparing the five required systems under identical repetition schedules:

- Single Model
- Mean Ensemble
- Static Weighted Ensemble
- Veto MAVS
- Pure MAVS-GC

This phase transforms the raw repeated execution corpus into aligned comparison tables that isolate governance effects from schedule differences.

### Files and Directories to Create

```text
src/mavs_ch10c/comparison/__init__.py
src/mavs_ch10c/comparison/alignment.py
src/mavs_ch10c/comparison/system_outputs.py
src/mavs_ch10c/comparison/variance_dataset.py
src/mavs_ch10c/comparison/baseline_deltas.py
scripts/build_variance_benchmark_dataset.py
results/variance_benchmarks/.gitkeep
results/variance_benchmarks/locked_variance_rows.csv
results/variance_benchmarks/audit_variance_rows.csv
results/variance_benchmarks/system_delta_rows.csv
results/variance_benchmarks/variance_dataset_manifest.json
tests/test_system_schedule_alignment.py
tests/test_identical_inputs_across_systems.py
tests/test_variance_dataset_complete.py
tests/test_static_weights_train_side_only.py
tests/test_governance_trace_alignment.py
```

### Code to Produce

- Alignment logic that joins system outputs by:
  - dataset id
  - run mode
  - execution seed
  - split schedule
  - initialization schedule
  - specialist composition
  - row id
  - label hash
- A system-output normalizer that maps each system to common fields:
  - probability or score
  - binary decision
  - confidence
  - correctness
  - F1 components
  - rejection/acceptance indicator
  - trace hash where available
- A variance dataset builder that emits one row per aligned system decision.
- Delta builders comparing Pure MAVS-GC against:
  - Single Model
  - Mean Ensemble
  - Static Weighted Ensemble
  - Veto MAVS
- Manifest generation with input corpus hashes, output hashes, row counts, and schedule coverage.

### Model Handling

No new models are trained in this phase. The phase consumes Phase 2 outputs only.

### Benchmarks Produced in This Phase

- Locked variance benchmark rows.
- Audit variance benchmark rows.
- System delta rows.
- Coverage tables proving every system was evaluated under the same repetition schedules.

### Anti-Overfitting Controls

- Phase 3 cannot modify model checkpoints, system configs, governance configs, or corpus outputs.
- If an alignment defect is found, the affected corpus units must be fixed or excluded with a recorded reason; missing rows must not be silently imputed.
- The audit variance dataset must remain separately labeled from locked results.
- Any exploratory rerun must remain excluded from final variance tables unless the entire frozen matrix is rerun.

### Phase 3 Acceptance Criteria

- Variance benchmark datasets exist for locked and audit modes.
- Every required dataset/system/repetition/composition combination is represented or explicitly documented as missing with a blocker.
- Input identity across systems is proven by tests and hashes.
- Pure MAVS-GC delta rows exist against all four comparison systems.
- `Path.md` records build commands, row counts, coverage checks, hashes, missing units, and compliance.

## Phase 4 - Stability Evaluation and Reproducibility Metrics

### Scope

Compute the Chapter 10C reproducibility measurements:

- Accuracy Variance
- F1 Variance
- Prediction Stability
- Decision Stability
- Consensus Stability
- Trace Stability
- Run-to-Run Agreement
- Confidence Interval Width

### Files and Directories to Create

```text
src/mavs_ch10c/evaluation/__init__.py
src/mavs_ch10c/evaluation/variance.py
src/mavs_ch10c/evaluation/stability.py
src/mavs_ch10c/evaluation/agreement.py
src/mavs_ch10c/evaluation/confidence_intervals.py
src/mavs_ch10c/evaluation/trace_stability.py
src/mavs_ch10c/evaluation/aggregation.py
scripts/build_reproducibility_metrics.py
scripts/build_stability_tables.py
results/stability_metrics/.gitkeep
results/stability_metrics/locked_metric_rows.csv
results/stability_metrics/audit_metric_rows.csv
results/stability_metrics/accuracy_variance.csv
results/stability_metrics/f1_variance.csv
results/stability_metrics/prediction_stability.csv
results/stability_metrics/decision_stability.csv
results/stability_metrics/consensus_stability.csv
results/stability_metrics/trace_stability.csv
results/stability_metrics/run_to_run_agreement.csv
results/stability_metrics/confidence_interval_widths.csv
results/stability_metrics/reproducibility_metric_manifest.json
tests/test_accuracy_variance_definition.py
tests/test_f1_variance_definition.py
tests/test_prediction_stability_definition.py
tests/test_decision_stability_definition.py
tests/test_consensus_stability_definition.py
tests/test_trace_stability_definition.py
tests/test_run_to_run_agreement_definition.py
tests/test_confidence_interval_width_definition.py
tests/test_metric_inputs_are_frozen.py
```

### Code to Produce

- Metric computation over aligned repeated runs.
- Aggregation by dataset, system, split schedule, initialization schedule, specialist composition, and run mode.
- Paired comparisons between Pure MAVS-GC and each baseline.
- Locked-vs-audit consistency checks.
- Confidence interval width estimation using predeclared bootstrap or analytical intervals.
- Trace field comparison for governance systems.

### Metric Definitions

Accuracy Variance:

- Sample variance and standard deviation of accuracy across repeated execution units for each dataset, system, and composition.
- Report locked and audit separately.

F1 Variance:

- Sample variance and standard deviation of binary F1 across repeated execution units.
- Undefined edge cases must be handled with a predeclared zero-division policy and recorded.

Prediction Stability:

- Row-aligned stability across repeated predictions.
- Primary binary definition: mean pairwise agreement of predicted labels for the same row id across runs where row alignment is valid.
- Secondary probability definition: one minus normalized mean absolute probability difference.

Decision Stability:

- Mean pairwise agreement of final accept/reject decisions for the same row id across repeated runs.
- For MAVS-GC and Veto MAVS, this is the governed final decision.

Consensus Stability:

- For Pure MAVS-GC, compute variance and pairwise stability of governed consensus `R` across repeated runs.
- For Veto MAVS, compute analogous governed decision-score stability where available.
- For aggregation-only baselines, record score/probability stability separately and mark MAVS-specific consensus fields as not applicable.

Trace Stability:

- For governance systems, compare trace fields:
  - `s`
  - `r`
  - `z`
  - `a`
  - `w`
  - `m`
  - `theta`
  - `R`
  - `hard_veto`
  - `decision`
- Report field-level variance, exact trace-hash repeat rates, and normalized trace-distance summaries.

Run-to-Run Agreement:

- Compute pairwise agreement and kappa-style agreement where label distributions permit.
- Report agreement for decisions and correctness outcomes.

Confidence Interval Width:

- Compute interval widths for accuracy and F1 per dataset/system/composition/run mode.
- Report whether MAVS-GC intervals are narrower, wider, or indistinguishable from baselines.

### Model Handling

No models are trained in this phase. The phase consumes frozen Phase 3 variance datasets.

### Anti-Overfitting Controls

- Metric code must be finalized and tested before final audit metrics are generated.
- Metrics must read only frozen variance benchmark datasets.
- The audit mode must not be used to select metric definitions.
- Confidence interval method and bootstrap seed must be predeclared.
- Negative, neutral, and mixed results must be preserved.

### Phase 4 Acceptance Criteria

- Every required Chapter 10C metric exists for locked and audit modes.
- Metric rows cover all required datasets, systems, and compositions.
- Pure MAVS-GC is compared against Single Model, Mean Ensemble, Static Weighted Ensemble, and Veto MAVS.
- Trace stability exists for governance systems.
- Tests pass for every metric definition and frozen-input guard.
- `Path.md` records metric commands, row counts, hash summaries, test outputs, metric definition choices, limitations, and compliance.

## Phase 5 - Analysis, Variance Tables, Stability Figures, and Reproducibility Report

### Scope

Analyze whether MAVS-GC measurably reduces experimental variance and increases reproducibility.

Determine:

- Whether MAVS reduces variance.
- Whether MAVS stabilizes decisions.
- Whether MAVS stabilizes governance traces.
- Whether MAVS increases reproducibility.

Generate:

- Reproducibility Report.
- Variance Tables.
- Stability Figures.
- Reproducibility Artifact Manifest.

### Files and Directories to Create

```text
configs/reports/reproducibility_report.yaml
src/mavs_ch10c/reporting/__init__.py
src/mavs_ch10c/reporting/tables.py
src/mavs_ch10c/reporting/figures.py
src/mavs_ch10c/reporting/reproducibility_report.py
src/mavs_ch10c/reporting/artifact_manifest.py
scripts/build_variance_tables.py
scripts/build_stability_figures.py
scripts/build_reproducibility_report.py
scripts/build_reproducibility_manifest.py
results/reports/reproducibility_report.md
results/reports/variance_tables.csv
results/reports/stability_tables.csv
results/reports/reproducibility_system_deltas.csv
results/reports/reproducibility_artifact_manifest.json
results/figures/accuracy_variance_by_system.png
results/figures/f1_variance_by_system.png
results/figures/prediction_stability_by_system.png
results/figures/decision_stability_by_system.png
results/figures/consensus_stability_by_system.png
results/figures/trace_stability_by_system.png
results/figures/confidence_interval_widths.png
tests/test_report_inputs_complete.py
tests/test_report_claims_reference_artifacts.py
tests/test_variance_tables_complete.py
tests/test_stability_figures_exist.py
tests/test_reproducibility_manifest_complete.py
```

### Code to Produce

- Table builders:
  - dataset x system x composition x run mode x metric
  - Pure MAVS-GC deltas against every baseline
  - locked-vs-audit consistency
  - confidence interval width comparisons
- Figure builders:
  - accuracy variance by system
  - F1 variance by system
  - prediction stability by system
  - decision stability by system
  - consensus stability by system
  - trace stability by governance system
  - confidence interval width by system
- Report generator:
  - source authority
  - methodology
  - imported Chapter 10A and 10B foundation
  - frozen governance policy
  - repeated execution matrix
  - independent benchmark design
  - anti-overfitting controls
  - results
  - limitations
  - final answer to Chapter 10C
- Reproducibility artifact manifest:
  - source document references
  - import source commits
  - dataset hashes
  - split schedule hashes
  - seed registry hashes
  - initialization schedule hashes
  - composition hashes
  - model config hashes
  - governance source hashes
  - corpus hashes
  - variance dataset hashes
  - metric table hashes
  - figure hashes
  - report hash

### Analysis Rules

- A reproducibility improvement claim must be supported across multiple datasets and multiple baselines, or clearly labeled as dataset-specific.
- Pure MAVS-GC must be compared separately against Veto MAVS because Veto MAVS is a governance control.
- Reduced variance with worse accuracy must be described as a tradeoff, not a universal improvement.
- Wider confidence intervals or lower stability for MAVS-GC must be stated plainly.
- Positive, negative, and mixed outcomes are all acceptable.
- The Phase 5 clean-condition report must not claim Chapter 10C evidence proves robustness under corruption. Corruption-aware reproducibility is evaluated only in Phase 6.
- The report must not claim universal superiority, cross-domain validity, or governance learning.

### Anti-Overfitting Controls

- The report must distinguish locked and audit evidence.
- The report must identify final vs exploratory runs.
- Every claim must reference generated artifacts.
- The report must include seed, split, initialization, and composition protocols.
- The report must include all relevant negative and neutral results.
- Report generation must fail if expected metric rows or figures are missing.

### Phase 5 Acceptance Criteria

- Reproducibility report exists and answers the Chapter 10C research question.
- Variance tables and stability tables exist.
- Stability figures exist.
- Reproducibility artifact manifest exists.
- Every claim maps to tables, figures, or trace-derived metrics.
- `Path.md` records report generation commands, artifact hashes, claim support, limitations, deviations, and compliance.

## Phase 6 - Corruption-Aware Reproducibility

### Objective

Determine whether MAVS-GC maintains reproducibility and stability under adverse conditions.

This phase extends Chapter 10C beyond clean-condition reproducibility and evaluates whether governance-induced stability survives corruption.

The objective is evidence, not validation.

### Motivation

The original Chapter 10C matrix evaluates reproducibility under repeated execution using different seeds, splits, initialization schedules, and specialist compositions.

Chapter 10B demonstrated that MAVS-GC exhibits its most distinctive behavior under adverse conditions, especially corruption regimes such as specialist failure.

Therefore, Chapter 10C must evaluate reproducibility under:

- clean repeated execution conditions
- controlled corruption conditions

This phase investigates whether governance preserves stability and reproducibility when systems are exposed to stress.

### Research Questions

1. Does MAVS-GC reduce variance under corruption?
2. Does MAVS-GC preserve prediction stability under corruption?
3. Does MAVS-GC preserve decision stability under corruption?
4. Does MAVS-GC preserve consensus stability under corruption?
5. Does MAVS-GC preserve trace stability under corruption?
6. Which corruption families destabilize MAVS-GC most?
7. Which corruption families destabilize baseline systems most?
8. Does MAVS-GC maintain stability by increasing rejection?
9. Does specialist failure significantly affect reproducibility?
10. Are governance-induced stability effects stronger under corruption than under clean conditions?

### Scope

Reuse the complete Chapter 10B corruption suite and apply it to the Chapter 10C repeated execution matrix.

This phase must compare corruption-aware reproducibility against the clean Phase 5 evidence without retroactively changing clean-condition metrics or claims.

Generate:

- Corruption Reproducibility Report.
- Corruption Stability Atlas.
- Corruption Variance Atlas.
- Corruption Trace Stability Report.
- Claim Support Ledger.
- Verification Report Addendum.

### Corruption Families

Reuse the complete Chapter 10B corruption suite:

```text
adversarial_confidence_inflation
confidence_distortion
distribution_shift
feature_noise
label_noise
missing_features
random_feature_deletion
specialist_failure
synthetic_sensor_failure
```

### Corruption Levels

```text
0.0
0.05
0.1
0.2
0.4
0.6
0.8
1.0
```

The `0.0` corruption level is the clean anchor and must be tied back to the Phase 5 clean-condition evidence.

### Experimental Matrix

The corruption-aware reproducibility matrix is:

```text
Dataset
x System
x Seed
x Split
x Initialization Schedule
x Specialist Composition
x Corruption Family
x Corruption Level
```

The matrix must preserve the locked and audit separation from earlier phases:

- locked corruption evidence
- audit corruption evidence

Shadow verification may be used for defect discovery but must not be used as final evidence.

### Files and Directories to Create

```text
configs/experiments/corruption_reproducibility.yaml
configs/corruption/ch10b_corruption_suite.yaml
src/mavs_ch10c/corruption/__init__.py
src/mavs_ch10c/corruption/ch10b_suite.py
src/mavs_ch10c/corruption/corruption_matrix.py
src/mavs_ch10c/corruption/corruption_runner.py
src/mavs_ch10c/corruption/corruption_writer.py
src/mavs_ch10c/corruption/cache.py
src/mavs_ch10c/corruption_metrics/__init__.py
src/mavs_ch10c/corruption_metrics/variance.py
src/mavs_ch10c/corruption_metrics/stability.py
src/mavs_ch10c/corruption_metrics/confidence.py
src/mavs_ch10c/corruption_metrics/trace.py
src/mavs_ch10c/corruption_metrics/reporting.py
src/mavs_ch10c/corruption_metrics/manifest.py
scripts/build_corruption_reproducibility_corpus.py
scripts/build_corruption_reproducibility_tables.py
scripts/build_corruption_stability_figures.py
scripts/build_corruption_reproducibility_report.py
results/corruption_reproducibility/.gitkeep
results/corruption_reproducibility/locked/.gitkeep
results/corruption_reproducibility/audit/.gitkeep
results/corruption_reproducibility/corruption_execution_manifest.json
results/corruption_reproducibility/corruption_metric_manifest.json
results/reports/corruption_reproducibility_tables.csv
results/reports/corruption_stability_tables.csv
results/reports/corruption_variance_tables.csv
results/reports/corruption_trace_stability_tables.csv
results/reports/corruption_claim_support_ledger.csv
results/reports/corruption_reproducibility_report.md
results/reports/corruption_verification_addendum.md
results/figures/prediction_stability_by_corruption.png
results/figures/decision_stability_by_corruption.png
results/figures/consensus_stability_by_corruption.png
results/figures/trace_stability_by_corruption.png
results/figures/variance_by_corruption.png
results/figures/confidence_interval_width_by_corruption.png
tests/test_corruption_suite_import_contract.py
tests/test_corruption_matrix_complete.py
tests/test_corruption_inputs_identical_across_systems.py
tests/test_corruption_metrics_complete.py
tests/test_corruption_trace_stability_complete.py
tests/test_corruption_report_claims_reference_artifacts.py
tests/test_corruption_clean_anchor_matches_phase5.py
tests/test_corruption_no_tuning_guard.py
```

### Code to Produce

- Chapter 10B corruption-suite adapter:
  - imports the exact corruption family definitions from Chapter 10B or a hashed local artifact copy
  - records source commit and corruption config hashes
  - fails closed if a corruption family is missing or hash-mismatched
- Corruption matrix builder:
  - expands dataset, system, seed, split schedule, initialization schedule, specialist composition, corruption family, corruption level, and run mode
  - includes `0.0` clean-anchor rows
  - preserves locked/audit separation
- Corruption runner:
  - applies corruption after training and calibration
  - evaluates corrupted benchmark inputs only
  - does not tune models, thresholds, or governance rules after observing corruption results
  - records all corruption parameters and corrupted-input hashes
- Corruption writer:
  - stores corrupted predictions, probabilities, decisions, labels, rejection state, thresholds, severity values, specialist weights, governance traces, run manifests, and artifact hashes
  - writes resumable cache records without changing completed artifact hashes
- Corruption metric builders:
  - compute variance metrics per corruption family and level
  - compute stability metrics per corruption family and level
  - compute confidence interval width and bootstrap confidence interval width
  - compute clean-vs-corruption deltas relative to Phase 5
- Corruption report generator:
  - answers the ten corruption-aware research questions
  - separates locked and audit evidence
  - emits a claim support ledger
  - records limitations, negative results, and caution tradeoffs

### Required Metrics

For every corruption family and corruption level compute:

Variance metrics:

- Accuracy Variance
- F1 Variance
- Rejection Variance
- Threshold Variance
- Severity Variance
- Weight Variance

Stability metrics:

- Prediction Stability
- Decision Stability
- Consensus Stability
- Trace Stability
- Run-to-Run Agreement

Confidence metrics:

- Confidence Interval Width
- Bootstrap Confidence Interval Width

### Benchmarks Produced in This Phase

- Locked corruption reproducibility corpus.
- Audit corruption reproducibility corpus.
- Corruption variance tables.
- Corruption stability tables.
- Corruption trace stability tables.
- Corruption confidence interval tables.
- Clean-vs-corruption delta tables.
- Claim support ledger.

### Interpretation Rules

If MAVS-GC shows only small benefits under clean conditions but large benefits under corruption:

```text
MAVS-GC primarily functions as a governance architecture under adverse conditions rather than as a clean-condition reproducibility optimizer.
```

If MAVS-GC remains stable while baseline systems destabilize:

```text
Governance contributes to reproducibility under stress.
```

If MAVS-GC preserves stability only by increasing rejection:

```text
Stability is achieved through a caution tradeoff.
```

If no stability benefit appears under corruption:

```text
The reproducibility effect does not generalize to stress conditions.
```

These interpretations are conditional. The report must choose only interpretations supported by generated corruption artifacts.

### Model Handling

No new model-development search is allowed in this phase.

Permitted:

- reuse frozen Phase 2 trained specialists and predictions where corruption can be applied post-training
- rerun specialists only under the already frozen Phase 2 repeated-execution protocol if corrupted benchmark artifacts require regeneration
- apply Chapter 10B corruption transformations to benchmark inputs, specialist outputs, or traces according to the imported Chapter 10B corruption definitions

Forbidden:

- hyperparameter search
- architecture search
- corruption-level tuning
- threshold tuning after corruption results are inspected
- governance-policy modification
- using audit corruption results to choose metrics, families, levels, or report templates

### Brutal Independent Benchmark Requirement

Every corruption-aware final claim must use corrupted locked or corrupted audit benchmark rows that remain disjoint from:

- training rows
- validation rows
- calibration rows
- clean locked benchmark rows when the claim is audit-only
- exploratory corruption runs
- smoke test runs

The `0.0` corruption level is allowed only as a clean anchor and must be labeled as such.

### Anti-Overfitting Controls

- Corruption families and levels must be frozen before execution.
- The Chapter 10B corruption suite hash must be stored before corrupted metrics are generated.
- Locked corruption evidence must be generated before audit corruption evidence is inspected.
- Audit corruption evidence must not select metrics, figures, or interpretation language.
- Clean Phase 5 metrics must not be rewritten to improve corruption comparisons.
- Negative, neutral, and mixed corruption outcomes must be preserved.
- A stability gain accompanied by increased rejection must be described as a caution tradeoff.
- All corruption report claims must reference generated corruption tables, figures, trace-derived metrics, or manifests.
- Corruption report generation must fail if expected corruption families, levels, rows, figures, or trace fields are missing.

### Phase 6 Acceptance Criteria

- Complete Chapter 10B corruption family suite is imported or hash-verified.
- Corruption matrix exists for every required dataset, system, locked/audit seed, split schedule, initialization schedule, specialist composition, corruption family, and corruption level.
- Clean anchor rows exist at corruption level `0.0` and tie back to Phase 5 clean evidence.
- Corruption reproducibility tables exist.
- Corruption stability tables exist.
- Corruption variance tables exist.
- Corruption trace stability tables exist.
- All six corruption figures exist.
- Corruption reproducibility report answers all ten research questions.
- Claim support ledger maps every corruption claim to tables, figures, trace metrics, or manifests.
- Verification report addendum records corruption-suite hashes, matrix coverage, artifact hashes, missing units, limitations, and compliance.
- Tests pass for corruption-suite import, matrix completeness, identical inputs across systems, metric completeness, trace stability, report claim references, clean-anchor consistency, and no-tuning guards.
- `Path.md` records commands, row counts, run ids, corruption families, corruption levels, output paths, hashes, failed/retried runs, limitations, and workplan compliance.

### Phase 6 Success Criterion

Chapter 10C succeeds if it can answer:

```text
Does MAVS-GC preserve reproducibility and stability under adverse conditions, and if so, under which corruption families and through which governance behaviors?
```

## Phase 7 - Verification, Reproduction, and Release Readiness

### Scope

Perform final end-to-end verification so the repository can serve as the Chapter 10C reproducibility artifact.

This phase extends the Chapter 10B final verification standard to Chapter 10C and verifies both the clean Phase 5 evidence and the corruption-aware Phase 6 evidence:

- Reproduce or validate the full pipeline.
- Hash all required artifacts.
- Verify matrix completeness.
- Verify no MAVS-GC algorithm changes occurred.
- Verify seed and split independence.
- Verify clean metrics and report claims.
- Verify corruption metrics and report claims.
- Produce final verification report.

### Files and Directories to Create

```text
scripts/reproduce_all.py
scripts/hash_artifacts.py
scripts/verify_artifacts.py
results/reports/artifact_inventory.json
results/reports/verification_report.md
results/reports/corruption_verification_addendum.md
tests/test_end_to_end_smoke.py
tests/test_artifact_inventory_complete.py
tests/test_final_run_guards.py
tests/test_locked_audit_independence.py
tests/test_no_governance_source_drift.py
tests/test_path_md_complete.py
tests/test_final_corruption_artifacts_complete.py
tests/test_final_corruption_claims_reference_artifacts.py
```

### Code to Produce

- One-command reproduction script:
  - import foundation
  - build repetition grid
  - run locked repetition corpus
  - run audit repetition corpus
  - build variance benchmark dataset
  - build reproducibility metrics
  - build variance tables
  - build stability figures
  - build reproducibility report
  - build corruption reproducibility corpus
  - build corruption reproducibility tables
  - build corruption stability figures
  - build corruption reproducibility report
  - hash artifacts
  - verify artifacts
- Artifact inventory:
  - configs
  - source files
  - tests
  - scripts
  - import manifests
  - seed registries
  - split schedules
  - initialization schedules
  - composition manifests
  - run manifests
  - corpus indexes
  - variance datasets
  - metric tables
  - corruption corpora
  - corruption metric tables
  - corruption figures
  - corruption reports
  - figures
  - reports
  - `Path.md`
- Verification gate:
  - required files exist
  - hashes match
  - imported Chapter 10A governance hashes match expected values
  - no forbidden governance algorithm changes occurred
  - seed registry is complete
  - locked and audit seeds are independent
  - split partitions are disjoint
  - all required systems are present
  - all required metrics are present
  - governance traces contain required MAVS-GC fields
  - report claims reference artifacts
  - corruption families and levels are complete
  - corruption report claims reference artifacts
  - clean-anchor corruption rows match Phase 5 clean evidence
  - `Path.md` records all phase evidence

### Model Handling

Final verification may rerun smoke-sized model training for test coverage, but final clean and corruption reproducibility evidence must be generated only by the frozen final matrices. Verification must fail if final reports use smoke, exploratory, training, validation, calibration, or corruption-development metrics as evidence.

### Anti-Overfitting Controls

- Final verification must fail if any final run used exploratory mode.
- Final verification must fail if configs changed after run manifests were written.
- Final verification must fail if audit seeds overlap locked seeds.
- Final verification must fail if benchmark rows overlap training, validation, or calibration rows.
- Final verification must fail if governance source hashes drift after Phase 1.
- Final verification must fail if `Path.md` lacks final run ids, artifact hashes, or deviation records.
- Final verification must fail if Chapter 10B corruption-suite hashes drift without an explicit recorded import update.
- Final verification must fail if corruption report claims are unsupported by generated corruption artifacts.
- Final verification must fail if Phase 6 clean-anchor rows do not match the Phase 5 clean-condition evidence within the declared tolerance.

### Phase 7 Acceptance Criteria

- `python scripts/reproduce_all.py --run-mode final` succeeds from a prepared checkout with access to required upstream artifacts.
- Artifact inventory is complete.
- Verification report has overall status `pass`.
- Corruption verification addendum has overall status `pass`.
- Test suite passes.
- `Path.md` contains the complete implementation trail from source review through final verification.

## Required Trace Contract

Pure MAVS-GC and Veto MAVS traces must preserve the MAVS interpretability fields inherited from Chapter 10A:

```text
x_id
dataset_id
run_mode
execution_seed
split_schedule_id
initialization_schedule_id
specialist_composition_id
system_id
specialist_ids
s
r
z
a
w
m
theta
R
hard_veto
decision
label
config_hash
checkpoint_hashes
trace_hash
```

Chapter 10C trace and prediction records must also include reproducibility provenance:

```text
repetition_id
run_manifest_hash
dataset_manifest_hash
split_hash
train_partition_hash
validation_partition_hash
calibration_partition_hash
benchmark_partition_hash
model_config_hashes
governance_source_hash
composition_hash
environment_hash
prediction_hash
```

Phase 6 corruption-aware trace and prediction records must additionally include:

```text
corruption_family
corruption_level
corruption_seed
corruption_config_hash
corrupted_input_hash
corrupted_specialist_output_hash
corruption_trace_hash
clean_anchor_hash
```

For clean Phase 5 records these corruption fields may be absent. For Phase 6 records they are required, including level `0.0` clean-anchor records.

Required trace tests:

- All active specialists speak for every input.
- Traces are deterministic for fixed inputs, configs, checkpoints, seeds, and environment.
- Clean-condition trace hash changes are explainable through model seed, split schedule, initialization schedule, or composition only.
- Corruption-condition trace hash changes are explainable through model seed, split schedule, initialization schedule, composition, corruption family, corruption level, or corruption seed only.
- Governance thresholds and hard veto behavior match imported Chapter 10A semantics.
- Trace fields align row-for-row with metric inputs.

## Required Benchmark Matrix

Datasets:

```text
breast_cancer_wisconsin
adult_income
credit_card_fraud
bank_marketing
```

Specialists:

```text
random_forest
gradient_boosted_trees
mlp
```

Systems:

```text
single_model
mean_ensemble
static_weighted_ensemble
veto_mavs
pure_mavs_gc
```

Run modes:

```text
locked
audit
shadow_verification
```

Corruption families for Phase 6:

```text
adversarial_confidence_inflation
confidence_distortion
distribution_shift
feature_noise
label_noise
missing_features
random_feature_deletion
specialist_failure
synthetic_sensor_failure
```

Corruption levels for Phase 6:

```text
0.0
0.05
0.1
0.2
0.4
0.6
0.8
1.0
```

Metrics:

```text
accuracy_variance
f1_variance
rejection_variance
threshold_variance
severity_variance
weight_variance
prediction_stability
decision_stability
consensus_stability
trace_stability
run_to_run_agreement
confidence_interval_width
bootstrap_confidence_interval_width
```

## Path.md Documentation Contract

`Path.md` must be updated as implementation proceeds. Each material update must include:

- date and local time
- phase
- files created or changed
- code produced
- commands run
- datasets touched
- models imported, trained, or evaluated
- systems evaluated
- seeds, splits, initialization schedules, and compositions touched
- benchmark or test outputs
- artifact hashes where applicable
- whether the work followed this WorkPlan
- deviations and reason
- risks or limitations
- next required action

No phase is complete until `Path.md` contains enough evidence to verify that phase against this workplan.
