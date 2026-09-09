# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""F5 fix: Postulate 1 — State is primary — must survive process exit."""
import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.state import PersistentStateStore


def test_state_persists_to_disk():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "state.json")
        s1 = PersistentStateStore(path)
        s1.set_goal("deploy")
        s1.set_expected({"version": "1"})
        s1.record({"event": "gap_opened", "id": 1})

        # New instance should load the same from disk
        s2 = PersistentStateStore(path)
        assert s2.goals == ["deploy"]
        assert s2.expected == {"version": "1"}
        assert len(s2.history) == 1
        assert s2.history[0]["event"] == "gap_opened"

        # File exists and is valid JSON
        assert os.path.exists(path)
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        assert "goals" in data and "history" in data


def test_memory_mode_does_not_create_file():
    with tempfile.TemporaryDirectory() as td:
        # Use :memory: — should not create a file
        s = PersistentStateStore(":memory:")
        s.set_goal("ephemeral")
        assert s.path is None
        # No file created in temp dir
        assert len(list(pathlib.Path(td).glob("*.json"))) == 0


def test_gap_history_survives():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "state.json")
        s1 = PersistentStateStore(path)
        for i in range(5):
            s1.record({"cycle": i, "label": "uncertain"})
        s2 = PersistentStateStore(path)
        assert len(s2.history) == 5
        assert s2.history[-1]["cycle"] == 4
