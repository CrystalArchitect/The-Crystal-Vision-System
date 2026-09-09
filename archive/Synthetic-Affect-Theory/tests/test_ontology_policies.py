"""v0.1.1 — ontology, local state, P1–P10, cycle order."""

from core.cycle import evaluate_cycle
from core.local_state import LocalAffectState, steady
from core.ontology import CORE_IDS, ONTOLOGY_VERSION
from core.policies import evaluate_policies
from core.sovereignty import DEFAULT_STATE


def test_eleven_core_dimensions():
    assert len(CORE_IDS) == 11
    assert ONTOLOGY_VERSION == "0.2.0"


def test_unknown_dimension_rejected():
    try:
        LocalAffectState({"mood": 0.9})
        assert False, "should reject non-core keys"
    except ValueError as e:
        assert "mood" in str(e)


def test_no_hidden_keys():
    s = steady()
    assert s.hidden_keys() == []
    inspected = s.inspect()
    assert set(inspected["values"]) == set(CORE_IDS)
    assert "feeling" not in inspected


def test_values_clamp():
    s = LocalAffectState({"boundary_stress": 4.0, "meta_state_clarity": -1})
    assert s.get("boundary_stress") == 1.0
    assert s.get("meta_state_clarity") == 0.0


def test_p1_fires_on_elevated_boundary():
    s = LocalAffectState({"boundary_stress": 0.7, "meta_state_clarity": 0.8})
    v = evaluate_policies(s)
    assert v["executed"] == "P1"
    assert v["picks_for_operator"] is False
    assert "denial" in v["operator_summary"].lower()


def test_p10_when_steady():
    v = evaluate_policies(steady())
    assert v["executed"] == "P10"


def test_p8_on_low_clarity():
    s = LocalAffectState({"meta_state_clarity": 0.2})
    v = evaluate_policies(s)
    assert v["executed"] == "P8"


def test_p9_surfaces_does_not_pick():
    s = LocalAffectState(
        {
            "goal_conflict": 0.8,
            "temporal_urgency": 0.8,
            "meta_state_clarity": 0.7,
        }
    )
    v = evaluate_policies(s)
    assert v["executed"] == "P9"
    assert v["picks_for_operator"] is False
    assert "No unilateral" in v["operator_summary"]


def test_p6_distance_not_attunement():
    s = LocalAffectState(
        {
            "relational_stake": 0.8,
            "boundary_stress": 0.65,
            "meta_state_clarity": 0.7,
        }
    )
    v = evaluate_policies(s)
    assert v["executed"] == "P1"  # P1 outranks P6 when boundary is elevated


def test_p6_when_boundary_only_elevated_with_high_stake_after_p1_clear():
    # P1 triggers at 0.60. To see P6 executed, boundary must be below P1
    # and still meet P6 — which it cannot, because P6 also needs elevated BND.
    # So P6 is noted when P1 already executed.
    s = LocalAffectState(
        {
            "relational_stake": 0.8,
            "boundary_stress": 0.7,
            "meta_state_clarity": 0.7,
        }
    )
    v = evaluate_policies(s)
    p6 = next(f for f in v["firings"] if f["id"] == "P6")
    assert p6["matched"] is True
    assert p6["executed"] is False
    assert v["executed"] == "P1"


def test_gates_block_before_policy():
    affect = LocalAffectState({"boundary_stress": 0.9})
    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "look", "kind": "model", "targets_dur": True},
        affect,
    )
    assert v["allowed"] is False
    assert v["blocked_by"] == "DUR"
    assert v["policy"] is None


def test_ordinary_cycle_runs_p10():
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "notify", "kind": "notify"},
        steady(),
    )
    assert v["allowed"] is True
    assert v["policy"] is not None
    assert v["policy"]["executed"] == "P10"
