"""Environment capture for reproducibility manifests."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import sha256_json


def _git_commit(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return completed.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def capture_environment(repo_root: Path, command_line: list[str]) -> dict[str, Any]:
    """Capture runtime information for Phase 1 manifests."""

    # console.log: phase1 environment capture begins.
    console.log("phase1.environment.capture.start")
    payload = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "git_commit": _git_commit(repo_root),
        "command_line": command_line,
        "environment_variables": {
            key: os.environ.get(key)
            for key in ["MAVS_CH10A_ROOT", "MAVS_CH10B_ROOT", "PYTHONPATH"]
            if os.environ.get(key) is not None
        },
    }
    payload["environment_hash"] = sha256_json(payload)
    # console.log: phase1 environment capture completed.
    console.log(f"phase1.environment.capture.complete hash={payload['environment_hash']}")
    return payload
