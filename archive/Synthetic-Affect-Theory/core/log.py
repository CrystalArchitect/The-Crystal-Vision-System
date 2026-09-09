# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CycleLogger — structured JSONL cycle log (track, gap, label, closure).

Determinism (F2): no wall-clock anywhere.
  ts    = log line sequence number, incremented once per line written
  cycle = loop cycle number, supplied by the caller (incremented once per
          run_cycle) — ts and cycle are not identical; both carry information.
Four lines per turn with a tracked event (track, gap_*, label, closure),
three without. Logs are byte-identical on re-run:
`git diff --stat examples/logs/` empty is a real check.

Truncate-on-construct is what makes a re-run byte-identical rather than an
accumulating artefact — but it means two CycleLoggers sharing a path would
silently destroy each other's lines: the second one's __init__ truncates
what the first already wrote, and interleaves its own lines into the same
file afterward. `Loop`'s default log_path is one literal string shared by
every default-constructed Loop, so this was reachable with zero arguments —
loop2 = Loop() while loop1 (also default-constructed) was still alive
corrupted loop1's log. Fixed by refusing the second construction outright:
loud and immediate beats a silently corrupted log every time.
"""
from __future__ import annotations

import json
import pathlib
import weakref
from typing import Any, Dict, List


class CycleLogger:
    #: path (resolved, absolute) -> the live CycleLogger currently writing
    #: it. A WeakValueDictionary so a CycleLogger that's gone out of scope
    #: releases its claim on the path without any explicit teardown.
    _owners: "weakref.WeakValueDictionary[str, CycleLogger]" = weakref.WeakValueDictionary()

    def __init__(self, path: str | pathlib.Path):
        self.path = pathlib.Path(path)
        resolved = str(self.path.resolve())
        owner = CycleLogger._owners.get(resolved)
        if owner is not None:
            raise RuntimeError(
                f"CycleLogger({self.path!s}) — another CycleLogger is already "
                "writing this path. Truncate-on-construct plus a shared path "
                "would silently corrupt both logs (the second truncates what "
                "the first wrote, then interleaves its own lines into it). "
                "Give each Loop/Runtime a distinct log_path."
            )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.ts = 0
        # fresh log per run — logs are outputs, not accumulating artefacts
        self.path.write_text("", encoding="utf-8")
        CycleLogger._owners[resolved] = self

    def log(self, op: str, data: Dict[str, Any], cycle: int) -> None:
        self.ts += 1
        entry = {"cycle": cycle, "op": op, "ts": self.ts, "data": data}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    def read_all(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines if line.strip()]
