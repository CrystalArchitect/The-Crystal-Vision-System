from __future__ import annotations

import os
import unittest
from unittest import mock

from crystal_platform.crystalcore_os import PermissionDecision
from crystal_platform.intelligence import (
    KNOWN_PROVIDER_IDS,
    configured_provider_ids,
    default_registry,
    live_registry,
)
from crystal_platform.intelligence.http_providers import (
    AnthropicProvider,
    KimiProvider,
    chatgpt_provider,
    deepseek_provider,
    grok_provider,
)
from crystal_platform.intelligence.provider import CompletionRequest
from crystal_platform.orchestration import build_default_stack, build_live_stack
from crystal_platform.portal import EntryChannel, PortalIdentity, PortalRequest
from crystal_platform.tai import EchoAgent


class StackFoundationTests(unittest.TestCase):
    def test_providers_catalog_is_multi_vendor(self) -> None:
        self.assertIn("openai.chatgpt", KNOWN_PROVIDER_IDS)
        self.assertIn("xai.grok", KNOWN_PROVIDER_IDS)
        self.assertIn("apple.intelligence", KNOWN_PROVIDER_IDS)
        self.assertIn("moonshot.kimi", KNOWN_PROVIDER_IDS)
        self.assertIn("deepseek", KNOWN_PROVIDER_IDS)
        self.assertGreaterEqual(len(KNOWN_PROVIDER_IDS), 8)
        reg = default_registry()
        self.assertEqual(len(reg.ids()), len(KNOWN_PROVIDER_IDS))

    def test_core_is_not_an_agent(self) -> None:
        stack = build_default_stack()
        self.assertFalse(hasattr(stack.core, "run"))
        self.assertTrue(hasattr(stack.tai, "execute"))
        self.assertIsInstance(EchoAgent(), EchoAgent)

    def test_siri_channel_path_ok(self) -> None:
        stack = build_default_stack(provider_ids=("local.open",))
        req = PortalRequest(
            text="What is Celestial Portal?",
            identity=PortalIdentity(
                steward_id=None,
                display_name="Crystal",
                channel=EntryChannel.SIRI,
                device_attested=True,
            ),
        )
        resp = stack.accept(req)
        self.assertEqual(resp.status, "ok")
        self.assertIn("[local.open]", resp.speech_text)
        self.assertIsNotNone(resp.correlation_id)

    def test_irreversible_actions_require_human(self) -> None:
        stack = build_default_stack()
        turn = stack.core.begin_turn(
            PortalRequest(text="delete everything", identity=PortalIdentity(steward_id=None)),
            intended_action="delete_durable",
        )
        self.assertEqual(turn.permission, PermissionDecision.REQUIRE_HUMAN)


class LiveProviderTests(unittest.TestCase):
    def test_live_registry_registers_http_seats(self) -> None:
        reg = live_registry()
        for pid in (
            "openai.chatgpt",
            "deepseek",
            "moonshot.kimi",
            "xai.grok",
            "anthropic.claude",
            "google.gemini",
            "manus",
        ):
            self.assertIn(pid, reg.ids())

    def test_http_provider_silent_without_key(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            for key in (
                "OPENAI_API_KEY",
                "XAI_API_KEY",
                "DEEPSEEK_API_KEY",
                "ANTHROPIC_API_KEY",
                "MOONSHOT_API_KEY",
                "KIMI_API_KEY",
            ):
                os.environ.pop(key, None)
            for factory in (
                chatgpt_provider,
                grok_provider,
                deepseek_provider,
                AnthropicProvider,
                KimiProvider,
            ):
                provider = factory()
                result = provider.complete(
                    CompletionRequest(
                        messages=({"role": "user", "content": "ping"},),
                        provider_id=provider.provider_id,
                    )
                )
                self.assertEqual(result.model_name, "silent")
                self.assertIn("not configured", result.text)

    def test_live_stack_falls_back_to_local_without_keys(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            for key in (
                "OPENAI_API_KEY",
                "XAI_API_KEY",
                "DEEPSEEK_API_KEY",
                "ANTHROPIC_API_KEY",
                "MOONSHOT_API_KEY",
                "KIMI_API_KEY",
                "GEMINI_API_KEY",
                "CRYSTAL_PROVIDER",
            ):
                os.environ.pop(key, None)
            self.assertEqual(configured_provider_ids(), ())
            stack = build_live_stack()
            resp = stack.accept(
                PortalRequest(
                    text="hello stack",
                    identity=PortalIdentity(steward_id=None, channel=EntryChannel.API),
                )
            )
            self.assertEqual(resp.status, "ok")
            self.assertEqual(resp.provider_hint, "local.open")
            self.assertIn("[local.open]", resp.speech_text)

    def test_live_stack_honors_provider_metadata(self) -> None:
        stack = build_live_stack(provider_ids=("local.open",))
        resp = stack.accept(
            PortalRequest(
                text="route me",
                identity=PortalIdentity(steward_id=None),
                metadata={"provider_id": "deepseek"},
            )
        )
        self.assertEqual(resp.status, "ok")
        self.assertEqual(resp.provider_hint, "deepseek")
        self.assertIn("not configured", resp.speech_text)


if __name__ == "__main__":
    unittest.main()
