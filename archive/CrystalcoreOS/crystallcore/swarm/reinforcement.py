#!/usr/bin/env python3
"""
Coherence Reinforcement — Phase 5
CrystalCore OS

The honest implementation of the "celebration layer": a periodic pulse that
rewards agents who kept moving through low-fitness stretches, restoring
coherence they spent on the climb.

Design constraints (all enforced, all tested):
- Persistence-gated: only agents that actually survived hard stretches
  qualify — a pulse is never a free ride.
- Diminishing returns: each agent has a lifetime reinforcement cap, and
  successive pulses to the same agent shrink geometrically. No agent can
  be pumped to artificial coherence by repetition.
- Rally mode: when swarm-average coherence is critically low the pulse
  strengthens (bounded), so a struggling swarm recovers rather than
  collapses.
- Truthful accounting: every pulse is returned in a report — nothing is
  silently injected.

Standard library only.
"""

from typing import Dict, List
from dataclasses import dataclass

from .agents import SwarmAgent


@dataclass
class PulseReport:
    """Truthful record of one reinforcement pulse."""
    step: int
    agents_boosted: int
    total_boost: float
    rally_mode: bool
    swarm_avg_coherence_before: float
    swarm_avg_coherence_after: float


class CoherenceReinforcement:
    """Persistence-gated, capped coherence restoration."""

    def __init__(self, period: int = 10, base_boost: float = 0.05,
                 lifetime_cap: float = 0.5, decay: float = 0.7,
                 rally_threshold: float = 0.5, rally_multiplier: float = 2.0,
                 persistence_required: int = 3):
        self.period = max(1, period)
        self.base_boost = base_boost
        self.lifetime_cap = lifetime_cap
        self.decay = decay
        self.rally_threshold = rally_threshold
        self.rally_multiplier = rally_multiplier
        self.persistence_required = persistence_required
        self.reports: List[PulseReport] = []

    def maybe_pulse(self, agents: List[SwarmAgent], step: int) -> PulseReport:
        """Apply a pulse if the step is on-period. Returns a truthful report
        (zero-boost report on off-period steps)."""
        live = [a for a in agents if a.finished_at_step is None]
        avg_before = (sum(a.coherence for a in live) / len(live)) if live else 0.0

        if step % self.period != 0 or not live:
            report = PulseReport(step, 0, 0.0, False, avg_before, avg_before)
            return report

        rally = avg_before < self.rally_threshold
        multiplier = self.rally_multiplier if rally else 1.0

        boosted = 0
        total = 0.0
        for agent in live:
            if agent.low_fitness_steps_survived < self.persistence_required:
                continue  # persistence gate: no free rides
            if agent.reinforcement_received >= self.lifetime_cap:
                continue  # lifetime cap reached
            # Geometric diminishing returns on repeated reinforcement
            prior_pulses = agent.reinforcement_received / max(self.base_boost, 1e-9)
            boost = self.base_boost * multiplier * (self.decay ** prior_pulses)
            boost = min(boost, self.lifetime_cap - agent.reinforcement_received)
            if boost <= 0:
                continue
            agent.coherence = min(1.0, agent.coherence + boost)
            agent.reinforcement_received += boost
            boosted += 1
            total += boost

        avg_after = (sum(a.coherence for a in live) / len(live)) if live else 0.0
        report = PulseReport(step, boosted, round(total, 6), rally,
                             round(avg_before, 6), round(avg_after, 6))
        self.reports.append(report)
        return report

    def summary(self) -> Dict:
        pulses = [r for r in self.reports if r.agents_boosted > 0]
        return {
            "pulses_applied": len(pulses),
            "total_boost_given": round(sum(r.total_boost for r in pulses), 6),
            "rally_pulses": sum(1 for r in pulses if r.rally_mode),
        }
