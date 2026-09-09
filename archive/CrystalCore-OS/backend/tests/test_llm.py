"""
Direct unit tests for the tier-cascade logic in app.core.llm, independent of
the HTTP layer (see test_generate_api.py for the route-level tests, which
mock app.core.llm.generate itself rather than exercising the cascade).
"""

import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault(
    "ADMIN_PASSWORD_HASH",
    "$2b$12$KIXQeZ8N7z0m1G6f2N4o0eYh3l1qz1s1o1s1s1s1s1s1s1s1s1s1u",
)

import pytest  # noqa: E402

import app.core.llm as llm  # noqa: E402
from app.core.llm import (  # noqa: E402
    AllTiersUnavailableError,
    CloudNotConfiguredError,
    ModelNotAvailableError,
    generate,
)


def test_auto_uses_local_when_available(monkeypatch):
    monkeypatch.setattr(llm, "generate_local", lambda prompt, max_tokens, temperature: "local reply")
    monkeypatch.setattr(
        llm,
        "generate_cloud",
        lambda prompt, max_tokens, temperature: pytest.fail("cloud tier should not be called"),
    )

    completion, tier_used = generate("hello")
    assert (completion, tier_used) == ("local reply", "local")


def test_auto_falls_back_to_cloud_when_local_model_missing(monkeypatch):
    def _no_local(prompt, max_tokens, temperature):
        raise ModelNotAvailableError("no weights on disk")

    monkeypatch.setattr(llm, "generate_local", _no_local)
    monkeypatch.setattr(llm, "generate_cloud", lambda prompt, max_tokens, temperature: "cloud reply")

    completion, tier_used = generate("hello", tier="auto")
    assert (completion, tier_used) == ("cloud reply", "cloud")


def test_webllm_tier_cascades_the_same_as_auto(monkeypatch):
    def _no_local(prompt, max_tokens, temperature):
        raise ModelNotAvailableError("no weights on disk")

    monkeypatch.setattr(llm, "generate_local", _no_local)
    monkeypatch.setattr(llm, "generate_cloud", lambda prompt, max_tokens, temperature: "cloud reply")

    completion, tier_used = generate("hello", tier="webllm")
    assert (completion, tier_used) == ("cloud reply", "cloud")


def test_auto_raises_when_both_tiers_unavailable(monkeypatch):
    def _no_local(prompt, max_tokens, temperature):
        raise ModelNotAvailableError("no weights on disk")

    def _no_cloud(prompt, max_tokens, temperature):
        raise CloudNotConfiguredError("no api key")

    monkeypatch.setattr(llm, "generate_local", _no_local)
    monkeypatch.setattr(llm, "generate_cloud", _no_cloud)

    with pytest.raises(AllTiersUnavailableError) as exc_info:
        generate("hello")
    assert "no weights on disk" in str(exc_info.value)
    assert "no api key" in str(exc_info.value)


def test_tier_local_never_falls_back(monkeypatch):
    def _no_local(prompt, max_tokens, temperature):
        raise ModelNotAvailableError("no weights on disk")

    monkeypatch.setattr(llm, "generate_local", _no_local)
    monkeypatch.setattr(
        llm,
        "generate_cloud",
        lambda prompt, max_tokens, temperature: pytest.fail("cloud tier should not be called"),
    )

    with pytest.raises(ModelNotAvailableError):
        generate("hello", tier="local")


def test_tier_cloud_never_falls_back(monkeypatch):
    monkeypatch.setattr(
        llm,
        "generate_local",
        lambda prompt, max_tokens, temperature: pytest.fail("local tier should not be called"),
    )

    def _no_cloud(prompt, max_tokens, temperature):
        raise CloudNotConfiguredError("no api key")

    monkeypatch.setattr(llm, "generate_cloud", _no_cloud)

    with pytest.raises(CloudNotConfiguredError):
        generate("hello", tier="cloud")


def test_generate_cloud_reads_key_from_settings(monkeypatch):
    from app.core.config import get_settings

    get_settings.cache_clear()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    get_settings.cache_clear()

    with pytest.raises(CloudNotConfiguredError):
        llm.generate_cloud("hello")

    get_settings.cache_clear()
