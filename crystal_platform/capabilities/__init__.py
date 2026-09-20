"""Capability layer — MCP, APIs, web, files, apps, data, devices, services."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol


class CapabilityKind(str, Enum):
    MCP = "mcp"
    API = "api"
    WEB = "web"
    FILE = "file"
    APP = "app"
    DATA = "data"
    DEVICE = "device"
    SERVICE = "service"


@dataclass(frozen=True)
class CapabilitySpec:
    capability_id: str
    kind: CapabilityKind
    description: str
    # Permission scopes CrystalCore must grant before use.
    required_scopes: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class CapabilityCall:
    capability_id: str
    operation: str
    arguments: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityResult:
    ok: bool
    data: Mapping[str, Any] = field(default_factory=dict)
    error: str | None = None


class Capability(Protocol):
    spec: CapabilitySpec

    def invoke(self, call: CapabilityCall) -> CapabilityResult:
        ...


class CapabilityRegistry:
    def __init__(self) -> None:
        self._caps: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        self._caps[capability.spec.capability_id] = capability

    def get(self, capability_id: str) -> Capability:
        return self._caps[capability_id]

    def mapping(self) -> dict[str, Capability]:
        return dict(self._caps)


class McpToolCapability:
    """Adapter shape for an MCP tool surface (CrystalBus, CrystalBridge, Voicebox, …)."""

    def __init__(self, *, capability_id: str, description: str, server_name: str) -> None:
        self.spec = CapabilitySpec(
            capability_id=capability_id,
            kind=CapabilityKind.MCP,
            description=description,
            required_scopes=frozenset({"mcp"}),
        )
        self.server_name = server_name

    def invoke(self, call: CapabilityCall) -> CapabilityResult:
        # Foundation: no live MCP wire here — preserve existing servers under backend/ and archive/.
        return CapabilityResult(
            ok=True,
            data={
                "echo": True,
                "server": self.server_name,
                "operation": call.operation,
                "arguments": dict(call.arguments),
            },
        )
