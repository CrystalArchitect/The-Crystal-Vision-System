# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
PersistentStateStore — goals, expected state, history (JSON-backed).

Postulate 1 — State is Primary. Every mutation persists immediately when a
file path is given, so state survives process exit with no explicit save()
call (F5). `store_path=":memory:"` discards at exit by design.

Australian spelling: labelled, behaviour, initialised.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List


class PersistentStateStore:
    def __init__(self, path: str | pathlib.Path = ":memory:"):
        self.path = pathlib.Path(path) if str(path) != ":memory:" else None
        self.goals: List[str] = []
        self.expected: Dict[str, Any] = {}
        self.actual: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
        if self.path and self.path.exists():
            self.load()

    def set_goal(self, goal: str) -> None:
        self.goals.append(goal)
        self.save()

    def set_expected(self, expected: Dict[str, Any]) -> None:
        self.expected = expected
        self.save()

    def update_actual(self, actual: Dict[str, Any]) -> None:
        self.actual = actual
        self.save()

    def record(self, event: Dict[str, Any]) -> None:
        self.history.append(event)
        self.save()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goals": self.goals,
            "expected": self.expected,
            "actual": self.actual,
            "history": self.history,
        }

    def save(self) -> None:
        # :memory: mode (path is None) discards at exit by design
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    def load(self) -> None:
        if self.path and self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.goals = data.get("goals", [])
            self.expected = data.get("expected", {})
            self.actual = data.get("actual", {})
            self.history = data.get("history", [])
