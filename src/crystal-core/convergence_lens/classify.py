"""
Classify — Identify statement type and evidence tier

Categorizes claims into: observation, evidence, interpretation, vision.

Each category has different rules:
- Observation: must be timestamped, measurable, reproducible
- Evidence: chains of reasoning or repeated observations
- Interpretation: meaning assigned to evidence
- Vision: speculative future possibility

This module enforces the MIRROR layer's type classification.
"""

from typing import NamedTuple


class Classification(NamedTuple):
  """Result of statement classification."""
  type: str  # 'observation' | 'evidence' | 'interpretation' | 'vision'
  confidence: str  # 'high' | 'medium' | 'low' | 'unknown'
  reason: str  # Why this classification was chosen


def classify(claim: str) -> Classification:
  """
  Identify what type of statement this is.

  Args:
    claim: A statement to classify

  Returns:
    Classification with type, confidence, and reasoning

  Rules:
    - If claim contains past-tense measured facts → observation
    - If claim cites evidence or data → evidence
    - If claim interprets without observation → interpretation
    - If claim is future-oriented without evidence → vision
  """

  claim_lower = claim.lower()

  # Check for future indicators
  future_words = ['will', 'would', 'shall', 'by 203', 'by 204', 'future', 'expect', 'predict']
  is_future = any(word in claim_lower for word in future_words)

  # Check for past/measured indicators
  measured_words = ['observed', 'measured', 'scored', 'showed', 'benchmark', 'on 202', 'date', 'found']
  is_measured = any(word in claim_lower for word in measured_words)

  # Check for evidence language
  evidence_words = ['data', 'evidence', 'research', 'study', 'found that', 'shows', 'demonstrated']
  cites_evidence = any(word in claim_lower for word in evidence_words)

  # Check for interpretation language
  interpretation_words = ['suggests', 'indicates', 'implies', 'may', 'might', 'could', 'appear', 'seem']
  uses_interpretation = any(word in claim_lower for word in interpretation_words)

  # Classify
  if is_measured:
    return Classification(
      type='observation',
      confidence='high',
      reason='Contains past-tense measured data or benchmarks'
    )

  if cites_evidence:
    return Classification(
      type='evidence',
      confidence='medium',
      reason='Cites data, research, or measurement'
    )

  if is_future:
    return Classification(
      type='vision',
      confidence='low',
      reason='Future-oriented claim without current measurement'
    )

  if uses_interpretation:
    return Classification(
      type='interpretation',
      confidence='medium',
      reason='Assigns meaning without direct observation'
    )

  # Default
  return Classification(
    type='interpretation',
    confidence='unknown',
    reason='Classification uncertain; claim requires context'
  )


if __name__ == '__main__':
  # Test cases
  test_claims = [
    "On 2026-07-27, LLM X scored 95 on benchmark Y",
    "Research shows that scaling laws hold over this range",
    "AI will create abundance within five years",
    "This suggests that capability growth may continue",
    "Superintelligence is inevitable",
  ]

  print("Classification Examples:\n")
  for claim in test_claims:
    result = classify(claim)
    print(f"Claim: {claim}")
    print(f"  Type: {result.type} (confidence: {result.confidence})")
    print(f"  Reason: {result.reason}\n")
