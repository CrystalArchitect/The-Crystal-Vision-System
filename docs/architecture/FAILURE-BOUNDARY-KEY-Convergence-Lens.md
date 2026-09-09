# Failure Boundary Key — Convergence Lens Safety Architecture

**Status**: LOCKED  
**Version**: 0.1.0  
**Date**: 2026-07-27

## Purpose

Establish the boundary between normal operation and fail-closed enforcement. When any of the five CONSTITUTION invariants are violated, the system stops processing immediately and escalates to governance. No automatic recovery.

## Core Principle

**Fail-closed, not fail-safe.** When in doubt, stop and wait for human decision. A false negative (rejecting valid work) is tolerable; a false positive (admitting invalid work) is not.

---

## Invariant Violations (Trigger Failure Boundary)

### Violation 1: Vision Observation Conflict

**Trigger**: A claim classified as 'vision' has a non-null observation field.

```python
if classification.type == 'vision' and components['observation'] is not None:
    → HALT
    → LOG: "Invariant 1 violated: vision claims cannot have observations"
    → ESCALATE: governance_view
```

**Action**: Claim is rejected; source reliability flag incremented. If source is Clementine, governance is alerted.

---

### Violation 2: Interpretation Evidence Clarity

**Trigger**: A claim classified as 'interpretation' does not use hedging language AND is stored as certainty.

```python
hedging_words = ['suggests', 'may', 'might', 'could', 'appears', 'seems', 'possibly']
if classification.type == 'interpretation' and not any(word in statement.lower() for word in hedging_words):
    if status != 'hypothesis':
        → HALT
        → LOG: "Invariant 2 violated: interpretation stored without hedging"
        → ESCALATE: governance_view
```

**Action**: Claim is queued for governance review. Not admitted until human approves hedging or reclassification.

---

### Violation 3: Confidence Not Authority

**Trigger**: Confidence level is used to suppress evidence latency requirements OR to skip validation gates.

```python
if confidence == 'high' and evidence_state == 'none':
    # High confidence but no evidence — attempt to bypass validation
    → HALT
    → LOG: "Invariant 3 violated: confidence used to suppress validation"
    → ESCALATE: governance_view
```

**Action**: Claim rejected; confidence and latency are re-evaluated independently. Source is flagged for confidence inflation.

---

### Violation 4: Disagreement Preservation

**Trigger**: System attempts to delete, merge, or suppress incompatible claims that both passed validation.

```python
if claim_A.status == claim_B.status and contradicts(claim_A, claim_B):
    if operation in ['delete', 'merge', 'suppress']:
        → HALT
        → LOG: "Invariant 4 violated: attempt to erase valid disagreement"
        → ESCALATE: governance_view
```

**Action**: Operation is blocked. Both claims remain in CHRONICLE. Governance is notified of conflict.

---

### Violation 5: Category Drift Detection

**Trigger**: A claim's classification type changes after initial admission, OR a 'vision' claim is later stored as 'observation'.

```python
if stored_claim.classification.type != current_classification.type:
    if stored_claim.id == current_claim.id:  # Same claim, different type
        → HALT
        → LOG: "Invariant 5 violated: category drift on existing claim"
        → ESCALATE: governance_view
```

**Action**: The new classification is rejected. Original claim remains in CHRONICLE with its original type. Submitter is flagged for reclassification attempt.

---

## Failure Log Structure

When a violation is detected, a **FailureRecord** is created:

```python
{
  "timestamp": ISO8601,
  "violation_type": int,              # 1–5 (which invariant)
  "severity": "critical",
  "claim_id": str,                    # claim that triggered it
  "source_origin": str,               # where the claim came from
  "message": str,                     # human-readable description
  "context": dict,                    # full claim data
  "escalation_target": "governance_view",
  "action_taken": str,                # "rejected" | "queued_for_review" | "blocked"
  "can_retry": bool,                  # false for invariant violations
  "governance_decision_required": bool
}
```

All FailureRecords are written to an immutable **failure_log** that governance can query. They are never deleted.

---

## System Halting Behavior

When a violation is detected:

1. **Processing stops immediately** — no further claims are processed until resolved
2. **Affected transaction is rolled back** — the claim is NOT admitted to MIRROR or CHRONICLE
3. **Governance is alerted** — if human oversight is required
4. **Source is flagged** — reliability metrics are updated
5. **Failure is recorded** — added to immutable failure_log

The system does **not** attempt to "fix" the violation automatically. No auto-repair, no defaults, no inference.

---

## Recovery Procedures

### Scenario A: Violation is a False Positive (Rule Too Strict)

1. Governance reviews the FailureRecord
2. Governance submits a Constitution Amendment request
3. System does not admit new claims until amendment is processed
4. Amendment is voted on by Constitution council (out of scope here)
5. Once approved, system resumes with updated rules

### Scenario B: Violation is Legitimate (Bad Claim)

1. Governance reviews the FailureRecord
2. Source is contacted (if applicable)
3. Source resubmits claim with corrections or different classification
4. System processes corrected claim through normal validation
5. Original FailureRecord is linked to the corrected version in CHRONICLE

### Scenario C: Violation is Source Misbehavior

1. Governance reviews source reliability metrics
2. Source is demoted to lower quality tier
3. All future claims from source require pre-approval
4. If source is Clementine, integration is paused pending investigation

**There is no "auto-recovery" mode.** All recovery requires explicit governance action.

---

## Safety Limits (Hard Caps)

| Limit | Value | Trigger |
|-------|-------|---------|
| Max claims from single source per day | 1000 | Rate limit applied; further claims queued |
| Max violations per source per week | 10 | Source demoted; requires governance approval |
| Max failed validations before escalation | 5 consecutive | Governance review mandatory |
| Failure log retention | Never deleted | Immutable archive |
| Halt duration (max) | Depends on governance | No automatic resume |

---

## Clementine-Specific Safety Rules

Clementine claims that violate invariants:
1. Are logged in failure_log with source_origin = "clementine"
2. Do **not** proceed to MIRROR decomposition
3. Trigger governance alert (email + dashboard notification)
4. Are queued for governance review (may be approved with modifications)
5. Are tracked in Clementine's reliability metrics

If Clementine violation rate exceeds 10% over 7 days, Clementine ingestion is **paused** until governance resolves the root cause.

---

## Testing Strategy (Parallel Track)

The Failure Boundary can be validated in isolation:

```python
# Test each violation independently
test_violation_1_vision_observation()      # ✓
test_violation_2_interpretation_clarity()  # ✓
test_violation_3_confidence_not_authority() # ✓
test_violation_4_disagreement_preserved()  # ✓
test_violation_5_category_drift()          # ✓

# Test under load
test_concurrent_violations_50_qps()        # concurrent load
test_failure_log_writes_under_stress()     # logging performance
test_governance_escalation_latency()       # alert timing

# Test recovery paths
test_source_demotion_flow()
test_violation_retry_with_fix()
test_halt_resume_sequence()
```

All tests must pass before Failure Boundary is locked.

---

## Success Criteria

Failure Boundary Key is locked when:
- ✓ All 5 invariant violations are detectable and halt processing immediately
- ✓ Failure log is immutable and governance-queryable
- ✓ System does not auto-recover; only governance can resume
- ✓ Clementine violations trigger governance alerts
- ✓ Rate limits prevent DoS via invalid claims
- ✓ Under load (50 qps), violations are detected <100ms
- ✓ Recovery procedures are documented and testable
