#!/usr/bin/env python3
"""Chaos Engine CLI — fan one question to weave seats via live stack.

    python3 scripts/chaos/run.py --topic "Where is each seat?"
    python3 scripts/chaos/run.py --seats deepseek,moonshot.kimi,local.open --out /tmp/chaos.md

Canon: no. Counts are not verdicts. Human publishes.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crystal_platform.chaos import DEFAULT_CHAOS_SEATS, ChaosEngine


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chaos Engine — multi-seat matrix fan-out")
    parser.add_argument(
        "--topic",
        default="Stack is live: Siri→Portal→CrystalCore.OS→TAI. Where is each seat?",
        help="Question asked independently to every seat",
    )
    parser.add_argument(
        "--seats",
        default="",
        help=f"comma-separated provider ids (default: {','.join(DEFAULT_CHAOS_SEATS)})",
    )
    parser.add_argument(
        "--out",
        default="",
        help="markdown ledger path (default: 14_AI_INTERACTIONS/chaos-ledger/<stamp>.md)",
    )
    args = parser.parse_args(argv)

    seats = tuple(s.strip() for s in args.seats.split(",") if s.strip()) or None
    engine = ChaosEngine()
    result = engine.run(args.topic, seats=seats)

    print(f"Chaos Engine run {result.run_id}")
    print(
        f"Cross-compare: asked={result.cross_compare['seats_asked']} "
        f"ok={result.cross_compare['seats_ok']} "
        f"silent={result.cross_compare['seats_silent']} "
        f"statuses={result.cross_compare['status_counts']}"
    )
    for r in result.replies:
        mark = "SILENT" if r.silent else r.status
        preview = r.text.replace("\n", " ")[:100]
        print(f"  {r.provider_id:>20} [{mark}] {preview}")

    if args.out:
        out = Path(args.out)
    else:
        stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = ROOT / "14_AI_INTERACTIONS" / "chaos-ledger" / f"{stamp}-{result.run_id[:8]}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.markdown(), encoding="utf-8")
    print(f"\nLedger: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
