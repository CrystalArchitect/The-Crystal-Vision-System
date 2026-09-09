# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""A handle that means one memory, and goes on meaning it.

tests/test_memory_handles.py records the hazard this closes: note and
reflection handles were positions, so deleting n2 made n3 mean what n4 meant.
Anything acting on a list it had read a moment earlier could permanently
destroy a memory nobody chose. The interface compensated with three guards.
Guards are the right answer while a format cannot be changed; they are the
wrong place to leave the problem permanently.

So the identifier is the fix, and the tests that matter are not "does an id
field exist" but the two promises it makes:

  * it names the same memory tomorrow that it named today, across reloads,
    edits, imports and the deletion of everything around it;
  * acting on it either does what was asked or does nothing at all — never
    the neighbouring memory.

Everything else here defends the migration, because this change touches
files that already exist and hold things people asked to be kept. A memory
store that loses entries while gaining identifiers would be a poor trade.
"""

import json

from crystalcore.companion import Clementine


def _old_style(tmp_path, notes=("ALPHA", "BRAVO", "CHARLIE", "DELTA")):
    """A memory folder written before identifiers existed."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "memory.json").write_text(json.dumps({
        "notes": [{"text": t, "tags": [], "when": ""} for t in notes],
        "reflections": [{"text": "prefers mornings", "when": ""}],
        "facts": {}, "conversation": [], "summaries": [], "last_seen": "",
    }))
    return _open(tmp_path)


def _open(tmp_path):
    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    return c


# --------------------------------------------------------------- migration

def test_a_companion_that_predates_identifiers_gains_them(tmp_path):
    c = _old_style(tmp_path)

    assert all(n.get("id") for n in c.memory.notes)
    assert all(r.get("id") for r in c.memory.reflections)


def test_nothing_is_lost_in_the_migration(tmp_path):
    """The point of care: this rewrites a file somebody's memories live in."""
    c = _old_style(tmp_path)

    assert [n["text"] for n in c.memory.notes] == [
        "ALPHA", "BRAVO", "CHARLIE", "DELTA"]
    assert c.memory.reflections[0]["text"] == "prefers mornings"


def test_the_migration_is_written_to_disk_not_just_held_in_memory(tmp_path):
    _old_style(tmp_path)
    on_disk = json.loads((tmp_path / "memory.json").read_text())
    assert all(n.get("id") for n in on_disk["notes"])


def test_a_note_added_by_hand_is_given_an_identifier(tmp_path):
    """The file invites being opened and edited. Adding {"text": "..."} in a
    text editor has to keep working."""
    c = _old_style(tmp_path)
    c.memory.notes.append({"text": "written by hand"})
    c.save()

    reopened = _open(tmp_path)
    handwritten = [n for n in reopened.memory.notes if n["text"] == "written by hand"]
    assert handwritten and handwritten[0].get("id")


def test_a_copied_entry_does_not_leave_two_memories_sharing_a_handle(tmp_path):
    """Duplicating a block in an editor is the obvious way to add a note by
    hand, and it copies the identifier with it."""
    c = _old_style(tmp_path)
    c.memory.notes.append(dict(c.memory.notes[0]))  # id and all
    c.save()

    ids = [n["id"] for n in _open(tmp_path).memory.notes]
    assert len(ids) == len(set(ids)), "two memories answered to one handle"


# --------------------------------------------------------------- stability

def test_an_identifier_survives_a_reload(tmp_path):
    before = [n["id"] for n in _old_style(tmp_path).memory.notes]
    assert [n["id"] for n in _open(tmp_path).memory.notes] == before


def test_identifiers_are_never_reassigned(tmp_path):
    """Rewriting them on load would break the only promise they make."""
    c = _old_style(tmp_path)
    kept = c.memory.notes[1]["id"]

    for _ in range(3):
        c = _open(tmp_path)
    assert c.memory.notes[1]["id"] == kept


def test_editing_a_note_keeps_its_identifier(tmp_path):
    """Rewording a note is correcting it, not replacing it with a different
    one — and this method rebuilds the whole entry, so the id has to be
    carried across deliberately."""
    c = _old_style(tmp_path)
    handle = c.memory.notes[1]["id"]

    assert c.edit_note(handle, "BRAVO, reworded") is True
    assert c.memory.notes[1]["id"] == handle
    assert c.memory.notes[1]["text"] == "BRAVO, reworded"


def test_an_identifier_survives_export_and_import(tmp_path):
    from server import create_app

    origin = _old_style(tmp_path / "home")
    handle = origin.memory.notes[2]["id"]
    bundle = json.loads(
        create_app(origin).test_client().get("/api/export").get_data(as_text=True))

    elsewhere = _open(tmp_path / "elsewhere")
    create_app(elsewhere).test_client().post("/api/import", json=bundle)

    assert [n["id"] for n in elsewhere.memory.notes] == \
           [n["id"] for n in origin.memory.notes]
    assert elsewhere.forget(handle) == "note 'CHARLIE'", \
        "a handle written down before the move still names the same memory"


# ------------------------------------------------------------- the hazard

def test_the_neighbouring_memory_is_not_destroyed(tmp_path):
    """The exact scenario from test_memory_handles.py, now harmless.

    Read the list, hold CHARLIE's handle, have something else delete an
    earlier note so every position shifts, then act. Positionally this used
    to remove DELTA.
    """
    c = _old_style(tmp_path)
    charlie = c.memory.notes[2]["id"]

    c.forget("n1")                                    # ALPHA goes
    assert c.memory.notes[2]["text"] == "DELTA", "positions did shift"

    assert c.forget(charlie) == "note 'CHARLIE'"
    assert [n["text"] for n in c.memory.notes] == ["BRAVO", "DELTA"]


def test_a_handle_for_something_already_gone_removes_nothing(tmp_path):
    """The other half of the promise: what it names, or nothing."""
    c = _old_style(tmp_path)
    handle = c.memory.notes[0]["id"]
    c.forget(handle)

    assert c.forget(handle) == ""
    assert len(c.memory.notes) == 3, "a second attempt took a bystander"


def test_reflections_are_addressable_too(tmp_path):
    c = _old_style(tmp_path)
    assert c.forget(c.memory.reflections[0]["id"]) == "reflection 'prefers mornings'"


# ------------------------------------------- the terminal keeps its numbers

def test_the_numbers_a_person_reads_and_types_still_work(tmp_path):
    """/notes prints n1, n2. Someone typing what they just read should not
    have to copy a hex string instead."""
    c = _old_style(tmp_path)

    assert c.forget("n2") == "note 'BRAVO'"
    assert c.edit_note("n1", "ALPHA, reworded") is True
    assert c.memory.notes[0]["text"] == "ALPHA, reworded"


def test_an_unknown_handle_of_either_kind_matches_nothing(tmp_path):
    c = _old_style(tmp_path)
    for junk in ("n99", "n-000000000000", "", "   ", "nonsense"):
        assert c.forget(junk) == "", junk
    assert len(c.memory.notes) == 4


# ------------------------------------------------------- as served over HTTP

def test_the_listing_hands_out_stable_handles(tmp_path):
    from server import create_app

    client = create_app(_old_style(tmp_path)).test_client()
    listed = client.get("/api/memories").get_json()

    for group in ("notes", "reflections"):
        for item in listed[group]:
            assert item["handle"].startswith(("n-", "r-")), item
            assert item["number"], "the display number comes along too"


def test_forgetting_over_http_by_stable_handle_takes_the_right_memory(tmp_path):
    from server import create_app

    c = _old_style(tmp_path)
    client = create_app(c).test_client()
    charlie = client.get("/api/memories").get_json()["notes"][2]["handle"]

    client.post("/api/forget", json={"handle": "n1"})       # the list shifts
    body = client.post("/api/forget", json={"handle": charlie}).get_json()

    assert body["ok"] is True
    assert "CHARLIE" in body["forgotten"]
    assert [n["text"] for n in c.memory.notes] == ["BRAVO", "DELTA"]
