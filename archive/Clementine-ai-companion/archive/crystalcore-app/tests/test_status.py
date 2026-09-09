"""Offline tests for crystalcore.status.

These were written pytest-style, using the `tmp_path` and `capsys` fixtures.
pytest is not a dependency of this project — `requirements.txt` is `requests`
and `flask` — so `unittest`, which is what the suite actually runs under,
imported this module, found no TestCase, and reported "Ran 0 tests ... OK".
Three tests contributed nothing while looking like coverage. Ported to
unittest so they run.
"""
from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from crystalcore.status import collect_status, format_human, main


class StatusTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_collect_status_shape(self):
        mem = self.tmp_path / "mem"
        mem.mkdir()
        (mem / "config.json").write_text(
            json.dumps({"name": "Lumina", "human_name": "Crystal", "model": "x", "provider": "ollama"}),
            encoding="utf-8",
        )
        (mem / "memory.json").write_text(
            json.dumps({
                "conversation": [{"role": "user", "content": "hi"}],
                "summaries": [],
                "notes": [{"text": "n"}],
                "facts": {"home": {"value": "Sydney"}},
                "reflections": [],
            }),
            encoding="utf-8",
        )
        data = collect_status(str(mem), repo_root=self.tmp_path)
        self.assertTrue(data["crystalcore"]["version"])
        self.assertEqual(data["companion_memory"]["name"], "Lumina")
        self.assertEqual(data["companion_memory"]["counts"]["conversation"], 1)
        self.assertEqual(data["companion_memory"]["counts"]["facts"], 1)
        self.assertIs(data["honesty"]["mesh_implemented"], False)
        human = format_human(data)
        self.assertTrue("Non Solus" in human or "CRYSTALCORE" in human)

    def test_status_cli_json(self):
        mem = self.tmp_path / "empty_mem"
        mem.mkdir()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--memory-dir", str(mem), "--json", "--repo-root", str(self.tmp_path)])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["crystalcore"]["status"], "BUILT")


if __name__ == "__main__":
    unittest.main()
