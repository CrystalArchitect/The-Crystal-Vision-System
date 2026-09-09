"""v0.1.2 — no token, no packet."""

from core.consent import ConsentToken, evaluate_consent
from core.cycle import evaluate_cycle
from core.local_state import LocalAffectState, steady
from core.sovereignty import DEFAULT_STATE

NOW = 1_000


def _token(**overrides) -> ConsentToken:
    t: ConsentToken = {
        "token_id": "tok-1",
        "operator_id": "op-1",
        "allowed_dimensions": ["resource_tension"],
        "allowed_destinations": ["node-b"],
        "purpose": "capacity",
        "expires_at": NOW + 60,
        "revoked": False,
    }
    t.update(overrides)  # type: ignore[typeddict-item]
    return t


def _packet(token=None, **extra):
    p = {
        "destination": "node-b",
        "dimension_id": "resource_tension",
        "purpose": "capacity",
    }
    p.update(extra)
    if token is not None:
        p["token"] = token
    return p


def test_absence_is_denial():
    v = evaluate_consent(None, now=NOW)
    assert v["allowed"] is False
    assert v["reason"] == "absent"


def test_matching_token_allows():
    v = evaluate_consent(_packet(token=_token()), now=NOW)
    assert v["allowed"] is True


def test_expired_token_denied():
    v = evaluate_consent(_packet(token=_token(expires_at=NOW - 1)), now=NOW)
    assert v["reason"] == "expired"


def test_revoked_token_denied():
    v = evaluate_consent(_packet(token=_token(revoked=True)), now=NOW)
    assert v["reason"] == "revoked"


def test_wrong_dimension_denied():
    v = evaluate_consent(
        _packet(token=_token(), dimension_id="relational_stake"),
        now=NOW,
    )
    assert v["reason"] == "dimension"


def test_wrong_destination_denied():
    v = evaluate_consent(_packet(token=_token(), destination="node-z"), now=NOW)
    assert v["reason"] == "destination"


def test_purpose_mismatch_denied():
    v = evaluate_consent(_packet(token=_token(), purpose="modelling"), now=NOW)
    assert v["reason"] == "purpose"


def test_cycle_notify_needs_no_token():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "n", "kind": "notify"},
        steady(),
    )
    assert v["allowed"] is True
    assert v["packet_emitted"] is False
    assert v["consent"] is None


def test_cycle_transmit_without_token_denied():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "p", "kind": "transmit"},
        steady(),
        packet=_packet(),
        now=NOW,
    )
    assert v["allowed"] is False
    assert v["blocked_by"] == "CONSENT"
    assert v["packet_emitted"] is False
    assert v["policy"] is not None  # local policy still ran


def test_cycle_transmit_with_token_emits():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "p", "kind": "transmit"},
        steady(),
        packet=_packet(token=_token()),
        now=NOW,
    )
    assert v["packet_emitted"] is True


def test_token_cannot_outrank_p1():
    affect = LocalAffectState({"boundary_stress": 0.8, "meta_state_clarity": 0.8})
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "p", "kind": "transmit"},
        affect,
        packet=_packet(token=_token()),
        now=NOW,
    )
    assert v["packet_emitted"] is False
    assert v["consent"] is not None
    assert v["consent"]["reason"] == "p1"


def test_restricted_blocks_rich_even_with_token():
    rel = _token(allowed_dimensions=["relational_stake"], purpose="sync")
    v = evaluate_consent(
        _packet(token=rel, dimension_id="relational_stake", purpose="sync"),
        now=NOW,
        restricted=True,
    )
    assert v["reason"] == "restricted"


def test_restricted_allows_capacity_with_token():
    v = evaluate_consent(_packet(token=_token()), now=NOW, restricted=True)
    assert v["allowed"] is True


def test_dur_still_outranks_consent():
    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "p", "kind": "transmit", "targets_dur": True},
        steady(),
        packet=_packet(token=_token()),
        now=NOW,
    )
    assert v["blocked_by"] == "DUR"
    assert v["consent"] is None
