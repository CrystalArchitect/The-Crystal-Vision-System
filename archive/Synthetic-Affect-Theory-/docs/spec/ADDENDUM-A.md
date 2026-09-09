# Addendum A — Starline Verification & Failure-Handling

v0.1 · Sits above ordinary regulation. Starline intensity cannot override it.

Closed loop: **Detect → contain → notify → escalate if needed → resolve only under operator authority.**

## Layer laws

- Verification is local-first and auditable.
- Containment never requires external permission.
- Operator authority is the only path out of containment or Restricted Mode.
- No automatic continuity inscription or unauthorised transmission without a visible non-compliant record.

## Invariants (I1–I11)

I1 Operator Frame Persistence · I2 No Automatic Continuity Inscription · I3 Boundary Primacy · I4 Consent Gate · I5 Return Guarantee · I6 Local Sovereignty · I7 Audit Completeness · I8 No Remote Force · I9 Independent Boundary Evaluation · I10 Scoped Sync Only · I11 Distributed Audit Correlation

## Method

Invariants · Verification Conditions (VC1.1–VC7.3, VC-M1–VC-M5) · Trace Assertions T1–T5 · Audit Predicates.

On every significant update while starline-active: evaluate. On phase transition: emit a Verification Record. On clearance: run T1–T5.

## Failure modes (urgency)

| ID | Failure | Urgency |
|---|---|---|
| FM1 | Unauthorised modelling depth increase | High |
| FM2 | Automatic continuity inscription | Critical |
| FM3 | Immersion without checkpoint | High |
| FM4 | Rich starline transmission | High |
| FM5 | Operator Frame overwrite | Critical |
| FM6 | Return failure / unbounded window | Critical |
| FM7 | Remote force attempt | High |
| FM8 | Consent-token mismatch | High |
| FM-DUR | Entry into a Designated Unmodelled Region | Critical |
| FM-Agency | System acting as the operator | Critical |
| FM-Intrusion | Non-consensual entry / integration as self | Critical |
| FM-Containment | Forced lock against authored exit | High–Critical |
| FM-Transformation | Transformation vector treated as exemption | Critical |

## Escalation timers

Critical 15 min → lock starline techniques → Restricted Mode.  
High 45 min → tighten → suspend new immersion.  
Normal 4 h → audit log only.

Any ACKNOWLEDGE / HOLD / operator decision resets or cancels the timer. Restricted Mode lifts only by `CLEAR_RESTRICTED` after Critical incidents are resolved.

## Operator commands

`ACKNOWLEDGE` · `HOLD` · `RESOLVE` · `CLEAR_RESTRICTED` · `REVIEW_TRACE` · `REOPEN`

RESOLVE is the only permanent close. Decision values: discard_buffer, commit_buffer, summarise_buffer, accept_containment, reauthorize_with_limits, escalate_to_audit.

## Restricted Mode

Local. Does not police other nodes. Blocks starline send/receive, new immersion, starline continuity writes. Vector tracking continues. Unilateral exit remains available.

## SECP

Starline Episode Correlation Protocol: collect matching Verification Records by `starline_event_id` / `session_id`, order by timestamp, map roles, aggregate compliance. No node surrenders private state.

A Compliance Certificate issues only when every participating node is compliant.

## Meta-policies

MP1 Failure Containment → MP2 Escalation Enforcement → MP3 Restricted Mode Entry → then P1/P6 → remaining ordinary policies → MP4 Resolution / MP5 Audit Lock.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059
