# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The receipt store — capture, byte-exact verify, canonical match, chain.

Layout under one root directory::

    artifacts/                stored canonical snapshots, one file per capture
    receipts.log              append-only JSON lines, each carrying ``prev``
    HEAD                      one JSON line: entry count + hash of last line

Filenames carry the content digest, so two captures in the same second can
never overwrite each other with different content: a different text is a
different digest is a different name. The same text captured twice in the
same second maps to the same artifact bytes — writing them again is
idempotent, and both receipts remain individually checkable.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterator, Optional

from .canon import CANON_VERSION, canonicalize_text

SCHEMA = 1
GENESIS = "0" * 64
_LABEL_RE = re.compile(r"[^a-z0-9-]+")


class ReceiptError(Exception):
    """A receipt operation failed in a way the caller must see."""


class ChainBroken(ReceiptError):
    """The log's hash chain does not verify; ``line_no`` is the first break."""

    def __init__(self, line_no: int, why: str):
        super().__init__(f"receipts.log line {line_no}: {why}")
        self.line_no = line_no
        self.why = why


class CanonVersionMismatch(ReceiptError):
    """A match was requested across canonicalization versions.

    Refusing loudly beats a silent false mismatch: the caller learns the
    receipt predates the current rules, instead of concluding the return
    changed when only the normalisation did.
    """


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Receipt:
    """One captured return. ``sha256`` is over the artifact's exact bytes."""

    schema: int
    canon_version: str
    timestamp: str
    label: str
    filename: str
    sha256: str
    bytes: int
    prev: str

    def to_line(self) -> str:
        return json.dumps(
            {
                "schema": self.schema,
                "canon_version": self.canon_version,
                "timestamp": self.timestamp,
                "label": self.label,
                "filename": self.filename,
                "sha256": self.sha256,
                "bytes": self.bytes,
                "prev": self.prev,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_line(cls, line: str) -> "Receipt":
        d = json.loads(line)
        return cls(**{k: d[k] for k in (
            "schema", "canon_version", "timestamp", "label",
            "filename", "sha256", "bytes", "prev",
        )})


class ReceiptStore:
    """A directory of artifacts plus their hash-chained receipt log."""

    def __init__(self, root: Path | str, clock: Optional[Callable[[], datetime]] = None):
        self.root = Path(root)
        self.artifacts = self.root / "artifacts"
        self.log = self.root / "receipts.log"
        self.head_file = self.root / "HEAD"
        self._clock = clock or _utcnow
        self.artifacts.mkdir(parents=True, exist_ok=True)

    # -- capture -----------------------------------------------------------

    def capture(self, text: str, label: str = "return") -> Receipt:
        """Canonicalize, store, and chain one behavioural return."""
        safe_label = _LABEL_RE.sub("-", label.lower()).strip("-") or "return"
        canonical = canonicalize_text(text)
        payload = canonical.encode("utf-8")
        digest = _sha256_hex(payload)
        ts = self._clock().strftime("%Y-%m-%dT%H:%M:%SZ")
        filename = f"{safe_label}-{ts.replace(':', '')}-{digest[:12]}.md"

        path = self.artifacts / filename
        if path.exists() and path.read_bytes() != payload:
            # Unreachable while the digest is in the name; kept as a guard so
            # a future naming change cannot silently reintroduce clobbering.
            raise ReceiptError(f"artifact name collision with different content: {filename}")
        path.write_bytes(payload)

        receipt = Receipt(
            schema=SCHEMA,
            canon_version=CANON_VERSION,
            timestamp=ts,
            label=safe_label,
            filename=filename,
            sha256=digest,
            bytes=len(payload),
            prev=self._tail_hash(),
        )
        with self.log.open("a", encoding="utf-8") as f:
            f.write(receipt.to_line() + "\n")
        self._write_head()
        return receipt

    # -- the two questions, kept apart -------------------------------------

    def verify(self, filename: str) -> tuple[bool, str, str]:
        """Byte-exact: has the stored artifact changed since its receipt?

        Returns ``(ok, expected_sha256, actual_sha256)``. The raw bytes on
        disk are hashed — nothing is canonicalized first, so an edit inside
        canonicalization's kernel (trailing whitespace, blank-line runs)
        still fails, which is the point of keeping this question separate.
        """
        receipt = self._receipt_for(filename)
        path = self.artifacts / filename
        if not path.exists():
            raise ReceiptError(f"artifact missing: {filename}")
        actual = _sha256_hex(path.read_bytes())
        return actual == receipt.sha256, receipt.sha256, actual

    def match(self, text: str, filename: str) -> tuple[bool, str, str]:
        """Canonical: does freshly produced text equal the recorded return?

        Returns ``(ok, expected_sha256, actual_sha256)``. Raises
        :class:`CanonVersionMismatch` when the receipt was written under
        different canonicalization rules than this code carries.
        """
        receipt = self._receipt_for(filename)
        if receipt.canon_version != CANON_VERSION:
            raise CanonVersionMismatch(
                f"receipt {filename} used canon v{receipt.canon_version}, "
                f"this code canonicalizes with v{CANON_VERSION}"
            )
        actual = _sha256_hex(canonicalize_text(text).encode("utf-8"))
        return actual == receipt.sha256, receipt.sha256, actual

    # -- the chain ----------------------------------------------------------

    def receipts(self) -> Iterator[Receipt]:
        if not self.log.exists():
            return
        with self.log.open(encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line:
                    yield Receipt.from_line(line)

    def check_chain(self) -> tuple[int, str]:
        """Walk the whole log; return ``(entries, head_hash)`` or raise.

        Each line must parse, carry the expected ``prev`` (the SHA-256 of the
        previous line's exact serialized bytes; zeros at genesis), and the
        HEAD file, if present, must agree with the recomputed tail. Editing,
        reordering, or deleting any line breaks every link after it.
        """
        count, prev = self._walk_chain()
        if self.head_file.exists():
            head = json.loads(self.head_file.read_text(encoding="utf-8"))
            if head.get("head") != prev or head.get("entries") != count:
                raise ChainBroken(count, "HEAD file disagrees with recomputed chain")
        return count, prev

    def _walk_chain(self) -> tuple[int, str]:
        """The chain walk alone — no HEAD comparison.

        ``_write_head`` must use this: at that moment the HEAD on disk is the
        stale one being replaced, and validating against it would break every
        second capture.
        """
        prev = GENESIS
        count = 0
        if self.log.exists():
            with self.log.open(encoding="utf-8") as f:
                for line_no, raw in enumerate(f, start=1):
                    line = raw.rstrip("\n")
                    if not line:
                        continue
                    try:
                        receipt = Receipt.from_line(line)
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        raise ChainBroken(line_no, f"unparseable receipt ({e})") from e
                    if receipt.prev != prev:
                        raise ChainBroken(
                            line_no,
                            f"prev is {receipt.prev[:12]}…, chain expects {prev[:12]}…",
                        )
                    prev = _sha256_hex(line.encode("utf-8"))
                    count += 1
        return count, prev

    def head(self) -> dict:
        """The anchorable summary: entry count and hash of the last line.

        This is the one line to feed the umbrella's OpenTimestamps flow.
        An anchored head witnesses the entire chain beneath it; the log
        alone only ever asserts its own clock.
        """
        count, tail = self.check_chain()
        return {"canon_version": CANON_VERSION, "entries": count, "head": tail, "schema": SCHEMA}

    # -- internals ----------------------------------------------------------

    def _tail_hash(self) -> str:
        prev = GENESIS
        if self.log.exists():
            with self.log.open(encoding="utf-8") as f:
                for raw in f:
                    line = raw.rstrip("\n")
                    if line:
                        prev = _sha256_hex(line.encode("utf-8"))
        return prev

    def _write_head(self) -> None:
        count, tail = self._walk_chain()
        self.head_file.write_text(
            json.dumps(
                {"canon_version": CANON_VERSION, "entries": count, "head": tail, "schema": SCHEMA},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )

    def _receipt_for(self, filename: str) -> Receipt:
        found = [r for r in self.receipts() if r.filename == filename]
        if not found:
            raise ReceiptError(f"no receipt for {filename}")
        digests = {r.sha256 for r in found}
        if len(digests) > 1:
            # Cannot happen while names embed the digest; loud if it ever does.
            raise ReceiptError(f"conflicting receipts for {filename}")
        return found[-1]
