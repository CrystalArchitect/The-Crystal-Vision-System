"""CrystalCore.OS — governance and cognitive substrate.

NOT an agent. Owns: governance, providence, memory, identity/context,
permissions/trust, models of thinking, intelligence routing, coordination,
persistent system state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Protocol, Sequence
from uuid import UUID, uuid4

from crystal_platform.portal import PortalIdentity, PortalRequest


class PermissionDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_HUMAN = "require_human"


@dataclass(frozen=True)
class MemoryRecord:
    """Durable memory belongs to CrystalCore.OS (Vault / MemoryCore)."""

    key: str
    content: Mapping[str, Any]
    layer: str = "fact"  # science | story | vision | fact | coordination
    provenance: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class TrustContext:
    identity: PortalIdentity
    scopes: frozenset[str] = field(default_factory=frozenset)
    risk_class: str = "normal"  # normal | elevated | irreversible


@dataclass(frozen=True)
class RoutePlan:
    """Core chooses *how* to think/act without becoming the actor."""

    agent_id: Optional[str]
    provider_ids: tuple[str, ...]
    capability_ids: tuple[str, ...] = ()
    thinking_model: str = "default"  # Core's model-of-thinking label, not a vendor
    rationale: str = ""


@dataclass(frozen=True)
class GovernedTurn:
    """A single governed request after permission + memory attach."""

    turn_id: str
    request: PortalRequest
    trust: TrustContext
    memory: tuple[MemoryRecord, ...]
    plan: RoutePlan
    permission: PermissionDecision


class MemoryStore(Protocol):
    def recall(self, identity: PortalIdentity, query: str, *, limit: int = 8) -> Sequence[MemoryRecord]:
        ...

    def remember(self, identity: PortalIdentity, record: MemoryRecord) -> None:
        ...


class PermissionGate(Protocol):
    def evaluate(self, trust: TrustContext, action: str, *, payload: Mapping[str, Any]) -> PermissionDecision:
        ...


class IntelligenceRouter(Protocol):
    """Select provider ids without leaking vendor APIs into callers."""

    def route(self, turn: GovernedTurn) -> tuple[str, ...]:
        ...


class CrystalCoreOS:
    """Governance substrate. Coordinates TAI + intelligence + capabilities; does not execute agent work."""

    def __init__(
        self,
        *,
        memory: MemoryStore,
        permissions: PermissionGate,
        router: IntelligenceRouter,
    ) -> None:
        self._memory = memory
        self._permissions = permissions
        self._router = router

    def begin_turn(self, request: PortalRequest, *, intended_action: str = "respond") -> GovernedTurn:
        trust = TrustContext(identity=request.identity)
        permission = self._permissions.evaluate(
            trust,
            intended_action,
            payload={"text": request.text, "channel": request.identity.channel.value},
        )
        memory = tuple(self._memory.recall(request.identity, request.text))
        # Agent selection is deferred to TAI; Core only frames the plan skeleton.
        skeleton = RoutePlan(
            agent_id=None,
            provider_ids=(),
            capability_ids=(),
            thinking_model="default",
            rationale="skeleton — TAI fills agent; router fills providers after allow",
        )
        turn = GovernedTurn(
            turn_id=str(uuid4()),
            request=request,
            trust=trust,
            memory=memory,
            plan=skeleton,
            permission=permission,
        )
        if permission is PermissionDecision.ALLOW:
            providers = self._router.route(turn)
            turn = GovernedTurn(
                turn_id=turn.turn_id,
                request=turn.request,
                trust=turn.trust,
                memory=turn.memory,
                plan=RoutePlan(
                    agent_id=turn.plan.agent_id,
                    provider_ids=tuple(providers),
                    capability_ids=turn.plan.capability_ids,
                    thinking_model=turn.plan.thinking_model,
                    rationale="providers assigned by CrystalCore intelligence router",
                ),
                permission=turn.permission,
            )
        return turn

    def attach_agent(self, turn: GovernedTurn, agent_id: str) -> GovernedTurn:
        """Record which TAI agent will act — Core still does not run it."""
        if turn.permission is not PermissionDecision.ALLOW:
            raise PermissionError("cannot attach agent when permission is not ALLOW")
        plan = RoutePlan(
            agent_id=agent_id,
            provider_ids=turn.plan.provider_ids,
            capability_ids=turn.plan.capability_ids,
            thinking_model=turn.plan.thinking_model,
            rationale=turn.plan.rationale,
        )
        return GovernedTurn(
            turn_id=turn.turn_id,
            request=turn.request,
            trust=turn.trust,
            memory=turn.memory,
            plan=plan,
            permission=turn.permission,
        )


# --- Default in-memory stubs (tests / local only; not production Vault) ---


class InMemoryStore:
    def __init__(self) -> None:
        self._rows: list[tuple[Optional[UUID], MemoryRecord]] = []

    def recall(self, identity: PortalIdentity, query: str, *, limit: int = 8) -> Sequence[MemoryRecord]:
        q = query.lower()
        hits = [r for _, r in self._rows if q in r.key.lower() or q in str(r.content).lower()]
        return hits[:limit]

    def remember(self, identity: PortalIdentity, record: MemoryRecord) -> None:
        self._rows.append((identity.steward_id, record))


class AllowlistPermissionGate:
    def __init__(self, *, allow_actions: frozenset[str] | None = None) -> None:
        self._allow = allow_actions or frozenset({"respond", "recall"})

    def evaluate(self, trust: TrustContext, action: str, *, payload: Mapping[str, Any]) -> PermissionDecision:
        if action in {"spend", "deploy", "delete_durable", "public_post"}:
            return PermissionDecision.REQUIRE_HUMAN
        if action in self._allow:
            return PermissionDecision.ALLOW
        return PermissionDecision.DENY


class StaticIntelligenceRouter:
    """Routes to configured provider ids — never imports a vendor SDK."""

    def __init__(self, provider_ids: Sequence[str]) -> None:
        self._provider_ids = tuple(provider_ids)

    def route(self, turn: GovernedTurn) -> tuple[str, ...]:
        return self._provider_ids
