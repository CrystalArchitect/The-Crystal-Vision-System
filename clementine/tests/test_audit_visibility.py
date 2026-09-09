# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""What the record can prove, what it cannot, and what it is safe to show.

The window now displays the consent record rather than asserting that it
verifies. That change is only an improvement if the words around it are true,
and two of them are load-bearing.

The first is "intact". The chain catches an entry altered after writing and
an entry cut out of the middle. It does not catch entries removed from the
*end* — a chain with its tail cut off is a shorter chain that verifies
perfectly. That is inherent to a hash chain with no anchor outside the file,
not a defect, but it means the panel must say every *remaining* entry rather
than every entry. The limit is pinned here so that nobody later reads the
green verdict, assumes it means completeness, and writes the stronger
sentence.

The second is that showing the record is safe. Entries carry a character
count, not the characters, so the panel reveals nothing the conversation did
not. If a message body ever starts being recorded, displaying the log would
begin leaking the very thing the log exists to protect — so that is pinned
too.
"""

import json

from crystalcore.audit import AuditLog


def _log(tmp_path, n=4):
    log = AuditLog(str(tmp_path / "audit.jsonl"))
    for i in range(n):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="llama3.1:8b", chars=100 + i, reason="local",
                   source=None)
    return log


def _lines(tmp_path):
    return (tmp_path / "audit.jsonl").read_text().strip().splitlines()


def _rewrite(tmp_path, lines):
    (tmp_path / "audit.jsonl").write_text("\n".join(lines) + "\n")
    return AuditLog(str(tmp_path / "audit.jsonl"))


# ------------------------------------------------------ what it does catch

def test_an_untouched_record_verifies(tmp_path):
    assert _log(tmp_path).verify() == (True, [])


def test_an_altered_entry_is_caught_and_named(tmp_path):
    _log(tmp_path)
    lines = _lines(tmp_path)
    lines[2] = lines[2].replace('"chars": 102', '"chars": 999')

    intact, problems = _rewrite(tmp_path, lines).verify()
    assert intact is False
    assert any("entry 2" in p for p in problems), problems
    assert any("altered" in p for p in problems), problems


def test_an_entry_removed_from_the_middle_is_caught(tmp_path):
    _log(tmp_path)
    lines = _lines(tmp_path)

    intact, problems = _rewrite(tmp_path, lines[:1] + lines[2:]).verify()
    assert intact is False
    assert any("chain break" in p for p in problems), problems


def test_reordering_is_caught(tmp_path):
    _log(tmp_path)
    lines = _lines(tmp_path)

    intact, _ = _rewrite(tmp_path, [lines[1], lines[0]] + lines[2:]).verify()
    assert intact is False


# --------------------------------------------------- what it does NOT catch

def test_entries_cut_from_the_end_are_NOT_caught(tmp_path):
    """Not a defect — a shorter chain is a valid chain — but the reason the
    interface says every *remaining* entry rather than every entry.

    If this ever starts failing, the record has gained an anchor outside
    itself and the wording in Record.svelte should be strengthened to match.
    """
    _log(tmp_path)
    lines = _lines(tmp_path)

    intact, problems = _rewrite(tmp_path, lines[:2]).verify()
    assert intact is True, "truncation is invisible to an unanchored chain"
    assert problems == []


# ------------------------------------------------- what it is safe to show

def test_an_entry_records_a_size_and_never_the_content(tmp_path):
    """The panel displays every field. If a message body is ever added, this
    fails — and it should, because showing the log would then leak exactly
    what the log exists to protect."""
    log = AuditLog(str(tmp_path / "audit.jsonl"))
    secret = "the quiet thing they told me in confidence"
    log.record(service="chat", destination="local", outcome="allowed",
               model="m", chars=len(secret), reason="local", source=None)

    raw = (tmp_path / "audit.jsonl").read_text()
    assert secret not in raw, "a message body reached the audit log"

    entry = json.loads(raw.strip())
    assert entry["chars"] == len(secret), "the size is kept"
    assert set(entry) == {"at", "service", "destination", "outcome", "model",
                          "chars", "reason", "source", "prev", "hash"}, \
        "a new field appeared — check it carries no content before showing it"


# -------------------------------------------------- as the interface reads it

def test_the_endpoint_gives_the_interface_what_it_displays(tmp_path):
    from crystalcore.companion import Clementine
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    _log(tmp_path, n=3)
    c.audit = AuditLog(str(tmp_path / "audit.jsonl"))

    body = create_app(c).test_client().get("/api/audit?limit=2").get_json()

    assert body["total"] == 3, "the true count, not the page size"
    assert len(body["entries"]) == 2, "limit returns the most recent"
    assert body["intact"] is True
    assert body["problems"] == []
    for field in ("at", "service", "destination", "outcome", "reason"):
        assert field in body["entries"][0], f"the panel shows {field}"


def test_a_broken_chain_reaches_the_interface_with_its_reasons(tmp_path):
    from crystalcore.companion import Clementine
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    _log(tmp_path)
    lines = _lines(tmp_path)
    lines[1] = lines[1].replace('"chars": 101', '"chars": 777')
    (tmp_path / "audit.jsonl").write_text("\n".join(lines) + "\n")
    c.audit = AuditLog(str(tmp_path / "audit.jsonl"))

    body = create_app(c).test_client().get("/api/audit").get_json()
    assert body["intact"] is False
    assert body["problems"], "the panel needs the reasons to show them"
