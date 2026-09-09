"""
Mirror — Statement Decomposition (MIRROR register)

Reflects a claim back in its component parts:
- observation: What was directly measured?
- evidence_required: What evidence would support this?
- interpretation: What meaning is assigned?
- vision: What future possibility is proposed?
- uncertainties: What remains unknown?

This is the core MIRROR capability from the architecture blueprint.
"""

from typing import NamedTuple, List, Optional
from .classify import classify


class MirrorResult(NamedTuple):
  """Complete decomposition of a statement."""
  statement: str
  classification: dict  # {'type': ..., 'confidence': ..., 'reason': ...}
  components: dict  # observation, evidence_required, interpretation, vision, uncertainties


def mirror(claim: str) -> MirrorResult:
  """
  Decompose a claim into its constituent parts.

  Args:
    claim: A statement to decompose

  Returns:
    MirrorResult with classification and all five components

  Invariants (enforced):
    - If type is 'vision', observation must be null
    - If type is 'observation', interpretation should be minimal
    - All uncertainties must be explicitly named
  """

  classification = classify(claim)

  # Decompose based on type
  observation = None
  evidence_required = []
  interpretation = None
  vision = None
  uncertainties = []

  if classification.type == 'observation':
    # Measured fact
    observation = claim
    interpretation = None
    vision = None
    evidence_required = []
    uncertainties = ['Generalization beyond this measurement', 'Causation vs correlation']

  elif classification.type == 'evidence':
    # Data-backed statement
    observation = None
    interpretation = "Evidence is cited; specific conclusion unclear without context"
    evidence_required = []
    vision = None
    uncertainties = ['Interpretation of evidence', 'Applicability to other domains']

  elif classification.type == 'interpretation':
    # Meaning assigned to evidence
    observation = None
    evidence_required = [
      'Direct measurement of the phenomenon',
      'Comparison to baseline or control',
      'Reproducibility across contexts',
    ]
    interpretation = claim
    vision = None
    uncertainties = [
      'Evidence availability',
      'Measurement method',
      'Generalization',
    ]

  elif classification.type == 'vision':
    # Future-oriented claim
    observation = None
    evidence_required = [
      'Clear definition of success metrics',
      'Current capability measurement',
      'Trend analysis or roadmap',
    ]
    interpretation = None  # No interpretation of current data
    vision = claim
    uncertainties = [
      'Time to achievement',
      'Resource requirements',
      'Coordinating actors',
      'Defining success',
    ]

  result_dict = {
    'statement': claim,
    'classification': {
      'type': classification.type,
      'confidence': classification.confidence,
      'reason': classification.reason,
    },
    'components': {
      'observation': observation,
      'evidence_required': evidence_required,
      'interpretation': interpretation,
      'vision': vision,
      'uncertainties': uncertainties,
    }
  }

  return MirrorResult(
    statement=claim,
    classification=result_dict['classification'],
    components=result_dict['components'],
  )


if __name__ == '__main__':
  # Example usage
  test_claims = [
    "AI will create an age of abundance within five years",
    "On 2026-07-27, LLM X scored 95 on benchmark Y",
    "Recent research suggests scaling laws may continue",
  ]

  print("Mirror Decomposition Examples:\n")
  for claim in test_claims:
    result = mirror(claim)
    print(f"Statement: {result.statement}")
    print(f"Classification: {result.classification['type']}")
    print(f"Components:")
    for key, value in result.components.items():
      if value:
        print(f"  {key}: {value}")
    print()
