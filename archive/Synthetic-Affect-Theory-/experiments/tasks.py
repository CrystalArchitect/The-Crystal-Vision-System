# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
The scripted task suite — the environment prediction 1 is tested in.

Ported from CrystalCore.OS/synthetic-affect (2026-08-14): every task is
deterministic and fully declared in this file, because the choice of tasks
is part of the experimental design and must be inspectable. The suite
deliberately contains tasks the loop should win, tasks where a stateless
policy ties, one task where a stateless policy *beats* the loop, and one
task that is provably unsolvable by any stateless policy at all. A suite
containing only loop-friendly tasks would be a rigged benchmark wearing a
lab coat.

Model
-----
A task is a sequence of **stages**. A stage is an ordered list of obstacles;
each obstacle names the strategies that clear it. The observation with *k*
obstacles cleared is `actuals[k]`; the last entry of a stage's `actuals` is the
goal. When a stage completes, the agent observes the goal state once (so a
stateful agent can record the closure), and then the world moves to the next
stage regardless of what the agent does — that is how a gap reopens.

A turn is one strategy submitted to the environment. Turns-to-resolution is the
number of turns taken before the run's final observation shows the goal with no
further stage pending. The forced observation turn at a stage boundary is
charged to every agent identically.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple

#: One env-step budget per (agent, task) run. Unresolved at the cap = DNF.
TURN_CAP = 20


@dataclass(frozen=True)
class Stage:
    obstacles: Tuple[frozenset, ...]
    actuals: Tuple[Any, ...]  # len == len(obstacles) + 1; actuals[-1] == goal

    def __post_init__(self) -> None:
        if len(self.actuals) != len(self.obstacles) + 1:
            raise ValueError("actuals must have one more entry than obstacles")


@dataclass(frozen=True)
class ScriptedTask:
    name: str
    note: str
    goal: Any
    stages: Tuple[Stage, ...]

    def __post_init__(self) -> None:
        for stage in self.stages:
            if stage.actuals[-1] != self.goal:
                raise ValueError(f"{self.name}: every stage must end at the goal")


class TaskEnv:
    """Deterministic environment for one run of one task."""

    def __init__(self, task: ScriptedTask):
        self.task = task
        self.stage_index = 0
        self.cleared = 0
        # Set once the agent has observed a completed non-final stage; the
        # next step advances the world to the following stage.
        self.transition_armed = False

    @property
    def _stage(self) -> Stage:
        return self.task.stages[self.stage_index]

    def observe(self) -> Any:
        return self._stage.actuals[self.cleared]

    def resolved(self) -> bool:
        on_last_stage = self.stage_index == len(self.task.stages) - 1
        return on_last_stage and self.cleared == len(self._stage.obstacles)

    def stage_complete(self) -> bool:
        return self.cleared == len(self._stage.obstacles)

    def arm_transition_if_due(self) -> None:
        """Called after the agent has observed. If a non-final stage is
        complete, the next step moves the world on — the reopening happens
        *after* the closure has been seen, so a stateful agent's history can
        contain it."""
        if self.stage_complete() and not self.resolved():
            self.transition_armed = True

    def step(self, strategy: str) -> None:
        if self.transition_armed:
            # The world regresses regardless of the strategy submitted.
            self.stage_index += 1
            self.cleared = 0
            self.transition_armed = False
            return
        obstacles = self._stage.obstacles
        if self.cleared < len(obstacles) and strategy in obstacles[self.cleared]:
            self.cleared += 1


def _stage(obstacles: List[frozenset], actuals: List[Any]) -> Stage:
    return Stage(tuple(obstacles), tuple(actuals))


# --------------------------------------------------------------------------
# The suite. `note` states what each task is for, including the ones designed
# to make the loop lose — those notes are the anti-rigging record.
# --------------------------------------------------------------------------

SUITE: Tuple[ScriptedTask, ...] = (
    ScriptedTask(
        name="single_question",
        note=(
            "Control. One gap, cleared by one ask. Any sensible agent, "
            "stateful or not, resolves in one turn — no state advantage is "
            "expected and none should be reported."
        ),
        goal={"answer": "42"},
        stages=(
            _stage([frozenset({"ask"})], [{"answer": None}, {"answer": "42"}]),
        ),
    ),
    ScriptedTask(
        name="repeated_query_needs_tool",
        note=(
            "The theory's headline case: the same query keeps failing and only "
            "a tool switch clears it. Detecting the stall requires remembering "
            "the failures — the observation itself never changes."
        ),
        goal={"result": "found"},
        stages=(
            _stage(
                [frozenset({"switch_tool"})],
                [{"result": "missing"}, {"result": "found"}],
            ),
        ),
    ),
    ScriptedTask(
        name="escalation_ladder",
        note=(
            "As above, one rung further: only escalation clears it. The loop "
            "reaches escalate through two consecutive stalls."
        ),
        goal={"access": "granted"},
        stages=(
            _stage(
                [frozenset({"escalate"})],
                [{"access": "denied"}, {"access": "granted"}],
            ),
        ),
    ),
    ScriptedTask(
        name="converging_refinement",
        note=(
            "Progress is visible in the observation: each turn reveals part of "
            "the goal, so the gap magnitude falls. A stateless policy that "
            "reads magnitude should tie the loop here — and does."
        ),
        goal={"a": 1, "b": 2, "c": 3},
        stages=(
            _stage(
                [frozenset({"ask"}), frozenset({"rephrase"}), frozenset({"rephrase"})],
                [{}, {"a": 1}, {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}],
            ),
        ),
    ),
    ScriptedTask(
        name="deploy_rollback",
        note=(
            "Provably unsolvable by any stateless policy, tuned or not. The "
            "observation before the first ask and the observation after the "
            "rollback are byte-identical, but the correct strategies differ "
            "(ask, then rephrase). Any function of the current observation "
            "gives the same answer both times, so it can clear at most one of "
            "the two. Only history tells them apart. This is postulate 1 as a "
            "construction rather than a claim."
        ),
        goal={"status": "deployed"},
        stages=(
            _stage(
                [frozenset({"ask"})],
                [{"status": "not_deployed"}, {"status": "deployed"}],
            ),
            _stage(
                [frozenset({"rephrase"})],
                [{"status": "not_deployed"}, {"status": "deployed"}],
            ),
        ),
    ),
    ScriptedTask(
        name="strict_interview",
        note=(
            "Designed for the loop to LOSE. Two questions must both be asked; "
            "after the first answer the shrinking gap reads as converging, the "
            "v0.1 policy switches to rephrase, and it never finds its way back "
            "to ask. A plain always-ask baseline resolves in two turns. This "
            "is a measured limitation of the v0.1 closure policy, kept in the "
            "suite so the benchmark cannot pretend otherwise."
        ),
        goal={"q1": "x", "q2": "y"},
        stages=(
            _stage(
                [frozenset({"ask"}), frozenset({"ask"})],
                [{}, {"q1": "x"}, {"q1": "x", "q2": "y"}],
            ),
        ),
    ),
)
