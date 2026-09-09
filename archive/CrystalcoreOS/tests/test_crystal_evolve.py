import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_memory import CrystalMemory
from src.crystal_flow import Rule, Value
from src.crystal_evolve import (
    CrystalEvolve, RuleRegistry, Genome, FitnessResult,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _registry():
    reg = RuleRegistry()
    reg.register(Rule(name="normalize", fn=lambda f: f, strength=0.95))
    reg.register(Rule(name="weight", fn=lambda f: f, strength=0.9))
    reg.register(Rule(name="aggregate", fn=lambda f: f, strength=0.8))
    return reg


def _scorer(target):
    def scorer(values):
        loss = Value(0.0)
        for v, t in zip(values, target):
            loss = loss + (v - t) ** 2
        return -loss          # higher (less negative) is better
    return scorer


def _evo(tmp_path, seed=42, **kw):
    mem = CrystalMemory(max_ram_mb=64, storage_path=str(tmp_path / "m.json"))
    defaults = dict(population_size=8, param_dim=3, max_chain_len=4)
    defaults.update(kw)
    return CrystalEvolve(mem, _registry(), _scorer([1.0, -1.0, 0.5]),
                         seed=seed, **defaults)


# --------------------------------------------------------------------------- #
# Registry (closed)
# --------------------------------------------------------------------------- #
def test_registry_closed_lookup():
    reg = _registry()
    assert reg.has("normalize")
    assert not reg.has("teleport")
    assert set(reg.names()) == {"normalize", "weight", "aggregate"}


# --------------------------------------------------------------------------- #
# Validity gate
# --------------------------------------------------------------------------- #
def test_valid_genome_passes(tmp_path):
    evo = _evo(tmp_path)
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize", "weight"])
    ok, reason = evo.validate(g)
    assert ok and reason == "ok"


def test_empty_chain_invalid(tmp_path):
    evo = _evo(tmp_path)
    g = Genome(params=[0.0], rule_chain=[])
    ok, reason = evo.validate(g)
    assert not ok and reason == "empty_rule_chain"


def test_unknown_rule_invalid(tmp_path):
    evo = _evo(tmp_path)
    g = Genome(params=[0.0], rule_chain=["normalize", "ghost"])
    ok, reason = evo.validate(g)
    assert not ok and reason.startswith("unknown_rule")


def test_chain_too_long_invalid(tmp_path):
    evo = _evo(tmp_path, max_chain_len=2)
    g = Genome(params=[0.0], rule_chain=["normalize", "weight", "aggregate"])
    ok, reason = evo.validate(g)
    assert not ok and reason == "chain_too_long"


# --------------------------------------------------------------------------- #
# Gated fitness
# --------------------------------------------------------------------------- #
def test_invalid_genome_gets_zero_fitness_and_logged(tmp_path):
    evo = _evo(tmp_path)
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["ghost"], genome_id="bad")
    res = evo.evaluate(g)
    assert res.valid is False
    assert res.fitness == 0.0
    assert res.reason.startswith("unknown_rule")
    # Logged.
    assert evo.get_eval_log()[-1]["genome_id"] == "bad"


def test_valid_fitness_is_squashed_times_coherence(tmp_path):
    evo = _evo(tmp_path)
    # Params exactly on target -> loss 0 -> raw score 0 -> squash(0)=0.5.
    g = Genome(params=[1.0, -1.0, 0.5], rule_chain=["normalize"])  # strength .95
    res = evo.evaluate(g)
    assert res.valid is True
    # fitness = 0.5 * 0.95 = 0.475
    assert abs(res.fitness - 0.475) < 1e-6


def test_higher_coherence_chain_scores_higher(tmp_path):
    """The gating sign-bug regression test: with identical params, a more
    coherent chain must score strictly higher — even though the raw numeric
    objective here is negative for off-target params."""
    evo = _evo(tmp_path)
    params = [0.0, 0.0, 0.0]   # off target -> negative raw score
    strong = Genome(params=list(params), rule_chain=["normalize"])  # 0.95
    weak = Genome(params=list(params), rule_chain=["aggregate"])    # 0.80
    fs = evo.evaluate(strong).fitness
    fw = evo.evaluate(weak).fitness
    assert fs > fw


# --------------------------------------------------------------------------- #
# Mutation (numeric + symbolic, registry-only)
# --------------------------------------------------------------------------- #
def test_symbolic_mutation_stays_in_registry(tmp_path):
    evo = _evo(tmp_path, mutation_rate=1.0)  # force mutation every time
    parent = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"],
                    genome_id="p")
    names = set(evo.registry.names())
    for _ in range(200):
        child = evo.mutate(parent)
        # Every rule a mutation produces must be a known registry name.
        assert set(child.rule_chain).issubset(names)


def test_numeric_mutation_perturbs_params(tmp_path):
    evo = _evo(tmp_path, mutation_rate=1.0, param_sigma=0.5)
    parent = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"])
    changed = False
    for _ in range(20):
        child = evo.mutate(parent)
        if child.params != parent.params:
            changed = True
            break
    assert changed


def test_mutation_records_parent(tmp_path):
    evo = _evo(tmp_path)
    parent = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"],
                    genome_id="parent42")
    child = evo.mutate(parent)
    assert child.parent_ids == ["parent42"]


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #
def test_same_seed_reproduces(tmp_path):
    e1 = _evo(tmp_path / "a" if False else tmp_path, seed=13)
    h1 = e1.run(6)
    e2 = _evo(tmp_path, seed=13)
    h2 = e2.run(6)
    assert [r["best_fitness"] for r in h1] == [r["best_fitness"] for r in h2]


def test_different_seed_diverges(tmp_path):
    h1 = _evo(tmp_path, seed=1).run(6)
    h2 = _evo(tmp_path, seed=2).run(6)
    assert [r["best_fitness"] for r in h1] != [r["best_fitness"] for r in h2]


# --------------------------------------------------------------------------- #
# Optimization actually improves
# --------------------------------------------------------------------------- #
def test_fitness_improves_over_generations(tmp_path):
    evo = _evo(tmp_path, seed=42, population_size=12, param_dim=3)
    history = evo.run(generations=10, refine_steps=5)
    assert history[-1]["best_fitness"] > history[0]["best_fitness"]


def test_population_size_stable(tmp_path):
    evo = _evo(tmp_path, population_size=10)
    history = evo.run(5)
    for h in history:
        assert h["population_size"] == 10


def test_n_valid_counts_structure_not_sign(tmp_path):
    # All seeded genomes are structurally valid even with a negative objective.
    evo = _evo(tmp_path)
    h = evo.run(1)
    assert h[0]["n_valid"] == evo.population_size


# --------------------------------------------------------------------------- #
# Persistence with provenance + high priority
# --------------------------------------------------------------------------- #
def test_persist_best_writes_durable_genome(tmp_path):
    evo = _evo(tmp_path, seed=42)
    evo.run(5, refine_steps=5)
    ids = evo.persist_best(top_k=1, consent_flags=0b01)
    assert len(ids) == 1

    got = evo.memory.retrieve(ids[0], min_coherence=0.0)
    payload = got["payload"]
    assert payload["type"] == "genome"
    assert "rule_chain" in payload and "params" in payload


def test_survivor_has_high_priority(tmp_path):
    evo = _evo(tmp_path, seed=42, survivor_priority=10.0)
    evo.run(3)
    ids = evo.persist_best(top_k=1)
    node = evo.memory.nodes[ids[0]]
    assert node.metadata.family_priority == 10.0


def test_survivor_survives_pruning_pressure(tmp_path):
    """A high-priority survivor should outlive low-priority churn."""
    evo = _evo(tmp_path, seed=42, survivor_priority=50.0)
    evo.run(3)
    ids = evo.persist_best(top_k=1)
    survivor = ids[0]

    # Flood memory with low-priority nodes under a tight budget.
    evo.memory.max_ram_mb = 0.05
    for i in range(120):
        evo.memory.encode([float(i)] * 30, coherence_boost=0.5,
                           family_priority=0.1, consent_flags=1)

    assert survivor in evo.memory.nodes


def test_persisted_genome_roundtrips_after_reload(tmp_path):
    path = str(tmp_path / "m.json")
    mem = CrystalMemory(max_ram_mb=64, storage_path=path)
    from src.crystal_evolve import CrystalEvolve as CE
    evo = CE(mem, _registry(), _scorer([1.0, -1.0, 0.5]),
             seed=42, population_size=8, param_dim=3)
    evo.run(5, refine_steps=5)
    ids = evo.persist_best(top_k=1, consent_flags=0b01)

    # Reload from disk.
    mem2 = CrystalMemory(max_ram_mb=64, storage_path=path)
    got = mem2.retrieve(ids[0], min_coherence=0.0)
    g = Genome.from_dict(got["payload"])
    assert len(g.params) == 3
    assert all(evo.registry.has(n) for n in g.rule_chain)


# --------------------------------------------------------------------------- #
# Inheritance modes: Lamarckian vs Baldwinian (NEW)
# --------------------------------------------------------------------------- #
def test_lamarckian_writes_refined_params_back(tmp_path):
    evo = _evo(tmp_path, lamarckian=True)
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"], genome_id="g")
    evo.evaluate(g, refine_steps=10)
    # Params should have moved toward the target under refinement.
    assert g.params != [0.0, 0.0, 0.0]


def test_baldwinian_keeps_original_params(tmp_path):
    evo = _evo(tmp_path, lamarckian=False)
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"], genome_id="g")
    evo.evaluate(g, refine_steps=10)
    # Original params untouched despite refinement.
    assert g.params == [0.0, 0.0, 0.0]


def test_baldwinian_still_scores_on_refined_values(tmp_path):
    """Baldwinian fitness should reflect the *refined* score, so a genome with
    learning capacity scores higher than its unrefined raw score would."""
    evo = _evo(tmp_path, lamarckian=False)
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"], genome_id="g")

    raw = evo.evaluate(g, refine_steps=0).fitness          # no learning
    # Reset eval log noise irrelevant; re-evaluate with refinement.
    g2 = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"], genome_id="g2")
    learned = evo.evaluate(g2, refine_steps=10).fitness    # with learning
    assert learned > raw
    # And g2's stored params are still the originals (Baldwinian).
    assert g2.params == [0.0, 0.0, 0.0]


def test_per_call_mode_overrides_instance_default(tmp_path):
    evo = _evo(tmp_path, lamarckian=True)   # instance default Lamarckian
    g = Genome(params=[0.0, 0.0, 0.0], rule_chain=["normalize"], genome_id="g")
    evo.evaluate(g, refine_steps=10, lamarckian=False)  # override to Baldwinian
    assert g.params == [0.0, 0.0, 0.0]


if __name__ == "__main__":
    sys.exit(0 if pytest is None else pytest.main([__file__, "-v"]))
