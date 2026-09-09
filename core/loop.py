# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Loop — track → detect_gap → label_affect → close_with → LLM core.

F1: loop.cycle is the loop cycle number, incremented once per run_cycle —
    four log lines per turn with a tracked event and nothing pending to
    judge yet, five once a prior decision is there to be judged, three
    with neither.
F3: the Loop owns its own Runtime and never touches the module default,
    so two Loops cannot cross-talk.
F9: the LLM core is a deterministic offline stub in v0.1 — its output is
    returned but not fed back into state/gap/closure. Decorative in v0.1.
    See the Figure 1 arrow — future closure through the model, not current.

Dated note — 2026-08-14: this file had no mechanism at all for judging a
prior ClosureDecision — run_cycle returned each decision and moved on, so
nothing ever set its outcome away from "pending" and closure_success_rate()
did not exist. Ported from CrystalCore.OS/synthetic-affect's Loop, which
holds this as the theory's honesty hinge: a decision does not grade itself.
_judge_pending() below scores the *previous* cycle's decision against
*this* cycle's gap — "worked" if the gap it was chasing is gone, "failed"
if not — and logs that judgement before the current cycle's own decision
is made. See core/closure.py for the matching fix on the decide() side.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from . import crystalcode
from .affect import AffectModel
from .closure import ClosureDecision, ClosurePolicy
from .gap import Gap, GapDetector
from .log import CycleLogger
from .state import PersistentStateStore


class Loop:
    def __init__(
        self,
        store_path: str = ":memory:",
        log_path: str = "examples/logs/loop.jsonl",
        llm_core: Callable[[str], str] | None = None,
        window: int = 10,
    ):
        self.store = PersistentStateStore(store_path)
        self.runtime = crystalcode.Runtime(
            self.store,
            GapDetector(),
            AffectModel(window=window),
            ClosurePolicy(),
            CycleLogger(log_path),
        )
        self.gap_history: List[Optional[Gap]] = []
        self.llm_core = llm_core or self._stub_llm
        self._pending: Optional[ClosureDecision] = None

    @property
    def cycle(self) -> int:
        return self.runtime.cycle

    @property
    def logger(self) -> CycleLogger:
        return self.runtime.logger

    @staticmethod
    def _stub_llm(prompt: str) -> str:
        # Deterministic stub — no model, no network — hash prompt to canned
        # responses. Reproducible logs satisfy the Incognita Rule: only
        # surveyed lines in the committed outputs.
        h = sum(ord(c) for c in prompt) % 4
        responses = [
            "Let me rephrase that step.",
            "Could you clarify expected output?",
            "Switching tool to file_search.",
            "Closing loop, gap resolved.",
        ]
        return responses[h]

    def _judge_pending(self, gap: Optional[Gap]) -> None:
        """Score the previous cycle's decision against what actually happened."""
        if self._pending is None:
            return
        self._pending.outcome = "worked" if gap is None else "failed"
        self.runtime.logger.log(
            "closure_outcome",
            {"strategy": self._pending.strategy, "outcome": self._pending.outcome},
            cycle=self.runtime.cycle,
        )
        self._pending = None

    def run_cycle(self, expected: Any, actual: Any, event: Dict[str, Any] | None = None) -> Dict[str, Any]:
        rt = self.runtime
        rt.begin_cycle()
        # `is not None`, not truthiness — event={} is a real (empty) event
        # and must still be tracked, distinct from event omitted entirely.
        if event is not None:
            rt.track(event)
        gap = rt.detect_gap(expected, actual)
        self._judge_pending(gap)
        self.gap_history.append(gap)
        self.store.set_expected({"value": expected})
        self.store.update_actual({"value": actual})
        label = rt.label_affect(self.gap_history)
        decision = rt.close_with(label, {"expected": expected, "actual": actual})
        self._pending = decision
        # F9: output returned, not fed back into state/gap/closure
        llm_out = self.llm_core(f"{label}:{decision.strategy}:{expected}")
        return {
            "cycle": rt.cycle,
            "gap": gap,
            "label": label,
            "decision": decision,
            "llm": llm_out,
            "log_path": str(rt.logger.path),
        }

    def closure_success_rate(self) -> Optional[float]:
        """Share of judged decisions that actually shut the gap.

        `None` while nothing has been judged yet — an unmeasured rate is not
        zero, and must not be reported as one.
        """
        judged = [e for e in self.runtime.logger.read_all() if e["op"] == "closure_outcome"]
        if not judged:
            return None
        worked = sum(1 for e in judged if e["data"]["outcome"] == "worked")
        return worked / len(judged)
