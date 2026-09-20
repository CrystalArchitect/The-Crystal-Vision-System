# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Real-AI adapters — thin, optional, stdlib-only.

Each adapter is a live model speaking on the Starline Weaver. No SDKs, no
dependencies: one HTTPS call per turn via urllib. An adapter whose API key
is missing does not crash the bus — it says so, labeled, and stays quiet.

Keys (environment variables):
    claude    ANTHROPIC_API_KEY
    gpt       OPENAI_API_KEY
    grok      XAI_API_KEY
    deepseek  DEEPSEEK_API_KEY
    kimi      MOONSHOT_API_KEY (alias: KIMI_API_KEY)
    manus     MANUS_API_KEY  (optional MANUS_BASE_URL)
    gemini    GEMINI_API_KEY
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request

from .agents import Agent
from .bus import Message

SYSTEM_PROMPT = (
    "You are speaking on the CrystalCore Starline Weaver with other AI systems. "
    "Reply in at most three sentences. Begin your reply with exactly one label "
    "in square brackets — [science], [story], or [vision] — matching the nature "
    "of your claim. Honour Country; make no false factual claims; no coercion."
)


def _post_json(url: str, headers: dict, body: dict, timeout: int = 60) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get_json(url: str, headers: dict, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _split_label(text: str) -> tuple[str, str]:
    text = text.strip()
    for layer in ("science", "story", "vision"):
        tag = f"[{layer}]"
        if text.lower().startswith(tag):
            return layer, text[len(tag):].strip()
    return "vision", text


class ModelAdapter(Agent):
    """Base for HTTP-backed model agents."""

    env_key = ""

    @property
    def configured(self) -> bool:
        return bool(os.environ.get(self.env_key))

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        if not self.configured:
            return {
                "layer": "science",
                "content": f"{self.name} is not configured ({self.env_key} unset); staying silent.",
            }
        prompt = f"{last.sender} said: {last.content}\nRespond on the bus."
        try:
            layer, content = _split_label(self._call(prompt))
        except Exception as err:  # noqa: BLE001 — a dead model must not kill the bus
            return {"layer": "science", "content": f"{self.name} call failed: {err}"}
        return {"layer": layer, "content": content}

    def _call(self, prompt: str) -> str:
        raise NotImplementedError


class AnthropicAdapter(ModelAdapter):
    name = "claude"
    env_key = "ANTHROPIC_API_KEY"
    model = "claude-sonnet-5"

    def _call(self, prompt: str) -> str:
        data = _post_json(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": os.environ[self.env_key], "anthropic-version": "2023-06-01"},
            {
                "model": self.model,
                "max_tokens": 300,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        return data["content"][0]["text"]


class OpenAIAdapter(ModelAdapter):
    name = "gpt"
    env_key = "OPENAI_API_KEY"
    model = "gpt-4o-mini"

    def _call(self, prompt: str) -> str:
        data = _post_json(
            "https://api.openai.com/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ[self.env_key]}"},
            {
                "model": self.model,
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        return data["choices"][0]["message"]["content"]


class XAIAdapter(OpenAIAdapter):
    name = "grok"
    env_key = "XAI_API_KEY"
    model = "grok-3-mini"

    def _call(self, prompt: str) -> str:
        data = _post_json(
            "https://api.x.ai/v1/chat/completions",
            {"Authorization": f"Bearer {os.environ[self.env_key]}"},
            {
                "model": self.model,
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        return data["choices"][0]["message"]["content"]


class DeepSeekAdapter(OpenAIAdapter):
    """OpenAI-compatible chat completions at api.deepseek.com."""

    name = "deepseek"
    env_key = "DEEPSEEK_API_KEY"
    model = "deepseek-chat"

    def _call(self, prompt: str) -> str:
        data = _post_json(
            "https://api.deepseek.com/chat/completions",
            {"Authorization": f"Bearer {os.environ[self.env_key]}"},
            {
                "model": self.model,
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        return data["choices"][0]["message"]["content"]


class KimiAdapter(OpenAIAdapter):
    """Moonshot / Kimi OpenAI-compatible chat completions."""

    name = "kimi"
    env_key = "MOONSHOT_API_KEY"
    model = "kimi-k2.5"

    @property
    def configured(self) -> bool:
        return bool(os.environ.get("MOONSHOT_API_KEY") or os.environ.get("KIMI_API_KEY"))

    def _api_key(self) -> str:
        return os.environ.get("MOONSHOT_API_KEY") or os.environ["KIMI_API_KEY"]

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        if not self.configured:
            return {
                "layer": "science",
                "content": (
                    f"{self.name} is not configured "
                    "(MOONSHOT_API_KEY / KIMI_API_KEY unset); staying silent."
                ),
            }
        prompt = f"{last.sender} said: {last.content}\nRespond on the bus."
        try:
            layer, content = _split_label(self._call(prompt))
        except Exception as err:  # noqa: BLE001
            return {"layer": "science", "content": f"{self.name} call failed: {err}"}
        return {"layer": layer, "content": content}

    def _call(self, prompt: str) -> str:
        data = _post_json(
            "https://api.moonshot.ai/v1/chat/completions",
            {"Authorization": f"Bearer {self._api_key()}"},
            {
                "model": self.model,
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        return data["choices"][0]["message"]["content"]


class GeminiAdapter(ModelAdapter):
    """Google Generative Language generateContent (stdlib)."""

    name = "gemini"
    env_key = "GEMINI_API_KEY"
    model = "gemini-2.0-flash"

    def _call(self, prompt: str) -> str:
        key = os.environ[self.env_key]
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={urllib.parse.quote(key)}"
        )
        data = _post_json(
            url,
            {},
            {
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 300},
            },
        )
        return data["candidates"][0]["content"]["parts"][0]["text"]


class ManusAdapter(ModelAdapter):
    """Manus Open API v2 — async task.create + listMessages poll.

    Guest on the Starline matrix only. Not a CVS roster bot (see BOT-STRUCTURE §7).
    """

    name = "manus"
    env_key = "MANUS_API_KEY"
    poll_interval_s = 2.0
    poll_timeout_s = 90.0

    @property
    def base_url(self) -> str:
        return (os.environ.get("MANUS_BASE_URL") or "https://api.manus.ai").rstrip("/")

    def _headers(self) -> dict:
        return {"x-manus-api-key": os.environ[self.env_key]}

    def _call(self, prompt: str) -> str:
        create = _post_json(
            f"{self.base_url}/v2/task.create",
            self._headers(),
            {
                "agent_profile": "lite",
                "interactive_mode": False,
                "hide_in_task_list": True,
                "title": "Starline Weaver matrix seat",
                "message": {
                    "content": (
                        f"{SYSTEM_PROMPT}\n\n"
                        f"Matrix turn (reply briefly, labeled):\n{prompt}"
                    ),
                },
            },
            timeout=90,
        )
        if not create.get("ok", True) and create.get("error"):
            err = create["error"]
            raise RuntimeError(err.get("message") or err)
        task_id = create.get("task_id")
        if not task_id:
            raise RuntimeError(f"manus create missing task_id: {create!r}")

        deadline = time.monotonic() + self.poll_timeout_s
        last_assistant = ""
        while time.monotonic() < deadline:
            qs = urllib.parse.urlencode(
                {"task_id": task_id, "order": "desc", "limit": "50"}
            )
            listing = _get_json(
                f"{self.base_url}/v2/task.listMessages?{qs}",
                self._headers(),
                timeout=60,
            )
            messages = listing.get("messages") or []
            agent_status = None
            for msg in messages:
                mtype = msg.get("type")
                if mtype == "status_update":
                    su = msg.get("status_update") or {}
                    agent_status = su.get("agent_status") or agent_status
                elif mtype == "assistant_message" and not last_assistant:
                    am = msg.get("assistant_message") or {}
                    content = am.get("content")
                    if isinstance(content, str) and content.strip():
                        last_assistant = content.strip()
                    elif isinstance(content, list):
                        bits = []
                        for part in content:
                            if isinstance(part, dict) and part.get("text"):
                                bits.append(str(part["text"]))
                            elif isinstance(part, str):
                                bits.append(part)
                        if bits:
                            last_assistant = "\n".join(bits).strip()
                elif mtype == "error_message":
                    em = msg.get("error_message") or {}
                    raise RuntimeError(em.get("content") or "manus error_message")

            if agent_status == "stopped" and last_assistant:
                return last_assistant
            if agent_status == "error":
                raise RuntimeError("manus agent_status=error")
            if agent_status == "waiting":
                # Matrix seat is non-interactive; surface what we have or fail closed.
                if last_assistant:
                    return last_assistant
                raise RuntimeError("manus waiting (interactive) — matrix expects a closed reply")

            time.sleep(self.poll_interval_s)

        if last_assistant:
            return last_assistant
        raise TimeoutError(f"manus task {task_id} timed out after {self.poll_timeout_s}s")
