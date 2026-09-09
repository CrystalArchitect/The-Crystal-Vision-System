# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Selftest — python3 -m core.selftest

Strict (F4): exact labels, exact strategies, exact log shape — the loop
proves itself, exit 0 if green. No assert statements (F10) — every check
raises with a message and survives `python3 -O`.
"""
from __future__ import annotations

import pathlib
import sys
import tempfile

from .loop import Loop


def _check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"[selftest] FAIL — {msg}")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        loop = Loop(store_path=":memory:", log_path=str(pathlib.Path(td) / "selftest.jsonl"))

        # Cycle 1 — first gap: uncertain -> ask (4 lines: track, gap_opened, label,
        # closure — nothing pending yet, so no closure_outcome).
        r1 = loop.run_cycle(expected="answer", actual="no answer", event={"q": "what is SAT?"})
        _check(r1["gap"] is not None, "cycle 1 should open a gap")
        _check(r1["label"] == "uncertain", f"cycle 1 label {r1['label']!r}, want 'uncertain'")
        _check(r1["decision"].strategy == "ask", f"cycle 1 strategy {r1['decision'].strategy!r}, want 'ask'")
        _check(r1["decision"].outcome == "pending", "cycle 1 decision must not grade itself")

        # Cycle 2 — gap closes: closed -> stop (4 lines: gap_none, closure_outcome
        # judging cycle 1's "ask" as worked, label, closure).
        r2 = loop.run_cycle(expected="answer", actual="answer")
        _check(r2["gap"] is None, "cycle 2 should close the gap")
        _check(r2["label"] == "closed", f"cycle 2 label {r2['label']!r}, want 'closed'")
        _check(r2["decision"].strategy == "stop", f"cycle 2 strategy {r2['decision'].strategy!r}, want 'stop'")

        # Cycle 3 — gap reopens after closure: reopened -> rephrase (5 lines: track,
        # gap_opened, closure_outcome judging cycle 2's "stop" as failed, label, closure).
        r3 = loop.run_cycle(expected="answer", actual="answer drifted", event={"q": "what is SAT, again?"})
        _check(r3["gap"] is not None, "cycle 3 should reopen a gap")
        _check(r3["label"] == "reopened", f"cycle 3 label {r3['label']!r}, want 'reopened'")
        _check(r3["decision"].strategy == "rephrase", f"cycle 3 strategy {r3['decision'].strategy!r}, want 'rephrase'")

        entries = loop.logger.read_all()
        _check(len(entries) == 13, f"expected exactly 13 log entries, got {len(entries)}")

        ops = [e["op"] for e in entries]
        want_ops = [
            "track", "gap_opened", "label", "closure",
            "gap_none", "closure_outcome", "label", "closure",
            "track", "gap_opened", "closure_outcome", "label", "closure",
        ]
        _check(ops == want_ops, f"op sequence {ops} != {want_ops}")

        cycles = [e["cycle"] for e in entries]
        _check(cycles == [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
               f"cycle grouping {cycles} — decisions must be judged by a later cycle")
        _check([e["ts"] for e in entries] == list(range(1, 14)),
               "ts must be the log line sequence 1..13 — cycle is cycle, ts is measure")

        labels = [e["data"]["label"] for e in entries if e["op"] == "label"]
        _check(labels == ["uncertain", "closed", "reopened"], f"labels exact check failed: {labels}")

        outcomes = [e["data"]["outcome"] for e in entries if e["op"] == "closure_outcome"]
        _check(outcomes == ["worked", "failed"],
               f"closure_outcome must judge each prior decision: {outcomes}")

        rate = loop.closure_success_rate()
        _check(rate == 1 / 2, f"closure success rate {rate}, want 0.5 (1 worked of 2 judged)")

        _check(loop.cycle == 3, f"loop.cycle is {loop.cycle}, want 3 after three run_cycle calls")
        _check(loop.store.path is None, ":memory: store must not carry a file path")

    print(
        "[selftest] PASS — 13 entries — labels exact: uncertain, closed, reopened — "
        "strategies: ask, stop, rephrase — closure success rate 0.50"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
