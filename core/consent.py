# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Consent tokens. Absence = denial. Tokens cannot outrank P1.

Nothing crosses the node boundary without a live, matching, unrevoked token.
No inferred consent. No emergency exception that quietly expands depth.

Ethics header: Synthetic = apparent / functional. Not a claim of feeling.
"""
from __future__ import annotations

from typing import TypedDict

from .ontology import CORE_IDS

PACKET_KINDS = frozenset({"transmit", "packet"})

# Under Restricted Mode only capacity-signal and hard-alert may still leave,
# and only with a valid token. Everything else stays home.
RESTRICTED_ALLOWED_DIMENSIONS = frozenset({"resource_tension", "boundary_stress"})


class ConsentToken(TypedDict):
    token_id: str
    operator_id: str
    allowed_dimensions: list[str]
    allowed_destinations: list[str]
    purpose: str
    expires_at: int
    revoked: bool


class PacketIntent(TypedDict, total=False):
    destination: str
    dimension_id: str
    purpose: str
    token: ConsentToken


class ConsentVerdict(TypedDict, total=False):
    allowed: bool
    reason: str
    operator_summary: str


def is_packet(kind: str) -> bool:
    return kind in PACKET_KINDS


def evaluate_consent(
    packet: PacketIntent | None,
    *,
    now: int,
    restricted: bool = False,
    p1_executed: bool = False,
) -> ConsentVerdict:
    """Allow a packet only if a live token matches destination, dimension, and purpose."""
    if packet is None:
        return {
            "allowed": False,
            "reason": "absent",
            "operator_summary": "Absence of token = denial. No packet.",
        }
    if p1_executed:
        return {
            "allowed": False,
            "reason": "p1",
            "operator_summary": "P1 is active. A valid token cannot outrank a boundary interrupt. No packet.",
        }

    token = packet.get("token")
    destination = packet.get("destination")
    dimension = packet.get("dimension_id")
    purpose = packet.get("purpose")

    if token is None:
        return {
            "allowed": False,
            "reason": "absent",
            "operator_summary": "Absence of token = denial. No packet.",
        }
    if token.get("revoked"):
        return {
            "allowed": False,
            "reason": "revoked",
            "operator_summary": "Token revoked. In-flight packets are invalid. No packet.",
        }
    if now >= int(token.get("expires_at", 0)):
        return {
            "allowed": False,
            "reason": "expired",
            "operator_summary": "Token expired. Continuity of consent is not inferred. No packet.",
        }
    if not destination or destination not in token.get("allowed_destinations", []):
        return {
            "allowed": False,
            "reason": "destination",
            "operator_summary": "Destination not on this token. No packet.",
        }
    if not dimension or dimension not in CORE_IDS:
        return {
            "allowed": False,
            "reason": "dimension",
            "operator_summary": "Unknown or missing dimension. No packet.",
        }
    if dimension not in token.get("allowed_dimensions", []):
        return {
            "allowed": False,
            "reason": "dimension",
            "operator_summary": "Dimension not on this token. No packet.",
        }
    if not purpose or purpose != token.get("purpose"):
        return {
            "allowed": False,
            "reason": "purpose",
            "operator_summary": "Purpose does not match. A capacity token is not a modelling token. No packet.",
        }
    if restricted and dimension not in RESTRICTED_ALLOWED_DIMENSIONS:
        return {
            "allowed": False,
            "reason": "restricted",
            "operator_summary": "Restricted Mode: rich transmission blocked. Token does not lift isolation.",
        }
    return {
        "allowed": True,
        "reason": "ok",
        "operator_summary": "Live token matches destination, dimension, and purpose. Packet may leave.",
    }
