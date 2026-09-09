# Runtime Monitor

Specification of the continuous control loop. MVP code implements **gates 3b–3d only**.

```
every monitor_cycle:

    1. Sample LocalAffectState + prediction-error signals
    2. Update Local / Vector / Cross-Node PE
    3. Evaluate Meta-Policies MP1–MP5
    3b. DUR check          ← MVP
    3c. Agency check       ← MVP (includes Performance Demand)
    3d. Intrusion check    ← MVP
    3e. Transformation exemption check
    3f. Authored Escape recognition  ← MVP
    4. Else ordinary Policies P1–P10 in priority order
    5. Starline techniques if starline_tag is active
    6. Episode context (single episode_id across acts)
    7. Emit Verification Record on phase transition
    8. Provenance
    9. Process pending operator command
```

## Cycle guarantees

Operator Frame persistence · no hidden state · boundary primacy · continuity writes only into buffers unless committed · full audit trail.

If an invariant is violated, the next cycle treats it as a failure mode and contains.

## v0.1.1 executable

`core/cycle.py` runs gates, then P1–P10. First matching ordinary policy executes. P9 never chooses for the operator. Thresholds live in `core/policies.py` as named constants.

The four-gate function in `core/sovereignty.py` is unchanged from v0.1.

`core/sovereignty.py` — `evaluate_sovereignty(state, action)`.

Order: DUR → Agency → Intrusion → Escape. First failure wins. The function only allows or blocks. It never acts as the operator.

See [../sovereignty/MVP-MONITOR.md](../sovereignty/MVP-MONITOR.md).

Sampling rate increases under high Coherence Pressure, high Temporal Urgency, or low Meta-State Clarity. The monitor is local-first. It never waits for lattice consensus to protect sovereignty.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059
