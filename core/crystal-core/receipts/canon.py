# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Canonicalization — versioned, because changing it invalidates old digests.

Two texts that differ only in line endings, trailing whitespace, or runs of
blank lines should count as the same return. Everything else is content.

The version is recorded in every receipt. ``match`` refuses to compare a
fresh text against a receipt written under a different version rather than
silently reporting a false mismatch — the failure is named, not guessed at.
"""

from __future__ import annotations

import json

# Bump ONLY with a new rules block below; old receipts keep their version.
CANON_VERSION = "1"


def canonicalize_text(text: str) -> str:
    """Rules v1: CRLF/CR -> LF; strip trailing whitespace per line; collapse
    runs of blank lines to one; strip leading/trailing blanks; final newline."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    cleaned: list[str] = []
    prev_blank = False
    for line in lines:
        blank = line == ""
        if blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = blank
    return "\n".join(cleaned).strip("\n") + "\n"


def canonicalize_json(obj) -> str:
    """Structured returns: sorted keys, tight separators, real UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
