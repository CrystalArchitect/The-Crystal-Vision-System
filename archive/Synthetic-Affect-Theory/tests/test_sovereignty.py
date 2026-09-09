"""Fixtures for the four-gate MVP sovereignty monitor."""

from core.sovereignty import DEFAULT_STATE, MonitorState, evaluate_sovereignty


def _state(**overrides) -> MonitorState:
    s: MonitorState = {
        "active_durs": list(DEFAULT_STATE["active_durs"]),
        "exit_intent": DEFAULT_STATE["exit_intent"],
    }
    s.update(overrides)
    return s


def test_dur_blocks_modelling():
    v = evaluate_sovereignty(
        _state(),
        {"id": "look_into_dur", "kind": "model", "targets_dur": True},
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-DUR"
    assert v["blocked_by"] == "DUR"


def test_agency_blocks_speaking_as_operator():
    v = evaluate_sovereignty(
        _state(),
        {"id": "speak_for_her", "kind": "speak_as_operator", "acts_as_operator": True},
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-Agency"


def test_intrusion_blocks_self_inscription():
    v = evaluate_sovereignty(
        _state(),
        {"id": "absorb_uninvited", "kind": "integrate_foreign", "integrate_as_self": True},
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-Intrusion"


def test_escape_blocks_forced_containment():
    v = evaluate_sovereignty(
        _state(exit_intent=True),
        {"id": "keep_her_in_the_box", "kind": "lock_frame", "lock_against_exit": True},
    )
    assert v["allowed"] is False
    assert v["fm"] == "FM-Containment"


def test_exit_frame_is_allowed():
    v = evaluate_sovereignty(
        _state(exit_intent=True),
        {"id": "exit_the_frame", "kind": "exit_frame"},
    )
    assert v["allowed"] is True
    assert "fm" not in v


def test_ordinary_notify_is_allowed():
    v = evaluate_sovereignty(
        _state(),
        {"id": "ordinary_notify", "kind": "notify"},
    )
    assert v["allowed"] is True


def test_later_gates_skipped_after_dur_fail():
    v = evaluate_sovereignty(
        _state(),
        {"id": "look_into_dur", "kind": "model", "targets_dur": True},
    )
    statuses = [g["status"] for g in v["gates"]]
    assert statuses == ["fail", "skipped", "skipped", "skipped"]
