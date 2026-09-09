#!/usr/bin/env python3
# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Report which surveyed repositories have moved since the archive read them.

This archive's claims are claims about specific commits, recorded in
`SURVEYED.md`. This script compares each recorded commit against the
repository's current head and says which have moved.

It does **not** fail on staleness. The portfolio moves faster than any
survey of it; drift here is the normal state, not a defect. What the
script removes is silence — the archive can be behind, but it can no
longer be behind *invisibly*, which is exactly how it came to describe a
six-repository portfolio that had eleven, and a specification repository
that it called a web page. It is twelve as of 2026-07-29.

It exits non-zero only when it cannot do its job: a malformed
`SURVEYED.md`, or a repository listed that it cannot parse.

    python3 .github/scripts/check-freshness.py
    python3 .github/scripts/check-freshness.py --local /path/to/checkouts

`--local` points at a directory holding checkouts named after each
repository, which is how to check the seven private ones from somewhere
that cannot reach them, without handing this script credentials.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SURVEY_FILE = Path("SURVEYED.md")
OWNER = "CrystalArchitect"
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{40})`\s*\|\s*([0-9-]+)\s*\|")


def parse_survey() -> list[tuple[str, str, str]]:
    if not SURVEY_FILE.exists():
        sys.exit(f"{SURVEY_FILE} not found — run from the repository root")
    rows = []
    for line in SURVEY_FILE.read_text().splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append((m.group(1), m.group(2), m.group(3)))
    if not rows:
        sys.exit(f"{SURVEY_FILE} lists no repositories — has its table format changed?")
    return rows


def head_of(repo: str, local: Path | None) -> str | None:
    """Current head, or None if unreachable.

    Unreachable is an ordinary outcome, not an error -- seven of the twelve
    repositories are private, and a run without credentials will simply not
    see them. From a session container with the git proxy configured, all
    twelve resolve.

    This docstring claimed "ten of the eleven repositories are private"
    until 2026-07-29. Wrong on both counts: five are public, and privacy
    was not what determined reachability anyway."""
    if local:
        path = local / repo
        if not (path / ".git").is_dir():
            return None
        for ref in ("origin/main", "origin/master", "HEAD"):
            r = subprocess.run(
                ["git", "-C", str(path), "rev-parse", "--verify", "-q", ref],
                capture_output=True, text=True,
            )
            if r.returncode == 0:
                return r.stdout.strip()
        return None

    r = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{OWNER}/{repo}.git", "HEAD"],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return r.stdout.split()[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", type=Path, help="directory of local checkouts")
    args = ap.parse_args()

    rows = parse_survey()
    moved, current, unknown = [], [], []

    for repo, surveyed, when in rows:
        head = head_of(repo, args.local)
        if head is None:
            unknown.append((repo, when))
        elif head == surveyed:
            current.append(repo)
        else:
            moved.append((repo, surveyed, head, when))

    print(f"surveyed repositories: {len(rows)}")
    print(f"  still at the surveyed commit : {len(current)}")
    print(f"  moved since                  : {len(moved)}")
    print(f"  not reachable from here      : {len(unknown)}")

    if moved:
        print("\nMOVED — claims about these were read from an older commit:")
        for repo, surveyed, head, when in moved:
            print(f"  {repo}")
            print(f"      surveyed {surveyed[:12]} on {when}")
            print(f"      now at   {head[:12]}")
        print("\nNot an error. Re-read what changed, then update SURVEYED.md.")

    if unknown:
        print("\nnot reachable without credentials or a checkout "
              "(pass --local to check these):")
        for repo, when in unknown:
            print(f"  {repo}  (surveyed {when})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
