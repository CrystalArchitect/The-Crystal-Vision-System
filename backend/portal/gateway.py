"""Portal gateway route — Siri/App Intent and other surfaces enter here.

Forwards to crystal_platform StackOrchestrator. Does not call TAI or vendors directly.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

import backend.portal._path_setup  # noqa: F401
from crystal_platform.orchestration import build_live_stack
from crystal_platform.portal import EntryChannel, PortalIdentity, PortalRequest

router = APIRouter(prefix="/v1/gateway", tags=["gateway"])

# Live stack: HTTP providers when keys exist; silent/stub otherwise. Core still governs.
_stack = build_live_stack()


class GatewayAskBody(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    channel: str = "api"
    client: Optional[str] = None
    display_name: Optional[str] = None
    # Optional seat id from KNOWN_PROVIDER_IDS — Core router may honor if registered.
    provider_id: Optional[str] = None


class GatewayAskResponse(BaseModel):
    speech_text: str
    display_text: Optional[str] = None
    status: str
    correlation_id: Optional[str] = None
    provider_hint: Optional[str] = None


def _channel(raw: str) -> EntryChannel:
    try:
        return EntryChannel(raw)
    except ValueError:
        return EntryChannel.API


@router.post("/ask", response_model=GatewayAskResponse)
def ask(body: GatewayAskBody) -> Any:
    meta: dict[str, Any] = {}
    if body.client:
        meta["client"] = body.client
    if body.provider_id:
        meta["provider_id"] = body.provider_id
    req = PortalRequest(
        text=body.text,
        identity=PortalIdentity(
            steward_id=None,
            display_name=body.display_name,
            channel=_channel(body.channel),
            device_attested=body.channel in {"siri", "shortcut", "app_ui"},
        ),
        metadata=meta,
    )
    resp = _stack.accept(req)
    return GatewayAskResponse(
        speech_text=resp.speech_text,
        display_text=resp.display_text,
        status=resp.status,
        correlation_id=resp.correlation_id,
        provider_hint=resp.provider_hint,
    )
