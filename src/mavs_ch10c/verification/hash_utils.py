"""Hashing and simple config-loading utilities for Chapter 10C."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def load_json_config(path: Path) -> dict[str, Any]:
    """Load JSON-formatted YAML config files used by this repository."""

    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(data: Any) -> str:
    """Return deterministic JSON text for hashing and manifests."""

    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True)


def sha256_text(text: str) -> str:
    """Hash text using SHA-256."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """Hash a file using SHA-256."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(data: Any) -> str:
    """Hash data after deterministic JSON serialization."""

    return sha256_text(canonical_json(data))


def write_json(path: Path, data: Any) -> str:
    """Write deterministic JSON and return its SHA-256 hash."""

    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(data) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256_text(text)


def hash_relative_files(root: Path, relative_paths: list[str]) -> dict[str, str]:
    """Hash required files relative to a source root."""

    hashes: dict[str, str] = {}
    for relative_path in relative_paths:
        path = root / relative_path
        hashes[relative_path] = sha256_file(path)
    return hashes
