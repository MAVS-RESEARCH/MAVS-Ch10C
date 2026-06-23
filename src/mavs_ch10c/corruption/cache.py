"""Phase 6 corruption artifact cache checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import load_json_config, sha256_file


def phase6_cache_hit(repo_root: Path, config: dict[str, Any]) -> bool:
    """Return True when all Phase 6 outputs exist and match the metric manifest."""

    # console.log: phase6 cache validation begins.
    console.log("phase6.cache.check.start")
    metric_manifest_path = repo_root / config["output_paths"]["metric_manifest"]
    execution_manifest_path = repo_root / config["output_paths"]["execution_manifest"]
    if not metric_manifest_path.exists() or not execution_manifest_path.exists():
        # console.log: phase6 cache validation detected missing manifests.
        console.log("phase6.cache.check.miss missing_manifest=true")
        return False
    try:
        manifest = load_json_config(metric_manifest_path)
    except Exception:
        # console.log: phase6 cache validation detected unreadable manifest.
        console.log("phase6.cache.check.miss unreadable_manifest=true")
        return False
    if manifest.get("status") != "pass":
        # console.log: phase6 cache validation detected non-pass manifest.
        console.log("phase6.cache.check.miss status_not_pass=true")
        return False
    required_paths = list(config["output_paths"].values()) + list(config["figure_paths"].values())
    artifact_hashes: dict[str, str] = manifest.get("artifact_hashes", {})
    for relative_path in required_paths:
        path = repo_root / relative_path
        if not path.exists():
            # console.log: phase6 cache validation detected missing artifact.
            console.log(f"phase6.cache.check.miss missing_artifact={relative_path}")
            return False
        expected_hash = artifact_hashes.get(relative_path)
        if expected_hash and sha256_file(path) != expected_hash:
            # console.log: phase6 cache validation detected artifact hash drift.
            console.log(f"phase6.cache.check.miss hash_drift={relative_path}")
            return False
    # console.log: phase6 cache validation completed with a hit.
    console.log("phase6.cache.check.hit")
    return True

