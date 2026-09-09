# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Provider dialect tests — offline, asserting on the request that would be
sent rather than sending one.

The regression these exist to keep caught: `--llm-provider openai` was
advertised in the help text but the code only special-cased "grok" for the
OpenAI wire shape, so "openai" silently posted Ollama-shaped JSON (options
dict, no Authorization header) at the remote endpoint. Any alias in
OPENAI_COMPATIBLE must get the OpenAI shape; everything else gets Ollama's.

These diverge deliberately from the monorepo copy they came from, and the
difference is the point. There, a companion could be pointed at
`https://example.test/...` and would simply post to it — the suite asserted
that an ungated remote call succeeds, because that fork has no gate. Ported
unchanged, that would make the hole the specification.

Here every remote destination passes the consent gate, so a test that wants
one has to say so: it supplies an `asker` that approves, and consent is
visible in the test rather than absent from it. The inverse — no asker, so
nothing to ask, so refused — is asserted alongside it, because a dialect
test that only ever runs with permission granted would not notice if the
permission stopped being required.
"""

import pytest

from crystalcore.companion import Clementine
from crystalcore.consent import ConsentRefused, Verdict

REMOTE = "https://example.test/v1/chat/completions"


class _Recorder:
    """Stands in for requests.post and records what would have been sent."""

    def __init__(self):
        self.url = None
        self.json = None
        self.headers = None
        self.calls = 0

    def __call__(self, url, json=None, headers=None, timeout=None, stream=False):
        self.url = url
        self.json = json
        self.headers = headers or {}
        self.calls += 1

        class _Resp:
            def raise_for_status(self):
                pass

            def json(self):
                # Shape a minimal valid body for whichever dialect was used.
                return {"choices": [{"message": {"content": "hi"}}],
                        "message": {"content": "hi"}}

        return _Resp()


def _consenting(_request):
    """An asker that says yes, standing in for a human who was asked.

    Named for what it is. A test that reaches a vendor is a test about a call
    leaving the machine, and that should be legible at the call site rather
    than buried in a fixture.
    """
    return Verdict(True, "approved by the test", remember=False)


def _companion(tmp_path, monkeypatch, provider, endpoint=REMOTE, asker=_consenting):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    return Clementine(memory_dir=str(tmp_path), llm_provider=provider,
                      llm_endpoint=endpoint, llm_model="some-model",
                      asker=asker)


# --------------------------------------------------------------------------
# Dialect selection — pure, no request at all
# --------------------------------------------------------------------------

@pytest.mark.parametrize("alias", ["openai-compatible", "xai", "groq",
                                   "together", "openrouter", "grok"])
def test_every_alias_gets_the_openai_dialect(tmp_path, monkeypatch, alias):
    c = _companion(tmp_path, monkeypatch, alias)
    assert c._dialect() == "openai"


def test_ollama_is_not_an_openai_alias(tmp_path, monkeypatch):
    c = _companion(tmp_path, monkeypatch, "ollama",
                   endpoint="http://localhost:11434/api/chat")
    assert c._dialect() == "ollama"


# --------------------------------------------------------------------------
# Endpoint resolution — never guess a vendor's address
# --------------------------------------------------------------------------

def test_grok_alias_keeps_its_historical_default_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    c = Clementine(memory_dir=str(tmp_path), llm_provider="grok")
    assert "inference.do-ai.run" in c.endpoint


def test_other_remote_aliases_refuse_to_guess_an_endpoint(tmp_path, monkeypatch):
    """Guessing a vendor URL would send conversation somewhere never chosen."""
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    with pytest.raises(ValueError, match="llm-endpoint"):
        Clementine(memory_dir=str(tmp_path), llm_provider="openai")


# --------------------------------------------------------------------------
# Wire shapes — with consent given explicitly, because the destination is remote
# --------------------------------------------------------------------------

def test_openai_provider_sends_openai_shape(tmp_path, monkeypatch):
    """The original bug: 'openai' used to fall into the Ollama branch.

    Consent is granted here on purpose. This asserts the shape of a call that
    the human has agreed to make, which is the only kind that should ever be
    made.
    """
    c = _companion(tmp_path, monkeypatch, "openai")
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    c._model_chat([{"role": "user", "content": "hello"}])

    assert rec.json["temperature"], "OpenAI shape puts temperature at top level"
    assert "options" not in rec.json, "options dict is Ollama's shape"
    assert rec.json["model"] == "some-model", "OpenAI shape uses llm_model"
    assert rec.headers.get("Authorization") == "Bearer test-key"


def test_the_same_call_is_refused_when_there_is_nobody_to_ask(tmp_path, monkeypatch):
    """The inverse of the test above, and the reason it needs an asker.

    Identical configuration, consent withheld only because there is no way to
    ask for it. If this ever passes a request through, the dialect tests above
    have stopped proving what they claim to prove.
    """
    c = _companion(tmp_path, monkeypatch, "openai", asker=None)
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    with pytest.raises(ConsentRefused):
        c._model_chat([{"role": "user", "content": "hello"}])

    assert rec.calls == 0, "refused at the gate, so nothing may be sent"


def test_ollama_sends_ollama_shape_without_auth(tmp_path, monkeypatch):
    """Local, so no asker is needed and no credential is attached."""
    c = _companion(tmp_path, monkeypatch, "ollama",
                   endpoint="http://localhost:11434/api/chat", asker=None)
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    c._model_chat([{"role": "user", "content": "hello"}])

    assert "options" in rec.json, "Ollama shape nests temperature in options"
    assert rec.headers.get("Authorization") is None


def test_the_openai_streaming_path_is_gated_too(tmp_path, monkeypatch):
    """Streaming reaches the same vendor by a different method."""
    c = _companion(tmp_path, monkeypatch, "openai", asker=None)
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    with pytest.raises(ConsentRefused):
        list(c._model_stream([{"role": "user", "content": "hello"}]))

    assert rec.calls == 0, "refused at the gate, so nothing may be sent"


# --------------------------------------------------------------------------
# The audit log must name the model that was actually used
# --------------------------------------------------------------------------

def test_the_log_records_the_model_that_went_on_the_wire(tmp_path, monkeypatch):
    """The same trap as the endpoint, one field over.

    The two dialects read the model name from different attributes. If the
    gate is told `self.model` while an OpenAI request carries `llm_model`,
    the log names a model nobody asked for — a record that is precise,
    plausible, and wrong.
    """
    c = _companion(tmp_path, monkeypatch, "openai")
    rec = _Recorder()
    monkeypatch.setattr("crystalcore.companion.requests.post", rec)

    c._model_chat([{"role": "user", "content": "hello"}])

    entry = c.audit.entries()[-1]
    assert entry["model"] == rec.json["model"] == "some-model"
    assert entry["destination"] == "example.test"
    assert entry["outcome"] == "allowed"
