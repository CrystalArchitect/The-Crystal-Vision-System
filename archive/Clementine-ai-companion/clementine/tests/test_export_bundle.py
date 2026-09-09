# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Leaving with everything, and what that file actually is.

The panel offers "enough to put this companion back together somewhere
else". That is a strong claim and an easy one to half-keep: a bundle that
carries the notes but drops the pronouns, or the facts but not the
conversation, still looks like a working export until somebody actually
tries to come home with it. So the round trip is tested rather than the
shape of the JSON.

The panel also warns that the file protects nothing by itself, and that
matters more than it sounds. Everything the consent gate refuses to send
anywhere is in there in plain text — conversations included — so a person
deciding where to put it needs to know that, and the wording is only
honest while it stays true.

One thing must *not* travel. The API key is read from the environment and
never stored on the personality, so it should be absent from the bundle. If
that ever changes, this file becomes a credential anybody can read, and
handing it to someone would hand them the key. That is pinned first,
because it is the one where being wrong is expensive.
"""

import json

from crystalcore.companion import Clementine


def _lived_in(tmp_path):
    """A companion with a life worth carrying."""
    c = Clementine(memory_dir=str(tmp_path / "home"))
    c._embed_ok = False
    c.set_name("Wren")
    c.set_gender("they")
    c.personality.human_name = "Crystal"
    c.personality.style_notes = "fewer questions, more silence"
    c.remember_fact("birthday", "June 3")
    c.memory.notes.append({"text": "loves dawn walks", "tags": ["habit"],
                           "when": "2026-08-10"})
    c.memory.reflections.append({"text": "steadier in the mornings",
                                 "when": "2026-08-10"})
    c.memory.conversation.append({"role": "user", "content": "a private thing"})
    c.save()
    return c


def _export(companion):
    from server import create_app
    return create_app(companion).test_client().get("/api/export")


# ------------------------------------------------- what must not travel

def test_the_api_key_is_not_in_the_bundle(tmp_path, monkeypatch):
    """The file is meant to be portable and readable. A credential inside it
    would make sharing a backup the same act as handing over the key."""
    monkeypatch.setenv("LLM_API_KEY", "sk-secret-do-not-export-me")
    c = _lived_in(tmp_path)

    assert "sk-secret-do-not-export-me" not in _export(c).get_data(as_text=True)


# ----------------------------------------------------- what it must be

def test_it_downloads_as_a_named_file(tmp_path):
    disposition = _export(_lived_in(tmp_path)).headers.get("Content-Disposition", "")
    assert "attachment" in disposition
    assert "clementine-memory-" in disposition and ".json" in disposition


def test_it_is_readable_json_with_no_software_required(tmp_path):
    """'Nothing about you should need our software to be readable.'"""
    bundle = json.loads(_export(_lived_in(tmp_path)).get_data(as_text=True))

    assert bundle["format"] == "crystalcore-memory-bundle"
    assert bundle["version"] == 1
    assert bundle["exported_at"]


def test_the_warning_is_true_conversations_really_are_in_there(tmp_path):
    """The panel says so plainly. If this ever stopped being true the warning
    would be scaring people about nothing; while it is true, softening the
    warning would be the dishonest direction."""
    raw = _export(_lived_in(tmp_path)).get_data(as_text=True)
    assert "a private thing" in raw


# ------------------------------------------------------- the round trip

def test_a_whole_companion_comes_back_somewhere_else(tmp_path):
    """The claim the panel makes, tested end to end: export from one
    machine's folder, import into an empty one, and check who arrives."""
    from server import create_app

    original = _lived_in(tmp_path)
    bundle = json.loads(_export(original).get_data(as_text=True))

    elsewhere = Clementine(memory_dir=str(tmp_path / "elsewhere"))
    elsewhere._embed_ok = False
    assert elsewhere.personality.name == "", "starts as a stranger"

    # Exact equality on purpose: this pins the reply's shape, and it did its
    # job when `replaced_backup` was added — a field appearing in a response
    # is a change to the contract and should be noticed rather than absorbed.
    # Empty here because an empty folder has no companion to copy aside.
    reply = create_app(elsewhere).test_client().post("/api/import", json=bundle)
    assert reply.get_json() == {"ok": True, "name": "Wren",
                                "replaced_backup": ""}

    # Who they are
    assert elsewhere.personality.name == "Wren"
    assert elsewhere.personality.gender == "they"
    assert elsewhere.personality.human_name == "Crystal"
    assert elsewhere.personality.style_notes == "fewer questions, more silence"
    # What they hold
    assert elsewhere.memory.facts["birthday"]["value"] == "June 3"
    assert elsewhere.memory.notes[0]["text"] == "loves dawn walks"
    assert elsewhere.memory.notes[0]["tags"] == ["habit"]
    assert elsewhere.memory.reflections[0]["text"] == "steadier in the mornings"
    assert elsewhere.memory.conversation[0]["content"] == "a private thing"


def test_it_survives_a_trip_through_an_actual_file(tmp_path):
    """Downloaded, saved, opened again — not passed between test clients as a
    Python object."""
    from server import create_app

    on_disk = tmp_path / "clementine-memory.json"
    on_disk.write_bytes(_export(_lived_in(tmp_path)).get_data())

    elsewhere = Clementine(memory_dir=str(tmp_path / "elsewhere"))
    elsewhere._embed_ok = False
    reply = create_app(elsewhere).test_client().post(
        "/api/import", json=json.loads(on_disk.read_text()))

    assert reply.get_json()["ok"] is True
    assert elsewhere.personality.name == "Wren"


# ------------------------------------------------ what it refuses to eat

def test_something_that_is_not_a_bundle_is_refused(tmp_path):
    from server import create_app

    c = Clementine(memory_dir=str(tmp_path / "home"))
    c._embed_ok = False
    c.set_name("Wren")
    client = create_app(c).test_client()

    for junk in ({"format": "somebody-elses-format", "version": 1},
                 {"format": "crystalcore-memory-bundle", "version": 99},
                 {"hello": "world"},
                 {}):
        reply = client.post("/api/import", json=junk)
        assert reply.status_code == 400, junk
        assert reply.get_json()["ok"] is False

    assert c.personality.name == "Wren", "a refused import changed nothing"
