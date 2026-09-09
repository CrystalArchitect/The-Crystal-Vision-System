# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""When recall stops choosing, the human is told.

Without embeddings there is no keyword fallback — that is a thing the old
docstring claimed and the code never did. What actually happens is that
`_memory_block` sends *every* memory instead of the most relevant ones, and
gets worse with each memory added. The companion keeps answering, so nothing
looks wrong; it is simply less focused than it was, for a reason nobody
mentioned.

A companion that quietly starts recalling worse while implying it has not is
the one behaviour this project exists to refuse. So these tests pin the
telling, not the degradation.

The threshold matters as much as the condition. Below MAX_MEMORIES the whole
store is sent anyway, so absent embeddings change nothing and announcing them
would be noise that teaches the human to ignore the notice. The tests check
both sides of that boundary.
"""

from crystalcore.companion import MAX_MEMORIES, Clementine


def _c(tmp_path, memories=0, embeddings=True):
    c = Clementine(memory_dir=str(tmp_path))
    c._embed_ok = True if embeddings else False
    for i in range(memories):
        c.memory.notes.append({"text": f"memory {i}", "tags": []})
    return c


# ------------------------------------------------------------ the condition

def test_working_embeddings_are_not_reported_as_degraded(tmp_path):
    c = _c(tmp_path, memories=MAX_MEMORIES + 20, embeddings=True)
    assert c.recall_degraded is False
    assert c.recall_notice() == ""


def test_untested_embeddings_are_not_reported_as_degraded(tmp_path):
    """None means nothing has been tried yet — not a failure."""
    c = _c(tmp_path, memories=MAX_MEMORIES + 20)
    c._embed_ok = None
    assert c.recall_degraded is False
    assert c.recall_notice() == ""


# ------------------------------------------------------------ the threshold

def test_a_small_memory_without_embeddings_is_not_degraded(tmp_path):
    """Everything is sent anyway at this size, so nothing has been lost and
    saying so would be noise."""
    c = _c(tmp_path, memories=MAX_MEMORIES - 1, embeddings=False)
    assert c.recall_degraded is False
    assert c.recall_notice() == ""


def test_exactly_at_the_limit_is_not_degraded(tmp_path):
    """The boundary is stated so it cannot drift silently."""
    c = _c(tmp_path, memories=MAX_MEMORIES, embeddings=False)
    assert c.recall_degraded is False


def test_one_over_the_limit_is_degraded(tmp_path):
    c = _c(tmp_path, memories=MAX_MEMORIES + 1, embeddings=False)
    assert c.recall_degraded is True


def test_facts_and_notes_count_together(tmp_path):
    """Recall draws on both, so the budget is shared."""
    c = _c(tmp_path, memories=MAX_MEMORIES - 3, embeddings=False)
    assert c.recall_degraded is False
    for i in range(4):
        c.memory.facts[f"k{i}"] = {"value": f"v{i}", "updated": "", "tags": []}
    assert c.recall_degraded is True


# --------------------------------------------------------------- the telling

def test_the_notice_says_what_and_why_and_how_to_fix_it(tmp_path):
    c = _c(tmp_path, memories=MAX_MEMORIES + 5, embeddings=False)
    c._embed_reason = "the embedding model could not be reached at local"
    notice = c.recall_notice()

    assert "could not be reached" in notice, "it must say why"
    assert str(MAX_MEMORIES + 5) in notice, "it must say how many are being sent"
    assert str(MAX_MEMORIES) in notice, "and how many should have been"
    assert "ollama pull" in notice, "it must say how to fix it"
    assert c.embed_model in notice, "naming the model that is missing"


def test_the_notice_still_works_when_the_reason_was_never_recorded(tmp_path):
    """Defensive: a future path could set the flag without the reason."""
    c = _c(tmp_path, memories=MAX_MEMORIES + 1, embeddings=False)
    c._embed_reason = ""
    assert "embeddings are unavailable" in c.recall_notice()


# ------------------------------------------------- the reason is distinguished

def test_a_refusal_at_the_gate_is_named_as_such(tmp_path, monkeypatch):
    """Three causes, told apart — a refusal is not an outage, and the fix
    differs."""
    c = _c(tmp_path, memories=MAX_MEMORIES + 1)
    c._embed_ok = None
    c.embed_endpoint = "https://api.example-vendor.test/v1/embeddings"

    assert c._embed("something") is None
    assert c._embed_ok is False
    assert "consent gate refused" in c._embed_reason


def test_an_unreachable_model_is_named_as_such(tmp_path, monkeypatch):
    import requests

    def boom(*a, **k):
        raise requests.exceptions.ConnectionError("nothing listening")

    c = _c(tmp_path, memories=MAX_MEMORIES + 1)
    c._embed_ok = None
    monkeypatch.setattr("crystalcore.companion.requests.post", boom)

    assert c._embed("something") is None
    assert "could not be reached" in c._embed_reason


def test_an_empty_response_is_named_as_such(tmp_path, monkeypatch):
    """The 'you never pulled the model' case, which looks like success at the
    HTTP layer and is the most confusing of the three."""
    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {}

    c = _c(tmp_path, memories=MAX_MEMORIES + 1)
    c._embed_ok = None
    monkeypatch.setattr("crystalcore.companion.requests.post",
                        lambda *a, **k: _Resp())

    assert c._embed("something") is None
    assert "returned nothing" in c._embed_reason
    assert c.embed_model in c._embed_reason


# ------------------------------------------------------- it reaches the human

def test_the_health_endpoint_reports_it(tmp_path):
    from server import create_app

    c = _c(tmp_path, memories=MAX_MEMORIES + 1, embeddings=False)
    c._embed_reason = "the embedding model could not be reached at local"
    client = create_app(c).test_client()

    body = client.get("/api/health").get_json()
    assert body["recall_degraded"] is True
    assert "could not be reached" in body["recall_notice"]


def test_the_health_endpoint_is_quiet_when_all_is_well(tmp_path):
    from server import create_app

    c = _c(tmp_path, memories=MAX_MEMORIES + 1, embeddings=True)
    body = create_app(c).test_client().get("/api/health").get_json()

    assert body["recall_degraded"] is False
    assert body["recall_notice"] == ""
