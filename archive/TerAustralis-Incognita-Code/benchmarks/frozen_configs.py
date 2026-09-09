"""H2 V0.1 frozen candidate configs (GOVERNANCE step 4).

Selected independently from results/validation-v0.1 using the freeze rule
in docs/H2/FROZEN-CONFIGS-V0.1.md. Not a 1M dual-gate. Not a performance claim.
"""

from __future__ import annotations

CANDIDATE_A_FROZEN = {
    "block_size": 512,
    "local_window": 2,
    "global_summaries": 1,
    "cross_block_selections": 32,
    "selection_frequency": "every_layer",
}

CANDIDATE_B_FROZEN = {
    "leaf_block": 512,
    "summary_levels": 2,
    "retrieved_blocks": 32,
    "refinement_stages": 2,
    "group_size": 4,
}

FROZEN_META = {
    "protocol": "H2-V0.1",
    "phase": "configuration-freeze",
    "configuration_frozen": True,
    "one_m_dual_gate_evaluated": False,
    "candidate_a_source": "validation.sweep_rank_1",
    "candidate_b_source": "validation.sweep_rank_2",
}
