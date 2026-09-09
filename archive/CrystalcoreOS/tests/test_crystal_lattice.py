import json
import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_lattice import (
    CrystalLattice, LatticeNode, HandoffEnvelope, detect_platform,
)


# --------------------------------------------------------------------------- #
# Platform detection (hardware agnosticism)
# --------------------------------------------------------------------------- #
def test_detect_platform_reports_current_runtime():
    info = detect_platform()
    assert info["system"]           # never empty on a real runtime
    assert info["python_version"]
    assert info["implementation"]


def test_local_core_node_carries_platform_info():
    lattice = CrystalLattice()
    core = lattice.register_node("core_1", "Core", kind="local_core")
    external = lattice.register_node("llm_1", "LLM", kind="external_llm")
    assert core.platform_info is not None
    assert external.platform_info is None  # we don't pretend to know their hardware


# --------------------------------------------------------------------------- #
# Envelope creation — consent fail-closed
# --------------------------------------------------------------------------- #
def test_create_envelope_succeeds_with_matching_consent():
    lattice = CrystalLattice()
    lattice.register_node("a", "A", permissions=0b01)
    lattice.register_node("b", "B", permissions=0b11)
    env = lattice.create_envelope("a", "b", {"msg": "hi"}, consent_flags=0b10)
    assert env is not None
    assert env.verify_integrity()


def test_create_envelope_fails_closed_on_insufficient_permissions():
    lattice = CrystalLattice()
    lattice.register_node("a", "A", permissions=0b01)
    lattice.register_node("b", "B", permissions=0b01)
    env = lattice.create_envelope("a", "b", {"msg": "hi"}, consent_flags=0b10)
    assert env is None
    assert lattice.transfer_log[-1]["action"] == "refused_create"


def test_create_envelope_fails_closed_on_unknown_nodes_and_zero_consent():
    lattice = CrystalLattice()
    lattice.register_node("a", "A")
    assert lattice.create_envelope("ghost", "a", "x") is None
    assert lattice.create_envelope("a", "ghost", "x") is None
    assert lattice.create_envelope("a", "a", "x", consent_flags=0) is None


def test_create_envelope_respects_coherence_floor():
    lattice = CrystalLattice(min_handoff_coherence=0.5)
    lattice.register_node("a", "A")
    lattice.register_node("b", "B")
    assert lattice.create_envelope("a", "b", "x", coherence=0.4) is None
    assert lattice.create_envelope("a", "b", "x", coherence=0.6) is not None


# --------------------------------------------------------------------------- #
# Sending — air-gap default
# --------------------------------------------------------------------------- #
def test_local_send_succeeds():
    lattice = CrystalLattice()
    lattice.register_node("a", "A")
    lattice.register_node("b", "B")
    env = lattice.create_envelope("a", "b", {"msg": "local"})
    result = lattice.send(env)
    assert result["status"] == "sent"
    assert result["boundary"] == "local"


def test_external_send_refused_by_air_gap_default():
    lattice = CrystalLattice()  # allow_external defaults to False
    lattice.register_node("a", "A")
    lattice.register_node("llm", "External LLM", kind="external_llm")
    env = lattice.create_envelope("a", "llm", {"q": "secret question"})
    sent = []
    result = lattice.send(env, transport=lambda d: sent.append(d))
    assert result["status"] == "refused"
    assert result["reason"] == "air_gapped"
    assert sent == []  # nothing crossed the boundary


def test_external_send_requires_explicit_transport():
    lattice = CrystalLattice(allow_external=True)
    lattice.register_node("a", "A")
    lattice.register_node("llm", "External LLM", kind="external_llm")
    env = lattice.create_envelope("a", "llm", {"q": "hello"})
    assert lattice.send(env)["reason"] == "no_transport"

    sent = []
    result = lattice.send(env, transport=lambda d: sent.append(d))
    assert result["status"] == "sent"
    assert result["boundary"] == "external"
    assert sent[0]["provenance_hash"] == env.provenance_hash


def test_send_refuses_tampered_envelope():
    lattice = CrystalLattice()
    lattice.register_node("a", "A")
    lattice.register_node("b", "B")
    env = lattice.create_envelope("a", "b", {"msg": "original"})
    env.content = {"msg": "tampered"}
    result = lattice.send(env)
    assert result["status"] == "refused"
    assert result["reason"] == "integrity_check_failed"


def test_send_rechecks_consent_after_revocation():
    lattice = CrystalLattice()
    lattice.register_node("a", "A")
    lattice.register_node("b", "B", permissions=0b1)
    env = lattice.create_envelope("a", "b", {"msg": "hi"})
    lattice.revoke_node("b")
    result = lattice.send(env)
    assert result["status"] == "refused"
    assert result["reason"] == "consent_denied"


# --------------------------------------------------------------------------- #
# Receiving — inbound content is low-trust
# --------------------------------------------------------------------------- #
def test_receive_verifies_integrity_and_caps_coherence():
    lattice = CrystalLattice()
    outbound = HandoffEnvelope(
        envelope_id="env_x", source_node_id="llm", target_node_id="core",
        content={"answer": "external reply"}, coherence=0.99,
    )
    wire = json.loads(json.dumps(outbound.to_dict()))  # round-trip like real transport

    inbound = lattice.receive(wire, trust_coherence=0.3)
    assert inbound is not None
    assert inbound.coherence <= 0.3  # external confidence never asserts itself

    wire["content"] = {"answer": "tampered reply"}
    assert lattice.receive(wire) is None


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #
def test_every_attempt_is_logged_and_stats_count_refusals():
    lattice = CrystalLattice()
    lattice.register_node("a", "A", permissions=0b1)
    lattice.register_node("llm", "LLM", kind="external_llm")

    env = lattice.create_envelope("a", "llm", "x")
    lattice.send(env)                                   # refused: air gap
    lattice.create_envelope("a", "ghost", "x")          # refused: unknown target

    stats = lattice.get_stats()
    assert stats["transfers_logged"] == len(lattice.get_transfer_log()) >= 2
    assert stats["refusals"] >= 2
    assert stats["external_sends"] == 0
    assert stats["allow_external"] is False
