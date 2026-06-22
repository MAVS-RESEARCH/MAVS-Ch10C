"""Source location for completed Chapter 10A and Chapter 10B repositories."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import load_json_config


@dataclass(frozen=True)
class SourceResolution:
    source_id: str
    path: Path
    origin: str
    repo_url: str
    commit: str


def _run_git(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def _git_commit(path: Path) -> str:
    try:
        return _run_git(["rev-parse", "HEAD"], cwd=path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _candidate_paths(repo_root: Path, config: dict[str, Any]) -> list[tuple[Path, str]]:
    candidates: list[tuple[Path, str]] = []
    env_var = config.get("env_var")
    if isinstance(env_var, str) and os.environ.get(env_var):
        candidates.append((Path(os.environ[env_var]), f"env:{env_var}"))

    for raw_candidate in config.get("local_candidates", []):
        candidate = Path(str(raw_candidate))
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        candidates.append((candidate, "configured_candidate"))

    clone_config = config.get("clone", {})
    clone_path = Path(str(clone_config.get("path", "")))
    if clone_path:
        if not clone_path.is_absolute():
            clone_path = repo_root / clone_path
        candidates.append((clone_path, "managed_clone"))

    return candidates


def load_source_config(config_path: Path) -> dict[str, Any]:
    # console.log: phase1 source config loading begins.
    console.log(f"phase1.source_config.load path={config_path}")
    config = load_json_config(config_path)
    if "source_id" not in config or "repo_url" not in config:
        raise ValueError(f"Source config is missing source_id or repo_url: {config_path}")
    return config


def resolve_source(repo_root: Path, config_path: Path) -> SourceResolution:
    """Resolve a Chapter source path, cloning only when explicitly configured."""

    config = load_source_config(config_path)
    source_id = str(config["source_id"])

    # console.log: phase1 source candidate scan begins.
    console.log(f"phase1.source.resolve.start source={source_id}")
    for candidate, origin in _candidate_paths(repo_root, config):
        if candidate.exists() and (candidate / ".git").exists():
            commit = _git_commit(candidate)
            # console.log: phase1 source candidate resolved.
            console.log(
                f"phase1.source.resolve.found source={source_id} origin={origin} path={candidate}"
            )
            return SourceResolution(
                source_id=source_id,
                path=candidate.resolve(),
                origin=origin,
                repo_url=str(config["repo_url"]),
                commit=commit,
            )

    clone_config = config.get("clone", {})
    if not clone_config.get("enabled", False):
        raise FileNotFoundError(f"No usable source found for {source_id}")

    clone_path = Path(str(clone_config["path"]))
    if not clone_path.is_absolute():
        clone_path = repo_root / clone_path
    clone_path.parent.mkdir(parents=True, exist_ok=True)
    depth = int(clone_config.get("depth", 1))

    # console.log: phase1 managed clone begins.
    console.log(
        f"phase1.source.clone.start source={source_id} repo={config['repo_url']} path={clone_path}"
    )
    _run_git(["clone", "--depth", str(depth), str(config["repo_url"]), str(clone_path)])
    commit = _git_commit(clone_path)
    # console.log: phase1 managed clone completed.
    console.log(f"phase1.source.clone.complete source={source_id} commit={commit}")
    return SourceResolution(
        source_id=source_id,
        path=clone_path.resolve(),
        origin="managed_clone",
        repo_url=str(config["repo_url"]),
        commit=commit,
    )
