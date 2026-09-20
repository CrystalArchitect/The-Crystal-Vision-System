"""Intelligence provider registry — add vendors without redesigning Core."""

from __future__ import annotations

import os
from typing import Dict, Iterable

from crystal_platform.intelligence.provider import IntelligenceProvider, StubProvider

# Stable ids for known seats. Implementations may be stubs until wired.
KNOWN_PROVIDER_IDS: tuple[str, ...] = (
    "openai.chatgpt",
    "anthropic.claude",
    "google.gemini",
    "xai.grok",
    "meta.ai",
    "moonshot.kimi",
    "deepseek",
    "manus",
    "apple.intelligence",
    "local.open",
)

PROVIDER_LABELS: dict[str, str] = {
    "openai.chatgpt": "ChatGPT / OpenAI",
    "anthropic.claude": "Claude / Anthropic",
    "google.gemini": "Gemini / Google",
    "xai.grok": "Grok / xAI",
    "meta.ai": "Meta AI",
    "moonshot.kimi": "Kimi / Moonshot",
    "deepseek": "DeepSeek",
    "manus": "Manus",
    "apple.intelligence": "Apple Intelligence",
    "local.open": "Local / open models",
}


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: Dict[str, IntelligenceProvider] = {}

    def register(self, provider: IntelligenceProvider) -> None:
        self._providers[provider.provider_id] = provider

    def get(self, provider_id: str) -> IntelligenceProvider:
        return self._providers[provider_id]

    def mapping(self) -> Dict[str, IntelligenceProvider]:
        return dict(self._providers)

    def ids(self) -> tuple[str, ...]:
        return tuple(self._providers.keys())


def default_registry(*, stub_ids: Iterable[str] | None = None) -> ProviderRegistry:
    """Register stub providers for the known catalog so Core never hard-codes one vendor."""
    reg = ProviderRegistry()
    ids = tuple(stub_ids) if stub_ids is not None else KNOWN_PROVIDER_IDS
    for pid in ids:
        reg.register(StubProvider(pid, PROVIDER_LABELS.get(pid, pid)))
    return reg


def live_registry(
    *,
    include_stubs_for: Iterable[str] | None = None,
    prefer_http: bool = True,
) -> ProviderRegistry:
    """HTTP providers for seats with adapters; stubs for the rest.

    Manus remains stub here (async Starline guest only). Missing env keys
    still register HTTP adapters — they return silent CompletionResults.
    """
    from crystal_platform.intelligence.http_providers import all_http_provider_factories

    reg = ProviderRegistry()
    factories = all_http_provider_factories() if prefer_http else {}
    stub_also = set(include_stubs_for) if include_stubs_for is not None else set(KNOWN_PROVIDER_IDS)

    for pid in KNOWN_PROVIDER_IDS:
        factory = factories.get(pid)
        if factory is not None:
            reg.register(factory())  # type: ignore[operator]
        elif pid in stub_also:
            reg.register(StubProvider(pid, PROVIDER_LABELS.get(pid, pid)))
    return reg


def configured_provider_ids() -> tuple[str, ...]:
    """Which HTTP seats have keys in this process (Manus never listed)."""
    checks = {
        "openai.chatgpt": ("OPENAI_API_KEY",),
        "anthropic.claude": ("ANTHROPIC_API_KEY",),
        "google.gemini": ("GEMINI_API_KEY",),
        "xai.grok": ("XAI_API_KEY",),
        "moonshot.kimi": ("MOONSHOT_API_KEY", "KIMI_API_KEY"),
        "deepseek": ("DEEPSEEK_API_KEY",),
    }
    found: list[str] = []
    for pid, keys in checks.items():
        if any(os.environ.get(k) for k in keys):
            found.append(pid)
    return tuple(found)
