"""
Record — Immutable Chronicle Entries (ARCHIVE + CHRONICLE registers)

Creates a point-in-time record of a claim's evidence status.
Records are append-only and immutable; new evidence = new record with timestamp.

This prevents historical rewriting and preserves evolution of understanding.
"""

from typing import NamedTuple, Optional, Dict
from datetime import datetime, timezone
from .mirror import mirror, MirrorResult
from .latency import latency_map, LatencyMap


class ChronicleEntry(NamedTuple):
  """An immutable record of a claim's status at a point in time."""
  timestamp: str  # ISO8601 UTC
  claim: str
  statement_type: str  # 'observation' | 'evidence' | 'interpretation' | 'vision'
  status: str  # 'measurement' | 'hypothesis' | 'proposed' | 'unknown'
  confidence: str  # 'unknown' | 'low' | 'medium' | 'high'
  evidence_state: str  # 'none' | 'developing' | 'established'
  latencies: Dict[str, str]  # Gap inventory at time of recording
  uncertainties: list  # What remains unknown
  future_review: bool  # Should this be revisited?
  review_trigger: Optional[str]  # What would trigger review


def chronicle(
  mirror_result: MirrorResult,
  latency_result: LatencyMap,
  timestamp: Optional[str] = None,
) -> ChronicleEntry:
  """
  Create an immutable Chronicle entry for a claim.

  Args:
    mirror_result: Output from mirror() decomposition
    latency_result: Output from latency_map()
    timestamp: ISO8601 UTC (default: now)

  Returns:
    ChronicleEntry recording evidence status at this moment

  Invariants:
    - confidence is orthogonal to latency (both recorded separately)
    - status is fixed; understanding evolution = new entry
    - uncertainties are explicitly named
  """

  if timestamp is None:
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

  # Determine confidence based on classification
  classification = mirror_result.classification
  if classification['confidence'] == 'high':
    confidence = 'high'
  elif classification['confidence'] == 'medium':
    confidence = 'medium'
  elif classification['confidence'] == 'low':
    confidence = 'low'
  else:
    confidence = 'unknown'

  # Determine status based on type
  statement_type = classification['type']
  if statement_type == 'observation':
    status = 'measurement'
    evidence_state = 'established'
  elif statement_type == 'evidence':
    status = 'measurement'
    evidence_state = 'established'
  elif statement_type == 'interpretation':
    status = 'hypothesis'
    evidence_state = 'developing'
  elif statement_type == 'vision':
    status = 'proposed'
    evidence_state = 'none'
  else:
    status = 'unknown'
    evidence_state = 'unknown'

  # Should this be revisited?
  future_review = statement_type in ['interpretation', 'vision']
  if future_review:
    highest_latency = latency_result.highest_latency
    review_trigger = f"When {highest_latency}_latency drops below 'high'"
  else:
    review_trigger = None

  entry = ChronicleEntry(
    timestamp=timestamp,
    claim=mirror_result.statement,
    statement_type=statement_type,
    status=status,
    confidence=confidence,
    evidence_state=evidence_state,
    latencies=latency_result.latencies,
    uncertainties=mirror_result.components.get('uncertainties', []),
    future_review=future_review,
    review_trigger=review_trigger,
  )

  return entry


def chronicle_entry_to_dict(entry: ChronicleEntry) -> dict:
  """Convert ChronicleEntry to dict for JSON serialization."""
  return {
    'timestamp': entry.timestamp,
    'claim': entry.claim,
    'type': entry.statement_type,
    'status': entry.status,
    'confidence': entry.confidence,
    'evidence_state': entry.evidence_state,
    'latencies': entry.latencies,
    'uncertainties': entry.uncertainties,
    'future_review': entry.future_review,
    'review_trigger': entry.review_trigger,
  }


if __name__ == '__main__':
  # Example usage
  from .mirror import mirror
  from .latency import latency_map

  claim = "AI will create an age of abundance within five years"

  # Decompose and analyze
  mirror_result = mirror(claim)
  latency_result = latency_map(claim)

  # Create Chronicle entry
  entry = chronicle(mirror_result, latency_result)

  print(f"Chronicle Entry for: {claim}\n")
  print(f"Timestamp: {entry.timestamp}")
  print(f"Type: {entry.statement_type}")
  print(f"Status: {entry.status}")
  print(f"Confidence: {entry.confidence}")
  print(f"Evidence state: {entry.evidence_state}")
  print(f"Highest latency: {latency_result.highest_latency}")
  print(f"Future review: {entry.future_review}")
  if entry.review_trigger:
    print(f"Review trigger: {entry.review_trigger}")
