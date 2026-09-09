"""Independent development-sweep grids.

Grids were specified before any sweep scores existed. Candidate B's grid
does not depend on Candidate A's results (independence rule).

This is not a full factorial of the spec ranges. It is a primary 2-D
grid plus one-factor-at-a-time on the remaining axes. Configuration
freeze has not occurred.
"""

from __future__ import annotations

from benchmarks.config import CANDIDATE_A_DEV, CANDIDATE_B_DEV


def grid_candidate_a() -> list[dict]:
    cfgs: list[dict] = []
    seen: set[tuple] = set()

    def add(block: int, window: int, summaries: int, k: int, freq: str) -> None:
        key = (block, window, summaries, k, freq)
        if key in seen:
            return
        seen.add(key)
        cfgs.append(
            {
                "block_size": block,
                "local_window": window,
                "global_summaries": summaries,
                "cross_block_selections": k,
                "selection_frequency": freq,
            }
        )

    for block in (512, 1024, 2048):
        for k in (4, 8, 16, 32):
            add(block, 2, 1, k, "every_layer")

    for window in (1, 2, 4):
        add(1024, window, 1, 16, "every_layer")

    for summaries in (1, 4, 8):
        add(1024, 2, summaries, 16, "every_layer")

    for freq in ("every_layer", "alternating"):
        add(1024, 2, 1, 16, freq)

    add(
        CANDIDATE_A_DEV["block_size"],
        CANDIDATE_A_DEV["local_window"],
        CANDIDATE_A_DEV["global_summaries"],
        CANDIDATE_A_DEV["cross_block_selections"],
        CANDIDATE_A_DEV["selection_frequency"],
    )
    return cfgs


def grid_candidate_b() -> list[dict]:
    cfgs: list[dict] = []
    seen: set[tuple] = set()

    def add(leaf: int, levels: int, retrieved: int, stages: int, group: int = 4) -> None:
        key = (leaf, levels, retrieved, stages, group)
        if key in seen:
            return
        seen.add(key)
        cfgs.append(
            {
                "leaf_block": leaf,
                "summary_levels": levels,
                "retrieved_blocks": retrieved,
                "refinement_stages": stages,
                "group_size": group,
            }
        )

    for leaf in (512, 1024, 2048):
        for retrieved in (4, 8, 16, 32):
            add(leaf, 2, retrieved, 2)

    for levels in (2, 3, 4):
        add(1024, levels, 16, 2)

    for stages in (1, 2, 3):
        add(1024, 2, 16, stages)

    add(
        CANDIDATE_B_DEV["leaf_block"],
        CANDIDATE_B_DEV["summary_levels"],
        CANDIDATE_B_DEV["retrieved_blocks"],
        CANDIDATE_B_DEV["refinement_stages"],
        CANDIDATE_B_DEV["group_size"],
    )
    return cfgs
