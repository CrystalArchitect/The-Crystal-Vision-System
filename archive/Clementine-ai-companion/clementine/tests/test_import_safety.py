# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Restoring a backup must not be how somebody loses a companion.

Import is the only operation here that replaces a whole companion at once —
identity and memory together, in one call. It used to check two labels and
then write. A bundle carrying `format` and `version` with a broken body
replaced the person's companion with an empty one and answered `{"ok":
true}`.

Nothing was deleted: `_load_json` preserved the unreadable files as
`.corrupt-*`. But the only notice went to the server's stdout, which nobody
running a browser ever sees, and the reply said success. A file truncated
mid-download, hand-edited, or written by a later version would all do it.

Two changes, and these tests hold both. The structure is checked before
anything is written, so a damaged file changes nothing and says why. And
what is already there is copied aside first, so even a valid import of the
wrong file can be walked back.

The second is the one worth stating plainly: it turns the last irreversible
operation in this program into a reversible one, which is a better property
than being careful.
"""

import json

from crystalcore.companion import Clementine


def _companion(tmp_path, name="Wren", key="birthday", value="June 3"):
    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    c.set_name(name)
    c.remember_fact(key, value)
    return c


def _client(companion):
    from server import create_app
    return create_app(companion).test_client()


def _bundle_of(companion):
    return json.loads(_client(companion).get("/api/export").get_data(as_text=True))


def _intact(companion, name="Wren", key="birthday"):
    return companion.personality.name == name and key in companion.memory.facts


# --------------------------------------- a damaged file changes nothing

def test_a_bundle_whose_memory_is_not_an_object_is_refused(tmp_path):
    c = _companion(tmp_path)
    reply = _client(c).post("/api/import", json={
        "format": "crystalcore-memory-bundle", "version": 1,
        "config": {"name": "X"}, "memory": "not a dict"})

    assert reply.status_code == 400
    assert "damaged" in reply.get_json()["error"]
    assert _intact(c), "the companion was replaced by a broken file"


def test_a_bundle_whose_config_is_not_an_object_is_refused(tmp_path):
    c = _companion(tmp_path)
    reply = _client(c).post("/api/import", json={
        "format": "crystalcore-memory-bundle", "version": 1,
        "config": [1, 2, 3], "memory": {}})

    assert reply.status_code == 400
    assert _intact(c)


def test_a_memory_field_of_the_wrong_type_is_refused_and_named(tmp_path):
    c = _companion(tmp_path)

    for field, wrong in (("notes", "oops"), ("facts", []),
                         ("reflections", {}), ("conversation", 7)):
        reply = _client(c).post("/api/import", json={
            "format": "crystalcore-memory-bundle", "version": 1,
            "config": {}, "memory": {field: wrong}})
        assert reply.status_code == 400, field
        assert field in reply.get_json()["error"], \
            "the error should say which field is wrong"
        assert _intact(c), f"{field} slipped through and emptied the companion"


def test_an_empty_bundle_is_refused_rather_than_used_to_erase(tmp_path):
    """It parses, it carries the right labels, and applying it would do
    nothing except leave the person with nobody."""
    c = _companion(tmp_path)
    reply = _client(c).post("/api/import", json={
        "format": "crystalcore-memory-bundle", "version": 1})

    assert reply.status_code == 400
    assert _intact(c)


def test_nothing_is_written_when_a_bundle_is_refused(tmp_path):
    """Not merely 'the companion still works' — the files must be untouched,
    since the old failure wrote first and discovered the problem after."""
    c = _companion(tmp_path)
    before = {n: (tmp_path / n).read_text() for n in ("config.json", "memory.json")}

    _client(c).post("/api/import", json={
        "format": "crystalcore-memory-bundle", "version": 1,
        "config": {}, "memory": {"notes": "oops"}})

    assert {n: (tmp_path / n).read_text() for n in before} == before
    assert not list(tmp_path.glob("*.corrupt-*")), \
        "a refused import should not even reach the corrupt-file path"


# ------------------------------------------------ a good import still works

def test_a_real_bundle_restores_and_names_who_arrived(tmp_path):
    origin = _companion(tmp_path / "origin", name="Aster", key="city",
                        value="Sydney")
    here = _companion(tmp_path / "here")

    body = _client(here).post("/api/import", json=_bundle_of(origin)).get_json()

    assert body["ok"] is True
    assert body["name"] == "Aster"
    assert here.personality.name == "Aster"
    assert "city" in here.memory.facts


# -------------------------------------------------- and it can be walked back

def test_the_replaced_companion_is_kept(tmp_path):
    origin = _companion(tmp_path / "origin", name="Aster", key="city",
                        value="Sydney")
    here = _companion(tmp_path / "here")

    kept = _client(here).post("/api/import",
                              json=_bundle_of(origin)).get_json()["replaced_backup"]

    assert kept, "the companion that was replaced should be somewhere"
    from pathlib import Path
    saved = json.loads((Path(kept) / "config.json").read_text())
    assert saved["name"] == "Wren"


def test_importing_the_wrong_file_can_be_undone(tmp_path):
    """The property that matters. Everything above only limits the damage;
    this is the one that means a mistake is survivable."""
    from pathlib import Path

    origin = _companion(tmp_path / "origin", name="Aster", key="city",
                        value="Sydney")
    here = _companion(tmp_path / "here")
    client = _client(here)

    kept = Path(client.post("/api/import",
                            json=_bundle_of(origin)).get_json()["replaced_backup"])
    assert here.personality.name == "Aster", "the wrong companion is loaded"

    client.post("/api/import", json={
        "format": "crystalcore-memory-bundle", "version": 1,
        "config": json.loads((kept / "config.json").read_text()),
        "memory": json.loads((kept / "memory.json").read_text())})

    assert _intact(here), "Wren should be back, with what they knew"


def test_a_first_import_into_an_empty_profile_keeps_nothing(tmp_path):
    """There is nothing to lose, and reporting a backup that holds an empty
    companion would be noise dressed as reassurance."""
    origin = _companion(tmp_path / "origin", name="Aster", key="city",
                        value="Sydney")
    empty = Clementine(memory_dir=str(tmp_path / "empty"))
    empty._embed_ok = False

    body = _client(empty).post("/api/import", json=_bundle_of(origin)).get_json()

    assert body["ok"] is True
    assert body["replaced_backup"] == ""


# ------------------------------------------------- what import must not touch

def test_the_consent_record_is_not_replaced(tmp_path):
    """The log records what this machine did. Whose memory is loaded does not
    change whether those calls happened, and a restore that quietly reset the
    record would put a hole in the one thing making the rest checkable."""
    from crystalcore.audit import AuditLog

    here = _companion(tmp_path / "here")
    log = AuditLog(str(tmp_path / "here" / "audit.jsonl"))
    for _ in range(2):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="m", chars=5, reason="local", source=None)
    here.audit = log
    origin = _companion(tmp_path / "origin", name="Aster", key="city",
                        value="Sydney")

    _client(here).post("/api/import", json=_bundle_of(origin))

    after = AuditLog(str(tmp_path / "here" / "audit.jsonl"))
    assert len(after.entries()) == 2, "the record of past calls survived"
    assert after.verify()[0] is True, "and still verifies"
