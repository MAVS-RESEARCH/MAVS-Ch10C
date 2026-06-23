from __future__ import annotations

from mavs_ch10c.verification.hash_utils import load_json_config

from phase6_helpers import ensure_phase6_outputs, phase6_config, repo_root


def test_corruption_no_tuning_guard() -> None:
    ensure_phase6_outputs()
    root = repo_root()
    config = phase6_config()
    execution = load_json_config(root / config["output_paths"]["execution_manifest"])
    metric = load_json_config(root / config["output_paths"]["metric_manifest"])

    assert config["allow_hyperparameter_search"] is False
    assert config["allow_architecture_search"] is False
    assert config["allow_corruption_level_tuning"] is False
    assert config["allow_threshold_tuning_after_corruption"] is False
    assert config["allow_governance_policy_modification"] is False
    assert execution["training_performed"] is False
    assert execution["hyperparameter_search_performed"] is False
    assert execution["threshold_tuning_after_corruption_performed"] is False
    assert execution["governance_policy_modified"] is False
    assert metric["training_performed"] is False
    assert metric["hyperparameter_search_performed"] is False

