# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
The prediction-1 harness: the stateful loop against stateless baselines.

Ported from CrystalCore.OS/synthetic-affect (2026-08-14). Run with:

    python3 -m experiments.harness

It executes every agent against every task in the suite, then writes
`experiments/results/results.json` and a generated `experiments/results/
RESULTS.md`. Both are deterministic — no wall clock appears anywhere — so the
committed results are byte-reproducible and `git diff` on them is a real check
that they are outputs rather than prose. The date of the committed run lives in
CHRONICLE.md, where dates belong.

This file decides nothing about who wins. It runs the runs and reports the
numbers, including the ones that go against the theory.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.closure import STRATEGIES

from .agents import (
    ConstantPolicy,
    LoopAgent,
    MagnitudeReactivePolicy,
    StallBlindLoopAgent,
    TunedLookupPolicy,
)
from .tasks import SUITE, TURN_CAP, ScriptedTask, TaskEnv

RESULTS_DIR = pathlib.Path(__file__).resolve().parent / "results"

#: Construction order fixes report order. A fresh agent per (agent, task) run;
#: each factory receives the task, which only the tuned ceiling uses.
AGENT_FACTORIES: Tuple[Tuple[str, Callable[[ScriptedTask], Any]], ...] = tuple(
    [("loop", lambda task: LoopAgent()),
     ("loop_stall_blind", lambda task: StallBlindLoopAgent())]
    + [(f"always_{s}", (lambda s=s: (lambda task: ConstantPolicy(s)))()) for s in STRATEGIES]
    + [("magnitude_reactive", lambda task: MagnitudeReactivePolicy()),
       ("tuned_lookup", lambda task: TunedLookupPolicy(task))]
)

STATEFUL_AGENTS = ("loop", "loop_stall_blind")

#: The agents eligible for the best-stateless comparison: stateless AND
#: task-agnostic. The tuned lookup is stateless but task-informed — it bounds
#: the comparison and must not sit inside it.
TASK_AGNOSTIC_STATELESS = tuple(
    [f"always_{s}" for s in STRATEGIES] + ["magnitude_reactive"]
)


def run_one(task: ScriptedTask, agent: Any) -> Dict[str, Any]:
    """One agent, one task, one deterministic run."""
    env = TaskEnv(task)
    strategies: List[str] = []
    resolved = False
    turns = 0

    while True:
        observation = env.observe()
        if env.resolved():
            resolved = True
            break
        if turns >= TURN_CAP:
            break
        env.arm_transition_if_due()
        strategy = agent.decide(task.goal, observation)
        strategies.append(strategy)
        env.step(strategy)
        turns += 1

    record: Dict[str, Any] = {
        "resolved": resolved,
        "turns": turns if resolved else None,
        "strategies": strategies,
    }
    if getattr(agent, "stateful", False):
        if resolved:
            agent.observe_final(task.goal, env.observe())
        record["labels"] = list(agent.labels)
        record["closure_success_rate"] = agent.closure_success_rate()
        agent.close()
    return record


def run_suite() -> Dict[str, Any]:
    runs: Dict[str, Dict[str, Any]] = {}
    for task in SUITE:
        runs[task.name] = {}
        for agent_name, factory in AGENT_FACTORIES:
            runs[task.name][agent_name] = run_one(task, factory(task))

    agent_names = [name for name, _ in AGENT_FACTORIES]
    stateless_names = [n for n in agent_names if n in TASK_AGNOSTIC_STATELESS]

    resolved_counts = {
        name: sum(1 for task in SUITE if runs[task.name][name]["resolved"])
        for name in agent_names
    }

    # Per task, the best stateless result — the maximally adversarial
    # comparator, since any constant policy may be pre-tuned to any one task.
    best_stateless: Dict[str, Optional[Dict[str, Any]]] = {}
    for task in SUITE:
        candidates = [
            {"agent": n, "turns": runs[task.name][n]["turns"]}
            for n in stateless_names
            if runs[task.name][n]["resolved"]
        ]
        best_stateless[task.name] = (
            min(candidates, key=lambda c: (c["turns"], c["agent"]))
            if candidates
            else None
        )

    loop_vs_best: Dict[str, str] = {}
    for task in SUITE:
        loop_run = runs[task.name]["loop"]
        best = best_stateless[task.name]
        if loop_run["resolved"] and best is None:
            loop_vs_best[task.name] = "loop_only"
        elif loop_run["resolved"] and best is not None:
            if loop_run["turns"] < best["turns"]:
                loop_vs_best[task.name] = "loop_faster"
            elif loop_run["turns"] == best["turns"]:
                loop_vs_best[task.name] = "tie"
            else:
                loop_vs_best[task.name] = "stateless_faster"
        elif best is not None:
            loop_vs_best[task.name] = "stateless_only"
        else:
            loop_vs_best[task.name] = "nobody"

    # The honest aggregates, computed rather than asserted. Adversarial
    # review (2026-08-12, canon) caught the prose compressing to the one
    # aggregate that flattered the loop; these fields make the full set
    # unavoidable.
    verdict_tally: Dict[str, int] = {}
    for verdict in loop_vs_best.values():
        verdict_tally[verdict] = verdict_tally.get(verdict, 0) + 1

    return {
        "turn_cap": TURN_CAP,
        "agents": agent_names,
        "tasks": {t.name: {"note": t.note, "goal": t.goal} for t in SUITE},
        "runs": runs,
        "summary": {
            "resolved_counts": resolved_counts,
            "best_stateless_per_task": best_stateless,
            "loop_vs_best_stateless": loop_vs_best,
            "verdict_tally": verdict_tally,
            "loop_strictly_faster_count": verdict_tally.get("loop_faster", 0),
            "best_stateless_portfolio_resolved": sum(
                1 for b in best_stateless.values() if b is not None
            ),
        },
    }


def render_markdown(results: Dict[str, Any]) -> str:
    """RESULTS.md, generated. Carries no date — CHRONICLE.md holds that."""
    agents = results["agents"]
    runs = results["runs"]
    task_names = list(results["tasks"].keys())

    def cell(task: str, agent: str) -> str:
        run = runs[task][agent]
        return str(run["turns"]) if run["resolved"] else "DNF"

    lines: List[str] = []
    lines.append("# Results — prediction 1 harness")
    lines.append("")
    lines.append(
        "> Synthetic = apparent / functional, for design purposes. Not a claim"
        " of feeling, consciousness, or inner experience."
    )
    lines.append("")
    lines.append(
        "**Generated by `python3 -m experiments.harness`.** Do not edit by"
        " hand — a fresh run must reproduce this file byte for byte. The date"
        " of the committed run is recorded in `CHRONICLE.md`. Ported from"
        " CrystalCore.OS/synthetic-affect, 2026-08-14 — these are this"
        " package's own numbers, measured against this package's own core/,"
        " not copied from canon."
    )
    lines.append("")
    lines.append("**Belt: Science, with stated scope.** These numbers are real"
                 " and reproducible, and they are measurements of a scripted,"
                 " deterministic environment — not of live LLM workloads. The"
                 " prediction for real workloads remains Vision.")
    lines.append("")
    lines.append("## Method, in one paragraph")
    lines.append("")
    lines.append(
        "Every agent sees the same observation each turn — expected state and"
        " actual state — and submits one strategy from the shared vocabulary."
        f" A run ends at resolution or at the {results['turn_cap']}-turn cap"
        " (DNF). Stateless agents are pure functions of the current"
        " observation, asserted by test. The stateless registry contains every"
        " constant policy, one per strategy, plus a magnitude-reactive policy"
        " that uses everything the current observation offers; the comparison"
        " below is against the **best stateless result per task**, which is"
        " maximally adversarial to the loop, since a constant policy may be"
        " pre-tuned to any single task. One further agent, `tuned_lookup`, is"
        " stateless but **task-informed** — a lookup table built from each"
        " task's definition. It is excluded from the best-stateless comparison"
        " and reported as a ceiling: what full task knowledge buys a stateless"
        " agent."
    )
    lines.append("")
    lines.append("## Turns to resolution")
    lines.append("")
    lines.append("| task | " + " | ".join(agents) + " |")
    lines.append("|---|" + "---|" * len(agents))
    for task in task_names:
        lines.append(
            f"| {task} | " + " | ".join(cell(task, a) for a in agents) + " |"
        )
    lines.append("")
    resolved = results["summary"]["resolved_counts"]
    lines.append(
        "**Tasks resolved:** "
        + " · ".join(f"{a} {resolved[a]}/{len(task_names)}" for a in agents)
    )
    lines.append("")
    lines.append("## The honest aggregates — all of them")
    lines.append("")
    lines.append(
        "Adversarial review caught an earlier draft of the surrounding"
        " documents quoting only the first of these, the one that most"
        " flatters the loop. They stand together or not at all:"
    )
    lines.append("")
    n = len(task_names)
    summary = results["summary"]
    lines.append(
        f"- **Best single task-agnostic stateless policy: "
        f"{max(resolved[a] for a in agents if a not in ('loop', 'loop_stall_blind', 'tuned_lookup'))}/{n}"
        f" resolved** — no one fixed stateless policy adapts across the suite."
    )
    lines.append(
        f"- **Per-task best-stateless portfolio: "
        f"{summary['best_stateless_portfolio_resolved']}/{n}** — allowed a"
        " different stateless policy per task, statelessness matches the"
        " loop's resolved count everywhere except deploy_rollback."
    )
    lines.append(
        f"- **Tasks where the loop is strictly faster than the best stateless:"
        f" {summary['loop_strictly_faster_count']} of {n}.** The loop never"
        " wins on raw speed; it wins on resolving with one policy and no task"
        " knowledge."
    )
    lines.append(
        f"- **Task-informed stateless ceiling (`tuned_lookup`):"
        f" {resolved['tuned_lookup']}/{n}**, faster-or-equal to the loop on"
        " every task both resolve, DNF only on deploy_rollback — the one task"
        " where no observation→strategy table can exist."
    )
    lines.append(
        "- **What state uniquely buys, on this suite:** resolving"
        f" {resolved['loop']}/{n} with a single policy and no task knowledge,"
        " and the only resolution of deploy_rollback."
    )
    lines.append("")
    lines.append("## Loop vs best stateless, per task")
    lines.append("")
    lines.append("| task | loop | best stateless | verdict |")
    lines.append("|---|---|---|---|")
    for task in task_names:
        best = results["summary"]["best_stateless_per_task"][task]
        best_text = f"{best['agent']} ({best['turns']})" if best else "none resolves it"
        lines.append(
            f"| {task} | {cell(task, 'loop')} |"
            f" {best_text} |"
            f" {results['summary']['loop_vs_best_stateless'][task]} |"
        )
    lines.append("")
    lines.append("## What the loop actually did")
    lines.append("")
    for task in task_names:
        run = runs[task]["loop"]
        lines.append(f"**{task}** — strategies `{' → '.join(run['strategies']) or '—'}`,"
                     f" labels `{' → '.join(run['labels'])}`,"
                     f" closure success rate"
                     f" {run['closure_success_rate'] if run['closure_success_rate'] is not None else 'unjudged'}")
        lines.append("")
    lines.append("## Findings that cut against the theory")
    lines.append("")
    lines.append(
        "- **strict_interview:** the loop DNFs where `always_ask` resolves in"
        " 2. After the first answer the shrinking gap reads as converging, the"
        " v0.1 policy moves to rephrase, and no route back to ask exists. A"
        " measured limitation of the shipped closure policy, in the suite on"
        " purpose."
    )
    lines.append(
        "- **Per-task pre-tuned constants win their own task:**"
        " `always_switch_tool` and `always_escalate` beat the loop on the one"
        " task each is tuned to, then resolve almost nothing else. State buys"
        " adaptivity across the suite, not victory on every task."
    )
    lines.append("")
    lines.append("## The construction, not just a measurement")
    lines.append("")
    lines.append(
        "`deploy_rollback` is unsolvable by **any** stateless policy, tuned or"
        " not: the observation before the first ask and the observation after"
        " the rollback are byte-identical, and the correct strategies differ."
        " A function of the current observation returns the same strategy both"
        " times, so it clears at most one of the two obstacles. The loop"
        " resolves it because its history distinguishes the two moments. That"
        " is postulate 1 operationalised."
    )
    lines.append("")
    lines.append("## Caveats, stated rather than buried")
    lines.append("")
    lines.append(
        "- The task suite is experimenter-chosen. It includes controls, ties,"
        " and a task the loop loses, but the selection is still part of the"
        " design. Criticism of the suite is invited; add a task and rerun."
    )
    lines.append(
        "- The task-agnostic baselines are not exhaustive; see canon"
        " (CrystalCore.OS/synthetic-affect) for the brute-forced"
        " suite-tuned-magnitude-map caveat this package's own test suite"
        " pins independently."
    )
    lines.append(
        "- Nothing here involves a language model. The LLM Core remains a"
        " deterministic stub; these are properties of the control loop."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**All rights reserved.**")
    lines.append("TerAustralis Incognita™️ — ABN 70 741 068 059")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    results = run_suite()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    # newline pinned so byte-reproducibility holds on every platform, not
    # just wherever os.linesep happens to be "\n".
    (RESULTS_DIR / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (RESULTS_DIR / "RESULTS.md").write_text(
        render_markdown(results), encoding="utf-8", newline="\n"
    )

    resolved = results["summary"]["resolved_counts"]
    print(f"[harness] {len(SUITE)} tasks × {len(results['agents'])} agents, cap {TURN_CAP}")
    for agent in results["agents"]:
        per_task = " ".join(
            (str(results["runs"][t][agent]["turns"])
             if results["runs"][t][agent]["resolved"] else "DNF").rjust(4)
            for t in results["tasks"]
        )
        print(f"[harness] {agent:>20}  resolved {resolved[agent]}/{len(SUITE)}  {per_task}")
    print(f"[harness] wrote {RESULTS_DIR / 'results.json'} and RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
