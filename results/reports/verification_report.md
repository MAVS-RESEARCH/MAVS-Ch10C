# MAVS Chapter 10C Verification Report

Overall status: `pass`.

## Verification Gates

### required_files_exist

Status: `pass`.

Evidence: missing=none

### artifact_inventory_complete

Status: `pass`.

Evidence: entries=204 missing_categories=[] missing_artifacts=[]

### artifact_hashes_match

Status: `pass`.

Evidence: mismatches=none

### no_governance_source_drift

Status: `pass`.

Evidence: mismatches=none

### seed_registry_complete

Status: `pass`.

Evidence: locked=30 audit=20 overlap=0

### locked_audit_independence

Status: `pass`.

Evidence: seed_overlap=0 split_overlap=0

### split_partitions_disjoint

Status: `pass`.

Evidence: failures=none

### systems_and_metrics_complete

Status: `pass`.

Evidence: systems=['mean_ensemble', 'pure_mavs_gc', 'single_model', 'static_weighted_ensemble', 'veto_mavs'] missing_metrics=[]

### governance_trace_contract

Status: `pass`.

Evidence: missing_columns=none

### clean_report_claims_reference_artifacts

Status: `pass`.

Evidence: policy={'corruption_robustness_claim_made': False, 'every_claim_references_artifacts': True, 'global_superiority_claim_made': False, 'negative_neutral_mixed_results_preserved': True}

### corruption_families_levels_metrics_complete

Status: `pass`.

Evidence: families=9 levels=[0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0] missing_metrics=[]

### corruption_claims_reference_artifacts

Status: `pass`.

Evidence: claims=10 missing_artifacts=none

### corruption_clean_anchor_matches_phase5

Status: `pass`.

Evidence: checked=2880 mismatches=0

### final_run_guards

Status: `pass`.

Evidence: clean_classification={'audit': 'final_independent_audit_repeated_execution', 'exploratory_results_used': False, 'locked': 'final_frozen_repeated_execution', 'training_diagnostics_used_as_final_evidence': False}

### path_md_complete

Status: `pass`.

Evidence: missing_terms=none

### corruption_verification_addendum_pass

Status: `pass`.

Evidence: overall status and missing-unit statement checked

## Final Evidence Policy

Final clean evidence is generated from the frozen Phase 2-5 matrices. Final corruption evidence is generated from the frozen Phase 6 matrix. Smoke, exploratory, training, validation, and calibration diagnostics are not used as final evidence.
