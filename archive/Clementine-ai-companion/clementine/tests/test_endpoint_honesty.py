# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The address the gate judges must be the address the request goes to.

These tests exist because of what happens when those two drift apart. The
consent gate decides by looking at a URL: `destination_of(url)` returns
"local" for this machine and the hostname for anywhere else, and local calls
are allowed without asking. So if the gate is handed a hardcoded
`http://localhost:11434/...` while `requests.post` is handed a vendor's
address, the gate approves silently, the call leaves the machine, and the
audit log records the destination as "local".

That is worse than having no gate at all. A missing record is an absence; a
record saying "local" for a call that reached a vendor is a false statement,
and the audit log is the artefact the project's honesty claim rests on.

Nothing here can drift today — one attribute feeds both. These tests are what
keeps that true once a provider setting can move the endpoint, which is the
whole reason the attribute was introduced ahead of the providers themselves.

Offline by construction: `requests.post` is replaced, so a test that fails
by actually reaching the network fails loudly rather than quietly passing.
"""

import pytest

from crystalcore.companion import Clementine
from crystalcore.consent import ConsentRefused, Verdict

REMOTE = "https://api.example-vendor.test/v1/chat/completions"


class _Recorder:
    """Stands in for requests.post and records where the call would have gone."""

    def __init__(self):
        self.url = None
        self.calls = 0

    def __call__(self, url, json=None, headers=None, timeout=None, stream=False):
        self.url = url
        self.calls += 1

        class _Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {"message": {"content": "hi"}}

        return _Resp()


def _approve_everything(_request):
    return Verdict(True, "approved by the test", remember=False)


def test_local_endpoint_is_reported_as_local(tmp_path):
    """The default case, stated so the remote cases mean something."""
    c = Clementine(memory_dir=str(tmp_path))
    assert c.destination == "local"


def test_moving_the_endpoint_moves_the_reported_destination(tmp_path):
    """The `destination` property must follow the endpoint, not a constant."""
    c = Clementine(memory_dir=str(tmp_path))
    c.endpoint = REMOTE
    assert c.destination == "api.example-vendor.test"


def test_a_remote_endpoint_is_refused_when_there_is_nobody_to_ask(tmp_path, monkeypatch):
    """Fail-closed. asker=None means no way to ask, so the answer is no."""
    c = Clementine(memory_dir=str(tmp_path))  # asker defaults to None
    c.endpoint = REMOTE
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    with pytest.raises(ConsentRefused):
        c._model_chat([{"role": "user", "content": "hello"}])

    assert rec.calls == 0, "refused at the gate, so nothing may be sent"


def test_a_refused_remote_call_is_logged_against_the_real_destination(tmp_path, monkeypatch):
    """The regression this file exists for: the log must not say 'local'."""
    c = Clementine(memory_dir=str(tmp_path))
    c.endpoint = REMOTE
    monkeypatch.setattr("crystalcore.companion.requests.post", _Recorder())

    with pytest.raises(ConsentRefused):
        c._model_chat([{"role": "user", "content": "hello"}])

    entry = c.audit.entries()[-1]
    assert entry["destination"] == "api.example-vendor.test"
    assert entry["destination"] != "local"
    assert entry["outcome"] == "refused"


def test_an_approved_remote_call_goes_to_the_address_the_gate_judged(tmp_path, monkeypatch):
    """With consent given, the POST must land on the same URL the gate saw."""
    c = Clementine(memory_dir=str(tmp_path), asker=_approve_everything)
    c.endpoint = REMOTE
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    c._model_chat([{"role": "user", "content": "hello"}])

    assert rec.url == REMOTE, "the request must go where the gate was told"
    entry = c.audit.entries()[-1]
    assert entry["destination"] == "api.example-vendor.test"
    assert entry["outcome"] == "allowed"


def test_embeddings_are_gated_against_their_own_endpoint(tmp_path, monkeypatch):
    """Embeddings send the text of memories, so they get the same treatment.

    A refusal here is not fatal by design — recall falls back to the keyword
    path — so the assertion is that it refused and sent nothing, not that it
    raised.
    """
    c = Clementine(memory_dir=str(tmp_path))
    c.embed_endpoint = "https://api.example-vendor.test/v1/embeddings"
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    assert c._embed("something remembered") is None
    assert rec.calls == 0, "refused at the gate, so nothing may be sent"

    entry = c.audit.entries()[-1]
    assert entry["service"] == "embed"
    assert entry["destination"] == "api.example-vendor.test"
    assert entry["outcome"] == "refused"


def test_the_streaming_path_is_gated_too(tmp_path, monkeypatch):
    """chat_stream takes a different route to the same place; it must not be
    the way around the gate."""
    c = Clementine(memory_dir=str(tmp_path))
    c.endpoint = REMOTE
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    with pytest.raises(ConsentRefused):
        list(c._model_stream([{"role": "user", "content": "hello"}]))

    assert rec.calls == 0, "refused at the gate, so nothing may be sent"
