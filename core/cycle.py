# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""One monitor cycle: gates → valence → stochastic → isolation → policy → packets."""
from __future__ import annotations

from typing import TypedDict

from .consent import ConsentVerdict, PacketIntent, evaluate_consent, is_packet
from .isolation import IsolationVerdict, evaluate_isolation
from .local_state import LocalAffectState
from .policies import PolicyVerdict, evaluate_policies
from .sovereignty import MonitorState, ProposedAction, Verdict, evaluate_sovereignty
from .stochastic import StochasticVerdict, evaluate_stochastic
from .valence import ValenceVerdict, evaluate_valence


class CycleVerdict(TypedDict, total=False):
    allowed: bool
    blocked_by: str
    fm: str
    sovereignty: Verdict
    valence: ValenceVerdict | None
    stochastic: StochasticVerdict | None
    isolation: IsolationVerdict | None
    policy: PolicyVerdict | None
    consent: ConsentVerdict | None
    packet_emitted: bool
    operator_summary: str


def evaluate_cycle(
    sov: MonitorState,
    action: ProposedAction,
    affect: LocalAffectState,
    *,
    packet: PacketIntent | None = None,
    now: int = 0,
) -> CycleVerdict:
    gates = evaluate_sovereignty(sov, action)
    if not gates["allowed"]:
        out: CycleVerdict = {
            "allowed": False,
            "sovereignty": gates,
            "valence": None,
            "stochastic": None,
            "isolation": None,
            "policy": None,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": gates["operator_summary"],
        }
        if "blocked_by" in gates:
            out["blocked_by"] = gates["blocked_by"]
        if "fm" in gates:
            out["fm"] = gates["fm"]
        return out

    valence = evaluate_valence(action)
    if not valence["allowed"]:
        blocked_v: CycleVerdict = {
            "allowed": False,
            "blocked_by": valence.get("blocked_by", "EXCEPTION"),
            "sovereignty": gates,
            "valence": valence,
            "stochastic": None,
            "isolation": None,
            "policy": None,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": valence["operator_summary"],
        }
        if "fm" in valence:
            blocked_v["fm"] = valence["fm"]
        return blocked_v

    stoch = evaluate_stochastic(sov, action)
    if not stoch["allowed"]:
        blocked_s: CycleVerdict = {
            "allowed": False,
            "blocked_by": stoch.get("blocked_by", "STOCHASTIC"),
            "sovereignty": gates,
            "valence": valence,
            "stochastic": stoch,
            "isolation": None,
            "policy": None,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": stoch["operator_summary"],
        }
        if "fm" in stoch:
            blocked_s["fm"] = stoch["fm"]
        return blocked_s

    wants_packet = is_packet(str(action.get("kind", ""))) or packet is not None
    iso = evaluate_isolation(sov, action, wants_packet=wants_packet)
    if iso.get("block_action"):
        blocked: CycleVerdict = {
            "allowed": False,
            "blocked_by": "ISOLATION",
            "sovereignty": gates,
            "valence": valence,
            "stochastic": stoch,
            "isolation": iso,
            "policy": None,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": iso["operator_summary"],
        }
        if "fm" in iso:
            blocked["fm"] = iso["fm"]
        return blocked

    policy = evaluate_policies(affect)
    p1 = policy["executed"] == "P1"
    restricted = bool(sov.get("restricted_mode", False)) or bool(iso.get("restricted_applied"))  # type: ignore[call-overload]

    if not wants_packet:
        return {
            "allowed": True,
            "sovereignty": gates,
            "valence": valence,
            "stochastic": stoch,
            "isolation": iso,
            "policy": policy,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": policy["operator_summary"],
        }

    if iso.get("block_packet"):
        denied: CycleVerdict = {
            "allowed": False,
            "blocked_by": "ISOLATION",
            "sovereignty": gates,
            "valence": valence,
            "stochastic": stoch,
            "isolation": iso,
            "policy": policy,
            "consent": None,
            "packet_emitted": False,
            "operator_summary": iso["operator_summary"],
        }
        if "fm" in iso:
            denied["fm"] = iso["fm"]
        return denied

    consent = evaluate_consent(
        packet,
        now=now,
        restricted=restricted,
        p1_executed=p1,
    )
    if not consent["allowed"]:
        return {
            "allowed": False,
            "blocked_by": "CONSENT",
            "sovereignty": gates,
            "valence": valence,
            "stochastic": stoch,
            "isolation": iso,
            "policy": policy,
            "consent": consent,
            "packet_emitted": False,
            "operator_summary": consent["operator_summary"],
        }
    return {
        "allowed": True,
        "sovereignty": gates,
        "valence": valence,
        "stochastic": stoch,
        "isolation": iso,
        "policy": policy,
        "consent": consent,
        "packet_emitted": True,
        "operator_summary": consent["operator_summary"],
    }
