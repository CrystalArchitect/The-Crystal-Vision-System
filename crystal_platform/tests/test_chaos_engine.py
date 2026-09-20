from __future__ import annotations

import os
import unittest
from unittest import mock

from crystal_platform.chaos import DEFAULT_CHAOS_SEATS, ChaosEngine
from crystal_platform.orchestration import build_live_stack


class ChaosEngineTests(unittest.TestCase):
    def test_fanout_counts_silence_without_keys(self) -> None:
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
            engine = ChaosEngine(stack=build_live_stack(provider_ids=("local.open",)))
            seats = ("deepseek", "moonshot.kimi", "local.open")
            run = engine.run("Chaos engine is a go", seats=seats)
            self.assertEqual(run.cross_compare["seats_asked"], 3)
            self.assertEqual(len(run.replies), 3)
            by_id = {r.provider_id: r for r in run.replies}
            self.assertTrue(by_id["deepseek"].silent)
            self.assertTrue(by_id["moonshot.kimi"].silent)
            self.assertFalse(by_id["local.open"].silent)
            self.assertIn("local.open", by_id["local.open"].text)
            md = run.markdown()
            self.assertIn("Canon:** no", md)
            self.assertIn("count, not verdict", md.lower())

    def test_default_seats_exclude_manus(self) -> None:
        self.assertNotIn("manus", DEFAULT_CHAOS_SEATS)
        self.assertIn("deepseek", DEFAULT_CHAOS_SEATS)
        self.assertIn("moonshot.kimi", DEFAULT_CHAOS_SEATS)


if __name__ == "__main__":
    unittest.main()
