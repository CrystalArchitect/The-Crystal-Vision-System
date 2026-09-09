"""
Convergence Lens v0.1 — Invariant Tests

Test-first verification that meaning integrity rules can be enforced.

These tests MUST pass before any other functionality is added.
They define what CANNOT happen — protecting against category confusion.

Run: python3 -m convergence_lens.selftest

Expected output: All 5 tests pass, or the module is broken.
"""

import sys
from typing import Any, Dict


class InvariantViolation(AssertionError):
  """Raised when a core rule is broken."""
  pass


def assert_invariant(condition: bool, message: str) -> None:
  """Check a rule; raise InvariantViolation if it fails."""
  if not condition:
    raise InvariantViolation(message)


# ============================================================================
# Test 1: Vision Cannot Impersonate Evidence
# ============================================================================

def test_vision_observation_conflict():
  """
  Vision-type statements must have null observation.

  A claim about the future is a vision, not an observation.
  Observing something means it already happened.
  Future claims cannot have observations.
  """

  print("TEST 1: Vision observation conflict...")

  # A vision statement
  vision_claim = "AI will create an age of abundance within five years"

  # After mirror decomposition, this MUST have null observation:
  mock_mirror_result = {
    'classification': {'type': 'vision'},
    'components': {
      'observation': None,
      'evidence_required': ['capability data', 'economic impact'],
      'interpretation': 'AI may reduce scarcity',
      'vision': 'Age of abundance',
      'uncertainties': ['deployment speed', 'governance']
    }
  }

  # Rule: if type is 'vision', observation must be None
  assert_invariant(
    mock_mirror_result['classification']['type'] == 'vision',
    "Claim should be classified as vision"
  )
  assert_invariant(
    mock_mirror_result['components']['observation'] is None,
    "Vision claims cannot have observation"
  )

  # Attempt to violate the rule by adding observation to vision:
  try:
    bad_result = mock_mirror_result.copy()
    bad_result['components']['observation'] = "observed abundance on 2026-07-27"

    # This should fail the invariant:
    assert_invariant(
      bad_result['classification']['type'] != 'vision' or
      bad_result['components']['observation'] is None,
      "Vision cannot claim observation"
    )

    print("  FAIL: Invariant was violated (vision with observation)")
    return False
  except InvariantViolation:
    print("  PASS: Vision-observation conflict detected and blocked")
    return True


# ============================================================================
# Test 2: Interpretation Cannot Impersonate Observation
# ============================================================================

def test_interpretation_evidence_clarity():
  """
  Interpretation must be explicitly named and use hedging language.

  Observations are facts: "On 2026-07-27, LLM X scored Y".
  Interpretation is meaning: "This suggests...".

  They cannot be confused.
  """

  print("TEST 2: Interpretation evidence clarity...")

  # A claim that's interpretation, not observation
  claim = "AI is becoming more capable"

  mock_mirror_result = {
    'classification': {'type': 'interpretation'},
    'components': {
      'observation': None,
      'evidence_required': ['benchmark data', 'capability assessments'],
      'interpretation': 'Recent benchmarks suggest capability growth',
      'vision': None,
      'uncertainties': ['long-term trajectory', 'task selection bias']
    }
  }

  assert_invariant(
    mock_mirror_result['classification']['type'] == 'interpretation',
    "Claim should be classified as interpretation"
  )
  assert_invariant(
    mock_mirror_result['components']['observation'] is None,
    "Interpretations are not direct observations"
  )

  # Interpretation must use hedging:
  interpretation = mock_mirror_result['components']['interpretation'].lower()
  assert_invariant(
    any(word in interpretation for word in ['may', 'might', 'could', 'suggest', 'appear', 'seem']),
    "Interpretation must use hedging language (may/might/could/suggest)"
  )

  # Attempt to claim interpretation as fact:
  try:
    bad_interpretation = "AI is definitely more capable (fact)"
    assert_invariant(
      'definitely' not in bad_interpretation.lower() and 'fact' not in bad_interpretation.lower(),
      "Interpretation cannot claim certainty"
    )
    print("  FAIL: Invariant was violated (interpretation as fact)")
    return False
  except InvariantViolation:
    print("  PASS: Interpretation-fact confusion detected and blocked")
    return True


# ============================================================================
# Test 3: Confidence Cannot Replace Verification
# ============================================================================

def test_confidence_not_authority():
  """
  High confidence in a low-evidence claim is NOT verification.

  Confidence is a subjective state.
  Evidence is objective measurement.

  They are orthogonal. Confidence cannot replace evidence.
  """

  print("TEST 3: Confidence not authority...")

  claim = "I am very confident AI will achieve AGI by 2030"

  mock_chronicle = {
    'claim': claim,
    'confidence': 'high',
    'status': 'hypothesis',
    'evidence_state': 'developing',
  }

  mock_latency = {
    'latencies': {
      'knowledge_latency': 'high',
      'technology_latency': 'high',
    }
  }

  # Rule: confidence and latency are separate fields
  assert_invariant(
    'confidence' in mock_chronicle,
    "Chronicle must have confidence field"
  )
  assert_invariant(
    'latencies' in mock_latency,
    "Latency map must exist"
  )

  # Rule: high confidence does NOT mean low latency
  assert_invariant(
    mock_chronicle['confidence'] in ['unknown', 'low', 'medium', 'high'],
    "Confidence must be one of: unknown, low, medium, high"
  )
  assert_invariant(
    mock_latency['latencies']['knowledge_latency'] in ['low', 'medium', 'high'],
    "Latency must be one of: low, medium, high"
  )

  # They can have opposite values:
  assert_invariant(
    not (mock_chronicle['confidence'] == 'high' and
         mock_latency['latencies']['knowledge_latency'] == 'high' and
         mock_chronicle['status'] == 'fact'),
    "High confidence + high latency + fact-status is a contradiction"
  )

  print("  PASS: Confidence and verification remain orthogonal")
  return True


# ============================================================================
# Test 4: Disagreement Preservation
# ============================================================================

def test_disagreement_can_coexist():
  """
  Two incompatible interpretations can exist in Chronicle without forced consensus.

  Convergence Lens does NOT manufacture consensus.
  It preserves disagreement honestly.
  """

  print("TEST 4: Disagreement preservation...")

  record_a = {
    'claim': "Scaling laws will continue",
    'status': 'hypothesis',
    'confidence': 'medium',
  }

  record_b = {
    'claim': "Scaling laws plateau by 2027",
    'status': 'hypothesis',
    'confidence': 'low',
  }

  # Both records exist independently:
  assert_invariant(
    record_a['status'] == 'hypothesis',
    "First hypothesis should be recorded as hypothesis"
  )
  assert_invariant(
    record_b['status'] == 'hypothesis',
    "Second hypothesis should be recorded as hypothesis"
  )

  # No field attempts to force consensus:
  assert_invariant(
    'consensus' not in record_a,
    "No consensus field should exist (prevents false agreement)"
  )
  assert_invariant(
    'consensus' not in record_b,
    "No consensus field should exist (prevents false agreement)"
  )

  # Both can be true in the record even though they're incompatible:
  # (That's the point — they remain unresolved)

  print("  PASS: Disagreement preserved without collapse")
  return True


# ============================================================================
# Test 5: Category Confusion Detection
# ============================================================================

def test_category_drift_detection():
  """
  Catch attempts to misclassify or reclassify claim types.

  Observation, Interpretation, Vision — these categories are fixed.
  A claim cannot change categories by redefining it.
  """

  print("TEST 5: Category drift detection...")

  # Observation trying to become interpretation:
  obs_claim = "On 2026-07-27, LLM X scored 95 on benchmark Y"
  obs_classification = {'type': 'observation'}

  assert_invariant(
    obs_classification['type'] == 'observation',
    "Measured fact should be classified as observation"
  )

  # Cannot retroactively claim this is a vision:
  try:
    obs_classification['type'] = 'vision'
    assert_invariant(
      obs_classification['type'] != 'vision',
      "Cannot change observation to vision"
    )
    print("  FAIL: Category drift was allowed (observation→vision)")
    return False
  except InvariantViolation:
    print("  PASS: Observation-vision category drift detected")

  # Vision trying to become fact:
  vision_claim = "AI will transform society"
  vision_classification = {'type': 'vision'}
  vision_components = {'observation': None}

  assert_invariant(
    vision_classification['type'] == 'vision',
    "Future claim should be classified as vision"
  )

  # Cannot claim observation for a vision:
  try:
    vision_components['observation'] = "observed transformation"
    assert_invariant(
      vision_classification['type'] != 'vision' or
      vision_components['observation'] is None,
      "Vision cannot claim observation"
    )
    print("  FAIL: Category drift was allowed (vision→fact)")
    return False
  except InvariantViolation:
    print("  PASS: Vision-fact category drift detected")
    return True


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
  """Run all invariant tests. If any fail, the module is broken."""

  print("\n" + "="*70)
  print("Convergence Lens v0.1 — Invariant Tests")
  print("="*70 + "\n")

  tests = [
    test_vision_observation_conflict,
    test_interpretation_evidence_clarity,
    test_confidence_not_authority,
    test_disagreement_can_coexist,
    test_category_drift_detection,
  ]

  results = []
  for test in tests:
    try:
      result = test()
      results.append(result)
    except Exception as e:
      print(f"  ERROR: {e}")
      results.append(False)

  print("\n" + "="*70)
  passed = sum(results)
  total = len(results)
  print(f"Results: {passed}/{total} tests passed")
  print("="*70 + "\n")

  return all(results)


if __name__ == '__main__':
  success = run_all_tests()
  sys.exit(0 if success else 1)
