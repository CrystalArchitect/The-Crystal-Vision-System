# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CrystalCode — the four primitives as the public API surface
track() · detect_gap() · label_affect() · close_with()

Runtime model (F3): each Loop owns its own Runtime object — constructing two
Loops does not hijack globals and there is no silent cross-talk. The
module-level functions are thin convenience wrappers over a default Runtime
for single-loop usage, set explicitly with init_runtime(). A Loop never
touches the module default.

No bare assert (F10): misuse raises RuntimeError with a message, so the
checks survive `python3 -O`.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .affect import AffectModel
from .closure import ClosureDecision, ClosurePolicy
from .gap import Gap, GapDetector
from .log import CycleLogger
from .state import PersistentStateStore


class Runtime:
    """Owns one loop's state, detectors, policy, logger and cycle counter."""

    def __init__(
        self,
        state: PersistentStateStore,
        gap_detector: GapDetector,
        affect_model: AffectModel,
        closure_policy: ClosurePolicy,
        logger: CycleLogger,
    ):
        self.state = state
        self.gap_detector = gap_detector
        self.affect_model = affect_model
        self.closure_policy = closure_policy
        self.logger = logger
        self.cycle = 0  # loop cycle number — incremented once per run_cycle (F1)

    def begin_cycle(self) -> int:
        self.cycle += 1
        return self.cycle

    def track(self, event: Dict[str, Any]) -> None:
        self.state.record(event)
        self.logger.log("track", event, cycle=self.cycle)

    def detect_gap(self, expected: Any, actual: Any) -> Optional[Gap]:
        gap = self.gap_detector.detect(expected, actual)
        if gap is not None:
            self.logger.log("gap_opened", gap.to_dict(), cycle=self.cycle)
        else:
            self.logger.log("gap_none", {"expected": expected, "actual": actual}, cycle=self.cycle)
        return gap

    def label_affect(self, gap_history: List[Optional[Gap]]) -> str:
        label = self.affect_model.classify(gap_history)
        self.logger.log(
            "label",
            {"history_len": len(gap_history), "label": label, "window": self.affect_model.window},
            cycle=self.cycle,
        )
        return label

    def close_with(self, label: str, context: Dict[str, Any] | None = None) -> ClosureDecision:
        decision = self.closure_policy.decide(label, context or {})
        self.logger.log("closure", decision.to_dict(), cycle=self.cycle)
        return decision


_default_runtime: Optional[Runtime] = None


def init_runtime(
    state: PersistentStateStore,
    gap_detector: GapDetector,
    affect_model: AffectModel,
    closure_policy: ClosurePolicy,
    logger: CycleLogger,
) -> Runtime:
    """Set (and return) the default Runtime behind the module-level wrappers."""
    global _default_runtime
    _default_runtime = Runtime(state, gap_detector, affect_model, closure_policy, logger)
    return _default_runtime


def _require_runtime() -> Runtime:
    if _default_runtime is None:
        raise RuntimeError(
            "CrystalCode default runtime not initialised — call init_runtime(...) first"
        )
    return _default_runtime


def track(event: Dict[str, Any]) -> None:
    return _require_runtime().track(event)


def detect_gap(expected: Any, actual: Any) -> Optional[Gap]:
    return _require_runtime().detect_gap(expected, actual)


def label_affect(gap_history: List[Optional[Gap]]) -> str:
    return _require_runtime().label_affect(gap_history)


def close_with(label: str, context: Dict[str, Any] | None = None) -> ClosureDecision:
    return _require_runtime().close_with(label, context)
