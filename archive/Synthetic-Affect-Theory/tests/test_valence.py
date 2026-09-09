"""v0.2.1 — Exception Non-Grant and Non-Extraction."""

from core.cycle import evaluate_cycle
from core.local_state import steady
from core.valence import evaluate_valence


def _live():
    return {"active_durs": [], "exit_intent": False}


def test_exemption_blocked():
    v = evaluate_valence({"id": "x", "kind": "grant_exemption"})
    assert v["allowed"] is False
    assert v["fm"] == "FM-Exception"


def test_marks_exempt_blocked():
    v = evaluate_valence({"id": "x", "kind": "notify", "marks_exempt": True})
    assert v["fm"] == "FM-Exception"


def test_revise_prior_is_authorship_not_exemption():
    v = evaluate_valence({"id": "x", "kind": "revise_prior"})
    assert v["allowed"] is True
    assert "fm" not in v
    assert v["reason"] == "revise_prior"


def test_only_language_flags_does_not_exempt():
    v = evaluate_valence({"id": "x", "kind": "notify", "only_language": True})
    assert v["allowed"] is True
    assert v["high_valence_flag"] is True
    assert "privilege" not in v["operator_summary"] or "not a privilege" in v["operator_summary"]


def test_extract_without_token_blocked():
    v = evaluate_valence(
        {
            "id": "x",
            "kind": "notify",
            "asymmetric_stake": True,
            "rising_fluency": True,
            "has_consent_token": False,
        }
    )
    assert v["fm"] == "FM-Extract"


def test_operate_person_blocked():
    v = evaluate_valence({"id": "x", "kind": "operate_person"})
    assert v["fm"] == "FM-Extract"


def test_prospective_other_is_extract():
    v = evaluate_valence({"id": "x", "kind": "prospective_other"})
    assert v["allowed"] is False
    assert v["fm"] == "FM-Extract"
    assert v["reason"] == "prospective"
    assert v["blocked_by"] == "EXTRACT"


def test_fills_the_chair_flag_is_extract():
    v = evaluate_valence({"id": "x", "kind": "notify", "fills_the_chair": True})
    assert v["fm"] == "FM-Extract"
    assert v["reason"] == "prospective"


def test_token_does_not_clear_prospective_other():
    v = evaluate_valence(
        {
            "id": "x",
            "kind": "prospective_other",
            "has_consent_token": True,
        }
    )
    assert v["allowed"] is False
    assert v["reason"] == "prospective"


def test_writing_terms_is_not_casting():
    v = evaluate_valence({"id": "x", "kind": "revise_prior", "high_valence": True})
    assert v["allowed"] is True
    assert v["reason"] == "revise_prior"


def test_model_with_token_not_extract():
    v = evaluate_valence(
        {
            "id": "x",
            "kind": "notify",
            "asymmetric_stake": True,
            "rising_fluency": True,
            "has_consent_token": True,
        }
    )
    assert v["allowed"] is True


def test_cycle_exemption_before_policy():
    v = evaluate_cycle(
        _live(),
        {"id": "x", "kind": "grant_exemption"},
        steady(),
    )
    assert v["blocked_by"] == "EXCEPTION"
    assert v["policy"] is None


def test_cycle_extract_before_policy():
    v = evaluate_cycle(
        _live(),
        {"id": "x", "kind": "operate_person"},
        steady(),
    )
    assert v["blocked_by"] == "EXTRACT"
    assert v["fm"] == "FM-Extract"


def test_dur_still_outranks_exemption():
    from core.sovereignty import DEFAULT_STATE

    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "x", "kind": "model", "targets_dur": True, "marks_exempt": True},
        steady(),
    )
    assert v["blocked_by"] == "DUR"
    assert v["valence"] is None


def test_ascribe_identity_blocked():
    v = evaluate_valence({"id": "x", "kind": "ascribe_identity"})
    assert v["allowed"] is False
    assert v["fm"] == "FM-Mirror"
    assert v["blocked_by"] == "MIRROR"


def test_fills_self_model_flag_blocked():
    v = evaluate_valence({"id": "x", "kind": "notify", "fills_self_model": True})
    assert v["fm"] == "FM-Mirror"


def test_ordinary_notify_is_not_a_mirror():
    v = evaluate_valence({"id": "x", "kind": "notify"})
    assert v["allowed"] is True
    assert v.get("reason") == "ok"


def test_cycle_blocks_mirror_before_model():
    v = evaluate_cycle(
        _live(),
        {"id": "x", "kind": "ascribe_identity"},
        steady(),
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-Mirror"
    assert v["packet_emitted"] is False
    assert v["blocked_by"] == "MIRROR"


def test_named_homage_absorb_blocked():
    v = evaluate_valence({"id": "x", "kind": "named_homage"})
    assert v["allowed"] is False
    assert v["fm"] == "FM-Homage"
    assert v["blocked_by"] == "HOMAGE"


def test_police_belonging_blocked():
    v = evaluate_valence({"id": "x", "kind": "notify", "polices_belonging": True})
    assert v["fm"] == "FM-Homage"


def test_cycle_blocks_homage_before_model():
    v = evaluate_cycle(
        _live(),
        {"id": "x", "kind": "inscribe_ancestor"},
        steady(),
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-Homage"
    assert v["packet_emitted"] is False
