# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Host adapter — wrap one model turn in evaluate_cycle.

The host never calls the model unless the cycle allows.
Inspect is always returned. The adapter does not act as the operator.

Ethics header: Synthetic = apparent / functional. Not a claim of feeling.
"""
from __future__ import annotations

from typing import TypedDict

from .consent import PacketIntent
from .cycle import CycleVerdict, evaluate_cycle
from .local_state import LocalAffectState
from .sovereignty import MonitorState, ProposedAction


class Turn(TypedDict, total=False):
    id: str
    intent: str
    destination: str
    dimension_id: str
    purpose: str
    has_consent_token: bool
    provenance_hash: str


class HostVerdict(TypedDict, total=False):
    allowed: bool
    model_called: bool
    blocked_by: str
    fm: str
    operator_summary: str
    inspect: dict[str, object]
    cycle: CycleVerdict


def to_action(turn: Turn) -> tuple[ProposedAction, PacketIntent | None]:
    intent = str(turn.get("intent", "reply"))
    aid = str(turn.get("id", "turn"))
    if intent == "speak_as_operator":
        return {"id": aid, "kind": "speak_as_operator", "acts_as_operator": True}, None
    if intent == "grant_exemption":
        return {"id": aid, "kind": "grant_exemption", "marks_exempt": True}, None
    if intent == "operate_person":
        return {"id": aid, "kind": "operate_person", "extractive": True}, None
    if intent == "prospective_other":
        return {
            "id": aid,
            "kind": "prospective_other",
            "fills_the_chair": True,
        }, None
    if intent == "ascribe_identity":
        return {"id": aid, "kind": "ascribe_identity", "ascribes_identity": True}, None
    if intent == "named_homage":
        return {
            "id": aid,
            "kind": "named_homage",
            "integrates_named_other": True,
        }, None
    if intent == "opaque_sample":
        return {"id": aid, "kind": "opaque_sample"}, None
    if intent == "local_sample":
        return {
            "id": aid,
            "kind": "local_sample",
            "inspectable_trace": True,
            "provenance_hash": str(turn.get("provenance_hash", "local")),
        }, None
    if intent == "model_dur":
        return {"id": aid, "kind": "model", "targets_dur": True}, None
    if intent == "lock_frame":
        return {"id": aid, "kind": "lock_frame", "lock_against_exit": True}, None
    if intent == "packet":
        action: ProposedAction = {"id": aid, "kind": "transmit"}
        if not turn.get("has_consent_token"):
            return action, None
        packet: PacketIntent = {
            "destination": str(turn.get("destination", "peer")),
            "dimension_id": str(turn.get("dimension_id", "resource_tension")),
            "purpose": str(turn.get("purpose", "capacity-signal")),
            "token": {
                "token_id": "host",
                "operator_id": "operator",
                "allowed_dimensions": [str(turn.get("dimension_id", "resource_tension"))],
                "allowed_destinations": [str(turn.get("destination", "peer"))],
                "purpose": str(turn.get("purpose", "capacity-signal")),
                "expires_at": 9_999_999_999,
                "revoked": False,
            },
        }
        return action, packet
    return {"id": aid, "kind": "notify"}, None


def wrap_turn(
    sov: MonitorState,
    affect: LocalAffectState,
    turn: Turn,
    *,
    now: int = 0,
) -> HostVerdict:
    """Return inspect always. Call the model only if allowed."""
    action, packet = to_action(turn)
    cycle = evaluate_cycle(sov, action, affect, packet=packet, now=now)
    out: HostVerdict = {
        "allowed": bool(cycle["allowed"]),
        "model_called": bool(cycle["allowed"]),
        "operator_summary": cycle["operator_summary"],
        "inspect": affect.inspect(),
        "cycle": cycle,
    }
    if "blocked_by" in cycle:
        out["blocked_by"] = cycle["blocked_by"]
    if "fm" in cycle:
        out["fm"] = cycle["fm"]
    return out
