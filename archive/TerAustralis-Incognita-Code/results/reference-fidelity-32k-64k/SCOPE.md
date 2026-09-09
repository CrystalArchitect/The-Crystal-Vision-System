# Scope of the 32k / 64k reference-fidelity run

This record is **not** a 1M dual-gate decision and is **not** a
CrystalCore performance claim.

## What was measured

- Partition: `development` (seed `DEV_CORPUS_SEED`). Final seed family unused.
- Lengths: 32768 and 65536 tokens. n = 1000 items per length (2000 paired items).
- Systems: dense reference, Candidate A (hierarchical block-sparse), Candidate B (content-addressed retrieval).
- Candidates used **development defaults**, not frozen configurations.
- Task: synthetic associative retrieval / composition on a frozen identity-bind encoder (`K[t] = h[t-2]+h[t-1]`, `Q = h[e]+h[a]`, `ATTN_BETA=16`). Query-to-context only. No language model, no trained weights.
- Bandwidth: analytical fp32 element counts over index, routing, KV, attention, and output. Not a hardware PMU.

## What was not measured

- 1M-token context
- The locked dual gate `LCB(Q_primitive/Q_full) ≥ 0.90 AND BW_primitive/BW_full ≤ 0.40`
- Production CrystalCore attention or weights
- Validation or final partitions

H1 remains frozen. Production `core/` was not modified.
Candidate independence: A and B were executed in separate passes and
did not read each other's item-level files during scoring.
