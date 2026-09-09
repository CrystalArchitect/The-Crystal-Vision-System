#!/usr/bin/env python3
"""
Check that Clementine's audit log has not been tampered with.

    python3 verify_audit.py                       # the default profile
    python3 verify_audit.py --memory-dir some_dir
    python3 verify_audit.py --show                # also print the entries

Exits non-zero if the chain is broken, so it can be used in a cron job or a
health check. A broken chain means an entry was edited or removed after it was
written — the log is designed so that this cannot happen quietly.
"""

import argparse
import sys
from pathlib import Path

from crystalcore import AuditLog


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--memory-dir", default="clementine_memory",
                    help="the profile folder holding audit.jsonl")
    ap.add_argument("--show", action="store_true", help="print every entry")
    args = ap.parse_args()

    path = Path(args.memory_dir) / "audit.jsonl"
    if not path.exists():
        print(f"No audit log at {path} — nothing has been recorded yet.")
        return 0

    log = AuditLog(path)
    entries = log.entries()
    intact, problems = log.verify()

    if args.show:
        for i, e in enumerate(entries):
            print(f"  {i:>4}  {e.get('at','?'):<25} {e.get('service','?'):<8} "
                  f"{e.get('destination','?'):<24} {e.get('outcome','?'):<8} "
                  f"{str(e.get('hash',''))[:12]}")
        print()

    allowed = sum(1 for e in entries if e.get("outcome") == "allowed")
    refused = sum(1 for e in entries if e.get("outcome") == "refused")
    remote = sorted({e.get("destination") for e in entries
                     if e.get("destination") not in (None, "local")})

    print(f"{path}")
    print(f"  entries   {len(entries)}  ({allowed} allowed, {refused} refused)")
    print(f"  head      {log.head()[:16]}")
    print(f"  offsite   {', '.join(remote) if remote else 'none — everything stayed local'}")

    if intact:
        print("  chain     intact")
        return 0

    print("  chain     BROKEN")
    for p in problems:
        print(f"            {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
