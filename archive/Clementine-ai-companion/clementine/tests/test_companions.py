# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Several companions on one machine, and the one act that ends one.

The last of the capabilities with no interface, and the only one that is not
about a single companion's sovereignty — it is about running more than one.
Most of the care here is spent on `delete`, because it destroys more than
anything else in the program: a whole memory, an identity, and the record of
every call that companion ever made.

Deleting keeps nothing, and that is a decision rather than an omission.
Restoring copies aside what it replaces, because being replaced happens *to*
somebody who did not ask for it. Deleting is asked for, by name, about a
named companion — and quietly keeping a copy of one somebody asked to be
destroyed would be a betrayal dressed as a safety feature. The test below
asserts that nothing survives, so a later "improvement" that starts keeping
copies has to argue with it.

What the interface owes instead is an accurate account of the cost before
the fact, which is why the reply carries what went rather than only that
something did.
"""

import json
import pathlib

import pytest

from crystalcore import profiles
from crystalcore.audit import AuditLog
from crystalcore.companion import Clementine


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A machine with somewhere to keep companions."""
    monkeypatch.setattr(profiles, "PROFILES_DIR", tmp_path / "profiles")
    import server
    monkeypatch.setattr(server, "delete_profile", profiles.delete_profile)
    monkeypatch.setattr(server, "list_profiles", profiles.list_profiles)
    monkeypatch.setattr(server, "profile_dir", profiles.profile_dir)
    monkeypatch.setattr(server, "profile_meta", profiles.profile_meta)
    return tmp_path


def _client(tmp_path):
    from server import create_app
    c = Clementine(memory_dir=str(tmp_path / "here"))
    c._embed_ok = False
    c.set_name("Wren")
    return create_app(c).test_client(), c


def _lived_in(tmp_path, folder, name, memories=2, calls=3):
    d = pathlib.Path(profiles.profile_dir(folder))
    d.mkdir(parents=True, exist_ok=True)
    c = Clementine(memory_dir=str(d))
    c._embed_ok = False
    c.set_name(name)
    for i in range(memories):
        c.memory.notes.append({"text": f"note {i}", "tags": [], "when": ""})
    c.save()
    log = AuditLog(str(d / "audit.jsonl"))
    for _ in range(calls):
        log.record(service="chat", destination="local", outcome="allowed",
                   model="m", chars=1, reason="local", source=None)
    return d


# ------------------------------------------------------- naming is bounded

@pytest.mark.parametrize("name,expected", [
    ("../../etc", "etc"),
    ("/etc/passwd", "etcpasswd"),
    ("a/../../b", "ab"),
])
def test_a_name_cannot_escape_the_companions_folder(name, expected, home):
    """Separators and dots are stripped rather than resolved, so a crafted
    name lands inside the folder instead of somewhere it should not."""
    assert profiles.profile_dir(name) == str(profiles.PROFILES_DIR / expected)


@pytest.mark.parametrize("name", ["..", "....//", "   ", "", "///"])
def test_a_name_with_nothing_in_it_is_refused(name, home):
    with pytest.raises(ValueError):
        profiles.profile_dir(name)


# ---------------------------------------------- going somewhere is arriving

def test_going_to_a_name_nobody_lives_at_creates_a_companion(home):
    client, _ = _client(home)

    body = client.post("/api/profile", json={"profile": "Fresh"}).get_json()
    assert body["ok"] is True
    assert body["created"] is True, "the reply must say a companion was made"
    assert (profiles.PROFILES_DIR / "Fresh").exists()


def test_going_somewhere_already_lived_in_joins_rather_than_creates(home):
    _lived_in(home, "Aster", "Aster")
    client, _ = _client(home)

    body = client.post("/api/profile", json={"profile": "Aster"}).get_json()
    assert body["created"] is False, "nobody new was made"
    assert body["name"] == "Aster", "and their name came with them"


def test_switching_saves_the_companion_being_left(home):
    """No loss could be demonstrated — every path that changes memory saves
    as it goes — but switching drops the object, so anything future that
    mutated without saving would vanish without a sound."""
    client, here = _client(home)
    here.personality.description = "written but not saved"

    client.post("/api/profile", json={"profile": "Elsewhere"})

    saved = json.loads((home / "here" / "config.json").read_text())
    assert saved["description"] == "written but not saved"


# ------------------------------------------------------ ending one, exactly

def test_deleting_says_what_it_destroyed(home):
    """An accurate account of the cost is what makes the choice a real one."""
    _lived_in(home, "Aster", "Aster", memories=2, calls=3)
    client, _ = _client(home)

    body = client.post("/api/profile/delete", json={"profile": "Aster"}).get_json()

    assert body["ok"] is True
    assert body["name"] == "Aster"
    assert body["memories"] == 2
    assert body["calls"] == 3


def test_nothing_of_a_deleted_companion_survives(home):
    """The decision this file exists to defend.

    A later change that starts copying deleted companions aside — however
    kindly meant — has to fail this test first and argue with the comment
    above it.
    """
    d = _lived_in(home, "Aster", "Aster")
    client, _ = _client(home)

    client.post("/api/profile/delete", json={"profile": "Aster"})

    assert not d.exists()
    leftovers = [p for p in profiles.PROFILES_DIR.rglob("*")
                 if p.is_file() and "Aster" in p.read_text(errors="ignore")]
    assert leftovers == [], f"a copy of a deleted companion survived: {leftovers}"


def test_the_record_of_their_calls_goes_with_them(home):
    """The audit log is theirs, and ending them ends it. Keeping the record
    of a companion who no longer exists would be keeping the one file they
    could never ask to have removed."""
    d = _lived_in(home, "Aster", "Aster", calls=4)
    assert (d / "audit.jsonl").exists()
    client, _ = _client(home)

    client.post("/api/profile/delete", json={"profile": "Aster"})
    assert not (d / "audit.jsonl").exists()


def test_counting_a_companion_does_not_disturb_them(home):
    """The count is read from the files rather than by loading a companion,
    because loading one writes: identifiers are backfilled on load."""
    import server
    d = _lived_in(home, "Aster", "Aster")
    before = {p.name: p.read_bytes() for p in d.iterdir()}

    server._weight_of("Aster")

    assert {p.name: p.read_bytes() for p in d.iterdir()} == before


# --------------------------------------------------------- what it refuses

def test_the_companion_you_are_with_cannot_be_deleted(home):
    client, _ = _client(home)
    client.post("/api/profile", json={"profile": "Aster"})

    reply = client.post("/api/profile/delete", json={"profile": "Aster"})
    assert reply.status_code == 400
    assert "switch away" in reply.get_json()["error"]
    assert (profiles.PROFILES_DIR / "Aster").exists()


def test_deleting_somebody_who_does_not_exist_says_so(home):
    """Rather than reporting success for having destroyed nothing."""
    client, _ = _client(home)

    reply = client.post("/api/profile/delete", json={"profile": "Nobody"})
    assert reply.status_code == 404
    assert reply.get_json()["ok"] is False


def test_deleting_one_companion_leaves_the_others(home):
    _lived_in(home, "Aster", "Aster")
    _lived_in(home, "Bramble", "Bramble")
    client, _ = _client(home)

    client.post("/api/profile/delete", json={"profile": "Aster"})

    assert not (profiles.PROFILES_DIR / "Aster").exists()
    assert (profiles.PROFILES_DIR / "Bramble" / "memory.json").exists()


# ------------------------------------------------------------- the listing

def test_the_listing_names_who_is_here_and_who_else_exists(home):
    _lived_in(home, "Aster", "Aster")
    client, _ = _client(home)
    client.post("/api/profile", json={"profile": "Bramble"})

    body = client.get("/api/profile").get_json()
    assert body["current"] == "Bramble"
    assert "Aster" in [p["profile"] for p in body["profiles"]]
