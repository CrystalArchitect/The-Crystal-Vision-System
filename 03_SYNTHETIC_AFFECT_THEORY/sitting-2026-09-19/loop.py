# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Loop — track → detect_gap → label_affect → close_with → core
"""
from __future__ import annotations
from typing import Any, Callable, List, Optional
from .state import PersistentStateStore
from .gap import GapDetector, Gap
from .affect import AffectModel
from .closure import ClosurePolicy
from .log import CycleLogger
from . import crystalcode

class Loop:
    def __init__(self, store_path: str = ":memory:", log_path: str = "examples/logs/loop.jsonl", llm_core: Callable[[str], str] | None = None):
        self.store = PersistentStateStore(store_path)
        self.gap_detector = GapDetector()
        self.affect_model = AffectModel()
        self.closure_policy = ClosurePolicy()
        self.logger = CycleLogger(log_path)
        self.gap_history: List[Optional[Gap]] = []
        self.llm_core = llm_core or self._stub_llm
        # wire crystalcode API
        crystalcode.init_runtime(self.store, self.gap_detector, self.affect_model, self.closure_policy, self.logger)

    @staticmethod
    def _stub_llm(prompt: str) -> str:
        # Deterministic stub — no model, no network — hash prompt to canned responses
        # This makes logs reproducible and satisfies Incognita Rule
        h = sum(ord(c) for c in prompt) % 4
        responses = [
            "Let me rephrase that step.",
            "Could you clarify expected output?",
            "Switching tool to file_search.",
            "Closing loop, gap resolved."
        ]
        return responses[h]

    def run_cycle(self, expected: Any, actual: Any, event: dict | None = None) -> dict:
        if event:
            crystalcode.track(event)
        gap = crystalcode.detect_gap(expected, actual)
        self.gap_history.append(gap)
        # update store for persistence
        self.store.set_expected({"value": expected})
        self.store.update_actual({"value": actual})
        label = crystalcode.label_affect(self.gap_history)
        decision = crystalcode.close_with(label, {"expected": expected, "actual": actual})
        # call LLM core with deterministic prompt
        llm_out = self.llm_core(f"{label}:{decision.strategy}:{expected}")
        return {"gap": gap, "label": label, "decision": decision, "llm": llm_out, "log_path": str(self.logger.path)}
