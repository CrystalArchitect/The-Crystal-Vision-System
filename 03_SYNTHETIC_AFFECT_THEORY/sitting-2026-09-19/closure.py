# Copyright (c) 2026 TerAustralis Incognita™ — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Closure Policy — postulate 4. The label selects the move.

One rule is load-bearing beyond its size: **a decision does not record its own
outcome.** `outcome` stays `pending` until the next cycle observes whether the
gap actually shut. An earlier draft stamped `"outcome": "asked"` at the moment
of deciding, which meant a closure-success-rate computed from the log would
read 100% forever — the system grading its own homework, which is exactly the
cosmetic-closure failure this theory has to guard against.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

STRATEGIES = ("stop", "ask", "rephrase", "switch_tool", "escalate")

#: Consecutive `stalled` labels before the policy stops retrying and escalates.
ESCALATE_AFTER_STALLS = 2


@dataclass
class ClosureDecision:
    strategy: str
    reason: str
    outcome: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy,
            "reason": self.reason,
            "outcome": self.outcome,
        }


class ClosurePolicy:
    """Stateful across a single goal's lifetime: it counts repeated stalls.

    One policy per goal. The counter resets the moment any non-stalled label
    arrives, so a session that stalls twice, recovers, and stalls again later
    gets `switch_tool` before `escalate` a second time rather than escalating
    forever after two stalls in its whole history.
    """

    def __init__(self) -> None:
        self._consecutive_stalls = 0

    def decide(
        self, label: str, context: Optional[Dict[str, Any]] = None
    ) -> ClosureDecision:
        if label != "stalled":
            self._consecutive_stalls = 0

        if label == "closed":
            return ClosureDecision("stop", "gap closed")
        if label == "reopened":
            return ClosureDecision("rephrase", "gap reopened")
        if label == "converging":
            return ClosureDecision("rephrase", "gap narrowing, continue")
        if label == "stalled":
            self._consecutive_stalls += 1
            if self._consecutive_stalls >= ESCALATE_AFTER_STALLS:
                return ClosureDecision(
                    "escalate",
                    f"stalled {self._consecutive_stalls} cycles running",
                )
            return ClosureDecision("switch_tool", "stalled, try another route")
        return ClosureDecision("ask", "uncertain, need clarification")
