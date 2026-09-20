"""TAI — TerAustralis Incognita agent layer.

Agents perform work. CrystalCore.OS governs; TAI executes.
Do not put MemoryCore ownership or Canon stamps in this package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Protocol, Sequence

from crystal_platform.crystalcore_os import GovernedTurn, PermissionDecision
from crystal_platform.intelligence.provider import CompletionRequest, CompletionResult, IntelligenceProvider


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    name: str
    description: str
    allowed_capabilities: frozenset[str] = field(default_factory=frozenset)
    # Preferred providers are hints only; Core router may override.
    preferred_providers: tuple[str, ...] = ()


@dataclass(frozen=True)
class AgentResult:
    agent_id: str
    output_text: str
    success: bool
    used_providers: tuple[str, ...] = ()
    used_capabilities: tuple[str, ...] = ()
    artifacts: Mapping[str, Any] = field(default_factory=dict)


class Agent(Protocol):
    spec: AgentSpec

    def run(
        self,
        turn: GovernedTurn,
        *,
        providers: Mapping[str, IntelligenceProvider],
        capabilities: Mapping[str, Any],
    ) -> AgentResult:
        ...


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        self._agents[agent.spec.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        return self._agents[agent_id]

    def list(self) -> Sequence[AgentSpec]:
        return tuple(a.spec for a in self._agents.values())

    def select_default(self, turn: GovernedTurn) -> Optional[str]:
        if not self._agents:
            return None
        # Stable default: first registered. Real policy lives in Core + TAI planners later.
        return next(iter(self._agents))


class TAIRuntime:
    """Executes agents only after CrystalCore.OS ALLOW."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def execute(
        self,
        turn: GovernedTurn,
        *,
        providers: Mapping[str, IntelligenceProvider],
        capabilities: Mapping[str, Any] | None = None,
        agent_id: Optional[str] = None,
    ) -> AgentResult:
        if turn.permission is not PermissionDecision.ALLOW:
            return AgentResult(
                agent_id=agent_id or "none",
                output_text="Permission denied or human approval required.",
                success=False,
            )
        chosen = agent_id or turn.plan.agent_id or self.registry.select_default(turn)
        if not chosen:
            return AgentResult(agent_id="none", output_text="No TAI agent registered.", success=False)
        agent = self.registry.get(chosen)
        return agent.run(turn, providers=providers, capabilities=capabilities or {})


class EchoAgent:
    """Minimal agent: asks an intelligence provider to think, returns text. No tools."""

    def __init__(self, spec: AgentSpec | None = None) -> None:
        self.spec = spec or AgentSpec(
            agent_id="tai.echo",
            name="Echo",
            description="Minimal think→speak agent for foundation tests",
        )

    def run(
        self,
        turn: GovernedTurn,
        *,
        providers: Mapping[str, IntelligenceProvider],
        capabilities: Mapping[str, Any],
    ) -> AgentResult:
        provider_ids = turn.plan.provider_ids or tuple(providers.keys())
        if not provider_ids:
            return AgentResult(agent_id=self.spec.agent_id, output_text="No intelligence provider.", success=False)
        pid = provider_ids[0]
        provider = providers[pid]
        result: CompletionResult = provider.complete(
            CompletionRequest(
                messages=(
                    {"role": "system", "content": "You are a TAI agent. Be concise. Do not claim Canon."},
                    {"role": "user", "content": turn.request.text},
                ),
                provider_id=pid,
            )
        )
        return AgentResult(
            agent_id=self.spec.agent_id,
            output_text=result.text,
            success=True,
            used_providers=(pid,),
        )
