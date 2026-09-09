#!/usr/bin/env python3
"""Build a deterministic hash manifest of the creative work.

Why this exists
---------------
The repository can prove *what* it contains and *in what order* things were
committed. It cannot prove *when* — git timestamps are written by whoever
makes the commit and can be set to anything. Nor can it prove anything to
someone who does not trust the author: the whole history could be rebuilt.

This tool produces one sorted, deterministic list of every creative file and
its SHA-256. That manifest is itself a file with a hash, and that single hash
is what gets anchored to Bitcoin with OpenTimestamps — one proof covering the
entire body of work, for free, with no token, no wallet and no cryptocurrency
touched at any point.

What the resulting proof does and does not say
----------------------------------------------
It says: these exact bytes existed no later than this block.
It does not say: who made them, or that they are original.

That distinction matters here. See `docs/governance/PROVENANCE-TIMESTAMPS.md`.

Usage
-----
    python3 mythos/tools/provenance.py            # write the manifest
    python3 mythos/tools/provenance.py --check    # verify nothing drifted
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "mythos" / "MANIFEST.sha256"
PROOFS = REPO / "mythos" / "proofs"

# What counts as the creative work. Deliberately not the whole repository:
# build output and dependencies are derived, and hashing them would make the
# manifest churn on every rebuild while proving nothing about authorship.
ROOTS = [
    "mythos/art",
    "mythos/music",
    "mythos/content",
    "mythos/teraustralis",
    "mythos/crystalcore-os",
    "mythos/COVENANT.md",
    "mythos/NAMES.md",
    "mythos/CRYSTALCORE-OS.md",
    "mythos/CRYSTALCORE-OS-KNOWLEDGE.md",
]

EXCLUDE_PARTS = {".git", "node_modules", "build", "dist", ".svelte-kit", "__pycache__",
                 "proofs"}
EXCLUDE_NAMES = {"MANIFEST.sha256", "MANIFEST.sha256.ots", ".DS_Store"}


def eligible(path: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    if path.name in EXCLUDE_NAMES:
        return False
    return not EXCLUDE_PARTS.intersection(path.parts)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect() -> list[tuple[str, str]]:
    seen: set[Path] = set()
    for root in ROOTS:
        target = REPO / root
        if not target.exists():
            continue
        candidates = target.rglob("*") if target.is_dir() else [target]
        seen.update(p for p in candidates if eligible(p))
    # Sorted by POSIX path so the manifest is byte-identical on any machine.
    return sorted(
        ((p.relative_to(REPO).as_posix(), digest(p)) for p in seen),
        key=lambda row: row[0],
    )


def render(rows: list[tuple[str, str]]) -> str:
    # sha256sum-compatible, so `sha256sum -c` works without this script.
    return "".join(f"{h}  {path}\n" for path, h in rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="compare against the committed manifest instead of rewriting it",
    )
    args = ap.parse_args()

    rows = collect()
    body = render(rows)
    root = hashlib.sha256(body.encode()).hexdigest()

    if args.check:
        if not MANIFEST.exists():
            print("no manifest committed yet — run without --check", file=sys.stderr)
            return 1
        current = MANIFEST.read_text(encoding="utf-8")
        if current == body:
            print(f"manifest matches: {len(rows)} files, root {root}")
            return 0
        print("manifest is stale — the work has changed since it was written")
        old = dict(
            (line.split("  ", 1)[1], line.split("  ", 1)[0])
            for line in current.splitlines()
            if "  " in line
        )
        new = dict((path, h) for path, h in rows)
        for path in sorted(set(new) - set(old)):
            print(f"  added    {path}")
        for path in sorted(set(old) - set(new)):
            print(f"  removed  {path}")
        for path in sorted(set(old) & set(new)):
            if old[path] != new[path]:
                print(f"  changed  {path}")
        return 1

    # A proof attests one exact manifest. If the manifest is about to change
    # and a proof exists, that proof does not become false — it becomes a true
    # statement about a state this file no longer describes. Upgrading it later
    # would refresh a proof for work that has moved on, and leave the
    # repository looking anchored when its current state is not.
    #
    # So the old proof is archived beside the manifest it attests, which is the
    # only form in which it stays meaningful, and a fresh stamp is taken for
    # the new state. Two dated proofs standing side by side is what this is
    # supposed to look like.
    existing = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else None
    proof = MANIFEST.with_suffix(MANIFEST.suffix + ".ots")
    if existing is not None and existing != body and proof.exists():
        stamp_date = date.today().isoformat()
        PROOFS.mkdir(exist_ok=True)
        keep_manifest = PROOFS / f"{stamp_date}-MANIFEST.sha256"
        keep_proof = PROOFS / f"{stamp_date}-MANIFEST.sha256.ots"
        n = 2
        while keep_manifest.exists() or keep_proof.exists():
            keep_manifest = PROOFS / f"{stamp_date}-{n}-MANIFEST.sha256"
            keep_proof = PROOFS / f"{stamp_date}-{n}-MANIFEST.sha256.ots"
            n += 1
        keep_manifest.write_text(existing, encoding="utf-8")
        keep_proof.write_bytes(proof.read_bytes())
        proof.unlink()
        print(f"the work changed, so the old proof was archived as a pair:")
        print(f"  {keep_manifest.relative_to(REPO)}")
        print(f"  {keep_proof.relative_to(REPO)}")
        print("it still attests the state it was made for. A fresh stamp is")
        print("needed for this one.\n")

    MANIFEST.write_text(body, encoding="utf-8")
    print(f"wrote {MANIFEST.relative_to(REPO)}: {len(rows)} files")
    print(f"root hash: {root}")
    print()
    print("To anchor it (needs network to the OpenTimestamps calendars):")
    print(f"    ots stamp {MANIFEST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
