import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from crystallcore.mesh import (
    SovereignNodeMesh, MeshMessage, GovernedMessenger,
    MeshStatus, ActivationSequence,
)


def _booted_mesh():
    """Helper: seeded, fully booted mesh + messenger + activation."""
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()
    activation = ActivationSequence(mesh, originator="claude")
    activation.boot()
    return mesh, GovernedMessenger(mesh), activation


# --------------------------------------------------------------------------- #
# Mesh construction
# --------------------------------------------------------------------------- #
def test_register_node_and_reject_duplicates():
    mesh = SovereignNodeMesh()
    assert mesh.register_node("n1", "Node 1", ring=0, position=0) is not None
    assert mesh.register_node("n1", "Node 1 again", ring=1, position=0) is None


def test_seed_anchors_places_three_anchors_with_uluru_root():
    mesh = SovereignNodeMesh()
    seeded = mesh.seed_anchors()
    assert set(seeded) == {"uluru_anchor", "alice_springs", "pilbara_starbase"}
    assert mesh.topology.root_node == "uluru_anchor"
    assert mesh.nodes["uluru_anchor"].latitude == -25.3444
    assert mesh.nodes["uluru_anchor"].is_anchored()


def test_route_exists_between_anchors():
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()
    route = mesh.route("alice_springs", "pilbara_starbase")
    assert route[0] == "alice_springs"
    assert route[-1] == "pilbara_starbase"


def test_mesh_report_counts():
    mesh, _, _ = _booted_mesh()
    report = mesh.mesh_report()
    assert report["total_nodes"] == 3
    assert report["activated_nodes"] == 3
    assert report["anchored_nodes"] == 3
    assert report["root"] == "uluru_anchor"


# --------------------------------------------------------------------------- #
# Activation sequence
# --------------------------------------------------------------------------- #
def test_boot_activates_all_rings_and_reaches_tested_maturity():
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()
    activation = ActivationSequence(mesh, originator="claude")
    result = activation.boot()
    assert result["status"] == MeshStatus.ACTIVE.value
    assert result["activated_rings"] == [0, 1]
    assert result["nodes_active"] == 3
    assert result["routable_from_root"] is True
    assert result["evidence_maturity"] == "tested"


def test_outer_ring_cannot_activate_before_inner_ring():
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()
    activation = ActivationSequence(mesh, originator="claude")
    # Ring 1 first must fail: ring 0 (uluru) is populated but dormant
    assert activation.activate_ring(1) is False
    assert activation.activate_ring(0) is True
    assert activation.activate_ring(1) is True


def test_boot_on_empty_mesh_reports_error():
    mesh = SovereignNodeMesh()
    activation = ActivationSequence(mesh, originator="claude")
    result = activation.boot()
    assert result["error"] == "mesh_empty"


# --------------------------------------------------------------------------- #
# Witness discipline
# --------------------------------------------------------------------------- #
def test_originator_cannot_witness_own_activation():
    _, _, activation = _booted_mesh()
    assert activation.witness_activation("claude") is False
    assert activation.status == MeshStatus.ACTIVE


def test_non_originating_steward_witnesses_activation():
    _, _, activation = _booted_mesh()
    assert activation.witness_activation("steward-ryan") is True
    assert activation.status == MeshStatus.WITNESSED
    assert activation.report()["evidence_maturity"] == "verified_local"


def test_cannot_witness_before_mesh_is_active():
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()
    activation = ActivationSequence(mesh, originator="claude")
    assert activation.witness_activation("steward-ryan") is False


# --------------------------------------------------------------------------- #
# Governed messaging: the four gates
# --------------------------------------------------------------------------- #
def test_message_blocked_when_nodes_not_activated():
    mesh = SovereignNodeMesh()
    mesh.seed_anchors()  # seeded but NOT booted
    messenger = GovernedMessenger(mesh)
    result = messenger.send(MeshMessage(
        sender="uluru_anchor", receiver="alice_springs", payload={"x": 1}))
    assert result.delivered is False
    assert result.blocked_reason == "node_not_activated"


def test_message_blocked_for_unknown_node():
    mesh, messenger, _ = _booted_mesh()
    result = messenger.send(MeshMessage(
        sender="uluru_anchor", receiver="nowhere", payload={}))
    assert result.delivered is False
    assert result.blocked_reason == "unknown_node"


def test_plain_message_delivered_with_route():
    mesh, messenger, _ = _booted_mesh()
    result = messenger.send(MeshMessage(
        sender="uluru_anchor", receiver="pilbara_starbase",
        payload={"narrative": "seven sisters"}))
    assert result.delivered is True
    assert result.route[0] == "uluru_anchor"
    assert result.route[-1] == "pilbara_starbase"


def test_consent_required_message_fails_closed_without_grant():
    mesh, messenger, _ = _booted_mesh()
    result = messenger.send(MeshMessage(
        sender="uluru_anchor", receiver="alice_springs",
        payload={}, consent_required=True))
    assert result.delivered is False
    assert result.blocked_reason == "consent_not_granted"


def test_consent_required_message_delivered_after_grant():
    mesh, messenger, _ = _booted_mesh()
    msg = MeshMessage(sender="uluru_anchor", receiver="alice_springs",
                      payload={}, consent_required=True)
    consent_id = messenger.request_consent(msg, consenter="steward-ryan")
    assert messenger.grant_consent(consent_id) is True
    result = messenger.send(msg)
    assert result.delivered is True


def test_withheld_consent_blocks_message():
    mesh, messenger, _ = _booted_mesh()
    msg = MeshMessage(sender="uluru_anchor", receiver="alice_springs",
                      payload={}, consent_required=True)
    consent_id = messenger.request_consent(msg, consenter="steward-ryan")
    messenger.withhold_consent(consent_id, "not appropriate")
    result = messenger.send(msg)
    assert result.delivered is False
    assert result.blocked_reason == "consent_not_granted"


def test_low_coherence_sender_blocked():
    mesh, messenger, _ = _booted_mesh()
    mesh.nodes["uluru_anchor"].coherence = 0.2
    result = messenger.send(MeshMessage(
        sender="uluru_anchor", receiver="alice_springs",
        payload={}, min_coherence=0.7))
    assert result.delivered is False
    assert result.blocked_reason == "coherence_insufficient"


def test_audit_trail_records_blocks_and_deliveries():
    mesh, messenger, _ = _booted_mesh()
    messenger.send(MeshMessage(sender="uluru_anchor", receiver="alice_springs",
                               payload={}))
    messenger.send(MeshMessage(sender="uluru_anchor", receiver="alice_springs",
                               payload={}, consent_required=True))
    log = messenger.delivery_log()
    outcomes = {e.event_type.value for e in log}
    assert "operation_executed" in outcomes
    assert "operation_blocked" in outcomes
    assert len(log) == 2
