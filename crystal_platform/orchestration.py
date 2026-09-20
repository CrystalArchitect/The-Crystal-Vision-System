"""Compose Siri/Portal → CrystalCore.OS → TAI → Intelligence / MCP without collapsing layers."""

from __future__ import annotations

import os
from typing import Sequence

from crystal_platform.capabilities import CapabilityRegistry
from crystal_platform.crystalcore_os import (
    AllowlistPermissionGate,
    CrystalCoreOS,
    GovernedTurn,
    InMemoryStore,
    PermissionDecision,
    StaticIntelligenceRouter,
)
from crystal_platform.intelligence import (
    ProviderRegistry,
    configured_provider_ids,
    default_registry,
    live_registry,
)
from crystal_platform.portal import PortalGateway, PortalRequest, PortalResponse
from crystal_platform.tai import EchoAgent, TAIRuntime, AgentRegistry


class PreferMetadataRouter:
    """Honor Portal metadata provider_id when present and known; else fallback list."""

    def __init__(self, fallback: Sequence[str], *, known: Sequence[str]) -> None:
        self._fallback = tuple(fallback)
        self._known = frozenset(known)

    def route(self, turn: GovernedTurn) -> tuple[str, ...]:
        hint = turn.request.metadata.get("provider_id")
        if isinstance(hint, str) and hint in self._known:
            return (hint,)
        return self._fallback


class StackOrchestrator(PortalGateway):
    """Portal gateway implementation that respects layer boundaries.

    Portal → Core.begin_turn → TAI.execute → providers/capabilities → PortalResponse
    """

    def __init__(
        self,
        *,
        core: CrystalCoreOS,
        tai: TAIRuntime,
        providers: ProviderRegistry,
        capabilities: CapabilityRegistry | None = None,
        default_agent_id: str = "tai.echo",
    ) -> None:
        self.core = core
        self.tai = tai
        self.providers = providers
        self.capabilities = capabilities or CapabilityRegistry()
        self.default_agent_id = default_agent_id

    def accept(self, request: PortalRequest) -> PortalResponse:
        turn = self.core.begin_turn(request, intended_action="respond")
        if turn.permission is PermissionDecision.DENY:
            return PortalResponse(
                speech_text="I can't do that.",
                status="denied",
                correlation_id=turn.turn_id,
            )
        if turn.permission is PermissionDecision.REQUIRE_HUMAN:
            return PortalResponse(
                speech_text="That needs your approval first.",
                status="needs_approval",
                correlation_id=turn.turn_id,
            )

        turn = self.core.attach_agent(turn, self.default_agent_id)
        result = self.tai.execute(
            turn,
            providers=self.providers.mapping(),
            capabilities=self.capabilities.mapping(),
            agent_id=self.default_agent_id,
        )
        return PortalResponse(
            speech_text=result.output_text,
            display_text=result.output_text,
            status="ok" if result.success else "error",
            correlation_id=turn.turn_id,
            provider_hint=",".join(result.used_providers) or None,
        )


def build_default_stack(*, provider_ids: tuple[str, ...] = ("local.open",)) -> StackOrchestrator:
    """Factory for local/dev: stub providers + echo agent + in-memory memory."""
    providers = default_registry(stub_ids=provider_ids)
    core = CrystalCoreOS(
        memory=InMemoryStore(),
        permissions=AllowlistPermissionGate(),
        router=StaticIntelligenceRouter(provider_ids),
    )
    agents = AgentRegistry()
    agents.register(EchoAgent())
    tai = TAIRuntime(agents)
    return StackOrchestrator(core=core, tai=tai, providers=providers)


def build_live_stack(
    *,
    provider_ids: tuple[str, ...] | None = None,
    prefer_env: bool = True,
) -> StackOrchestrator:
    """Portal path with HTTP providers behind Core routing.

    Default provider order: CRYSTAL_PROVIDER env → first configured key → local.open stub.
    Request metadata provider_id may override when registered.
    """
    providers = live_registry(include_stubs_for=("local.open", "manus", "meta.ai", "apple.intelligence"))
    # Always ensure local.open exists for offline fallback.
    if "local.open" not in providers.ids():
        from crystal_platform.intelligence.provider import StubProvider

        providers.register(StubProvider("local.open", "Local / open models"))

    if provider_ids is not None:
        fallback = provider_ids
    else:
        env_pref = os.environ.get("CRYSTAL_PROVIDER", "").strip()
        configured = configured_provider_ids() if prefer_env else ()
        if env_pref and env_pref in providers.ids():
            fallback = (env_pref,)
        elif configured:
            fallback = (configured[0],)
        else:
            fallback = ("local.open",)

    core = CrystalCoreOS(
        memory=InMemoryStore(),
        permissions=AllowlistPermissionGate(),
        router=PreferMetadataRouter(fallback, known=providers.ids()),
    )
    agents = AgentRegistry()
    agents.register(EchoAgent())
    tai = TAIRuntime(agents)
    return StackOrchestrator(core=core, tai=tai, providers=providers)
