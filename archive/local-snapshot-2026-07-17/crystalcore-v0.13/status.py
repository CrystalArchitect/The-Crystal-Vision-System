"""
CrystalCore live status board — human-readable, local-only.

Reports what is actually running on this machine: package version,
Ollama reachability, companion memory counts, optional SpaceXAI key
presence, and honesty flags. Nothing is sent off-device.

    python -m crystalcore.status
    python -m crystalcore.status --memory-dir clementine_memory --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import requests

from .envutil import xai_api_key_present
from .ollama import CHAT_URL, DEFAULT_EMBED_MODEL
from .version import __version__


PROJECT_ROOT = "Australia · TerAustralis Incognita"
PROJECT_DEDICATION = "Bridge gift: Africa (operator dedication; not a claim of presence)"
NON_CLAIMS = [
    "No affiliation with xAI, Tesla, SpaceX, or any named company",
    "No mesh / CrystalMatrix networking implemented yet",
    "No physical 'field presence' — software + mythos only",
    "Companion warmth is architecture run faithfully, not proven AGI",
]


def _ollama_tags(timeout: float = 2.0) -> dict[str, Any]:
    """Probe local Ollama. Never raises out of this helper."""
    base = CHAT_URL.rsplit("/api/", 1)[0]
    tags_url = f"{base}/api/tags"
    try:
        r = requests.get(tags_url, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        return {"ok": True, "url": base, "models": models, "error": None}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "url": base, "models": [],
                "error": "Ollama not reachable (is it running?)"}
    except Exception as e:
        return {"ok": False, "url": base, "models": [], "error": str(e)}


def _memory_snapshot(memory_dir: Path) -> dict[str, Any]:
    config_path = memory_dir / "config.json"
    memory_path = memory_dir / "memory.json"
    snap = {
        "memory_dir": str(memory_dir.resolve()),
        "config_exists": config_path.exists(),
        "memory_exists": memory_path.exists(),
        "name": "",
        "human_name": "",
        "model": "",
        "provider": "",
        "counts": {"conversation": 0, "summaries": 0, "notes": 0,
                   "facts": 0, "reflections": 0},
    }
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            snap["name"] = cfg.get("name") or ""
            snap["human_name"] = cfg.get("human_name") or ""
            snap["model"] = cfg.get("model") or ""
            snap["provider"] = cfg.get("provider") or "ollama"
        except (OSError, json.JSONDecodeError):
            snap["config_error"] = "config.json unreadable"
    if memory_path.exists():
        try:
            mem = json.loads(memory_path.read_text(encoding="utf-8"))
            snap["counts"] = {
                "conversation": len(mem.get("conversation") or []),
                "summaries": len(mem.get("summaries") or []),
                "notes": len(mem.get("notes") or []),
                "facts": len(mem.get("facts") or {}),
                "reflections": len(mem.get("reflections") or []),
            }
        except (OSError, json.JSONDecodeError):
            snap["memory_error"] = "memory.json unreadable"
    return snap


def collect_status(memory_dir: str = "clementine_memory", *,
                   repo_root: Optional[Path] = None) -> dict[str, Any]:
    """Assemble a full status dict (JSON-serializable)."""
    root = repo_root or Path.cwd()
    mem_path = Path(memory_dir)
    if not mem_path.is_absolute():
        mem_path = root / mem_path
    ollama = _ollama_tags()
    memory = _memory_snapshot(mem_path)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crystalcore": {
            "version": __version__,
            "status": "BUILT",
            "default_embed_model": DEFAULT_EMBED_MODEL,
        },
        "project": {
            "name": "The Crystal Vision · TerAustralis Incognita",
            "root": PROJECT_ROOT,
            "dedication": PROJECT_DEDICATION,
            "steward": "CrystalArchitect · @M13CrystalAT",
        },
        "ollama": ollama,
        "spacexai": {
            "api_key_present": xai_api_key_present(),
            "note": "Opt-in chat only; memory stays local",
        },
        "companion_memory": memory,
        "entrypoints": {
            "status": "python -m crystalcore.status",
            "expose": "python -m crystalcore.expose",
            "terminal": "python clementine.py",
            "web": "python clementine_web.py  # http://127.0.0.1:5000",
        },
        "honesty": {
            "mesh_implemented": False,
            "crystalmatrix_implemented": False,
            "web_binds": "127.0.0.1 only",
            "data_leaves_device_by_default": False,
            "non_claims": NON_CLAIMS,
        },
        "built": [
            "Layered local memory (JSON on disk)",
            "Semantic recall via local embeddings",
            "Profiles / multi-companion isolation",
            "Terminal + local web UI",
            "Optional SpaceXAI chat (explicit opt-in)",
            "Full transparency dump (expose)",
            "This status board",
        ],
        "design_only": [
            "CrystalMatrix P2P mesh",
            "Planetary multi-node network",
            "Zero-knowledge identity layer",
        ],
    }


def format_human(data: dict[str, Any]) -> str:
    """Pretty terminal board."""
    cc = data["crystalcore"]
    ol = data["ollama"]
    mem = data["companion_memory"]
    counts = mem["counts"]
    sp = data["spacexai"]

    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║  CRYSTALCORE — LIVE STATUS (real machine, not mythos)        ║",
        "╚══════════════════════════════════════════════════════════════╝",
        "",
        f"  Version ........ {cc['version']}  [{cc['status']}]",
        f"  Generated ...... {data['generated_at']}",
        f"  Project ........ {data['project']['name']}",
        f"  Root ........... {data['project']['root']}",
        f"  Dedication ..... {data['project']['dedication']}",
        f"  Steward ........ {data['project']['steward']}",
        "",
        "── Local model runtime ─────────────────────────────────────────",
        f"  Ollama ......... {'ONLINE' if ol['ok'] else 'OFFLINE'}  ({ol['url']})",
    ]
    if ol["ok"]:
        models = ", ".join(ol["models"][:8]) if ol["models"] else "(no models listed)"
        if len(ol["models"]) > 8:
            models += f" … +{len(ol['models']) - 8} more"
        lines.append(f"  Models ......... {models}")
    else:
        lines.append(f"  Error .......... {ol.get('error')}")

    lines += [
        "",
        "── Companion memory (on disk) ──────────────────────────────────",
        f"  Dir ............ {mem['memory_dir']}",
        f"  Config ......... {'yes' if mem['config_exists'] else 'no'}",
        f"  Memory ......... {'yes' if mem['memory_exists'] else 'no'}",
        f"  Name ........... {mem['name'] or '—'}",
        f"  Human .......... {mem['human_name'] or '—'}",
        f"  Model/provider . {mem['model'] or '—'} / {mem['provider'] or '—'}",
        f"  Conversation ... {counts['conversation']} messages",
        f"  Notes/facts .... {counts['notes']} notes · {counts['facts']} facts",
        f"  Summaries ...... {counts['summaries']}",
        f"  Reflections .... {counts['reflections']}",
        "",
        "── Optional cloud chat ─────────────────────────────────────────",
        f"  XAI_API_KEY .... {'present' if sp['api_key_present'] else 'not set'}",
        f"  Note ........... {sp['note']}",
        "",
        "── Built (code exists) ─────────────────────────────────────────",
    ]
    for item in data["built"]:
        lines.append(f"  ✅ {item}")
    lines.append("")
    lines.append("── Design only (not implemented) ───────────────────────────────")
    for item in data["design_only"]:
        lines.append(f"  ⬜ {item}")
    lines.append("")
    lines.append("── Non-claims ──────────────────────────────────────────────────")
    for item in data["honesty"]["non_claims"]:
        lines.append(f"  · {item}")
    lines += [
        "",
        "── Run next ────────────────────────────────────────────────────",
        f"  {data['entrypoints']['terminal']}",
        f"  {data['entrypoints']['web']}",
        f"  {data['entrypoints']['expose']}",
        "",
        "  Non Solus — Not Alone",
        "",
    ]
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="CrystalCore live status board (local, honest).")
    p.add_argument("--memory-dir", default="clementine_memory",
                   help="Companion memory folder (default: clementine_memory)")
    p.add_argument("--json", action="store_true",
                   help="Emit machine-readable JSON instead of the board")
    p.add_argument("-o", "--output", default="",
                   help="Write output to a file")
    p.add_argument("--repo-root", default="",
                   help="Repo root for resolving relative memory-dir (default: cwd)")
    args = p.parse_args(argv)

    root = Path(args.repo_root) if args.repo_root else Path.cwd()
    data = collect_status(args.memory_dir, repo_root=root)
    text = (json.dumps(data, indent=2, ensure_ascii=False)
            if args.json else format_human(data))
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
