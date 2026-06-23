# Corruption Verification Addendum

Overall status: `pass`.

## Suite Hashes

- Suite hash: `87c98140d082c07e744e7f1374b8d8a5707ea7eea091fd84f5422426ab76c190`
- Chapter 10B grid manifest payload hash: `2e18454a30dc9c83b9c74af3bf432b93ea6434a88205b107238447f2677f0523`
- Family config hashes: `148000ea263fd10e569e38a58f7d564e7fe7757e636f303990d1a9d1f5f9b074`

## Matrix Coverage

- Source run rows: 50400
- Expected expanded run rows: 3628800
- Missing units: none.
- Locked/audit separation: preserved.

## Guards

- Training performed in Phase 6: false.
- Hyperparameter search performed: false.
- Threshold tuning after corruption: false.
- Governance-policy modification: false.
- Audit evidence used to select metrics or language: false.

## Artifact Hashes

- `results/corruption_reproducibility/audit/corruption_run_summary.csv`: `ec1a60d4e98bfe9c6848b55a430aee74fc901ee3b9be91ce7ecc7e806bf03b29`
- `results/corruption_reproducibility/corruption_execution_manifest.json`: `b1b89df83bfb7abf7de7c12942fe918d312c36548bc8fe2b9f87a1a964542c37`
- `results/corruption_reproducibility/locked/corruption_run_summary.csv`: `bbcbe4d0c479c59de6c7fc75d830528a85f61bd64eb6f44bf788511b9f539995`
- `results/figures/confidence_interval_width_by_corruption.png`: `cb7b42d87805f9b094cc5662c41a2403ba483bc783d394ab87dc6d571b10cce1`
- `results/figures/consensus_stability_by_corruption.png`: `722d18be04e1d4ca42e96a514b497d6db372c366baf5e9d8d57da508ec25eb5b`
- `results/figures/decision_stability_by_corruption.png`: `80756a2e1a3a274551d29a36471b54a0d37637025773a376aa2deb92f4a6d3c9`
- `results/figures/prediction_stability_by_corruption.png`: `11456cf57e63e3c874785494f199bf9677c7d11ab2965ee7ff506dd084f52fe9`
- `results/figures/trace_stability_by_corruption.png`: `0955e89de79cd62176fde8db4ef945ecbe4ee10cbb411de2fa91852cfd7acfd1`
- `results/figures/variance_by_corruption.png`: `f13b36dfa58298c2dfee1bbce27f731679af6b9951e651a3ca181e10eb68cb5c`
- `results/reports/corruption_claim_support_ledger.csv`: `e07a9b6e3b643f8b6f4157c896952479c6a2eb62ef63bf181f9e41c1a68eb947`
- `results/reports/corruption_reproducibility_report.md`: `d1230ad883c78b40f3ef06165234da6cbd86c68ffb885e8fb2279c8a2d54a283`
- `results/reports/corruption_reproducibility_tables.csv`: `ec32e33cbfcd6a5776fef19c5e9b524c29370fe0ceaf71e6e21c9c909aa0ce45`
- `results/reports/corruption_stability_tables.csv`: `eabe173f98ad776d4c5835f1be98b567b55c6101bc220bbd7ffe7f735ff87423`
- `results/reports/corruption_trace_stability_tables.csv`: `98222c03f06935d0232ab1748e14bfbdfe332d81420135e946da1b1d75dd5bd3`
- `results/reports/corruption_variance_tables.csv`: `59777b17e4d188b9e76c46c46700a3202668b45dfe9d43604583cc69c3e5fd4f`

## Limitations

- Corruption-aware metrics are deterministic projections over the frozen benchmark corpus and are not model-development runs.
- The addendum verifies matrix coverage, suite identity, artifact hashes, no-tuning guards, clean-anchor linkage, and claim-reference discipline.
