"""Celestial Portal — human-facing gateway contracts.

Portal is the universal surface. It does not govern memory or run agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional
from uuid import UUID


class EntryChannel(str, Enum):
    """How a human request entered the gateway."""

    SIRI = "siri"
    APP_UI = "app_ui"
    VOICE = "voice"
    API = "api"
    SHORTCUT = "shortcut"


@dataclass(frozen=True)
class PortalIdentity:
    """Authenticated steward / user as seen by Portal (device-local biometrics upstream)."""

    steward_id: Optional[UUID]
    display_name: Optional[str] = None
    channel: EntryChannel = EntryChannel.API
    device_attested: bool = False


@dataclass(frozen=True)
class PortalRequest:
    """Inbound utterance or structured ask from a surface (including Siri App Intent)."""

    text: str
    identity: PortalIdentity
    locale: str = "en-AU"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    # Opaque correlation id for audit; Core assigns durable ids later.
    client_request_id: Optional[str] = None


@dataclass(frozen=True)
class PortalResponse:
    """What Portal may show / speak back. Provenance is Core's job."""

    speech_text: str
    display_text: Optional[str] = None
    status: str = "ok"  # ok | denied | needs_approval | error
    correlation_id: Optional[str] = None
    provider_hint: Optional[str] = None  # never required; Core may omit
    extras: Mapping[str, Any] = field(default_factory=dict)


class PortalGateway:
    """Surface adapter. Implementations forward to CrystalCore.OS — never to TAI directly."""

    def accept(self, request: PortalRequest) -> PortalResponse:
        raise NotImplementedError
