"""Intelligence provider registry — add vendors without redesigning Core."""

from __future__ import annotations

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
    labels = {
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
    for pid in ids:
        reg.register(StubProvider(pid, labels.get(pid, pid)))
    return reg
