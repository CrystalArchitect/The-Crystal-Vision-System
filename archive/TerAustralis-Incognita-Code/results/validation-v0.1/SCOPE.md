# Scope of the H2 validation (V0.1)

## Interpretation Boundary

This record does **not** demonstrate:

- A frozen candidate configuration (GOVERNANCE step 4 has not occurred)
- A 1M-token result, nor a dual-gate pass or fail
- Language-model quality (synthetic associative-memory encoder only)
- Hardware bandwidth or dollar cost (analytical fp32 counts + wall-clock only)
- CrystalCore production quality, an Optimus-relevant result, or an xAI-relevant advantage
- Anything about H1
- Non-local, dimensional, or brain-to-brain information transfer

Brain-to-brain synchrony remains ordinary sensory-mediated coupling and is
out of scope for this validation.

## What was measured

- Partition: `validation` (seed family `VAL_CORPUS_SEED`). Development items
  from steps 1–2 were not reused. Final seed family sealed.
- Lengths: 32768 and 65536. n = 1000 items per length (protocol primary size).
- Measurement axis: receiver fidelity = agreement with the dense reference
  (gold accuracy and quality-ratio LCB also recorded).
- Bandwidth: analytical, recorded, **not gated**.
- Candidates executed independently. B's config set was specified from B's
  own published sweep ranking and does not use A's validation scores.
- Production `core/` unmodified.

## Config selection (not a freeze)

Applied independently to each candidate's published development-sweep ranking:

1. highest receiver-fidelity, then lowest BW/ref
2. next distinct config under the same ranking
3. Step-1 development default (continuity probe)

See `benchmarks/validation_configs.py`. Sweep rank is not a frozen config:
on this partition, Candidate B's sweep_rank_2 outranked sweep_rank_1 on
agreement. That is why GOVERNANCE keeps freeze as a later, explicit step.

## Observation (not a gate)

No tested validation config produced analytical BW/ref ≤ 0.40. That is
**not** a 1M dual-gate fail; the gate was not evaluated.
