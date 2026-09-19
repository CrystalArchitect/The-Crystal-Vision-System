# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CrystalCode — the four primitives as the public API surface
track() · detect_gap() · label_affect() · close_with()
"""
from __future__ import annotations
from typing import Any, List, Optional
from .state import PersistentStateStore
from .gap import GapDetector, Gap
from .affect import AffectModel
from .closure import ClosurePolicy, ClosureDecision
from .log import CycleLogger

# Module-level singletons for simple API — reinitialised by Loop
_state: PersistentStateStore | None = None
_gap_detector: GapDetector | None = None
_affect_model: AffectModel | None = None
_closure_policy: ClosurePolicy | None = None
_logger: CycleLogger | None = None

def init_runtime(state: PersistentStateStore, gap_detector: GapDetector, affect_model: AffectModel, closure_policy: ClosurePolicy, logger: CycleLogger):
    global _state, _gap_detector, _affect_model, _closure_policy, _logger
    _state = state
    _gap_detector = gap_detector
    _affect_model = affect_model
    _closure_policy = closure_policy
    _logger = logger

def track(event: dict) -> None:
    assert _state is not None and _logger is not None
    _state.record(event)
    _logger.log("track", event)

def detect_gap(expected: Any, actual: Any) -> Optional[Gap]:
    assert _gap_detector is not None and _logger is not None
    gap = _gap_detector.detect(expected, actual)
    if gap:
        _logger.log("gap_opened", gap.to_dict())
    else:
        _logger.log("gap_none", {"expected": expected, "actual": actual})
    return gap

def label_affect(gap_history: List[Optional[Gap]]) -> str:
    assert _affect_model is not None and _logger is not None
    label = _affect_model.classify(gap_history)
    _logger.log("label", {"label": label, "reason": f"history_len {len(gap_history)}", "history_len": len(gap_history)})
    return label

def close_with(label: str, context: dict | None = None) -> ClosureDecision:
    assert _closure_policy is not None and _logger is not None
    decision = _closure_policy.decide(label, context or {})
    _logger.log("closure", decision.to_dict())
    return decision
