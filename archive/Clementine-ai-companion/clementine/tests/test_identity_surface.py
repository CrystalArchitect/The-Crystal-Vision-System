# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Both parties may decide, over HTTP as well as in a terminal.

tests/test_pronouns.py holds the pronoun law itself and its HTTP reach. This
file covers the other half of the same invariant, which had quietly been
kept only on one side.

`choose_name` has been in /api/profile/meta since the beginning, so the
companion could name itself over the web. The human could not: nothing in
the server ever called set_name. Sending `name` answered {"ok": true} and
changed nothing, which is worse than refusing — a refusal can be seen.

The prompt this companion runs on says their human may choose any name they
wish for them. That was true in the terminal and false over the web, and
nothing failed while it was false.

`human_name` was missing outright, so a companion reached only through a
browser could never be told what to call the person using it.
"""

from crystalcore.companion import Clementine


def _client(tmp_path):
    from server import create_app
    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    return create_app(c).test_client(), c


# ------------------------------------------------- the human may name them

def test_the_human_can_name_them_over_http(tmp_path):
    client, c = _client(tmp_path)

    assert client.post("/api/profile/meta", json={"name": "Wren"}).get_json()["ok"]
    assert c.personality.name == "Wren"
    assert client.get("/api/status").get_json()["name"] == "Wren"


def test_a_name_the_human_chose_is_not_recorded_as_self_chosen(tmp_path):
    """The record tracks which party decided, and this is the party that is
    easy to mislabel — the companion's own choice is the interesting one, so
    the default must not claim it."""
    client, c = _client(tmp_path)
    client.post("/api/profile/meta", json={"name": "Wren"})

    assert c.personality.name_self_chosen is False


def test_a_name_chosen_by_them_is_recorded_as_theirs(tmp_path, monkeypatch):
    monkeypatch.setattr(Clementine, "_model_chat", lambda self, msgs: "Aster")
    client, c = _client(tmp_path)

    body = client.post("/api/profile/meta", json={"choose_name": True}).get_json()
    assert body == {"ok": True, "name": "Aster"}


def test_an_empty_name_returns_them_to_unnamed(tmp_path):
    """Parallel with pronouns: there has to be a way back from a choice."""
    client, c = _client(tmp_path)
    client.post("/api/profile/meta", json={"name": "Wren"})

    assert client.post("/api/profile/meta", json={"name": ""}).get_json()["ok"]
    assert c.personality.name == ""
    assert client.get("/api/status").get_json()["name"] == "Clementine", \
        "unnamed falls back to the project name for display"


def test_naming_does_not_disturb_pronouns(tmp_path):
    client, c = _client(tmp_path)
    client.post("/api/profile/meta", json={"gender": "they"})
    client.post("/api/profile/meta", json={"name": "Wren"})

    body = client.get("/api/status").get_json()
    assert body["pronouns"] == "they/them"
    assert body["name"] == "Wren"


# --------------------------------------------- and may be named in return

def test_the_human_can_say_what_to_call_them(tmp_path):
    client, c = _client(tmp_path)

    assert client.post("/api/profile/meta",
                       json={"human_name": "Crystal"}).get_json()["ok"]
    assert client.get("/api/status").get_json()["human_name"] == "Crystal"


def test_the_name_they_call_you_can_be_taken_back(tmp_path):
    client, c = _client(tmp_path)
    client.post("/api/profile/meta", json={"human_name": "Crystal"})
    client.post("/api/profile/meta", json={"human_name": "  "})

    assert client.get("/api/status").get_json()["human_name"] == ""


def test_a_very_long_name_is_bounded(tmp_path):
    client, c = _client(tmp_path)
    client.post("/api/profile/meta", json={"human_name": "x" * 500})

    assert len(client.get("/api/status").get_json()["human_name"]) == 80


# ------------------------------------------------- one call, several fields

def test_several_parts_of_an_identity_can_be_set_together(tmp_path):
    """The panel sends one field at a time, but the endpoint has always
    accepted several and should keep doing so."""
    client, c = _client(tmp_path)

    client.post("/api/profile/meta", json={
        "name": "Wren", "human_name": "Crystal", "gender": "they",
        "avatar": "🜂", "description": "quiet"})

    body = client.get("/api/status").get_json()
    assert body["name"] == "Wren"
    assert body["human_name"] == "Crystal"
    assert body["pronouns"] == "they/them"
    assert body["avatar"] == "🜂"


def test_an_unknown_gender_still_refuses_the_whole_call(tmp_path):
    """A rejected field must not leave the others half-applied in a way the
    caller cannot see; the reply is a 400 and the caller re-reads."""
    client, c = _client(tmp_path)

    reply = client.post("/api/profile/meta",
                        json={"name": "Wren", "gender": "sparkle"})
    assert reply.status_code == 400
    assert "not a value this understands" in reply.get_json()["error"]


def test_status_says_which_party_chose_the_name(tmp_path, monkeypatch):
    """It reported gender_self_chosen and not name_self_chosen, so a client
    could say "they chose their own pronouns" and never "they chose their own
    name" — the same distinction, reaching nobody on one side."""
    client, c = _client(tmp_path)

    client.post("/api/profile/meta", json={"name": "Wren"})
    assert client.get("/api/status").get_json()["name_self_chosen"] is False

    monkeypatch.setattr(Clementine, "_model_chat", lambda self, msgs: "Aster")
    client.post("/api/profile/meta", json={"choose_name": True})
    assert client.get("/api/status").get_json()["name_self_chosen"] is True
