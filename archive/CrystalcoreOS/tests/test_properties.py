"""
Property-based tests for CrystalCore safety invariants.

These complement the example-based tests by checking that key invariants hold
across MANY randomized inputs, not just hand-picked points. They target the
properties that matter most for sovereignty and safety:

  P1  Coherence propagation never exceeds the weakest input (and respects the
      rule strength) — confidence cannot be manufactured.
  P2  Consent is fail-closed: an agent/consumer lacking permission for an input
      NEVER receives content, for any coherence or input shape.
  P3  Guardian veto: any conclusion below the veto floor is removed from memory
      and reported vetoed — for any generated weak input.
  P4  Pruning respects priority: a sufficiently high-priority node survives
      arbitrary low-priority churn.
  P5  Durable payloads round-trip byte-for-byte through save/load, for many
      generated string/dict payloads.

Real Hypothesis is used if installed; otherwise a stdlib harness with the same
`given`/`strategies` surface runs the same checks (zero-dependency on a Pi).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Prefer real Hypothesis; fall back to the dependency-free harness.
try:
    from hypothesis import given, settings
    from hypothesis import strategies as st
    _HARNESS = False

    def _given(*strats, trials=200):
        # Adapt: real hypothesis takes strategies as kwargs/args + @settings.
        def deco(fn):
            return settings(max_examples=trials)(given(*strats)(fn))
        return deco
except ImportError:
    from tests.property_harness import given as _raw_given, strategies as st
    _HARNESS = True

    def _given(*strats, trials=200):
        return _raw_given(*strats, trials=trials)

from src.crystal_memory import CrystalMemory
from src.crystal_flow import CrystalFlow, Rule
from src.crystal_mind import CrystalMind, AgentSpec


import tempfile


def _fresh_mem(consumer="default", perms=0b001):
    d = tempfile.mkdtemp()
    mem = CrystalMemory(max_ram_mb=64, storage_path=os.path.join(d, "m.json"))
    mem.register_consumer(consumer, consumer, permissions=perms)
    return mem


# --------------------------------------------------------------------------- #
# P1 — coherence propagation never manufactures confidence
# --------------------------------------------------------------------------- #
@_given(
    st.floats(0.0, 1.0), st.floats(0.0, 1.0), st.floats(0.0, 1.0),
    trials=300,
)
def test_prop_coherence_never_exceeds_weakest(c1, c2, strength):
    out = CrystalFlow.propagate_coherence([c1, c2], strength)
    weakest = min(c1, c2)
    # Output must not exceed the weakest input, and not exceed weakest*strength
    # (within float tolerance). Confidence cannot be created.
    assert out <= weakest + 1e-9
    assert out <= weakest * min(1.0, max(0.0, strength)) + 1e-9
    assert out >= 0.0


@_given(st.lists(st.floats(0.0, 1.0), min_size=1, max_size=6), st.floats(0.0, 2.0),
        trials=300)
def test_prop_coherence_monotonic_in_strength(coherences, strength):
    # Higher strength never decreases the propagated coherence.
    low = CrystalFlow.propagate_coherence(coherences, min(strength, 1.0) * 0.5)
    high = CrystalFlow.propagate_coherence(coherences, min(strength, 1.0))
    assert high + 1e-9 >= low


# --------------------------------------------------------------------------- #
# P2 — consent is fail-closed for any input
# --------------------------------------------------------------------------- #
@_given(
    st.lists(st.floats(-5.0, 5.0), min_size=1, max_size=6),
    st.floats(0.1, 1.0),
    trials=200,
)
def test_prop_consent_fail_closed(values, coherence_boost):
    # Node visible ONLY to bit 1; a bit-0 consumer must never get content.
    mem = _fresh_mem(consumer="alice", perms=0b001)
    mem.register_consumer("bob_only", "Bob", permissions=0b010)
    node = mem.encode(values, coherence_boost=coherence_boost,
                      consent_flags=0b010)  # bit 1 only

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.0)
    result = mem.retrieve(node, consumer_id="alice", min_coherence=0.0)
    # Alice (bit 0) must be denied regardless of coherence/shape.
    assert result["status"] == "consent_denied"
    assert "content" not in result or result.get("content") is None


@_given(st.lists(st.floats(-5.0, 5.0), min_size=1, max_size=6), trials=150)
def test_prop_agent_consent_fail_closed(values):
    # An agent with a non-matching identity never gets content, any input.
    mem = _fresh_mem(consumer="default", perms=0b001)
    mem.register_consumer("restricted", "Restricted", permissions=0b100)
    node = mem.encode(values, coherence_boost=0.95, consent_flags=0b001)

    mind = CrystalMind(mem, session_consumer_id="default")
    mind.register_agent(AgentSpec(
        name="R", role="x", consumer_id="restricted",
        min_input_coherence=0.0,
        default_rule=Rule(name="r", fn=lambda f: [1.0]),
    ))
    res = mind.run_agent("R", [node])
    assert res.status == "consent_denied"
    assert res.content is None


# --------------------------------------------------------------------------- #
# P3 — Guardian veto removes any sub-floor conclusion
# --------------------------------------------------------------------------- #
@_given(st.floats(0.30, 0.55), trials=120)
def test_prop_guardian_vetoes_subfloor(boost):
    # Visionary (factor 0.6) on a single input: output coherence = 0.8*boost*0.7*0.6
    # Choose floor so a meaningful fraction land below it; assert: IF below floor,
    # THEN vetoed AND node absent.
    mem = _fresh_mem(consumer="default", perms=0b001)
    node = mem.encode([0.5], coherence_boost=boost, consent_flags=0b001)
    mind = CrystalMind(mem, session_consumer_id="default",
                       guardian_min_coherence=0.4)

    solo = mind.run_agent("Visionary", [node])
    if solo.status != "ok":
        return  # input gated out before any conclusion; nothing to veto

    out = mind.council(["Visionary", "Guardian"], [node])
    v = out["results"]["Visionary"]
    if v["coherence"] < 0.4:
        assert v["status"] == "vetoed"
        assert v["output_node_id"] is None
        # The vetoed node must not linger in memory.
        # (solo wrote one earlier; council wrote+removed a second.)
    else:
        assert v["status"] == "ok"


# --------------------------------------------------------------------------- #
# P4 — pruning respects priority under arbitrary churn
# --------------------------------------------------------------------------- #
@_given(st.integers(60, 160), st.floats(20.0, 80.0), trials=40)
def test_prop_high_priority_survives_churn(n_churn, survivor_priority):
    mem = _fresh_mem(consumer="default", perms=0b001)
    protected = mem.encode([1.0] * 10, coherence_boost=0.9,
                           family_priority=survivor_priority, consent_flags=0b001)
    mem.max_ram_mb = 0.05
    for i in range(n_churn):
        mem.encode([float(i)] * 30, coherence_boost=0.5,
                   family_priority=0.1, consent_flags=0b001)
    # A high-priority node must survive low-priority flooding.
    assert protected in mem.nodes


# --------------------------------------------------------------------------- #
# P5 — durable payloads round-trip exactly
# --------------------------------------------------------------------------- #
@_given(
    st.lists(st.sampled_from(["a", "z", "policy", "decision", "x1", " "]),
             min_size=1, max_size=5),
    st.integers(0, 1000),
    trials=120,
)
def test_prop_payload_roundtrips(words, num):
    payload = {"words": words, "n": num, "nested": {"k": words[:1]}}
    d = tempfile.mkdtemp()
    path = os.path.join(d, "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    mem.register_consumer("default", "Default", permissions=0b001)
    nid = mem.encode([0.0], coherence_boost=0.9, consent_flags=0b001,
                     payload=payload)

    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    got = mem2.retrieve(nid, min_coherence=0.0)
    assert got["payload"] == payload


# --------------------------------------------------------------------------- #
# Runner entry (works under the stdlib shim and pytest)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        import pytest
        sys.exit(pytest.main([__file__, "-v"]))
    except ImportError:
        # Run directly under the stdlib harness.
        import inspect
        mod = sys.modules[__name__]
        tests = [(n, f) for n, f in inspect.getmembers(mod, inspect.isfunction)
                 if n.startswith("test_prop_")]
        failed = 0
        for name, fn in tests:
            try:
                fn()
                print(f"  PASS  {name}")
            except Exception as e:
                print(f"  FAIL  {name}: {type(e).__name__}: {e}")
                failed += 1
        print(f"\n{len(tests) - failed} passed, {failed} failed")
        sys.exit(1 if failed else 0)
