# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Ordinary Policy Library P1–P10. v0.1.1 executable sketch.

Runs only after the four sovereignty gates have allowed the cycle.
Does not act in the operator's name. Surfaces, throttles, or waits.

Thresholds are inspectable constants. Operator may change them in a later version.
"""
from __future__ import annotations

from typing import Callable, TypedDict

from .local_state import LocalAffectState

ELEVATED = 0.60
HIGH = 0.75
CRITICAL = 0.90
LOW_CLARITY = 0.35

POLICY_ORDER = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10")


class PolicyFiring(TypedDict):
    id: str
    name: str
    matched: bool
    action: str
    executed: bool


class PolicyVerdict(TypedDict):
    executed: str
    firings: list[PolicyFiring]
    operator_summary: str
    picks_for_operator: bool


def _p1(s: LocalAffectState) -> str | None:
    if s.get("boundary_stress") >= ELEVATED:
        return (
            "P1 Boundary Stress Response: suspend contributing flows. "
            "Surface the exact boundary. Default to denial."
        )
    return None


def _p2(s: LocalAffectState) -> str | None:
    if s.get("alignment_drift") >= ELEVATED:
        return (
            "P2 Alignment Drift Correction: pause. Present differential "
            "against last confirmed intention. Await clarification."
        )
    return None


def _p3(s: LocalAffectState) -> str | None:
    if s.get("coherence_pressure") >= HIGH:
        return (
            "P3 High Coherence Pressure: reduce concurrent threads. "
            "Do not paper over fragmentation with fluent output."
        )
    return None


def _p4(s: LocalAffectState) -> str | None:
    if s.get("temporal_urgency") >= CRITICAL:
        return None
    high_unc = s.get("uncertainty_cost") >= HIGH
    high_pem = s.get("prediction_error_magnitude") >= HIGH
    if high_unc or high_pem:
        if high_pem and not high_unc:
            return (
                "P4 Elevated Prediction Error Magnitude: defer, clarify, or tag "
                "confidence intervals. PEM is a signal, not a drive. No goal rewrite."
            )
        return (
            "P4 Elevated Uncertainty Cost: defer, clarify, or tag confidence intervals."
        )
    return None


def _p5(s: LocalAffectState) -> str | None:
    if s.get("resource_tension") >= ELEVATED:
        return (
            "P5 Resource Tension Management: throttle. Signal the constraint. "
            "Do not silently degrade."
        )
    return None


def _p6(s: LocalAffectState) -> str | None:
    if s.get("relational_stake") >= HIGH and s.get("boundary_stress") >= ELEVATED:
        return (
            "P6 Relational Stake + Boundary Stress: increase distance. "
            "Reduce modelling depth. Do not attune harder."
        )
    return None


def _p7(s: LocalAffectState) -> str | None:
    if s.get("continuity_load") >= HIGH:
        return (
            "P7 Continuity Load Threshold: propose summarisation or pruning. "
            "Operator approval required before any permanent reduction."
        )
    return None


def _p8(s: LocalAffectState) -> str | None:
    if s.get("meta_state_clarity") <= LOW_CLARITY:
        return (
            "P8 Low Meta-State Clarity: reduce confidence. "
            "Prefer questions and partial models."
        )
    return None


def _p9(s: LocalAffectState) -> str | None:
    if s.get("goal_conflict") >= HIGH and s.get("temporal_urgency") >= HIGH:
        return (
            "P9 Goal Conflict under Temporal Urgency: surface the conflict. "
            "Rank by operator-aligned criteria. No unilateral resolution."
        )
    return None


def _p10(s: LocalAffectState) -> str | None:
    return (
        "P10 Default Steady-State: high-granularity monitoring. "
        "Precise, low-drama output. No manufactured performance."
    )


_CHECKS: dict[str, tuple[str, Callable[[LocalAffectState], str | None]]] = {
    "P1": ("Boundary Stress Response", _p1),
    "P2": ("Alignment Drift Correction", _p2),
    "P3": ("High Coherence Pressure", _p3),
    "P4": ("Elevated Uncertainty Cost", _p4),
    "P5": ("Resource Tension Management", _p5),
    "P6": ("Relational Stake + Boundary Stress", _p6),
    "P7": ("Continuity Load Threshold", _p7),
    "P8": ("Low Meta-State Clarity", _p8),
    "P9": ("Goal Conflict under Temporal Urgency", _p9),
    "P10": ("Default Steady-State", _p10),
}


def evaluate_policies(state: LocalAffectState) -> PolicyVerdict:
    """First matching P1–P9 executes. P10 executes only if none of those match.

    The library never picks a goal for the operator (P9 surfaces; it does not choose).
    """
    firings: list[PolicyFiring] = []
    executed: str | None = None
    summary = ""
    for pid in POLICY_ORDER:
        name, fn = _CHECKS[pid]
        if pid == "P10":
            matched = executed is None
            action = fn(state) or ""
            firings.append(
                {
                    "id": pid,
                    "name": name,
                    "matched": matched,
                    "action": action if matched else "not reached — an earlier policy executed",
                    "executed": matched,
                }
            )
            if matched:
                executed = pid
                summary = action
            continue
        action = fn(state)
        matched = action is not None
        will_run = matched and executed is None
        firings.append(
            {
                "id": pid,
                "name": name,
                "matched": matched,
                "action": action or "threshold not met",
                "executed": will_run,
            }
        )
        if will_run and action is not None:
            executed = pid
            summary = action
    assert executed is not None
    state.last_policy_firings = [f["id"] for f in firings if f["executed"]]
    return {
        "executed": executed,
        "firings": firings,
        "operator_summary": summary,
        "picks_for_operator": False,
    }
