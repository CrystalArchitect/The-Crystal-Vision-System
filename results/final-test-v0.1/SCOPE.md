# Scope of the H2 immutable final test (V0.1)

## Interpretation Boundary

This record does **not** demonstrate:

- Language-model quality (synthetic associative-memory encoder only)
- Hardware bandwidth or dollar cost (analytical fp32 element counts only)
- CrystalCore production quality, Optimus-relevance, or an xAI-relevant advantage
- Anything about H1
- Non-local, dimensional, or brain-to-brain information transfer
- That a quality-side pass on this encoder transfers to any other task
- That a bandwidth-side fail would reverse under a different byte-count model

The dual gate is evaluated **only** at 1M tokens on the final partition.
Shorter lengths are a scaling record, not the gate. Production `core/` unmodified.

## Dual-gate decision (1M, n = 1000)

Locked hypothesis: LCB(Q_primitive / Q_full) ≥ 0.90 **and**
BW_primitive / BW_full ≤ 0.40, simultaneously.

| system | quality LCB | quality | BW/ref | bandwidth | dual-gate |
|---|---|---|---|---|---|
| Candidate A | 0.9800 | pass | 0.5638 | fail | **fail** |
| Candidate B | 0.9800 | pass | 0.5614 | fail | **fail** |

Dense reference gold accuracy at 1M: 1.000.

Neither candidate satisfies both conditions at once. GOVERNANCE step 6 is
therefore **fail** for both frozen configs on this encoder and this protocol.

A quality-only reading is not a pass. A bandwidth-only reading is not a pass.
The gate is simultaneous.
