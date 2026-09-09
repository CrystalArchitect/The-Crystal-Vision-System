"""
Full local transparency dump for CrystalCore.

Nothing is hidden from the human who owns the device. This module serializes
framework state, companion memory, node stubs, and API surface into plain
JSON-friendly dicts. It does not send data off-machine.

    python -m crystalcore.expose
    python -m crystalcore.expose --memory-dir clementine_memory
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any, Optional

from .companion import (
    BASE_PROMPT,
    BASE_PROMPT_LOCAL,
    BASE_PROMPT_SPACEXAI,
    Clementine,
    MAX_MEMORIES,
)
from .memory import Memory, Personality
from .node import IncognitaNode, local_node
from .ollama import CHAT_URL, DEFAULT_EMBED_MODEL, EMBED_URL
from .profiles import PROFILES_DIR, list_profiles, profile_meta
from .spacexai import BASE_URL as SPACEXAI_BASE_URL, DEFAULT_MODEL as SPACEXAI_DEFAULT_MODEL
from .version import __version__


def _strip_embeddings(obj: Any) -> Any:
    """Drop huge float vectors so dumps stay human-readable."""
    if isinstance(obj, dict):
        return {
            k: _strip_embeddings(v)
            for k, v in obj.items()
            if k != "embedding"
        }
    if isinstance(obj, list):
        return [_strip_embeddings(x) for x in obj]
    return obj


def _dc(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return _strip_embeddings(asdict(obj))
    return obj


def package_surface() -> dict[str, Any]:
    """Everything the package claims to export / contain."""
    import crystalcore as pkg

    return {
        "version": __version__,
        "package": "crystalcore",
        "modules": [
            "companion", "memory", "profiles", "ollama", "spacexai",
            "envutil", "node", "expose", "status",
        ],
        "exports": sorted(getattr(pkg, "__all__", [])),
        "constants": {
            "MAX_MEMORIES": MAX_MEMORIES,
            "DEFAULT_EMBED_MODEL": DEFAULT_EMBED_MODEL,
            "CHAT_URL": CHAT_URL,
            "EMBED_URL": EMBED_URL,
            "SPACEXAI_BASE_URL": SPACEXAI_BASE_URL,
            "SPACEXAI_DEFAULT_MODEL": SPACEXAI_DEFAULT_MODEL,
            "PROFILES_DIR": str(PROFILES_DIR),
        },
        "dataclass_fields": {
            "Personality": [f.name for f in fields(Personality)],
            "Memory": [f.name for f in fields(Memory)],
        },
        "honesty": {
            "mesh_implemented": False,
            "crystalmatrix_implemented": False,
            "data_leaves_device_by_default": False,
            "web_binds": "127.0.0.1 only",
            "cloud_ai_in_this_package": True,
            "cloud_ai_note": (
                "SpaceXAI (xAI) is optional opt-in for chat only. "
                "Default remains local Ollama. Memory/embeddings stay local. "
                "Requires XAI_API_KEY when provider=spacexai."
            ),
        },
    }


def web_routes_catalog() -> list[dict[str, str]]:
    """Documented HTTP surface of clementine_web (localhost)."""
    return [
        {"method": "GET", "path": "/", "what": "Chat UI HTML"},
        {"method": "POST", "path": "/api/chat", "what": "Non-streaming chat JSON"},
        {"method": "POST", "path": "/api/chat/stream", "what": "Streaming chat text"},
        {"method": "GET", "path": "/api/memories", "what": "Facts, notes, reflections"},
        {"method": "POST", "path": "/api/teach", "what": "Remember fact or note"},
        {"method": "POST", "path": "/api/forget", "what": "Forget by handle"},
        {"method": "POST", "path": "/api/reflect", "what": "Run reflection"},
        {"method": "GET", "path": "/api/profile", "what": "List/switch profiles"},
        {"method": "POST", "path": "/api/profile", "what": "Switch profile"},
        {"method": "POST", "path": "/api/profile/meta", "what": "Update profile meta"},
        {"method": "POST", "path": "/api/profile/delete", "what": "Delete profile"},
        {"method": "GET", "path": "/api/expose", "what": "Full transparency dump"},
        {"method": "GET", "path": "/api/conversation", "what": "Full conversation log"},
        {"method": "GET", "path": "/api/system", "what": "Alias of /api/expose"},
        {"method": "GET", "path": "/api/prompt", "what": "Live system prompt"},
    ]


def cli_commands_catalog() -> list[str]:
    return [
        "/help", "/name", "/iam", "/remember", "/fact", "/notes", "/forget",
        "/editnote", "/summary", "/reflect", "/style", "/temp", "/model",
        "/exit",
    ]


def companion_dump(c: Clementine, *, include_prompt: bool = True) -> dict[str, Any]:
    """Full companion state: personality, memory (no embeddings), paths."""
    mem = _dc(c.memory)
    out: dict[str, Any] = {
        "model": c.model,
        "provider": getattr(c, "provider", "ollama"),
        "cloud_opt_in": bool(getattr(c.personality, "cloud_opt_in", False)),
        "cloud_opt_in_at": getattr(c.personality, "cloud_opt_in_at", "") or "",
        "embed_model": c.embed_model,
        "memory_dir": str(Path(c.memory_dir).resolve()),
        "max_recent_turns": c.max_recent_turns,
        "personality": _dc(c.personality),
        "memory": mem,
        "counts": {
            "conversation_messages": len(c.memory.conversation),
            "summaries": len(c.memory.summaries),
            "notes": len(c.memory.notes),
            "facts": len(c.memory.facts),
            "reflections": len(c.memory.reflections),
        },
        "files": {
            "config": str((Path(c.memory_dir) / "config.json").resolve()),
            "memory": str((Path(c.memory_dir) / "memory.json").resolve()),
            "config_exists": (Path(c.memory_dir) / "config.json").exists(),
            "memory_exists": (Path(c.memory_dir) / "memory.json").exists(),
        },
    }
    if include_prompt:
        out["system_prompt_live"] = c.system_prompt("")
        out["base_prompt"] = (
            BASE_PROMPT_SPACEXAI
            if getattr(c, "provider", "ollama") == "spacexai"
            else BASE_PROMPT_LOCAL
        )
    return out


def node_dump(node: Optional[IncognitaNode] = None) -> dict[str, Any]:
    n = node or local_node()
    return {
        "id": n.id,
        "connected_nodes": len(n.connected_nodes),
        "mesh_online": False,
        "red_dust_buffer_len": len(n.red_dust_buffer),
        "starline_ports": [
            {"name": p.name, "target": p.target, "active": p.active}
            for p in n.starline_ports
        ],
        "resonance_field": _dc(n.resonance_field),
        "ethics": {
            "version": n.ethics_signature.version,
            "lock": n.ethics_signature.lock,
            "intent": _dc(n.ethics_signature.intent),
            "timestamp": n.ethics_signature.timestamp,
        },
        "has_crystal_core": n.crystal_core is not None,
    }


def profiles_dump() -> dict[str, Any]:
    names = list_profiles()
    return {
        "profiles_dir": str(Path(PROFILES_DIR).resolve()),
        "names": names,
        "meta": [profile_meta(n) for n in names],
    }


def full_expose(
    companion: Optional[Clementine] = None,
    memory_dir: str = "clementine_memory",
    model: str = "llama3.1:8b",
    *,
    include_prompt: bool = True,
) -> dict[str, Any]:
    """Everything: package + companion + node + profiles + catalogs."""
    c = companion or Clementine(model=model, memory_dir=memory_dir)
    node = local_node(c)
    return {
        "expose_version": 1,
        "package": package_surface(),
        "companion": companion_dump(c, include_prompt=include_prompt),
        "node": node_dump(node),
        "profiles": profiles_dump(),
        "cli_commands": cli_commands_catalog(),
        "web_routes": web_routes_catalog(),
        "entrypoints": {
            "terminal": "python clementine.py",
            "web": "python clementine_web.py  # http://127.0.0.1:5000",
            "expose_cli": "python -m crystalcore.expose",
            "status_cli": "python -m crystalcore.status",
            "package_cli": "python -m crystalcore  # status by default",
            "start_bat": ["Start-Lumina.bat", "Start-Lumina-Web.bat"],
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Dump full CrystalCore state (local JSON).")
    p.add_argument("--memory-dir", default="clementine_memory")
    p.add_argument("--model", default="llama3.1:8b")
    p.add_argument("--no-prompt", action="store_true",
                   help="Omit live system prompt (shorter dump).")
    p.add_argument("-o", "--output", default="",
                   help="Write JSON to file instead of stdout.")
    args = p.parse_args(argv)

    data = full_expose(
        memory_dir=args.memory_dir,
        model=args.model,
        include_prompt=not args.no_prompt,
    )
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
