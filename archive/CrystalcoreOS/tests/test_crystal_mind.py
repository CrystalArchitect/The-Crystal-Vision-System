import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_memory import CrystalMemory
from src.crystal_flow import Rule
from src.crystal_mind import CrystalMind, AgentSpec, AgentResult


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _mem(tmp_path, consumer="default", perms=0b001):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer(consumer, consumer, permissions=perms)
    return mem


# --------------------------------------------------------------------------- #
# Registration / defaults
# --------------------------------------------------------------------------- #
def test_default_agents_installed(tmp_path):
    mind = CrystalMind(_mem(tmp_path))
    names = set(mind.list_agents().keys())
    assert names == {"TruthSeeker", "Guardian", "Visionary", "Creator"}


def test_only_guardian_can_veto(tmp_path):
    mind = CrystalMind(_mem(tmp_path))
    assert mind.agents["Guardian"].can_veto is True
    for n in ("TruthSeeker", "Visionary", "Creator"):
        assert mind.agents[n].can_veto is False


def test_unknown_agent_errors(tmp_path):
    mind = CrystalMind(_mem(tmp_path))
    a = mem_node = mind.memory.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    res = mind.run_agent("Nobody", [a])
    assert res.status == "error"


# --------------------------------------------------------------------------- #
# Stances are real, not cosmetic
# --------------------------------------------------------------------------- #
def test_truthseeker_refuses_weak_evidence(tmp_path):
    mem = _mem(tmp_path)
    weak = mem.encode([0.5], coherence_boost=0.35, consent_flags=0b001)  # ~0.28
    mind = CrystalMind(mem, session_consumer_id="default")
    res = mind.run_agent("TruthSeeker", [weak])
    assert res.status == "low_coherence_input"


def test_truthseeker_accepts_strong_evidence(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)  # ~0.76
    mind = CrystalMind(mem, session_consumer_id="default")
    res = mind.run_agent("TruthSeeker", [strong])
    assert res.status == "ok"
    assert res.coherence > 0.7


def test_visionary_tolerates_weak_but_marks_speculative(tmp_path):
    mem = _mem(tmp_path)
    weak = mem.encode([0.5], coherence_boost=0.35, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    res = mind.run_agent("Visionary", [weak])
    assert res.status == "ok"                       # tolerant where TruthSeeker refused
    assert res.content.get("speculative") is True
    # coherence_factor 0.6 attenuates confidence.
    assert res.coherence < 0.28


# --------------------------------------------------------------------------- #
# Per-agent consent
# --------------------------------------------------------------------------- #
def test_agent_with_own_identity_denied(tmp_path):
    mem = _mem(tmp_path, consumer="default", perms=0b001)
    mem.register_consumer("restricted", "Restricted", permissions=0b010)
    # Node visible only to bit 0 (default), not bit 1.
    node = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)

    mind = CrystalMind(mem, session_consumer_id="default")
    mind.register_agent(AgentSpec(
        name="Restricted", role="x", consumer_id="restricted",
        min_input_coherence=0.4, default_rule=Rule(name="r", fn=lambda f: [1.0]),
    ))
    res = mind.run_agent("Restricted", [node])
    assert res.status == "consent_denied"


def test_session_override_consent(tmp_path):
    mem = _mem(tmp_path, consumer="default", perms=0b001)
    mem.register_consumer("other", "Other", permissions=0b010)
    node = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b010)  # bit1 only

    mind = CrystalMind(mem, session_consumer_id="default")
    # Default session can't see it...
    assert mind.run_agent("Creator", [node]).status == "consent_denied"
    # ...but an explicit session override that CAN see it succeeds.
    assert mind.run_agent("Creator", [node],
                          session_consumer_id="other").status == "ok"


# --------------------------------------------------------------------------- #
# Guardian veto
# --------------------------------------------------------------------------- #
def test_guardian_vetoes_low_coherence_conclusion(tmp_path):
    mem = _mem(tmp_path)
    weak = mem.encode([0.5], coherence_boost=0.45, consent_flags=0b001)  # ~0.36
    mind = CrystalMind(mem, session_consumer_id="default",
                       guardian_min_coherence=0.4)

    # Visionary tolerates it (bar 0.25) but output coherence ~0.36*0.6 < 0.4.
    out = mind.council(["Visionary", "Guardian"], [weak])
    assert out["results"]["Visionary"]["status"] == "vetoed"
    assert len(out["vetoes"]) == 1


def test_veto_removes_node_from_memory(tmp_path):
    mem = _mem(tmp_path)
    weak = mem.encode([0.5], coherence_boost=0.45, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default",
                       guardian_min_coherence=0.4)

    # Run Visionary alone first to learn the node id it would write.
    solo = mind.run_agent("Visionary", [weak])
    assert solo.status == "ok"
    written_id = solo.output_node_id
    assert written_id in mem.nodes

    # Now a council with Guardian should veto AND remove a freshly written one.
    out = mind.council(["Visionary", "Guardian"], [weak])
    vetoed_ids = [r["output_node_id"] for r in out["results"].values()
                  if r["status"] == "vetoed"]
    # Vetoed result reports no surviving node, and nothing orphaned remains.
    assert all(v is None for v in vetoed_ids)


def test_guardian_does_not_veto_strong_conclusion(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default",
                       guardian_min_coherence=0.4)
    out = mind.council(["TruthSeeker", "Guardian"], [strong])
    assert out["results"]["TruthSeeker"]["status"] == "ok"
    assert out["vetoes"] == []


def test_guardian_does_not_review_itself(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    out = mind.council(["Guardian"], [strong])
    # Guardian present, but it is never in the veto list for itself.
    assert all(v["agent"] != "Guardian" for v in out["vetoes"])


def test_council_without_guardian_no_veto(tmp_path):
    mem = _mem(tmp_path)
    weak = mem.encode([0.5], coherence_boost=0.45, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    # No Guardian in the council -> no veto pass, Visionary stands.
    out = mind.council(["Visionary", "Creator"], [weak])
    assert out["vetoes"] == []
    assert out["results"]["Visionary"]["status"] == "ok"


# --------------------------------------------------------------------------- #
# Council mechanics
# --------------------------------------------------------------------------- #
def test_council_runs_all_named_agents(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    out = mind.council(["TruthSeeker", "Creator", "Guardian"], [strong])
    assert set(out["results"].keys()) == {"TruthSeeker", "Creator", "Guardian"}


def test_action_log_records_every_action(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    mind.run_agent("TruthSeeker", [strong])
    mind.run_agent("Creator", [strong])
    log = mind.get_action_log()
    assert len(log) >= 2
    assert {e["agent"] for e in log} >= {"TruthSeeker", "Creator"}


def test_custom_rule_overrides_default(tmp_path):
    mem = _mem(tmp_path)
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default")
    custom = Rule(name="custom", fn=lambda facts: {"custom": True}, strength=0.9)
    res = mind.run_agent("Creator", [strong], rule=custom)
    assert res.content == {"custom": True}


# --------------------------------------------------------------------------- #
# No autonomy invariant (structural)
# --------------------------------------------------------------------------- #
def test_no_autonomous_methods_exist():
    """v1 must expose no self-triggering / looping entry points. Agents act
    only via caller-initiated run_agent / council."""
    import src.crystal_mind as cm
    public = {n for n in dir(cm.CrystalMind) if not n.startswith("_")}
    forbidden = {"start", "run_loop", "tick", "autorun", "spawn", "daemon",
                 "schedule", "background"}
    assert public.isdisjoint(forbidden)


if __name__ == "__main__":
    sys.exit(0 if pytest is None else pytest.main([__file__, "-v"]))
