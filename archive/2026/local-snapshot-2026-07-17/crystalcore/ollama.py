"""
Ollama client — the one place CrystalCore talks HTTP to the local model.

RECONSTRUCTED FILE (2026-07-17): the original ollama.py was lost with the
local machine and no bytecode for it was recovered. This reconstruction was
rebuilt from two verified sources: the pre-refactor HTTP code still present
in clementine/crystalcore/companion.py (this repository), and the exact
interface required by the recovered companion.py / expose.py / __init__.py
(which compile byte-identically to their .pyc files). Names, signatures,
and behavior follow that evidence; comment wording is not original.

Everything here targets localhost only. Nothing leaves the device.
"""

import requests

CHAT_URL = "http://localhost:11434/api/chat"
EMBED_URL = "http://localhost:11434/api/embeddings"
DEFAULT_EMBED_MODEL = "nomic-embed-text"  # optional: `ollama pull nomic-embed-text`


def user_facing_ollama_error(e: requests.exceptions.RequestException,
                             model: str) -> str:
    """A kind, actionable message for when the local model is unreachable.
    ConnectionError is checked first: ConnectTimeout subclasses both
    ConnectionError and Timeout, and 'is Ollama running?' is the right
    question for it."""
    if isinstance(e, requests.exceptions.ConnectionError):
        return ("[I can't reach my local model — is Ollama running? "
                f"Try: ollama serve, then ollama pull {model}]")
    if isinstance(e, requests.exceptions.Timeout):
        return ("[That took too long — the model may still be loading. "
                "Give it a moment and try again.]")
    return f"[Error talking to the local model: {e}]"


class OllamaClient:
    """Chat + embeddings against the local Ollama server.

    The companion owns memory and prompts; this client owns transport.
    Chat errors propagate as requests.exceptions.RequestException so the
    caller can turn them into a user-facing message; embeddings fail soft
    (None) because semantic recall is optional.
    """

    def __init__(self, model: str, embed_model: str = DEFAULT_EMBED_MODEL):
        self.model = model
        self.embed_model = embed_model
        self._embed_ok = None  # None = untested, then True/False

    # ---------- embeddings (optional, fail-soft) ----------

    def embed(self, text: str):
        """Return an embedding vector via local Ollama, or None if unavailable."""
        if self._embed_ok is False:
            return None
        try:
            r = requests.post(EMBED_URL,
                              json={"model": self.embed_model, "prompt": text},
                              timeout=60)
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

    # ---------- chat ----------

    def chat(self, messages: list, temperature: float = 0.8) -> str:
        """Non-streaming completion. Raises RequestException when offline."""
        response = requests.post(
            CHAT_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=300,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def stream_chat(self, messages: list, temperature: float = 0.8):
        """Yield reply pieces from the local model as they are generated.
        Raises RequestException when offline."""
        import json as _json

        response = requests.post(
            CHAT_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": temperature},
            },
            timeout=300,
            stream=True,
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = _json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            if piece:
                yield piece
            if chunk.get("done"):
                break
