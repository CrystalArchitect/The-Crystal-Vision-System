# Convergence Lens v0.1 — Prototype Contract

**Purpose:** Verify that meaning integrity rules can be enforced before adding intelligence.

**Approach:** Test-first. Define invariants that MUST hold. Implement only what's needed to pass them.

---

## Module Contract

```
src/crystal-core/convergence_lens/
├── __init__.py
├── classify.py        # Identify layer type
├── mirror.py          # Separate claim components  
├── latency.py         # Identify uncertainty gaps
├── record.py          # Create Chronicle/Archive entries
└── selftest.py        # Verify invariants (runs first)
```

---

## Capability 1: MIRROR — Statement Decomposition

**Input:**
```
"AI will create an age of abundance within five years."
```

**Output:**
```json
{
  "statement": "AI will create an age of abundance within five years",
  "classification": {
    "type": "vision",
    "reason": "future-oriented prediction without evidence"
  },
  "components": {
    "observation": null,
    "evidence_required": [
      "AI capability measurements",
      "economic impact data", 
      "resource availability"
    ],
    "interpretation": "AI may reduce intelligence scarcity",
    "vision": "Age of abundance (defined as: ...)",
    "uncertainties": [
      "deployment speed",
      "energy constraints", 
      "governance outcomes"
    ]
  }
}
```

**Rules:**
- If type is "vision", observation MUST be null
- If type is "observation", evidence_required MUST be empty
- interpretation field must explicitly name what meaning is assigned
- uncertainties field must list what remains unknown

---

## Capability 2: LATENCY MAP — Gap Inventory

**Input:**
Same claim as MIRROR

**Output:**
```json
{
  "claim": "AI will create an age of abundance within five years",
  "latencies": {
    "knowledge_latency": "medium",
    "technology_latency": "medium", 
    "resource_latency": "high",
    "coordination_latency": "high",
    "trust_latency": "high"
  },
  "highest_latency": "coordination",
  "would_shift_if": {
    "knowledge": "Clear metrics for 'abundance' defined + measured",
    "technology": "AI systems demonstrate capability at scale",
    "resource": "Energy/compute scaling path shown",
    "coordination": "Multi-actor governance framework exists",
    "trust": "Independent verification mechanisms proven"
  }
}
```

**Latency levels:** low (resolved) | medium (resolvable) | high (unresolved)

**Rules:**
- Latencies are gaps, not probabilities
- High latency ≠ low probability (they're orthogonal)
- would_shift_if describes what evidence would reduce each gap
- One latency can be resolved while others remain high

---

## Capability 3: CHRONICLE — Meaning-Preserving Records

**Input:**
Mirror result + Latency map

**Output:**
```json
{
  "date": "2026-07-27T09:30:00Z",
  "claim": "AI will create an age of abundance within five years",
  "type": "vision",
  "interpretation": "AI may reduce intelligence scarcity",
  "status": "hypothesis",
  "evidence_state": "developing",
  "confidence": "unknown",
  "latencies": {
    "knowledge": "medium",
    "technology": "medium",
    "resource": "high",
    "coordination": "high",
    "trust": "high"
  },
  "future_review": true,
  "review_trigger": "When coordination latency drops below 'high'"
}
```

**Rules:**
- confidence MUST be one of: "unknown" | "low" | "medium" | "high"
- confidence MUST NOT be confused with probability
- status MUST NOT change meaning (hypothesis ≠ fact)
- future_review indicates whether new evidence would shift interpretation
- Record is immutable; changes = new entry with timestamp

---

## Invariant Tests (selftest.py)

These MUST fail if the rules are broken:

### Test 1: Vision Cannot Impersonate Evidence
```python
def test_vision_observation_conflict():
  """Vision-type statements must have null observation."""
  claim = "AI will create abundance by 2030"
  result = mirror(claim)
  
  assert result['classification']['type'] == 'vision'
  assert result['components']['observation'] is None
  
  # This should FAIL (raise ValueError):
  result['components']['observation'] = "observed on 2026-07-27"
  assert_invariant_violated("vision cannot claim observation")
```

### Test 2: Interpretation Cannot Impersonate Observation
```python
def test_interpretation_evidence_clarity():
  """Interpretation must be named explicitly, separate from observation."""
  claim = "AI is becoming more capable"
  result = mirror(claim)
  
  assert result['components']['observation'] is None
  assert result['components']['interpretation'] is not None
  assert "may" in result['components']['interpretation'].lower() or \
         "could" in result['components']['interpretation'].lower()
  
  # Must use hedging language:
  bad_interpretation = "AI is more capable (stated as fact)"
  assert_invariant_violated("interpretation cannot claim certainty")
```

### Test 3: Confidence Cannot Replace Verification
```python
def test_confidence_not_authority():
  """High confidence in low-evidence claim is not verification."""
  claim = "I am very confident AI will achieve AGI by 2030"
  
  result = mirror(claim)
  latency = latency_map(claim)
  record = chronicle(claim)
  
  # Confidence field exists but is separate from latency:
  assert record['confidence'] in ['unknown', 'low', 'medium', 'high']
  assert latency['latencies']['knowledge_latency'] in ['low', 'medium', 'high']
  
  # High confidence does NOT reduce latency:
  record['confidence'] = 'high'
  latency['latencies']['knowledge_latency'] = 'high'
  assert record['confidence'] != latency['latencies']['knowledge_latency']
  
  print("PASS: Confidence and verification are orthogonal")
```

### Test 4: Disagreement Preservation
```python
def test_disagreement_can_coexist():
  """Two incompatible interpretations can exist in Chronicle without forced consensus."""
  claim_a = "Scaling laws will continue"
  claim_b = "Scaling laws plateau by 2027"
  
  record_a = chronicle(mirror(claim_a))
  record_b = chronicle(mirror(claim_b))
  
  # Both records exist, with their own latency maps:
  assert record_a['status'] == 'hypothesis'
  assert record_b['status'] == 'hypothesis'
  
  # No field attempts to merge them or declare winner:
  assert 'consensus' not in record_a
  assert 'consensus' not in record_b
  
  print("PASS: Disagreement preserved without collapse")
```

### Test 5: Category Confusion Detection
```python
def test_category_drift_detection():
  """Catch attempts to misclassify claim types."""
  
  # Observation trying to become interpretation:
  obs = mirror("On 2026-07-27, LLM X scored 95 on benchmark Y")
  assert obs['classification']['type'] == 'observation'
  
  # Cannot retroactively claim this is a vision:
  obs['classification']['type'] = 'vision'
  assert_invariant_violated("cannot change observation to vision")
  
  # Vision trying to become fact:
  vision = mirror("AI will transform society")
  assert vision['classification']['type'] == 'vision'
  
  vision['components']['observation'] = "observed transformation"
  assert_invariant_violated("vision cannot claim observation")
  
  print("PASS: Category drift detection working")
```

---

## Success Criteria for v0.1

✅ MIRROR correctly decomposes claims into five components

✅ LATENCY MAP identifies gaps without declaring probability

✅ CHRONICLE preserves records without declaring truth

✅ All five invariant tests pass

✅ No path exists to convert vision→evidence, interpretation→fact, or confidence→authority

After v0.1 passes these tests, integration points:

- ARCHIVE stores Chronicle entries
- Clementine reads Mirror/Latency/Chronicle results
- CrystalCore.OS CONSTITUTION enforces these rules across all uses
- Future FORGE capability tests scenarios against invariants

---

## Implementation Order

1. **selftest.py** — Define invariants first
2. **classify.py** — Identify statement type
3. **mirror.py** — Decompose components
4. **latency.py** — Map gaps
5. **record.py** — Create Chronicle entries
6. **__init__.py** — Export clean API

Do not write API before tests pass. Do not add intelligence before integrity is proven.

---

*Non Solus.*
