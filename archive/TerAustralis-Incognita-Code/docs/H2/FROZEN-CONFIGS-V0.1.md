# H2 V0.1 — Frozen configurations

**Status:** GOVERNANCE step 4 recorded · 2026-08-23  
**Not a 1M dual-gate decision. No performance claims.**

One config per candidate. Selected independently from each candidate’s own
validation record (`results/validation-v0.1/`). Candidate B’s freeze does not
use Candidate A’s scores.

## Interpretation Boundary

This freeze does **not** demonstrate:

- A 1M-token result, nor a dual-gate pass or fail
- Language-model quality (synthetic associative-memory encoder only)
- Hardware bandwidth (analytical fp32 element counts only)
- That the frozen config is “best” outside the validation partition
- CrystalCore production quality or an xAI-relevant advantage
- Anything about H1, Optimus, or non-local coupling

Bandwidth ratios remain ~0.70 on the validation partition. The 1M gate
requires ≤ 0.40 **and** quality LCB ≥ 0.90 simultaneously. That gate is
recorded in [`../../results/final-test-v0.1/`](../../results/final-test-v0.1/)
(GOVERNANCE steps 5–6). This freeze document is not that record.


## Freeze rule (locked before selection)

Applied independently to the three validation configs of each candidate:

1. Highest receiver fidelity (agreement with dense reference)
2. Then highest quality-ratio LCB
3. Then lowest analytical BW/ref

No new compute. Numbers are copied from the validation record.

## Frozen — Candidate A (hierarchical block-sparse)

| field | value |
|---|---|
| label | `validation.sweep_rank_1` |
| block_size | 512 |
| local_window | 2 |
| global_summaries | 1 |
| cross_block_selections | 32 |
| selection_frequency | every_layer |
| validation agree | 0.9995 |
| validation Q-ratio LCB | 0.9985 |
| validation BW/ref | 0.7145 |

## Frozen — Candidate B (content-addressed retrieval)

| field | value |
|---|---|
| label | `validation.sweep_rank_2` |
| leaf_block | 512 |
| summary_levels | 2 |
| retrieved_blocks | 32 |
| refinement_stages | 2 |
| group_size | 4 |
| validation agree | 0.9995 |
| validation Q-ratio LCB | 0.9985 |
| validation BW/ref | 0.7041 |

On the validation partition, B’s sweep_rank_2 outranked sweep_rank_1. Sweep
rank is not the freeze; the rule above is.

## What happened next

GOVERNANCE step 5: immutable final test, 32k → 1M, **only** these two configs
plus the dense reference — recorded 2026-08-23. Dual-gate **fail** (quality
LCB pass, analytical BW/ref fail). See [`../../results/final-test-v0.1/`](../../results/final-test-v0.1/).

