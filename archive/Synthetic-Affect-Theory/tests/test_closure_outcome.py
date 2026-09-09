# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Dated note, 2026-08-14: the honesty hinge. A ClosureDecision does not
grade itself — Loop._judge_pending() scores the *previous* cycle's
decision against *this* cycle's gap, one cycle late, every time. Ported
from CrystalCore.OS/synthetic-affect; see core/closure.py and core/loop.py
for the defect this covers (outcome stamped at decide-time in PR #1,
merged 2026-08-12, which made a closure-success-rate computed from the
logs read 100% forever)."""
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.closure import ClosurePolicy
from core.loop import Loop


def test_decision_does_not_grade_itself():
    # A fresh decision's outcome is unresolved until a later cycle judges it.
    assert ClosurePolicy().decide("closed").outcome == "pending"


def test_success_rate_is_none_before_anything_is_judged():
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=os.path.join(td, "loop.jsonl"))
        loop.run_cycle(expected="deploy", actual="pending")
        # One decision made, nothing judged yet — an unmeasured rate is not zero.
        assert loop.closure_success_rate() is None


def test_success_rate_reflects_worked_and_failed_judgements():
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=os.path.join(td, "loop.jsonl"))
        loop.run_cycle(expected="deploy", actual="pending")  # decision 1: pending
        loop.run_cycle(expected="deploy", actual="deploy")  # gap gone -> decision 1 "worked"
        loop.run_cycle(expected="deploy", actual="rollback")  # gap reopened -> decision 2 "failed"
        loop.run_cycle(expected="deploy", actual="deploy")  # gap gone -> decision 3 "worked"

        entries = [e for e in loop.logger.read_all() if e["op"] == "closure_outcome"]
        assert [e["data"]["outcome"] for e in entries] == ["worked", "failed", "worked"]
        assert loop.closure_success_rate() == 2 / 3


def test_final_decision_of_a_run_stays_pending_until_judged():
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=os.path.join(td, "loop.jsonl"))
        result = loop.run_cycle(expected="deploy", actual="pending")
        # Nothing has judged this cycle's decision yet.
        assert result["decision"].outcome == "pending"
