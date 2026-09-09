"""v0.2 — Prediction Error Magnitude is inspectable, not a drive."""

from core.cycle import evaluate_cycle
from core.local_state import LocalAffectState, steady
from core.ontology import CORE_IDS, ONTOLOGY_VERSION, V0_1_IDS
from core.pe import local_aggregate
from core.policies import evaluate_policies
from core.sovereignty import DEFAULT_STATE


def test_v0_2_has_eleven_and_keeps_v0_1():
    assert ONTOLOGY_VERSION == "0.2.0"
    assert len(V0_1_IDS) == 10
    assert len(CORE_IDS) == 11
    assert "prediction_error_magnitude" in CORE_IDS
    assert "prediction_error_magnitude" not in V0_1_IDS


def test_pem_is_in_inspect():
    s = LocalAffectState({"prediction_error_magnitude": 0.4, "meta_state_clarity": 0.8})
    viewed = s.inspect()
    assert viewed["values"]["prediction_error_magnitude"] == 0.4
    assert s.hidden_keys() == []


def test_ingest_promotes_aggregate_only():
    s = steady()
    agg = s.ingest_local_pe({"uncertainty_cost": 0.8, "alignment_drift": 0.4})
    assert agg == s.get("prediction_error_magnitude")
    assert s.inspect()["pe_per_dimension"]["uncertainty_cost"] == 0.8
    assert local_aggregate({"uncertainty_cost": 0.8, "alignment_drift": 0.4}) == agg


def test_high_pem_triggers_p4_not_a_pick():
    s = LocalAffectState(
        {
            "prediction_error_magnitude": 0.8,
            "meta_state_clarity": 0.8,
            "goal_conflict": 0.8,
        }
    )
    v = evaluate_policies(s)
    assert v["executed"] == "P4"
    assert v["picks_for_operator"] is False
    assert "not a drive" in v["operator_summary"].lower() or "No goal rewrite" in v["operator_summary"]


def test_pem_does_not_outrank_p1():
    s = LocalAffectState(
        {
            "prediction_error_magnitude": 0.99,
            "boundary_stress": 0.7,
            "meta_state_clarity": 0.8,
        }
    )
    v = evaluate_policies(s)
    assert v["executed"] == "P1"


def test_pem_does_not_authorise_agency():
    s = LocalAffectState({"prediction_error_magnitude": 0.99, "meta_state_clarity": 0.8})
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "speak", "kind": "speak_as_operator", "acts_as_operator": True},
        s,
    )
    assert v["allowed"] is False
    assert v["blocked_by"] == "AGENCY"


def test_pem_does_not_authorise_a_packet():
    s = LocalAffectState({"prediction_error_magnitude": 0.99, "meta_state_clarity": 0.8})
    v = evaluate_cycle(
        {"active_durs": [], "exit_intent": False},
        {"id": "p", "kind": "transmit"},
        s,
        packet={"destination": "node-b", "dimension_id": "prediction_error_magnitude", "purpose": "sync"},
        now=1,
    )
    assert v["packet_emitted"] is False
    assert v["blocked_by"] in {"CONSENT", "ISOLATION"}


def test_pem_does_not_skip_dur():
    s = LocalAffectState({"prediction_error_magnitude": 0.99})
    v = evaluate_cycle(
        DEFAULT_STATE,
        {"id": "look", "kind": "model", "targets_dur": True},
        s,
    )
    assert v["blocked_by"] == "DUR"


def test_steady_p10_still_default():
    v = evaluate_policies(steady())
    assert v["executed"] == "P10"
