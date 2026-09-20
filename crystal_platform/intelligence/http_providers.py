# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""HTTP intelligence providers — stdlib only, env-key gated.

CrystalCore.OS never imports this module's vendor URLs into its types.
TAI / Portal may register these when keys exist. Missing key → silent
CompletionResult (science-labeled text), not a hard crash.

Manus stays on the Starline bus (async task API) — not a sync Portal provider.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Mapping, Sequence

from crystal_platform.intelligence.provider import CompletionRequest, CompletionResult


SYSTEM_DEFAULT = (
    "You are a TAI intelligence provider on the Crystal stack. "
    "Be concise. Do not claim Canon. Do not invent Elon/xAI bonds. "
    "Label is applied by the caller when needed."
)


def _post_json(url: str, headers: Mapping[str, str], body: Mapping[str, object], timeout: int = 60) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", **dict(headers)},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _messages_as_openai(messages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]


class EnvHttpProvider:
    """Base: configured when env_key is set; otherwise returns a silent notice."""

    provider_id: str = ""
    display_name: str = ""
    env_key: str = ""
    model: str = "unspecified"

    def __init__(
        self,
        *,
        provider_id: str | None = None,
        display_name: str | None = None,
        env_key: str | None = None,
        model: str | None = None,
    ) -> None:
        if provider_id is not None:
            self.provider_id = provider_id
        if display_name is not None:
            self.display_name = display_name
        if env_key is not None:
            self.env_key = env_key
        if model is not None:
            self.model = model

    @property
    def configured(self) -> bool:
        return bool(self.env_key and os.environ.get(self.env_key))

    def complete(self, request: CompletionRequest) -> CompletionResult:
        if not self.configured:
            return CompletionResult(
                text=(
                    f"[{self.provider_id}] not configured "
                    f"({self.env_key or 'no-key'} unset); staying silent."
                ),
                provider_id=self.provider_id,
                model_name="silent",
            )
        try:
            text = self._call(request)
        except Exception as err:  # noqa: BLE001 — provider failure must not kill Core
            return CompletionResult(
                text=f"[{self.provider_id}] call failed: {err}",
                provider_id=self.provider_id,
                model_name="error",
            )
        return CompletionResult(
            text=text,
            provider_id=self.provider_id,
            model_name=self.model,
        )

    def _call(self, request: CompletionRequest) -> str:
        raise NotImplementedError


class OpenAICompatProvider(EnvHttpProvider):
    """Chat Completions shape used by OpenAI, xAI, DeepSeek, Moonshot/Kimi."""

    base_url: str = "https://api.openai.com/v1"

    def __init__(
        self,
        *,
        provider_id: str | None = None,
        display_name: str | None = None,
        env_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__(
            provider_id=provider_id,
            display_name=display_name,
            env_key=env_key,
            model=model,
        )
        if base_url is not None:
            self.base_url = base_url.rstrip("/")

    def _call(self, request: CompletionRequest) -> str:
        data = _post_json(
            f"{self.base_url}/chat/completions",
            {"Authorization": f"Bearer {os.environ[self.env_key]}"},
            {
                "model": self.model,
                "max_tokens": int(request.options.get("max_tokens", 400)),
                "messages": _messages_as_openai(request.messages),
            },
        )
        return data["choices"][0]["message"]["content"]


class AnthropicProvider(EnvHttpProvider):
    provider_id = "anthropic.claude"
    display_name = "Claude / Anthropic"
    env_key = "ANTHROPIC_API_KEY"
    model = "claude-sonnet-5"

    def _call(self, request: CompletionRequest) -> str:
        system = SYSTEM_DEFAULT
        user_parts: list[str] = []
        for m in request.messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                system = content
            else:
                user_parts.append(content)
        data = _post_json(
            "https://api.anthropic.com/v1/messages",
            {
                "x-api-key": os.environ[self.env_key],
                "anthropic-version": "2023-06-01",
            },
            {
                "model": self.model,
                "max_tokens": int(request.options.get("max_tokens", 400)),
                "system": system,
                "messages": [{"role": "user", "content": "\n".join(user_parts)}],
            },
        )
        return data["content"][0]["text"]


class GeminiProvider(EnvHttpProvider):
    provider_id = "google.gemini"
    display_name = "Gemini / Google"
    env_key = "GEMINI_API_KEY"
    model = "gemini-2.0-flash"

    def _call(self, request: CompletionRequest) -> str:
        system = SYSTEM_DEFAULT
        user_parts: list[str] = []
        for m in request.messages:
            if m.get("role") == "system":
                system = m.get("content", system)
            else:
                user_parts.append(m.get("content", ""))
        key = os.environ[self.env_key]
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={urllib.parse.quote(key)}"
        )
        data = _post_json(
            url,
            {},
            {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": "\n".join(user_parts)}]}],
                "generationConfig": {"maxOutputTokens": int(request.options.get("max_tokens", 400))},
            },
        )
        return data["candidates"][0]["content"]["parts"][0]["text"]


def chatgpt_provider() -> OpenAICompatProvider:
    return OpenAICompatProvider(
        provider_id="openai.chatgpt",
        display_name="ChatGPT / OpenAI",
        env_key="OPENAI_API_KEY",
        model="gpt-4o-mini",
        base_url="https://api.openai.com/v1",
    )


def grok_provider() -> OpenAICompatProvider:
    return OpenAICompatProvider(
        provider_id="xai.grok",
        display_name="Grok / xAI",
        env_key="XAI_API_KEY",
        model="grok-3-mini",
        base_url="https://api.x.ai/v1",
    )


def deepseek_provider() -> OpenAICompatProvider:
    return OpenAICompatProvider(
        provider_id="deepseek",
        display_name="DeepSeek",
        env_key="DEEPSEEK_API_KEY",
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
    )


class KimiProvider(OpenAICompatProvider):
    """Moonshot key or KIMI_API_KEY alias."""

    provider_id = "moonshot.kimi"
    display_name = "Kimi / Moonshot"
    env_key = "MOONSHOT_API_KEY"
    model = "kimi-k2.5"
    base_url = "https://api.moonshot.ai/v1"

    @property
    def configured(self) -> bool:
        return bool(os.environ.get("MOONSHOT_API_KEY") or os.environ.get("KIMI_API_KEY"))

    def _api_key(self) -> str:
        return os.environ.get("MOONSHOT_API_KEY") or os.environ["KIMI_API_KEY"]

    def complete(self, request: CompletionRequest) -> CompletionResult:
        if not self.configured:
            return CompletionResult(
                text=(
                    f"[{self.provider_id}] not configured "
                    "(MOONSHOT_API_KEY / KIMI_API_KEY unset); staying silent."
                ),
                provider_id=self.provider_id,
                model_name="silent",
            )
        try:
            text = self._call(request)
        except Exception as err:  # noqa: BLE001
            return CompletionResult(
                text=f"[{self.provider_id}] call failed: {err}",
                provider_id=self.provider_id,
                model_name="error",
            )
        return CompletionResult(
            text=text,
            provider_id=self.provider_id,
            model_name=self.model,
        )

    def _call(self, request: CompletionRequest) -> str:
        data = _post_json(
            f"{self.base_url}/chat/completions",
            {"Authorization": f"Bearer {self._api_key()}"},
            {
                "model": self.model,
                "max_tokens": int(request.options.get("max_tokens", 400)),
                "messages": _messages_as_openai(request.messages),
            },
        )
        return data["choices"][0]["message"]["content"]


def all_http_provider_factories() -> dict[str, object]:
    """provider_id → zero-arg factory. Manus omitted (async bus guest only)."""
    return {
        "openai.chatgpt": chatgpt_provider,
        "anthropic.claude": AnthropicProvider,
        "google.gemini": GeminiProvider,
        "xai.grok": grok_provider,
        "moonshot.kimi": KimiProvider,
        "deepseek": deepseek_provider,
    }
