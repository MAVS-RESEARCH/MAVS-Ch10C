"""Small append-safe cache helpers for Phase 2 corpus generation."""

from __future__ import annotations

from pathlib import Path

from mavs_ch10c import console


class CorpusCache:
    """Tracks completed run ids for resumable corpus execution."""

    def __init__(self, cache_path: Path) -> None:
        self.cache_path = cache_path
        self.completed_run_ids = self._load()

    def _load(self) -> set[str]:
        # console.log: phase2 cache load begins.
        console.log(f"phase2.cache.load.start path={self.cache_path}")
        if not self.cache_path.exists():
            # console.log: phase2 cache load completed with empty cache.
            console.log("phase2.cache.load.complete entries=0")
            return set()
        entries = {
            line.strip()
            for line in self.cache_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        # console.log: phase2 cache load completed.
        console.log(f"phase2.cache.load.complete entries={len(entries)}")
        return entries

    def add(self, run_id: str) -> None:
        self.completed_run_ids.add(run_id)

    def write(self) -> None:
        # console.log: phase2 cache write begins.
        console.log(f"phase2.cache.write.start path={self.cache_path}")
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            "\n".join(sorted(self.completed_run_ids)) + "\n", encoding="utf-8"
        )
        # console.log: phase2 cache write completed.
        console.log(f"phase2.cache.write.complete entries={len(self.completed_run_ids)}")
