"""
Latency — Uncertainty Gap Inventory (LOOM register)

Identifies what kinds of gaps exist:
- knowledge_latency: What do we not yet know?
- technology_latency: What could we build but haven't?
- resource_latency: What requires investment?
- coordination_latency: What needs alignment?
- trust_latency: What would make this credible?

Latencies are not probabilities. High latency means high uncertainty,
which is orthogonal to likelihood or desirability.
"""

from typing import NamedTuple, Dict, Optional


class LatencyMap(NamedTuple):
  """Inventory of gaps for a claim."""
  claim: str
  latencies: Dict[str, str]  # 'low' | 'medium' | 'high'
  highest_latency: Optional[str]
  would_shift_if: Dict[str, str]  # What evidence would reduce each gap


def latency_map(claim: str) -> LatencyMap:
  """
  Identify uncertainty gaps in a claim.

  Args:
    claim: A statement to analyze

  Returns:
    LatencyMap with gap types and their severity

  Latency levels:
    - low: Gap is largely resolved, minimal uncertainty
    - medium: Gap is resolvable with available methods, realistic effort
    - high: Gap is unresolved, requires new evidence or technology
  """

  claim_lower = claim.lower()

  # Determine latencies based on claim content
  latencies = {
    'knowledge_latency': 'medium',
    'technology_latency': 'medium',
    'resource_latency': 'medium',
    'coordination_latency': 'medium',
    'trust_latency': 'medium',
  }

  would_shift_if = {
    'knowledge': 'Clear metrics defined and measured',
    'technology': 'Prototype demonstrates capability at scale',
    'resource': 'Energy/cost scaling path shown',
    'coordination': 'Multi-actor governance framework agreed',
    'trust': 'Independent verification mechanisms proven',
  }

  # Adjust based on claim characteristics
  if 'abundance' in claim_lower or 'transform' in claim_lower:
    # High ambiguity in definition
    latencies['knowledge_latency'] = 'high'
    would_shift_if['knowledge'] = 'Specific definition of "abundance" with measurable criteria'

  if '203' in claim_lower or 'five years' in claim_lower:
    # Near-term future claims have high technology latency
    latencies['technology_latency'] = 'high'
    would_shift_if['technology'] = 'Current capability gap < time to achievement measured'

  if 'will' in claim_lower or 'inevitable' in claim_lower:
    # Future claims require coordination
    latencies['coordination_latency'] = 'high'
    would_shift_if['coordination'] = 'Multi-actor alignment on deployment path'

  if 'uncertainty' in claim_lower or 'uncertain' in claim_lower:
    # Explicitly uncertain claims need evidence
    latencies['knowledge_latency'] = 'high'
    would_shift_if['knowledge'] = 'Empirical resolution of the stated uncertainty'

  # Highest latency determines what to focus on first
  highest = max(latencies.items(), key=lambda x: (
    {'high': 3, 'medium': 2, 'low': 1}[x[1]]
  ))[0]

  return LatencyMap(
    claim=claim,
    latencies=latencies,
    highest_latency=highest.replace('_latency', ''),
    would_shift_if=would_shift_if,
  )


if __name__ == '__main__':
  # Example usage
  test_claims = [
    "AI will create an age of abundance within five years",
    "Scaling laws will continue for the next decade",
    "We must coordinate on AI safety",
  ]

  print("Latency Map Examples:\n")
  for claim in test_claims:
    result = latency_map(claim)
    print(f"Claim: {claim}")
    print(f"Latencies:")
    for lat_type, level in result.latencies.items():
      short_name = lat_type.replace('_latency', '')
      print(f"  {short_name}: {level}")
    print(f"Highest: {result.highest_latency}")
    print(f"Would shift if: {result.would_shift_if[result.highest_latency]}")
    print()
