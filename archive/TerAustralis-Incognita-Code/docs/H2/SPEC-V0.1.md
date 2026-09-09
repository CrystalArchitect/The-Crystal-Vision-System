# CrystalCore H2 — Primitive Specification V0.1

**Status:** Design phase — no performance claims

## Hypothesis

A defined sparse/hierarchical attention or coherence primitive can retain ≥90% of an explicitly selected full-attention quality metric at 1M-token context, while using ≤40% of the corresponding memory bandwidth, under a locked workload and precision configuration. Both conditions must pass simultaneously.

## Candidate A — Hierarchical Block-Sparse Attention

Partition context into fixed-size blocks. Perform local attention + coarse global summaries + limited selected cross-block attention. Initial parameter sweeps (development only):

* Block size: 512 / 1024 / 2048
* Local window: 1–4 neighbouring blocks
* Global summaries: 1–8 per block
* Cross-block selections: 4–32
* Selection frequency: every layer / alternating layers

## Candidate B — Content-Addressed Hierarchical Retrieval Attention

Build hierarchical content-addressable index → retrieve top-k regions → dense attention only over retrieved regions. Initial parameter sweeps (development only):

* Leaf block: 512–2048 tokens
* Summary levels: 2–4
* Retrieved blocks: 4 / 8 / 16 / 32
* Refinement stages: 1–3

## Common Rules

* Measurement boundary must include all index, routing, KV, attention and output traffic.
* Neither candidate may receive ground-truth evidence locations.
* Only the attention mechanism may change. Model weights, tokenizer, task, precision and evaluation set remain frozen.
* Candidates are independent. One may not use the other’s final-test results.

## Pass Gate (1M tokens)

LCB(Q_primitive / Q_full) ≥ 0.90 AND BW_primitive / BW_full ≤ 0.40
