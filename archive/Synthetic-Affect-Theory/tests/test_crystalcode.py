# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""F8 fix: primitives track()/detect_gap()/label_affect()/close_with() tested directly.
F3 fix: Runtime object prevents singleton cross-talk."""
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core import crystalcode
from core.affect import AffectModel
from core.closure import ClosurePolicy
from core.gap import GapDetector
from core.log import CycleLogger
from core.state import PersistentStateStore


def test_crystalcode_operators_directly():
    with tempfile.TemporaryDirectory() as td:
        store = PersistentStateStore(":memory:")
        gd = GapDetector()
        am = AffectModel(window=10)
        cp = ClosurePolicy()
        lg = CycleLogger(os.path.join(td, "c.jsonl"))

        rt = crystalcode.init_runtime(store, gd, am, cp, lg)
        assert isinstance(rt, crystalcode.Runtime)

        crystalcode.track({"q": "test"})
        assert len(store.history) == 1

        gap = crystalcode.detect_gap("expected", "actual")
        assert gap is not None
        assert gap.expected == "expected"

        label = crystalcode.label_affect([gap])
        assert label in ("stalled", "uncertain", "reopened", "converging", "closed")

        decision = crystalcode.close_with(label, {"test": True})
        assert decision.strategy in ("rephrase", "ask", "switch_tool", "escalate", "stop")

        entries = lg.read_all()
        assert len(entries) == 4
        assert entries[0]["op"] == "track"
        assert entries[1]["op"] == "gap_opened"
        assert entries[2]["op"] == "label"
        assert entries[3]["op"] == "closure"


def test_runtime_isolation():
    # F3: Runtime object prevents cross-talk
    with tempfile.TemporaryDirectory() as td:
        s1 = PersistentStateStore(":memory:")
        rt1 = crystalcode.Runtime(s1, GapDetector(), AffectModel(), ClosurePolicy(),
                                  CycleLogger(os.path.join(td, "1.jsonl")))

        s2 = PersistentStateStore(":memory:")
        rt2 = crystalcode.Runtime(s2, GapDetector(), AffectModel(), ClosurePolicy(),
                                  CycleLogger(os.path.join(td, "2.jsonl")))

        rt1.track({"owner": "rt1"})
        rt2.track({"owner": "rt2"})

        assert len(s1.history) == 1 and s1.history[0]["owner"] == "rt1"
        assert len(s2.history) == 1 and s2.history[0]["owner"] == "rt2"
