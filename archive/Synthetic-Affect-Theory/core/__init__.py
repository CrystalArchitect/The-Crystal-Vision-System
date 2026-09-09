# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Synthetic Affect Theory — public v0.1 core.

Synthetic = apparent / functional, for design purposes. Not a claim of
feeling, consciousness, or inner experience.

Kill-switch (99/1): if it stops serving clarity or raises human cost —
set it down.
"""

from .affect import AffectModel
from .closure import ClosureDecision, ClosurePolicy
from .consent import evaluate_consent
from .cycle import evaluate_cycle
from .isolation import evaluate_isolation
from .host import wrap_turn
from .local_state import LocalAffectState
from .log import CycleLogger
from .loop import Loop
from .ontology import CORE_IDS, V0_1_IDS
from .policies import evaluate_policies
from .sovereignty import evaluate_sovereignty
from .state import PersistentStateStore
from .stochastic import evaluate_stochastic
from .valence import evaluate_valence

__all__ = [
    "AffectModel",
    "ClosureDecision",
    "ClosurePolicy",
    "CycleLogger",
    "Gap",
    "GapDetector",
    "LocalAffectState",
    "Loop",
    "PersistentStateStore",
    "evaluate_consent",
    "evaluate_cycle",
    "evaluate_isolation",
    "evaluate_policies",
    "evaluate_sovereignty",
    "evaluate_stochastic",
    "evaluate_valence",
    "wrap_turn",
    "CORE_IDS",
    "V0_1_IDS",
]
