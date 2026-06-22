# MAVS Chapter 10C Reproducibility Benchmarks

This repository implements Phase 1 of the MAVS Chapter 10C reproducibility benchmark program. Chapter 10C measures whether the frozen MAVS-GC governance implementation reduces experimental variance relative to traditional aggregation systems.

## Phase 1 Scope

Phase 1 builds the repeatability foundation and import controller:

- Locate the completed Chapter 10A and Chapter 10B repositories or artifact bundles.
- Validate Chapter 10A dataset, specialist, system, and governance source contracts.
- Validate Chapter 10B hashing and verification patterns.
- Freeze seed, split, initialization, and specialist-composition schedules.
- Generate the Chapter 10C repetition grid.
- Capture environment and run manifests for auditability.

No model training is performed in Phase 1.

## Commands

Import and validate upstream foundations:

```powershell
python scripts/import_foundation.py --repo-root .
```

Build the locked and audit repetition grid:

```powershell
python scripts/build_repetition_grid.py --repo-root . --run-mode all
```

Run tests:

```powershell
python -m pytest -q
```

## Documentation

- `WorkPlan.md` defines the Chapter 10C execution contract.
- `Path.md` records implementation evidence, commands, hashes, deviations, and `console.log` audit lines.
