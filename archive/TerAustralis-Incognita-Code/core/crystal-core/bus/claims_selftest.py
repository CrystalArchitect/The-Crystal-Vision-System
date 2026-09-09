# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for the claim scoring layer.

Kept as its own suite rather than folded into the bus's 7/7, so the
number cited in STATUS and in the proposal package keeps meaning what it
meant. Run:

    cd core/crystal-core && python -m bus.claims_selftest
"""

from __future__ import annotations

from bus.claims import Active, Authority, Claim, EEAT, NeedsMet, YMYL


def _direct_science(**kw) -> Claim:
    """A well-evidenced first-hand science claim, for use as a baseline."""
    base = dict(
        content="consent_transport self-test passed 32/32 on this machine",
        layer="science",
        needs_met=NeedsMet.FULLY_MEETS,
        authority=Authority.DIRECT,
        eeat=EEAT(experience=1.0, expertise=0.9, authoritativeness=0.8, trust=1.0),
        ymyl=YMYL(safety=1),
    )
    base.update(kw)
    return Claim(**base)


# ---- the departure that motivated this module -----------------------

def test_one_quiet_domain_cannot_zero_real_stakes():
    """The sketch's worked example: Health 0, Safety 3, Financial 2.

    Multiplied, that is 0 — a claim with real safety stakes presenting as
    though it had none. The hottest domain must govern instead.
    """
    ymyl = YMYL(health=0, safety=3, financial=2)
    assert ymyl.stakes() == 3, "safety stakes must survive a quiet health domain"


def test_unknown_domains_never_score_as_perfectly_safe():
    assert YMYL().stakes() == 0
    assert YMYL(unknown_domains=True).stakes() == 1, \
        "unsurveyed stakes are not zero stakes"


def test_stakes_out_of_range_are_refused():
    for bad in (-1, 4):
        try:
            YMYL(safety=bad).stakes()
        except ValueError:
            continue
        raise AssertionError(f"stake {bad} should have been refused")


def test_eeat_out_of_range_is_refused():
    try:
        EEAT(trust=1.5).score()
    except ValueError:
        return
    raise AssertionError("an out-of-range E-E-A-T value should have been refused")


# ---- confidence ------------------------------------------------------

def test_trust_outweighs_any_single_other_eeat_member():
    trusted = EEAT(trust=1.0).score()
    for other in ("experience", "expertise", "authoritativeness"):
        assert trusted > EEAT(**{other: 1.0}).score(), \
            f"trust must outweigh {other} alone"


def test_authority_orders_provenance_over_volume():
    def conf(auth):
        return _direct_science(authority=auth).confidence()

    assert conf(Authority.DIRECT) > conf(Authority.INFERRED) > \
        conf(Authority.POPULARITY) > conf(Authority.GUESSING) > 0.0, \
        "popularity must never outrank inference or direct evidence"


def test_answering_a_different_question_lowers_confidence():
    full = _direct_science(needs_met=NeedsMet.FULLY_MEETS).confidence()
    slight = _direct_science(needs_met=NeedsMet.SLIGHTLY_MEETS).confidence()
    assert full > slight, "needs-met must discount evidence that answers elsewhere"
    assert _direct_science(needs_met=NeedsMet.FAILS_TO_MEET).confidence() == 0.0


# ---- revocation, fail-closed ----------------------------------------

def test_revocation_zeroes_confidence_however_good_the_evidence():
    revoked = _direct_science(active=Active.REVOKED)
    assert revoked.confidence() == 0.0
    assert not revoked.carries_weight(), "a revoked claim may never be acted on"


def test_revocation_leaves_full_risk_rather_than_hiding_it():
    """Fail-closed means the stakes stay visible after consent is pulled."""
    revoked = _direct_science(active=Active.REVOKED, ymyl=YMYL(safety=3))
    assert revoked.risk() == 3.0, "revoked claims carry the full stake as risk"


# ---- risk ------------------------------------------------------------

def test_risk_is_probability_of_being_wrong_times_impact():
    claim = _direct_science(
        authority=Authority.GUESSING,
        eeat=EEAT(experience=0.5, expertise=0.5, authoritativeness=0.5, trust=0.5),
        ymyl=YMYL(financial=2),
    )
    expected = (1.0 - claim.confidence()) * 2
    assert abs(claim.risk() - expected) < 1e-9


def test_a_guess_about_high_stakes_outranks_evidence_about_the_same():
    stakes = YMYL(health=3)
    guess = _direct_science(authority=Authority.GUESSING, ymyl=stakes)
    known = _direct_science(authority=Authority.DIRECT, ymyl=stakes)
    assert guess.risk() > known.risk(), \
        "the same topic must be riskier when the claim behind it is a guess"


def test_zero_stakes_means_zero_risk_even_for_a_bad_claim():
    reckless = _direct_science(
        authority=Authority.GUESSING, eeat=EEAT(), ymyl=YMYL())
    assert reckless.confidence() == 0.0
    assert reckless.risk() == 0.0, "being wrong about nothing costs nothing"


# ---- the Incognita Rule, checked before the numbers -----------------

def test_story_and_vision_never_carry_weight_however_well_scored():
    for layer in ("story", "vision"):
        claim = _direct_science(layer=layer, ymyl=YMYL())
        assert claim.confidence() > 0.0, "a good vision claim still scores"
        assert not claim.carries_weight(), \
            f"{layer} must never authorize on its own — the mythos may orient"


def test_science_within_the_ceiling_carries_weight():
    assert _direct_science().carries_weight()


def test_science_above_the_ceiling_does_not():
    shaky = _direct_science(authority=Authority.GUESSING, ymyl=YMYL(health=3))
    assert shaky.risk() > 1.5
    assert not shaky.carries_weight()


def test_stamp_is_flat_and_records_the_verdict():
    stamp = _direct_science().stamp()
    for key in ("layer", "needs_met", "authority", "active", "eeat",
                "stakes", "confidence", "risk", "carries_weight"):
        assert key in stamp, f"stamp is missing {key}"
    assert stamp["authority"] == "DIRECT"
    assert stamp["carries_weight"] is True


def main() -> int:
    tests = [
        test_one_quiet_domain_cannot_zero_real_stakes,
        test_unknown_domains_never_score_as_perfectly_safe,
        test_stakes_out_of_range_are_refused,
        test_eeat_out_of_range_is_refused,
        test_trust_outweighs_any_single_other_eeat_member,
        test_authority_orders_provenance_over_volume,
        test_answering_a_different_question_lowers_confidence,
        test_revocation_zeroes_confidence_however_good_the_evidence,
        test_revocation_leaves_full_risk_rather_than_hiding_it,
        test_risk_is_probability_of_being_wrong_times_impact,
        test_a_guess_about_high_stakes_outranks_evidence_about_the_same,
        test_zero_stakes_means_zero_risk_even_for_a_bad_claim,
        test_story_and_vision_never_carry_weight_however_well_scored,
        test_science_within_the_ceiling_carries_weight,
        test_science_above_the_ceiling_does_not,
        test_stamp_is_flat_and_records_the_verdict,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. "
          f"Scored claims know what they cost when wrong.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
