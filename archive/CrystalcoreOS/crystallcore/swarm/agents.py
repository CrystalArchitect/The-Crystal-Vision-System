#!/usr/bin/env python3
"""
Swarm Agents — Phase 5
CrystalCore OS

A SwarmAgent is an evolutionary racer whose behaviour is expressed by a
crystal_evolve Genome: numeric params weight a chain of behaviour primitives
drawn from a CLOSED registry (the same discipline as crystal_evolve's
RuleRegistry — mutation may recombine named primitives, never invent logic).

Kinship is real genome similarity: shared rule-chain entries and parameter
distance. Kin agents may share bounded state (a small, capped parameter
blend) — the honest implementation of "entanglement".

Standard library only.
"""

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass, field
import math

try:
    from src.crystal_evolve import Genome
except ImportError:  # flat / direct execution
    from crystal_evolve import Genome


# --------------------------------------------------------------------------- #
# Closed behaviour registry
# --------------------------------------------------------------------------- #
class BehaviorRegistry:
    """Closed set of named behaviour primitives.

    Each primitive maps (agent, env_state) -> a velocity contribution in
    [-1, 1]. Genomes reference primitives ONLY by name; mutation recombines
    names from this registry and never creates new behaviour.
    """

    def __init__(self):
        self._primitives: Dict[str, Callable] = {}

    def register(self, name: str, fn: Callable) -> None:
        self._primitives[name] = fn

    def get(self, name: str) -> Optional[Callable]:
        return self._primitives.get(name)

    def has(self, name: str) -> bool:
        return name in self._primitives

    def names(self) -> List[str]:
        return list(self._primitives.keys())

    def __len__(self) -> int:
        return len(self._primitives)


def default_behavior_registry() -> BehaviorRegistry:
    """The standard closed set of racing behaviours."""
    reg = BehaviorRegistry()

    def seek_goal(agent: "SwarmAgent", env: Dict) -> float:
        # Push toward the goal, harder the further away
        remaining = env["goal"] - agent.position
        return max(-1.0, min(1.0, remaining / max(1.0, env["goal"])))

    def pace_conserve(agent: "SwarmAgent", env: Dict) -> float:
        # Move steadily; conserve coherence by avoiding max-effort bursts
        return 0.4

    def kin_align(agent: "SwarmAgent", env: Dict) -> float:
        # Drift toward the mean position of registered kin
        if not agent.kin_ids:
            return 0.0
        positions = env.get("positions", {})
        kin_pos = [positions[k] for k in agent.kin_ids if k in positions]
        if not kin_pos:
            return 0.0
        mean_kin = sum(kin_pos) / len(kin_pos)
        return max(-1.0, min(1.0, (mean_kin - agent.position) / max(1.0, env["goal"])))

    def surge(agent: "SwarmAgent", env: Dict) -> float:
        # High-effort burst, costs coherence (applied by the environment)
        return 1.0

    reg.register("seek_goal", seek_goal)
    reg.register("pace_conserve", pace_conserve)
    reg.register("kin_align", kin_align)
    reg.register("surge", surge)
    return reg


# --------------------------------------------------------------------------- #
# Swarm agent
# --------------------------------------------------------------------------- #
@dataclass
class SwarmAgent:
    """One evolutionary racer."""
    agent_id: str
    genome: Genome
    position: float = 0.0
    coherence: float = 1.0
    kin_ids: List[str] = field(default_factory=list)
    finished_at_step: Optional[int] = None
    low_fitness_steps_survived: int = 0   # persistence through hard stretches
    reinforcement_received: float = 0.0   # total pulse boost (for cap/decay)

    def velocity(self, registry: BehaviorRegistry, env: Dict) -> float:
        """Weighted sum of the genome's behaviour chain, coherence-scaled.

        params[i] weights rule_chain[i]; missing weights default to 1.0.
        Output clamped to [0, 1] — racers move forward only, at a rate
        bounded by their coherence (an incoherent agent crawls).
        """
        total = 0.0
        for i, name in enumerate(self.genome.rule_chain):
            fn = registry.get(name)
            if fn is None:
                continue
            weight = self.genome.params[i] if i < len(self.genome.params) else 1.0
            total += weight * fn(self, env)
        # Squash to (0, 1) then scale by coherence
        squashed = 1.0 / (1.0 + math.exp(-total))
        return squashed * max(0.1, self.coherence)

    def is_kin(self, other: "SwarmAgent", param_tolerance: float = 1.5) -> bool:
        """Kinship = shared behaviour ancestry + nearby parameters.

        True when the two genomes share at least half of the shorter
        rule chain AND their common-length parameter distance is small.
        """
        if not self.genome.rule_chain or not other.genome.rule_chain:
            return False
        shared = set(self.genome.rule_chain) & set(other.genome.rule_chain)
        min_len = min(len(self.genome.rule_chain), len(other.genome.rule_chain))
        if len(shared) * 2 < min_len:
            return False
        n = min(len(self.genome.params), len(other.genome.params))
        if n == 0:
            return True
        dist = math.sqrt(sum(
            (self.genome.params[i] - other.genome.params[i]) ** 2 for i in range(n)))
        return dist <= param_tolerance

    def share_state_with(self, other: "SwarmAgent", blend: float = 0.1) -> bool:
        """Bounded state sharing between kin (both drift slightly together).

        Only kin may share; blend is capped at 0.25 so no agent's identity
        is overwritten — diversity is preserved by construction.
        """
        if not self.is_kin(other):
            return False
        blend = max(0.0, min(0.25, blend))
        n = min(len(self.genome.params), len(other.genome.params))
        for i in range(n):
            a, b = self.genome.params[i], other.genome.params[i]
            self.genome.params[i] = a + blend * (b - a)
            other.genome.params[i] = b + blend * (a - b)
        if other.agent_id not in self.kin_ids:
            self.kin_ids.append(other.agent_id)
        if self.agent_id not in other.kin_ids:
            other.kin_ids.append(self.agent_id)
        return True
