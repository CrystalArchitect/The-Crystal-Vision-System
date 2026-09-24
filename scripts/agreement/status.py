#!/usr/bin/env python3
"""Report hub agreement ledger status.

Usage:
  python3 scripts/agreement/status.py
  python3 scripts/agreement/status.py --open
  python3 scripts/agreement/status.py --id DEC-C
  python3 scripts/agreement/status.py --json

Canon: no. Crystal stamps via AGREE/REJECT/CANON/INTERIM <id> — see
00_MASTER_INDEX/AGREEMENT-WORKFLOW.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "00_MASTER_INDEX" / "agreement-ledger.yaml"

OPEN_STATUSES = {"proposed"}
ATTENTION_STATUSES = {"proposed", "interim"}


def load_ledger() -> dict:
    text = LEDGER.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        return _minimal_yaml(text)


def _minimal_yaml(text: str) -> dict:
    """Tiny subset parser for this ledger shape (no PyYAML required)."""
    items: list[dict] = []
    current: dict | None = None
    meta: dict = {"items": items}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("version:"):
            meta["version"] = line.split(":", 1)[1].strip()
        elif line.startswith("updated:"):
            meta["updated"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("authority:"):
            meta["authority"] = line.split(":", 1)[1].strip()
        elif line.startswith("  - id:"):
            if current:
                items.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current is not None and line.startswith("    "):
            key, _, val = line.strip().partition(":")
            val = val.strip().strip('"')
            if val == "null":
                val = None
            current[key] = val
    if current:
        items.append(current)
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Hub agreement ledger status")
    parser.add_argument("--open", action="store_true", help="Only proposed items")
    parser.add_argument(
        "--attention",
        action="store_true",
        help="Proposed + interim (needs Crystal eyes)",
    )
    parser.add_argument("--id", help="Show one item by id")
    parser.add_argument("--json", action="store_true", help="Machine-readable dump")
    args = parser.parse_args()

    if not LEDGER.is_file():
        print(f"[ERROR] Ledger missing: {LEDGER}", file=sys.stderr)
        return 1

    data = load_ledger()
    items = list(data.get("items") or [])

    if args.id:
        items = [i for i in items if i.get("id") == args.id]
        if not items:
            print(f"[ERROR] Unknown id: {args.id}", file=sys.stderr)
            return 2

    if args.open:
        items = [i for i in items if i.get("status") in OPEN_STATUSES]
    elif args.attention and not args.id:
        items = [i for i in items if i.get("status") in ATTENTION_STATUSES]

    if args.json:
        print(json.dumps({"updated": data.get("updated"), "items": items}, indent=2))
        return 0

    counts: dict[str, int] = {}
    for i in data.get("items") or []:
        st = str(i.get("status") or "?")
        counts[st] = counts.get(st, 0) + 1

    print("Agreement ledger")
    print(f"  updated:   {data.get('updated')}")
    print(f"  authority: {data.get('authority')}")
    print(f"  file:      {LEDGER.relative_to(ROOT)}")
    print(f"  counts:    {counts}")
    print()
    if not items:
        print("  (no rows match filter)")
        return 0

    print(f"{'ID':<22} {'STATUS':<18} TITLE")
    print("-" * 72)
    for i in items:
        print(
            f"{i.get('id', '?'):<22} {i.get('status', '?'):<18} {i.get('title', '')}"
        )
        if args.id:
            print(f"  source:    {i.get('source')}")
            print(f"  confirmed: {i.get('confirmed')}")
            print(f"  note:      {i.get('note')}")

    print()
    print("Crystal reply shapes: AGREE|REJECT|CANON|INTERIM <id> — note")
    print("Workflow: 00_MASTER_INDEX/AGREEMENT-WORKFLOW.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
