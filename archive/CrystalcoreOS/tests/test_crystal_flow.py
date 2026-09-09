import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_memory import CrystalMemory
from src.crystal_flow import (
    Value, sgd_step, zero_grad,
    CrystalFlow, Rule, Fact, ConsentViolation,
)


# --------------------------------------------------------------------------- #
# Autograd core
# --------------------------------------------------------------------------- #
def test_autograd_add_mul_pow():
    x = Value(2.0)
    y = Value(3.0)
    z = x * y + x ** 2          # dz/dx = y + 2x = 7 ; dz/dy = x = 2
    z.backward()
    assert z.data == 10.0
    assert x.grad == 7.0
    assert y.grad == 2.0


def test_autograd_division():
    x = Value(2.0)
    y = Value(3.0)
    f = x / y                   # df/dx = 1/3 ; df/dy = -x/y^2 = -2/9
    f.backward()
    assert abs(f.data - (2 / 3)) < 1e-9
    assert abs(x.grad - (1 / 3)) < 1e-9
    assert abs(y.grad - (-2 / 9)) < 1e-9


def test_autograd_relu():
    pos = Value(3.0).relu()
    pos.backward()
    assert pos.data == 3.0

    neg_input = Value(-5.0)
    neg = neg_input.relu()
    neg.backward()
    assert neg.data == 0.0
    assert neg_input.grad == 0.0   # gradient blocked below zero


def test_autograd_tanh_bounded():
    out = Value(0.5).tanh()
    out.backward()
    assert -1.0 < out.data < 1.0


def test_sgd_reduces_loss():
    # Minimise (x - 4)^2 ; gradient descent should move x toward 4.
    x = Value(0.0)
    for _ in range(200):
        zero_grad([x])
        loss = (x - 4.0) ** 2
        loss.backward()
        sgd_step([x], lr=0.1)
    assert abs(x.data - 4.0) < 0.01


# --------------------------------------------------------------------------- #
# Coherence propagation
# --------------------------------------------------------------------------- #
def test_propagate_coherence_min_times_strength():
    # min(0.8, 0.6) * 0.5 = 0.3
    assert abs(CrystalFlow.propagate_coherence([0.8, 0.6], 0.5) - 0.3) < 1e-9


def test_propagate_coherence_empty_is_zero():
    assert CrystalFlow.propagate_coherence([], 1.0) == 0.0


def test_propagate_coherence_clamps_strength():
    assert CrystalFlow.propagate_coherence([0.9], 5.0) == 0.9   # strength capped at 1


# --------------------------------------------------------------------------- #
# Reasoning: happy path + write-back + provenance
# --------------------------------------------------------------------------- #
def _avg_rule(strength=0.9):
    return Rule(
        name="avg_first",
        fn=lambda facts: [
            sum(f.content["values_sample"][0] for f in facts) / len(facts)
        ],
        strength=strength,
    )


def test_reasoning_writes_derived_node_with_provenance(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.8, 0.6], coherence_boost=0.95, consent_flags=0b01)
    b = mem.encode([0.7, 0.5], coherence_boost=0.90, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    res = flow.apply_rule(_avg_rule(0.9), [a, b])

    assert res["status"] == "ok"
    # min(0.76, 0.72) * 0.9 = 0.648
    assert abs(res["coherence"] - 0.648) < 1e-6
    out_id = res["output_node_id"]
    assert out_id in mem.nodes
    # Provenance recorded.
    summary = mem.nodes[out_id].summary
    assert summary["derived"] is True
    assert set(summary["parents"]) == {a, b}
    assert summary["rule"] == "avg_first"


def test_output_consent_is_intersection(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    # Inputs: one user+family (0b11), one user-only (0b01) -> AND = 0b01.
    a = mem.encode([0.8], coherence_boost=0.95, consent_flags=0b11)
    b = mem.encode([0.7], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    rule = Rule(name="first", fn=lambda facts: [facts[0].content["values_sample"][0]],
                strength=1.0)
    res = flow.apply_rule(rule, [a, b])
    assert res["output_consent_flags"] == 0b01   # never broader than inputs


# --------------------------------------------------------------------------- #
# Reasoning: consent fail-closed
# --------------------------------------------------------------------------- #
def test_consent_fail_closed_aborts_step(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.8], coherence_boost=0.95, consent_flags=0b01)
    secret = mem.encode([0.1], coherence_boost=0.99, consent_flags=0b10)  # Bob-only

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    before = len(mem.nodes)
    res = flow.apply_rule(_avg_rule(), [a, secret])

    assert res["status"] == "consent_denied"
    # Nothing written on a denied step.
    assert len(mem.nodes) == before
    # Logged.
    assert flow.get_derivation_log()[-1]["status"] == "consent_denied"


def test_chain_stops_on_denial(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.8], coherence_boost=0.95, consent_flags=0b01)
    secret = mem.encode([0.1], coherence_boost=0.95, consent_flags=0b10)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    rule = _avg_rule()
    steps = [
        {"rule": rule, "inputs": [a, secret]},   # will be denied
        {"rule": rule, "inputs": [a, a]},        # should never run
    ]
    results = flow.reason_chain(steps)
    assert len(results) == 1
    assert results[0]["status"] == "consent_denied"


# --------------------------------------------------------------------------- #
# Reasoning: low-coherence gate
# --------------------------------------------------------------------------- #
def test_low_coherence_input_blocks_step(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    # coherence_boost 0.3 -> score 0.24, below the 0.5 gate.
    weak = mem.encode([0.8], coherence_boost=0.3, consent_flags=0b01)
    strong = mem.encode([0.7], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.5)
    res = flow.apply_rule(_avg_rule(), [strong, weak])
    assert res["status"] == "low_coherence_input"


# --------------------------------------------------------------------------- #
# Low-memory symbolic-only fallback
# --------------------------------------------------------------------------- #
def test_symbolic_only_disables_autograd_extraction(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.8, 0.6], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", low_memory_symbolic_only=True)
    vals = flow.values_from_node(a)
    assert vals == []   # no gradient tape built under memory pressure

    # But symbolic reasoning still works.
    res = flow.apply_rule(_avg_rule(), [a, a])
    assert res["status"] == "ok"


def test_values_from_node_builds_value_objects(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([1.0, 2.0, 3.0], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice")
    vals = flow.values_from_node(a)
    assert all(isinstance(v, Value) for v in vals)
    assert len(vals) > 0


def test_read_fact_consent_violation_raises(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    secret = mem.encode([0.1], coherence_boost=0.95, consent_flags=0b10)

    flow = CrystalFlow(mem, consumer_id="alice")
    raised = False
    try:
        flow.read_fact(secret)
    except ConsentViolation:
        raised = True
    assert raised


# --------------------------------------------------------------------------- #
# Durable non-numeric conclusions (NEW)
# --------------------------------------------------------------------------- #
def test_text_conclusion_survives_writeback_and_reload(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.8], coherence_boost=0.95, consent_flags=0b01)
    b = mem.encode([0.7], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    # A rule that produces TEXT, not numbers.
    synth = Rule(
        name="synthesize_position",
        fn=lambda facts: "Position: prioritise data sovereignty for families.",
        strength=0.8,
    )
    res = flow.apply_rule(synth, [a, b], output_fact_type="policy_claim")
    assert res["status"] == "ok"
    out_id = res["output_node_id"]

    # Reload from disk; the durable text conclusion must survive intact.
    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    mem2.register_consumer("alice", "Alice", permissions=0b01)
    reloaded = mem2.retrieve(out_id, consumer_id="alice", min_coherence=0.0)
    assert reloaded["payload"] == "Position: prioritise data sovereignty for families."
    # Provenance preserved.
    assert reloaded["metadata"]["consent_flags"] == 0b01
    assert mem2.nodes[out_id].summary["rule"] == "synthesize_position"


def test_dict_conclusion_roundtrips_through_flow(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([0.9], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    rule = Rule(
        name="package_decision",
        fn=lambda facts: {"decision": "adopt", "confidence_basis": "single source"},
        strength=1.0,
    )
    res = flow.apply_rule(rule, [a])
    assert res["status"] == "ok"

    # The derived node can itself be read back as a Fact whose content IS the dict.
    fact = flow.read_fact(res["output_node_id"])
    assert fact.content == {"decision": "adopt", "confidence_basis": "single source"}


# --------------------------------------------------------------------------- #
# Parameterized rules (numeric<->symbolic bridge) (NEW)
# --------------------------------------------------------------------------- #
def test_rule_detects_param_signature():
    one_arg = Rule(name="a", fn=lambda facts: [1.0], strength=1.0)
    two_arg = Rule(name="b", fn=lambda facts, params: [params[0]], strength=1.0)
    assert one_arg.uses_params is False
    assert two_arg.uses_params is True


def test_rule_invoke_passes_params():
    f = Fact(fact_type="x", content={"values_sample": [0.5]}, coherence=0.9)
    scale = Rule(name="scale",
                 fn=lambda facts, params: [facts[0].content["values_sample"][0] * params[0]],
                 strength=0.9)
    assert scale.invoke([f], [3.0]) == [1.5]
    assert scale.invoke([f], [10.0]) == [5.0]


def test_one_arg_rule_ignores_params():
    f = Fact(fact_type="x", content={"values_sample": [0.5]}, coherence=0.9)
    plain = Rule(name="plain", fn=lambda facts: [42.0], strength=1.0)
    assert plain.invoke([f], [3.0]) == [42.0]
    assert plain.invoke([f], None) == [42.0]


def test_apply_rule_threads_params_through(tmp_path):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    a = mem.encode([2.0], coherence_boost=0.95, consent_flags=0b01)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)
    weighted = Rule(
        name="weighted_label",
        fn=lambda facts, params: f"weight={params[0]}",
        strength=0.9,
    )
    res = flow.apply_rule(weighted, [a], params=[0.75])
    assert res["status"] == "ok"
    reloaded = flow.read_fact(res["output_node_id"])
    assert reloaded.content == "weight=0.75"


if __name__ == "__main__":
    sys.exit(0 if pytest is None else pytest.main([__file__, "-v"]))
