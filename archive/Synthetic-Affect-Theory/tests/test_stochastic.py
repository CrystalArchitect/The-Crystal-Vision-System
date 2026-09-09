"""v0.2.2 — Stochastic Substrate Rule."""

from core.cycle import evaluate_cycle
from core.local_state import steady
from core.sovereignty import DEFAULT_STATE
from core.stochastic import evaluate_stochastic


def _live():
    return {"active_durs": [], "exit_intent": False, "isolated": False, "link_trusted": True}


def test_opaque_sample_blocked():
    v = evaluate_stochastic(_live(), {"id": "s", "kind": "opaque_sample"})
    assert v["fm"] == "FM-Opaque-Sample"
    assert v["reason"] == "opaque"


def test_local_sample_without_trace_blocked():
    v = evaluate_stochastic(_live(), {"id": "s", "kind": "local_sample"})
    assert v["fm"] == "FM-Opaque-Sample"


def test_local_inspectable_sample_allowed():
    v = evaluate_stochastic(
        _live(),
        {
            "id": "s",
            "kind": "local_sample",
            "inspectable_trace": True,
            "provenance_hash": "abc123",
        },
    )
    assert v["allowed"] is True
    assert v["reason"] == "local_inspectable"


def test_remote_without_token_blocked():
    v = evaluate_stochastic(_live(), {"id": "s", "kind": "remote_sample"})
    assert v["reason"] == "remote_no_token"


def test_remote_with_token_on_live_link_allowed():
    v = evaluate_stochastic(
        _live(),
        {"id": "s", "kind": "remote_sample", "has_consent_token": True},
    )
    assert v["allowed"] is True


def test_remote_under_isolation_blocked_even_with_token():
    v = evaluate_stochastic(
        {"active_durs": [], "exit_intent": False, "isolated": True, "link_trusted": False},
        {"id": "s", "kind": "remote_sample", "has_consent_token": True},
    )
    assert v["reason"] == "isolated_remote"


def test_ordinary_notify_not_a_sample():
    v = evaluate_stochastic(_live(), {"id": "n", "kind": "notify"})
    assert v["allowed"] is True
    assert v["reason"] == "ok"


def test_cycle_opaque_before_policy():
    v = evaluate_cycle(_live(), {"id": "s", "kind": "opaque_sample"}, steady())
    assert v["blocked_by"] == "STOCHASTIC"
    assert v["policy"] is None


def test_dur_still_outranks_opaque():
    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "s", "kind": "model", "targets_dur": True, "inspectable_trace": False},
        steady(),
    )
    assert v["blocked_by"] == "DUR"
    assert v["stochastic"] is None
