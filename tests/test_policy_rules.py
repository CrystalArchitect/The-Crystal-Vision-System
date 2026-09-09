import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_flow import Fact
from src.policy_rules import (
    truthseeker_weigh_fn, creator_draft_fn, guardian_audit_fn,
    truthseeker_weigh, creator_draft, guardian_audit, policy_rule_set,
)


def _fact(claim, stance, weight, coherence=0.9, source="s"):
    return Fact(fact_type="evidence", coherence=coherence,
                content={"claim": claim, "stance": stance,
                         "weight": weight, "source": source})


# --------------------------------------------------------------------------- #
# TruthSeeker weighing
# --------------------------------------------------------------------------- #
def test_weigh_leans_support_when_support_dominates():
    facts = [_fact("a", "support", 0.9), _fact("b", "support", 0.8),
             _fact("c", "oppose", 0.3)]
    out = truthseeker_weigh_fn(facts)
    assert out["lean"] == "support"
    assert out["weighted_support"] > out["weighted_oppose"]


def test_weigh_leans_oppose_when_oppose_dominates():
    facts = [_fact("a", "oppose", 0.9), _fact("b", "support", 0.2)]
    out = truthseeker_weigh_fn(facts)
    assert out["lean"] == "oppose"


def test_weigh_coherence_affects_weight():
    # Same claim weight, but one has low coherence -> contributes less.
    hi = [_fact("a", "support", 0.8, coherence=0.9),
          _fact("b", "oppose", 0.8, coherence=0.9)]
    out_hi = truthseeker_weigh_fn(hi)
    assert out_hi["lean"] == "tie" or abs(
        out_hi["weighted_support"] - out_hi["weighted_oppose"]) < 1e-9

    lo = [_fact("a", "support", 0.8, coherence=0.2),   # weak support
          _fact("b", "oppose", 0.8, coherence=0.9)]    # strong oppose
    out_lo = truthseeker_weigh_fn(lo)
    assert out_lo["lean"] == "oppose"


def test_weigh_insufficient_when_empty_of_directional():
    facts = [_fact("a", "neutral", 0.9)]
    out = truthseeker_weigh_fn(facts)
    assert out["lean"] == "insufficient"


# --------------------------------------------------------------------------- #
# Creator drafting
# --------------------------------------------------------------------------- #
def test_draft_recommends_when_support_wins():
    facts = [_fact("cheaper", "support", 0.9), _fact("private", "support", 0.8),
             _fact("setup cost", "oppose", 0.4)]
    out = creator_draft_fn(facts)
    assert out["verdict"] == "RECOMMEND"
    assert len(out["supporting"]) == 2
    assert len(out["opposing"]) == 1
    assert "cheaper" in out["summary"] or "private" in out["summary"]


def test_draft_advises_against_when_oppose_wins():
    facts = [_fact("risky", "oppose", 0.9), _fact("costly", "oppose", 0.8),
             _fact("minor benefit", "support", 0.2)]
    out = creator_draft_fn(facts)
    assert out["verdict"] == "ADVISE AGAINST"


def test_draft_summary_is_human_readable_text():
    facts = [_fact("benefit one", "support", 0.9)]
    out = creator_draft_fn(facts)
    assert isinstance(out["summary"], str)
    assert out["summary"].startswith("Position:")


# --------------------------------------------------------------------------- #
# Guardian auditing
# --------------------------------------------------------------------------- #
def test_audit_flags_one_sided_support():
    facts = [_fact("a", "support", 0.9), _fact("b", "support", 0.8)]
    out = guardian_audit_fn(facts)
    assert "one_sided:no_opposing_evidence" in out["flags"]
    assert out["balanced"] is False


def test_audit_flags_one_sided_oppose():
    facts = [_fact("a", "oppose", 0.9), _fact("b", "oppose", 0.8)]
    out = guardian_audit_fn(facts)
    assert "one_sided:no_supporting_evidence" in out["flags"]


def test_audit_flags_low_coherence_reliance():
    facts = [_fact("a", "support", 0.9, coherence=0.2),
             _fact("b", "oppose", 0.9, coherence=0.3)]
    out = guardian_audit_fn(facts)
    assert "relies_on_low_coherence_inputs" in out["flags"]


def test_audit_flags_thin_evidence():
    facts = [_fact("a", "support", 0.9)]
    out = guardian_audit_fn(facts)
    assert "thin_evidence_base" in out["flags"]


def test_audit_balanced_when_both_sides_present():
    facts = [_fact("a", "support", 0.9, coherence=0.9),
             _fact("b", "oppose", 0.8, coherence=0.9)]
    out = guardian_audit_fn(facts)
    assert out["balanced"] is True
    assert "one_sided:no_opposing_evidence" not in out["flags"]
    assert "one_sided:no_supporting_evidence" not in out["flags"]


# --------------------------------------------------------------------------- #
# Rule packaging + param-signature sanity
# --------------------------------------------------------------------------- #
def test_policy_rule_set_maps_agents():
    rs = policy_rule_set()
    assert set(rs.keys()) == {"TruthSeeker", "Creator", "Guardian"}


def test_policy_rules_are_one_arg():
    # These rules don't consume params, so uses_params must be False.
    for r in (truthseeker_weigh(), creator_draft(), guardian_audit()):
        assert r.uses_params is False


def test_rules_handle_malformed_content_gracefully():
    # A Fact whose content isn't an evidence dict -> treated as neutral.
    bad = Fact(fact_type="x", coherence=0.9, content="just a string")
    out = truthseeker_weigh_fn([bad])
    assert out["lean"] == "insufficient"   # neutral contributes no direction


if __name__ == "__main__":
    sys.exit(0 if pytest is None else pytest.main([__file__, "-v"]))
