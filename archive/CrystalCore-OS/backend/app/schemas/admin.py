from datetime import datetime

from pydantic import BaseModel


class MemoryDiagnostics(BaseModel):
    total_gb: float
    used_gb: float
    percent: float


class DiskDiagnostics(BaseModel):
    total_gb: float
    used_gb: float
    percent: float


class DiagnosticsResponse(BaseModel):
    cpu_percent: float
    memory: MemoryDiagnostics
    disk: DiskDiagnostics
    collected_at: datetime


class ContainerResponse(BaseModel):
    id: str
    status: str
    image: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TerminalLogResponse(BaseModel):
    container_id: str
    lines: list[str]
    note: str = (
        "Log-replay only. Real command execution is not wired up in this "
        "prototype -- see backend/README.md before connecting a real "
        "container runtime."
    )
