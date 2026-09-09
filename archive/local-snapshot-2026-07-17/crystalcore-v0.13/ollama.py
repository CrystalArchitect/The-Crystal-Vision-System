"""
Local Ollama HTTP boundary — chat, stream, embeddings.

One place for URLs, timeouts, and request shapes so companion.py does not
re-implement transport for every call path.
"""

from __future__ import annotations

import json
from typing import Any, Iterator, Optional

import requests

CHAT_URL = "http://localhost:11434/api/chat"
EMBED_URL = "http://localhost:11434/api/embeddings"
DEFAULT_EMBED_MODEL = "nomic-embed-text"


class OllamaClient:
    """Thin client for a local Ollama daemon. Nothing leaves the machine."""

    def __init__(self, model: str = "llama3.1:8b",
                 embed_model: str = DEFAULT_EMBED_MODEL,
                 chat_timeout: float = 300,
                 embed_timeout: float = 60):
        self.model = model
        self.embed_model = embed_model
        self.chat_timeout = chat_timeout
        self.embed_timeout = embed_timeout
        self._embed_ok = None

    def stream_chat(self, messages: list[dict[str, Any]],
                    temperature: float = 0.8) -> Iterator[str]:
        response = requests.post(
            CHAT_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": temperature},
            },
            timeout=self.chat_timeout,
            stream=True,
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            if piece:
                yield piece
            if chunk.get("done"):
                return

    def chat(self, messages: list[dict[str, Any]],
             temperature: float = 0.8) -> str:
        response = requests.post(
            CHAT_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=self.chat_timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def embed(self, text: str) -> Optional[list[float]]:
        """Return embedding vector, or None if unavailable this session."""
        if self._embed_ok is False:
            return None
        try:
            r = requests.post(
                EMBED_URL,
                json={"model": self.embed_model, "prompt": text},
                timeout=self.embed_timeout,
            )
            r.raise_for_status()
            emb = r.json().get("embedding")
        except requests.exceptions.RequestException:
            self._embed_ok = False
            return None
        if not emb:
            self._embed_ok = False
            return None
        self._embed_ok = True
        return emb


def user_facing_ollama_error(exc: BaseException, model: str) -> str:
    """Map transport failures to the same strings the CLI/web already show."""
    if isinstance(exc, requests.exceptions.ConnectionError):
        return (f"[I can't reach my local model — is Ollama running? "
                f"Try: ollama serve, then ollama pull {model}]")
    if isinstance(exc, requests.exceptions.Timeout):
        return ("[That took too long — the model may still be loading. "
                "Give it a moment and try again.]")
    if isinstance(exc, requests.exceptions.RequestException):
        return f"[Error talking to the local model: {exc}]"
    return f"[Error talking to the local model: {exc}]"
