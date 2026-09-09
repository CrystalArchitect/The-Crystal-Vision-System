# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for the receipt store — proves the separations are real.

    python3 -m receipts.selftest

The suite's centre of gravity is the two failure modes this module exists
to close: a verify that canonicalizes (so whitespace edits pass), and an
append-only log that is only append-only by good manners (so history can
be rewritten silently). Both are attacked directly here.
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .canon import CANON_VERSION, canonicalize_text
from .store import CanonVersionMismatch, ChainBroken, GENESIS, ReceiptError, ReceiptStore

SAMPLE = "Session return.\nThe lattice is a design, not a machine.\nNon Solus.\n"


def _store(tmp: str, times=None) -> ReceiptStore:
    if times is None:
        return ReceiptStore(Path(tmp))
    seq = iter(times)
    return ReceiptStore(Path(tmp), clock=lambda: next(seq))


_T0 = datetime(2026, 8, 9, 3, 0, 0, tzinfo=timezone.utc)


def test_capture_writes_artifact_receipt_and_head():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE, label="continuity")
        assert (s.artifacts / r.filename).exists(), "artifact must be on disk"
        assert r.prev == GENESIS, "first receipt chains from genesis"
        assert r.canon_version == CANON_VERSION, "every receipt names its canon rules"
        head = json.loads(s.head_file.read_text())
        assert head["entries"] == 1


def test_verify_passes_untouched():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE)
        ok, expected, actual = s.verify(r.filename)
        assert ok and expected == actual


def test_verify_is_byte_exact_not_canonical():
    """The sketch's hole: an edit canonicalization erases must still fail."""
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE)
        path = s.artifacts / r.filename
        tampered = path.read_text().replace("\n", "  \n", 1)  # trailing spaces only
        path.write_text(tampered)
        assert canonicalize_text(tampered) == canonicalize_text(SAMPLE), \
            "the tamper must be invisible to canonicalization for this test to bite"
        ok, _, _ = s.verify(r.filename)
        assert not ok, "byte-exact verify must catch a canonicalization-invisible edit"


def test_match_accepts_messy_rerelay():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE)
        messy = ("\n\nSession return.   \r\nThe lattice is a design, not a machine.  \r\n"
                 "Non Solus.\r\n\r\n\r\n")
        ok, _, _ = s.match(messy, r.filename)
        assert ok, "line endings, trailing spaces and edge blank runs are not content"
        # A blank line inserted where the original had none IS content: single
        # blanks are structure under canon v1, only runs collapse.
        restructured = "Session return.\n\nThe lattice is a design, not a machine.\nNon Solus.\n"
        ok, _, _ = s.match(restructured, r.filename)
        assert not ok, "new paragraph structure must not match"


def test_match_rejects_different_content():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE)
        ok, _, _ = s.match(SAMPLE + "Lattice coherence: 100%\n", r.filename)
        assert not ok, "an added claim is content, and content must not match"


def test_same_second_different_content_never_collides():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0, _T0])  # identical timestamps
        r1 = s.capture("first return", label="x")
        r2 = s.capture("second return", label="x")
        assert r1.filename != r2.filename, "digest-in-name must separate same-second captures"
        assert s.verify(r1.filename)[0] and s.verify(r2.filename)[0]


def test_same_second_same_content_is_idempotent_and_unambiguous():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0, _T0])
        r1 = s.capture(SAMPLE, label="x")
        r2 = s.capture(SAMPLE, label="x")
        assert r1.filename == r2.filename and r1.sha256 == r2.sha256
        assert s.verify(r1.filename)[0], "duplicate receipts agree, so verify stays unambiguous"
        assert s.check_chain()[0] == 2, "both captures are chain entries"


def test_chain_links_are_real():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.capture("one")
        s.capture("two")
        lines = [l for l in s.log.read_text().splitlines() if l]
        import hashlib
        expected_prev = hashlib.sha256(lines[0].encode()).hexdigest()
        assert json.loads(lines[1])["prev"] == expected_prev


def test_editing_history_breaks_the_chain():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.capture("one"); s.capture("two"); s.capture("three")
        lines = s.log.read_text().splitlines()
        forged = json.loads(lines[0]); forged["label"] = "rewritten"
        lines[0] = json.dumps(forged, sort_keys=True, separators=(",", ":"))
        s.log.write_text("\n".join(lines) + "\n")
        try:
            s.check_chain()
            assert False, "an edited line one must break the chain"
        except ChainBroken as e:
            assert e.line_no == 2, "the break surfaces at the first line whose prev no longer holds"


def test_deleting_history_breaks_the_chain():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.capture("one"); s.capture("two"); s.capture("three")
        lines = s.log.read_text().splitlines()
        s.log.write_text("\n".join(lines[:1] + lines[2:]) + "\n")
        try:
            s.check_chain()
            assert False, "a deleted middle line must break the chain"
        except ChainBroken:
            pass


def test_canon_version_mismatch_is_loud():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        r = s.capture(SAMPLE)
        lines = s.log.read_text().splitlines()
        old = json.loads(lines[-1]); old["canon_version"] = "0"
        # Rebuild the log so the chain still verifies, then ask for a match.
        import hashlib
        rebuilt = json.dumps(old, sort_keys=True, separators=(",", ":"))
        s.log.write_text(rebuilt + "\n")
        s.head_file.unlink()
        try:
            s.match(SAMPLE, r.filename)
            assert False, "a cross-version match must refuse, not report a false mismatch"
        except CanonVersionMismatch:
            pass


def test_head_witnesses_the_tail():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.capture("one"); s.capture("two")
        import hashlib
        last = [l for l in s.log.read_text().splitlines() if l][-1]
        h = s.head()
        assert h["head"] == hashlib.sha256(last.encode()).hexdigest()
        assert h["entries"] == 2
        assert json.loads(s.head_file.read_text()) == h, "HEAD on disk is the anchorable line"


def test_tampered_head_file_is_caught():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.capture("one")
        head = json.loads(s.head_file.read_text()); head["entries"] = 99
        s.head_file.write_text(json.dumps(head, sort_keys=True, separators=(",", ":")) + "\n")
        try:
            s.check_chain()
            assert False, "a HEAD that disagrees with the log must be named"
        except ChainBroken:
            pass


def test_labels_are_sanitised():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE, label="../Sneaky Label!/..")
        assert "/" not in r.filename and " " not in r.filename
        assert (s.artifacts / r.filename).exists()
        assert (s.artifacts / r.filename).resolve().parent == s.artifacts.resolve(), \
            "a hostile label must not escape the artifacts directory"


def test_missing_receipt_and_missing_artifact_are_loud():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp, [_T0])
        r = s.capture(SAMPLE)
        try:
            s.verify("never-captured.md"); assert False
        except ReceiptError:
            pass
        (s.artifacts / r.filename).unlink()
        try:
            s.verify(r.filename); assert False
        except ReceiptError:
            pass


def main() -> int:
    tests = [
        test_capture_writes_artifact_receipt_and_head,
        test_verify_passes_untouched,
        test_verify_is_byte_exact_not_canonical,
        test_match_accepts_messy_rerelay,
        test_match_rejects_different_content,
        test_same_second_different_content_never_collides,
        test_same_second_same_content_is_idempotent_and_unambiguous,
        test_chain_links_are_real,
        test_editing_history_breaks_the_chain,
        test_deleting_history_breaks_the_chain,
        test_canon_version_mismatch_is_loud,
        test_head_witnesses_the_tail,
        test_tampered_head_file_is_caught,
        test_labels_are_sanitised,
        test_missing_receipt_and_missing_artifact_are_loud,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. A receipt that can be quietly rewritten is not a receipt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
