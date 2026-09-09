# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""A backup as the anchor the record cannot be for itself.

tests/test_audit_visibility.py pins what the chain catches and what it does
not: an entry altered, cut from the middle, or reordered is caught; entries
removed from the *end* are not, because a chain with its tail cut off is a
shorter chain that verifies perfectly. Nothing inside a file can prove what
is missing from the end of it.

The usual fix is an anchor outside the file. Here that is worse than the
problem — publishing the head anywhere is a network call the human did not
choose, leaking that they use this, how often, and when, which is exactly
what the gate refuses. So the anchor is the human's own backup, which never
leaves the machine and sits in their hands rather than a third party's.

These tests hold both halves of that, and the second matters as much as the
first: what it proves, and what it cannot. A witness that were quietly
believed to cover the tail would be worse than none, because the honest
sentence in VERIFIED.md would have been traded for a false sense of a
closed hole.
"""

import json

from crystalcore.audit import AuditLog


def _log(tmp_path, n=4):
    log = AuditLog(str(tmp_path / "audit.jsonl"))
    for i in range(n):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="m", chars=10 + i, reason="local", source=None)
    return log


def _lines(tmp_path):
    return (tmp_path / "audit.jsonl").read_text().strip().splitlines()


def _rewrite(tmp_path, lines):
    (tmp_path / "audit.jsonl").write_text("\n".join(lines) + "\n")
    return AuditLog(str(tmp_path / "audit.jsonl"))


# ------------------------------------------------------ what it testifies to

def test_a_witness_records_where_the_record_stood(tmp_path):
    log = _log(tmp_path, n=3)
    w = log.witness()

    assert w["count"] == 3
    assert w["head"] == log.head()


def test_an_untouched_record_still_agrees_with_its_backup(tmp_path):
    log = _log(tmp_path)
    w = log.witness()

    ok, said = log.check_witness(w)
    assert ok is True
    assert "still agrees" in said


def test_calls_made_after_the_backup_do_not_disturb_it(tmp_path):
    """The ordinary case. A backup goes stale in coverage, never in truth."""
    log = _log(tmp_path, n=3)
    w = log.witness()
    for _ in range(4):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="m", chars=1, reason="local", source=None)

    ok, _ = log.check_witness(w)
    assert ok is True


# ------------------------------------------------------------ what it catches

def test_a_tail_cut_back_past_the_backup_is_caught(tmp_path):
    """The hole this exists to cover. verify() returns True here."""
    log = _log(tmp_path, n=6)
    w = log.witness()
    truncated = _rewrite(tmp_path, _lines(tmp_path)[:3])

    assert truncated.verify()[0] is True, "the chain itself sees nothing wrong"

    ok, said = truncated.check_witness(w)
    assert ok is False
    assert "no longer in the record" in said


def test_an_entry_removed_before_the_witnessed_one_is_caught(tmp_path):
    log = _log(tmp_path, n=5)
    w = log.witness()
    lines = _lines(tmp_path)
    shortened = _rewrite(tmp_path, lines[1:])   # drop the first

    ok, said = shortened.check_witness(w)
    assert ok is False
    assert "number 5" in said and "number 4" in said


def test_an_emptied_record_is_caught(tmp_path):
    log = _log(tmp_path, n=3)
    w = log.witness()
    (tmp_path / "audit.jsonl").write_text("")

    ok, _ = AuditLog(str(tmp_path / "audit.jsonl")).check_witness(w)
    assert ok is False


# ------------------------------------------------- what it explicitly cannot

def test_it_cannot_see_a_tail_cut_back_only_to_the_backup(tmp_path):
    """The boundary, pinned so it cannot be quietly overstated later.

    Entries recorded after the backup are outside what it saw. Removing
    exactly those leaves the witnessed prefix intact, and this returns True
    — correctly, because the backup genuinely cannot speak to them.

    The interface and VERIFIED.md both say so in the same breath as the
    capability. If this test ever starts failing, the witness has grown
    stronger and that wording should be revisited.
    """
    log = _log(tmp_path, n=3)
    w = log.witness()
    for _ in range(4):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="m", chars=1, reason="local", source=None)

    back_to_the_backup = _rewrite(tmp_path, _lines(tmp_path)[:3])
    ok, said = back_to_the_backup.check_witness(w)

    assert ok is True, "four later calls were erased and the backup cannot tell"
    assert "outside what it can vouch for" in said, \
        "so the sentence it returns must say where its knowledge stops"


def test_a_witness_from_before_any_call_attests_to_nothing(tmp_path):
    """None, not True. Silence is not a clean bill of health."""
    empty = AuditLog(str(tmp_path / "audit.jsonl"))
    w = empty.witness()

    ok, said = _log(tmp_path).check_witness(w)
    assert ok is None
    assert "nothing to attest" in said


def test_a_missing_or_malformed_witness_attests_to_nothing(tmp_path):
    log = _log(tmp_path)
    for junk in (None, {}, {"head": ""}, {"count": 3}, {"head": "x"}):
        ok, _ = log.check_witness(junk)
        assert ok is None, junk


# ---------------------------------------------------- as carried by a backup

def test_the_export_carries_a_witness(tmp_path):
    from crystalcore.companion import Clementine
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    _log(tmp_path, n=2)
    c.audit = AuditLog(str(tmp_path / "audit.jsonl"))

    bundle = json.loads(
        create_app(c).test_client().get("/api/export").get_data(as_text=True))

    assert bundle["audit"]["count"] == 2
    assert bundle["audit"]["head"] == c.audit.head()


def test_the_bundle_carries_a_fingerprint_and_not_the_record(tmp_path):
    """The log stays on the machine that made it. Only enough to recognise it
    travels — otherwise export would quietly start moving the one file whose
    whole point is that it does not."""
    from crystalcore.companion import Clementine
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    log = _log(tmp_path, n=3)
    c.audit = AuditLog(str(tmp_path / "audit.jsonl"))

    raw = create_app(c).test_client().get("/api/export").get_data(as_text=True)
    bundle = json.loads(raw)

    assert set(bundle["audit"]) == {"head", "count"}
    for entry in log.entries():
        assert entry["at"] not in raw, "a log entry travelled with the backup"


def test_a_witness_round_trips_through_a_saved_file(tmp_path):
    """Downloaded, kept, and read back later — which is the only way it is
    ever actually used."""
    from crystalcore.companion import Clementine
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path / "home"))
    c._embed_ok = False
    log = _log(tmp_path / "home", n=4)
    c.audit = AuditLog(str(tmp_path / "home" / "audit.jsonl"))

    on_disk = tmp_path / "backup.json"
    on_disk.write_bytes(
        create_app(c).test_client().get("/api/export").get_data())

    saved = json.loads(on_disk.read_text())["audit"]
    assert log.check_witness(saved)[0] is True

    _rewrite(tmp_path / "home", _lines(tmp_path / "home")[:2])
    reopened = AuditLog(str(tmp_path / "home" / "audit.jsonl"))
    assert reopened.verify()[0] is True, "the chain is content"
    assert reopened.check_witness(saved)[0] is False, "the backup is not"


def test_importing_a_bundle_does_not_touch_the_record(tmp_path):
    """A witness in a bundle is a fingerprint to compare against, never
    something to write back. Restoring a companion must not be able to
    rewrite the account of what this machine did."""
    from crystalcore.companion import Clementine
    from server import create_app

    here = Clementine(memory_dir=str(tmp_path / "here"))
    here._embed_ok = False
    _log(tmp_path / "here", n=3)
    here.audit = AuditLog(str(tmp_path / "here" / "audit.jsonl"))
    before = _lines(tmp_path / "here")

    other = Clementine(memory_dir=str(tmp_path / "other"))
    other._embed_ok = False
    other.set_name("Aster")
    bundle = json.loads(
        create_app(other).test_client().get("/api/export").get_data(as_text=True))

    create_app(here).test_client().post("/api/import", json=bundle)

    assert _lines(tmp_path / "here") == before
