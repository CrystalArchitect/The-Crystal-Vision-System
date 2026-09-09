#!/usr/bin/env python3
"""
Swarm Race — Phase 5
CrystalCore OS

Population-based evolutionary race built on the crystal_evolve Genome model.
Agents race toward a goal line; selection is multi-objective (Pareto
dominance over progress, coherence, and persistence), mutation follows the
closed-registry discipline (recombine named behaviours, never invent logic),
and every generation is recorded in the governance audit trail.

Standard library only. Deterministic under a fixed seed.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random

try:
    from src.crystal_evolve import Genome
except ImportError:
    from crystal_evolve import Genome

from crystallcore.governance.sces_volume_8_tracking import (
    AuditTrail, AuditEvent, EventType,
)
from .agents import SwarmAgent, BehaviorRegistry, default_behavior_registry
from .reinforcement import CoherenceReinforcement


# Effort spent moving costs coherence; racing is not free.
EFFORT_COST = 0.015
# A step counts as a "hard stretch survived" when the agent kept moving
# despite depleted coherence.
HARD_STRETCH_COHERENCE = 0.6
MIN_CHAIN, MAX_CHAIN = 1, 4


@dataclass
class AgentFitness:
    """Multi-objective outcome for one agent. Fully inspectable."""
    agent_id: str
    progress: float       # 0..1+ (>=1.0 means finished; earlier finish scores higher)
    coherence: float      # final coherence 0..1
    persistence: float    # normalized hard-stretches survived
    pareto_rank: int = 0  # 0 = non-dominated front

    def objectives(self) -> Tuple[float, float, float]:
        return (self.progress, self.coherence, self.persistence)

    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "progress": round(self.progress, 4),
            "coherence": round(self.coherence, 4),
            "persistence": round(self.persistence, 4),
            "pareto_rank": self.pareto_rank,
        }


def _dominates(a: Tuple[float, ...], b: Tuple[float, ...]) -> bool:
    """Pareto dominance: >= everywhere, > somewhere."""
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


def pareto_ranks(fitnesses: List[AgentFitness]) -> None:
    """Assign Pareto ranks in place (rank 0 = non-dominated front)."""
    remaining = list(fitnesses)
    rank = 0
    while remaining:
        front = [f for f in remaining
                 if not any(_dominates(g.objectives(), f.objectives())
                            for g in remaining if g is not f)]
        if not front:  # total tie safety valve
            front = list(remaining)
        for f in front:
            f.pareto_rank = rank
        remaining = [f for f in remaining if f not in front]
        rank += 1


class SwarmRace:
    """Evolutionary race trainer with governed, audited generations."""

    def __init__(self, population_size: int = 12, goal: float = 100.0,
                 seed: int = 0,
                 registry: Optional[BehaviorRegistry] = None,
                 reinforcement: Optional[CoherenceReinforcement] = None,
                 audit_trail: Optional[AuditTrail] = None):
        self.rng = random.Random(seed)
        self.goal = goal
        self.population_size = population_size
        self.registry = registry or default_behavior_registry()
        self.reinforcement = reinforcement or CoherenceReinforcement()
        self.audit = audit_trail or AuditTrail()
        self.generation = 0
        self.agents: List[SwarmAgent] = []
        self._next_id = 0
        self._seed_population()

    # ------------------------------------------------------------------ #
    # Population
    # ------------------------------------------------------------------ #
    def _new_agent_id(self) -> str:
        self._next_id += 1
        return f"agent_{self._next_id:04d}"

    def _random_genome(self) -> Genome:
        names = self.registry.names()
        chain_len = self.rng.randint(MIN_CHAIN, MAX_CHAIN)
        chain = [self.rng.choice(names) for _ in range(chain_len)]
        params = [self.rng.uniform(-1.0, 1.0) for _ in range(chain_len)]
        return Genome(params=params, rule_chain=chain,
                      genome_id=f"g_{self._next_id:04d}",
                      generation=self.generation)

    def _seed_population(self) -> None:
        self.agents = []
        for _ in range(self.population_size):
            agent_id = self._new_agent_id()
            self.agents.append(SwarmAgent(agent_id=agent_id,
                                          genome=self._random_genome()))

    def mutate(self, parent: Genome) -> Genome:
        """Closed-registry mutation: perturb weights; swap/add/remove
        behaviour NAMES drawn only from the registry."""
        params = [p + self.rng.gauss(0.0, 0.3) for p in parent.params]
        chain = list(parent.rule_chain)
        names = self.registry.names()
        roll = self.rng.random()
        if roll < 0.3 and chain:
            chain[self.rng.randrange(len(chain))] = self.rng.choice(names)
        elif roll < 0.4 and len(chain) < MAX_CHAIN:
            chain.append(self.rng.choice(names))
            params.append(self.rng.uniform(-1.0, 1.0))
        elif roll < 0.5 and len(chain) > MIN_CHAIN:
            idx = self.rng.randrange(len(chain))
            chain.pop(idx)
            if idx < len(params):
                params.pop(idx)
        return Genome(params=params, rule_chain=chain,
                      genome_id=f"g_{self._next_id:04d}m",
                      parent_ids=[parent.genome_id],
                      generation=self.generation + 1)

    # ------------------------------------------------------------------ #
    # Racing
    # ------------------------------------------------------------------ #
    def _race(self, steps: int) -> None:
        """Run one race: agents move, spend coherence, share with kin,
        and receive persistence-gated reinforcement pulses."""
        for agent in self.agents:
            agent.position = 0.0
            agent.finished_at_step = None

        for step in range(1, steps + 1):
            env = {
                "goal": self.goal,
                "positions": {a.agent_id: a.position for a in self.agents},
            }
            for agent in self.agents:
                if agent.finished_at_step is not None:
                    continue
                v = agent.velocity(self.registry, env)
                agent.position += v * (self.goal / steps) * 2.0
                agent.coherence = max(0.05, agent.coherence - EFFORT_COST * v)
                if agent.coherence < HARD_STRETCH_COHERENCE and v > 0.05:
                    agent.low_fitness_steps_survived += 1
                if agent.position >= self.goal:
                    agent.finished_at_step = step

            # Kinship state-sharing: adjacent pairs, bounded blend
            live = [a for a in self.agents if a.finished_at_step is None]
            for i in range(0, len(live) - 1, 2):
                live[i].share_state_with(live[i + 1])

            self.reinforcement.maybe_pulse(self.agents, step)

    def _evaluate(self, steps: int) -> List[AgentFitness]:
        max_persist = max((a.low_fitness_steps_survived for a in self.agents),
                          default=0) or 1
        fitnesses = []
        for a in self.agents:
            if a.finished_at_step is not None:
                progress = 1.0 + (steps - a.finished_at_step) / steps
            else:
                progress = min(1.0, a.position / self.goal)
            fitnesses.append(AgentFitness(
                agent_id=a.agent_id,
                progress=progress,
                coherence=a.coherence,
                persistence=a.low_fitness_steps_survived / max_persist,
            ))
        pareto_ranks(fitnesses)
        return fitnesses

    def run_generation(self, steps: int = 50) -> Dict:
        """Race, evaluate, select on Pareto rank, mutate to refill. Audited."""
        self._race(steps)
        fitnesses = self._evaluate(steps)

        # Selection: keep the best half by (pareto_rank asc, progress desc)
        by_agent = {f.agent_id: f for f in fitnesses}
        survivors = sorted(
            self.agents,
            key=lambda a: (by_agent[a.agent_id].pareto_rank,
                           -by_agent[a.agent_id].progress),
        )[: max(2, self.population_size // 2)]

        next_gen = list(survivors)
        while len(next_gen) < self.population_size:
            parent = self.rng.choice(survivors)
            agent_id = self._new_agent_id()
            next_gen.append(SwarmAgent(agent_id=agent_id,
                                       genome=self.mutate(parent.genome)))
        self.agents = next_gen
        self.generation += 1

        report = {
            "generation": self.generation,
            "finishers": sum(1 for f in fitnesses if f.progress >= 1.0),
            "best_progress": round(max(f.progress for f in fitnesses), 4),
            "avg_coherence": round(
                sum(f.coherence for f in fitnesses) / len(fitnesses), 4),
            "pareto_front_size": sum(1 for f in fitnesses if f.pareto_rank == 0),
            "reinforcement": self.reinforcement.summary(),
            "fitness_table": [f.to_dict() for f in fitnesses],
        }
        self.audit.record_event(AuditEvent(
            event_id=f"swarm_gen_{self.generation}",
            event_type=EventType.OPERATION_EXECUTED,
            actor="swarm_race",
            subject=f"generation_{self.generation}",
            new_state={k: report[k] for k in
                       ("generation", "finishers", "best_progress",
                        "avg_coherence", "pareto_front_size")},
        ))
        return report

    def run(self, generations: int, steps: int = 50) -> List[Dict]:
        """Run several audited generations; returns all reports."""
        return [self.run_generation(steps) for _ in range(generations)]
