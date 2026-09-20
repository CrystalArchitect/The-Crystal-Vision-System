from __future__ import annotations

import unittest

from crystal_platform.crystalcore_os import PermissionDecision
from crystal_platform.orchestration import build_default_stack
from crystal_platform.portal import EntryChannel, PortalIdentity, PortalRequest
from crystal_platform.intelligence import KNOWN_PROVIDER_IDS, default_registry
from crystal_platform.tai import EchoAgent


class StackFoundationTests(unittest.TestCase):
    def test_providers_catalog_is_multi_vendor(self) -> None:
        self.assertIn("openai.chatgpt", KNOWN_PROVIDER_IDS)
        self.assertIn("xai.grok", KNOWN_PROVIDER_IDS)
        self.assertIn("apple.intelligence", KNOWN_PROVIDER_IDS)
        self.assertGreaterEqual(len(KNOWN_PROVIDER_IDS), 8)
        reg = default_registry()
        self.assertEqual(len(reg.ids()), len(KNOWN_PROVIDER_IDS))

    def test_core_is_not_an_agent(self) -> None:
        stack = build_default_stack()
        # CrystalCoreOS has begin_turn / attach_agent — no .run agent method.
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


if __name__ == "__main__":
    unittest.main()
