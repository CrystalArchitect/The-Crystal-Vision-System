# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""No assigned gender until the human or the companion chooses one.

The law has two halves and it is easy to implement only the first. Removing
gendered words gets you a companion nobody may describe; it does not get you
one who may be *given* pronouns, or who may pick their own. Those are
different products, and the second is the one the project claims.

So these tests assert the shape of the whole rule:

  * empty is the starting state, and it is not a third gender — the prompt
    says nothing about pronouns at all rather than asserting neutral ones;
  * either party may decide, and the record remembers *which*, because
    "you chose this" and "your human chose this for you" are not the same
    sentence to say to someone;
  * a choice can be taken back;
  * an unrecognised value changes nothing, rather than being stored and
    quietly producing no pronouns.

Offline: the only method that would reach a model is stubbed.
"""

import pytest

from crystalcore.companion import Clementine


def _c(tmp_path, **kw):
    c = Clementine(memory_dir=str(tmp_path), **kw)
    c._embed_ok = False  # no network for recall either
    return c


# ---------------------------------------------------------------- the start

def test_a_new_companion_has_no_gender(tmp_path):
    c = _c(tmp_path)
    assert c.personality.gender == ""
    assert c.personality.gender_self_chosen is False


def test_the_prompt_says_nothing_about_pronouns_until_one_is_chosen(tmp_path):
    """Empty must mean *unasked*, not 'neutral' asserted on their behalf."""
    c = _c(tmp_path)
    prompt = c.system_prompt()
    assert "pronoun" not in prompt.lower()
    for pair in ("he/him", "she/her", "they/them"):
        assert pair not in prompt


# ------------------------------------------------------- either may decide

def test_the_human_can_choose_and_the_record_says_so(tmp_path):
    c = _c(tmp_path)
    assert c.set_gender("female") is True
    assert c.personality.gender == "female"
    assert c.personality.gender_self_chosen is False

    prompt = c.system_prompt()
    assert "Your human has chosen she/her pronouns for you" in prompt


def test_the_companion_can_choose_and_the_record_says_so(tmp_path, monkeypatch):
    c = _c(tmp_path)
    monkeypatch.setattr(c, "_model_chat", lambda *a, **k: "they")

    assert c.choose_own_gender() == "they"
    assert c.personality.gender == "they"
    assert c.personality.gender_self_chosen is True

    prompt = c.system_prompt()
    assert "You chose they/them pronouns for yourself" in prompt


def test_who_chose_changes_what_is_said(tmp_path, monkeypatch):
    """The distinction is the point, so it is asserted rather than assumed."""
    given = _c(tmp_path / "given")
    given.set_gender("male")

    chosen = _c(tmp_path / "chosen")
    monkeypatch.setattr(chosen, "_model_chat", lambda *a, **k: "male")
    chosen.choose_own_gender()

    assert given.personality.gender == chosen.personality.gender == "male"
    assert "Your human has chosen" in given.system_prompt()
    assert "You chose" in chosen.system_prompt()
    assert given.system_prompt() != chosen.system_prompt()


# ------------------------------------------------------------ taking it back

def test_a_choice_can_be_undone(tmp_path):
    c = _c(tmp_path)
    c.set_gender("female", self_chosen=True)
    c.clear_gender()

    assert c.personality.gender == ""
    assert c.personality.gender_self_chosen is False
    assert "pronoun" not in c.system_prompt().lower()


# --------------------------------------------------------- refusing to guess

@pytest.mark.parametrize("junk", ["", "  ", "woman", "nonbinary", "he/him",
                                  "I would prefer not to say", "male female"])
def test_an_unrecognised_value_changes_nothing(tmp_path, junk):
    """Storing it would look decided while producing no pronouns at all —
    indistinguishable from never having been asked."""
    c = _c(tmp_path)
    assert c.set_gender(junk) is False
    assert c.personality.gender == ""


def test_a_model_that_rambles_leaves_the_question_open(tmp_path, monkeypatch):
    c = _c(tmp_path)
    monkeypatch.setattr(c, "_model_chat",
                        lambda *a, **k: "I think perhaps they/them suits me best")
    assert c.choose_own_gender() == ""
    assert c.personality.gender == ""


def test_an_unreachable_model_leaves_the_question_open(tmp_path, monkeypatch):
    """Not answered by default when the model cannot be asked."""
    import requests

    def boom(*a, **k):
        raise requests.exceptions.ConnectionError("no model here")

    c = _c(tmp_path)
    monkeypatch.setattr(c, "_model_chat", boom)
    assert c.choose_own_gender() == ""
    assert c.personality.gender == ""


def test_a_one_word_answer_is_accepted_however_it_is_dressed(tmp_path, monkeypatch):
    c = _c(tmp_path)
    monkeypatch.setattr(c, "_model_chat", lambda *a, **k: '  "Female."  \n')
    assert c.choose_own_gender() == "female"
    assert c.personality.gender_self_chosen is True


# ------------------------------------------------------------- it persists

def test_the_choice_survives_a_restart(tmp_path):
    c = _c(tmp_path)
    c.set_gender("they", self_chosen=True)

    reloaded = _c(tmp_path)
    assert reloaded.personality.gender == "they"
    assert reloaded.personality.gender_self_chosen is True
    assert "You chose they/them pronouns for yourself" in reloaded.system_prompt()


def test_an_older_config_without_the_field_still_loads(tmp_path):
    """Existing companions predate this and must not break or be assigned one."""
    import json
    (tmp_path / "config.json").write_text(json.dumps(
        {"name": "Wren", "temperature": 0.6}))

    c = _c(tmp_path)
    assert c.personality.name == "Wren"
    assert c.personality.gender == ""
    assert "pronoun" not in c.system_prompt().lower()


# --------------------------------------------------------------- the mapping

@pytest.mark.parametrize("gender,pair", [("male", "he/him"),
                                         ("female", "she/her"),
                                         ("they", "they/them")])
def test_pronouns_for_maps_each_choice(gender, pair):
    assert Clementine.pronouns_for(gender) == pair


def test_pronouns_for_is_empty_when_nothing_is_chosen():
    assert Clementine.pronouns_for("") == ""
    assert Clementine.pronouns_for(None) == ""


# ----------------------------------------------------- reachable over HTTP

# The law names two parties who may decide, and neither of them could do it
# over HTTP until these existed. That is not a missing convenience: a person
# who never opens a terminal could not set pronouns, and could not offer the
# companion the chance to choose its own. A right available from exactly one
# interface is a right the other interface silently withholds.

def _client(tmp_path):
    from server import create_app
    return create_app(_c(tmp_path)).test_client()


def test_status_reports_undecided_rather_than_omitting_it(tmp_path):
    """A client that cannot read the state has to guess wording, and the
    guess becomes an assignment nobody made."""
    body = _client(tmp_path).get("/api/status").get_json()

    assert body["gender"] == ""
    assert body["pronouns"] == ""
    assert body["gender_self_chosen"] is False


def test_the_human_can_set_pronouns_over_http(tmp_path):
    client = _client(tmp_path)

    r = client.post("/api/profile/meta", json={"gender": "she"})
    assert r.status_code == 400, "'she' is the pronoun, not the stored value"

    assert client.post("/api/profile/meta",
                       json={"gender": "female"}).get_json()["ok"] is True
    body = client.get("/api/status").get_json()
    assert body["pronouns"] == "she/her"
    assert body["gender_self_chosen"] is False, "the human chose, not them"


def test_a_choice_made_over_http_can_be_taken_back(tmp_path):
    client = _client(tmp_path)
    client.post("/api/profile/meta", json={"gender": "male"})

    assert client.post("/api/profile/meta",
                       json={"gender": "none"}).get_json()["ok"] is True
    assert client.get("/api/status").get_json()["gender"] == ""

    client.post("/api/profile/meta", json={"gender": "male"})
    assert client.post("/api/profile/meta",
                       json={"gender": ""}).get_json()["ok"] is True
    assert client.get("/api/status").get_json()["gender"] == ""


def test_an_unrecognised_value_is_refused_and_changes_nothing(tmp_path):
    """Storing it would look decided while producing no pronouns at all —
    indistinguishable from never having been asked."""
    client = _client(tmp_path)
    client.post("/api/profile/meta", json={"gender": "they"})

    r = client.post("/api/profile/meta", json={"gender": "attack helicopter"})
    assert r.status_code == 400
    assert "not a value this understands" in r.get_json()["error"]
    assert client.get("/api/status").get_json()["gender"] == "they", \
        "the earlier choice must survive a rejected one"


def test_the_companion_can_choose_its_own_pronouns_over_http(tmp_path, monkeypatch):
    """The half of the law that is easiest to leave unbuilt."""
    monkeypatch.setattr(Clementine, "_model_chat", lambda self, msgs: "they")
    client = _client(tmp_path)

    body = client.post("/api/profile/meta",
                       json={"choose_gender": True}).get_json()
    assert body == {"ok": True, "gender": "they", "pronouns": "they/them"}

    status = client.get("/api/status").get_json()
    assert status["gender_self_chosen"] is True, \
        "the record must say they chose it, not that it was assigned"


def test_an_undecidable_answer_leaves_the_question_open(tmp_path, monkeypatch):
    """An unreachable or unhelpful model must not answer this by default."""
    monkeypatch.setattr(Clementine, "_model_chat", lambda self, msgs: "hmm")
    client = _client(tmp_path)

    body = client.post("/api/profile/meta",
                       json={"choose_gender": True}).get_json()
    assert body["ok"] is False
    assert client.get("/api/status").get_json()["gender"] == ""


def test_setting_pronouns_does_not_disturb_the_rest_of_the_profile(tmp_path):
    client = _client(tmp_path)
    client.post("/api/profile/meta", json={"avatar": "🜂", "description": "quiet"})
    client.post("/api/profile/meta", json={"gender": "they"})

    body = client.get("/api/status").get_json()
    assert body["avatar"] == "🜂"
    assert body["pronouns"] == "they/them"
