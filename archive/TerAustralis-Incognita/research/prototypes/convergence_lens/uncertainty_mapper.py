"""
Uncertainty Mapper: Gap identification (LOOM register)

Identifies where uncertainty exists and what kind of gap it is:
- Knowledge gap: What do we not yet know?
- Technology gap: What could we build but haven't?
- Resource gap: What requires investment?
- Coordination gap: What needs alignment?
- Trust gap: What would make this credible?

Example:
  claim = "AI will achieve AGI by 2030"
  gaps = map_uncertainty(claim)

  gaps.knowledge = "What constitutes AGI? (definitional)"
  gaps.technology = "Can we scale inference cost below threshold?"
  gaps.coordination = "Would actors coordinate on safety?"
  gaps.trust = "How would we verify AGI occurred?"
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Uncertainty:
  """A single gap in understanding."""

  gap_type: str
  """Type: 'knowledge' | 'technology' | 'resource' | 'coordination' | 'trust'"""

  description: str
  """What is unknown."""

  priority: str
  """Priority: 'high' | 'medium' | 'low'"""

  would_resolve: Optional[str] = None
  """What observation would resolve this gap."""


@dataclass
class UncertaintyMap:
  """Complete inventory of gaps for a claim."""

  claim: str
  gaps: List[Uncertainty] = field(default_factory=list)

  def add_gap(self, gap_type: str, description: str, priority: str,
              would_resolve: Optional[str] = None):
    """Register a new gap."""
    self.gaps.append(Uncertainty(
      gap_type=gap_type,
      description=description,
      priority=priority,
      would_resolve=would_resolve,
    ))

  def by_type(self, gap_type: str) -> List[Uncertainty]:
    """Get all gaps of a specific type."""
    return [g for g in self.gaps if g.gap_type == gap_type]

  def high_priority(self) -> List[Uncertainty]:
    """Get high-priority gaps only."""
    return [g for g in self.gaps if g.priority == 'high']


def map_uncertainty(claim: str) -> UncertaintyMap:
  """
  Identify gaps in understanding for a claim.

  This is a placeholder. Real implementation would use:
  - Domain knowledge to identify blindspots
  - Prior claims in ARCHIVE to identify unresolved disagreements
  - CONSTITUTION rules to validate gap classification

  Args:
    claim: A statement to analyze

  Returns:
    UncertaintyMap with identified gaps and their types
  """

  result = UncertaintyMap(claim=claim)

  # Placeholder: generic gaps for any future-oriented claim
  if 'will' in claim.lower() or '203' in claim:
    result.add_gap(
      gap_type='knowledge',
      description='Definition of success criteria unclear',
      priority='high',
      would_resolve='Explicit definition + measurement plan',
    )
    result.add_gap(
      gap_type='technology',
      description='Feasibility beyond current capability unknown',
      priority='high',
      would_resolve='Prototype or technical proof',
    )
    result.add_gap(
      gap_type='coordination',
      description='Multi-actor alignment unspecified',
      priority='medium',
      would_resolve='Explicit governance model',
    )
    result.add_gap(
      gap_type='trust',
      description='Verification mechanism unknown',
      priority='medium',
      would_resolve='Auditable measurement + independent validation',
    )

  return result


if __name__ == '__main__':
  # Example usage
  claims = [
    "AI will achieve AGI by 2030",
    "Scaling laws will continue for 10 more years",
    "We need to coordinate on AI safety",
  ]

  for claim in claims:
    result = map_uncertainty(claim)
    print(f"\nClaim: {claim}")
    print(f"  Total gaps: {len(result.gaps)}")
    for gap in result.high_priority():
      print(f"  [{gap.gap_type}] {gap.description}")
      if gap.would_resolve:
        print(f"    → Resolved by: {gap.would_resolve}")
