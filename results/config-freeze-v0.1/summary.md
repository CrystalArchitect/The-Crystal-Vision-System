# H2 configuration freeze (V0.1)

**Status:** Step 4 recorded · not a 1M dual-gate · no performance claims

## Interpretation Boundary

This freeze does **not** demonstrate 1M-token behaviour, a dual-gate pass or
fail, language-model quality, hardware bandwidth, CrystalCore advantage, H1,
Optimus, or non-local coupling. No new items were scored. Final seed family
sealed. Production `core/` unmodified.

## Frozen configs

| candidate | source | agree | Q-ratio LCB | BW/ref | cfg |
|---|---|---|---|---|---|
| A hierarchical block-sparse | validation.sweep_rank_1 | 0.9995 | 0.9985 | 0.7145 | block 512, window 2, summaries 1, k 32, every_layer |
| B content-addressed retrieval | validation.sweep_rank_2 | 0.9995 | 0.9985 | 0.7041 | leaf 512, levels 2, retrieved 32, stages 2, group 4 |

No frozen config has analytical BW/ref ≤ 0.40. That is **not** a 1M dual-gate
fail; the gate was not evaluated.

Machine record: `frozen.json`. Rule: `docs/H2/FROZEN-CONFIGS-V0.1.md`.

Locked next step, when ordered: immutable final test (32k → 1M) on **only**
these two configs plus the dense reference.
