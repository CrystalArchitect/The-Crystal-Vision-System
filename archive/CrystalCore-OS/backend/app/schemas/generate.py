from typing import Literal

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    max_tokens: int = Field(default=256, ge=1, le=2048)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    # "auto" (default) and "webllm" both cascade local -> cloud server-side.
    # "webllm" exists as a distinct value so a client that already tried the
    # in-browser tier and failed can say so explicitly (useful in logs/metrics)
    # without changing behavior. "local"/"cloud" pin to one tier, no fallback.
    tier: Literal["auto", "webllm", "local", "cloud"] = "auto"


class GenerateResponse(BaseModel):
    completion: str
    tier_used: Literal["local", "cloud"]
