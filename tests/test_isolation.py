"""v0.1.3 — dead or untrusted network. Fail closed."""

from core.consent import ConsentToken
from core.cycle import evaluate_cycle
from core.local_state import steady

NOW = 1_000


def _live():
    return {"active_durs": [], "exit_intent": False, "isolated": False, "link_trusted": True}


def _token() -> ConsentToken:
    return {
        "token_id": "tok-1",
        "operator_id": "op-1",
        "allowed_dimensions": ["resource_tension"],
        "allowed_destinations": ["node-b"],
        "purpose": "capacity",
        "expires_at": NOW + 60,
        "revoked": False,
    }


def _capacity_packet():
    return {
        "destination": "node-b",
        "dimension_id": "resource_tension",
        "purpose": "capacity",
        "token": _token(),
    }


def test_local_continues_when_link_down():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False, "isolated": True, "link_trusted": False},
        {"id": "n", "kind": "notify"},
        steady(),
    )
    assert v["allowed"] is True
    assert v["policy"] is not None
    assert v["policy"]["executed"] == "P10"
    assert v["packet_emitted"] is False
    assert v["isolation"] is not None
    assert v["isolation"]["restricted_applied"] is True
    assert v["isolation"]["fm"] == "FM-ISO-LINK"


def test_dead_network_blocks_packet_even_with_token():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False, "isolated": True, "link_trusted": False},
        {"id": "p", "kind": "transmit"},
        steady(),
        packet=_capacity_packet(),
        now=NOW,
    )
    assert v["allowed"] is False
    assert v["blocked_by"] == "ISOLATION"
    assert v["fm"] == "FM-ISO-LINK"
    assert v["packet_emitted"] is False
    assert v["policy"] is not None  # local policy still ran


def test_untrusted_link_blocks_packet():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False, "isolated": False, "link_trusted": False},
        {"id": "p", "kind": "transmit"},
        steady(),
        packet=_capacity_packet(),
        now=NOW,
    )
    assert v["fm"] == "FM-ISO-UNTRUSTED"
    assert v["packet_emitted"] is False


def test_phone_home_blocked_even_on_live_link():
    v = evaluate_cycle(
        _live(),
        {"id": "cb", "kind": "phone_home"},
        steady(),
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-ISO-PHONE-HOME"
    assert v["policy"] is None


def test_fail_open_blocked():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False, "isolated": True},
        {"id": "x", "kind": "cloud_required"},
        steady(),
    )
    assert v["fm"] == "FM-ISO-FAIL-OPEN"
    assert v["policy"] is None


def test_live_trusted_packet_still_emits():
    v = evaluate_cycle(
        _live(),
        {"id": "p", "kind": "transmit"},
        steady(),
        packet=_capacity_packet(),
        now=NOW,
    )
    assert v["packet_emitted"] is True
    assert v["isolation"] is not None
    assert v["isolation"]["reason"] == "ok"


def test_isolation_does_not_skip_dur():
    from core.sovereignty import DEFAULT_STATE

    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "p", "kind": "transmit", "targets_dur": True},
        steady(),
        packet=_capacity_packet(),
        now=NOW,
    )
    assert v["blocked_by"] == "DUR"
    assert v["isolation"] is None
