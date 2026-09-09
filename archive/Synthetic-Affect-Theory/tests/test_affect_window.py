# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""F6 fix: windowed classifier — same-shaped input at cycle 3 and cycle 300.
F7 fix: `uncertain` reachable and tested.

Regression tests below (converging-before-stalled ordering, raw-tail-only
stalled) cover a defect that shipped in Synthetic-Affect-Theory- PR #1
(merged 2026-08-12) and was fixed by porting the already-adversarially-
verified fix from CrystalCore.OS/synthetic-affect — see core/affect.py."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.affect import AffectModel
from core.gap import Gap


def _gap(i, expected, magnitude):
    return Gap(id=i, expected=expected, actual=f"not-{expected}", magnitude=magnitude, kind="mismatch")


def test_window_sees_same_shape_at_cycle_3_and_cycle_300():
    am = AffectModel(window=10)
    stalled_tail = [_gap(1, "X", 1.0), _gap(2, "X", 1.0), _gap(3, "X", 1.0)]

    short_history = list(stalled_tail)
    long_history = [_gap(100 + i, f"old-{i % 7}", 1.0) for i in range(297)] + stalled_tail

    assert am.classify(short_history) == "stalled"
    # Window of ten, not forever — ancient history cannot drown the stalled rule
    assert am.classify(long_history) == am.classify(short_history) == "stalled"


def test_uncertain_reachable_when_gap_widens():
    am = AffectModel(window=10)
    # First gap alone — nothing to compare against yet
    assert am.classify([_gap(1, "A", 0.5)]) == "uncertain"
    # Magnitude increasing — the gap is widening
    assert am.classify([_gap(1, "A", 0.5), _gap(2, "B", 1.0)]) == "uncertain"


def test_converging_then_closed_then_reopened():
    am = AffectModel(window=10)
    g1, g2 = _gap(1, "A", 1.0), _gap(2, "B", 0.5)
    assert am.classify([g1, g2]) == "converging"
    assert am.classify([g1, g2, None]) == "closed"
    assert am.classify([g1, g2, None, _gap(3, "C", 1.0)]) == "reopened"


def test_shrinking_same_goal_run_is_converging_not_stalled():
    # The exact shape PR #1's ordering got wrong: three same-expected gaps
    # whose magnitude is falling — [1.0, 0.67, 0.33], the numbers named in
    # CrystalCore.OS/synthetic-affect's own CHRONICLE.md entry for this
    # defect. A same-goal run making progress must not be routed away from
    # a strategy that is working.
    am = AffectModel(window=10)
    run = [_gap(1, "X", 1.0), _gap(2, "X", 0.67), _gap(3, "X", 0.33)]
    assert am.classify(run) == "converging"
    # A flat run (no progress) still reaches stalled — converging requires
    # a strict decrease, so this is not a false negative introduced by the
    # reorder.
    flat = [_gap(1, "X", 1.0), _gap(2, "X", 1.0), _gap(3, "X", 1.0)]
    assert am.classify(flat) == "stalled"


def test_stalled_requires_consecutive_raw_cycles_not_filtered_gaps():
    # Gap X opens, closes, then reopens as gap X twice more. Three Gaps
    # share `expected == "X"`, but a closure sits between the first and the
    # second — this is not one continuous stall. The middle cycle already
    # earns its own `reopened` label; a version of classify() that filtered
    # closures out before counting would call the combination `stalled`
    # regardless, which is exactly the bug ported out of this file.
    am = AffectModel(window=10)
    g1 = _gap(1, "X", 1.0)
    g2 = _gap(2, "X", 1.0)
    g3 = _gap(3, "X", 1.0)

    history_after_reopen = [g1, None, g2]
    assert am.classify(history_after_reopen) == "reopened"

    history_one_more_cycle = [g1, None, g2, g3]
    assert am.classify(history_one_more_cycle) == "uncertain"

    # Three genuinely consecutive raw cycles, no closure between any of
    # them, still classify as stalled.
    assert am.classify([g1, g2, g3]) == "stalled"


def test_stalled_recognises_dict_expected_regardless_of_key_order():
    # The regression the first port of this fix introduced: repr() is not
    # order-independent for dicts, so three `==`-equal dicts built with
    # different key insertion order used to read as three different goals.
    am = AffectModel(window=10)
    e1 = {"a": 1, "b": 2}
    e2 = {"b": 2, "a": 1}  # == e1, but repr(e2) != repr(e1)
    assert e1 == e2 and repr(e1) != repr(e2)

    run = [_gap(1, e1, 1.0), _gap(2, e2, 1.0), _gap(3, e1, 1.0)]
    assert am.classify(run) == "stalled"
