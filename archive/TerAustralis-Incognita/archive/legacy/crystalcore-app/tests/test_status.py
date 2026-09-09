"""Offline tests for crystalcore.status."""
from __future__ import annotations

import json
from pathlib import Path

from crystalcore.status import collect_status, format_human, main


def test_collect_status_shape(tmp_path: Path):
    mem = tmp_path / "mem"
    mem.mkdir()
    (mem / "config.json").write_text(
        json.dumps({"name": "Clementine", "human_name": "Crystal", "model": "x", "provider": "ollama"}),
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
    data = collect_status(str(mem), repo_root=tmp_path)
    assert data["crystalcore"]["version"]
    assert data["companion_memory"]["name"] == "Clementine"
    assert data["companion_memory"]["counts"]["conversation"] == 1
    assert data["companion_memory"]["counts"]["facts"] == 1
    assert data["honesty"]["mesh_implemented"] is False
    assert "Non Solus" in format_human(data) or "CRYSTALCORE" in format_human(data)


def test_status_cli_json(tmp_path: Path, capsys):
    mem = tmp_path / "empty_mem"
    mem.mkdir()
    rc = main(["--memory-dir", str(mem), "--json", "--repo-root", str(tmp_path)])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["crystalcore"]["status"] == "BUILT"
