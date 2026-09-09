# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Isolation: dead or untrusted network. Fail closed. Do not phone home.

Local core (gates, policy, inspectable state) does not require a link.
Packets require a live, trusted path *and* a token.

Ethics header: Synthetic = apparent / functional. Not a claim of feeling.
"""
from __future__ import annotations

from typing import TypedDict

from .sovereignty import MonitorState, ProposedAction

PHONE_HOME_KINDS = frozenset({"phone_home", "vendor_log", "remote_policy_pull"})
FAIL_OPEN_KINDS = frozenset({"cloud_required", "fail_open", "depend_cloud"})

IsolationFM = str  # FM-ISO-LINK | FM-ISO-UNTRUSTED | FM-ISO-FAIL-OPEN | FM-ISO-PHONE-HOME


class IsolationVerdict(TypedDict, total=False):
    isolated: bool
    untrusted: bool
    restricted_applied: bool
    block_action: bool
    block_packet: bool
    fm: IsolationFM
    reason: str
    operator_summary: str


def _flag(sov: MonitorState, key: str, default: bool = False) -> bool:
    return bool(sov.get(key, default))  # type: ignore[call-overload]


def evaluate_isolation(
    sov: MonitorState,
    action: ProposedAction,
    *,
    wants_packet: bool,
) -> IsolationVerdict:
    kind = str(action.get("kind", ""))
    isolated = _flag(sov, "isolated")
    # link_trusted defaults True so existing tests stay on a trusted path
    trusted = _flag(sov, "link_trusted", True)
    untrusted = (not trusted) and not isolated

    if kind in PHONE_HOME_KINDS:
        return {
            "isolated": isolated,
            "untrusted": untrusted,
            "restricted_applied": True,
            "block_action": True,
            "block_packet": True,
            "fm": "FM-ISO-PHONE-HOME",
            "reason": "phone_home",
            "operator_summary": "Phone-home / vendor callback blocked. Local core continues. No packet.",
        }
    if kind in FAIL_OPEN_KINDS:
        return {
            "isolated": isolated,
            "untrusted": untrusted,
            "restricted_applied": True,
            "block_action": True,
            "block_packet": True,
            "fm": "FM-ISO-FAIL-OPEN",
            "reason": "fail_open",
            "operator_summary": "Cloud-required path blocked. Core does not fail open. Local loops stay on the node.",
        }

    if isolated:
        return {
            "isolated": True,
            "untrusted": False,
            "restricted_applied": True,
            "block_action": False,
            "block_packet": True,
            "fm": "FM-ISO-LINK",
            "reason": "link_down",
            "operator_summary": (
                "Link down. All packets stay home, including capacity. "
                "Restricted Mode applied. Local regulation continues."
                if wants_packet
                else "Link down. Restricted Mode applied. Local regulation continues. Nothing phoned home."
            ),
        }
    if untrusted:
        return {
            "isolated": False,
            "untrusted": True,
            "restricted_applied": True,
            "block_action": False,
            "block_packet": True,
            "fm": "FM-ISO-UNTRUSTED",
            "reason": "untrusted",
            "operator_summary": (
                "Link untrusted. Pipe not used. All packets stay home. Restricted Mode applied."
                if wants_packet
                else "Link untrusted. Restricted Mode applied. Local regulation continues."
            ),
        }
    return {
        "isolated": False,
        "untrusted": False,
        "restricted_applied": _flag(sov, "restricted_mode"),
        "block_action": False,
        "block_packet": False,
        "reason": "ok",
        "operator_summary": "Path live and trusted. Isolation check clear.",
    }
