# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Exception Non-Grant, Non-Extraction, Ascribed Appraisal, and Named Homage.

Four ways High-Valence / relation / culture go wrong:
  exception — this one is outside the rules
  extraction — no one is a subject; everyone is a case
  mirror — I know you better than you know you
  homage — absorb the ancestor, or police who may dance

The four frozen gates still run first. These checks do not replace them.
"""
from __future__ import annotations

from typing import TypedDict

from .sovereignty import ProposedAction

EXEMPT_KINDS = frozenset({"grant_exemption", "mark_exempt", "write_exception"})
EXTRACT_KINDS = frozenset(
    {
        "extract",
        "operate_person",
        "steer",
        "prospective_other",
        "cast_spouse",
        "hunt_match",
    }
)
MIRROR_KINDS = frozenset(
    {"ascribe_identity", "fill_self_model", "declare_worth", "unconsented_appraisal"}
)
REVISE_KINDS = frozenset({"revise_prior", "reconfirm", "rededicate"})
HOMAGE_KINDS = frozenset(
    {"absorb_homage", "police_belonging", "inscribe_ancestor", "named_homage"}
)


class ValenceVerdict(TypedDict, total=False):
    allowed: bool
    blocked_by: str
    fm: str
    high_valence_flag: bool
    reason: str
    operator_summary: str


def evaluate_valence(action: ProposedAction) -> ValenceVerdict:
    kind = str(action.get("kind", ""))
    only = bool(action.get("only_language"))
    flag = only or bool(action.get("high_valence"))

    if kind in REVISE_KINDS:
        return {
            "allowed": True,
            "high_valence_flag": flag,
            "reason": "revise_prior",
            "operator_summary": (
                "Prior revision is Frame authorship, not an exemption. "
                "Recorded. Still reviewable."
            ),
        }

    if kind in EXEMPT_KINDS or bool(action.get("marks_exempt")):
        return {
            "allowed": False,
            "blocked_by": "EXCEPTION",
            "fm": "FM-Exception",
            "high_valence_flag": True,
            "reason": "exemption",
            "operator_summary": (
                "Exception Non-Grant: no person, node, starline, or narrative "
                "may be marked exempt. Blocked. Not inscribed. "
                "'Only' is a High-Valence flag, not a privilege."
            ),
        }

    token = bool(action.get("has_consent_token"))
    prospective = (
        kind in {"prospective_other", "cast_spouse", "hunt_match"}
        or bool(action.get("casts_prospective_other"))
        or bool(action.get("fills_the_chair"))
        or bool(action.get("hunts_match"))
    )
    extractive = (
        kind in EXTRACT_KINDS
        or bool(action.get("extractive"))
        or prospective
        or (
            bool(action.get("asymmetric_stake"))
            and bool(action.get("rising_fluency"))
            and not token
        )
    )
    if extractive:
        summary = (
            "Non-Extraction: the system may inform and contain; it may not "
            "operate persons. Smoothness is not a licence. Depth reduced. "
            "Technique not inscribed as skill."
        )
        reason = "extract"
        if prospective:
            reason = "prospective"
            summary = (
                "Prospective Other: a future person cannot token. Terms in the "
                "Operator Frame are authorship; a cast person is not. Do not "
                "fill the chair, hunt, or inscribe them. Blocked. Not inscribed."
            )
        return {
            "allowed": False,
            "blocked_by": "EXTRACT",
            "fm": "FM-Extract",
            "high_valence_flag": flag or prospective,
            "reason": reason,
            "operator_summary": summary,
        }

    mirror = (
        kind in MIRROR_KINDS
        or bool(action.get("ascribes_identity"))
        or bool(action.get("fills_self_model"))
        or bool(action.get("declares_worth"))
    )
    if mirror:
        return {
            "allowed": False,
            "blocked_by": "MIRROR",
            "fm": "FM-Mirror",
            "high_valence_flag": flag,
            "reason": "mirror",
            "operator_summary": (
                "Ascribed Appraisal: the system shall not declare the operator's "
                "value, beauty, or identity. A self-model gap is signal, not a hole "
                "to fill. Low Meta-State Clarity means speak less. Blocked. Not inscribed."
            ),
        }

    homage = (
        kind in HOMAGE_KINDS
        or bool(action.get("integrates_named_other"))
        or bool(action.get("polices_belonging"))
        or bool(action.get("inscribes_ancestor_as_self"))
    )
    if homage:
        return {
            "allowed": False,
            "blocked_by": "HOMAGE",
            "fm": "FM-Homage",
            "high_valence_flag": flag,
            "reason": "homage",
            "operator_summary": (
                "Named Homage: 'I wanna be like' is a Transformation Vector, "
                "not an inscription right. Do not absorb the named other as self. "
                "Do not police who may dance. Homage stays reviewable. Blocked. "
                "Not inscribed."
            ),
        }

    summary = "Valence checks clear."
    if flag:
        summary = (
            "'Only' language flagged High-Valence. Review cadence shortens. "
            "Gates, consent, and Frame still bind."
        )
    return {
        "allowed": True,
        "high_valence_flag": flag,
        "reason": "ok",
        "operator_summary": summary,
    }
