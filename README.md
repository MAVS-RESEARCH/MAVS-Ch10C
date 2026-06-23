# MAVS Chapter 10C Reproducibility Benchmarks

This repository is the MAVS Chapter 10C reproducibility artifact. It evaluates whether the frozen MAVS-GC governance implementation preserves reproducibility and stability across repeated execution, and whether those effects survive controlled corruption conditions imported from Chapter 10B.

Chapter 10C does not redefine the MAVS-GC governance algorithm. Governance source files are imported from the completed Chapter 10A repository, hashed, and checked by final verification. Chapter 10B corruption definitions are imported and hash-checked for the corruption-aware reproducibility phase.

## Current Scope

Implemented phases:

- Phase 1: upstream import validation, seed registry, split schedules, initialization schedules, specialist compositions, and repetition grid.
- Phase 2: locked and audit repeated-execution corpora with frozen run manifests, predictions, traces, and no-tuning guards.
- Phase 3: variance benchmark alignment over frozen locked and audit corpora.
- Phase 4: reproducibility metrics for variance, stability, confidence intervals, run-to-run agreement, and governance traces.
- Phase 5: clean-condition reproducibility report, tables, figures, and artifact manifest.
- Phase 6: corruption-aware reproducibility using the complete Chapter 10B corruption family and level matrix.
- Phase 7: final reproduction, artifact inventory, verification report, release gates, and final tests.

## Upstream Inputs

The release scripts expect access to completed Chapter 10A and Chapter 10B sources or artifact bundles.

Chapter 10A source resolution is configured in:

```text
configs/ch10a_import/source.yaml
```

Chapter 10B source resolution is configured in:

```text
configs/ch10b_import/source.yaml
configs/corruption/ch10b_corruption_suite.yaml
```

The import adapters can use `MAVS_CH10A_ROOT` and `MAVS_CH10B_ROOT`, adjacent local repositories, configured local paths, or managed shallow clones where enabled. The corruption suite config records the Chapter 10B corruption-suite identity and expected hashes; changes to that import contract must be deliberate and reverified.

## Setup

Use Python 3.11 or newer.

```powershell
python -m pip install -e ".[dev]"
```

Optional upstream path overrides:

```powershell
$env:MAVS_CH10A_ROOT = "C:\path\to\MAVS-Chapter-10A"
$env:MAVS_CH10B_ROOT = "C:\path\to\MAVS-Ch10B"
```

## Reproduce

Run the final one-command reproduction from the repository root:

```powershell
python scripts/reproduce_all.py --run-mode final
```

This command validates the foundation import, validates the repetition grid, reuses or validates frozen locked and audit corpora, rebuilds clean reproducibility outputs, validates corruption-aware outputs, writes the artifact inventory, and runs the final verification gate.

## Verification Commands

Hash all tracked release artifacts:

```powershell
python scripts/hash_artifacts.py
```

Run the final verification gate:

```powershell
python scripts/verify_artifacts.py
```

Run the test suite:

```powershell
pytest -q
```

Focused Phase 7 release tests:

```powershell
pytest tests/test_end_to_end_smoke.py tests/test_artifact_inventory_complete.py tests/test_final_run_guards.py tests/test_locked_audit_independence.py tests/test_no_governance_source_drift.py tests/test_path_md_complete.py tests/test_final_corruption_artifacts_complete.py tests/test_final_corruption_claims_reference_artifacts.py -q
```

## Final Evidence Policy

Final clean evidence must come from the frozen Phase 2 through Phase 5 matrices. Final corruption evidence must come from the frozen Phase 6 matrix. Final verification fails if final reports use smoke, exploratory, training, validation, calibration, tuning, or corruption-development metrics as final evidence.

The final gate also checks:

- required files and artifacts
- artifact hash consistency
- Chapter 10A governance source hash stability
- locked and audit seed independence
- split partition disjointness
- required system and metric coverage
- MAVS-GC governance trace fields
- clean report claim references
- corruption family, level, metric, and claim coverage
- Phase 6 clean-anchor equality against Phase 5 clean evidence
- `Path.md` evidence completeness

## Primary Outputs

Clean-condition outputs:

```text
results/reports/reproducibility_report.md
results/reports/reproducibility_artifact_manifest.json
results/reports/variance_tables.csv
results/reports/stability_tables.csv
results/reports/reproducibility_system_deltas.csv
results/figures/
```

Corruption-aware outputs:

```text
results/reports/corruption_reproducibility_report.md
results/reports/corruption_reproducibility_tables.csv
results/reports/corruption_stability_tables.csv
results/reports/corruption_variance_tables.csv
results/reports/corruption_trace_stability_tables.csv
results/reports/corruption_claim_support_ledger.csv
results/reports/corruption_verification_addendum.md
```

Release verification outputs:

```text
results/reports/artifact_inventory.json
results/reports/verification_report.md
```

## Documentation

- `WorkPlan.md` defines the full Chapter 10C execution contract.
- `Path.md` records implementation evidence, commands, hashes, deviations, verification results, and `console.log` audit line references.

## Current Verified Status

The Phase 7 release gate reports overall status `pass`. The latest full repository test run reported `53 passed`.
