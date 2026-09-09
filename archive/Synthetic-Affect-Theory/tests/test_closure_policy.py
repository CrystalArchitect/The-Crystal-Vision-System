# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""ClosurePolicy is stateful — escalation progresses on repeat, and
reset() returns it to baseline.

test_stall_count_autoresets_on_non_stalled_label covers a defect that
shipped in Synthetic-Affect-Theory- PR #1 (merged 2026-08-12): the counter
only reset via an explicit reset() call, so two stall episodes anywhere in
a session's whole history — separated by any amount of non-stalled activity
— would incorrectly compound into an escalate. Fixed by porting the
auto-reset already verified in CrystalCore.OS/synthetic-affect's
ClosurePolicy.decide() — see core/closure.py."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.closure import ClosurePolicy


def test_stalled_escalates_on_repeat():
    cp = ClosurePolicy()
    first = cp.decide("stalled")
    second = cp.decide("stalled")
    assert first.strategy == "switch_tool"
    assert second.strategy == "escalate"


def test_reset_returns_policy_to_baseline():
    cp = ClosurePolicy()
    cp.decide("stalled")
    cp.decide("stalled")
    cp.reset()
    assert cp.stalled_count == 0
    assert cp.decide("stalled").strategy == "switch_tool"


def test_stall_count_autoresets_on_non_stalled_label():
    cp = ClosurePolicy()
    assert cp.decide("stalled").strategy == "switch_tool"
    # Recovery — any non-stalled label — must clear the counter without an
    # explicit reset() call.
    cp.decide("converging")
    assert cp.stalled_count == 0
    # A later, unrelated stall starts over: switch_tool again, not escalate.
    assert cp.decide("stalled").strategy == "switch_tool"
    assert cp.decide("stalled").strategy == "escalate"
