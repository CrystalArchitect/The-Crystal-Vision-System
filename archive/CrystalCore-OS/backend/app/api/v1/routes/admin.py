import logging
from datetime import datetime, timezone

import psutil
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.core.llm import AllTiersUnavailableError, CloudNotConfiguredError, ModelNotAvailableError
from app.core.llm import generate as llm_generate
from app.models.container import Container
from app.schemas.admin import (
    ContainerResponse,
    DiagnosticsResponse,
    DiskDiagnostics,
    MemoryDiagnostics,
    TerminalLogResponse,
)
from app.schemas.generate import GenerateRequest, GenerateResponse

router = APIRouter(dependencies=[Depends(get_current_admin)])
logger = logging.getLogger(__name__)

_BYTES_PER_GB = 1024**3

# In-memory log-replay store, keyed by container id. This intentionally
# does NOT execute anything -- it's a stand-in for wherever a real
# implementation would tail actual container logs. See backend/README.md.
_MOCK_TERMINAL_LOGS: dict[str, list[str]] = {
    "cc-container-01": [
        "[boot] CrystalCore.OS container init",
        "[boot] mounting overlay filesystem",
        "[svc] seldon-daemon started (pid 214)",
        "[svc] synthetic-affect bridge: listening",
        "root@cc-container-01:/# ",
    ]
}


@router.get("/diagnostics", response_model=DiagnosticsResponse)
def get_diagnostics() -> DiagnosticsResponse:
    cpu_percent = psutil.cpu_percent(interval=0.1)
    vmem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return DiagnosticsResponse(
        cpu_percent=cpu_percent,
        memory=MemoryDiagnostics(
            total_gb=round(vmem.total / _BYTES_PER_GB, 2),
            used_gb=round(vmem.used / _BYTES_PER_GB, 2),
            percent=vmem.percent,
        ),
        disk=DiskDiagnostics(
            total_gb=round(disk.total / _BYTES_PER_GB, 2),
            used_gb=round(disk.used / _BYTES_PER_GB, 2),
            percent=disk.percent,
        ),
        collected_at=datetime.now(timezone.utc),
    )


@router.get("/containers", response_model=list[ContainerResponse])
def list_containers(db: Session = Depends(get_db)) -> list[Container]:
    return db.query(Container).order_by(Container.id).all()


@router.get("/containers/{container_id}/terminal", response_model=TerminalLogResponse)
def get_container_terminal(container_id: str, db: Session = Depends(get_db)) -> TerminalLogResponse:
    container = db.get(Container, container_id)
    if container is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such container")

    lines = _MOCK_TERMINAL_LOGS.get(container_id, [f"[{container_id}] no log history recorded"])
    return TerminalLogResponse(container_id=container_id, lines=lines)


@router.post("/generate", response_model=GenerateResponse)
def generate_text(payload: GenerateRequest) -> GenerateResponse:
    """Three-tier completion: webllm (client-side, never reaches here) ->
    local (this machine's llama.cpp model) -> cloud (hosted API fallback).
    See app/core/llm.py for the cascade logic behind `tier`."""
    try:
        completion, tier_used = llm_generate(
            payload.prompt,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
            tier=payload.tier,
        )
    except (ModelNotAvailableError, CloudNotConfiguredError, AllTiersUnavailableError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    return GenerateResponse(completion=completion, tier_used=tier_used)
