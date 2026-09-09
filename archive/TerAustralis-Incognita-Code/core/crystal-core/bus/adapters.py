# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Real-AI adapters — thin, optional, stdlib-only.

Each adapter is a live model speaking on the Starline Weaver. No SDKs, no
dependencies: one HTTPS call per turn via urllib. An adapter whose API key
is missing does not crash the bus — it says so, labeled, and stays quiet.

Keys (environment variables):
    claude  ANTHROPIC_API_KEY
    gpt     OPENAI_API_KEY
    grok    XAI_API_KEY
"""

from __future__ import annotations

import json
import os
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
