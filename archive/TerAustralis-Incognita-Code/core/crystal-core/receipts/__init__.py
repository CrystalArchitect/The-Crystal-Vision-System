# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Receipts — tamper-evident records of what a companion actually said.

A behavioural return (a text a model produced) is captured, canonicalized,
hashed, and appended to a hash-chained log. Later, anyone with the directory
can check two different questions, which this module keeps deliberately
separate because conflating them is the classic hole in receipt schemes:

  * ``verify``  — has this stored artifact changed since its receipt was
    written? Byte-exact: the artifact's raw bytes are hashed, nothing is
    normalised first. An edit that survives canonicalization (trailing
    whitespace, a collapsed blank line) still fails, as it must.
  * ``match``   — does this freshly produced text equal a recorded return?
    Canonical: the fresh text is normalised under the receipt's recorded
    canonicalization version, then compared by digest.

Every receipt carries ``prev`` — the SHA-256 of the previous receipt line —
so editing or deleting any past entry breaks every link after it
(``check_chain`` names the first broken line). The chain head is exported to
``HEAD``; anchoring that one line externally (the umbrella repository's
OpenTimestamps flow, ``mythos/tools/stamp.sh``) buys witnessed time, which an
append-only file on its own can never provide.

What a receipt proves, and does not — the same register as the umbrella's
``provenance.py``:

  It says: these exact bytes existed, in this order, no later than whenever
  the chain head was last anchored.
  It does not say: who produced them, that the producing model is unchanged,
  or that the content of the return is true. Hashing a claim does not make
  the claim so; a fabricated telemetry line, receipted and anchored, becomes
  a durable record of a fabrication and nothing more.

Vision: the substrate of a "same someone" continuity metric.
Reality (labeled): a hash-chained SHA-256 receipt log over text artifacts,
stdlib-only, with byte-exact verification and canonical matching kept apart.

    python3 -m receipts.selftest
"""

from .canon import CANON_VERSION, canonicalize_json, canonicalize_text
from .store import (
    CanonVersionMismatch,
    ChainBroken,
    ReceiptError,
    ReceiptStore,
)

__version__ = "0.1.0"

__all__ = [
    "CANON_VERSION",
    "CanonVersionMismatch",
    "ChainBroken",
    "ReceiptError",
    "ReceiptStore",
    "canonicalize_json",
    "canonicalize_text",
]
