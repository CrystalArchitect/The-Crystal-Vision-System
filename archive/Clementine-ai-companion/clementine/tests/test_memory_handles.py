# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The contract the memory interface's safety guards are built on.

Forgetting is immediate and permanent — no undo, no bin. The interface that
offers it therefore has to be careful about *which* memory it destroys, and
the care it takes depends on two properties of this API. Neither was written
down anywhere, so neither was protected from a well-meant tidy-up.

The first is a hazard: note and reflection handles are positions in a list,
so deleting one renumbers every handle after it. A client holding a list
fetched a moment ago can therefore ask for `n3` and mean something the server
no longer agrees with. The interface closes that window by re-reading and
re-checking immediately before it deletes.

The second is the mitigation: /api/forget reports *what* it removed. That is
what lets a client compare the result against what the human agreed to and
say so when they differ. Losing that return value would not fail any existing
test while quietly turning a detectable wrong deletion into a silent one.

These tests pin both, so that changing either is a decision someone makes on
purpose rather than a side effect they never see.
"""

import pytest

from crystalcore.companion import Clementine


def _c(tmp_path, notes=(), facts=()):
    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = False
    for text in notes:
        c.memory.notes.append({"text": text, "tags": [], "when": ""})
    for key, value in facts:
        c.remember_fact(key, value)
    return c


# ------------------------------------------------------------- the hazard

def test_deleting_a_note_renumbers_the_ones_after_it(tmp_path):
    """The reason the interface re-checks before it destroys anything.

    If this ever becomes false the guard is merely redundant, which is fine.
    While it is true, removing the guard permanently destroys the wrong
    memory for anyone with two tabs open.
    """
    c = _c(tmp_path, notes=["ALPHA", "BRAVO", "CHARLIE", "DELTA"])

    assert c.memory.notes[2]["text"] == "CHARLIE", "n3 means CHARLIE"
    c.forget("n2")
    assert c.memory.notes[2]["text"] == "DELTA", "n3 now means DELTA"


def test_facts_keep_their_handle_when_a_neighbour_goes(tmp_path):
    """Facts are keyed, not positioned — the interface may trust their
    handle, and only theirs."""
    c = _c(tmp_path, facts=[("birthday", "June 3"), ("city", "Sydney")])

    c.forget("birthday")
    assert "city" in c.memory.facts
    assert c.memory.facts["city"]["value"] == "Sydney"


def test_reflections_renumber_the_same_way(tmp_path):
    c = _c(tmp_path)
    for text in ["first", "second", "third"]:
        c.memory.reflections.append({"text": text, "when": ""})

    c.forget("r1")
    assert c.memory.reflections[0]["text"] == "second"


# -------------------------------------------------------- the mitigation

def test_forget_reports_what_it_removed(tmp_path):
    """The interface compares this against what the human agreed to. Drop it
    and a wrong deletion stops being detectable."""
    c = _c(tmp_path, notes=["ALPHA", "BRAVO"])

    assert "BRAVO" in c.forget("n2")


def test_forgetting_a_fact_names_the_fact(tmp_path):
    c = _c(tmp_path, facts=[("birthday", "June 3")])
    assert "birthday" in c.forget("birthday")


def test_an_unmatched_handle_removes_nothing_and_says_so(tmp_path):
    c = _c(tmp_path, notes=["ALPHA"])

    assert c.forget("n9") == ""
    assert c.forget("") == ""
    assert len(c.memory.notes) == 1, "a miss must not disturb the store"


# ---------------------------------------------------- over HTTP, as served

def test_the_endpoint_returns_the_text_the_interface_checks(tmp_path):
    from server import create_app

    c = _c(tmp_path, notes=["ALPHA", "BRAVO"])
    client = create_app(c).test_client()

    body = client.post("/api/forget", json={"handle": "n2"}).get_json()
    assert body["ok"] is True
    assert "BRAVO" in body["forgotten"], \
        "the interface needs this to confirm the right memory went"


def test_a_miss_over_http_is_reported_as_a_miss(tmp_path):
    from server import create_app

    c = _c(tmp_path, notes=["ALPHA"])
    client = create_app(c).test_client()

    body = client.post("/api/forget", json={"handle": "n9"}).get_json()
    assert body["ok"] is False
    assert client.get("/api/memories").get_json()["notes"], "nothing was lost"


def _seeded(tmp_path):
    """One fact, two notes and a reflection, saved to disk."""
    c = _c(tmp_path, notes=["ALPHA", "BRAVO"], facts=[("birthday", "June 3")])
    c.memory.reflections.append({"text": "quiet mornings", "when": ""})
    c.save()
    return c


def test_every_listed_handle_is_one_forget_accepts(tmp_path):
    """The two endpoints have to agree, or the interface offers a button that
    deletes by a handle the server does not recognise."""
    from server import create_app

    client = create_app(_seeded(tmp_path)).test_client()
    listed = client.get("/api/memories").get_json()

    handles = ([m["handle"] for m in listed["facts"]]
               + [m["handle"] for m in listed["notes"]]
               + [m["handle"] for m in listed["reflections"]])
    assert handles == ["birthday", "n1", "n2", "r1"]


@pytest.mark.parametrize("handle", ["birthday", "n1", "n2", "r1"])
def test_each_listed_handle_resolves(tmp_path, handle):
    """Seeded fresh per handle on purpose: deleting one renumbers the rest,
    so checking them in sequence against a single store would test the
    renumbering rather than the handles."""
    assert _seeded(tmp_path).forget(handle) != "", \
        f"{handle} was listed by /api/memories but matched nothing"
