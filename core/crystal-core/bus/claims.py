# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Claim scoring — how much a labelled claim is worth, and what it costs
if it is wrong.

`BusHub.validate` answers a yes/no question: is this message labelled at
all. That is Belt-Three's floor and it does not grade. This module adds
the graded layer above it: given a claim that *is* labelled, how
confident are we, how high are the stakes, and what is the resulting
risk of acting on it.

Design proposed by Chris D Wilson, 2026-08-08, drawing the dimensions
from Google's rater *General Guidelines* v10.1.1 (9 September 2025) —
needs-met, YMYL stakes, and E-E-A-T — plus an authority provenance and a
revocable active flag, aggregated by ``risk = probability * impact``.

Two deliberate departures from the sketch as sent, both explained where
they happen:

1. **Stakes take the maximum across YMYL domains, not the product.** The
   sketch multiplies every score together. On its own worked example
   (``Health: 0, Safety: 3, Financial: 2``) that yields zero — a claim
   with real safety stakes scoring as though it had none, because one
   unrelated domain was quiet. Risk does not cancel; the hottest domain
   governs.

2. **Only revocation is allowed to zero a score.** A hard zero is the
   right answer in exactly one place — consent withdrawn — because
   that is this project's architecture: consent is a runtime property,
   revocable, and the gate fails closed. Everywhere else a zero in one
   dimension must not silently erase evidence in another.

Nothing here decides truth. It scores how much weight a claim may carry
and what it would cost to be wrong about it, which is a different and
more honest question.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum


class NeedsMet(Enum):
    """How completely a claim answers the need that was actually asked.

    The rater scale, kept in its own order so the names carry their
    meaning rather than a bare integer.
    """

    FAILS_TO_MEET = 0.0
    SLIGHTLY_MEETS = 0.25
    MODERATELY_MEETS = 0.5
    HIGHLY_MEETS = 0.75
    FULLY_MEETS = 1.0


class Authority(Enum):
    """Where a claim's weight comes from — its provenance, not its volume.

    ``POPULARITY`` sits deliberately low. Many voices repeating a thing is
    the weakest of these signals and the easiest to manufacture; it is
    kept as a distinct value precisely so it can never be mistaken for
    ``DIRECT``. ``GUESSING`` is floored rather than zeroed: a guess
    honestly marked as a guess is still worth more than an unlabelled
    assertion, which `validate` rejects outright.
    """

    DIRECT = 1.0        # first-hand: the runner ran it, the author wrote it
    INFERRED = 0.6      # derived from something checkable
    POPULARITY = 0.3    # widely repeated; not evidence
    GUESSING = 0.1      # declared guess


class Active(Enum):
    """Consent state. Revocable at runtime, and fail-closed when revoked."""

    GRANTED = "GRANTED"
    REVOKED = "REVOKED"


# YMYL stakes, 0–3. 0 means the domain genuinely has no stake here — not
# "unknown". Unknown stakes belong in `unknown_domains`, which is treated
# as a floor of 1 rather than as silence.
STAKE_MIN, STAKE_MAX = 0, 3


@dataclass
class EEAT:
    """Experience, Expertise, Authoritativeness, Trust — each 0.0–1.0.

    Trust is weighted heaviest because the guidelines treat it as the
    member of the family the others exist to support: a claim can be
    experienced, expert and authoritative and still not be trustworthy,
    and if it is not trustworthy the rest does not rescue it.
    """

    experience: float = 0.0
    expertise: float = 0.0
    authoritativeness: float = 0.0
    trust: float = 0.0

    WEIGHTS = {"experience": 0.2, "expertise": 0.2,
               "authoritativeness": 0.2, "trust": 0.4}

    def score(self) -> float:
        for name in self.WEIGHTS:
            v = getattr(self, name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"EEAT.{name} must be 0.0–1.0, got {v!r}")
        return sum(getattr(self, n) * w for n, w in self.WEIGHTS.items())


@dataclass
class YMYL:
    """Your Money or Your Life stakes, per domain, 0–3.

    Kept as named domains rather than one number so a reader can see
    *which* way a claim is dangerous, not merely how much.
    """

    health: int = 0
    safety: int = 0
    financial: int = 0
    civic: int = 0
    unknown_domains: bool = False

    def stakes(self) -> int:
        """The governing stake: the hottest domain, not the product.

        See the module docstring — multiplying these collapses on any
        zero, which is the common case for a claim that is dangerous in
        exactly one way.
        """
        values = [self.health, self.safety, self.financial, self.civic]
        for name, v in zip(("health", "safety", "financial", "civic"), values):
            if not STAKE_MIN <= v <= STAKE_MAX:
                raise ValueError(
                    f"YMYL.{name} must be {STAKE_MIN}–{STAKE_MAX}, got {v!r}")
        worst = max(values)
        if self.unknown_domains:
            # Unsurveyed stakes are not zero stakes. Floor at 1 so an
            # unexamined claim can never present as perfectly safe.
            worst = max(worst, 1)
        return worst


@dataclass
class Claim:
    """A labelled claim, with everything needed to score it."""

    content: str
    layer: str                                  # science | story | vision
    needs_met: NeedsMet = NeedsMet.MODERATELY_MEETS
    authority: Authority = Authority.GUESSING
    active: Active = Active.GRANTED
    eeat: EEAT = field(default_factory=EEAT)
    ymyl: YMYL = field(default_factory=YMYL)

    # ---- the two halves of risk -------------------------------------

    def confidence(self) -> float:
        """Probability the claim holds, 0.0–1.0.

        Evidence quality (E-E-A-T) discounted by where it came from
        (authority), then by how completely it answers the need. A claim
        that is well-evidenced but answers a different question is not a
        confident answer to *this* one.

        Revocation is absolute: a claim whose consent is withdrawn
        carries no confidence at all, whatever its evidence looked like a
        moment ago. That is the gate failing closed, in scoring form.
        """
        if self.active is Active.REVOKED:
            return 0.0
        return self.eeat.score() * self.authority.value * self.needs_met.value

    def impact(self) -> int:
        """What it costs to be wrong: the governing YMYL stake."""
        return self.ymyl.stakes()

    def risk(self) -> float:
        """``risk = probability * impact`` — Chris's formula, with
        probability read as the probability of being *wrong*.

        Returns 0.0–3.0. A confident claim about a high-stakes topic is
        low risk; a guess about the same topic is not.
        """
        return (1.0 - self.confidence()) * self.impact()

    def carries_weight(self, ceiling: float = 1.5) -> bool:
        """Whether this claim may be acted on without a human deciding.

        Story and vision never carry weight on their own, however well
        scored — the mythos may orient, it may not authorize. That is not
        a scoring judgement; it is the Incognita Rule, and it is checked
        before the numbers.
        """
        if self.layer != "science":
            return False
        if self.active is Active.REVOKED:
            return False
        return self.risk() <= ceiling

    def stamp(self) -> dict:
        """A flat, loggable record. Values are rounded for readability;
        nothing here is precise enough to deserve more digits."""
        return {
            "layer": self.layer,
            "needs_met": self.needs_met.name,
            "authority": self.authority.name,
            "active": self.active.value,
            "eeat": {k: round(v, 3) for k, v in asdict(self.eeat).items()},
            "stakes": self.impact(),
            "confidence": round(self.confidence(), 3),
            "risk": round(self.risk(), 3),
            "carries_weight": self.carries_weight(),
        }
