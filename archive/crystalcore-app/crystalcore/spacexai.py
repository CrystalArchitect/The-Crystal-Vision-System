"""
SpaceXAI (xAI) HTTP boundary — chat and stream only.

Naming: "SpaceXAI" is the provider name; the real API is xAI's
OpenAI-compatible surface. Use XAI_API_KEY, https://api.x.ai/v1, and
current model ids from https://docs.x.ai — do not invent SPACEXAI_* vars.

Memory, embeddings, and files stay local. Only chat inference leaves the
device when the user explicitly opts into this provider.
"""

from __future__ import annotations

import json
import os
from typing import Any, Iterator, Optional

import requests

BASE_URL = "https://api.x.ai/v1"
CHAT_URL = f"{BASE_URL}/chat/completions"
DEFAULT_MODEL = "grok-4.5"
DEFAULT_PROVIDER = "spacexai"
# Reasoning models can think for a long time; docs recommend a high timeout.
DEFAULT_CHAT_TIMEOUT = 3600.0


class SpaceXAIClient:
    """Thin client for SpaceXAI / xAI. Requires XAI_API_KEY in the environment."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        chat_timeout: float = DEFAULT_CHAT_TIMEOUT,
    ):
        self.model = model or DEFAULT_MODEL
        # None = re-read os.environ each request (picks up late .env loads).
        self._api_key_override = api_key
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.chat_url = f"{self.base_url}/chat/completions"
        self.chat_timeout = chat_timeout

    @property
    def api_key(self) -> str:
        if self._api_key_override is not None:
            return self._api_key_override.strip()
        return os.environ.get("XAI_API_KEY", "").strip()

    def _headers(self) -> dict[str, str]:
        key = self.api_key
        if not key:
            raise RuntimeError(
                "XAI_API_KEY is not set. Create a key at https://console.x.ai "
                "and export it (or put it in a git-ignored .env)."
            )
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

    def stream_chat(
        self, messages: list[dict[str, Any]], temperature: float = 0.8
    ) -> Iterator[str]:
        response = requests.post(
            self.chat_url,
            headers=self._headers(),
            json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "temperature": temperature,
            },
            timeout=self.chat_timeout,
            stream=True,
        )
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            # Some proxies prefix SSE with whitespace or "data: "
            raw = line.strip()
            if not raw.startswith("data:"):
                continue
            payload = raw[5:].strip()
            if not payload:
                continue
            if payload == "[DONE]":
                break
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            # Surface mid-stream API errors if present
            if chunk.get("error"):
                msg = chunk["error"]
                if isinstance(msg, dict):
                    msg = msg.get("message") or str(msg)
                raise requests.exceptions.HTTPError(
                    str(msg), response=response
                )
            choices = chunk.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            piece = delta.get("content") or ""
            if piece:
                yield piece
            if choices[0].get("finish_reason"):
                break

    def chat(
        self, messages: list[dict[str, Any]], temperature: float = 0.8
    ) -> str:
        response = requests.post(
            self.chat_url,
            headers=self._headers(),
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "temperature": temperature,
            },
            timeout=self.chat_timeout,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            err = data["error"]
            if isinstance(err, dict):
                err = err.get("message") or str(err)
            raise RuntimeError(f"SpaceXAI error: {err}")
        choices = data.get("choices") or []
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        return message.get("content") or ""


def user_facing_spacexai_error(exc: BaseException, model: str) -> str:
    """Map transport / auth failures to plain companion-facing strings."""
    if isinstance(exc, RuntimeError) and "XAI_API_KEY" in str(exc):
        return (
            "[SpaceXAI needs an API key. Set XAI_API_KEY "
            "(https://console.x.ai), then try again.]"
        )
    if isinstance(exc, RuntimeError) and "SpaceXAI" in str(exc):
        return f"[{exc}]"
    if isinstance(exc, requests.exceptions.ConnectionError):
        return (
            "[I can't reach SpaceXAI (api.x.ai) — check your network "
            f"and try again. Model was {model}.]"
        )
    if isinstance(exc, requests.exceptions.Timeout):
        return (
            "[That took too long on SpaceXAI. Reasoning models can need a few "
            "minutes — try again, or lower temperature.]"
        )
    if isinstance(exc, requests.exceptions.HTTPError):
        status = getattr(exc.response, "status_code", None)
        if status in (401, 403):
            return (
                "[SpaceXAI rejected the API key. Check XAI_API_KEY at "
                "https://console.x.ai.]"
            )
        if status == 429:
            return "[SpaceXAI rate-limited this request. Wait a little and try again.]"
        detail = str(exc)
        if exc.response is not None:
            try:
                body = exc.response.json()
                detail = (
                    body.get("error", {}).get("message")
                    or body.get("message")
                    or detail
                )
            except Exception:
                text = (exc.response.text or "")[:200]
                if text:
                    detail = text
        extra = f" — {detail}" if detail else ""
        return f"[SpaceXAI error ({status}){extra}]"
    if isinstance(exc, requests.exceptions.RequestException):
        return f"[Error talking to SpaceXAI: {exc}]"
    return f"[Error talking to SpaceXAI: {exc}]"


def looks_like_spacexai_model(tag: str) -> bool:
    """Heuristic: grok-* model tags imply SpaceXAI when provider is auto."""
    t = (tag or "").strip().lower()
    return t.startswith("grok-") or t.startswith("xai:")
