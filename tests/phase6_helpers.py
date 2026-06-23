from __future__ import annotations

from pathlib import Path

from mavs_ch10c.corruption.corruption_writer import build_corruption_reproducibility_outputs
from mavs_ch10c.verification.hash_utils import load_json_config


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_phase6_outputs() -> dict:
    root = repo_root()
    return build_corruption_reproducibility_outputs(root, force=False)


def phase6_config() -> dict:
    return load_json_config(repo_root() / "configs" / "experiments" / "corruption_reproducibility.yaml")

