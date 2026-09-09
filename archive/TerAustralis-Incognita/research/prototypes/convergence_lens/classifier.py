"""
Classifier: Statement decomposition (MIRROR register)

Separates claims into their component parts:
- Observation: What was directly measured/recorded?
- Evidence: What supports this claim?
- Interpretation: What meaning is assigned?
- Vision: What future possibility is imagined?

Example:
  claim = "AI systems will be superintelligent by 2030"
  result = classify(claim)

  result.observation = None (future claim, not measured yet)
  result.evidence = "Scaling laws, benchmark trends, compute growth"
  result.interpretation = "Current trends continue linearly to capability threshold"
  result.vision = "If true, autonomous systems exceed human capability in all domains"
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Classification:
  """Result of claim decomposition."""

  observation: Optional[str]
  """Directly measurable, timestamped, reproducible fact."""

  evidence: Optional[str]
  """Repeated observations, inference chains, prior work."""

  interpretation: Optional[str]
  """Meaning assigned to evidence; model or hypothesis."""

  vision: Optional[str]
  """Proposed future consistent with interpretation."""

  category: str
  """Label: 'observation' | 'evidence' | 'interpretation' | 'vision' | 'mixed'"""

  evidence_tier: str
  """Tier: 'direct' | 'measured' | 'inferred' | 'speculative'"""


def classify(claim: str) -> Classification:
  """
  Decompose a claim into observation / evidence / interpretation / vision.

  This is a placeholder. Real implementation would use:
  - NLP to parse claim structure
  - Knowledge base to identify what's measured vs. proposed
  - Category rules from CONSTITUTION

  Args:
    claim: A statement about current or future state

  Returns:
    Classification with all five components named
  """

  # Placeholder: minimal heuristic-based classification
  claim_lower = claim.lower()

  is_future = any(word in claim_lower for word in [
    'will', 'would', 'might', 'could', 'shall', 'by 20', 'future',
    'expect', 'predict', 'project'
  ])
  is_measured = any(word in claim_lower for word in [
    'measured', 'observed', 'found', 'showed', 'demonstrated',
    'on date', 'in 202', 'benchmark', 'test', 'score'
  ])

  if is_future:
    category = 'vision'
    evidence_tier = 'speculative'
    observation = None
  elif is_measured:
    category = 'observation'
    evidence_tier = 'direct'
  else:
    category = 'interpretation'
    evidence_tier = 'inferred'
    observation = None

  return Classification(
    observation=claim if category == 'observation' else None,
    evidence="[To be filled by caller]",
    interpretation=claim if category == 'interpretation' else None,
    vision=claim if category == 'vision' else None,
    category=category,
    evidence_tier=evidence_tier,
  )


if __name__ == '__main__':
  # Example usage
  claims = [
    "On 2026-07-27, LLM X scored 92% on benchmark Y",
    "AI systems are becoming more capable",
    "By 2030, AI will exceed human intelligence in all domains",
  ]

  for claim in claims:
    result = classify(claim)
    print(f"\nClaim: {claim}")
    print(f"  Category: {result.category}")
    print(f"  Evidence tier: {result.evidence_tier}")
    print(f"  Observation: {result.observation}")
    print(f"  Interpretation: {result.interpretation}")
    print(f"  Vision: {result.vision}")
