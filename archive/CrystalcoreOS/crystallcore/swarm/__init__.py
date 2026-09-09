"""
Swarm Layer — Evolutionary Racing on Real Foundations
CrystalCore OS Phase 5

Built on the crystal_evolve Genome model (hybrid numeric params + closed
symbolic rule chains) and integrated with the governance audit trail:

- agents: SwarmAgent, closed BehaviorRegistry, genome-similarity kinship
  with bounded state sharing
- race: SwarmRace evolutionary trainer — multi-objective Pareto fitness
  (progress, coherence, persistence), closed-registry mutation, audited
  generations
- reinforcement: CoherenceReinforcement — persistence-gated, capped,
  diminishing-return coherence restoration with truthful pulse reports

All modules use Python stdlib only. Zero external dependencies.
Version: v0.5 (Phase 5: Swarm)
"""

from .agents import SwarmAgent, BehaviorRegistry, default_behavior_registry
from .race import SwarmRace, AgentFitness, pareto_ranks
from .reinforcement import CoherenceReinforcement, PulseReport

__version__ = "v0.5"
__phase__ = "5"

__all__ = [
    "SwarmAgent", "BehaviorRegistry", "default_behavior_registry",
    "SwarmRace", "AgentFitness", "pareto_ranks",
    "CoherenceReinforcement", "PulseReport",
]
