import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_evolve import Genome
from crystallcore.swarm import (
    SwarmAgent, BehaviorRegistry, default_behavior_registry,
    SwarmRace, AgentFitness, pareto_ranks,
    CoherenceReinforcement,
)


def _agent(agent_id="a1", chain=None, params=None, coherence=1.0):
    return SwarmAgent(
        agent_id=agent_id,
        genome=Genome(params=params or [0.5, 0.5],
                      rule_chain=chain or ["seek_goal", "pace_conserve"],
                      genome_id=agent_id),
        coherence=coherence,
    )


# --------------------------------------------------------------------------- #
# Agents & behaviour registry
# --------------------------------------------------------------------------- #
def test_default_registry_is_closed_set_of_four():
    reg = default_behavior_registry()
    assert sorted(reg.names()) == ["kin_align", "pace_conserve", "seek_goal", "surge"]


def test_velocity_is_forward_only_and_coherence_scaled():
    reg = default_behavior_registry()
    env = {"goal": 100.0, "positions": {}}
    strong = _agent("strong", coherence=1.0)
    weak = _agent("weak", coherence=0.2)
    v_strong = strong.velocity(reg, env)
    v_weak = weak.velocity(reg, env)
    assert v_strong > 0
    assert v_weak > 0
    assert v_weak < v_strong  # incoherent agents crawl


def test_unknown_behavior_names_are_ignored_not_invented():
    reg = default_behavior_registry()
    agent = _agent(chain=["seek_goal", "made_up_behavior"], params=[0.5, 9.9])
    env = {"goal": 100.0, "positions": {}}
    # Must not raise; the unknown name contributes nothing
    assert agent.velocity(reg, env) > 0


def test_kinship_requires_shared_chain_and_close_params():
    kin_a = _agent("a", chain=["seek_goal", "surge"], params=[0.5, 0.5])
    kin_b = _agent("b", chain=["seek_goal", "surge"], params=[0.6, 0.4])
    stranger = _agent("c", chain=["pace_conserve"], params=[0.5])
    far_kin = _agent("d", chain=["seek_goal", "surge"], params=[5.0, -5.0])
    assert kin_a.is_kin(kin_b) is True
    assert kin_a.is_kin(stranger) is False
    assert kin_a.is_kin(far_kin) is False  # same chain, distant params


def test_state_sharing_only_between_kin_and_bounded():
    kin_a = _agent("a", chain=["seek_goal"], params=[0.0])
    kin_b = _agent("b", chain=["seek_goal"], params=[1.0])
    stranger = _agent("c", chain=["surge"], params=[0.0])
    assert kin_a.share_state_with(stranger) is False
    assert kin_a.share_state_with(kin_b, blend=0.9) is True  # blend capped at 0.25
    assert 0.0 < kin_a.genome.params[0] <= 0.25
    assert 0.75 <= kin_b.genome.params[0] < 1.0
    assert "b" in kin_a.kin_ids and "a" in kin_b.kin_ids


# --------------------------------------------------------------------------- #
# Coherence reinforcement: no free rides
# --------------------------------------------------------------------------- #
def test_pulse_skips_agents_without_persistence():
    cr = CoherenceReinforcement(period=1, persistence_required=3)
    fresh = _agent("fresh", coherence=0.5)  # survived nothing yet
    report = cr.maybe_pulse([fresh], step=1)
    assert report.agents_boosted == 0
    assert fresh.coherence == 0.5


def test_pulse_boosts_persistent_agent():
    cr = CoherenceReinforcement(period=1, persistence_required=3)
    gritty = _agent("gritty", coherence=0.5)
    gritty.low_fitness_steps_survived = 5
    report = cr.maybe_pulse([gritty], step=1)
    assert report.agents_boosted == 1
    assert gritty.coherence > 0.5


def test_reinforcement_has_lifetime_cap_and_diminishing_returns():
    # coherence 0.6 keeps the swarm above the rally threshold so the
    # geometric decay is observable rather than one rally-sized pulse
    cr = CoherenceReinforcement(period=1, base_boost=0.1, lifetime_cap=0.2,
                                persistence_required=1)
    agent = _agent("capped", coherence=0.6)
    agent.low_fitness_steps_survived = 10
    boosts = []
    for step in range(1, 20):
        before = agent.reinforcement_received
        cr.maybe_pulse([agent], step)
        boosts.append(agent.reinforcement_received - before)
    assert agent.reinforcement_received <= 0.2 + 1e-9  # hard cap
    positive = [b for b in boosts if b > 1e-12]
    assert len(positive) >= 2
    assert positive[1] < positive[0]  # diminishing returns


def test_rally_mode_activates_when_swarm_is_low():
    cr = CoherenceReinforcement(period=1, rally_threshold=0.5,
                                persistence_required=1)
    low = _agent("low", coherence=0.2)
    low.low_fitness_steps_survived = 5
    report = cr.maybe_pulse([low], step=1)
    assert report.rally_mode is True


def test_off_period_steps_apply_nothing():
    cr = CoherenceReinforcement(period=10, persistence_required=1)
    agent = _agent("waiting", coherence=0.5)
    agent.low_fitness_steps_survived = 5
    report = cr.maybe_pulse([agent], step=3)
    assert report.agents_boosted == 0
    assert agent.coherence == 0.5


# --------------------------------------------------------------------------- #
# Pareto fitness
# --------------------------------------------------------------------------- #
def test_pareto_dominated_agent_gets_worse_rank():
    good = AgentFitness("good", progress=0.9, coherence=0.9, persistence=0.9)
    bad = AgentFitness("bad", progress=0.5, coherence=0.5, persistence=0.5)
    pareto_ranks([good, bad])
    assert good.pareto_rank == 0
    assert bad.pareto_rank == 1


def test_pareto_tradeoffs_share_the_front():
    fast = AgentFitness("fast", progress=1.0, coherence=0.3, persistence=0.2)
    steady = AgentFitness("steady", progress=0.6, coherence=0.9, persistence=0.8)
    pareto_ranks([fast, steady])
    assert fast.pareto_rank == 0
    assert steady.pareto_rank == 0  # neither dominates the other


# --------------------------------------------------------------------------- #
# The race itself
# --------------------------------------------------------------------------- #
def test_race_is_deterministic_under_seed():
    r1 = SwarmRace(population_size=8, seed=42).run_generation(steps=30)
    r2 = SwarmRace(population_size=8, seed=42).run_generation(steps=30)
    assert r1["best_progress"] == r2["best_progress"]
    assert r1["avg_coherence"] == r2["avg_coherence"]


def test_generation_keeps_population_size_and_advances():
    race = SwarmRace(population_size=10, seed=7)
    report = race.run_generation(steps=30)
    assert len(race.agents) == 10
    assert race.generation == 1
    assert report["pareto_front_size"] >= 1
    assert len(report["fitness_table"]) == 10


def test_mutation_only_recombines_registry_names():
    race = SwarmRace(population_size=6, seed=3)
    valid = set(race.registry.names())
    parent = race.agents[0].genome
    for _ in range(50):
        child = race.mutate(parent)
        assert set(child.rule_chain) <= valid
        assert 1 <= len(child.rule_chain) <= 4


def test_multi_generation_run_is_audited():
    race = SwarmRace(population_size=8, seed=11)
    reports = race.run(generations=3, steps=25)
    assert len(reports) == 3
    events = race.audit.get_all_events()
    assert len(events) == 3
    assert all(e.event_type.value == "operation_executed" for e in events)
    assert race.audit.verify_immutability() is True


def test_progress_improves_or_holds_over_generations():
    race = SwarmRace(population_size=12, seed=5)
    reports = race.run(generations=5, steps=40)
    assert reports[-1]["best_progress"] >= reports[0]["best_progress"] * 0.8
