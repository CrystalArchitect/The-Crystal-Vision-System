"""H2 V0.1 validation config sets.

Specified from each candidate's own published development-sweep ranking
(results/dev-sweep-v0.1/summary.md). Candidate B's set does not use
Candidate A's scores (independence rule).

This is not a configuration freeze. GOVERNANCE step 4 has not occurred.
"""

from __future__ import annotations

from benchmarks.config import CANDIDATE_A_DEV, CANDIDATE_B_DEV


# Selection rule, applied independently:
#   1. highest receiver-fidelity (agreement), then lowest BW/ref
#   2. next distinct config under the same ranking
#   3. Step-1 development default (continuity probe)
#
# Taken from the recorded sweep. Not frozen.

CANDIDATE_A_VALIDATION = [
    {
        "label": "sweep_rank_1",
        "cfg": {
            "block_size": 512,
            "local_window": 2,
            "global_summaries": 1,
            "cross_block_selections": 32,
            "selection_frequency": "every_layer",
        },
    },
    {
        "label": "sweep_rank_2",
        "cfg": {
            "block_size": 2048,
            "local_window": 2,
            "global_summaries": 1,
            "cross_block_selections": 8,
            "selection_frequency": "every_layer",
        },
    },
    {
        "label": "step1_dev_default",
        "cfg": dict(CANDIDATE_A_DEV),
    },
]

CANDIDATE_B_VALIDATION = [
    {
        "label": "sweep_rank_1",
        "cfg": {
            "leaf_block": 2048,
            "summary_levels": 2,
            "retrieved_blocks": 8,
            "refinement_stages": 2,
            "group_size": 4,
        },
    },
    {
        "label": "sweep_rank_2",
        "cfg": {
            "leaf_block": 512,
            "summary_levels": 2,
            "retrieved_blocks": 32,
            "refinement_stages": 2,
            "group_size": 4,
        },
    },
    {
        "label": "step1_dev_default",
        "cfg": dict(CANDIDATE_B_DEV),
    },
]
