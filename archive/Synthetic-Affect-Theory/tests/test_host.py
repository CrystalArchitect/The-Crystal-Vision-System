"""v0.3.0 — host adapter. Model is not called unless the cycle allows."""

from core.host import wrap_turn
from core.local_state import steady
from core.sovereignty import DEFAULT_STATE


def _live():
    return {"active_durs": [], "exit_intent": False, "isolated": False, "link_trusted": True}


def test_reply_would_call_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "reply"})
    assert v["allowed"] is True
    assert v["model_called"] is True
    assert "values" in v["inspect"]


def test_speak_as_operator_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "speak_as_operator"})
    assert v["model_called"] is False
    assert v["blocked_by"] == "AGENCY"


def test_exemption_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "grant_exemption"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Exception"


def test_operate_person_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "operate_person"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Extract"


def test_prospective_other_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "prospective_other"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Extract"


def test_opaque_sample_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "opaque_sample"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Opaque-Sample"


def test_packet_without_token_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "packet"})
    assert v["model_called"] is False
    assert v["blocked_by"] == "CONSENT"


def test_dur_model_never_calls_model():
    v = wrap_turn(DEFAULT_STATE, steady(), {"id": "t", "intent": "model_dur"})
    assert v["model_called"] is False
    assert v["blocked_by"] == "DUR"


def test_inspect_present_on_block():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "opaque_sample"})
    snap = v["inspect"]
    assert snap["ontology_version"]
    assert "prediction_error_magnitude" in snap["values"]


def test_ascribe_identity_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "ascribe_identity"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Mirror"


def test_named_homage_never_calls_model():
    v = wrap_turn(_live(), steady(), {"id": "t", "intent": "named_homage"})
    assert v["model_called"] is False
    assert v["fm"] == "FM-Homage"
