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
- The report must not claim Chapter 10C evidence proves robustness under corruption; that belongs to Chapter 10B.
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

## Phase 6 - Verification, Reproduction, and Release Readiness

### Scope

Perform final end-to-end verification so the repository can serve as the Chapter 10C reproducibility artifact.

This phase extends the Chapter 10B Phase 6 standard to Chapter 10C:

- Reproduce or validate the full pipeline.
- Hash all required artifacts.
- Verify matrix completeness.
- Verify no MAVS-GC algorithm changes occurred.
- Verify seed and split independence.
- Verify metrics and report claims.
- Produce final verification report.

### Files and Directories to Create

```text
scripts/reproduce_all.py
scripts/hash_artifacts.py
scripts/verify_artifacts.py
results/reports/artifact_inventory.json
results/reports/verification_report.md
tests/test_end_to_end_smoke.py
tests/test_artifact_inventory_complete.py
tests/test_final_run_guards.py
tests/test_locked_audit_independence.py
tests/test_no_governance_source_drift.py
tests/test_path_md_complete.py
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
  - `Path.md` records all phase evidence

### Model Handling

Final verification may rerun smoke-sized model training for test coverage, but final reproducibility evidence must be generated only by the frozen final matrix. Verification must fail if final reports use smoke, exploratory, training, validation, or calibration metrics as evidence.

### Anti-Overfitting Controls

- Final verification must fail if any final run used exploratory mode.
- Final verification must fail if configs changed after run manifests were written.
- Final verification must fail if audit seeds overlap locked seeds.
- Final verification must fail if benchmark rows overlap training, validation, or calibration rows.
- Final verification must fail if governance source hashes drift after Phase 1.
- Final verification must fail if `Path.md` lacks final run ids, artifact hashes, or deviation records.

### Phase 6 Acceptance Criteria

- `python scripts/reproduce_all.py --run-mode final` succeeds from a prepared checkout with access to required upstream artifacts.
- Artifact inventory is complete.
- Verification report has overall status `pass`.
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

Required trace tests:

- All active specialists speak for every input.
- Traces are deterministic for fixed inputs, configs, checkpoints, seeds, and environment.
- Trace hash changes are explainable through model seed, split schedule, initialization schedule, or composition only.
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

Metrics:

```text
accuracy_variance
f1_variance
prediction_stability
decision_stability
consensus_stability
trace_stability
run_to_run_agreement
confidence_interval_width
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

