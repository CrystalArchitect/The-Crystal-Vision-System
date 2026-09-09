#!/usr/bin/env python3
# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Verify the site's content set is a faithful mirror of umbrella canon.

`vision/site/src/content/` is a copy of `mythos/content/` from the
umbrella repository. Copies drift. Before this check, drift was found by
reading both trees and diffing by hand -- which is how two documents
diverged and nine more were never copied at all, undetected for weeks.

## Why this pins a commit instead of tracking the umbrella's main

The obvious design -- compare against the umbrella's latest main -- has a
failure mode this repository has already been bitten by once, and
documented in `core/crystalcore/requirements-bridge.txt`: a dependency
written as an open range "broke CI on every commit without anything in
this repository changing." Comparing against a moving target does the
same thing. Someone edits canon in the umbrella, and *this* repository
goes red having done nothing.

So the mirror records the exact canon commit it was taken from, in
`vision/site/src/content/.canon-source`. This check verifies the content
matches *that* commit. Then:

  * editing a site copy by hand  -> red, which is the drift we want caught
  * canon moving forward         -> green, and the pin is simply behind

Bumping the pin is a deliberate act: re-copy the content, update the
file, and the diff shows exactly what became public.

## What fails, and what only reports

**Fails**: a document present in both trees whose bytes differ. That can
only happen if one copy was edited, which is the defect.

**Reports, does not fail**: canon documents with no counterpart here.
Copying canon to the site *publishes* it, and publication is the
maintainer's decision, not a build's. A missing document is news, not an
error.

    python3 .github/scripts/check-canon-mirror.py

Set CANON_LOCAL to an existing umbrella checkout to skip the clone
(useful offline, and for testing this script).
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

UMBRELLA = "https://github.com/CrystalArchitect/TerAustralis-Incognita.git"
CANON_SUBDIR = "mythos/content"
SITE_CONTENT = Path("vision/site/src/content")
PIN_FILE = SITE_CONTENT / ".canon-source"

# Same filename, two entirely different works: the umbrella's is a design
# overview that opens by saying most components remain at concept stage;
# the site's is a Built-vs-Vision map. Mirroring either over the other
# destroys a document, so this pair is excluded by name and by intent.
NOT_A_COPY = {"ARCHITECTURE.md"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def read_pin() -> str:
    if not PIN_FILE.exists():
        sys.exit(f"missing {PIN_FILE} — the mirror does not record its source commit")
    for line in PIN_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    sys.exit(f"{PIN_FILE} contains no commit sha")


def canon_dir(pin: str) -> Path:
    local = os.environ.get("CANON_LOCAL")
    if local:
        print(f"using local umbrella checkout: {local}")
        return Path(local) / CANON_SUBDIR

    tmp = Path(tempfile.mkdtemp(prefix="canon-"))
    # The umbrella is public, so this needs no credentials -- deliberately,
    # because a cross-repo token would be a standing secret in a repository
    # that only needs to read published text.
    subprocess.run(
        ["git", "init", "-q", str(tmp)], check=True
    )
    subprocess.run(
        ["git", "-C", str(tmp), "remote", "add", "origin", UMBRELLA], check=True
    )
    subprocess.run(
        ["git", "-C", str(tmp), "fetch", "-q", "--depth", "1", "origin", pin],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp), "checkout", "-q", "FETCH_HEAD"], check=True
    )
    return tmp / CANON_SUBDIR


def main() -> int:
    if not SITE_CONTENT.is_dir():
        sys.exit(f"run from the repository root; {SITE_CONTENT} not found")

    pin = read_pin()
    print(f"canon pinned at {pin}")
    canon = canon_dir(pin)
    if not canon.is_dir():
        sys.exit(f"canon directory not found at {canon}")

    drifted: list[str] = []
    unmirrored: list[str] = []
    matched = 0

    for src in sorted(canon.glob("*.md")):
        name = src.name
        if name in NOT_A_COPY:
            continue
        dst = SITE_CONTENT / name
        if not dst.exists():
            unmirrored.append(name)
        elif sha(src) != sha(dst):
            drifted.append(name)
        else:
            matched += 1

    print(f"canon documents mirrored and identical: {matched}")

    if unmirrored:
        print(f"\nnot mirrored to the site ({len(unmirrored)}) — not an error, "
              f"publishing is a decision:")
        for n in unmirrored:
            print(f"  {n}")

    if drifted:
        print(f"\nDRIFT — present in both trees, contents differ ({len(drifted)}):")
        for n in drifted:
            print(f"  {n}")
            print(f"      canon {sha(canon / n)}   site {sha(SITE_CONTENT / n)}")
        print("\nA copy was edited. Re-copy from canon, or if canon should change, "
              "change it in the umbrella and bump .canon-source.")
        return 1

    print("\nmirror is faithful.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
