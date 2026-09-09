#!/usr/bin/env python3
# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Check relative Markdown links against what git actually tracks.

`.github/workflows/markdown-link-check-config.json` deliberately scopes
markdown-link-check to `^https?://`, because that tool reports
parent-relative local links (`../adr/ADR-0005.md`) as dead even when the
target is right there — reproducible across versions 3.11-3.14, and
independent of config. That was an honest trade, but it left internal
cross-references unchecked entirely, and 62 of them had rotted by the
2026-07-28 review.

Resolving links against `git ls-files` instead of over HTTP sidesteps the
bug completely: no network, no tool, just path arithmetic against the
index. External links stay markdown-link-check's job.

    python3 .github/scripts/check-internal-links.py [--all]

Exits non-zero if any tracked Markdown file links to something that is
neither tracked nor present on disk.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

# Frozen provenance. Their dead links are historical facts about what the
# tree looked like when it was snapshotted, not defects to repair -- the
# same trees the markdownlint and link-check steps already exclude.
EXCLUDED_PREFIXES = ("archive/",)
EXCLUDED_SUBSTRINGS = ("local-snapshot",)

# Known-absent trees, each already tracked as staged debt in
# docs/governance/Migration-Plan.md rather than as link rot. Referring to
# them is intentional: the documents describe where code went and where it
# is going. Listed explicitly so that a *new* broken path still fails.
#
# `vision/` and `core/` are the post-split successors of `src/`: Migration
# Plan Stages 1-2 moved src/apps/ -> vision/apps/ and src/crystalcore/ ->
# core/crystalcore/ in the Code repository. They were absent from this list
# only because no document here had been updated to the new paths yet, so
# nothing exercised them. A document that cites where the code lives *now*
# is doing the same job as one citing where it used to.
KNOWN_ABSENT_ROOTS = (
    "src/", "vision/", "core/",
    "packages/", "scripts/", "tests/", "corpus/",
)

LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

# Links inside code are being *quoted*, not followed -- a document that
# shows `![cover](assets/cover.jpeg)` as an example of markup is not
# claiming that path exists relative to itself. Strip fenced blocks and
# inline spans before matching, or every doc that quotes a link fails.
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INDENTED_FENCE = re.compile(r"^~~~.*?^~~~", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`+[^`\n]*`+")


def strip_code(text: str) -> str:
    """Blank out code regions, preserving line count so any future
    line-numbered reporting still points at the right place."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = FENCE.sub(blank, text)
    text = INDENTED_FENCE.sub(blank, text)
    return INLINE_CODE.sub(blank, text)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return out.split("\n") if out else []


def is_excluded(path: str) -> bool:
    return path.startswith(EXCLUDED_PREFIXES) or any(
        s in path for s in EXCLUDED_SUBSTRINGS
    )


def main(argv: list[str]) -> int:
    check_everything = "--all" in argv
    files = [f for f in tracked_files() if f]
    tracked = set(files)
    dirs = {os.path.dirname(f) for f in files}

    broken: list[tuple[str, str, str]] = []
    checked = 0

    for path in files:
        if not path.endswith(".md"):
            continue
        if not check_everything and is_excluded(path):
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue

        for match in LINK.finditer(strip_code(text)):
            url = match.group(1)
            if url.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
                continue
            target = url.split("#", 1)[0]
            if not target:
                continue  # pure anchor
            checked += 1

            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if resolved.startswith(".."):
                broken.append((path, url, "escapes the repository"))
                continue
            if resolved in tracked or os.path.exists(resolved):
                continue
            bare = resolved.rstrip("/")
            if bare in dirs or any(d.startswith(bare + "/") for d in dirs):
                continue  # link to a directory
            if resolved.startswith(KNOWN_ABSENT_ROOTS):
                continue  # staged debt, see Migration-Plan.md
            broken.append((path, url, "no such tracked file"))

    print(f"internal links checked: {checked}")
    if not broken:
        print("all resolve.")
        return 0

    print(f"broken: {len(broken)}\n")
    for path, url, why in broken:
        print(f"  {path}\n      -> {url}  ({why})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
