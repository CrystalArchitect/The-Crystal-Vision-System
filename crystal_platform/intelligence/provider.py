"""Provider-agnostic intelligence contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence


@dataclass(frozen=True)
class CompletionRequest:
    messages: Sequence[Mapping[str, str]]
    provider_id: str
    # Vendor options stay in a bag — Core must not depend on their shape.
    options: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CompletionResult:
    text: str
    provider_id: str
    model_name: str = "unspecified"
    usage: Mapping[str, object] = field(default_factory=dict)


class IntelligenceProvider(Protocol):
    provider_id: str
    display_name: str

    def complete(self, request: CompletionRequest) -> CompletionResult:
        ...


class StubProvider:
    """Deterministic local stub — no network, no vendor SDK."""

    def __init__(self, provider_id: str, display_name: str) -> None:
        self.provider_id = provider_id
        self.display_name = display_name

    def complete(self, request: CompletionRequest) -> CompletionResult:
        last = request.messages[-1]["content"] if request.messages else ""
        return CompletionResult(
            text=f"[{self.provider_id}] {last}",
            provider_id=self.provider_id,
            model_name="stub",
        )
