# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""F1/F2 fixes: cycle vs ts both carry information; no wall-clock;
re-runs are byte-identical."""
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.loop import Loop


def _run(log_path):
    loop = Loop(store_path=":memory:", log_path=str(log_path))
    loop.run_cycle(expected="deploy", actual="pending", event={"state": "pending"})
    loop.run_cycle(expected="deploy", actual="deploy", event={"state": "deploy"})
    return loop


def test_cycle_vs_ts_both_carry_information():
    with tempfile.TemporaryDirectory() as td:
        loop = _run(os.path.join(td, "loop.jsonl"))
        entries = loop.logger.read_all()
        # Cycle 1: track, gap_opened, label, closure — nothing pending yet.
        # Cycle 2: track, gap_none, closure_outcome (judging cycle 1's
        # decision), label, closure — five lines once a decision is there
        # to be judged (dated note, 2026-08-14, core/loop.py).
        assert [e["cycle"] for e in entries] == [1, 1, 1, 1, 2, 2, 2, 2, 2]
        assert [e["ts"] for e in entries] == list(range(1, 10))
        assert [e["op"] for e in entries] == [
            "track", "gap_opened", "label", "closure",
            "track", "gap_none", "closure_outcome", "label", "closure",
        ]
        # Not identical — cycle is cycle, ts is measure
        assert any(e["ts"] != e["cycle"] for e in entries)
        assert loop.cycle == 2


def test_rerun_is_byte_identical():
    with tempfile.TemporaryDirectory() as td:
        p1 = os.path.join(td, "a.jsonl")
        p2 = os.path.join(td, "b.jsonl")
        _run(p1)
        _run(p2)
        assert pathlib.Path(p1).read_bytes() == pathlib.Path(p2).read_bytes()


def test_empty_event_dict_is_still_tracked():
    # event={} is a real (empty) event, distinct from event omitted (None).
    # `if event:` treated both the same and silently dropped the track().
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=os.path.join(td, "loop.jsonl"))
        loop.run_cycle(expected="a", actual="b", event={})

        assert len(loop.store.history) == 1
        assert loop.store.history[0] == {}

        entries = loop.logger.read_all()
        assert [e["op"] for e in entries] == ["track", "gap_opened", "label", "closure"]
        assert entries[0]["data"] == {}


def test_omitted_event_is_not_tracked():
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=os.path.join(td, "loop.jsonl"))
        loop.run_cycle(expected="a", actual="b")

        assert loop.store.history == []
        entries = loop.logger.read_all()
        assert [e["op"] for e in entries] == ["gap_opened", "label", "closure"]
