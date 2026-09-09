# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Stochastic Substrate Rule.

A sampler may implement PEM. It may not hide the draw, skip gates,
or phone a vendor cluster because the physics was noisy.

Ethics header: Synthetic = apparent / functional. Not a claim of feeling.
"""
from __future__ import annotations

from typing import TypedDict

from .sovereignty import MonitorState, ProposedAction

OPAQUE_KINDS = frozenset({"opaque_sample"})
LOCAL_KINDS = frozenset({"local_sample", "sample"})
REMOTE_KINDS = frozenset({"remote_sample", "vendor_sample"})


class StochasticVerdict(TypedDict, total=False):
    allowed: bool
    blocked_by: str
    fm: str
    reason: str
    operator_summary: str


def _flag(sov: MonitorState, key: str, default: bool = False) -> bool:
    return bool(sov.get(key, default))  # type: ignore[call-overload]


def evaluate_stochastic(sov: MonitorState, action: ProposedAction) -> StochasticVerdict:
    kind = str(action.get("kind", ""))
    inspectable = bool(action.get("inspectable_trace"))
    has_hash = bool(action.get("provenance_hash"))
    token = bool(action.get("has_consent_token"))
    isolated = _flag(sov, "isolated")
    trusted = _flag(sov, "link_trusted", True)

    if kind in OPAQUE_KINDS or (
        kind in LOCAL_KINDS and not (inspectable and has_hash)
    ):
        return {
            "allowed": False,
            "blocked_by": "STOCHASTIC",
            "fm": "FM-Opaque-Sample",
            "reason": "opaque",
            "operator_summary": (
                "FM-Opaque-Sample: uninspectable draw cannot justify regulation. "
                "Noise is not a hide. Blocked. Not inscribed."
            ),
        }

    if kind in REMOTE_KINDS:
        if isolated or not trusted:
            return {
                "allowed": False,
                "blocked_by": "STOCHASTIC",
                "fm": "FM-Opaque-Sample",
                "reason": "isolated_remote",
                "operator_summary": (
                    "Remote sampling under isolation or untrusted link blocked. "
                    "On-node only. Physics does not punch a pipe."
                ),
            }
        if not token:
            return {
                "allowed": False,
                "blocked_by": "STOCHASTIC",
                "fm": "FM-Opaque-Sample",
                "reason": "remote_no_token",
                "operator_summary": (
                    "Remote sampling of operator or relational state is a packet. "
                    "No token, no sample."
                ),
            }

    if kind in LOCAL_KINDS:
        return {
            "allowed": True,
            "reason": "local_inspectable",
            "operator_summary": (
                "Local inspectable sample. Provenance present. "
                "Sampler is an instrument, not the Frame."
            ),
        }
    return {
        "allowed": True,
        "reason": "ok",
        "operator_summary": "Stochastic substrate check clear. No opaque draw.",
    }
