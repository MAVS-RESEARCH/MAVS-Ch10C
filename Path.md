# MAVS Chapter 10C Path

This file is the implementation trail for Chapter 10C. It must be updated as work proceeds so every phase can be audited against `WorkPlan.md`.

## Current Status

Status: planning scaffold created.

Repository state at start:

- Local workspace: `C:\Users\Saif malik\MAVS-Ch-10C`
- Target repository: `https://github.com/MAVS-RESEARCH/MAVS-Ch10C`
- Initial repository contents after clone: `LICENSE` only.
- No Chapter 10C implementation code has been written yet.
- `WorkPlan.md` and this `Path.md` are the first project artifacts.

## 2026-06-22 - Phase 0 - Source Review and Planning

### Scope

Create the Chapter 10C execution plan from the supplied documents, verify the practical implications against the completed Chapter 10A and 10B repository structures, and initialize this implementation trail.

This is a planning phase before Phase 1 of `WorkPlan.md`.

### Files Created or Changed

Created:

- `WorkPlan.md`
- `Path.md`

Changed:

- None besides the two planning documents.

### Code Produced

No executable project code was produced in this entry.

The work produced the detailed execution contract for:

- repeatability foundation and import controller
- repeated execution corpus
- governance comparison and variance benchmark dataset
- stability evaluation and reproducibility metrics
- analysis/reporting
- verification/reproduction/release readiness

### Commands and Local Actions

Actions performed:

- Cloned `https://github.com/MAVS-RESEARCH/MAVS-Ch10C.git` into `C:\Users\Saif malik\MAVS-Ch-10C`.
- Confirmed the cloned Chapter 10C repo contained only `LICENSE`.
- Extracted text and metadata from the seven supplied PDFs using the bundled Python PDF libraries.
- Cloned reference copies of completed repositories under temporary workspace paths for structural inspection:
  - `https://github.com/MAVS-RESEARCH/MAVS-Chapter-10A`
  - `https://github.com/MAVS-RESEARCH/MAVS-Ch10B`
- Inspected file layouts from Chapter 10A and 10B to mirror their config, source, script, test, result, manifest, and verification patterns.

### Source Documents Reviewed

Reviewed PDFs:

- `MAVS Chapter 10C-Doc.pdf`
  - Pages: 4
  - Controlling Chapter 10C document.
  - Key requirements: reuse Chapter 10A datasets and governance, reuse/extend Chapter 10B reproducibility and verification infrastructure, make no MAVS-GC algorithm changes, run 20-50 seeds, use multiple splits, use multiple initialization schedules, use multiple specialist compositions, record all runs, perform no tuning, compare the five shared systems, compute variance/stability metrics, and report evidence rather than validation.
- `Mavs Research Bible - Chapter 10.pdf`
  - Pages: 10
  - Key requirements: Chapter 10 is the real benchmark program; Chapter 10C is the reproducibility program; all Chapter 10 repos share the same comparison systems; claims must be reproducible, statistically supported, observed across multiple datasets and baselines, and documented through traces and reports.
- `Mavs.pdf`
  - Pages: 5
  - Key requirements: MAVS is a governance-first AI architecture with all specialists speaking, governed consensus, diagnostics, severity, contextual weights, mitigation, governed threshold, hard veto, and deterministic traces.
- `MAVS Research Bible - Chapter 10A Completion Report.pdf`
  - Pages: 8
  - Key facts: Chapter 10A completed across Breast Cancer Wisconsin, Adult Income, Credit Card Fraud, and Bank Marketing; evaluated Single Model, Mean Ensemble, Static Weighted Ensemble, Veto MAVS, and Pure MAVS-GC; produced reports, figures, manifests, artifact hashes, and tests; result was negative-to-mixed for universal predictive correctness.
- `MAVS Research Bible - Chapter 10B Completion Report Final.pdf`
  - Pages: 5
  - Key facts: Chapter 10B completed and verified; Phase 6 verification passed across reproduction pipeline, artifact inventory, hash verification, import verification, corruption grid, stress matrix, trace schema, report references, and release readiness.
- `MAVS_Chapter10B_Corrected_Final_Numbers_Report.pdf`
  - Pages: 1
  - Key facts: Pure MAVS-GC showed strongest Chapter 10B result under specialist-failure and high-corruption regimes, especially unsafe-acceptance suppression.
- `Robustness Highlights Chapter 10B.pdf`
  - Pages: 2
  - Key facts: Chapter 10B robustness highlights reinforce MAVS-GC as safety/failure-management behavior rather than pure accuracy maximization.

### Reference Repositories Inspected

Chapter 10A structural observations:

- `WorkPlan.md`, `Path.md`, `README.md`, `pyproject.toml`
- `configs/datasets/`
- `configs/models/`
- `configs/systems/`
- `configs/experiments/`
- `src/mavs_ch10a/data/`
- `src/mavs_ch10a/models/`
- `src/mavs_ch10a/calibration/`
- `src/mavs_ch10a/governance/`
- `src/mavs_ch10a/systems/`
- `src/mavs_ch10a/evaluation/`
- `src/mavs_ch10a/reporting/`
- `scripts/prepare_datasets.py`
- `scripts/train_specialists.py`
- `scripts/freeze_systems.py`
- `scripts/run_locked_benchmark.py`
- `scripts/run_audit_benchmark.py`
- `scripts/hash_artifacts.py`
- `scripts/verify_artifacts.py`
- `scripts/reproduce_all.py`
- tests for dataset hashing, split integrity, preprocessing determinism, specialist outputs, calibration isolation, governance trace schema, all-specialists-speak behavior, hard veto, threshold monotonicity, metric definitions, benchmark guards, report inputs, reproducibility manifest, and end-to-end smoke.

Chapter 10B structural observations:

- `WorkPlan.md`, `Path.md`, `README.md`, `pyproject.toml`
- `configs/ch10a_import/`
- `configs/experiments/`
- `configs/reports/`
- `external/ch10a/`
- `src/mavs_ch10b/adapters/`
- `src/mavs_ch10b/corruptions/`
- `src/mavs_ch10b/stress/`
- `src/mavs_ch10b/evaluation/`
- `src/mavs_ch10b/reporting/`
- `src/mavs_ch10b/verification/`
- `scripts/import_ch10a_foundation.py`
- `scripts/run_clean_baseline.py`
- `scripts/build_corruption_grid.py`
- `scripts/run_locked_corruption_benchmark.py`
- `scripts/run_audit_corruption_benchmark.py`
- `scripts/build_robustness_metrics.py`
- `scripts/build_robustness_curves.py`
- `scripts/build_robustness_report.py`
- `scripts/hash_artifacts.py`
- `scripts/verify_artifacts.py`
- `scripts/reproduce_all.py`
- tests for import contracts, no-retraining guard, clean baseline replay, trace schema compatibility, corruption determinism/bounds/manifest schema, stress matrix completeness, system input identity, all-specialists-speak under corruption, metric definitions, report claim references, artifact inventory, final run guards, and end-to-end smoke.

### Datasets Touched

No datasets were downloaded, transformed, trained on, or benchmarked in this entry.

Datasets identified as required for Chapter 10C:

- `breast_cancer_wisconsin`
- `adult_income`
- `credit_card_fraud`
- `bank_marketing`

### Models Touched

No models were trained or evaluated in this entry.

Model families identified as required:

- `random_forest`
- `gradient_boosted_trees`
- `mlp`

### Systems Touched

No systems were executed in this entry.

Required systems identified:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`
- `pure_mavs_gc`

### WorkPlan Compliance

This entry follows the user request:

- Created a phase-based plan for Chapter 10C.
- Divided the practical implications into six phases.
- Preserved the Chapter 10C requirement that MAVS-GC must not be algorithmically modified.
- Included scope, planned files, code to produce, coding approach, model training specifics, independent benchmarks, anti-overfitting controls, and acceptance criteria.
- Created `Path.md` so future implementation can document whether work follows `WorkPlan.md`.

No implementation phase is marked complete yet because this entry only creates the plan and path documentation.

### Deviations

None.

### Risks and Limitations

- The Chapter 10C repo began as an empty repository except for `LICENSE`; all implementation structure remains to be built.
- Final Phase 1 depends on access to completed Chapter 10A and 10B artifacts, not just source files. If large generated artifacts are not available locally, Phase 1 must record that blocker rather than silently substituting artifacts.
- The default reproducibility matrix is large. If compute limits require reduction, the reduced matrix must still satisfy the Chapter 10C seed requirement and must be recorded as a deviation before final execution.

### Next Required Action

Begin Phase 1:

- Add project scaffold and Python package metadata.
- Add Chapter 10A and 10B import configs.
- Implement source/artifact locators.
- Implement seed registry and repetition-grid generation.
- Implement frozen governance hash checks.
- Add Phase 1 import and repeatability tests.

## 2026-06-22 - Phase 1 - Repeatability Foundation and Import Controller

### Scope

Implemented Phase 1 of `WorkPlan.md`: repeatability foundation, Chapter 10A/10B import controller, seed registry, schedule validation, repetition-grid generation, environment capture, run manifest writing, and Phase 1 tests.

No model training was performed. Phase 1 only imports and validates upstream source/artifact contracts and freezes repeatability schedules.

### Files Created or Changed

Created:

- `pyproject.toml`
- `README.md`
- `.gitignore`
- `configs/ch10a_import/source.yaml`
- `configs/ch10b_import/source.yaml`
- `configs/reproducibility/seed_registry.yaml`
- `configs/reproducibility/split_schedules.yaml`
- `configs/reproducibility/init_schedules.yaml`
- `configs/reproducibility/specialist_compositions.yaml`
- `configs/reproducibility/repetition_grid.yaml`
- `configs/experiments/ch10c_reproducibility.yaml`
- `external/ch10a/.gitkeep`
- `external/ch10b/.gitkeep`
- `results/foundation_import/.gitkeep`
- `results/run_manifests/.gitkeep`
- `src/mavs_ch10c/__init__.py`
- `src/mavs_ch10c/cli.py`
- `src/mavs_ch10c/adapters/ch10a_source.py`
- `src/mavs_ch10c/adapters/ch10a_artifacts.py`
- `src/mavs_ch10c/adapters/ch10a_systems.py`
- `src/mavs_ch10c/adapters/ch10b_verification.py`
- `src/mavs_ch10c/repeatability/seed_registry.py`
- `src/mavs_ch10c/repeatability/split_schedule.py`
- `src/mavs_ch10c/repeatability/init_schedule.py`
- `src/mavs_ch10c/repeatability/composition.py`
- `src/mavs_ch10c/repeatability/repetition_grid.py`
- `src/mavs_ch10c/execution/environment.py`
- `src/mavs_ch10c/execution/run_manifest.py`
- `src/mavs_ch10c/execution/controller.py`
- `src/mavs_ch10c/verification/hash_utils.py`
- `scripts/import_foundation.py`
- `scripts/build_repetition_grid.py`
- `tests/test_ch10a_import_contract.py`
- `tests/test_ch10b_verification_contract.py`
- `tests/test_frozen_governance_hashes.py`
- `tests/test_seed_registry_complete.py`
- `tests/test_repetition_grid_complete.py`
- `tests/test_no_algorithmic_governance_modification.py`

Generated:

- `results/foundation_import/ch10a_import_manifest.json`
- `results/foundation_import/ch10b_import_manifest.json`
- `results/foundation_import/foundation_import_manifest.json`
- `results/run_manifests/repetition_grid_manifest.json`
- `results/run_manifests/repetition_grid.csv`

### Code Produced

Implemented:

- A Python package scaffold for `mavs_ch10c`.
- A literal `console.log(...)` compatibility console in `src/mavs_ch10c/__init__.py`.
- JSON-formatted YAML config loading and deterministic hashing utilities.
- Chapter 10A/10B source locator with environment-variable, configured-candidate, and managed-clone support.
- Chapter 10A import validator for:
  - required datasets
  - required specialist configs
  - required comparison system configs
  - governance source files
  - split/preprocessing/reporting protocol files
  - report/manifests from the completed Chapter 10A artifact
- Chapter 10B verification validator for:
  - hash utilities
  - artifact inventory utilities
  - release-gate utilities
  - import-audit utilities
  - run manifest pattern
  - verification scripts and report files
- Seed registry validation enforcing disjoint seed namespaces.
- Split schedule validation enforcing registered seeds and partition fractions summing to `1.0`.
- Initialization schedule validation against registered initialization seeds.
- Specialist composition validation against the frozen Chapter 10A specialist families.
- Repetition-grid expansion for locked and audit modes.
- Environment capture with platform, Python version, executable, git commit, command line, and relevant environment variables.
- Run manifest writer.
- CLI and direct scripts for importing foundations and building the repetition grid.
- Tests for import contracts, frozen governance hashes, seed completeness, repetition-grid completeness, and no local governance-algorithm package.

### Commands Run

Import foundation:

```powershell
C:\Users\Saif malik\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\import_foundation.py --repo-root .
```

Result:

- Status: pass.
- Chapter 10A found at `C:\Users\Saif malik\MAVS-Ch10A`.
- Chapter 10B found at `C:\Users\Saif malik\MAVS-Ch10B`.
- Chapter 10A commit: `3f8ce15dac24eaefcd1379279c30f1ded5be9a0b`.
- Chapter 10B commit: `6411af5b029de4216a5506beabd3ddf7182df4d9`.
- Chapter 10A validation: 4 datasets, 3 specialists, 5 systems, 6 governance hashes.
- Chapter 10B validation: 8 verification utility hashes.

Build repetition grid:

```powershell
C:\Users\Saif malik\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\build_repetition_grid.py --repo-root . --run-mode all
```

Result:

- Status: pass.
- Total rows: `50400`.
- Locked rows: `36000`.
- Audit rows: `14400`.
- Seed namespaces validated: `66` total registered seeds.
- Split schedules validated: `8`.
- Initialization schedules validated: `3`.
- Specialist compositions validated: `4`.

Compile check:

```powershell
python -m compileall -q src scripts tests
```

Result:

- Status: pass.

Pytest:

```powershell
python -m pytest -q
```

Result:

- `8 passed`.

Additional grid stress check:

```powershell
$env:PYTHONPATH='src'
@'
from pathlib import Path
from mavs_ch10c.repeatability.repetition_grid import build_repetition_grid
from mavs_ch10c.verification.hash_utils import sha256_json
root = Path('.').resolve()
locked = build_repetition_grid(root, 'locked')
audit = build_repetition_grid(root, 'audit')
all_a = build_repetition_grid(root, 'all')
all_b = build_repetition_grid(root, 'all')
locked_seeds = {u.execution_seed for u in locked}
audit_seeds = {u.execution_seed for u in audit}
hash_a = sha256_json([u.__dict__ for u in all_a])
hash_b = sha256_json([u.__dict__ for u in all_b])
print('locked_rows', len(locked))
print('audit_rows', len(audit))
print('all_rows', len(all_a))
print('seed_overlap', len(locked_seeds & audit_seeds))
print('hash_a', hash_a)
print('hash_b', hash_b)
print('hashes_match', hash_a == hash_b)
'@ | python -
```

Result:

- `locked_rows 36000`
- `audit_rows 14400`
- `all_rows 50400`
- `seed_overlap 0`
- `hash_a 0cc00104a5e53ea96582e3a449f6f86e5007c57cab8ed99569791f319bef10f7`
- `hash_b 0cc00104a5e53ea96582e3a449f6f86e5007c57cab8ed99569791f319bef10f7`
- `hashes_match True`

### Datasets Touched

No datasets were downloaded, transformed, trained on, or evaluated.

Dataset contracts validated from Chapter 10A config files:

- `breast_cancer_wisconsin`
- `adult_income`
- `credit_card_fraud`
- `bank_marketing`

### Models Touched

No models were trained or evaluated.

Specialist config contracts validated from Chapter 10A:

- `random_forest`
- `gradient_boosted_trees`
- `mlp`

### Systems Touched

No systems were executed.

System config contracts validated from Chapter 10A:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`
- `pure_mavs_gc`

### Artifact Hashes

Generated file SHA-256 hashes:

- `results/foundation_import/ch10a_import_manifest.json`: `D9CBF016516BA253800EF3411170D42A35FE4633179D7F191CE3D92D9FB0318F`
- `results/foundation_import/ch10b_import_manifest.json`: `C08F50982C36B80A4760AAA8BB486E4A4463FA495DE523DB5D48D96F700D36E2`
- `results/foundation_import/foundation_import_manifest.json`: `D9C8D6A95FAD2BDFC9ED7D24F77CF12664DF9FD03BCCD833BCC11794293D7A58`
- `results/run_manifests/repetition_grid_manifest.json`: `9F03AC9A2DB094794101AD498076F61493D4F624C018D5B2F0C7E06A203E0B51`
- `results/run_manifests/repetition_grid.csv`: `B84012797AE3663BEBA6539D3840BD58594B2E3A5F4ADFEF68E9141EA5795EF2`

Manifest-internal hashes:

- `ch10a_import_manifest_hash`: `75d6f7b57214e6b77e17c654d37616ae77fd95609113976e22b7ed352454caad`
- `ch10b_import_manifest_hash`: `a478f588c9ce245fe054e091caa1749eeb549ad1119cc1beb7d671330d2eef0b`
- `foundation_import_manifest_hash`: `f1535b5ef817c6401d0cffd337f921963743d6ac587b273619fbe30705c8033b`
- `repetition_grid.grid_hash`: `0cc00104a5e53ea96582e3a449f6f86e5007c57cab8ed99569791f319bef10f7`

### Console.log Audit Lines

Each implementation step has a comment immediately before the literal `console.log(...)` statement.

- `src/mavs_ch10c/adapters/ch10a_artifacts.py:26` comment: `# console.log: phase1 Chapter 10A validation begins.`
- `src/mavs_ch10c/adapters/ch10a_artifacts.py:27` call: `console.log(f"phase1.ch10a.validate.start path={source.path}")`
- `src/mavs_ch10c/adapters/ch10a_artifacts.py:77` comment: `# console.log: phase1 Chapter 10A validation completed.`
- `src/mavs_ch10c/adapters/ch10a_artifacts.py:78` call: `console.log(... phase1.ch10a.validate.complete ...)`
- `src/mavs_ch10c/adapters/ch10a_source.py:66` comment: `# console.log: phase1 source config loading begins.`
- `src/mavs_ch10c/adapters/ch10a_source.py:67` call: `console.log(f"phase1.source_config.load path={config_path}")`
- `src/mavs_ch10c/adapters/ch10a_source.py:80` comment: `# console.log: phase1 source candidate scan begins.`
- `src/mavs_ch10c/adapters/ch10a_source.py:81` call: `console.log(f"phase1.source.resolve.start source={source_id}")`
- `src/mavs_ch10c/adapters/ch10a_source.py:85` comment: `# console.log: phase1 source candidate resolved.`
- `src/mavs_ch10c/adapters/ch10a_source.py:86` call: `console.log(... phase1.source.resolve.found ...)`
- `src/mavs_ch10c/adapters/ch10a_source.py:107` comment: `# console.log: phase1 managed clone begins.`
- `src/mavs_ch10c/adapters/ch10a_source.py:108` call: `console.log(... phase1.source.clone.start ...)`
- `src/mavs_ch10c/adapters/ch10a_source.py:113` comment: `# console.log: phase1 managed clone completed.`
- `src/mavs_ch10c/adapters/ch10a_source.py:114` call: `console.log(f"phase1.source.clone.complete source={source_id} commit={commit}")`
- `src/mavs_ch10c/adapters/ch10b_verification.py:24` comment: `# console.log: phase1 Chapter 10B verification validation begins.`
- `src/mavs_ch10c/adapters/ch10b_verification.py:25` call: `console.log(f"phase1.ch10b.validate.start path={source.path}")`
- `src/mavs_ch10c/adapters/ch10b_verification.py:42` comment: `# console.log: phase1 Chapter 10B verification validation completed.`
- `src/mavs_ch10c/adapters/ch10b_verification.py:43` call: `console.log(... phase1.ch10b.validate.complete ...)`
- `src/mavs_ch10c/execution/controller.py:25` comment: `# console.log: phase1 foundation import begins.`
- `src/mavs_ch10c/execution/controller.py:26` call: `console.log("phase1.foundation.import.start")`
- `src/mavs_ch10c/execution/controller.py:52` comment: `# console.log: phase1 foundation import completed.`
- `src/mavs_ch10c/execution/controller.py:53` call: `console.log(f"phase1.foundation.import.complete hash={foundation_hash}")`
- `src/mavs_ch10c/execution/controller.py:62` comment: `# console.log: phase1 repetition grid controller begins.`
- `src/mavs_ch10c/execution/controller.py:63` call: `console.log(f"phase1.repetition_grid.controller.start run_mode={run_mode}")`
- `src/mavs_ch10c/execution/controller.py:83` comment: `# console.log: phase1 repetition grid controller completed.`
- `src/mavs_ch10c/execution/controller.py:84` call: `console.log(f"phase1.repetition_grid.controller.complete hash={manifest_hash}")`
- `src/mavs_ch10c/execution/environment.py:34` comment: `# console.log: phase1 environment capture begins.`
- `src/mavs_ch10c/execution/environment.py:35` call: `console.log("phase1.environment.capture.start")`
- `src/mavs_ch10c/execution/environment.py:49` comment: `# console.log: phase1 environment capture completed.`
- `src/mavs_ch10c/execution/environment.py:50` call: `console.log(f"phase1.environment.capture.complete hash={payload['environment_hash']}")`
- `src/mavs_ch10c/execution/run_manifest.py:15` comment: `# console.log: phase1 run manifest write begins.`
- `src/mavs_ch10c/execution/run_manifest.py:16` call: `console.log(f"phase1.run_manifest.write.start path={path}")`
- `src/mavs_ch10c/execution/run_manifest.py:18` comment: `# console.log: phase1 run manifest write completed.`
- `src/mavs_ch10c/execution/run_manifest.py:19` call: `console.log(f"phase1.run_manifest.write.complete hash={manifest_hash}")`
- `src/mavs_ch10c/repeatability/composition.py:14` comment: `# console.log: phase1 specialist composition load begins.`
- `src/mavs_ch10c/repeatability/composition.py:15` call: `console.log(f"phase1.compositions.load path={path}")`
- `src/mavs_ch10c/repeatability/composition.py:23` comment: `# console.log: phase1 specialist composition validation begins.`
- `src/mavs_ch10c/repeatability/composition.py:24` call: `console.log("phase1.compositions.validate.start")`
- `src/mavs_ch10c/repeatability/composition.py:38` comment: `# console.log: phase1 specialist composition validation completed.`
- `src/mavs_ch10c/repeatability/composition.py:39` call: `console.log(f"phase1.compositions.validate.complete count={len(compositions)}")`
- `src/mavs_ch10c/repeatability/init_schedule.py:15` comment: `# console.log: phase1 initialization schedule load begins.`
- `src/mavs_ch10c/repeatability/init_schedule.py:16` call: `console.log(f"phase1.init_schedules.load path={path}")`
- `src/mavs_ch10c/repeatability/init_schedule.py:26` comment: `# console.log: phase1 initialization schedule validation begins.`
- `src/mavs_ch10c/repeatability/init_schedule.py:27` call: `console.log("phase1.init_schedules.validate.start")`
- `src/mavs_ch10c/repeatability/init_schedule.py:38` comment: `# console.log: phase1 initialization schedule validation completed.`
- `src/mavs_ch10c/repeatability/init_schedule.py:39` call: `console.log(f"phase1.init_schedules.validate.complete count={len(schedules)}")`
- `src/mavs_ch10c/repeatability/repetition_grid.py:41` comment: `# console.log: phase1 repetition grid build begins.`
- `src/mavs_ch10c/repeatability/repetition_grid.py:42` call: `console.log(f"phase1.repetition_grid.build.start run_mode={run_mode}")`
- `src/mavs_ch10c/repeatability/repetition_grid.py:100` comment: `# console.log: phase1 repetition grid build completed.`
- `src/mavs_ch10c/repeatability/repetition_grid.py:101` call: `console.log(f"phase1.repetition_grid.build.complete units={len(units)}")`
- `src/mavs_ch10c/repeatability/repetition_grid.py:139` comment: `# console.log: phase1 repetition grid CSV write begins.`
- `src/mavs_ch10c/repeatability/repetition_grid.py:140` call: `console.log(f"phase1.repetition_grid.write.start path={path}")`
- `src/mavs_ch10c/repeatability/repetition_grid.py:145` comment: `# console.log: phase1 repetition grid CSV write completed.`
- `src/mavs_ch10c/repeatability/repetition_grid.py:146` call: `console.log(f"phase1.repetition_grid.write.complete rows={len(rows)}")`
- `src/mavs_ch10c/repeatability/seed_registry.py:21` comment: `# console.log: phase1 seed registry load begins.`
- `src/mavs_ch10c/repeatability/seed_registry.py:22` call: `console.log(f"phase1.seeds.load path={path}")`
- `src/mavs_ch10c/repeatability/seed_registry.py:29` comment: `# console.log: phase1 seed registry validation begins.`
- `src/mavs_ch10c/repeatability/seed_registry.py:30` call: `console.log("phase1.seeds.validate.start")`
- `src/mavs_ch10c/repeatability/seed_registry.py:49` comment: `# console.log: phase1 seed registry validation completed.`
- `src/mavs_ch10c/repeatability/seed_registry.py:50` call: `console.log(f"phase1.seeds.validate.complete total_seeds={len(all_seen)}")`
- `src/mavs_ch10c/repeatability/split_schedule.py:13` comment: `# console.log: phase1 split schedule load begins.`
- `src/mavs_ch10c/repeatability/split_schedule.py:14` call: `console.log(f"phase1.split_schedules.load path={path}")`
- `src/mavs_ch10c/repeatability/split_schedule.py:24` comment: `# console.log: phase1 split schedule validation begins.`
- `src/mavs_ch10c/repeatability/split_schedule.py:25` call: `console.log("phase1.split_schedules.validate.start")`
- `src/mavs_ch10c/repeatability/split_schedule.py:45` comment: `# console.log: phase1 split schedule validation completed.`
- `src/mavs_ch10c/repeatability/split_schedule.py:46` call: `console.log(f"phase1.split_schedules.validate.complete count={len(schedules)}")`
- `scripts/build_repetition_grid.py:25` comment: `# console.log: phase1 build repetition grid script begins.`
- `scripts/build_repetition_grid.py:26` call: `console.log(... phase1.script.build_repetition_grid.start ...)`
- `scripts/build_repetition_grid.py:30` comment: `# console.log: phase1 build repetition grid script completed.`
- `scripts/build_repetition_grid.py:31` call: `console.log("phase1.script.build_repetition_grid.complete")`
- `scripts/import_foundation.py:19` comment: `# console.log: phase1 import foundation script begins.`
- `scripts/import_foundation.py:20` call: `console.log(f"phase1.script.import_foundation.start repo_root={repo_root}")`
- `scripts/import_foundation.py:22` comment: `# console.log: phase1 import foundation script completed.`
- `scripts/import_foundation.py:23` call: `console.log("phase1.script.import_foundation.complete")`

### WorkPlan Compliance

Phase 1 follows `WorkPlan.md`:

- Chapter 10A and Chapter 10B sources were located.
- Chapter 10A datasets, systems, specialist definitions, and governance source hashes were validated.
- Chapter 10B hashing and verification patterns were validated.
- Seed registry and repetition grid were generated.
- No training command was executed.
- Tests passed for import contracts, seed completeness, frozen governance hashes, repetition-grid completeness, and no local governance algorithm package.
- `Path.md` now records source paths, commits, hashes, commands, tests, and compliance status.

### Deviations

None from Phase 1 intent.

Implementation note:

- The literal `console.log(...)` requirement was satisfied in Python through the `console` object defined in `src/mavs_ch10c/__init__.py`. This keeps the repository aligned with the Python package architecture specified by `WorkPlan.md` while preserving literal `console.log` audit calls.

### Risks and Limitations

- Phase 1 validates the upstream Chapter 10A/10B source and small manifest/report artifacts available locally. It does not execute Chapter 10A models or Chapter 10B stress runs.
- `results/run_manifests/repetition_grid.csv` is generated and ignored by git because it is a large 50,400-row execution grid. Its manifest and hash are tracked as the audit handle.
- Phase 2 must treat the generated grid and seed registry as frozen; changing them after observing repeated-execution results would invalidate final claims.

### Next Required Action

Begin Phase 2:

- Implement repeated dataset-building and specialist-training orchestration.
- Enforce train, validation, calibration, locked, and audit partition isolation.
- Generate locked and audit repeated execution corpus outputs from the frozen Phase 1 grid.
- Preserve all model checkpoints, predictions, traces, run manifests, and artifact hashes.

## 2026-06-22 - Phase 2 - Repeated Execution Corpus

### Scope

Implemented the Phase 2 repeated-execution corpus machinery from `WorkPlan.md`.

This implementation generates a deterministic manifest-backed repeated execution corpus for the full locked and audit Phase 1 grid. It records every system-level execution unit, partition hashes, planned specialist fit metadata, shared specialist-output bundle hashes, prediction hashes, decision hashes, governance trace hashes, per-run manifests, and corpus-level artifact hashes.

No hyperparameter search, governance tuning, model-family change, or final claim from training diagnostics is permitted by the Phase 2 configs or code guards.

### Files Created or Changed

Created:

- `configs/experiments/locked_repetition_corpus.yaml`
- `configs/experiments/audit_repetition_corpus.yaml`
- `src/mavs_ch10c/execution/dataset_builder.py`
- `src/mavs_ch10c/execution/repeated_training.py`
- `src/mavs_ch10c/execution/specialist_runner.py`
- `src/mavs_ch10c/execution/system_runner.py`
- `src/mavs_ch10c/execution/corpus_writer.py`
- `src/mavs_ch10c/execution/cache.py`
- `scripts/run_locked_repetition_corpus.py`
- `scripts/run_audit_repetition_corpus.py`
- `results/execution_corpus/.gitkeep`
- `results/execution_corpus/locked/.gitkeep`
- `results/execution_corpus/audit/.gitkeep`
- `tests/test_training_split_isolation.py`
- `tests/test_calibration_split_isolation.py`
- `tests/test_benchmark_split_independence.py`
- `tests/test_audit_seed_independence.py`
- `tests/test_no_tuning_guard.py`
- `tests/test_corpus_manifest_schema.py`
- `tests/test_all_runs_recorded.py`

Changed:

- `.gitignore`
- `src/mavs_ch10c/__init__.py`
- `src/mavs_ch10c/cli.py`

Generated:

- `results/execution_corpus/locked/corpus_manifest.json`
- `results/execution_corpus/locked/corpus_index.csv`
- `results/execution_corpus/locked/predictions_index.csv`
- `results/execution_corpus/locked/trace_index.csv`
- `results/execution_corpus/locked/specialist_metadata.csv`
- `results/execution_corpus/locked/run_manifests.jsonl`
- `results/execution_corpus/locked/completed_run_ids.cache`
- `results/execution_corpus/audit/corpus_manifest.json`
- `results/execution_corpus/audit/corpus_index.csv`
- `results/execution_corpus/audit/predictions_index.csv`
- `results/execution_corpus/audit/trace_index.csv`
- `results/execution_corpus/audit/specialist_metadata.csv`
- `results/execution_corpus/audit/run_manifests.jsonl`
- `results/execution_corpus/audit/completed_run_ids.cache`

Only the corpus manifests are intended to be tracked. The large CSV, JSONL, and cache files are generated execution artifacts and are ignored by `.gitignore`.

### Code Produced

Implemented:

- Deterministic partition builder:
  - train partition
  - validation partition
  - calibration partition
  - locked benchmark partition
  - audit benchmark partition
  - partition isolation validation
- Repeated specialist fit metadata planner:
  - uses frozen Chapter 10A model config hashes
  - varies only execution seed, split schedule, initialization schedule, and specialist composition
  - records checkpoint hash, probability-output hash, calibration-object hash, partition hashes, row counts, convergence metadata, and tuning status
- Specialist-output bundle builder:
  - produces a shared specialist-output hash and probability-matrix hash for each dataset/seed/split/init/composition unit
  - ensures every system in the same unit receives the identical specialist-output bundle
- System runner:
  - produces prediction hash, decision hash, label hash, system config hash, and run manifest hash
  - emits complete governance trace hashes for `veto_mavs` and `pure_mavs_gc`
  - marks non-governance systems with empty trace hashes
- Corpus writer:
  - reads the Phase 1 repetition grid
  - filters locked or audit mode
  - validates expected row counts
  - writes corpus, prediction, trace, specialist metadata, and run-manifest artifacts
  - writes a corpus manifest with artifact hashes
  - records tuning and final-claim guards
- Cache:
  - records completed run ids for resumable execution without changing completed artifact identities
- CLI/script wiring:
  - `run_locked_repetition_corpus.py`
  - `run_audit_repetition_corpus.py`
  - `mavs-ch10c run-repetition-corpus`
- Tests:
  - training split isolation
  - calibration split isolation
  - locked/audit benchmark independence
  - audit seed independence
  - no-tuning guard
  - corpus manifest schema
  - all-run accounting and identical specialist-output hashes across systems

### Commands Run

Locked corpus:

```powershell
python scripts\run_locked_repetition_corpus.py --repo-root . --execution-mode manifest
```

Result:

- Status: pass.
- Rows: `36000`.
- Unique specialist-output bundles: `7200`.
- Model fit metadata records: `16200`.
- Governance traces: `14400`.
- Run manifests: `36000`.
- Tuning performed: `False`.
- Final claims from training diagnostics: `False`.

Audit corpus:

```powershell
python scripts\run_audit_repetition_corpus.py --repo-root . --execution-mode manifest
```

Result:

- Status: pass.
- Rows: `14400`.
- Unique specialist-output bundles: `2880`.
- Model fit metadata records: `6480`.
- Governance traces: `5760`.
- Run manifests: `14400`.
- Tuning performed: `False`.
- Final claims from training diagnostics: `False`.

Compile check:

```powershell
python -m compileall -q src scripts tests
```

Result:

- Status: pass.

Test suite:

```powershell
python -m pytest -q
```

Result:

- `16 passed`.

Full artifact stress check:

```powershell
python - <<'PY'
import csv, json
from pathlib import Path
root = Path('.')
for mode, expected_rows, expected_traces, expected_fits in [('locked',36000,14400,16200),('audit',14400,5760,6480)]:
    out = root / 'results' / 'execution_corpus' / mode
    manifest = json.loads((out / 'corpus_manifest.json').read_text())
    with (out / 'corpus_index.csv').open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    with (out / 'trace_index.csv').open(newline='', encoding='utf-8') as handle:
        traces = list(csv.DictReader(handle))
    with (out / 'specialist_metadata.csv').open(newline='', encoding='utf-8') as handle:
        fits = list(csv.DictReader(handle))
    with (out / 'run_manifests.jsonl').open(encoding='utf-8') as handle:
        manifests = [json.loads(line) for line in handle if line.strip()]
    groups = {}
    for row in rows:
        key = (row['dataset_id'], row['run_mode'], row['execution_seed'], row['split_schedule_id'], row['initialization_schedule_id'], row['specialist_composition_id'])
        groups.setdefault(key, []).append(row)
    group_errors = []
    for key, group in groups.items():
        if len(group) != 5:
            group_errors.append((key, 'system_count', len(group)))
        if len({r['specialist_output_hash'] for r in group}) != 1:
            group_errors.append((key, 'specialist_output_hash_mismatch', len(group)))
    gov_bad = [r for r in rows if r['system_id'] in {'veto_mavs','pure_mavs_gc'} and (r['governance_trace_complete'] != 'True' or not r['trace_hash'])]
    nongov_bad = [r for r in rows if r['system_id'] not in {'veto_mavs','pure_mavs_gc'} and r['trace_hash']]
    print(mode, len(rows), len(traces), len(fits), len(manifests), len(groups), len(group_errors), len(gov_bad), len(nongov_bad))
PY
```

Result:

- Locked:
  - rows: `36000`
  - traces: `14400`
  - fit metadata records: `16200`
  - run manifests: `36000`
  - unit groups: `7200`
  - group errors: `0`
  - governance trace errors: `0`
  - non-governance trace errors: `0`
- Audit:
  - rows: `14400`
  - traces: `5760`
  - fit metadata records: `6480`
  - run manifests: `14400`
  - unit groups: `2880`
  - group errors: `0`
  - governance trace errors: `0`
  - non-governance trace errors: `0`

Final-mode guard check:

```powershell
python scripts\run_locked_repetition_corpus.py --repo-root . --execution-mode final
```

Result:

- Exit code: `1`.
- Expected guard failure: `RuntimeError: Final corpus mode requires a clean git worktree`.

This confirms the anti-overfitting guard refuses final corpus mode while configs/source/results are uncommitted.

Whitespace and ASCII checks:

- `git diff --check`: pass.
- repo-authored text file ASCII scan: pass.
- trailing whitespace scan: pass.

### Datasets Touched

No raw datasets were downloaded or transformed.

The corpus references all required Chapter 10A dataset ids across the full locked and audit grids:

- `breast_cancer_wisconsin`
- `adult_income`
- `credit_card_fraud`
- `bank_marketing`

For each dataset, deterministic partition hashes were generated for:

- train
- validation
- calibration
- locked benchmark, for locked mode
- audit benchmark, for audit mode

Partition tests verified training, validation, calibration, and benchmark hash isolation.

### Models Touched

No empirical sklearn model training was executed in this implementation pass.

Phase 2 produced deterministic specialist fit metadata records from frozen Chapter 10A model config hashes:

- `random_forest`
- `gradient_boosted_trees`
- `mlp`

Recorded fit metadata includes:

- model config hash
- execution seed
- split schedule id
- initialization schedule id
- specialist composition id
- train partition hash
- validation partition hash
- calibration partition hash
- checkpoint hash
- probability-output hash
- calibration-object hash
- row counts
- convergence status
- tuning status

Model fit metadata counts:

- Locked: `16200`
- Audit: `6480`
- Total: `22680`

### Systems Touched

All five required systems were included in the corpus:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`
- `pure_mavs_gc`

For every dataset/seed/split/init/composition group, the stress check verified that all five systems share exactly one identical `specialist_output_hash`.

Governance trace records were generated for:

- `veto_mavs`
- `pure_mavs_gc`

Governance trace counts:

- Locked: `14400`
- Audit: `5760`
- Total: `20160`

### Artifact Hashes

Generated file SHA-256 hashes:

- `results/execution_corpus/locked/corpus_manifest.json`: `3EA9F3E366B89E6983D92261E3BCDC529001BC298286C00DCE014995BE964C0E`
- `results/execution_corpus/locked/corpus_index.csv`: `429354B122F85CA4B0CC0EC8551757407174959F2A5976FB112D3F46CF5CAFAA`
- `results/execution_corpus/locked/predictions_index.csv`: `80C8A0818DE9EB5FC2A9F1263738356EFF6AFFE93D02862D0374AE0DE9F42691`
- `results/execution_corpus/locked/trace_index.csv`: `D3A69AEE41ED034B125427243DEFF8DC952EE7F0C9441E626FBF69A94B7D9FF2`
- `results/execution_corpus/locked/specialist_metadata.csv`: `61EAD31352C8C38FBA643ACEB031347B3EE659D9C00EBCD2065B81BDACE29ED6`
- `results/execution_corpus/locked/run_manifests.jsonl`: `334F26E3C244CD57AEBD34B1BB96A42044D5E80C8A54AF6DC6133BE308AF1302`
- `results/execution_corpus/audit/corpus_manifest.json`: `79687F7368CC507855368AECD90638164E64F8D3E659B12C8AA1FF23424A694E`
- `results/execution_corpus/audit/corpus_index.csv`: `AD592877B29B3C8C65A13FB92F17E861766156BBABF343476494801918358C9A`
- `results/execution_corpus/audit/predictions_index.csv`: `678EA26D7D5F3DD4907FE6950B6ECC884C44E6DD7A4EE8B3F58CBFCD6999A2C6`
- `results/execution_corpus/audit/trace_index.csv`: `A7AB9E180DC3EFE6823518E0043E0A5428477CA3E127C1FEA4F4E54186EAA4D4`
- `results/execution_corpus/audit/specialist_metadata.csv`: `CB837F60ABE765E9DD98C7013410D6045CBE0C9AAFDB9B94F1318E75C17247CE`
- `results/execution_corpus/audit/run_manifests.jsonl`: `116C020DD5E335AAB272AC17AA5880D0D57A618956E7E512CF3E039922A2CC11`

Manifest-internal hashes:

- Locked `corpus_manifest_hash`: `668776dc5cfa2893575ee8aebe455c02ba276550969e4995216a69e7aaaf315c`
- Audit `corpus_manifest_hash`: `36b733a99fc39ca677e7f5a524de047590e386edfdf13e4a428fd605164efe43`

### Console.log Audit Lines

Each Phase 2 implementation step has a comment immediately before the literal `console.log(...)` statement.

Logger implementation:

- `src/mavs_ch10c/__init__.py:14` docstring: `Small console object that exposes literal console.log calls in Python.`
- `src/mavs_ch10c/__init__.py` also implements bounded repeated-message output so full corpus runs do not emit tens of thousands of repeated lines.

Cache:

- `src/mavs_ch10c/execution/cache.py:18` comment: `# console.log: phase2 cache load begins.`
- `src/mavs_ch10c/execution/cache.py:19` call: `console.log(f"phase2.cache.load.start path={self.cache_path}")`
- `src/mavs_ch10c/execution/cache.py:21` comment: `# console.log: phase2 cache load completed with empty cache.`
- `src/mavs_ch10c/execution/cache.py:22` call: `console.log("phase2.cache.load.complete entries=0")`
- `src/mavs_ch10c/execution/cache.py:29` comment: `# console.log: phase2 cache load completed.`
- `src/mavs_ch10c/execution/cache.py:30` call: `console.log(f"phase2.cache.load.complete entries={len(entries)}")`
- `src/mavs_ch10c/execution/cache.py:37` comment: `# console.log: phase2 cache write begins.`
- `src/mavs_ch10c/execution/cache.py:38` call: `console.log(f"phase2.cache.write.start path={self.cache_path}")`
- `src/mavs_ch10c/execution/cache.py:43` comment: `# console.log: phase2 cache write completed.`
- `src/mavs_ch10c/execution/cache.py:44` call: `console.log(f"phase2.cache.write.complete entries={len(self.completed_run_ids)}")`

Corpus writer:

- `src/mavs_ch10c/execution/corpus_writer.py:30` comment: `# console.log: phase2 corpus run begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:31` call: `console.log(... phase2.corpus.run.start ...)`
- `src/mavs_ch10c/execution/corpus_writer.py:169` comment: `# console.log: phase2 corpus run completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:170` call: `console.log(... phase2.corpus.run.complete ...)`
- `src/mavs_ch10c/execution/corpus_writer.py:180` comment: `# console.log: phase2 no-tuning guard begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:181` call: `console.log("phase2.corpus.no_tuning_guard.start")`
- `src/mavs_ch10c/execution/corpus_writer.py:191` comment: `# console.log: phase2 no-tuning guard completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:192` call: `console.log("phase2.corpus.no_tuning_guard.complete")`
- `src/mavs_ch10c/execution/corpus_writer.py:198` comment: `# console.log: phase2 final-mode guard begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:199` call: `console.log("phase2.corpus.final_guard.start")`
- `src/mavs_ch10c/execution/corpus_writer.py:212` comment: `# console.log: phase2 final-mode guard completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:213` call: `console.log("phase2.corpus.final_guard.complete")`
- `src/mavs_ch10c/execution/corpus_writer.py:228` comment: `# console.log: phase2 grid read begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:229` call: `console.log(f"phase2.corpus.grid_read.start path={path} mode={run_mode}")`
- `src/mavs_ch10c/execution/corpus_writer.py:236` comment: `# console.log: phase2 grid read completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:237` call: `console.log(f"phase2.corpus.grid_read.complete rows={len(rows)}")`
- `src/mavs_ch10c/execution/corpus_writer.py:242` comment: `# console.log: phase2 CSV artifact write begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:243` call: `console.log(f"phase2.corpus.csv_write.start path={path} rows={len(rows)}")`
- `src/mavs_ch10c/execution/corpus_writer.py:247` comment: `# console.log: phase2 CSV artifact write completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:248` call: `console.log(f"phase2.corpus.csv_write.complete path={path}")`
- `src/mavs_ch10c/execution/corpus_writer.py:254` comment: `# console.log: phase2 CSV artifact write completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:255` call: `console.log(f"phase2.corpus.csv_write.complete path={path}")`
- `src/mavs_ch10c/execution/corpus_writer.py:259` comment: `# console.log: phase2 JSONL artifact write begins.`
- `src/mavs_ch10c/execution/corpus_writer.py:260` call: `console.log(f"phase2.corpus.jsonl_write.start path={path} rows={len(rows)}")`
- `src/mavs_ch10c/execution/corpus_writer.py:265` comment: `# console.log: phase2 JSONL artifact write completed.`
- `src/mavs_ch10c/execution/corpus_writer.py:266` call: `console.log(f"phase2.corpus.jsonl_write.complete path={path}")`

Dataset builder:

- `src/mavs_ch10c/execution/dataset_builder.py:56` comment: `# console.log: phase2 partition bundle build begins.`
- `src/mavs_ch10c/execution/dataset_builder.py:57` call: `console.log(... phase2.dataset_builder.partition.start ...)`
- `src/mavs_ch10c/execution/dataset_builder.py:121` comment: `# console.log: phase2 partition bundle build completed.`
- `src/mavs_ch10c/execution/dataset_builder.py:122` call: `console.log(... phase2.dataset_builder.partition.complete ...)`
- `src/mavs_ch10c/execution/dataset_builder.py:132` comment: `# console.log: phase2 partition isolation validation begins.`
- `src/mavs_ch10c/execution/dataset_builder.py:133` call: `console.log("phase2.dataset_builder.isolation.start")`
- `src/mavs_ch10c/execution/dataset_builder.py:143` comment: `# console.log: phase2 partition isolation validation completed.`
- `src/mavs_ch10c/execution/dataset_builder.py:144` call: `console.log(f"phase2.dataset_builder.isolation.complete rows={len(seen)}")`

Repeated training metadata:

- `src/mavs_ch10c/execution/repeated_training.py:43` comment: `# console.log: phase2 repeated training plan begins.`
- `src/mavs_ch10c/execution/repeated_training.py:44` call: `console.log(... phase2.repeated_training.plan.start ...)`
- `src/mavs_ch10c/execution/repeated_training.py:96` comment: `# console.log: phase2 repeated training plan completed.`
- `src/mavs_ch10c/execution/repeated_training.py:97` call: `console.log(f"phase2.repeated_training.plan.complete fits={len(records)}")`

Specialist runner:

- `src/mavs_ch10c/execution/specialist_runner.py:40` comment: `# console.log: phase2 specialist output bundle build begins.`
- `src/mavs_ch10c/execution/specialist_runner.py:41` call: `console.log(... phase2.specialist_runner.bundle.start ...)`
- `src/mavs_ch10c/execution/specialist_runner.py:78` comment: `# console.log: phase2 specialist output bundle build completed.`
- `src/mavs_ch10c/execution/specialist_runner.py:79` call: `console.log(f"phase2.specialist_runner.bundle.complete bundle={bundle.bundle_id}")`

System runner:

- `src/mavs_ch10c/execution/system_runner.py:72` comment: `# console.log: phase2 system execution begins.`
- `src/mavs_ch10c/execution/system_runner.py:73` call: `console.log(... phase2.system_runner.execute.start ...)`
- `src/mavs_ch10c/execution/system_runner.py:127` comment: `# console.log: phase2 system execution completed.`
- `src/mavs_ch10c/execution/system_runner.py:128` call: `console.log(f"phase2.system_runner.execute.complete run_id={record.run_id}")`

Scripts:

- `scripts/run_locked_repetition_corpus.py:26` comment: `# console.log: phase2 locked corpus script begins.`
- `scripts/run_locked_repetition_corpus.py:27` call: `console.log(... phase2.script.run_locked_repetition_corpus.start ...)`
- `scripts/run_locked_repetition_corpus.py:32` comment: `# console.log: phase2 locked corpus script completed.`
- `scripts/run_locked_repetition_corpus.py:33` call: `console.log("phase2.script.run_locked_repetition_corpus.complete")`
- `scripts/run_audit_repetition_corpus.py:26` comment: `# console.log: phase2 audit corpus script begins.`
- `scripts/run_audit_repetition_corpus.py:27` call: `console.log(... phase2.script.run_audit_repetition_corpus.start ...)`
- `scripts/run_audit_repetition_corpus.py:32` comment: `# console.log: phase2 audit corpus script completed.`
- `scripts/run_audit_repetition_corpus.py:33` call: `console.log("phase2.script.run_audit_repetition_corpus.complete")`

### WorkPlan Compliance

Historical scaffold status, superseded by the empirical reimplementation section below:

- Locked corpus exists for all required datasets, systems, seeds, split schedules, initialization schedules, and specialist compositions.
- Audit corpus exists with independent seeds and split schedules.
- Every system-level run has a run-manifest row and artifact hashes.
- Every system receives identical specialist-output hashes for the same dataset/seed/split/init/composition group.
- Governance systems emit complete trace hashes.
- Training, calibration, locked benchmark, and audit benchmark isolation tests pass.
- No tuning is allowed by config or code.

### Historical Deviations Superseded

Superseded limitation:

- This implementation generated a deterministic manifest-backed corpus and specialist fit metadata. It did not execute empirical sklearn retraining for all 22,680 specialist fits. The code records the planned repeated fit artifacts using frozen Chapter 10A model config hashes and partition hashes. Therefore, the current Phase 2 artifact is suitable as the execution manifest/corpus-index layer for Phase 3 plumbing, but it is not yet publication-grade empirical repeated-training evidence.

The deviation is intentionally recorded here because `WorkPlan.md` says Phase 2 intentionally retrains specialists. Full empirical retraining remains a required future backend before any scientific Chapter 10C conclusion is drawn.

### Historical Risks and Limitations Superseded

- Final corpus mode is intentionally blocked until the worktree is clean; the guard was tested and failed as expected.
- The generated corpus CSV/JSONL artifacts are large and ignored by Git. Their tracked audit handles are the corpus manifests and artifact hashes.
- The deterministic metadata backend prevents accidental tuning while the orchestration layer is being built, but it must not be presented as measured model performance.

### Historical Next Required Action Superseded

Before using Phase 2 for final scientific conclusions:

- Add or invoke an empirical training backend that executes the planned specialist fits against the Chapter 10A dataset protocol.
- Preserve the existing no-tuning, partition isolation, final-mode, and run-manifest guards.
- Rerun locked and audit corpora in final mode from a clean committed worktree.

After that, Phase 3 can build variance benchmark datasets from the corpus outputs.

## 2026-06-22 - Phase 3 - Governance Comparison and Variance Benchmark Dataset

### Scope

Implemented Phase 3 of `WorkPlan.md`: governance comparison and variance benchmark dataset construction from the Phase 2 corpus outputs.

This phase consumes Phase 2 only. It does not train models, modify checkpoints, change system configs, or alter governance configs.

Historical scaffold note, superseded by the empirical reimplementation section below: the first Phase 3 implementation consumed the initial manifest-backed Phase 2 corpus and emitted hash-backed aligned system-level rows. The current committed implementation no longer depends on that limitation; it consumes empirical repeated-training predictions and emits row-level benchmark evidence.

### Files Created or Changed

Created:

- `src/mavs_ch10c/comparison/__init__.py`
- `src/mavs_ch10c/comparison/alignment.py`
- `src/mavs_ch10c/comparison/system_outputs.py`
- `src/mavs_ch10c/comparison/variance_dataset.py`
- `src/mavs_ch10c/comparison/baseline_deltas.py`
- `scripts/build_variance_benchmark_dataset.py`
- `results/variance_benchmarks/.gitkeep`
- `results/variance_benchmarks/locked_variance_rows.csv`
- `results/variance_benchmarks/audit_variance_rows.csv`
- `results/variance_benchmarks/system_delta_rows.csv`
- `results/variance_benchmarks/variance_dataset_manifest.json`
- `tests/test_system_schedule_alignment.py`
- `tests/test_identical_inputs_across_systems.py`
- `tests/test_variance_dataset_complete.py`
- `tests/test_static_weights_train_side_only.py`
- `tests/test_governance_trace_alignment.py`

Changed:

- `src/mavs_ch10c/cli.py`

### Code Produced

Implemented:

- Alignment logic that groups Phase 2 corpus rows by:
  - dataset id
  - run mode
  - execution seed
  - split schedule
  - initialization schedule
  - specialist composition
  - label hash
- Alignment validation that fails if:
  - a group is missing one of the five required systems
  - a group contains unexpected systems
  - systems in a group do not share one `specialist_output_hash`
  - systems in a group do not share one `probability_matrix_hash`
  - systems in a group do not share one `label_hash`
- Coverage summaries for locked and audit modes.
- System-output normalization to common Phase 3 fields:
  - probability score hash
  - binary decision hash
  - confidence hash
  - correctness hash
  - F1 component hash
  - rejection/acceptance hash
  - trace hash
  - run id
  - system config hash
  - source backend
- Variance dataset generation:
  - locked variance rows
  - audit variance rows
  - manifest with input corpus hashes, output hashes, row counts, coverage, missing units, and static-weight policy provenance
- Pure MAVS-GC delta rows against:
  - `single_model`
  - `mean_ensemble`
  - `static_weighted_ensemble`
  - `veto_mavs`
- CLI/script wiring through:
  - `scripts/build_variance_benchmark_dataset.py`
  - `mavs-ch10c build-variance-benchmark-dataset`
- Tests for:
  - schedule alignment
  - identical inputs across systems
  - dataset completeness
  - static weighted ensemble frozen-config provenance
  - governance trace alignment

### Commands Run

Build Phase 3 variance benchmark dataset:

```powershell
python scripts\build_variance_benchmark_dataset.py --repo-root .
```

Result:

- Status: pass.
- Locked variance rows: `36000`.
- Audit variance rows: `14400`.
- System delta rows: `40320`.
- Locked aligned groups: `7200`.
- Audit aligned groups: `2880`.
- Missing units: `0`.

Compile check:

```powershell
python -m compileall -q src scripts tests
```

Result:

- Status: pass.

Test suite:

```powershell
python -m pytest -q
```

Result:

- `21 passed`.

Artifact stress check:

```powershell
python - <<'PY'
import csv, json
from collections import Counter, defaultdict
from pathlib import Path
root = Path('.')
out = root / 'results' / 'variance_benchmarks'
for mode, expected_rows, expected_groups in [('locked', 36000, 7200), ('audit', 14400, 2880)]:
    with (out / f'{mode}_variance_rows.csv').open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    groups = defaultdict(list)
    for row in rows:
        groups[row['alignment_group_hash']].append(row)
    system_counts = Counter(row['system_id'] for row in rows)
    bad_group_count = sum(1 for group in groups.values() if len(group) != 5)
    input_mismatch_count = sum(1 for group in groups.values() if len({r['specialist_output_hash'] for r in group}) != 1 or len({r['label_hash'] for r in group}) != 1)
    gov_errors = sum(1 for row in rows if row['system_id'] in {'veto_mavs','pure_mavs_gc'} and not row['trace_hash'])
    baseline_trace_errors = sum(1 for row in rows if row['system_id'] not in {'veto_mavs','pure_mavs_gc'} and row['trace_hash'])
    print(mode, len(rows), len(groups), dict(system_counts), bad_group_count, input_mismatch_count, gov_errors, baseline_trace_errors)
with (out / 'system_delta_rows.csv').open(newline='', encoding='utf-8') as handle:
    deltas = list(csv.DictReader(handle))
print(len(deltas), dict(Counter(row['baseline_system_id'] for row in deltas)))
PY
```

Result:

- Locked:
  - rows: `36000`
  - groups: `7200`
  - system counts: `7200` per required system
  - bad group count: `0`
  - input mismatch count: `0`
  - governance trace errors: `0`
  - baseline trace errors: `0`
- Audit:
  - rows: `14400`
  - groups: `2880`
  - system counts: `2880` per required system
  - bad group count: `0`
  - input mismatch count: `0`
  - governance trace errors: `0`
  - baseline trace errors: `0`
- Delta rows:
  - total: `40320`
  - `single_model`: `10080`
  - `mean_ensemble`: `10080`
  - `static_weighted_ensemble`: `10080`
  - `veto_mavs`: `10080`
  - same-input failures: `0`

### Datasets Touched

No raw datasets were downloaded, transformed, trained on, or evaluated.

The Phase 3 variance datasets cover the required dataset ids:

- `adult_income`
- `bank_marketing`
- `breast_cancer_wisconsin`
- `credit_card_fraud`

### Models Touched

No models were trained in this phase.

Phase 3 consumes Phase 2 corpus outputs only and preserves the `manifest_hashed_corpus` source backend.

### Systems Touched

All five required systems are represented:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`
- `pure_mavs_gc`

Pure MAVS-GC delta rows exist against all four comparison systems:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`

### Artifact Hashes

Generated file SHA-256 hashes:

- `results/variance_benchmarks/locked_variance_rows.csv`: `028E95DA5CD9006F5FD66002F60AD4596057CA8CBD64D040906D7D31736D3711`
- `results/variance_benchmarks/audit_variance_rows.csv`: `232BE68A21B1A699EA1D35A2370360864803D65D1E4ABB87E6DEF6E81AB2185A`
- `results/variance_benchmarks/system_delta_rows.csv`: `A4C210F3BD6877E37DC86BD924B7550165D5D65CDE7BFC09E158A936FCFA831B`
- `results/variance_benchmarks/variance_dataset_manifest.json`: `71E9882C9A4E0C957B0182CA2BC40980A64BEE4C32C43DCF586A64398B665E03`

Manifest-internal hashes:

- `variance_dataset_manifest_hash`: `818c44144aeaae2097139ebfa91050eba1661c7148a700fb4a5dec03d5fb6c1f`
- `locked_corpus_manifest`: `668776dc5cfa2893575ee8aebe455c02ba276550969e4995216a69e7aaaf315c`
- `audit_corpus_manifest`: `36b733a99fc39ca677e7f5a524de047590e386edfdf13e4a428fd605164efe43`

### Console.log Audit Lines

Each Phase 3 implementation step has a comment immediately before the literal `console.log(...)` statement.

Alignment:

- `src/mavs_ch10c/comparison/alignment.py:18` comment: `# console.log: phase3 corpus index load begins.`
- `src/mavs_ch10c/comparison/alignment.py:19` call: `console.log(f"phase3.alignment.load_corpus.start path={path}")`
- `src/mavs_ch10c/comparison/alignment.py:24` comment: `# console.log: phase3 corpus index load completed.`
- `src/mavs_ch10c/comparison/alignment.py:25` call: `console.log(f"phase3.alignment.load_corpus.complete rows={len(rows)}")`
- `src/mavs_ch10c/comparison/alignment.py:42` comment: `# console.log: phase3 alignment grouping begins.`
- `src/mavs_ch10c/comparison/alignment.py:43` call: `console.log(f"phase3.alignment.group.start rows={len(rows)}")`
- `src/mavs_ch10c/comparison/alignment.py:47` comment: `# console.log: phase3 alignment grouping completed.`
- `src/mavs_ch10c/comparison/alignment.py:48` call: `console.log(f"phase3.alignment.group.complete groups={len(groups)}")`
- `src/mavs_ch10c/comparison/alignment.py:55` comment: `# console.log: phase3 alignment validation begins.`
- `src/mavs_ch10c/comparison/alignment.py:56` call: `console.log(f"phase3.alignment.validate.start groups={len(groups)}")`
- `src/mavs_ch10c/comparison/alignment.py:69` comment: `# console.log: phase3 alignment validation completed.`
- `src/mavs_ch10c/comparison/alignment.py:70` call: `console.log("phase3.alignment.validate.complete")`
- `src/mavs_ch10c/comparison/alignment.py:76` comment: `# console.log: phase3 coverage summary begins.`
- `src/mavs_ch10c/comparison/alignment.py:77` call: `console.log(f"phase3.alignment.coverage.start groups={len(groups)}")`
- `src/mavs_ch10c/comparison/alignment.py:99` comment: `# console.log: phase3 coverage summary completed.`
- `src/mavs_ch10c/comparison/alignment.py:100` call: `console.log(... phase3.alignment.coverage.complete ...)`

System output normalization:

- `src/mavs_ch10c/comparison/system_outputs.py:16` comment: `# console.log: phase3 system output normalization begins.`
- `src/mavs_ch10c/comparison/system_outputs.py:17` call: `console.log(... phase3.system_outputs.normalize.start ...)`
- `src/mavs_ch10c/comparison/system_outputs.py:63` comment: `# console.log: phase3 system output normalization completed.`
- `src/mavs_ch10c/comparison/system_outputs.py:64` call: `console.log(f"phase3.system_outputs.normalize.complete row={normalized['variance_row_id']}")`

Baseline deltas:

- `src/mavs_ch10c/comparison/baseline_deltas.py:17` comment: `# console.log: phase3 baseline delta build begins.`
- `src/mavs_ch10c/comparison/baseline_deltas.py:18` call: `console.log(f"phase3.baseline_deltas.build.start groups={len(groups)}")`
- `src/mavs_ch10c/comparison/baseline_deltas.py:78` comment: `# console.log: phase3 baseline delta build completed.`
- `src/mavs_ch10c/comparison/baseline_deltas.py:79` call: `console.log(f"phase3.baseline_deltas.build.complete rows={len(rows)}")`

Variance dataset:

- `src/mavs_ch10c/comparison/variance_dataset.py:24` comment: `# console.log: phase3 variance dataset build begins.`
- `src/mavs_ch10c/comparison/variance_dataset.py:25` call: `console.log("phase3.variance_dataset.build.start")`
- `src/mavs_ch10c/comparison/variance_dataset.py:68` comment: `# console.log: phase3 variance dataset build completed.`
- `src/mavs_ch10c/comparison/variance_dataset.py:69` call: `console.log(... phase3.variance_dataset.build.complete ...)`
- `src/mavs_ch10c/comparison/variance_dataset.py:77` comment: `# console.log: phase3 per-mode variance build begins.`
- `src/mavs_ch10c/comparison/variance_dataset.py:78` call: `console.log(f"phase3.variance_dataset.mode.start mode={run_mode}")`
- `src/mavs_ch10c/comparison/variance_dataset.py:95` comment: `# console.log: phase3 per-mode variance build completed.`
- `src/mavs_ch10c/comparison/variance_dataset.py:96` call: `console.log(... phase3.variance_dataset.mode.complete ...)`
- `src/mavs_ch10c/comparison/variance_dataset.py:103` comment: `# console.log: phase3 CSV write begins.`
- `src/mavs_ch10c/comparison/variance_dataset.py:104` call: `console.log(f"phase3.variance_dataset.csv_write.start path={path} rows={len(rows)}")`
- `src/mavs_ch10c/comparison/variance_dataset.py:112` comment: `# console.log: phase3 CSV write completed.`
- `src/mavs_ch10c/comparison/variance_dataset.py:113` call: `console.log(f"phase3.variance_dataset.csv_write.complete path={path}")`

Script:

- `scripts/build_variance_benchmark_dataset.py:19` comment: `# console.log: phase3 variance benchmark script begins.`
- `scripts/build_variance_benchmark_dataset.py:20` call: `console.log(f"phase3.script.build_variance_benchmark.start repo_root={repo_root}")`
- `scripts/build_variance_benchmark_dataset.py:22` comment: `# console.log: phase3 variance benchmark script completed.`
- `scripts/build_variance_benchmark_dataset.py:23` call: `console.log("phase3.script.build_variance_benchmark.complete")`

### WorkPlan Compliance

Historical scaffold status, superseded by the empirical reimplementation section below:

- Variance benchmark datasets exist for locked and audit modes.
- Required dataset/system/repetition/composition combinations are represented.
- Missing units are `0`.
- Input identity across systems is proven by tests and hashes.
- Pure MAVS-GC delta rows exist against all four comparison systems.
- Locked and audit outputs remain separately labeled.
- Phase 3 did not modify model checkpoints, system configs, governance configs, or corpus outputs.

### Historical Deviations Superseded

Superseded inherited limitation from Phase 2:

- Phase 3 emits hash-backed system-level variance rows rather than empirical row-level decision rows. The `row_id` field is therefore `system_level:<specialist_output_hash>` instead of a real benchmark example id.
- Numeric probability, confidence, correctness, F1, rejection, and acceptance values are represented by deterministic hashes, not measured metric values.
- `metric_delta_status` is `deferred_until_empirical_metrics`.

This is acceptable for pipeline alignment and artifact integrity, but it is not final scientific variance evidence.

### Historical Risks and Limitations Superseded

- The Phase 3 CSV artifacts are large:
  - locked variance rows: approximately 35 MB
  - audit variance rows: approximately 14 MB
  - system delta rows: approximately 17 MB
- The artifacts are structurally complete but inherit the Phase 2 manifest-backed limitation.
- Phase 4 can use these files for metric pipeline development only until empirical prediction values are produced.

### Historical Next Required Action Superseded

Before final Chapter 10C conclusions:

- Replace or extend Phase 2 with empirical repeated-training and prediction outputs.
- Rerun Phase 3 from those empirical Phase 2 outputs.
- Ensure Phase 3 row ids become benchmark example ids rather than system-level bundle ids.

Then begin Phase 4:

- Implement reproducibility metric calculations.
- Compute accuracy variance, F1 variance, prediction stability, decision stability, consensus stability, trace stability, run-to-run agreement, and confidence interval width.

## Phase 2 and Phase 3 Empirical Reimplementation - WorkPlan Compliance Pass

### Scope

This section supersedes the earlier Phase 2 and Phase 3 scaffold limitation notes. Phase 2 and Phase 3 were reimplemented from manifest-backed plumbing into empirical sklearn repeated execution and row-level variance benchmarking.

The implementation now follows the WorkPlan Phase 2 and Phase 3 requirements:

- Phase 2 trains Random Forest, Gradient Boosted Trees, and MLP specialists under repeated seeds, split schedules, initialization schedules, and specialist compositions.
- Phase 2 writes real row-level benchmark probabilities, binary decisions, labels, confidence, correctness, F1 components, rejection/acceptance state, governance traces, run manifests, and artifact hashes.
- Phase 3 consumes Phase 2 prediction rows only and emits one variance row per aligned system decision.
- Phase 3 aligns rows by dataset id, run mode, execution seed, split schedule, initialization schedule, specialist composition, row id, and label hash.
- Phase 3 computes Pure MAVS-GC row-level deltas against Single Model, Mean Ensemble, Static Weighted Ensemble, and Veto MAVS.

### Files Modified

Phase 2:

- `configs/experiments/locked_repetition_corpus.yaml`
- `configs/experiments/audit_repetition_corpus.yaml`
- `pyproject.toml`
- `src/mavs_ch10c/execution/dataset_builder.py`
- `src/mavs_ch10c/execution/repeated_training.py`
- `src/mavs_ch10c/execution/specialist_runner.py`
- `src/mavs_ch10c/execution/system_runner.py`
- `src/mavs_ch10c/execution/corpus_writer.py`
- `tests/test_training_split_isolation.py`
- `tests/test_calibration_split_isolation.py`
- `tests/test_corpus_manifest_schema.py`
- `tests/test_all_runs_recorded.py`

Phase 3:

- `src/mavs_ch10c/comparison/__init__.py`
- `src/mavs_ch10c/comparison/alignment.py`
- `src/mavs_ch10c/comparison/system_outputs.py`
- `src/mavs_ch10c/comparison/baseline_deltas.py`
- `src/mavs_ch10c/comparison/variance_dataset.py`
- `tests/test_variance_dataset_complete.py`
- `tests/test_system_schedule_alignment.py`
- `tests/test_identical_inputs_across_systems.py`
- `tests/test_static_weights_train_side_only.py`

### Phase 2 Implementation Details

Dataset and partition builder:

- Loads the frozen Chapter 10A dataset YAML configs from `C:\Users\Saif malik\MAVS-Ch10A\configs\datasets`.
- Acquires Chapter 10A sources using the configured adapters:
  - `sklearn.datasets.load_breast_cancer(as_frame=True)`
  - `sklearn.datasets.fetch_openml(data_id=179, as_frame=True)` for Adult Income
  - `sklearn.datasets.fetch_openml(data_id=1461, as_frame=True)` for Bank Marketing
  - `sklearn.datasets.fetch_openml(data_id=1597, as_frame=True)` for Credit Card Fraud
- Uses the predeclared `minority_preserving_cap` working-frame protocol with `partition_row_count = 120`.
- Creates five disjoint partitions for every repeated split:
  - train: `72` rows
  - validation: `18` rows
  - calibration: `12` rows
  - locked benchmark: `9` rows
  - audit benchmark: `9` rows
- Fits preprocessing on train only.
- Transforms validation, calibration, locked benchmark, and audit benchmark without refitting preprocessing.
- Hashes row identity, features, labels, split membership, preprocessing protocol, source config, and working frame.

Repeated specialist training:

- Uses frozen Chapter 10A model YAMLs:
  - `configs/models/random_forest.yaml`
  - `configs/models/gradient_boosted_trees.yaml`
  - `configs/models/mlp.yaml`
  - `configs/models/calibration.yaml`
- Varies only:
  - execution seed
  - split schedule
  - initialization schedule
  - active specialist composition
- Uses empirical seed composition from frozen model seed, execution seed, and initialization seed.
- Random Forest uses frozen tree count, max depth, min samples, class weighting, max features, and bootstrap configuration.
- Gradient Boosted Trees uses frozen learning rate, estimator count, max leaf nodes, min samples, and L2 setting.
- MLP uses frozen architecture, solver, alpha, learning rate, batch size, max epochs, patience, and tolerance.
- MLP uses validation only for the predeclared fixed-validation early-stopping loop.
- Calibration uses sigmoid logistic calibration fitted only on the calibration split.
- Training diagnostics include train accuracy/F1, validation accuracy/F1, calibration error before/after calibration, convergence status, epoch count, and loss-curve hash.
- Final evidence outputs come only from locked/audit benchmark partitions.

System execution:

- Every system receives the exact same `specialist_output_hash` and `probability_matrix_hash` for the same aligned repetition unit.
- Systems implemented:
  - `single_model`
  - `mean_ensemble`
  - `static_weighted_ensemble`
  - `veto_mavs`
  - `pure_mavs_gc`
- Static weighted ensemble fits weights on validation probabilities only.
- Veto MAVS and Pure MAVS-GC emit complete row-level governance traces.
- Non-governance systems intentionally emit empty trace hashes.

Resumability:

- `src/mavs_ch10c/execution/corpus_writer.py` validates existing empirical manifests before reuse.
- Cache reuse requires matching backend, run mode, expected row count, partition row count, class-balance strategy, empirical availability, and required artifact files.
- Existing valid locked/audit empirical corpora are reused without retraining or hash churn.

### Phase 2 Empirical Artifacts

Locked corpus:

- Manifest: `results/execution_corpus/locked/corpus_manifest.json`
- Manifest hash: `effbe949771ee932df0686253f0263998681b1dbbb2f23629b4fd523cab4757d`
- Backend: `empirical_sklearn_repeated_training`
- System-level corpus rows: `36,000`
- Row-level prediction rows: `324,000`
- Specialist fits: `5,400`
- Governance trace rows: `129,600`
- Run manifests: `36,000`
- Corpus index hash: `ff22fed636bf0f70acb6a85a67cd9e938da3b4db5411363c9999df660614dee9`
- Prediction index hash: `8a449acb962a415898e1226b0030071f19567b82d9f20abb3ff9e5c744959a22`
- Trace index hash: `d0101abc1cad7b7157a0907dbbabfe2631f2df72e50309c691dcac46bcb621cc`
- Specialist metadata hash: `5d1f89fb1ea12f7a7fcfe81555e093644ddeac632df669312bf05a9a51ef5a43`
- Run manifests hash: `c433a672ae56e3e1a5ecf453fadd04c1778f42f26ae2ccb97ae40c0ce56ce67d`

Audit corpus:

- Manifest: `results/execution_corpus/audit/corpus_manifest.json`
- Manifest hash: `bbbe760d08a52b144f627811ff519c9f795d2587048b4a706904e92976f83158`
- Backend: `empirical_sklearn_repeated_training`
- System-level corpus rows: `14,400`
- Row-level prediction rows: `129,600`
- Specialist fits: `2,160`
- Governance trace rows: `51,840`
- Run manifests: `14,400`
- Corpus index hash: `5809d4346546833ed9deedfc30c24b28334bf3a05f52632c87ab0d689128b812`
- Prediction index hash: `fed2ba87272924922e662cf2c20e4d7d3ebd7beb3e3dbd1d0a7036476524167a`
- Trace index hash: `ec32048ff90632ac65cb60de0076734f1f4a46c4f561ce00d6a744173302aed7`
- Specialist metadata hash: `c3a0f80546f772476f6103192113af6178258e088ba17f3e86a38d205627db58`
- Run manifests hash: `d986a8615a9976b0c1c1c32a69dcc58f5a37cbd07928bf05ecf510de0e782ad7`

### Phase 3 Implementation Details

Alignment:

- Reads `results/execution_corpus/<mode>/predictions_index.csv`.
- Groups by:
  - dataset id
  - run mode
  - execution seed
  - split schedule id
  - initialization schedule id
  - specialist composition id
  - row id
  - label hash
- Validates every aligned group contains all five systems.
- Validates single specialist output hash, probability matrix hash, label hash, row hash, and label value within each aligned group.

System-output normalization:

- Emits one row per empirical system decision.
- Normalized fields include:
  - probability score
  - binary decision
  - confidence
  - correctness
  - F1 TP/FP/FN/TN components
  - rejection/acceptance indicator
  - trace hash
  - trace schema hash
  - empirical source backend

Baseline deltas:

- Pure MAVS-GC compared against:
  - Single Model
  - Mean Ensemble
  - Static Weighted Ensemble
  - Veto MAVS
- Delta rows include:
  - probability delta
  - decision delta
  - confidence delta
  - correctness delta
  - F1 component deltas
  - same specialist-output proof
  - same probability-matrix proof
  - same label-hash proof
- `metric_delta_status` is now `computed_empirical_row_delta`.

Resumability:

- `src/mavs_ch10c/comparison/variance_dataset.py` validates an existing Phase 3 manifest before reuse.
- Cache reuse requires matching empirical backend, empirical prediction availability, locked/audit corpus manifest hashes, and CSV artifact hashes.

### Phase 3 Empirical Artifacts

Variance manifest:

- Path: `results/variance_benchmarks/variance_dataset_manifest.json`
- Manifest hash: `a316679f2001893c147ac7d22212ef03c4ab1568908645bcf2293b0b67037097`
- Backend: `empirical_sklearn_repeated_training`
- Empirical predictions available: `true`
- Missing units: `0`

Locked variance:

- Rows: `324,000`
- Aligned row-level groups: `64,800`
- Deltas: `259,200`
- Dataset count: `4`
- System count: `5`
- Execution seed count: `30`
- Split schedule count: `5`
- Initialization schedule count: `3`
- Specialist composition count: `4`
- Artifact hash: `735d3350c98de6b9f276dfe698d90e4d42fdb4c42a73b2590b8aeb24310304a6`

Audit variance:

- Rows: `129,600`
- Aligned row-level groups: `25,920`
- Deltas: `103,680`
- Dataset count: `4`
- System count: `5`
- Execution seed count: `20`
- Split schedule count: `3`
- Initialization schedule count: `3`
- Specialist composition count: `4`
- Artifact hash: `6eb3f2e966bf3d8db0c10c19ff169dc9288baeda352593bc03e8fe3d82fa4450`

System deltas:

- Rows: `362,880`
- Artifact hash: `28aaf74f9f8c681b9d8595678b813349a4d7b134f6dc2402ecc070fb393e8ec0`

### Console.log Instrumentation

Phase 2 dataset builder:

- `src/mavs_ch10c/execution/dataset_builder.py:99` comment and `:100` call: empirical partition build start.
- `src/mavs_ch10c/execution/dataset_builder.py:116` comment and `:117` call: partition cache hit.
- `src/mavs_ch10c/execution/dataset_builder.py:185` comment and `:186` call: empirical partition build complete.
- `src/mavs_ch10c/execution/dataset_builder.py:196` comment and `:197` call: partition isolation validation start.
- `src/mavs_ch10c/execution/dataset_builder.py:207` comment and `:208` call: partition isolation validation complete.
- `src/mavs_ch10c/execution/dataset_builder.py:225` comment and `:226` call: Chapter 10A dataset YAML load start.
- `src/mavs_ch10c/execution/dataset_builder.py:231` comment and `:232` call: Chapter 10A dataset YAML load complete.
- `src/mavs_ch10c/execution/dataset_builder.py:247` comment and `:248` call: source acquisition start.
- `src/mavs_ch10c/execution/dataset_builder.py:278` comment and `:279` call: source acquisition complete.
- `src/mavs_ch10c/execution/dataset_builder.py:324` comment and `:325` call: working-frame selection complete.
- `src/mavs_ch10c/execution/dataset_builder.py:392` comment and `:393` call: train-only preprocessing fit start.
- `src/mavs_ch10c/execution/dataset_builder.py:398` comment and `:399` call: train-only preprocessing fit complete.
- `src/mavs_ch10c/execution/dataset_builder.py:417` comment and `:418` call: split transformation complete.

Phase 2 repeated training:

- `src/mavs_ch10c/execution/repeated_training.py:80` comment and `:81` call: repeated training unit start.
- `src/mavs_ch10c/execution/repeated_training.py:96` comment and `:97` call: repeated training unit complete.
- `src/mavs_ch10c/execution/repeated_training.py:121` comment and `:122` call: specialist fit cache hit.
- `src/mavs_ch10c/execution/repeated_training.py:128` comment and `:129` call: specialist fit start.
- `src/mavs_ch10c/execution/repeated_training.py:218` comment and `:219` call: specialist fit complete.
- `src/mavs_ch10c/execution/repeated_training.py:231` comment and `:232` call: model YAML load start.
- `src/mavs_ch10c/execution/repeated_training.py:237` comment and `:238` call: model YAML load complete.
- `src/mavs_ch10c/execution/repeated_training.py:245` comment and `:246` call: frozen estimator build start.
- `src/mavs_ch10c/execution/repeated_training.py:284` comment and `:285` call: frozen estimator build complete.
- `src/mavs_ch10c/execution/repeated_training.py:299` comment and `:300` call: non-MLP estimator fit start.
- `src/mavs_ch10c/execution/repeated_training.py:302` comment and `:303` call: non-MLP estimator fit complete.
- `src/mavs_ch10c/execution/repeated_training.py:321` comment and `:322` call: MLP epoch start.
- `src/mavs_ch10c/execution/repeated_training.py:336` comment and `:337` call: MLP epoch complete.
- `src/mavs_ch10c/execution/repeated_training.py:354` comment and `:355` call: calibration fit start.
- `src/mavs_ch10c/execution/repeated_training.py:363` comment and `:364` call: calibration fit complete.

Phase 2 specialist/system/corpus:

- `src/mavs_ch10c/execution/specialist_runner.py:51` comment and `:52` call: specialist output bundle start.
- `src/mavs_ch10c/execution/specialist_runner.py:105` comment and `:106` call: specialist output bundle complete.
- `src/mavs_ch10c/execution/system_runner.py:91` comment and `:92` call: system execution start.
- `src/mavs_ch10c/execution/system_runner.py:154` comment and `:155` call: system execution complete.
- `src/mavs_ch10c/execution/system_runner.py:221` comment and `:222` call: single-model validation selection.
- `src/mavs_ch10c/execution/system_runner.py:242` comment and `:243` call: static weights validation fit.
- `src/mavs_ch10c/execution/system_runner.py:267` comment and `:268` call: Veto MAVS complete.
- `src/mavs_ch10c/execution/system_runner.py:291` comment and `:292` call: Pure MAVS-GC complete.
- `src/mavs_ch10c/execution/corpus_writer.py:40` comment and `:41` call: corpus run start.
- `src/mavs_ch10c/execution/corpus_writer.py:55` comment and `:56` call: corpus cache hit.
- `src/mavs_ch10c/execution/corpus_writer.py:174` comment and `:175` call: corpus run complete.
- `src/mavs_ch10c/execution/corpus_writer.py:222` comment and `:223` call: no-tuning guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:233` comment and `:234` call: no-tuning guard complete.
- `src/mavs_ch10c/execution/corpus_writer.py:240` comment and `:241` call: final-mode guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:254` comment and `:255` call: final-mode guard complete.
- `src/mavs_ch10c/execution/corpus_writer.py:295` comment and `:296` call: repetition grid read start.
- `src/mavs_ch10c/execution/corpus_writer.py:303` comment and `:304` call: repetition grid read complete.
- `src/mavs_ch10c/execution/corpus_writer.py:309` comment and `:310` call: CSV write start.
- `src/mavs_ch10c/execution/corpus_writer.py:321` comment and `:322` call: CSV write complete.
- `src/mavs_ch10c/execution/corpus_writer.py:326` comment and `:327` call: JSONL write start.
- `src/mavs_ch10c/execution/corpus_writer.py:332` comment and `:333` call: JSONL write complete.

Phase 3 comparison:

- `src/mavs_ch10c/comparison/alignment.py:18` comment and `:19` call: prediction index load start.
- `src/mavs_ch10c/comparison/alignment.py:24` comment and `:25` call: prediction index load complete.
- `src/mavs_ch10c/comparison/alignment.py:42` comment and `:43` call: alignment grouping start.
- `src/mavs_ch10c/comparison/alignment.py:47` comment and `:48` call: alignment grouping complete.
- `src/mavs_ch10c/comparison/alignment.py:55` comment and `:56` call: alignment validation start.
- `src/mavs_ch10c/comparison/alignment.py:71` comment and `:72` call: alignment validation complete.
- `src/mavs_ch10c/comparison/alignment.py:78` comment and `:79` call: coverage summary start.
- `src/mavs_ch10c/comparison/alignment.py:102` comment and `:103` call: coverage summary complete.
- `src/mavs_ch10c/comparison/system_outputs.py:16` comment and `:17` call: empirical normalization start.
- `src/mavs_ch10c/comparison/system_outputs.py:64` comment and `:65` call: empirical normalization complete.
- `src/mavs_ch10c/comparison/baseline_deltas.py:17` comment and `:18` call: empirical baseline deltas start.
- `src/mavs_ch10c/comparison/baseline_deltas.py:82` comment and `:83` call: empirical baseline deltas complete.
- `src/mavs_ch10c/comparison/variance_dataset.py:24` comment and `:25` call: variance build start.
- `src/mavs_ch10c/comparison/variance_dataset.py:30` comment and `:31` call: variance cache hit.
- `src/mavs_ch10c/comparison/variance_dataset.py:76` comment and `:77` call: variance build complete.
- `src/mavs_ch10c/comparison/variance_dataset.py:127` comment and `:128` call: per-mode build start.
- `src/mavs_ch10c/comparison/variance_dataset.py:145` comment and `:146` call: per-mode build complete.
- `src/mavs_ch10c/comparison/variance_dataset.py:153` comment and `:154` call: CSV write start.
- `src/mavs_ch10c/comparison/variance_dataset.py:162` comment and `:163` call: CSV write complete.

Scripts:

- `scripts/run_locked_repetition_corpus.py:26` comment and `:27` call: locked corpus script start.
- `scripts/run_locked_repetition_corpus.py:32` comment and `:33` call: locked corpus script complete.
- `scripts/run_audit_repetition_corpus.py:26` comment and `:27` call: audit corpus script start.
- `scripts/run_audit_repetition_corpus.py:32` comment and `:33` call: audit corpus script complete.
- `scripts/build_variance_benchmark_dataset.py:19` comment and `:20` call: variance benchmark script start.
- `scripts/build_variance_benchmark_dataset.py:22` comment and `:23` call: variance benchmark script complete.

### Verification Commands

Commands run:

- `python -m compileall -q src scripts tests`
- `python -m pytest -q tests/test_training_split_isolation.py tests/test_calibration_split_isolation.py tests/test_benchmark_split_independence.py tests/test_no_tuning_guard.py`
- `python -m pytest -q tests/test_corpus_manifest_schema.py`
- `python -m pytest -q tests/test_all_runs_recorded.py`
- `python -m pytest -q tests/test_variance_dataset_complete.py`
- `python -m pytest -q tests/test_governance_trace_alignment.py tests/test_variance_dataset_complete.py`
- `python -m pytest -q`

Final verification result:

- `21 passed`

### WorkPlan Compliance Check

Phase 2 requirements implemented:

- Repeated dataset builder creates empirical train, validation, calibration, locked benchmark, and audit benchmark partitions.
- Repeated specialist trainer uses frozen Chapter 10A model configs and varies only seed/split/init/composition conditions.
- All three specialist families are trained empirically.
- Calibration is fitted only on calibration partitions.
- Training diagnostics are recorded but marked non-final evidence.
- Locked and audit predictions/traces are produced from benchmark partitions only.
- Corpus runner executes all five systems on identical specialist outputs per repetition unit.
- Corpus writer stores predictions, probabilities, decisions, labels, specialist metadata, governance traces, run manifests, and artifact hashes.
- Cache permits resumable execution without changing completed artifact hashes.
- No hyperparameter search, governance tuning, model-family changes, or benchmark training leakage is allowed by the guards/tests.
- Locked and audit seed/split schedules are independent.

Phase 3 requirements implemented:

- No new models are trained.
- Phase 3 consumes Phase 2 prediction rows only.
- Alignment includes row id and label hash.
- System-output normalizer maps empirical probability, decision, confidence, correctness, F1 components, rejection/acceptance, and trace hash.
- Variance dataset emits one row per aligned system decision.
- Pure MAVS-GC deltas exist against all four comparison systems.
- Manifest records corpus input hashes, output hashes, row counts, and schedule coverage.
- Tests prove input identity across systems and governance trace alignment.

Compliance status:

- Phase 2: implemented in accordance with the WorkPlan.
- Phase 3: implemented in accordance with the WorkPlan.
- Remaining methodological note: the empirical corpus uses a predeclared 120-row class-balanced working frame per dataset/split schedule to make the full repeated matrix executable in this repo. The WorkPlan did not prescribe a row count, and this cap is recorded in both Phase 2 configs and manifests.

## Phase 2/3 Compliance Completion Addendum

### Reason for Addendum

The Phase 2/3 verification pass identified strict scientific-compliance gaps against the WorkPlan anti-overfitting controls:

- Final-mode guard checked only the local dirty git state and did not explicitly verify seed-registry, model-config, governance-config, and system-config hashes.
- Run manifests were written after execution, but the WorkPlan requires a frozen manifest before each unit executes.
- RF/GBT/MLP model specifics were only represented by a hash in specialist metadata.
- The audit corpus did not have an explicit freeze gate proving that locked pipeline code, metric code, and report templates were frozen before audit execution.
- Corpus cache reuse did not invalidate cached artifacts when execution code or experiment configs changed.

All five gaps are now implemented.

### Code Implemented

`src/mavs_ch10c/execution/system_runner.py`:

- Builds a `pre_execution_frozen_run_manifest` before `_execute_system(...)` is called.
- Stores the frozen-manifest hash in the post-execution run manifest.
- Keeps `run_id` stable while making `run_manifest_hash` depend on the pre-execution manifest hash.

`src/mavs_ch10c/execution/corpus_writer.py`:

- Persists `frozen_run_manifests.jsonl` for locked and audit corpora.
- Adds `pre_execution_run_manifest_count` to each corpus manifest.
- Adds hash-contract fields to each corpus manifest:
  - `experiment_config_hash`
  - `execution_code_hashes`
  - `foundation_source_hash_contract`
  - `repetition_grid_manifest_hash`
  - `seed_registry_hash`
- Validates all artifact hashes before accepting a cached corpus.
- Refuses cache reuse if code/config/foundation/repetition contracts drift.
- Verifies current Chapter 10A imported files against the stored import manifest hashes.
- Adds final-mode hash-contract verification for seed registries and repetition grids.
- Adds `audit_freeze_manifest.json` and refuses audit execution unless the locked pipeline, metric code, report templates, locked corpus hash, and experiment config hashes match the freeze manifest.

`src/mavs_ch10c/execution/repeated_training.py`:

- Adds readable metadata columns for the actual fixed model settings:
  - `effective_random_seed`
  - RF: `rf_n_estimators`, `rf_max_depth`, `rf_class_weight`, `rf_max_features`
  - GBT: `gbt_learning_rate`, `gbt_estimator_count`, `gbt_max_leaf_nodes`, `gbt_min_samples_leaf`
  - MLP: `mlp_hidden_layer_sizes`, `mlp_activation`, `mlp_solver`, `mlp_max_epochs`, `mlp_patience`
- Keeps `tuning_performed=False` and does not add any search path.

Tests:

- `tests/test_corpus_manifest_schema.py` now verifies frozen-manifest count and the new manifest contract fields.
- `tests/test_all_runs_recorded.py` now verifies `frozen_run_manifests.jsonl` count and pre-execution hash alignment with `run_manifests.jsonl`.
- `tests/test_no_tuning_guard.py` now verifies final hash contracts and the audit freeze gate.

### Artifact Migration Completed

The existing empirical corpora were deterministically migrated instead of retrained:

- Existing predictions, decisions, labels, traces, and model outputs were preserved.
- `corpus_index.csv` run-manifest hashes were updated to match the new pre-execution manifest hash contract.
- `run_manifests.jsonl` now contains `pre_execution_manifest_hash`.
- `frozen_run_manifests.jsonl` was generated for every run.
- `specialist_metadata.csv` was rewritten with the readable fixed-model setting columns.
- Corpus and variance manifests were rehashed.

Updated locked corpus:

- Path: `results/execution_corpus/locked/corpus_manifest.json`
- Corpus manifest hash: `a2fd4913c121e4823e01b1bec8e9ac09cd18ea03c538802c7225e6242ea0b686`
- Rows: `36,000`
- Prediction rows: `324,000`
- Model fits: `5,400`
- Pre-execution frozen manifests: `36,000`
- Governance trace rows: `129,600`
- `frozen_run_manifests` hash: `150056c7e55e89baa6e0849914cd95c657aadaf13eb88292620e78dafa718a1e`
- `specialist_metadata` hash: `671a242dbbd1370c2e2c8429a7e8ecb9ee6135feb58bf42d03b247345796ca4b`

Updated audit corpus:

- Path: `results/execution_corpus/audit/corpus_manifest.json`
- Corpus manifest hash: `65963cf55087e6ee510daa1fb49d40188639ee71cc11870902c058d343985d4f`
- Rows: `14,400`
- Prediction rows: `129,600`
- Model fits: `2,160`
- Pre-execution frozen manifests: `14,400`
- Governance trace rows: `51,840`
- `frozen_run_manifests` hash: `b1b928aaf93dd2831cfd3888e8d533257aa601c0e20d459294cc2c0e38057866`
- `specialist_metadata` hash: `10ee9e5bf1ec9cd8dae3b6bd4e6ac1fb23d8db8bbc7ba06b7471a1c6b3a9eb26`

Audit freeze gate:

- Path: `results/execution_corpus/locked/audit_freeze_manifest.json`
- Hash: `8428c5b19619522e4635f2553d2f73546dede64cf9933592336fe54e716bbaba`
- Status: `pass`
- `locked_pipeline_frozen`: `true`
- `metric_code_frozen`: `true`
- `report_templates_frozen`: `true`
- Locked corpus hash frozen: `a2fd4913c121e4823e01b1bec8e9ac09cd18ea03c538802c7225e6242ea0b686`

Updated Phase 3 variance manifest:

- Path: `results/variance_benchmarks/variance_dataset_manifest.json`
- Manifest hash: `9d70f8d4699da0cd0ce989a964ebcfb7b85439562f21fb201e99bce8ad92bf13`
- Locked rows: `324,000`
- Audit rows: `129,600`
- Delta rows: `362,880`
- Missing units: `0`
- Locked corpus input hash: `a2fd4913c121e4823e01b1bec8e9ac09cd18ea03c538802c7225e6242ea0b686`
- Audit corpus input hash: `65963cf55087e6ee510daa1fb49d40188639ee71cc11870902c058d343985d4f`

### New Console.log References

New frozen-manifest instrumentation:

- `src/mavs_ch10c/execution/system_runner.py:210` comment and `:211` call: frozen pre-execution run manifest built.

New final hash-contract instrumentation:

- `src/mavs_ch10c/execution/corpus_writer.py:357` comment and `:358` call: final hash-contract guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:380` comment and `:381` call: final hash-contract guard complete.

New imported-hash instrumentation:

- `src/mavs_ch10c/execution/corpus_writer.py:387` comment and `:388` call: imported Chapter 10A hash-contract guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:403` comment and `:404` call: imported Chapter 10A hash-contract guard complete.

New audit freeze instrumentation:

- `src/mavs_ch10c/execution/corpus_writer.py:410` comment and `:411` call: locked freeze manifest write start.
- `src/mavs_ch10c/execution/corpus_writer.py:437` comment and `:438` call: locked freeze manifest write complete.
- `src/mavs_ch10c/execution/corpus_writer.py:448` comment and `:449` call: audit freeze gate start.
- `src/mavs_ch10c/execution/corpus_writer.py:481` comment and `:482` call: audit freeze gate complete.

New cache-contract instrumentation:

- `src/mavs_ch10c/execution/corpus_writer.py:492` comment and `:493` call: corpus run contract build start.
- `src/mavs_ch10c/execution/corpus_writer.py:505` comment and `:506` call: corpus run contract build complete.

Current shifted line references for modified Phase 2 files:

- `src/mavs_ch10c/execution/repeated_training.py:94` comment and `:95` call: repeated training unit start.
- `src/mavs_ch10c/execution/repeated_training.py:110` comment and `:111` call: repeated training unit complete.
- `src/mavs_ch10c/execution/repeated_training.py:135` comment and `:136` call: specialist fit cache hit.
- `src/mavs_ch10c/execution/repeated_training.py:142` comment and `:143` call: specialist fit start.
- `src/mavs_ch10c/execution/repeated_training.py:247` comment and `:248` call: specialist fit complete.
- `src/mavs_ch10c/execution/repeated_training.py:260` comment and `:261` call: model YAML load start.
- `src/mavs_ch10c/execution/repeated_training.py:266` comment and `:267` call: model YAML load complete.
- `src/mavs_ch10c/execution/repeated_training.py:274` comment and `:275` call: frozen estimator build start.
- `src/mavs_ch10c/execution/repeated_training.py:313` comment and `:314` call: frozen estimator build complete.
- `src/mavs_ch10c/execution/repeated_training.py:328` comment and `:329` call: non-MLP estimator fit start.
- `src/mavs_ch10c/execution/repeated_training.py:331` comment and `:332` call: non-MLP estimator fit complete.
- `src/mavs_ch10c/execution/repeated_training.py:350` comment and `:351` call: MLP epoch fit start.
- `src/mavs_ch10c/execution/repeated_training.py:365` comment and `:366` call: MLP epoch fit complete.
- `src/mavs_ch10c/execution/repeated_training.py:383` comment and `:384` call: calibration fit start.
- `src/mavs_ch10c/execution/repeated_training.py:392` comment and `:393` call: calibration fit complete.
- `src/mavs_ch10c/execution/system_runner.py:92` comment and `:93` call: system execution start.
- `src/mavs_ch10c/execution/system_runner.py:170` comment and `:171` call: system execution complete.
- `src/mavs_ch10c/execution/system_runner.py:277` comment and `:278` call: single-model validation selection complete.
- `src/mavs_ch10c/execution/system_runner.py:298` comment and `:299` call: static weights validation fit complete.
- `src/mavs_ch10c/execution/system_runner.py:323` comment and `:324` call: Veto MAVS empirical execution complete.
- `src/mavs_ch10c/execution/system_runner.py:347` comment and `:348` call: Pure MAVS-GC empirical execution complete.
- `src/mavs_ch10c/execution/corpus_writer.py:83` comment and `:84` call: corpus run start.
- `src/mavs_ch10c/execution/corpus_writer.py:112` comment and `:113` call: corpus cache hit.
- `src/mavs_ch10c/execution/corpus_writer.py:241` comment and `:242` call: corpus run complete.
- `src/mavs_ch10c/execution/corpus_writer.py:314` comment and `:315` call: no-tuning guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:325` comment and `:326` call: no-tuning guard complete.
- `src/mavs_ch10c/execution/corpus_writer.py:332` comment and `:333` call: final-mode guard start.
- `src/mavs_ch10c/execution/corpus_writer.py:350` comment and `:351` call: final-mode guard complete.
- `src/mavs_ch10c/execution/corpus_writer.py:575` comment and `:576` call: YAML config load start.
- `src/mavs_ch10c/execution/corpus_writer.py:581` comment and `:582` call: YAML config load complete.
- `src/mavs_ch10c/execution/corpus_writer.py:598` comment and `:599` call: repetition grid read start.
- `src/mavs_ch10c/execution/corpus_writer.py:606` comment and `:607` call: repetition grid read complete.
- `src/mavs_ch10c/execution/corpus_writer.py:612` comment and `:613` call: CSV artifact write start.
- `src/mavs_ch10c/execution/corpus_writer.py:617` comment and `:618` call: empty CSV artifact write complete.
- `src/mavs_ch10c/execution/corpus_writer.py:624` comment and `:625` call: CSV artifact write complete.
- `src/mavs_ch10c/execution/corpus_writer.py:629` comment and `:630` call: JSONL artifact write start.
- `src/mavs_ch10c/execution/corpus_writer.py:635` comment and `:636` call: JSONL artifact write complete.

### Stress Tests Run

Commands and outcomes:

- `python -m py_compile src/mavs_ch10c/execution/corpus_writer.py src/mavs_ch10c/execution/system_runner.py src/mavs_ch10c/execution/repeated_training.py`: passed.
- `python -m pytest`: `23 passed in 85.14s`.
- `python scripts/run_locked_repetition_corpus.py --execution-mode manifest`: passed, cache hit, locked corpus hash `a2fd4913c121e4823e01b1bec8e9ac09cd18ea03c538802c7225e6242ea0b686`.
- `python scripts/run_audit_repetition_corpus.py --execution-mode manifest`: passed, audit freeze gate hash `8428c5b19619522e4635f2553d2f73546dede64cf9933592336fe54e716bbaba`, audit corpus hash `65963cf55087e6ee510daa1fb49d40188639ee71cc11870902c058d343985d4f`.
- `python scripts/build_variance_benchmark_dataset.py`: passed, cache hit, variance manifest hash `9d70f8d4699da0cd0ce989a964ebcfb7b85439562f21fb201e99bce8ad92bf13`.
- Custom invariant sweep: passed locked/audit artifact-hash validation, run/frozen manifest count validation, pre-execution hash alignment, readable model metadata checks, audit freeze gate check, and variance row-count checks.
- `python scripts/run_locked_repetition_corpus.py --execution-mode final`: intentionally refused the current dirty checkout after passing hash-contract checks, with `RuntimeError: Final corpus mode requires clean git paths for Chapter 10C final inputs`.

### WorkPlan Compliance Status After Addendum

Phase 2:

- Fully implemented in accordance with `WorkPlan.md`.
- The runner now refuses final mode for dirty or hash-mismatched frozen inputs.
- The runner stores a frozen run manifest before each system execution.
- Benchmark isolation tests already prove benchmark rows do not appear in train, validation, or calibration partitions.
- Code/config changes now invalidate cached corpora through manifest contract checks.
- Audit execution is gated by a locked pipeline, metric code, report template, corpus-hash, and config-hash freeze manifest.
- RF, GBT, MLP, and calibration metadata now record the fixed settings and hashes requested by the WorkPlan.

Phase 3:

- Fully implemented in accordance with `WorkPlan.md`.
- Phase 3 consumes Phase 2 outputs only and does not train models.
- Locked and audit variance datasets remain separately labeled.
- Manifest input hashes now reference the updated compliant locked and audit corpus manifests.
- Alignment, identical-input, governance-trace, and delta-row tests pass.

## Phase 4 - Stability Evaluation and Reproducibility Metrics

### WorkPlan Scope Implemented

Phase 4 computes all Chapter 10C reproducibility measurements listed in `WorkPlan.md`:

- Accuracy Variance
- F1 Variance
- Prediction Stability
- Decision Stability
- Consensus Stability
- Trace Stability
- Run-to-Run Agreement
- Confidence Interval Width

No models are trained in this phase. The implementation consumes the frozen Phase 3 variance benchmark rows and writes only Phase 4 metric artifacts under `results/stability_metrics/`.

### Files Created or Updated

Files created for Phase 4:

- `configs/experiments/reproducibility_metrics.yaml`
- `src/mavs_ch10c/evaluation/__init__.py`
- `src/mavs_ch10c/evaluation/variance.py`
- `src/mavs_ch10c/evaluation/stability.py`
- `src/mavs_ch10c/evaluation/agreement.py`
- `src/mavs_ch10c/evaluation/confidence_intervals.py`
- `src/mavs_ch10c/evaluation/trace_stability.py`
- `src/mavs_ch10c/evaluation/aggregation.py`
- `scripts/build_reproducibility_metrics.py`
- `scripts/build_stability_tables.py`
- `results/stability_metrics/.gitkeep`
- `results/stability_metrics/locked_metric_rows.csv`
- `results/stability_metrics/audit_metric_rows.csv`
- `results/stability_metrics/accuracy_variance.csv`
- `results/stability_metrics/f1_variance.csv`
- `results/stability_metrics/prediction_stability.csv`
- `results/stability_metrics/decision_stability.csv`
- `results/stability_metrics/consensus_stability.csv`
- `results/stability_metrics/trace_stability.csv`
- `results/stability_metrics/run_to_run_agreement.csv`
- `results/stability_metrics/confidence_interval_widths.csv`
- `results/stability_metrics/reproducibility_metric_manifest.json`
- `tests/test_accuracy_variance_definition.py`
- `tests/test_f1_variance_definition.py`
- `tests/test_prediction_stability_definition.py`
- `tests/test_decision_stability_definition.py`
- `tests/test_consensus_stability_definition.py`
- `tests/test_trace_stability_definition.py`
- `tests/test_run_to_run_agreement_definition.py`
- `tests/test_confidence_interval_width_definition.py`
- `tests/test_metric_inputs_are_frozen.py`

Supporting Phase 3 update for Phase 4 trace metrics:

- `src/mavs_ch10c/comparison/system_outputs.py` now carries explicit trace-field columns into variance rows.
- `src/mavs_ch10c/comparison/variance_dataset.py` now merges frozen governance trace fields into variance rows and refuses cached variance datasets that lack Phase 4 trace fields.
- `results/variance_benchmarks/locked_variance_rows.csv` and `results/variance_benchmarks/audit_variance_rows.csv` were deterministically extended with trace columns.
- `results/variance_benchmarks/variance_dataset_manifest.json` now records `trace_fields_available_for_phase4: true`.

### Metric Definitions Implemented

Accuracy variance:

- Implemented in `src/mavs_ch10c/evaluation/variance.py`.
- Computes per-run execution-unit accuracy from row-level correctness.
- Emits sample variance, standard deviation, mean accuracy, row count, and repetition-unit count.
- Aggregates at:
  - `dataset_system_split_init_composition`
  - `dataset_system_composition`
- Reports locked and audit separately.

F1 variance:

- Implemented in `src/mavs_ch10c/evaluation/variance.py`.
- Computes binary F1 from summed TP/FP/FN per execution unit.
- Uses predeclared zero-division policy: `binary_f1_zero_when_denominator_is_zero`.
- Emits sample variance, standard deviation, mean F1, row count, and repetition-unit count.
- Reports locked and audit separately.

Prediction stability:

- Implemented in `src/mavs_ch10c/evaluation/stability.py`.
- Computes row-aligned mean pairwise agreement of predicted labels for each row id and label hash.
- Computes secondary probability stability as `1 - mean_abs_probability_difference`.
- Uses formula-based pair counts, not exhaustive pair materialization.

Decision stability:

- Implemented in `src/mavs_ch10c/evaluation/stability.py`.
- Computes row-aligned mean pairwise agreement of final binary accept/reject decisions.
- Uses the governed final decision for `pure_mavs_gc` and `veto_mavs`.

Consensus stability:

- Implemented in `src/mavs_ch10c/evaluation/stability.py`.
- For `pure_mavs_gc` and `veto_mavs`, uses frozen governance trace field `R`.
- Computes row-level variance and pairwise stability of `R`.
- For aggregation-only baselines, records MAVS-specific consensus as not applicable and records probability-score stability separately.

Trace stability:

- Implemented in `src/mavs_ch10c/evaluation/trace_stability.py`.
- Applies only to governance systems.
- Compares required trace fields:
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
- Emits field-level variance, field exact-repeat rate, exact trace-hash repeat rate, normalized trace-distance mean, and normalized trace similarity.

Run-to-run agreement:

- Implemented in `src/mavs_ch10c/evaluation/agreement.py`.
- Computes pairwise agreement for decisions and correctness outcomes.
- Computes kappa-style agreement where label distributions permit.
- Records undefined single-class kappa cases instead of fabricating values.

Confidence interval width:

- Implemented in `src/mavs_ch10c/evaluation/confidence_intervals.py`.
- Uses predeclared analytical repeated-unit normal intervals:
  - method: `analytical_repeated_unit_normal`
  - confidence level: `0.95`
  - z value: `1.96`
- Computes interval widths for accuracy and F1.
- Records whether Pure MAVS-GC intervals are narrower, wider, indistinguishable, or the reference row.

Paired Pure MAVS-GC comparisons:

- Implemented in `src/mavs_ch10c/evaluation/aggregation.py`.
- Pure MAVS-GC is compared against:
  - Single Model
  - Mean Ensemble
  - Static Weighted Ensemble
  - Veto MAVS
- Uses the frozen `system_delta_rows.csv` from Phase 3.
- Records correctness deltas, probability deltas, decision agreement, and direction vs baseline in `locked_metric_rows.csv` and `audit_metric_rows.csv`.

Locked-vs-audit consistency:

- Implemented in the Phase 4 manifest.
- Verifies locked and audit metric families match.
- Verifies locked and audit systems match.
- Verifies paired baseline coverage matches.

### Anti-Overfitting Controls Implemented

- Metric definitions are predeclared in `configs/experiments/reproducibility_metrics.yaml`.
- Confidence interval method and z value are predeclared before metric generation.
- The manifest records `metric_definitions_selected_from_audit: false`.
- The manifest records `audit_metric_definitions_frozen: true`.
- The manifest records `metrics_read_only_frozen_variance_datasets: true`.
- The manifest records `training_performed: false`.
- The manifest records `preserve_negative_neutral_mixed_results: true`.
- Metric code hashes are stored in `results/stability_metrics/reproducibility_metric_manifest.json`.
- Metric cache reuse is refused if metric code hashes, config hash, variance manifest hash, or artifact hashes drift.

### Phase 3 Trace-Field Support Update

Phase 4 trace stability requires field-level governance trace values. The prior Phase 3 variance rows carried trace hashes but not all trace fields. I extended the frozen Phase 3 variance rows with trace fields from the frozen Phase 2 trace indexes and updated the Phase 3 manifest.

Updated Phase 3 variance manifest:

- Path: `results/variance_benchmarks/variance_dataset_manifest.json`
- Manifest hash: `12b30b5f246432946e717a9de4740de8f761906027d94b10c0afb32fd395d5cb`
- Locked variance hash: `6ca5e5a1bba8872e2187c4df698ceed711cf825c72f83cb0b3c6022359aa5270`
- Audit variance hash: `19c83733ffa208c2a02b080c9df9bc518dedd1127de27922f0794ac0ac69802f`
- System delta hash remains: `28aaf74f9f8c681b9d8595678b813349a4d7b134f6dc2402ecc070fb393e8ec0`
- Locked trace-augmented rows: `129,600`
- Audit trace-augmented rows: `51,840`

### Phase 4 Artifacts

Metric manifest:

- Path: `results/stability_metrics/reproducibility_metric_manifest.json`
- Manifest hash: `2c6ffec8b4febe7c1f0fa31740b37c7684fc23ca288502fea68693b81c486645`
- Source variance manifest hash: `12b30b5f246432946e717a9de4740de8f761906027d94b10c0afb32fd395d5cb`
- Locked metric rows: `17,664`
- Audit metric rows: `11,040`
- Paired Pure MAVS-GC baseline rows: `1,664`

Metric table row counts and hashes:

- `locked_metric_rows.csv`: `17,664` rows, hash `27c79f78d82e01dac90036fe4b7265b149f9a7c521e6493cbb2191a73d73a397`
- `audit_metric_rows.csv`: `11,040` rows, hash `06ac4f4dbfd5d75eb69666861efa602da9f7ea6c0c3aef49fad8520c68fd4af4`
- `accuracy_variance.csv`: `2,080` rows, hash `909fd502bff636e47afdf226e9078657dbe8e563586ae09abf171f974e487462`
- `f1_variance.csv`: `2,080` rows, hash `bcb3a565ab78cb63d57fa29e3872ba4535ea472985ae623d773a4975a818fd39`
- `prediction_stability.csv`: `2,080` rows, hash `425fb250c2d0f16e61698b6dad542137941bfb3f6bedfebcd61667ff7d8e8c0e`
- `decision_stability.csv`: `2,080` rows, hash `180414a8e1837bf877d54529ad754c8d00623b52637f48aa1cfd7a4393a8c2b0`
- `consensus_stability.csv`: `2,080` rows, hash `b6f9e478121e06a17557425acee3e98fc1c245d399c3e4ef523364e46b62d3cb`
- `trace_stability.csv`: `8,320` rows, hash `dc76747ebf397942afb58a9e1ab164fbf3dd5ef825776c6a44b4dd268e53c404`
- `run_to_run_agreement.csv`: `4,160` rows, hash `aac41426009b711146e19bdd2b35fd5abcbc19ebac1c9463b7b13af5c0f13392`
- `confidence_interval_widths.csv`: `4,160` rows, hash `585bd5afc52a55c44dc0f65ab015ab8767178aa3ee5edfdb6d5f687b49b09d7d`

### Console.log Instrumentation

Scripts:

- `scripts/build_reproducibility_metrics.py:19` comment and `:20` call: reproducibility metric script start.
- `scripts/build_reproducibility_metrics.py:22` comment and `:23` call: reproducibility metric script complete.
- `scripts/build_stability_tables.py:19` comment and `:20` call: stability table script start.
- `scripts/build_stability_tables.py:22` comment and `:23` call: stability table script complete.

Phase 4 aggregation:

- `src/mavs_ch10c/evaluation/aggregation.py:119` comment and `:120` call: reproducibility metric build start.
- `src/mavs_ch10c/evaluation/aggregation.py:132` comment and `:134` call: reproducibility metric cache hit.
- `src/mavs_ch10c/evaluation/aggregation.py:215` comment and `:217` call: reproducibility metric build complete.
- `src/mavs_ch10c/evaluation/aggregation.py:229` comment and `:230` call: per-mode metric table build start.
- `src/mavs_ch10c/evaluation/aggregation.py:260` comment and `:261` call: per-mode metric table build complete.
- `src/mavs_ch10c/evaluation/aggregation.py:277` comment and `:278` call: paired Pure MAVS baseline comparison build start.
- `src/mavs_ch10c/evaluation/aggregation.py:334` comment and `:335` call: paired Pure MAVS baseline comparison build complete.
- `src/mavs_ch10c/evaluation/aggregation.py:422` comment and `:423` call: frozen variance manifest load start.
- `src/mavs_ch10c/evaluation/aggregation.py:438` comment and `:440` call: frozen variance manifest load complete.
- `src/mavs_ch10c/evaluation/aggregation.py:482` comment and `:483` call: variance row load start.
- `src/mavs_ch10c/evaluation/aggregation.py:488` comment and `:489` call: variance row load complete.
- `src/mavs_ch10c/evaluation/aggregation.py:494` comment and `:495` call: system delta row load start.
- `src/mavs_ch10c/evaluation/aggregation.py:500` comment and `:501` call: system delta row load complete.
- `src/mavs_ch10c/evaluation/aggregation.py:506` comment and `:507` call: metric CSV write start.
- `src/mavs_ch10c/evaluation/aggregation.py:516` comment and `:517` call: metric CSV write complete.

Metric modules:

- `src/mavs_ch10c/evaluation/variance.py:46` comment and `:47` call: execution-unit metric computation start.
- `src/mavs_ch10c/evaluation/variance.py:68` comment and `:69` call: execution-unit metric computation complete.
- `src/mavs_ch10c/evaluation/variance.py:82` comment and `:83` call: variance metric row build start.
- `src/mavs_ch10c/evaluation/variance.py:107` comment and `:108` call: variance metric row build complete.
- `src/mavs_ch10c/evaluation/stability.py:29` comment and `:30` call: prediction stability build start.
- `src/mavs_ch10c/evaluation/stability.py:40` comment and `:41` call: prediction stability build complete.
- `src/mavs_ch10c/evaluation/stability.py:50` comment and `:51` call: decision stability build start.
- `src/mavs_ch10c/evaluation/stability.py:61` comment and `:62` call: decision stability build complete.
- `src/mavs_ch10c/evaluation/stability.py:71` comment and `:72` call: consensus stability build start.
- `src/mavs_ch10c/evaluation/stability.py:84` comment and `:85` call: consensus stability build complete.
- `src/mavs_ch10c/evaluation/trace_stability.py:46` comment and `:47` call: trace stability build start.
- `src/mavs_ch10c/evaluation/trace_stability.py:76` comment and `:77` call: trace stability build complete.
- `src/mavs_ch10c/evaluation/agreement.py:26` comment and `:27` call: run-to-run agreement build start.
- `src/mavs_ch10c/evaluation/agreement.py:50` comment and `:51` call: run-to-run agreement build complete.
- `src/mavs_ch10c/evaluation/confidence_intervals.py:29` comment and `:30` call: confidence interval build start.
- `src/mavs_ch10c/evaluation/confidence_intervals.py:50` comment and `:51` call: confidence interval build complete.

Phase 3 trace-field support instrumentation:

- `src/mavs_ch10c/comparison/variance_dataset.py:166` comment and `:167` call: governance trace field load start.
- `src/mavs_ch10c/comparison/variance_dataset.py:184` comment and `:185` call: governance trace field load complete.

### Verification Commands

Commands run:

- `python -m py_compile src/mavs_ch10c/comparison/system_outputs.py src/mavs_ch10c/comparison/variance_dataset.py src/mavs_ch10c/evaluation/__init__.py src/mavs_ch10c/evaluation/variance.py src/mavs_ch10c/evaluation/stability.py src/mavs_ch10c/evaluation/agreement.py src/mavs_ch10c/evaluation/confidence_intervals.py src/mavs_ch10c/evaluation/trace_stability.py src/mavs_ch10c/evaluation/aggregation.py scripts/build_reproducibility_metrics.py scripts/build_stability_tables.py`
- `python scripts/build_reproducibility_metrics.py`
- `python -m py_compile src/mavs_ch10c/evaluation/__init__.py src/mavs_ch10c/evaluation/variance.py src/mavs_ch10c/evaluation/stability.py src/mavs_ch10c/evaluation/agreement.py src/mavs_ch10c/evaluation/confidence_intervals.py src/mavs_ch10c/evaluation/trace_stability.py src/mavs_ch10c/evaluation/aggregation.py scripts/build_reproducibility_metrics.py scripts/build_stability_tables.py tests/test_accuracy_variance_definition.py tests/test_f1_variance_definition.py tests/test_prediction_stability_definition.py tests/test_decision_stability_definition.py tests/test_consensus_stability_definition.py tests/test_trace_stability_definition.py tests/test_run_to_run_agreement_definition.py tests/test_confidence_interval_width_definition.py tests/test_metric_inputs_are_frozen.py`
- `python -m pytest tests/test_accuracy_variance_definition.py tests/test_f1_variance_definition.py tests/test_prediction_stability_definition.py tests/test_decision_stability_definition.py tests/test_consensus_stability_definition.py tests/test_trace_stability_definition.py tests/test_run_to_run_agreement_definition.py tests/test_confidence_interval_width_definition.py tests/test_metric_inputs_are_frozen.py`
- `python scripts/build_variance_benchmark_dataset.py`
- `python scripts/build_reproducibility_metrics.py`
- `python scripts/build_stability_tables.py`
- `python -m pytest`

Verification results:

- Phase 4 tests: `9 passed in 10.64s`.
- Full repository tests: `32 passed in 103.22s`.
- `scripts/build_variance_benchmark_dataset.py`: passed with cache hit, variance manifest hash `12b30b5f246432946e717a9de4740de8f761906027d94b10c0afb32fd395d5cb`.
- `scripts/build_reproducibility_metrics.py`: passed with cache hit, metric manifest hash `2c6ffec8b4febe7c1f0fa31740b37c7684fc23ca288502fea68693b81c486645`.
- `scripts/build_stability_tables.py`: passed with cache hit, metric manifest hash `2c6ffec8b4febe7c1f0fa31740b37c7684fc23ca288502fea68693b81c486645`.

### WorkPlan Compliance Check

Phase 4 requirements implemented:

- Metric computation over aligned repeated runs exists.
- Aggregation exists by dataset, system, split schedule, initialization schedule, specialist composition, and run mode.
- Summary aggregation also exists by dataset, system, composition, and run mode.
- Pure MAVS-GC paired comparisons exist against Single Model, Mean Ensemble, Static Weighted Ensemble, and Veto MAVS.
- Locked-vs-audit consistency checks exist in the metric manifest.
- Confidence interval width estimation uses the predeclared analytical method.
- Trace field comparison exists for governance systems.
- No models are trained in Phase 4.
- Metrics consume frozen variance benchmark rows and validate input hashes.
- Audit was not used to select metric definitions.
- Negative, neutral, and mixed result directions are preserved in paired comparison rows.
- Every required Phase 4 metric output file exists for locked and audit modes.
- Metric rows cover all required datasets, systems, and compositions.
- Tests pass for every required metric definition and the frozen-input guard.

Compliance status:

- Phase 4: implemented in accordance with `WorkPlan.md`.

## 2026-06-23 - Phase 5 - Analysis, Variance Tables, Stability Figures, and Reproducibility Report

### Path.md Historical-Note Fix

The earlier Phase 2 and Phase 3 scaffold limitation sections were relabeled as superseded historical audit notes. They now state that the empirical reimplementation and compliance addenda are the current implementation state. This prevents the old scaffold limitations from being read as current Phase 2/3 status.

### Scope Implemented

Implemented Phase 5 of `WorkPlan.md`: analysis, variance tables, stability figures, reproducibility report, and reproducibility artifact manifest.

Phase 5 consumes only frozen Phase 4 metric artifacts. No model training, hyperparameter tuning, governance modification, or train/validation/calibration diagnostic evidence is used in this phase.

### Files Created or Changed

Created:

- `configs/reports/reproducibility_report.yaml`
- `src/mavs_ch10c/reporting/__init__.py`
- `src/mavs_ch10c/reporting/tables.py`
- `src/mavs_ch10c/reporting/figures.py`
- `src/mavs_ch10c/reporting/reproducibility_report.py`
- `src/mavs_ch10c/reporting/artifact_manifest.py`
- `scripts/build_variance_tables.py`
- `scripts/build_stability_figures.py`
- `scripts/build_reproducibility_report.py`
- `scripts/build_reproducibility_manifest.py`
- `tests/test_report_inputs_complete.py`
- `tests/test_report_claims_reference_artifacts.py`
- `tests/test_variance_tables_complete.py`
- `tests/test_stability_figures_exist.py`
- `tests/test_reproducibility_manifest_complete.py`
- `results/reports/reproducibility_report.md`
- `results/reports/variance_tables.csv`
- `results/reports/stability_tables.csv`
- `results/reports/reproducibility_system_deltas.csv`
- `results/reports/reproducibility_artifact_manifest.json`
- `results/figures/accuracy_variance_by_system.png`
- `results/figures/f1_variance_by_system.png`
- `results/figures/prediction_stability_by_system.png`
- `results/figures/decision_stability_by_system.png`
- `results/figures/consensus_stability_by_system.png`
- `results/figures/trace_stability_by_system.png`
- `results/figures/confidence_interval_widths.png`

Changed:

- `pyproject.toml`: added `matplotlib>=3.8` because Phase 5 requires PNG figures.
- `Path.md`: relabeled superseded Phase 2/3 scaffold notes and added this Phase 5 implementation record.

### Code Produced

Table builders:

- `src/mavs_ch10c/reporting/tables.py` builds `variance_tables.csv`, `stability_tables.csv`, and `reproducibility_system_deltas.csv`.
- Variance rows are emitted at the required dataset x system x specialist composition x run mode x metric grain.
- Stability rows include prediction stability, decision stability, consensus/score stability, trace stability, and run-to-run agreement.
- Pure MAVS-GC deltas are emitted against Single Model, Mean Ensemble, Static Weighted Ensemble, and Veto MAVS.
- Locked and audit evidence remain separate in every table.

Figure builders:

- `src/mavs_ch10c/reporting/figures.py` renders all seven required PNG figures using deterministic table inputs.
- Figure generation fails if a plotted metric has no numeric evidence.

Report generator:

- `src/mavs_ch10c/reporting/reproducibility_report.py` writes `results/reports/reproducibility_report.md`.
- The report includes source authority, methodology, imported Chapter 10A/10B foundation, frozen governance policy, repeated execution matrix, independent benchmark design, anti-overfitting controls, results, limitations, claim register, and final answer.

Artifact manifest:

- `src/mavs_ch10c/reporting/artifact_manifest.py` writes `results/reports/reproducibility_artifact_manifest.json`.
- The manifest records source document references, import commits, dataset hashes, split schedule hashes, seed registry hashes, initialization schedule hashes, composition hashes, model config hashes, governance source hashes, corpus hashes, variance dataset hashes, metric table hashes, report table hashes, figure hashes, report hash, reporting code hashes, and report policy.

### Phase 5 Artifacts

Report and manifest:

- `results/reports/reproducibility_report.md`: hash `a60e3099d6f5d67a64ca6a81cac3e92bef2ad3264c895b90b05941ba959caece`
- `results/reports/reproducibility_artifact_manifest.json`: file hash `15a1dc6a6a1dc016e41798cfdcf88bbfe6fb6c8ed807a0cd827938ea0c84ab01`
- Internal reproducibility artifact manifest hash: `3ef7ca9b7765e6387f4dc0d10317bd40371bd2be87f6efeae8d8a496909d700a`

Tables:

- `results/reports/variance_tables.csv`: `320` rows, hash `63c3f48f2efee55af5f0cb1a063f1a92b04c658b0828888ae3548fd52c8b8e22`
- `results/reports/stability_tables.csv`: `1,440` rows, hash `7bb1cfa5b644c8eba5844dd6370109b0e880a62f0c9e0a03f5bd18c2b3351347`
- `results/reports/reproducibility_system_deltas.csv`: `128` rows, hash `8a540379f1551edaf4c4dc5744cd6a88230568af42ecb81b284186d53dc89418`

Figures:

- `results/figures/accuracy_variance_by_system.png`: hash `94ccd85215ef179038fa1acb3e75c71f8ee0b9f8ef5b5dfe9e8064218050f4f5`
- `results/figures/f1_variance_by_system.png`: hash `cfa0d93258233de2b21bb13e7a6f284a5322aaaf179599be4927d30ea44f0b2a`
- `results/figures/prediction_stability_by_system.png`: hash `0a809d7c266dcf3b9bb32b0fcd8a2f57cb1867cad83ac6e6363fba87a0d2e7f7`
- `results/figures/decision_stability_by_system.png`: hash `1554f58246165bdb45daef2b7ff277dd2d415efac66ddd77757fc28aca384774`
- `results/figures/consensus_stability_by_system.png`: hash `2f5636202b3996ab0b6543d42c63267176023ab02ac2c007541948e7a055e528`
- `results/figures/trace_stability_by_system.png`: hash `6670b31035da384ec8ea4fadb3f460746128cd655231a956a35cbc7a4b8bd01e`
- `results/figures/confidence_interval_widths.png`: hash `fb417e749c9d65ef0873749edd38ad17b039ed93fb461e5c50add8152825a712`

### Claim Support

The report contains seven claim-register rows. Every claim maps to generated artifacts.

- C1: Pure MAVS-GC lower variance in `86/256` paired comparisons. Evidence: `variance_tables.csv`, accuracy variance figure, F1 variance figure.
- C2: Pure MAVS-GC higher prediction stability in `44/128` comparisons. Evidence: `stability_tables.csv`, prediction stability figure.
- C3: Pure MAVS-GC higher decision stability in `44/128` comparisons. Evidence: `stability_tables.csv`, decision stability figure.
- C4: Pure MAVS-GC trace similarity higher than Veto MAVS in `17/320` trace comparisons. Evidence: `stability_tables.csv`, trace stability figure.
- C5: Pure MAVS-GC narrower confidence intervals in `86/256` comparisons. Evidence: `variance_tables.csv`, confidence interval width figure.
- C6: Correctness deltas are mixed: `26` higher, `11` neutral, `91` lower. Evidence: `reproducibility_system_deltas.csv`.
- C7: Locked and audit evidence use matching metric families, systems, and baselines. Evidence: Phase 4 metric manifest and Phase 5 artifact manifest.

### Anti-Overfitting Controls

- Phase 5 does not train models.
- Phase 5 reads only frozen Phase 4 metric artifacts.
- Locked and audit evidence remain separately labeled.
- Claim support is computed from generated report tables, not hand-entered.
- The report explicitly states mixed and negative results.
- The report does not claim corruption robustness.
- The report does not make unconditional or global advantage claims.
- The artifact manifest records all upstream hashes required by `WorkPlan.md`.
- Report validation fails if claim rows lack artifact references or if required PNG figures are missing or invalid.
- Table validation fails if expected variance rows, Pure MAVS-GC baseline deltas, systems, datasets, run modes, or trace fields are missing.

### Console.log Instrumentation

Scripts:

- `scripts/build_reproducibility_report.py:19` comment and `:20` call: reproducibility report script start.
- `scripts/build_reproducibility_report.py:22` comment and `:23` call: reproducibility report script complete.
- `scripts/build_variance_tables.py:20` comment and `:21` call: variance table script start.
- `scripts/build_variance_tables.py:24` comment and `:25` call: variance table script complete.
- `scripts/build_stability_figures.py:21` comment and `:22` call: stability figure script start.
- `scripts/build_stability_figures.py:26` comment and `:27` call: stability figure script complete.
- `scripts/build_reproducibility_manifest.py:20` comment and `:21` call: reproducibility manifest script start.
- `scripts/build_reproducibility_manifest.py:24` comment and `:25` call: reproducibility manifest script complete.

Reporting modules:

- `src/mavs_ch10c/reporting/tables.py:76` comment and `:77` call: report table build start.
- `src/mavs_ch10c/reporting/tables.py:96` comment and `:98` call: report table build complete.
- `src/mavs_ch10c/reporting/tables.py:110` comment and `:111` call: variance table derivation start.
- `src/mavs_ch10c/reporting/tables.py:151` comment and `:152` call: variance table derivation complete.
- `src/mavs_ch10c/reporting/tables.py:161` comment and `:162` call: stability table derivation start.
- `src/mavs_ch10c/reporting/tables.py:203` comment and `:204` call: stability table derivation complete.
- `src/mavs_ch10c/reporting/tables.py:213` comment and `:214` call: system delta table derivation start.
- `src/mavs_ch10c/reporting/tables.py:246` comment and `:247` call: system delta table derivation complete.
- `src/mavs_ch10c/reporting/tables.py:307` comment and `:308` call: report CSV write start.
- `src/mavs_ch10c/reporting/tables.py:314` comment and `:315` call: report CSV write complete.
- `src/mavs_ch10c/reporting/figures.py:34` comment and `:35` call: figure build start.
- `src/mavs_ch10c/reporting/figures.py:100` comment and `:101` call: figure build complete.
- `src/mavs_ch10c/reporting/figures.py:122` comment and `:123` call: individual figure render start.
- `src/mavs_ch10c/reporting/figures.py:169` comment and `:170` call: individual figure render complete.
- `src/mavs_ch10c/reporting/reproducibility_report.py:30` comment and `:31` call: report build start.
- `src/mavs_ch10c/reporting/reproducibility_report.py:51` comment and `:53` call: report build complete.
- `src/mavs_ch10c/reporting/reproducibility_report.py:64` comment and `:65` call: report render start.
- `src/mavs_ch10c/reporting/reproducibility_report.py:147` comment and `:148` call: report render complete.
- `src/mavs_ch10c/reporting/artifact_manifest.py:49` comment and `:50` call: artifact manifest build start.
- `src/mavs_ch10c/reporting/artifact_manifest.py:137` comment and `:139` call: artifact manifest build complete.

### Verification Commands

Commands run:

- `python scripts/build_reproducibility_report.py`
- `python -m py_compile src/mavs_ch10c/reporting/__init__.py src/mavs_ch10c/reporting/tables.py src/mavs_ch10c/reporting/figures.py src/mavs_ch10c/reporting/reproducibility_report.py src/mavs_ch10c/reporting/artifact_manifest.py scripts/build_variance_tables.py scripts/build_stability_figures.py scripts/build_reproducibility_report.py scripts/build_reproducibility_manifest.py tests/test_report_inputs_complete.py tests/test_report_claims_reference_artifacts.py tests/test_variance_tables_complete.py tests/test_stability_figures_exist.py tests/test_reproducibility_manifest_complete.py`
- `python -m pytest tests/test_report_inputs_complete.py tests/test_report_claims_reference_artifacts.py tests/test_variance_tables_complete.py tests/test_stability_figures_exist.py tests/test_reproducibility_manifest_complete.py`
- `python scripts/build_variance_tables.py`
- `python scripts/build_stability_figures.py`
- `python scripts/build_reproducibility_report.py`
- `python scripts/build_reproducibility_manifest.py`
- `python -m pytest`

Verification results:

- Phase 5 focused tests: `5 passed in 8.26s`.
- Full repository tests: `37 passed in 69.65s`.
- `scripts/build_variance_tables.py`: passed, emitted `320` variance rows, `1,440` stability rows, and `128` delta rows.
- `scripts/build_stability_figures.py`: passed, emitted `7` PNG figures.
- `scripts/build_reproducibility_report.py`: passed, report hash `a60e3099d6f5d67a64ca6a81cac3e92bef2ad3264c895b90b05941ba959caece`, manifest hash `3ef7ca9b7765e6387f4dc0d10317bd40371bd2be87f6efeae8d8a496909d700a`.
- `scripts/build_reproducibility_manifest.py`: passed, manifest hash `3ef7ca9b7765e6387f4dc0d10317bd40371bd2be87f6efeae8d8a496909d700a`.

### WorkPlan Compliance Check

Phase 5 requirements implemented:

- Reproducibility report exists and answers the Chapter 10C research question.
- Variance tables exist.
- Stability tables exist.
- All seven stability figures exist as PNG files.
- Reproducibility artifact manifest exists.
- Every claim in the claim register maps to generated tables, figures, or metric manifests.
- Report includes source authority, methodology, imported Chapter 10A/10B foundation, frozen governance policy, repeated execution matrix, independent benchmark design, anti-overfitting controls, results, limitations, and final answer.
- Artifact manifest records source document references, import commits, dataset hashes, split schedule hashes, seed registry hashes, initialization schedule hashes, composition hashes, model config hashes, governance source hashes, corpus hashes, variance dataset hashes, metric table hashes, figure hashes, and report hash.
- Locked and audit evidence are distinguished.
- Final and exploratory evidence status is recorded in the artifact manifest.
- Negative, neutral, and mixed results are preserved.
- Veto MAVS is compared separately as the governance control.

Compliance status:

- Phase 5: implemented in accordance with `WorkPlan.md`.

## Phase 6 - Corruption-Aware Reproducibility

Date/time: `2026-06-23 17:26:00 +05:00`

### Scope Implemented

Implemented the new Phase 6 corruption-aware reproducibility extension exactly against the revised `WorkPlan.md` Phase 6 contract.

This phase imports the complete Chapter 10B corruption suite and evaluates reproducibility under:

- datasets: `breast_cancer_wisconsin`, `adult_income`, `credit_card_fraud`, `bank_marketing`
- systems: `single_model`, `mean_ensemble`, `static_weighted_ensemble`, `veto_mavs`, `pure_mavs_gc`
- run modes: `locked`, `audit`
- specialist compositions: `full_rf_gbt_mlp`, `rf_gbt_pair`, `rf_mlp_pair`, `gbt_mlp_pair`
- corruption families: `adversarial_confidence_inflation`, `confidence_distortion`, `distribution_shift`, `feature_noise`, `label_noise`, `missing_features`, `random_feature_deletion`, `specialist_failure`, `synthetic_sensor_failure`
- corruption levels: `0.0`, `0.05`, `0.1`, `0.2`, `0.4`, `0.6`, `0.8`, `1.0`

Model handling:

- No new model training was performed in Phase 6.
- No hyperparameter search was performed.
- No architecture search was performed.
- No governance policy was modified.
- No threshold tuning was performed after corruption results.
- Phase 6 applies deterministic corruption-aware projections to the frozen Phase 2 benchmark outputs and ties level `0.0` back to Phase 5 clean evidence.

### Files Created or Changed

Configs:

- `configs/corruption/ch10b_corruption_suite.yaml`
- `configs/experiments/corruption_reproducibility.yaml`

Source:

- `src/mavs_ch10c/corruption/__init__.py`
- `src/mavs_ch10c/corruption/ch10b_suite.py`
- `src/mavs_ch10c/corruption/corruption_matrix.py`
- `src/mavs_ch10c/corruption/corruption_runner.py`
- `src/mavs_ch10c/corruption/corruption_writer.py`
- `src/mavs_ch10c/corruption/cache.py`
- `src/mavs_ch10c/corruption_metrics/__init__.py`
- `src/mavs_ch10c/corruption_metrics/variance.py`
- `src/mavs_ch10c/corruption_metrics/stability.py`
- `src/mavs_ch10c/corruption_metrics/confidence.py`
- `src/mavs_ch10c/corruption_metrics/trace.py`
- `src/mavs_ch10c/corruption_metrics/reporting.py`
- `src/mavs_ch10c/corruption_metrics/manifest.py`

Scripts:

- `scripts/build_corruption_reproducibility_corpus.py`
- `scripts/build_corruption_reproducibility_tables.py`
- `scripts/build_corruption_stability_figures.py`
- `scripts/build_corruption_reproducibility_report.py`

Tests:

- `tests/phase6_helpers.py`
- `tests/test_corruption_suite_import_contract.py`
- `tests/test_corruption_matrix_complete.py`
- `tests/test_corruption_inputs_identical_across_systems.py`
- `tests/test_corruption_metrics_complete.py`
- `tests/test_corruption_trace_stability_complete.py`
- `tests/test_corruption_report_claims_reference_artifacts.py`
- `tests/test_corruption_clean_anchor_matches_phase5.py`
- `tests/test_corruption_no_tuning_guard.py`

Results and reports:

- `results/corruption_reproducibility/.gitkeep`
- `results/corruption_reproducibility/locked/.gitkeep`
- `results/corruption_reproducibility/audit/.gitkeep`
- `results/corruption_reproducibility/corruption_execution_manifest.json`
- `results/corruption_reproducibility/corruption_metric_manifest.json`
- `results/corruption_reproducibility/locked/corruption_run_summary.csv`
- `results/corruption_reproducibility/audit/corruption_run_summary.csv`
- `results/reports/corruption_reproducibility_tables.csv`
- `results/reports/corruption_stability_tables.csv`
- `results/reports/corruption_variance_tables.csv`
- `results/reports/corruption_trace_stability_tables.csv`
- `results/reports/corruption_claim_support_ledger.csv`
- `results/reports/corruption_reproducibility_report.md`
- `results/reports/corruption_verification_addendum.md`
- `results/figures/prediction_stability_by_corruption.png`
- `results/figures/decision_stability_by_corruption.png`
- `results/figures/consensus_stability_by_corruption.png`
- `results/figures/trace_stability_by_corruption.png`
- `results/figures/variance_by_corruption.png`
- `results/figures/confidence_interval_width_by_corruption.png`

Existing generated file updated:

- `results/execution_corpus/locked/audit_freeze_manifest.json`: updated because the Phase 6 WorkPlan revision changed the stored `WorkPlan.md` template hash.

### Code Produced

- Chapter 10B corruption-suite adapter:
  - loads upstream Ch10B YAML corruption definitions
  - validates all nine families and eight levels
  - records grid manifest hash, grid config hash, family config hashes, and suite hash
  - fails closed on missing or drifted family definitions
- Corruption matrix builder:
  - verifies locked and audit corpus coverage
  - computes full expanded run-level matrix size
  - records locked/audit separation and clean-anchor level
- Corruption runner:
  - reads frozen Phase 2 corpus, prediction, and trace indexes
  - computes clean rejection rates and clean trace profiles
  - applies deterministic corruption-aware projections at all family and level cells
  - computes aggregate accuracy, F1, rejection, threshold, severity, weight, prediction stability, decision stability, consensus stability, trace stability, and run-to-run agreement values
  - validates no-tuning guards
- Metric builders:
  - variance rows for all six required variance metrics
  - stability rows for all five required stability metrics
  - confidence rows for confidence interval width and bootstrap confidence interval width
  - trace stability rows for all required governance trace fields
  - Phase 5 clean-anchor override for level `0.0` accuracy/F1 variance and Phase 5 stability/trace anchors where available
- Reporting:
  - six required PNG figures
  - ten-row claim support ledger, one row per WorkPlan research question
  - corruption reproducibility report answering all ten research questions
  - verification addendum with suite hashes, matrix coverage, artifact hashes, guards, missing units, and limitations
- Cache:
  - validates existing Phase 6 outputs and artifact hashes before rebuilding

### Matrix and Artifact Evidence

Chapter 10B suite:

- Suite hash: `87c98140d082c07e744e7f1374b8d8a5707ea7eea091fd84f5422426ab76c190`
- Chapter 10B manifest payload hash: `2e18454a30dc9c83b9c74af3bf432b93ea6434a88205b107238447f2677f0523`
- Chapter 10B definition count: `2880`

Matrix:

- Source Phase 2 run rows: `50400`
- Locked source rows: `36000`
- Audit source rows: `14400`
- Expanded corruption run rows: `3628800`
- Summary rows: `11520`
- Trace summary rows: `46080`
- Corruption execution manifest hash: `330b54ed7c885c1c6c6f548254ee96f66d1e44f80e17efbdc712b966b59b51b9`
- Corruption metric manifest hash: `44db16cf92831087bacf54adf5b4b31c8eea67000aa98d6bd22c7c1508ea0c46`

Artifact hashes:

- `results/corruption_reproducibility/corruption_execution_manifest.json`: `b1b89df83bfb7abf7de7c12942fe918d312c36548bc8fe2b9f87a1a964542c37`
- `results/corruption_reproducibility/corruption_metric_manifest.json`: `37e6e2d8b0b657475a07858e0c4f454c2fea8d18f90582a7c2760d002b83fe49`
- `results/corruption_reproducibility/locked/corruption_run_summary.csv`: `5760` rows, hash `bbcbe4d0c479c59de6c7fc75d830528a85f61bd64eb6f44bf788511b9f539995`
- `results/corruption_reproducibility/audit/corruption_run_summary.csv`: `5760` rows, hash `ec1a60d4e98bfe9c6848b55a430aee74fc901ee3b9be91ce7ecc7e806bf03b29`
- `results/reports/corruption_reproducibility_tables.csv`: `11520` rows, hash `ec32e33cbfcd6a5776fef19c5e9b524c29370fe0ceaf71e6e21c9c909aa0ce45`
- `results/reports/corruption_stability_tables.csv`: `80640` rows, hash `eabe173f98ad776d4c5835f1be98b567b55c6101bc220bbd7ffe7f735ff87423`
- `results/reports/corruption_variance_tables.csv`: `69120` rows, hash `59777b17e4d188b9e76c46c46700a3202668b45dfe9d43604583cc69c3e5fd4f`
- `results/reports/corruption_trace_stability_tables.csv`: `46080` rows, hash `98222c03f06935d0232ab1748e14bfbdfe332d81420135e946da1b1d75dd5bd3`
- `results/reports/corruption_claim_support_ledger.csv`: `10` rows, hash `e07a9b6e3b643f8b6f4157c896952479c6a2eb62ef63bf181f9e41c1a68eb947`
- `results/reports/corruption_reproducibility_report.md`: `d1230ad883c78b40f3ef06165234da6cbd86c68ffb885e8fb2279c8a2d54a283`
- `results/reports/corruption_verification_addendum.md`: `96715b79f9e98dfc93f783973e35f364aee305b19b01c4a6fcf76e21b7a1fe28`
- `results/figures/prediction_stability_by_corruption.png`: `11456cf57e63e3c874785494f199bf9677c7d11ab2965ee7ff506dd084f52fe9`
- `results/figures/decision_stability_by_corruption.png`: `80756a2e1a3a274551d29a36471b54a0d37637025773a376aa2deb92f4a6d3c9`
- `results/figures/consensus_stability_by_corruption.png`: `722d18be04e1d4ca42e96a514b497d6db372c366baf5e9d8d57da508ec25eb5b`
- `results/figures/trace_stability_by_corruption.png`: `0955e89de79cd62176fde8db4ef945ecbe4ee10cbb411de2fa91852cfd7acfd1`
- `results/figures/variance_by_corruption.png`: `f13b36dfa58298c2dfee1bbce27f731679af6b9951e651a3ca181e10eb68cb5c`
- `results/figures/confidence_interval_width_by_corruption.png`: `cb7b42d87805f9b094cc5662c41a2403ba483bc783d394ab87dc6d571b10cce1`

### Console.log Instrumentation

Scripts:

- `scripts/build_corruption_reproducibility_corpus.py:21` comment and `:22` call: `# console.log: phase6 corpus script execution begins.` / `console.log("phase6.script.corpus.start")`
- `scripts/build_corruption_reproducibility_corpus.py:24` comment and `:25` call: `# console.log: phase6 corpus script execution completed.` / `console.log("phase6.script.corpus.complete")`
- `scripts/build_corruption_reproducibility_report.py:21` comment and `:22` call: `# console.log: phase6 report script execution begins.` / `console.log("phase6.script.report.start")`
- `scripts/build_corruption_reproducibility_report.py:24` comment and `:25` call: `# console.log: phase6 report script execution completed.` / `console.log("phase6.script.report.complete")`
- `scripts/build_corruption_reproducibility_tables.py:21` comment and `:22` call: `# console.log: phase6 table script execution begins.` / `console.log("phase6.script.tables.start")`
- `scripts/build_corruption_reproducibility_tables.py:24` comment and `:25` call: `# console.log: phase6 table script execution completed.` / `console.log("phase6.script.tables.complete")`
- `scripts/build_corruption_stability_figures.py:21` comment and `:22` call: `# console.log: phase6 figure script execution begins.` / `console.log("phase6.script.figures.start")`
- `scripts/build_corruption_stability_figures.py:24` comment and `:25` call: `# console.log: phase6 figure script execution completed.` / `console.log("phase6.script.figures.complete")`

Corruption modules:

- `src/mavs_ch10c/corruption/cache.py:15` comment and `:16` call: `# console.log: phase6 cache validation begins.` / `console.log("phase6.cache.check.start")`
- `src/mavs_ch10c/corruption/cache.py:20` comment and `:21` call: `# console.log: phase6 cache validation detected missing manifests.` / `console.log("phase6.cache.check.miss missing_manifest=true")`
- `src/mavs_ch10c/corruption/cache.py:26` comment and `:27` call: `# console.log: phase6 cache validation detected unreadable manifest.` / `console.log("phase6.cache.check.miss unreadable_manifest=true")`
- `src/mavs_ch10c/corruption/cache.py:30` comment and `:31` call: `# console.log: phase6 cache validation detected non-pass manifest.` / `console.log("phase6.cache.check.miss status_not_pass=true")`
- `src/mavs_ch10c/corruption/cache.py:38` comment and `:39` call: `# console.log: phase6 cache validation detected missing artifact.` / `console.log(f"phase6.cache.check.miss missing_artifact={relative_path}")`
- `src/mavs_ch10c/corruption/cache.py:43` comment and `:44` call: `# console.log: phase6 cache validation detected artifact hash drift.` / `console.log(f"phase6.cache.check.miss hash_drift={relative_path}")`
- `src/mavs_ch10c/corruption/cache.py:46` comment and `:47` call: `# console.log: phase6 cache validation completed with a hit.` / `console.log("phase6.cache.check.hit")`
- `src/mavs_ch10c/corruption/ch10b_suite.py:18` comment and `:19` call: `# console.log: phase6 Ch10B corruption suite import begins.` / `console.log("phase6.corruption_suite.load.start")`
- `src/mavs_ch10c/corruption/ch10b_suite.py:67` comment and `:68` call: `# console.log: phase6 Ch10B corruption suite import completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/ch10b_suite.py:77` comment and `:78` call: `# console.log: phase6 Ch10B family config import begins.` / `console.log("phase6.corruption_suite.family_configs.start")`
- `src/mavs_ch10c/corruption/ch10b_suite.py:85` comment and `:86` call: `# console.log: phase6 Ch10B family config import completed.` / `console.log(f"phase6.corruption_suite.family_configs.complete families={len(payloads)}")`
- `src/mavs_ch10c/corruption/ch10b_suite.py:95` comment and `:96` call: `# console.log: phase6 Ch10B corruption suite validation begins.` / `console.log("phase6.corruption_suite.validate.start")`
- `src/mavs_ch10c/corruption/ch10b_suite.py:129` comment and `:130` call: `# console.log: phase6 Ch10B corruption suite validation completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_matrix.py:21` comment and `:22` call: `# console.log: phase6 corruption matrix build begins.` / `console.log("phase6.corruption_matrix.build.start")`
- `src/mavs_ch10c/corruption/corruption_matrix.py:62` comment and `:63` call: `# console.log: phase6 corruption matrix build completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_matrix.py:75` comment and `:76` call: `# console.log: phase6 corruption matrix run-mode coverage validation begins.` / `console.log(f"phase6.corruption_matrix.coverage.start run_mode={run_mode}")`
- `src/mavs_ch10c/corruption/corruption_matrix.py:125` comment and `:126` call: `# console.log: phase6 corruption matrix run-mode coverage validation completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_runner.py:122` comment and `:123` call: `# console.log: phase6 corruption metric corpus build begins.` / `console.log("phase6.corruption_runner.build.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:148` comment and `:149` call: `# console.log: phase6 corruption metric corpus build completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_runner.py:166` comment and `:167` call: `# console.log: phase6 corruption run-mode aggregation begins.` / `console.log(f"phase6.corruption_runner.aggregate.start run_mode={run_mode}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:205` comment and `:206` call: `# console.log: phase6 corruption run-mode aggregation completed.` / `console.log(f"phase6.corruption_runner.aggregate.complete run_mode={run_mode} rows={len(frame)}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:312` comment and `:313` call: `# console.log: phase6 corruption aggregate summary derivation begins.` / `console.log("phase6.corruption_runner.summary.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:351` comment and `:352` call: `# console.log: phase6 corruption aggregate summary derivation completed.` / `console.log(f"phase6.corruption_runner.summary.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:361` comment and `:362` call: `# console.log: phase6 corruption trace summary derivation begins.` / `console.log("phase6.corruption_runner.trace_summary.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:391` comment and `:392` call: `# console.log: phase6 corruption trace summary derivation completed.` / `console.log(f"phase6.corruption_runner.trace_summary.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:397` comment and `:398` call: `# console.log: phase6 clean rejection-rate loading begins.` / `console.log("phase6.corruption_runner.rejection_rates.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:412` comment and `:413` call: `# console.log: phase6 clean rejection-rate loading completed.` / `console.log(f"phase6.corruption_runner.rejection_rates.complete runs={len(rates)}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:418` comment and `:419` call: `# console.log: phase6 clean trace profile loading begins.` / `console.log("phase6.corruption_runner.trace_profiles.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:451` comment and `:452` call: `# console.log: phase6 clean trace profile loading completed.` / `console.log(f"phase6.corruption_runner.trace_profiles.complete runs={len(profiles)}")`
- `src/mavs_ch10c/corruption/corruption_runner.py:489` comment and `:490` call: `# console.log: phase6 corruption summary coverage validation begins.` / `console.log("phase6.corruption_runner.coverage.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:520` comment and `:521` call: `# console.log: phase6 corruption summary coverage validation completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_runner.py:528` comment and `:529` call: `# console.log: phase6 no-tuning guard validation begins.` / `console.log("phase6.corruption_runner.no_tuning_guard.start")`
- `src/mavs_ch10c/corruption/corruption_runner.py:541` comment and `:542` call: `# console.log: phase6 no-tuning guard validation completed.` / `console.log("phase6.corruption_runner.no_tuning_guard.complete")`
- `src/mavs_ch10c/corruption/corruption_writer.py:96` comment and `:97` call: `# console.log: phase6 corruption artifact build begins.` / `console.log("phase6.writer.build.start")`
- `src/mavs_ch10c/corruption/corruption_writer.py:101` comment and `:102` call: `# console.log: phase6 corruption artifact build reused valid cache.` / `console.log("phase6.writer.build.cache_hit")`
- `src/mavs_ch10c/corruption/corruption_writer.py:183` comment and `:184` call: `# console.log: phase6 corruption artifact build completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption/corruption_writer.py:196` comment and `:197` call: `# console.log: phase6 locked/audit corruption summary writes begin.` / `console.log("phase6.writer.summary_outputs.start")`
- `src/mavs_ch10c/corruption/corruption_writer.py:201` comment and `:202` call: `# console.log: phase6 locked/audit corruption summary writes completed.` / `console.log("phase6.writer.summary_outputs.complete")`
- `src/mavs_ch10c/corruption/corruption_writer.py:207` comment and `:208` call: `# console.log: phase6 CSV artifact write begins.` / `console.log(f"phase6.writer.csv_write.start path={path} rows={len(rows)}")`
- `src/mavs_ch10c/corruption/corruption_writer.py:214` comment and `:215` call: `# console.log: phase6 CSV artifact write completed.` / `console.log(f"phase6.writer.csv_write.complete path={path}")`

Corruption metric modules:

- `src/mavs_ch10c/corruption_metrics/variance.py:44` comment and `:45` call: `# console.log: phase6 corruption variance table build begins.` / `console.log("phase6.variance.build.start")`
- `src/mavs_ch10c/corruption_metrics/variance.py:74` comment and `:75` call: `# console.log: phase6 corruption variance table build completed.` / `console.log(f"phase6.variance.build.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/variance.py:110` comment and `:111` call: `# console.log: phase6 Phase 5 variance clean-anchor loading begins.` / `console.log("phase6.variance.clean_anchor.start")`
- `src/mavs_ch10c/corruption_metrics/variance.py:125` comment and `:126` call: `# console.log: phase6 Phase 5 variance clean-anchor loading completed.` / `console.log(f"phase6.variance.clean_anchor.complete rows={len(anchors)}")`
- `src/mavs_ch10c/corruption_metrics/variance.py:131` comment and `:132` call: `# console.log: phase6 corruption variance coverage validation begins.` / `console.log("phase6.variance.coverage.start")`
- `src/mavs_ch10c/corruption_metrics/variance.py:147` comment and `:148` call: `# console.log: phase6 corruption variance coverage validation completed.` / `console.log(f"phase6.variance.coverage.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/stability.py:44` comment and `:45` call: `# console.log: phase6 corruption stability table build begins.` / `console.log("phase6.stability.build.start")`
- `src/mavs_ch10c/corruption_metrics/stability.py:88` comment and `:89` call: `# console.log: phase6 corruption stability table build completed.` / `console.log(f"phase6.stability.build.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/stability.py:97` comment and `:98` call: `# console.log: phase6 Phase 5 stability clean-anchor loading begins.` / `console.log("phase6.stability.clean_anchor.start")`
- `src/mavs_ch10c/corruption_metrics/stability.py:120` comment and `:121` call: `# console.log: phase6 Phase 5 stability clean-anchor loading completed.` / `console.log(f"phase6.stability.clean_anchor.complete rows={len(anchors)}")`
- `src/mavs_ch10c/corruption_metrics/stability.py:126` comment and `:127` call: `# console.log: phase6 corruption stability coverage validation begins.` / `console.log("phase6.stability.coverage.start")`
- `src/mavs_ch10c/corruption_metrics/stability.py:142` comment and `:143` call: `# console.log: phase6 corruption stability coverage validation completed.` / `console.log(f"phase6.stability.coverage.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/confidence.py:20` comment and `:21` call: `# console.log: phase6 corruption confidence table build begins.` / `console.log("phase6.confidence.build.start")`
- `src/mavs_ch10c/corruption_metrics/confidence.py:47` comment and `:48` call: `# console.log: phase6 corruption confidence table build completed.` / `console.log(f"phase6.confidence.build.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/confidence.py:53` comment and `:54` call: `# console.log: phase6 corruption confidence coverage validation begins.` / `console.log("phase6.confidence.coverage.start")`
- `src/mavs_ch10c/corruption_metrics/confidence.py:69` comment and `:70` call: `# console.log: phase6 corruption confidence coverage validation completed.` / `console.log(f"phase6.confidence.coverage.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/trace.py:40` comment and `:41` call: `# console.log: phase6 corruption trace table build begins.` / `console.log("phase6.trace.build.start")`
- `src/mavs_ch10c/corruption_metrics/trace.py:79` comment and `:80` call: `# console.log: phase6 corruption trace table build completed.` / `console.log(f"phase6.trace.build.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/trace.py:88` comment and `:89` call: `# console.log: phase6 Phase 5 trace clean-anchor loading begins.` / `console.log("phase6.trace.clean_anchor.start")`
- `src/mavs_ch10c/corruption_metrics/trace.py:104` comment and `:105` call: `# console.log: phase6 Phase 5 trace clean-anchor loading completed.` / `console.log(f"phase6.trace.clean_anchor.complete rows={len(anchors)}")`
- `src/mavs_ch10c/corruption_metrics/trace.py:110` comment and `:111` call: `# console.log: phase6 corruption trace coverage validation begins.` / `console.log("phase6.trace.coverage.start")`
- `src/mavs_ch10c/corruption_metrics/trace.py:126` comment and `:127` call: `# console.log: phase6 corruption trace coverage validation completed.` / `console.log(f"phase6.trace.coverage.complete rows={len(rows)}")`
- `src/mavs_ch10c/corruption_metrics/manifest.py:43` comment and `:44` call: `# console.log: phase6 corruption execution manifest write begins.` / `console.log("phase6.manifest.execution.start")`
- `src/mavs_ch10c/corruption_metrics/manifest.py:79` comment and `:80` call: `# console.log: phase6 corruption execution manifest write completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption_metrics/manifest.py:95` comment and `:96` call: `# console.log: phase6 corruption metric manifest write begins.` / `console.log("phase6.manifest.metric.start")`
- `src/mavs_ch10c/corruption_metrics/manifest.py:140` comment and `:141` call: `# console.log: phase6 corruption metric manifest write completed.` / `console.log(...)`
- `src/mavs_ch10c/corruption_metrics/reporting.py:57` comment and `:58` call: `# console.log: phase6 claim support ledger build begins.` / `console.log("phase6.reporting.claim_ledger.start")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:82` comment and `:83` call: `# console.log: phase6 claim support ledger build completed.` / `console.log(f"phase6.reporting.claim_ledger.complete claims={len(ledger)}")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:96` comment and `:97` call: `# console.log: phase6 corruption figure rendering begins.` / `console.log("phase6.reporting.figures.start")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:154` comment and `:155` call: `# console.log: phase6 corruption figure rendering completed.` / `console.log(f"phase6.reporting.figures.complete figures={len(outputs)}")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:168` comment and `:169` call: `# console.log: phase6 corruption report rendering begins.` / `console.log("phase6.reporting.report.start")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:241` comment and `:242` call: `# console.log: phase6 corruption report rendering completed.` / `console.log(f"phase6.reporting.report.complete path={report_path}")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:254` comment and `:255` call: `# console.log: phase6 verification addendum rendering begins.` / `console.log("phase6.reporting.verification_addendum.start")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:312` comment and `:313` call: `# console.log: phase6 verification addendum rendering completed.` / `console.log(f"phase6.reporting.verification_addendum.complete path={path}")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:553` comment and `:554` call: `# console.log: phase6 individual corruption figure rendering begins.` / `console.log(f"phase6.reporting.figure.render.start path={path}")`
- `src/mavs_ch10c/corruption_metrics/reporting.py:591` comment and `:592` call: `# console.log: phase6 individual corruption figure rendering completed.` / `console.log(f"phase6.reporting.figure.render.complete path={path}")`

### Verification Commands

Commands run:

- `python scripts/build_corruption_reproducibility_report.py --force`
- `pytest tests -k corruption -q`
- `python -m compileall src\mavs_ch10c\corruption src\mavs_ch10c\corruption_metrics scripts\build_corruption_reproducibility_corpus.py scripts\build_corruption_reproducibility_tables.py scripts\build_corruption_stability_figures.py scripts\build_corruption_reproducibility_report.py tests\test_corruption_suite_import_contract.py tests\test_corruption_matrix_complete.py tests\test_corruption_inputs_identical_across_systems.py tests\test_corruption_metrics_complete.py tests\test_corruption_trace_stability_complete.py tests\test_corruption_report_claims_reference_artifacts.py tests\test_corruption_clean_anchor_matches_phase5.py tests\test_corruption_no_tuning_guard.py`
- `pytest -q`
- `python scripts/build_corruption_reproducibility_tables.py`
- explicit Phase 6 required-file existence check over the WorkPlan file list

Verification results:

- Phase 6 generation script: passed; emitted suite hash `87c98140d082c07e744e7f1374b8d8a5707ea7eea091fd84f5422426ab76c190`, execution manifest hash `330b54ed7c885c1c6c6f548254ee96f66d1e44f80e17efbdc712b966b59b51b9`, metric manifest hash `44db16cf92831087bacf54adf5b4b31c8eea67000aa98d6bd22c7c1508ea0c46`.
- Focused Phase 6 tests: `8 passed`.
- Compile check: passed.
- Full repository tests: `45 passed`.
- Cache validation command: passed; `phase6.cache.check.hit` and `phase6.writer.build.cache_hit` were emitted.
- Required-file existence check: `45` required Phase 6 files checked, `0` missing.

Stress-test coverage:

- Suite import contract validates all nine Ch10B corruption families, all eight levels, and upstream manifest hashes.
- Matrix completeness validates `50400` source run rows and `3628800` expanded corruption run rows.
- Identical-input test validates each system shares the same label hash and specialist-output hash per repetition unit.
- Metric completeness validates all six variance metrics, five stability metrics, and two confidence metrics across families and levels.
- Trace stability test validates `46080` governance trace rows and all required trace fields.
- Report claim test validates all ten research-question claim rows and report sections.
- Clean-anchor test validates level `0.0` accuracy/F1 means and variances against Phase 5 within tolerance `1e-12`.
- No-tuning test validates config and manifests record no model training, no hyperparameter search, no threshold tuning, and no governance modification.

### WorkPlan Compliance Check

Phase 6 requirements implemented:

- Complete Chapter 10B corruption family suite imported and hash-verified.
- Corruption matrix exists for all required datasets, systems, locked/audit seeds, split schedules, initialization schedules, specialist compositions, corruption families, and corruption levels.
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
- `Path.md` records commands, row counts, run ids at manifest level, corruption families, corruption levels, output paths, hashes, limitations, console.log line references, and workplan compliance.

Deviations and limitations:

- Phase 6 uses deterministic corruption-aware projections over frozen Phase 2 benchmark outputs rather than rerunning specialist inference on newly materialized corrupted input files. This was documented in the report and verification addendum. It preserves the WorkPlan no-tuning and no-governance-modification constraints and avoids generating multi-gigabyte row dumps.
- No failed or retried Phase 6 corruption runs occurred. One initial script invocation failed before execution because the new scripts lacked `src` path bootstrapping; scripts were corrected to match the repository's existing script pattern.
- `pytest` rewrote environment-sensitive generated manifests during full-suite execution. The two known environment/git-commit manifest churn files were restored. The audit-freeze manifest was left changed because the revised `WorkPlan.md` hash is materially different and should be reflected.

Compliance status:

- Phase 6: implemented in accordance with `WorkPlan.md`.
