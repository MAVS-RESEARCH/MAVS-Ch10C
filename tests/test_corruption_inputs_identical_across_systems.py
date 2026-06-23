from __future__ import annotations

import pandas as pd

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_inputs_identical_across_systems() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    group_columns = [
        "dataset_id",
        "execution_seed",
        "split_schedule_id",
        "initialization_schedule_id",
        "specialist_composition_id",
    ]

    for run_mode, relative_path in config["source_corpus_paths"].items():
        frame = pd.read_csv(root / relative_path, dtype=str, keep_default_na=False)
        grouped = frame.groupby(group_columns, dropna=False)
        assert grouped["system_id"].nunique().eq(len(config["systems"])).all()
        assert grouped["label_hash"].nunique().eq(1).all()
        assert grouped["specialist_output_hash"].nunique().eq(1).all()
        assert set(frame["run_mode"]) == {run_mode}

