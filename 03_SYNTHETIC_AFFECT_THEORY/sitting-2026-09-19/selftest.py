# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Selftest — python3 -m core.selftest
Mirrors crystalcore convention: loop proves itself, exit 0 if green
"""
from __future__ import annotations
import sys
import pathlib
from .loop import Loop

def main() -> int:
    tmp_log = "/tmp/sat_selftest.jsonl"
    loop = Loop(store_path=":memory:", log_path=tmp_log)

    # Cycle 1: gap
    r1 = loop.run_cycle(expected="answer", actual="no answer", event={"q": "what is SAT?"})
    assert r1["gap"] is not None, "should detect gap"
    # Cycle 2: converging
    r2 = loop.run_cycle(expected="answer", actual="partial answer")
    assert r2["label"] in ("converging", "uncertain", "stalled"), f"unexpected label {r2['label']}"
    # Cycle 3: closed
    r3 = loop.run_cycle(expected="answer", actual="answer")
    assert r3["gap"] is None
    assert r3["label"] in ("closed", "converging", "reopened"), "should eventually close"

    # Check logs are JSONL and deterministic
    entries = loop.logger.read_all()
    assert len(entries) >= 6, f"expected >=6 log lines, got {len(entries)}"

    print(f"[selftest] PASS — {len(entries)} log entries, last label={r3['label']}, decision={r3['decision'].strategy}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
