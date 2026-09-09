# H2 development sweep (V0.1)

**Status:** Development partition · no configuration freeze · no performance claims

## Interpretation Boundary

This report does **not** demonstrate:

- A frozen candidate configuration (GOVERNANCE step 4 has not occurred)
- A 1M-token result, nor a dual-gate pass or fail
- A language-model result (synthetic associative-memory encoder only)
- Hardware bandwidth (analytical fp32 element counts only)
- CrystalCore production quality or an xAI-relevant advantage
- Anything about H1, Optimus, or brain-to-brain / non-local coupling

Receiver fidelity (agreement with the dense reference on the development
subsample) is the sole ranking axis. Bandwidth is recorded, not gated.
Top-ranked configs are development observations, not selected finals.

Subsample: n = 100 items per length, lengths = [32768, 65536].
Generator: development seed family, item indices `[0, n)`.
Final seed family was not used. Production `core/` was not modified.

Compute envelope: reference 8.9s; A 217.2s / 17 configs; B 130.8s / 16 configs.
Not a dollar BOM.

## Observations (not freeze, not claims)

- Dense reference gold accuracy on this subsample: 1.000.
- Candidate A `selection_frequency=alternating` dropped agreement to 0.110. Every-layer selection did not.
- On this encoder, agreement reached 1.000 for several wider retrieval settings. Narrower settings (A `cross_block_selections=4`, B `retrieved_blocks=4`) sat at 0.985–0.990.
- B `summary_levels` {2,3,4} and `refinement_stages` {1,2,3} at leaf=1024 / retrieved=16 were tied at 0.995 on this subsample.
- No tested config produced an analytical BW/ref ≤ 0.40. That is **not** a 1M dual-gate fail; the gate was not evaluated.
- Step 1 (n=1000/length) numbers are not replaced by this subsample.

### Candidate A (hierarchical block-sparse) — top 5 by receiver fidelity (not frozen)

| rank | agree | gold acc | BW/ref | cfg |
|---|---|---|---|---|
| 1 | 1.0000 | 1.0000 | 0.7148 | `{'block_size': 512, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 32, 'selection_frequency': 'every_layer'}` |
| 2 | 1.0000 | 1.0000 | 0.7402 | `{'block_size': 2048, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 8, 'selection_frequency': 'every_layer'}` |
| 3 | 1.0000 | 1.0000 | 0.8620 | `{'block_size': 1024, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 32, 'selection_frequency': 'every_layer'}` |
| 4 | 1.0000 | 1.0000 | 0.8685 | `{'block_size': 2048, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 16, 'selection_frequency': 'every_layer'}` |
| 5 | 1.0000 | 1.0000 | 1.0039 | `{'block_size': 2048, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 32, 'selection_frequency': 'every_layer'}` |

### Candidate B (content-addressed retrieval) — top 5 by receiver fidelity (not frozen)

| rank | agree | gold acc | BW/ref | cfg |
|---|---|---|---|---|
| 1 | 1.0000 | 1.0000 | 0.7041 | `{'leaf_block': 2048, 'summary_levels': 2, 'retrieved_blocks': 8, 'refinement_stages': 2, 'group_size': 4}` |
| 2 | 1.0000 | 1.0000 | 0.7041 | `{'leaf_block': 512, 'summary_levels': 2, 'retrieved_blocks': 32, 'refinement_stages': 2, 'group_size': 4}` |
| 3 | 1.0000 | 1.0000 | 0.8538 | `{'leaf_block': 2048, 'summary_levels': 2, 'retrieved_blocks': 16, 'refinement_stages': 2, 'group_size': 4}` |
| 4 | 1.0000 | 1.0000 | 0.8538 | `{'leaf_block': 1024, 'summary_levels': 2, 'retrieved_blocks': 32, 'refinement_stages': 2, 'group_size': 4}` |
| 5 | 1.0000 | 1.0000 | 1.0034 | `{'leaf_block': 2048, 'summary_levels': 2, 'retrieved_blocks': 32, 'refinement_stages': 2, 'group_size': 4}` |

Full ranked lists: `summary.json`. Item-level reference: `reference.json`.

H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven.
External / xAI pitch remains Hold.
