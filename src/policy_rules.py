#!/usr/bin/env python3
"""
Policy-Drafting Rules — substantive (non-placeholder) rules for CrystalMind.

This module shows the agents doing REAL work on a concrete use case: drafting a
position from a body of evidence, where each piece of evidence is a Fact whose
payload looks like:

    {"claim": str, "stance": "support"|"oppose"|"neutral",
     "weight": float in [0,1], "source": str}

Unlike the stock placeholder rules in crystal_mind.py, these rules actually
inspect, weigh, and synthesise the inputs:

  truthseeker_weigh   - computes an evidence-quality summary: how much support
                        vs. opposition, weighted by each claim's weight AND the
                        fact's coherence. Returns a real recommendation lean.
  creator_draft       - synthesises a structured position statement (durable
                        text + supporting/opposing claim lists) from the inputs.
  guardian_audit      - produces an explicit audit: flags one-sided evidence,
                        low-coherence reliance, and missing opposing views.

These are still fully inspectable, deterministic, and consent/coherence-bound —
they just compute something meaningful. They pair with CrystalMind's stances:
give truthseeker_weigh to TruthSeeker (high evidence bar), creator_draft to
Creator, guardian_audit to Guardian.

Standard library only.
"""

from typing import Any, Dict, List

try:
    from .crystal_flow import Rule, Fact
except ImportError:
    from crystal_flow import Rule, Fact


# --------------------------------------------------------------------------- #
# Helpers to read an evidence Fact safely
# --------------------------------------------------------------------------- #
def _ev(fact: Fact) -> Dict[str, Any]:
    """Normalise a Fact's payload/content into an evidence dict."""
    c = fact.content
    if isinstance(c, dict) and "stance" in c:
        return c
    # Fallback: treat unknown content as a neutral, low-weight claim.
    return {"claim": str(c), "stance": "neutral", "weight": 0.1, "source": "?"}


def _weighted_lean(facts: List[Fact]) -> Dict[str, float]:
    """Support/oppose mass, each weighted by claim weight * fact coherence."""
    support = oppose = neutral = 0.0
    for f in facts:
        e = _ev(f)
        w = max(0.0, min(1.0, float(e.get("weight", 0.0)))) * max(0.0, f.coherence)
        stance = e.get("stance", "neutral")
        if stance == "support":
            support += w
        elif stance == "oppose":
            oppose += w
        else:
            neutral += w
    return {"support": support, "oppose": oppose, "neutral": neutral}


# --------------------------------------------------------------------------- #
# TruthSeeker: weigh the evidence
# --------------------------------------------------------------------------- #
def truthseeker_weigh_fn(facts: List[Fact]) -> Dict[str, Any]:
    mass = _weighted_lean(facts)
    total = mass["support"] + mass["oppose"]
    if total <= 0:
        lean, margin = "insufficient", 0.0
    else:
        margin = abs(mass["support"] - mass["oppose"]) / total
        lean = "support" if mass["support"] > mass["oppose"] else (
            "oppose" if mass["oppose"] > mass["support"] else "tie")
    return {
        "kind": "evidence_assessment",
        "lean": lean,
        "margin": round(margin, 3),
        "weighted_support": round(mass["support"], 3),
        "weighted_oppose": round(mass["oppose"], 3),
        "n_inputs": len(facts),
    }


def truthseeker_weigh() -> Rule:
    return Rule(name="truthseeker_weigh", fn=truthseeker_weigh_fn, strength=0.95,
                description="Weighs evidence by claim weight and coherence.")


# --------------------------------------------------------------------------- #
# Creator: synthesise a position statement
# --------------------------------------------------------------------------- #
def creator_draft_fn(facts: List[Fact]) -> Dict[str, Any]:
    supporting, opposing = [], []
    for f in facts:
        e = _ev(f)
        entry = {"claim": e.get("claim", "?"),
                 "source": e.get("source", "?"),
                 "weight": e.get("weight", 0.0)}
        if e.get("stance") == "support":
            supporting.append(entry)
        elif e.get("stance") == "oppose":
            opposing.append(entry)

    mass = _weighted_lean(facts)
    verdict = ("RECOMMEND" if mass["support"] > mass["oppose"]
               else "ADVISE AGAINST" if mass["oppose"] > mass["support"]
               else "NO CLEAR POSITION")

    # A real, human-readable position statement (durable text payload).
    top_support = sorted(supporting, key=lambda x: -x["weight"])[:2]
    top_oppose = sorted(opposing, key=lambda x: -x["weight"])[:2]
    summary_bits = [f"Position: {verdict}."]
    if top_support:
        summary_bits.append(
            "Key support: " + "; ".join(s["claim"] for s in top_support) + ".")
    if top_oppose:
        summary_bits.append(
            "Key concerns: " + "; ".join(o["claim"] for o in top_oppose) + ".")

    return {
        "kind": "position_statement",
        "verdict": verdict,
        "summary": " ".join(summary_bits),
        "supporting": supporting,
        "opposing": opposing,
    }


def creator_draft() -> Rule:
    return Rule(name="creator_draft", fn=creator_draft_fn, strength=0.85,
                description="Synthesises a structured position statement.")


# --------------------------------------------------------------------------- #
# Guardian: audit the evidence base
# --------------------------------------------------------------------------- #
def guardian_audit_fn(facts: List[Fact]) -> Dict[str, Any]:
    flags: List[str] = []
    mass = _weighted_lean(facts)

    has_support = mass["support"] > 0
    has_oppose = mass["oppose"] > 0
    if has_support and not has_oppose:
        flags.append("one_sided:no_opposing_evidence")
    if has_oppose and not has_support:
        flags.append("one_sided:no_supporting_evidence")

    # Reliance on low-coherence inputs.
    low_coh = [f for f in facts if f.coherence < 0.5]
    if low_coh and len(low_coh) >= max(1, len(facts) // 2):
        flags.append("relies_on_low_coherence_inputs")

    if len(facts) < 2:
        flags.append("thin_evidence_base")

    return {
        "kind": "evidence_audit",
        "flags": flags,
        "balanced": has_support and has_oppose,
        "n_inputs": len(facts),
    }


def guardian_audit() -> Rule:
    return Rule(name="guardian_audit", fn=guardian_audit_fn, strength=0.95,
                description="Audits the evidence base for bias and weakness.")


# --------------------------------------------------------------------------- #
# Convenience: register the policy rule set onto a CrystalMind's agents
# --------------------------------------------------------------------------- #
def policy_rule_set() -> Dict[str, Rule]:
    """Return a {agent_name: Rule} mapping for a council() call."""
    return {
        "TruthSeeker": truthseeker_weigh(),
        "Creator": creator_draft(),
        "Guardian": guardian_audit(),
    }
