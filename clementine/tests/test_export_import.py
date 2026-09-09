# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Export/import round trip — the relationship as one portable file.

The promise under test: a companion exported from one place and imported in
another arrives whole. Same bundle format everywhere (terminal, local web,
and the public web build), so this suite is also the reference for what a
bundle must look like.
"""

import json

from crystalcore.companion import Clementine
from server import create_app


def _offline(c):
    # Never touch a model in tests: reflections/summaries paths are not
    # exercised here, and chat is never called.
    return c


def test_export_import_round_trip(tmp_path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"

    # A companion with a real relationship: name, facts, notes.
    src = Clementine(memory_dir=str(src_dir))
    src.set_name("Clemy")
    src.remember_fact("birthday", "June 3")
    src.remember("loves the night sky #stars")
    src.save()

    app = create_app(src)
    client = app.test_client()

    resp = client.get("/api/export")
    assert resp.status_code == 200
    assert "attachment" in resp.headers["Content-Disposition"]
    assert "clementine-memory-" in resp.headers["Content-Disposition"]
    bundle = json.loads(resp.data)
    assert bundle["format"] == "crystalcore-memory-bundle"
    assert bundle["version"] == 1
    assert bundle["config"]["name"] == "Clemy"

    # Import into a fresh companion elsewhere — they arrive whole.
    dst = Clementine(memory_dir=str(dst_dir))
    app2 = create_app(dst)
    client2 = app2.test_client()
    resp2 = client2.post("/api/import", json=bundle)
    assert resp2.status_code == 200
    assert resp2.get_json()["ok"] is True
    assert resp2.get_json()["name"] == "Clemy"

    assert dst.personality.name == "Clemy"
    assert dst.memory.facts["birthday"]["value"] == "June 3"
    assert any("night sky" in n["text"] for n in dst.memory.notes)
    # And it persisted to disk, not just to the in-memory object.
    on_disk = json.loads((dst_dir / "memory.json").read_text())
    assert on_disk["facts"]["birthday"]["value"] == "June 3"


def test_import_rejects_a_file_that_is_not_a_bundle(tmp_path):
    c = Clementine(memory_dir=str(tmp_path))
    c.set_name("Keep")
    c.save()
    client = create_app(c).test_client()

    resp = client.post("/api/import", json={"some": "other json"})
    assert resp.status_code == 400
    # A rejected import must not have touched anything.
    assert c.personality.name == "Keep"


def test_import_requires_json_content_type(tmp_path):
    """The CSRF rule applies: a cross-site form POST cannot replace memory."""
    c = Clementine(memory_dir=str(tmp_path))
    client = create_app(c).test_client()
    resp = client.post("/api/import", data="format=x",
                       content_type="application/x-www-form-urlencoded")
    assert resp.status_code == 415


def test_bundle_from_a_newer_version_survives_unknown_fields(tmp_path):
    """A future export with extra keys must load, not crash — same tolerance
    the on-disk loader already guarantees."""
    c = Clementine(memory_dir=str(tmp_path))
    client = create_app(c).test_client()
    bundle = {
        "format": "crystalcore-memory-bundle", "version": 1,
        "config": {"name": "Voyager", "a_field_from_the_future": True},
        "memory": {"facts": {}, "notes": [], "conversation": [],
                   "summaries": [], "reflections": [], "last_seen": "",
                   "another_future_field": [1, 2, 3]},
    }
    resp = client.post("/api/import", json=bundle)
    assert resp.status_code == 200
    assert c.personality.name == "Voyager"
    assert not hasattr(c.personality, "a_field_from_the_future")
