# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The parts of the Discord bot that can be wrong without anyone noticing.

Nothing here connects to Discord or starts a server. The gateway glue in
`discord_bot.build_client` is deliberately thin so that everything worth
checking — splitting, pacing, the allowlist, the error text — sits in
plain functions above it and can be driven directly.

`discord.py` is an optional dependency, and these tests do not import it.
That is on purpose: a test suite that only runs once you have installed
the optional extra is a test suite that stops running.
"""

import os

import pytest
import requests

import clementine_api
import discord_bot
from clementine_api import Clementine, ClementineAPIError, ClementineOffline


# ---------------------------------------------------------------- splitting

def test_short_text_is_one_piece():
    assert discord_bot.split_for_discord("hello") == ["hello"]


def test_empty_text_produces_nothing():
    assert discord_bot.split_for_discord("") == []


@pytest.mark.parametrize("text", [
    "word " * 900,                        # splits on spaces
    ("paragraph one.\n\n" * 200),         # splits on blank lines
    ("a line\n" * 500),                   # splits on newlines
    "Sentence here. " * 400,              # splits on sentence ends
    "x" * 5000,                           # no boundary at all
    "🍊" * 1500,                          # multi-byte, no boundary
])
def test_splitting_never_loses_a_character(text):
    """The property that matters more than tidy edges.

    A companion that silently drops the tail of a long answer is worse
    than one that breaks a sentence in an ugly place, so this is asserted
    for every shape of input rather than eyeballed on one.
    """
    pieces = discord_bot.split_for_discord(text)
    assert "".join(pieces) == text
    assert all(len(p) <= discord_bot.DISCORD_LIMIT for p in pieces)
    assert all(p for p in pieces), "produced an empty piece"


def test_splitting_prefers_a_paragraph_break_over_a_word_break():
    para = "a" * 1500 + "\n\n" + "b" * 1000
    first = discord_bot.split_for_discord(para)[0]
    assert first.endswith("\n\n"), "cut somewhere other than the blank line"


def test_unsplittable_run_is_cut_rather_than_refused():
    """A long URL has no boundary. Sending it in pieces beats not sending."""
    pieces = discord_bot.split_for_discord("x" * 4100)
    assert len(pieces) == 3
    assert [len(p) for p in pieces] == [2000, 2000, 100]


# ------------------------------------------------------------------- pacing

def test_pacer_does_not_push_when_nothing_arrived():
    pacer = discord_bot.StreamPacer(interval=1.0)
    pacer.pushed(now=10.0, current_len=50)
    assert pacer.should_push(now=99.0, current_len=50) is False


def test_pacer_waits_out_the_interval():
    pacer = discord_bot.StreamPacer(interval=1.0)
    pacer.pushed(now=10.0, current_len=50)
    assert pacer.should_push(now=10.5, current_len=60) is False
    assert pacer.should_push(now=11.0, current_len=60) is True


def test_pacer_pushes_immediately_when_a_message_is_full():
    """Waiting out the timer here would mean exceeding Discord's limit."""
    pacer = discord_bot.StreamPacer(interval=100.0)
    pacer.pushed(now=0.0, current_len=10)
    assert pacer.should_push(now=0.01, current_len=discord_bot.DISCORD_LIMIT) is True


# ---------------------------------------------------------------- allowlist

@pytest.mark.parametrize("raw,expected", [
    ("123", {123}),
    ("123,456", {123, 456}),
    ("123, 456", {123, 456}),
    ("123 456", {123, 456}),
    ("<@123>", {123}),           # pasted from Discord's copy-mention
    ("<@!123>", {123}),          # the nickname form
    ("", set()),
    ("   ", set()),
    ("not-an-id", set()),
    ("123,notanid,456", {123, 456}),
])
def test_owner_ids_parse_the_ways_people_write_them(raw, expected):
    assert discord_bot.parse_owner_ids(raw) == expected


def test_empty_allowlist_parses_to_empty_not_to_everyone():
    """The refusal in main() depends on this being falsy, so pin it."""
    assert not discord_bot.parse_owner_ids("")


@pytest.mark.parametrize("author,is_dm,mentioned,expected", [
    (1, True,  False, True),    # a DM from an owner
    (1, False, True,  True),    # mentioned in a channel by an owner
    (1, False, False, False),   # owner talking to someone else
    (2, True,  False, False),   # a DM from a stranger
    (2, False, True,  False),   # a stranger mentioning the bot
])
def test_who_gets_answered(author, is_dm, mentioned, expected):
    assert discord_bot.should_answer(
        author_id=author, is_dm=is_dm, mentioned=mentioned,
        author_is_self=False, owners={1}) is expected


def test_the_bot_never_answers_itself():
    """Without this a bot in its own DM channel can talk to itself forever."""
    assert discord_bot.should_answer(
        author_id=1, is_dm=True, mentioned=True,
        author_is_self=True, owners={1}) is False


def test_a_stranger_is_refused_even_in_a_dm():
    """The allowlist is the security gate; DMs must not bypass it."""
    assert discord_bot.should_answer(
        author_id=999, is_dm=True, mentioned=True,
        author_is_self=False, owners={1}) is False


# ------------------------------------------------------------------ replies

def test_status_falls_back_when_the_companion_has_no_name_yet():
    """A fresh profile has no name until they pick one, and `**{''}**`
    renders as a stray `****`. Caught by running the real client against a
    real server on a new memory folder, not by reading the code."""
    line = discord_bot.format_status(
        {"name": "", "avatar": "", "model": "llama3.1:8b",
         "profile": "default", "last_seen": "just now"})
    assert "****" not in line
    assert "**Clementine**" in line


def test_status_omits_fields_the_server_left_empty():
    line = discord_bot.format_status({"name": "Clementine", "avatar": "",
                                      "model": "", "profile": "", "last_seen": ""})
    assert line == "**Clementine**"


def test_status_includes_everything_when_present():
    line = discord_bot.format_status(
        {"name": "Clementine", "avatar": "🍊", "model": "m",
         "profile": "p", "last_seen": "an hour ago"})
    assert line == ("**Clementine** 🍊 · model `m` · profile `p` "
                    "· last seen an hour ago")


def test_mentions_are_stripped_before_the_model_sees_them():
    assert discord_bot.strip_mentions("<@42> hello", 42) == "hello"
    assert discord_bot.strip_mentions("<@!42> hello", 42) == "hello"


def test_mention_stripping_survives_a_client_with_no_identity_yet():
    """`client.user` is None until the gateway says ready."""
    assert discord_bot.strip_mentions("<@42> hello", None) == "<@42> hello"


def test_someone_elses_mention_is_left_alone():
    assert discord_bot.strip_mentions("<@7> hi", 42) == "<@7> hi"


# ------------------------------------------------------------------- --check

def _report(**over):
    args = dict(api_ok=True, api_detail="Clementine at x, model m",
                token_present=True, owners={1},
                gateway="ok", gateway_detail="connected as Bot#1")
    args.update(over)
    return discord_bot.check_report(**args)


def test_check_reports_all_clear_when_everything_passes():
    out = _report()
    assert "FAIL" not in out
    assert "All four green" in out


def test_check_names_the_missing_intent_and_how_to_fix_it():
    """The failure that makes a bot connect happily and then appear deaf."""
    out = _report(gateway="intent", gateway_detail="refused the intent")
    assert "FAIL" in out
    assert "MESSAGE CONTENT INTENT" in out


def test_check_explains_a_rejected_token():
    out = _report(gateway="token", gateway_detail="rejected")
    assert "Reset it" in out


def test_check_tells_you_where_to_find_your_user_id():
    out = _report(owners=set())
    assert "Copy User ID" in out
    assert "Developer Mode" in out


def test_check_tells_you_to_start_the_server():
    out = _report(api_ok=False, api_detail="nothing answering")
    assert "python server.py" in out


def test_check_shows_each_of_the_four_parts_separately():
    """One pass/fail would hide which part is broken. Counts the status
    markers only — the closing line mentions FAIL too, and an earlier
    version of this assertion tripped over exactly that."""
    out = _report(api_ok=False, api_detail="d", token_present=False,
                  owners=set(), gateway="network", gateway_detail="d")
    assert out.count("[ FAIL ]") == 4, "a failing part was reported as passing"


def test_check_does_not_blame_a_token_that_was_never_set():
    """Telling someone to reset a token they have not made yet is a wrong
    instruction at the moment they are following instructions."""
    out = _report(token_present=False, gateway="skipped",
                  gateway_detail="not attempted — no token set")
    assert "rejected" not in out
    assert "set DISCORD_TOKEN" in out


def test_memories_are_grouped_and_truncation_is_admitted():
    payload = {"facts": [{"handle": f"f{i}", "text": f"fact {i}"}
                         for i in range(30)],
               "notes": [], "reflections": []}
    out = discord_bot.format_memories(payload, limit=25)
    assert "**facts** (30)" in out
    assert "…and 5 more" in out, "hid the truncation"


def test_empty_memories_say_so_plainly():
    out = discord_bot.format_memories({"facts": [], "notes": [],
                                       "reflections": []})
    assert "isn't holding anything" in out


# ------------------------------------------------------------- the API client

class _FakeResponse:
    def __init__(self, status=200, body="", chunks=None):
        self.status_code = status
        self.text = body
        self._chunks = chunks or []

    def json(self):
        import json as _json
        return _json.loads(self.text)

    def iter_content(self, chunk_size=None, decode_unicode=False):
        return iter(self._chunks)


class _FakeSession:
    """Records what was sent, so the request itself can be asserted on."""

    def __init__(self, response=None, raises=None):
        self.response = response
        self.raises = raises
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if self.raises:
            raise self.raises
        return self.response


def test_a_refused_connection_becomes_a_named_offline_error():
    """The most common failure by far, and not the caller's fault."""
    session = _FakeSession(raises=requests.exceptions.ConnectionError("refused"))
    clem = Clementine(session=session)
    with pytest.raises(ClementineOffline) as caught:
        clem.status()
    assert "server.py" in str(caught.value), "didn't say how to fix it"


def test_an_error_status_carries_the_code_and_body():
    session = _FakeSession(_FakeResponse(415, "needs application/json"))
    clem = Clementine(session=session)
    with pytest.raises(ClementineAPIError) as caught:
        clem.teach("hi")
    assert caught.value.status == 415
    assert "application/json" in caught.value.body


def test_every_post_sets_the_json_content_type():
    """Without this header the server answers 415 — the guard that stops a
    cross-origin form from writing to memory."""
    session = _FakeSession(_FakeResponse(200, '{"ok": true}'))
    clem = Clementine(session=session)
    clem.teach("something")
    _, _, kwargs = session.calls[0]
    assert kwargs["headers"]["Content-Type"] == "application/json"


def test_reflect_sends_a_body_even_though_the_route_reads_none():
    """`/api/reflect` was the route a bodyless cross-site POST could reach.
    The client must not recreate that shape."""
    session = _FakeSession(_FakeResponse(200, '{"insights": "hm"}'))
    Clementine(session=session).reflect()
    _, _, kwargs = session.calls[0]
    assert kwargs["json"] == {}
    assert kwargs["headers"]["Content-Type"] == "application/json"


def test_chat_stream_yields_chunks_as_they_arrive():
    session = _FakeSession(_FakeResponse(200, "", chunks=["Hel", "lo ", "there"]))
    clem = Clementine(session=session)
    assert list(clem.chat_stream("hi")) == ["Hel", "lo ", "there"]


def test_chat_stream_decodes_bytes_and_skips_empty_chunks():
    session = _FakeSession(_FakeResponse(200, "", chunks=[b"caf", b"\xc3\xa9", "", b"!"]))
    assert Clementine(session=session).chat("hi") == "café!"


def test_offline_message_names_the_address_it_tried():
    text = clementine_api.describe_offline("http://127.0.0.1:5000")
    assert "127.0.0.1:5000" in text
    assert "own machine" in text


# --------------------------------------------- the client matches the server

def test_every_client_method_maps_to_a_route_that_exists():
    """The client is a third thing that can drift from the API.

    `api_surface.ROUTES` is the table `server.py` is held against, so
    holding the client against it too closes the loop: a method here for
    a route nobody serves fails, exactly as a documented-but-unbuilt
    route does.
    """
    if not os.environ.get("CLEMENTINE_SRC", "").strip():
        pytest.skip("needs the companion's source: set CLEMENTINE_SRC to the "
                    "clementine/ directory of a Clementine-ai-companion "
                    "checkout. See tests/conftest.py.")
    import api_surface
    paths = {r.path for r in api_surface.ROUTES}
    used = {
        "/api", "/api/status", "/api/chat/stream", "/api/memories",
        "/api/teach", "/api/forget", "/api/reflect", "/api/export",
        "/api/profile",
    }
    missing = used - paths
    assert not missing, f"the client calls routes that do not exist: {missing}"


def test_client_calls_the_paths_it_claims():
    """Guards the set above from going stale by checking the real calls."""
    expected = {
        "status": "/api/status",
        "memories": "/api/memories",
        "export": "/api/export",
        "profiles": "/api/profile",
    }
    for method, path in expected.items():
        session = _FakeSession(_FakeResponse(200, "{}"))
        getattr(Clementine(session=session), method)()
        _, url, _ = session.calls[0]
        assert url.endswith(path), f"{method}() called {url}"


def test_base_url_trailing_slash_does_not_double_up():
    session = _FakeSession(_FakeResponse(200, "{}"))
    Clementine(base="http://127.0.0.1:5000/", session=session).status()
    _, url, _ = session.calls[0]
    assert url == "http://127.0.0.1:5000/api/status"
