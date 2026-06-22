"""MAVS Chapter 10C reproducibility benchmark package."""

from __future__ import annotations

import os
from datetime import datetime, timezone

__all__ = ["__version__", "console"]

__version__ = "0.1.0"


class _ResearchConsole:
    """Small console object that exposes literal console.log calls in Python."""

    def __init__(self) -> None:
        self._seen: dict[str, int] = {}
        self._max_repeated = int(os.environ.get("MAVS_CH10C_MAX_REPEATED_LOGS", "8"))

    def log(self, message: str) -> None:
        key = message.split(" ", 1)[0]
        count = self._seen.get(key, 0)
        self._seen[key] = count + 1
        if count == self._max_repeated:
            timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
            print(
                f"[MAVS-Ch10C][{timestamp}] {key} repeated log limit reached; suppressing further repeated output",
                flush=True,
            )
            return
        if count > self._max_repeated:
            return
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        print(f"[MAVS-Ch10C][{timestamp}] {message}", flush=True)


console = _ResearchConsole()
