# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Example 02 — a gap that reopens, to show the `reopened` label doing work.
Deterministic — produces examples/logs/02_gap_reopens.jsonl.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.loop import Loop


def main():
    base = pathlib.Path(__file__).resolve().parent
    log_path = base / "logs" / "02_gap_reopens.jsonl"
    loop = Loop(store_path=":memory:", log_path=str(log_path))

    steps = [
        ("deploy", "pending"),   # gap opened
        ("deploy", "deploy"),    # closed
        ("deploy", "rollback"),  # reopened
        ("deploy", "deploy"),    # closed again
    ]
    for expected, actual in steps:
        result = loop.run_cycle(expected=expected, actual=actual, event={"deploy_state": actual})
        gap_mag = "None" if not result["gap"] else result["gap"].magnitude
        print(
            f"Cycle {result['cycle']}: label={result['label']} "
            f"strategy={result['decision'].strategy} gap={gap_mag}"
        )

    print(f"Log written to {log_path}")


if __name__ == "__main__":
    main()
