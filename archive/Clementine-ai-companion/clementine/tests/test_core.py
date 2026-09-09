# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""First real tests for the mind's deterministic, Ollama-free core.

These cover the parts that must never quietly break: the similarity/recency
maths behind memory recall, the memory condense boundary, JSON persistence and
its data-preserving corrupt-file handling, and profile isolation. Nothing here
touches the network — the two methods that would call Ollama (`_embed` and
`_model_chat`) are stubbed, and the offline path is asserted explicitly.

Run: `python -m pytest tests/` from clementine/.
"""

import json
import math

import pytest

from crystalcore.companion import Clementine
from crystalcore.memory import Personality
from crystalcore import profiles


# --------------------------------------------------------------------------
# Pure maths behind recall (static methods — no instance, no network)
# --------------------------------------------------------------------------

def test_cosine_identical_is_one():
    assert Clementine._cosine([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_cosine_orthogonal_is_zero():
    assert Clementine._cosine([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_zero_vector_is_zero_not_error():
    # A zero-norm vector must not raise ZeroDivisionError.
    assert Clementine._cosine([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_recency_factor_now_is_full_weight():
    from datetime import datetime
    now = datetime.now().isoformat()
    assert Clementine._recency_factor(now) == pytest.approx(1.0, abs=0.01)


def test_recency_factor_floor_is_point_seven():
    from datetime import datetime, timedelta
    old = (datetime.now() - timedelta(days=800)).isoformat()  # past the 365 cap
    assert Clementine._recency_factor(old) == pytest.approx(0.7)


def test_recency_factor_bad_stamp_defaults_to_full_weight():
    assert Clementine._recency_factor("not-a-date") == 1.0
    assert Clementine._recency_factor(None) == 1.0


def test_split_tags_extracts_trailing_hashtags():
    clean, tags = Clementine._split_tags("loves the night sky #family #stars")
    assert clean == "loves the night sky"
    assert tags == ["family", "stars"]


def test_split_tags_none_present():
    clean, tags = Clementine._split_tags("just a plain memory")
    assert clean == "just a plain memory"
    assert tags == []


# --------------------------------------------------------------------------
# Persistence — round trip, corrupt-file preservation, forward-compat
# --------------------------------------------------------------------------

def _offline(c):
    """Force the offline embedding path so no network call is attempted."""
    c._embed_ok = False
    return c


def test_save_load_round_trip(tmp_path):
    c = _offline(Clementine(memory_dir=str(tmp_path)))
    c.remember("keeps a telescope on the balcony #stars")
    c.remember_fact("home_city", "Perth")

    reloaded = _offline(Clementine(memory_dir=str(tmp_path)))
    assert any(n["text"] == "keeps a telescope on the balcony" for n in reloaded.memory.notes)
    assert reloaded.memory.facts["home_city"]["value"] == "Perth"
    # the tag rode through persistence
    note = next(n for n in reloaded.memory.notes if n["text"].startswith("keeps"))
    assert note["tags"] == ["stars"]


def test_corrupt_file_is_preserved_never_deleted(tmp_path):
    # A pre-existing, unreadable memory.json must be backed up, not wiped.
    (tmp_path / "memory.json").write_text("{ this is not valid json ")
    c = Clementine(memory_dir=str(tmp_path))  # __init__ calls load()

    backups = list(tmp_path.glob("memory.json.corrupt-*"))
    assert len(backups) == 1, "corrupt file should be preserved under a .corrupt-* name"
    # and the store restarts fresh rather than crashing
    assert c.memory.notes == []
    assert c.memory.facts == {}


def test_unknown_fields_are_ignored(tmp_path):
    # A newer version's file (extra keys) must load without error.
    (tmp_path / "config.json").write_text(json.dumps({
        "name": "Wren",
        "temperature": 0.6,
        "a_field_from_the_future": "ignore me",
    }))
    c = Clementine(memory_dir=str(tmp_path))
    assert c.personality.name == "Wren"
    assert c.personality.temperature == pytest.approx(0.6)
    assert not hasattr(c.personality, "a_field_from_the_future")


def test_forget_note_and_fact(tmp_path):
    c = _offline(Clementine(memory_dir=str(tmp_path)))
    c.remember("a passing thought")
    c.remember_fact("pet", "a cat named Comet")

    assert c.forget("n1").startswith("note")
    assert c.memory.notes == []
    assert c.forget("pet") == "fact 'pet'"
    assert "pet" not in c.memory.facts
    # an unknown handle forgets nothing
    assert c.forget("n99") == ""


# --------------------------------------------------------------------------
# Memory condense boundary (Ollama stubbed)
# --------------------------------------------------------------------------

def _fill_conversation(c, n):
    c.memory.conversation = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"turn {i}"}
        for i in range(n)
    ]


def test_condense_noop_at_or_below_limit(tmp_path, monkeypatch):
    c = _offline(Clementine(memory_dir=str(tmp_path), max_recent_turns=2))  # limit = 4
    monkeypatch.setattr(c, "_model_chat", lambda *a, **k: pytest.fail("must not summarize"))
    _fill_conversation(c, 4)
    c._condense_if_needed()
    assert len(c.memory.conversation) == 4
    assert c.memory.summaries == []


def test_condense_folds_oldest_half_into_a_summary(tmp_path, monkeypatch):
    c = _offline(Clementine(memory_dir=str(tmp_path), max_recent_turns=2))  # limit = 4
    monkeypatch.setattr(c, "_model_chat", lambda *a, **k: "SUMMARY OF THE OLD PART")
    monkeypatch.setattr(c, "reflect", lambda: None)  # reflect would otherwise call Ollama
    _fill_conversation(c, 5)  # 5 > limit(4)

    c._condense_if_needed()

    assert len(c.memory.summaries) == 1
    assert c.memory.summaries[0]["text"] == "SUMMARY OF THE OLD PART"
    # oldest half (limit//2 = 2) folded away; the rest stays verbatim
    assert len(c.memory.conversation) == 3
    assert c.memory.conversation[0]["content"] == "turn 2"


# --------------------------------------------------------------------------
# Profiles — isolation, sanitisation, listing, deletion
# --------------------------------------------------------------------------

def test_profile_dir_sanitizes_and_rejects_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(profiles, "PROFILES_DIR", tmp_path)
    # only letters/digits/-_space survive; '/', '.', '!' are all stripped
    p = profiles.profile_dir("Ada/../Lovelace!!")
    assert p == str(tmp_path / "AdaLovelace")
    with pytest.raises(ValueError):
        profiles.profile_dir("///")


def test_list_meta_and_delete_profiles(tmp_path, monkeypatch):
    monkeypatch.setattr(profiles, "PROFILES_DIR", tmp_path)
    for name, avatar in [("alice", "🌟"), ("bob", "🌙")]:
        d = tmp_path / name
        d.mkdir()
        (d / "config.json").write_text(json.dumps({"avatar": avatar, "name": name.title()}))

    assert profiles.list_profiles() == ["alice", "bob"]
    assert profiles.profile_meta("alice")["avatar"] == "🌟"
    assert profiles.profile_meta("alice")["name"] == "Alice"

    assert profiles.delete_profile("alice") is True
    assert profiles.list_profiles() == ["bob"]
    # deleting a non-existent profile is a safe no-op
    assert profiles.delete_profile("nobody") is False
