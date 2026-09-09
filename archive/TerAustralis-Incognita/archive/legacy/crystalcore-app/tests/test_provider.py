"""Offline tests for SpaceXAI / Ollama provider selection.

No network calls — never hit api.x.ai or Ollama.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from crystalcore import (
    BASE_PROMPT_LOCAL,
    BASE_PROMPT_SPACEXAI,
    Clementine,
    __version__,
    load_dotenv,
    looks_like_spacexai_model,
    normalize_provider,
    user_facing_spacexai_error,
    xai_api_key_present,
)
from crystalcore.profiles import profile_meta


class NormalizeProviderTests(unittest.TestCase):
    def test_aliases(self):
        self.assertEqual(normalize_provider("spacexai"), "spacexai")
        self.assertEqual(normalize_provider("xai"), "spacexai")
        self.assertEqual(normalize_provider("X.AI"), "spacexai")
        self.assertEqual(normalize_provider("grok"), "spacexai")
        self.assertEqual(normalize_provider("ollama"), "ollama")
        self.assertEqual(normalize_provider("local"), "ollama")
        self.assertEqual(normalize_provider(""), "ollama")
        self.assertEqual(normalize_provider("unknown"), "ollama")


class ModelHeuristicTests(unittest.TestCase):
    def test_grok_tags(self):
        self.assertTrue(looks_like_spacexai_model("grok-4.5"))
        self.assertTrue(looks_like_spacexai_model("xai:grok-4.5"))
        self.assertFalse(looks_like_spacexai_model("llama3.1:8b"))
        self.assertFalse(looks_like_spacexai_model(""))


class CompanionProviderTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.mem = self._tmpdir.name

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_default_is_ollama(self):
        c = Clementine(memory_dir=self.mem, provider="")
        self.assertEqual(c.provider, "ollama")
        prompt = c.system_prompt()
        self.assertIn("no connection to any external servers", prompt)
        self.assertNotIn("opted in to SpaceXAI", prompt)

    def test_set_provider_spacexai_upgrades_model(self):
        c = Clementine(model="llama3.1:8b", memory_dir=self.mem, provider="ollama")
        c.set_provider("spacexai")
        self.assertEqual(c.provider, "spacexai")
        self.assertEqual(c.model, "grok-4.5")
        self.assertEqual(c.personality.provider, "spacexai")
        self.assertTrue(c.personality.cloud_opt_in)
        self.assertTrue(c.personality.cloud_opt_in_at)
        prompt = c.system_prompt()
        self.assertIn("opted in to SpaceXAI", prompt)
        # Without XAI_API_KEY, runtime is local fallback — prompt says so.
        if c.spacexai_using_local_fallback():
            self.assertIn("local model", prompt.lower())
        else:
            self.assertNotIn("no connection to any external servers", prompt)

    def test_set_model_grok_auto_provider(self):
        c = Clementine(model="llama3.1:8b", memory_dir=self.mem, provider="ollama")
        c.set_model("grok-4.5")
        self.assertEqual(c.provider, "spacexai")
        self.assertEqual(c.model, "grok-4.5")
        self.assertTrue(c.personality.cloud_opt_in)

    def test_set_model_xai_prefix(self):
        c = Clementine(memory_dir=self.mem, provider="ollama")
        c.set_model("xai:grok-4.5")
        self.assertEqual(c.provider, "spacexai")
        self.assertEqual(c.model, "grok-4.5")

    def test_set_model_local_leaves_cloud_backend(self):
        c = Clementine(memory_dir=self.mem, provider="spacexai")
        self.assertEqual(c.provider, "spacexai")
        c.set_model("llama3.2:3b")
        self.assertEqual(c.provider, "ollama")
        self.assertEqual(c.model, "llama3.2:3b")

    def test_set_provider_back_to_ollama(self):
        c = Clementine(memory_dir=self.mem, provider="spacexai")
        self.assertEqual(c.provider, "spacexai")
        c.set_provider("ollama")
        self.assertEqual(c.provider, "ollama")
        self.assertEqual(c.model, "llama3.1:8b")
        self.assertFalse(c.personality.cloud_opt_in)

    def test_profile_persists_provider(self):
        c = Clementine(memory_dir=self.mem, provider="spacexai")
        c.set_provider("spacexai")
        c2 = Clementine(memory_dir=self.mem, provider="")
        self.assertEqual(c2.provider, "spacexai")
        self.assertEqual(c2.model, "grok-4.5")
        self.assertTrue(c2.personality.cloud_opt_in)

    def test_no_cloud_without_consent_on_reload(self):
        # Saved provider alone without opt-in is migrated to opt-in (legacy).
        # Fresh ollama profile must not jump to cloud just for a grok model tag
        # written without provider/opt-in.
        cfg = Path(self.mem) / "config.json"
        Path(self.mem).mkdir(parents=True, exist_ok=True)
        cfg.write_text(
            '{"name":"T","model":"grok-4.5","provider":"","cloud_opt_in":false}',
            encoding="utf-8",
        )
        c = Clementine(memory_dir=self.mem, provider="")
        self.assertEqual(c.provider, "ollama")

    def test_base_prompt_constants(self):
        self.assertIn("locally-run", BASE_PROMPT_LOCAL)
        self.assertIn("SpaceXAI", BASE_PROMPT_SPACEXAI)

    def test_local_fallback_without_key(self):
        # Force "no key" even if project .env has one (empty env wins over load).
        old = os.environ.get("XAI_API_KEY")
        os.environ["XAI_API_KEY"] = ""
        try:
            c = Clementine(memory_dir=self.mem, provider="spacexai")
            self.assertEqual(c.provider, "spacexai")
            self.assertTrue(c.personality.cloud_opt_in)
            self.assertTrue(c.spacexai_using_local_fallback())
            self.assertEqual(c.active_chat_provider(), "ollama")
            self.assertEqual(c.active_chat_model(), "llama3.1:8b")
            prompt = c.system_prompt()
            self.assertIn("local model", prompt.lower())
        finally:
            if old is None:
                os.environ.pop("XAI_API_KEY", None)
            else:
                os.environ["XAI_API_KEY"] = old


class ErrorAndEnvTests(unittest.TestCase):
    def test_missing_key_message(self):
        msg = user_facing_spacexai_error(
            RuntimeError("XAI_API_KEY is not set"), "grok-4.5"
        )
        self.assertIn("XAI_API_KEY", msg)
        self.assertIn("console.x.ai", msg)

    def test_load_dotenv_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            env_path = Path(d) / ".env"
            env_path.write_text("TEST_CRYSTAL_KEY=fromfile\n", encoding="utf-8")
            os.environ["TEST_CRYSTAL_KEY"] = "fromenv"
            try:
                load_dotenv(env_path)
                self.assertEqual(os.environ["TEST_CRYSTAL_KEY"], "fromenv")
            finally:
                os.environ.pop("TEST_CRYSTAL_KEY", None)

    def test_load_dotenv_sets_missing(self):
        with tempfile.TemporaryDirectory() as d:
            env_path = Path(d) / ".env"
            env_path.write_text("TEST_CRYSTAL_KEY2=fromfile\n", encoding="utf-8")
            os.environ.pop("TEST_CRYSTAL_KEY2", None)
            try:
                self.assertTrue(load_dotenv(env_path))
                self.assertEqual(os.environ.get("TEST_CRYSTAL_KEY2"), "fromfile")
            finally:
                os.environ.pop("TEST_CRYSTAL_KEY2", None)

    def test_xai_key_present_bool(self):
        # Just ensure it returns a bool without raising.
        self.assertIsInstance(xai_api_key_present(), bool)


class ProfileMetaTests(unittest.TestCase):
    def test_provider_in_meta(self):
        with tempfile.TemporaryDirectory() as d:
            # profile_dir is relative to cwd under clementine_profiles/
            # Write a fake profile folder next to the process cwd via profiles API.
            from crystalcore.profiles import PROFILES_DIR, profile_dir

            name = "_unittest_provider_meta"
            pdir = Path(profile_dir(name))
            pdir.mkdir(parents=True, exist_ok=True)
            (pdir / "config.json").write_text(
                '{"name":"T","model":"grok-4.5","provider":"spacexai"}',
                encoding="utf-8",
            )
            try:
                meta = profile_meta(name)
                self.assertEqual(meta.get("provider"), "spacexai")
                self.assertEqual(meta.get("model"), "grok-4.5")
            finally:
                import shutil
                if pdir.exists() and pdir.parent.resolve() == PROFILES_DIR.resolve():
                    shutil.rmtree(pdir)


class VersionTests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.13.3")


if __name__ == "__main__":
    unittest.main()
