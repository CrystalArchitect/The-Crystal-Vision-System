# H2 validation (V0.1)

**Status:** Validation partition · no configuration freeze · no performance claims

## Interpretation Boundary

This report does **not** demonstrate:

- A frozen candidate configuration (GOVERNANCE step 4 has not occurred)
- A 1M-token result, nor a dual-gate pass or fail
- A language-model result (synthetic associative-memory encoder only)
- Hardware bandwidth (analytical fp32 element counts only)
- CrystalCore production quality or an xAI-relevant advantage
- Anything about H1, Optimus, or brain-to-brain / non-local coupling

Receiver fidelity (agreement with the dense reference on the validation
partition) is the sole measurement axis. Bandwidth is recorded, not gated.
Configs under test were taken from each candidate's own published sweep
ranking plus the Step-1 development default. They are not selected finals.

n = 1000 items per length, lengths = [32768, 65536].
Generator: validation seed family. Development items were not reused.
Final seed family was not used. Production `core/` was not modified.

Dense reference gold accuracy on this partition: 1.0000.

Compute envelope: reference 78.6s; A 351.0s / 3 configs; B 227.7s / 3 configs.
Not a dollar BOM.

## Observations (not freeze, not claims)

- All six validation configs stayed at agreement ≥ 0.9980 on n = 2000.
- Candidate B's sweep_rank_2 (leaf 512, retrieved 32) outranked sweep_rank_1
  on this partition (0.9995 vs 0.9980). Sweep rank is not a freeze.
- No tested config produced analytical BW/ref ≤ 0.40. That is **not** a 1M
  dual-gate fail; the gate was not evaluated.
- Step 1 (development, n=1000/length) and Step 2 (development subsample)
  are not replaced by this validation record.


### Candidate A (hierarchical block-sparse) (not frozen)

| label | agree | gold acc | Q-ratio LCB | BW/ref | cfg |
|---|---|---|---|---|---|
| sweep_rank_1 | 0.9995 | 0.9995 | 0.9985 | 0.7145 | `{'block_size': 512, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 32, 'selection_frequency': 'every_layer'}` |
| sweep_rank_2 | 0.9985 | 0.9985 | 0.9965 | 0.7371 | `{'block_size': 2048, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 8, 'selection_frequency': 'every_layer'}` |
| step1_dev_default | 0.9990 | 0.9990 | 0.9975 | 0.7219 | `{'block_size': 1024, 'local_window': 2, 'global_summaries': 1, 'cross_block_selections': 16, 'selection_frequency': 'every_layer'}` |

### Candidate B (content-addressed retrieval) (not frozen)

| label | agree | gold acc | Q-ratio LCB | BW/ref | cfg |
|---|---|---|---|---|---|
| sweep_rank_1 | 0.9980 | 0.9980 | 0.9955 | 0.7041 | `{'leaf_block': 2048, 'summary_levels': 2, 'retrieved_blocks': 8, 'refinement_stages': 2, 'group_size': 4}` |
| sweep_rank_2 | 0.9995 | 0.9995 | 0.9985 | 0.7041 | `{'leaf_block': 512, 'summary_levels': 2, 'retrieved_blocks': 32, 'refinement_stages': 2, 'group_size': 4}` |
| step1_dev_default | 0.9990 | 0.9990 | 0.9975 | 0.7041 | `{'leaf_block': 1024, 'summary_levels': 2, 'retrieved_blocks': 16, 'refinement_stages': 2, 'group_size': 4}` |

Full metrics: `summary.json`. Item-level rows: `reference.json`,
`candidate_a.json`, `candidate_b.json`.

H1 remains Frozen · Unproven. CrystalCore advantage remains Unproven.
External / xAI pitch remains Hold.

Locked next step, when ordered: configuration freeze (one config per
candidate). Still not 1M.
