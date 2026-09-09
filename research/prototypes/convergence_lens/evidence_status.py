"""
Evidence Status: Confidence tracking (CHRONICLE register)

Records the evidence status and confidence level of a claim at point-in-time.

Example:
  status = EvidenceStatus(
    claim="AI will reach AGI by 2030",
    confidence_percent=35,
    evidence_tier="speculative",
    sources=["scaling_law_extrapolation", "expert_opinion"],
    timestamp="2026-07-27T09:30:00Z",
  )

  status.summary()
  # "AGI by 2030: 35% confidence, speculative tier, based on 2 sources"

The same claim recorded on a different date = different evidence status.
This prevents historical rewriting: CHRONICLE preserves both.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class EvidenceStatus:
  """Confidence and evidence record at a specific point in time."""

  claim: str
  """The statement being evaluated."""

  confidence_percent: int
  """Confidence level: 0-100. Does NOT equal probability."""

  evidence_tier: str
  """Tier: 'direct' | 'measured' | 'inferred' | 'speculative'"""

  sources: List[str]
  """What evidence or reasoning supports this confidence level."""

  timestamp: str
  """ISO8601 datetime when this status was recorded."""

  uncertainty: Optional[str] = None
  """Explicit acknowledgment of what remains unknown."""

  later_update: Optional['EvidenceStatus'] = None
  """If this status was later superseded, link to the newer one."""

  def summary(self) -> str:
    """Human-readable summary."""
    return (f"{self.claim[:50]}... "
            f"({self.confidence_percent}% confidence, "
            f"{self.evidence_tier} tier, "
            f"{len(self.sources)} source(s))")

  def evolved_to(self, new_status: 'EvidenceStatus'):
    """Link this status to a newer one."""
    self.later_update = new_status

  def as_chronicle_entry(self) -> dict:
    """Serialize as CHRONICLE record for archival."""
    return {
      'claim': self.claim,
      'confidence': self.confidence_percent,
      'evidence_tier': self.evidence_tier,
      'sources': self.sources,
      'recorded_at': self.timestamp,
      'uncertainty': self.uncertainty,
    }


class StatusTimeline:
  """Track how a claim's confidence evolved over time."""

  def __init__(self, claim: str):
    self.claim = claim
    self.statuses: List[EvidenceStatus] = []

  def add_status(self, confidence_percent: int, evidence_tier: str,
                 sources: List[str], timestamp: str,
                 uncertainty: Optional[str] = None) -> EvidenceStatus:
    """Record a new evidence status."""

    new_status = EvidenceStatus(
      claim=self.claim,
      confidence_percent=confidence_percent,
      evidence_tier=evidence_tier,
      sources=sources,
      timestamp=timestamp,
      uncertainty=uncertainty,
    )

    if self.statuses:
      self.statuses[-1].evolved_to(new_status)

    self.statuses.append(new_status)
    return new_status

  def current(self) -> Optional[EvidenceStatus]:
    """Get the most recent status."""
    return self.statuses[-1] if self.statuses else None

  def delta(self) -> Optional[int]:
    """Confidence change since first recording (as percentage points)."""
    if len(self.statuses) < 2:
      return None
    return self.statuses[-1].confidence_percent - self.statuses[0].confidence_percent

  def chronicle(self) -> List[dict]:
    """Export as CHRONICLE entries."""
    return [status.as_chronicle_entry() for status in self.statuses]


if __name__ == '__main__':
  # Example: track how confidence in an idea changes
  timeline = StatusTimeline("AI will reach AGI by 2030")

  timeline.add_status(
    confidence_percent=35,
    evidence_tier='speculative',
    sources=['scaling_law_extrapolation'],
    timestamp='2026-01-01T00:00:00Z',
    uncertainty='Scaling laws hold beyond observed range unproven',
  )

  timeline.add_status(
    confidence_percent=42,
    evidence_tier='inferred',
    sources=['scaling_law_extrapolation', 'benchmark_trends'],
    timestamp='2026-07-01T00:00:00Z',
    uncertainty='Hardware scaling / energy constraints unresolved',
  )

  timeline.add_status(
    confidence_percent=28,
    evidence_tier='inferred',
    sources=['scaling_law_analysis', 'alignment_difficulty_evidence'],
    timestamp='2026-07-27T00:00:00Z',
    uncertainty='Alignment may be harder constraint than capability scaling',
  )

  print(f"Claim: {timeline.claim}")
  print(f"Confidence delta: {timeline.delta():+d}pp")
  print(f"\nTimeline:")
  for status in timeline.statuses:
    print(f"  {status.timestamp}: {status.confidence_percent}% ({status.evidence_tier})")
    if status.uncertainty:
      print(f"    Uncertainty: {status.uncertainty}")
