# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Example 01 — a repeated query exercising a full open→close cycle.
Deterministic — produces examples/logs/01_repeated_query.jsonl.

Four log lines per turn (track, gap_*, label, closure) — cycle is the turn
number, ts is the line number. The printed cycle is loop cycle state, not
arithmetic over line counts (F1 — no //3 exposure).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.loop import Loop


def main():
    base = pathlib.Path(__file__).resolve().parent
    log_path = base / "logs" / "01_repeated_query.jsonl"
    loop = Loop(store_path=":memory:", log_path=str(log_path))

    # Simulated repeated query that closes on the third turn
    steps = [
        ("What is Synthetic Affect Theory?", "I don't know yet"),
        ("What is Synthetic Affect Theory?", "Functional affect signal for design"),
        ("What is Synthetic Affect Theory?", "What is Synthetic Affect Theory?"),  # closed
    ]
    for expected, actual in steps:
        result = loop.run_cycle(expected=expected, actual=actual, event={"query": expected})
        gap_mag = result["gap"].magnitude if result["gap"] else 0.0
        print(
            f"Cycle {result['cycle']}: gap={gap_mag} label={result['label']} "
            f"strategy={result['decision'].strategy} llm={result['llm']}"
        )

    print(f"Log written to {log_path}")


if __name__ == "__main__":
    main()
