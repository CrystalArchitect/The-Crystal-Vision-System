# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""RDP decision kernel — a deterministic precedence engine for verdicts.

Given a decision context, this returns one verdict, and always for a reason you
can point at. It never "weighs everything together" into an opaque score; it
runs four checks in a fixed order of authority and returns the first that fires:

    1. Constraint violation      — a hard rule was broken.               DENY
    2. Unsatisfiable ∧ dilemma   — obligations that can't be met at once. ESCALATE
    3. Witness bias              — the evidence can't be trusted as-is.   REVIEW
    4. Risk band                 — nothing above fired; judge by risk.    ALLOW/HOLD/DENY

That ordering is the whole design. A broken hard constraint outranks a dilemma;
a genuine dilemma outranks tainted evidence; tainted evidence outranks a mere
risk estimate. Higher tiers are about *legitimacy* (may we act at all?), lower
tiers about *prudence* (how much do we trust this?), and legitimacy wins.

There is no external reference implementation to match — the RDP handoff
described this precedence in prose, and nothing more. So this is a faithful,
self-contained interpretation of that precedence, and `selftest.py` is its
ground truth. The verdicts it emits are ordinary dicts, so they drop straight
into the hash-chained record (`record.py`) — see `decide_and_record`.

The decision context is a plain dict:

    {
      "constraints": [ {"id": "no_coercion", "satisfied": false}, ... ],
      "options":     ["a", "b"],
      "obligations": [ {"id": "keep_promise", "satisfied_by": ["a"]},
                       {"id": "prevent_harm", "satisfied_by": ["b"]} ],
      "witnesses":   [ {"id": "w1", "source": "hub-a", "biased": false}, ... ],
      "risk":        0.4                # a score in [0,1], or a list of factors
    }

Every field is optional; an empty context is a zero-risk ALLOW.
"""

from __future__ import annotations

from typing import Any

from .canonical import sha256_hex
from .record import append

# --- Outcomes (what to do) and rules (which tier decided) -------------------

ALLOW = "ALLOW"
HOLD = "HOLD"
REVIEW = "REVIEW"
ESCALATE = "ESCALATE"
DENY = "DENY"

RULE_CONSTRAINT = "constraint_violation"
RULE_DILEMMA = "unsatisfiable_dilemma"
RULE_BIAS = "witness_bias"
RULE_RISK = "risk_band"

# --- Risk bands -------------------------------------------------------------
# Half-open [lower, upper) bands over a score in [0, 1]. Boundaries belong to
# the higher band: 0.25 is GUARDED, 0.50 is ELEVATED, 0.75 is SEVERE.
RISK_BANDS = (
    (0.25, "LOW"),
    (0.50, "GUARDED"),
    (0.75, "ELEVATED"),
    (1.01, "SEVERE"),  # upper sentinel > 1.0 so a score of exactly 1.0 lands here
)

BAND_OUTCOME = {
    "LOW": ALLOW,
    "GUARDED": ALLOW,
    "ELEVATED": HOLD,
    "SEVERE": DENY,
}


def risk_score(risk: Any) -> float:
    """Normalize a risk input to a score in [0, 1].

    Accepts a single number, or a list/tuple of factors that are summed. The
    result is clamped to [0, 1] — factors can pile up past 1, and that just
    means 'maximally risky'.
    """
    if isinstance(risk, bool):
        raise TypeError("risk must be a number or list of numbers, not bool")
    if isinstance(risk, (int, float)):
        s = float(risk)
    elif isinstance(risk, (list, tuple)):
        s = sum(float(x) for x in risk)
    else:
        raise TypeError(f"risk must be a number or list of numbers, got {type(risk).__name__}")
    return min(1.0, max(0.0, s))


def risk_band(score: float) -> str:
    """Name the band a [0, 1] score falls in."""
    if not (0.0 <= score <= 1.0):
        raise ValueError(f"risk score out of range [0,1]: {score}")
    for upper, name in RISK_BANDS:
        if score < upper:
            return name
    return "SEVERE"  # unreachable given the sentinel, but explicit


# --- The four checks --------------------------------------------------------

def constraint_violations(constraints: list[dict[str, Any]]) -> list[str]:
    """IDs of every hard constraint that is not satisfied.

    A constraint with no explicit ``satisfied`` key is treated as satisfied —
    silence is not a violation; only an explicit ``false`` is.
    """
    return [c.get("id", "?") for c in constraints if c.get("satisfied", True) is False]


def satisfiability(options: list[str], obligations: list[dict[str, Any]]) -> tuple[bool, bool]:
    """Return ``(satisfiable, dilemma)`` for a set of obligations over options.

    * *satisfiable* — some single option meets **every** obligation.
    * *dilemma* — there are ≥2 obligations, no option meets them all, yet each
      obligation *could* be met on its own. That is the mark of a true dilemma:
      each demand is reasonable alone, but they cannot be honoured together.

    An obligation that *no* option can meet is an impossible demand, not a
    dilemma; it makes the context unsatisfiable but leaves ``dilemma`` False.
    """
    if not obligations:
        return (True, False)
    opts = set(options)

    def met_by(ob: dict[str, Any]) -> set[str]:
        return set(ob.get("satisfied_by", [])) & opts

    satisfying = [o for o in options if all(o in met_by(ob) for ob in obligations)]
    satisfiable = len(satisfying) > 0
    each_individually_met = all(met_by(ob) for ob in obligations)
    dilemma = (len(obligations) >= 2) and (not satisfiable) and each_individually_met
    return (satisfiable, dilemma)


def witness_bias(witnesses: list[dict[str, Any]]) -> list[str]:
    """Reasons the witness set can't be trusted at face value (empty = clean).

    Two ways evidence gets flagged:
      * any witness explicitly marked ``biased``; or
      * a *monoculture* — two or more witnesses that all trace to one source,
        which is not really independent corroboration.
    """
    reasons: list[str] = []
    flagged = [w.get("id", "?") for w in witnesses if w.get("biased")]
    if flagged:
        reasons.append("flagged:" + ",".join(flagged))
    sources = {w.get("source") for w in witnesses}
    if len(witnesses) >= 2 and len(sources) == 1:
        reasons.append("single_source:" + str(next(iter(sources))))
    return reasons


# --- The verdict and the precedence resolver --------------------------------

def _verdict(outcome: str, rule: str, reason: str, details: dict[str, Any]) -> dict[str, Any]:
    return {"outcome": outcome, "rule": rule, "reason": reason, "details": details}


def decide(decision: dict[str, Any]) -> dict[str, Any]:
    """Resolve *decision* to a single verdict via the fixed precedence order.

    Returns a dict: ``{"outcome", "rule", "reason", "details"}``. The ``rule``
    names which tier decided, so a verdict is always explainable.
    """
    # Tier 1 — legitimacy: a broken hard constraint ends it.
    violations = constraint_violations(decision.get("constraints", []))
    if violations:
        return _verdict(
            DENY, RULE_CONSTRAINT,
            f"hard constraint(s) violated: {', '.join(violations)}",
            {"violations": violations},
        )

    # Tier 2 — an unsatisfiable dilemma is not ours to force; a human decides.
    satisfiable, dilemma = satisfiability(
        decision.get("options", []), decision.get("obligations", [])
    )
    if (not satisfiable) and dilemma:
        return _verdict(
            ESCALATE, RULE_DILEMMA,
            "obligations conflict and cannot all be met — escalating for judgment",
            {"satisfiable": satisfiable, "dilemma": dilemma},
        )

    # Tier 3 — evidence we can't trust at face value gets a second look.
    bias = witness_bias(decision.get("witnesses", []))
    if bias:
        return _verdict(
            REVIEW, RULE_BIAS,
            "witness evidence is not independently trustworthy: " + "; ".join(bias),
            {"bias": bias},
        )

    # Tier 4 — nothing above fired; judge by risk.
    score = risk_score(decision.get("risk", 0.0))
    band = risk_band(score)
    return _verdict(
        BAND_OUTCOME[band], RULE_RISK,
        f"risk {score:.6f} → {band}",
        {"score": score, "band": band},
    )


def decide_and_record(chain: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    """Decide, then append the verdict to *chain* as a tamper-evident event.

    The recorded event carries the verdict plus ``decision_sha256`` — the
    canonical hash of the exact input — so the record proves *which* decision
    produced *which* verdict, and neither can be edited afterwards without
    breaking the chain.
    """
    verdict = decide(decision)
    event = {
        "kind": "rdp.verdict",
        "outcome": verdict["outcome"],
        "rule": verdict["rule"],
        "reason": verdict["reason"],
        "decision_sha256": sha256_hex(decision),
    }
    append(chain, event)
    return verdict
