# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Structured JSONL cycle log (gap opened, label, strategy, outcome)
Deterministic ts = cycle counter
"""
from __future__ import annotations
import json
import pathlib
from typing import Any, Dict

class CycleLogger:
    def __init__(self, path: str | pathlib.Path):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.cycle = 0
        # clear on init
        self.path.write_text("", encoding="utf-8")

    def _next(self) -> int:
        self.cycle += 1
        return self.cycle

    def log(self, op: str, data: Dict[str, Any]) -> None:
        entry = {"cycle": self._next(), "op": op, "ts": self.cycle, "data": data}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    def read_all(self):
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(l) for l in lines if l.strip()]
