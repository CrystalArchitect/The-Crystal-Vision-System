# Scope of the H2 development sweep (V0.1)

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
out of scope for this sweep.

## What was measured

- Partition: `development` only. Final seed family sealed.
- Lengths: 32768 and 65536. n = 100 items per length (development-sweep subsample, not the 1000-item primary set).
- Ranking axis: receiver fidelity = agreement with the dense reference (gold accuracy also recorded).
- Bandwidth: analytical, recorded, **not gated**.
- Candidates executed independently. B's grid was specified without A's scores.
- Production `core/` unmodified.

## Grid design

Not a full factorial. Primary 2-D grid (block/leaf × retrieval width) plus
one-factor-at-a-time on the remaining spec axes. See `benchmarks/sweep_grids.py`.
