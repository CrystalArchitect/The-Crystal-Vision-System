# H2 immutable final test (V0.1)

**Status:** GOVERNANCE step 5 recorded · dual-gate evaluated at 1M · no extra claims

## Interpretation Boundary

This report does **not** demonstrate:

- Language-model quality (synthetic associative-memory encoder only)
- Hardware bandwidth or dollar cost (analytical fp32 element counts only)
- CrystalCore production quality, Optimus-relevance, or an xAI-relevant advantage
- Anything about H1
- Non-local, dimensional, or brain-to-brain information transfer
- That a failed or passed 1M gate on this encoder transfers to any other task

The dual gate is evaluated **only** on the 1M-token final-partition subset.
Shorter lengths are a scaling record, not the gate. Candidates were scored
independently against the dense reference. Production `core/` unmodified.

n = 1000 items per length, lengths = [32768, 65536, 131072, 262144, 524288, 1048576].
Generator: final seed family (unsealed for this run only).

Dense reference gold accuracy (all lengths): 1.0000.
Dense reference gold accuracy at 1M: 1.0000.

Compute envelope: reference 2504.9s; A 3443.8s; B 2452.1s. Not a dollar BOM.

## Dual-gate at 1M (locked hypothesis)

LCB(Q_primitive / Q_full) ≥ 0.9 **and** BW_primitive / BW_full ≤ 0.4, simultaneously.

- Candidate A: **FAIL (quality LCB 0.9800 ≥ 0.9; BW/ref 0.5638 > 0.4)**
- Candidate B: **FAIL (quality LCB 0.9800 ≥ 0.9; BW/ref 0.5614 > 0.4)**

## Frozen configs under test

- Dense reference: full attention
- Candidate A: `{'block_size': 512, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 32, 'selection_frequency': 'every_layer'}`
- Candidate B: `{'leaf_block': 512, 'summary_levels': 2, 'retrieved_blocks': 32, 'refinement_stages': 2, 'group_size': 4}`

## Per-length record

| length | ref acc | A agree | A Q-LCB | A BW/ref | B agree | B Q-LCB | B BW/ref |
|---|---|---|---|---|---|---|---|
| 32768 | 1.0000 | 1.0000 | 1.0000 | 0.7914 | 1.0000 | 1.0000 | 0.7790 |
| 65536 | 1.0000 | 0.9990 | 0.9970 | 0.6763 | 0.9990 | 0.9970 | 0.6667 |
| 131072 | 1.0000 | 0.9980 | 0.9950 | 0.6168 | 0.9980 | 0.9950 | 0.6106 |
| 262144 | 1.0000 | 0.9930 | 0.9880 | 0.5866 | 0.9930 | 0.9880 | 0.5825 |
| 524288 | 1.0000 | 0.9950 | 0.9900 | 0.5714 | 0.9940 | 0.9890 | 0.5685 |
| 1048576 | 1.0000 | 0.9870 | 0.9800 | 0.5638 | 0.9870 | 0.9800 | 0.5614 |

Machine record: `summary.json`. Item-level rows: `reference.json`,
`candidate_a.json`, `candidate_b.json`.

H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven
until a separate, later decision — not implied by this gate.
External / xAI pitch remains Hold unless the steward changes it.
