"""Run the whole spine on a JSONL file: decode → ingest → twin report.

    python3 -m services.pipeline services/sample-events/budapest.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .decode import decode_batch
from .ingest import DEFAULT_DB, connect, ingest_events
from .twin import flows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Decode → Ingest → Twin, one shot")
    parser.add_argument("jsonl", help="file of raw events, one JSON object per line")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args(argv)

    raws = []
    for line in Path(args.jsonl).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                raws.append(json.loads(line))
            except json.JSONDecodeError:
                raws.append({"_unparseable": line})

    accepted, quarantined = decode_batch(raws)
    conn = connect(args.db)
    try:
        written = ingest_events(conn, accepted)
        print(f"raw: {len(raws)}  decoded: {len(accepted)}  "
              f"stored new: {written}  quarantined: {len(quarantined)}")
        for q in quarantined:
            print(f"  QUARANTINE: {q['reason']}")
        print("\nTWIN FLOWS")
        for f in flows(conn):
            print(f"  {f['h3']}  {f['class']:<18} {f['events']:>4} events  "
                  f"total {f['total']} {f['unit']}  last {f['last_observed']}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
