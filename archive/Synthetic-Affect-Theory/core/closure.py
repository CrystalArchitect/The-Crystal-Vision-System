# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
ClosurePolicy — selects rephrase | ask | switch_tool | escalate | stop

Dated note — 2026-08-14: decide() shipped in PR #1 (merged 2026-08-12)
stamping `outcome` to a strategy-derived string ("closed", "escalated", ...)
at the moment of deciding. `ClosureDecision.outcome` defaults to "pending"
for a reason: a decision does not record its own outcome. The *next* cycle
is meant to judge whether the gap it was chasing actually shut — "worked" if
so, "failed" if not — the same way canon's Loop._judge_pending does in
CrystalCore.OS/synthetic-affect. Stamping outcome here bypassed that judge
entirely, which is the exact cosmetic-closure failure the theory exists to
guard against: a closure-success-rate computed from these logs would have
read 100% forever, the system grading its own homework. Fixed by no longer
passing `outcome=` from decide() — the dataclass default carries it until
Loop judges it against the next cycle's gap. See core/loop.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

STRATEGIES = ("rephrase", "ask", "switch_tool", "escalate", "stop")


@dataclass
class ClosureDecision:
    strategy: str  # rephrase | ask | switch_tool | escalate | stop
    reason: str
    outcome: str = "pending"

    def to_dict(self):
        return {"strategy": self.strategy, "reason": self.reason, "outcome": self.outcome}


class ClosurePolicy:
    """Stateful: repeated stalled decisions escalate.

    The counter resets the moment any non-stalled label arrives — inside
    decide() itself, not only via the explicit reset() below — so a session
    that stalls, recovers, and stalls again later gets switch_tool before
    escalate a second time, rather than escalating forever after two stalls
    anywhere in its whole history. Ported from the same verified fix as
    affect.py's check order; see that file's docstring for the provenance.
    """

    def __init__(self):
        self.stalled_count = 0

    def reset(self) -> None:
        self.stalled_count = 0

    def decide(self, label: str, context: Dict | None = None) -> ClosureDecision:
        context = context or {}
        if label != "stalled":
            self.stalled_count = 0
        if label == "closed":
            return ClosureDecision(strategy="stop", reason="gap closed, no further action")
        if label == "stalled":
            self.stalled_count += 1
            if self.stalled_count >= 2:
                return ClosureDecision(strategy="escalate", reason=f"stalled {self.stalled_count} times")
            return ClosureDecision(strategy="switch_tool", reason="repeated expected, switch tool")
        if label == "uncertain":
            return ClosureDecision(strategy="ask", reason="gap not narrowing, need clarification")
        if label == "reopened":
            return ClosureDecision(strategy="rephrase", reason="gap reopened after closure")
        if label == "converging":
            return ClosureDecision(strategy="rephrase", reason="magnitude decreasing, rephrase to close")
        return ClosureDecision(strategy="ask", reason="fallback")
