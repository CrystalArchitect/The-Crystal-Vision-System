#!/usr/bin/env python3
# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Local diagnostic for Clementine / Ollama.

Surveys what is actually true on this machine. No invented VRAM, token, or
throughput numbers — only what Ollama and (optionally) Clementine answer.

Usage:
  python3 diagnose_clementine_ollama.py
  python3 diagnose_clementine_ollama.py --probe
  python3 diagnose_clementine_ollama.py --clementine-root /path/to/Clementine-ai-companion
  OLLAMA_HOST=http://127.0.0.1:11434 python3 diagnose_clementine_ollama.py

Exit codes:
  0  Ollama reachable and default chat model present
  1  Ollama unreachable
  2  Ollama up but default chat model missing, or Clementine tree broken
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
DEFAULT_CHAT_MODEL = os.environ.get("CLEM_MODEL", "llama3.1:8b")
DEFAULT_EMBED_MODEL = "nomic-embed-text"
RECOMMENDED_CHAT = ("llama3.1:8b", "hermes3:8b", "llama3.2:3b")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"}
CLEMENTINE_API = os.environ.get("CLEM_API", "http://127.0.0.1:5000").rstrip("/")


def destination_of(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return "local" if host in LOCAL_HOSTS else (host or "unknown")


def http_json(url: str, *, timeout: float = 5.0, method: str = "GET",
              body: dict | None = None) -> tuple[int | None, Any, float, str]:
    """Return (status, parsed_json_or_None, elapsed_ms, error_or_empty)."""
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            elapsed = (time.perf_counter() - t0) * 1000
            try:
                return resp.status, json.loads(raw.decode("utf-8")), elapsed, ""
            except json.JSONDecodeError:
                return resp.status, None, elapsed, "response was not JSON"
    except urllib.error.HTTPError as e:
        elapsed = (time.perf_counter() - t0) * 1000
        return e.code, None, elapsed, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        elapsed = (time.perf_counter() - t0) * 1000
        return None, None, elapsed, str(e.reason if hasattr(e, "reason") else e)
    except TimeoutError:
        elapsed = (time.perf_counter() - t0) * 1000
        return None, None, elapsed, "timeout"
    except Exception as e:  # noqa: BLE001 — diagnostic must never crash mid-report
        elapsed = (time.perf_counter() - t0) * 1000
        return None, None, elapsed, f"{type(e).__name__}: {e}"


def line(ok: bool | None, label: str, detail: str = "") -> str:
    mark = {True: "PASS", False: "FAIL", None: "SKIP"}[ok]
    suffix = f" — {detail}" if detail else ""
    return f"[{mark}] {label}{suffix}"


def check_cli() -> tuple[bool, str]:
    path = shutil.which("ollama")
    if not path:
        return False, "ollama binary not on PATH"
    return True, path


def check_port(host_url: str) -> tuple[bool, str]:
    parsed = urlparse(host_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if host_url.rstrip("/").endswith(":11434") or "11434" in host_url:
        port = parsed.port or 11434
    try:
        with socket.create_connection((host, port), timeout=2.0):
            return True, f"{host}:{port} accepts TCP"
    except OSError as e:
        return False, f"{host}:{port} — {e}"


def model_names(tags_body: Any) -> list[str]:
    if not isinstance(tags_body, dict):
        return []
    out = []
    for m in tags_body.get("models") or []:
        name = m.get("name") or m.get("model")
        if name:
            out.append(name)
    return sorted(out)


def model_present(names: list[str], wanted: str) -> bool:
    """Exact tag or same family:tag prefix match Ollama often reports."""
    if wanted in names:
        return True
    # Ollama may list "llama3.1:8b" while wanted is identical; also accept
    # when the listed name starts with wanted + "-" (quant variants).
    for n in names:
        if n == wanted or n.startswith(wanted + "-") or n.startswith(wanted + ":"):
            return True
        # wanted "llama3.1:8b" vs listed "llama3.1:8b-instruct-q5_K_M"
        if ":" in wanted:
            fam, tag = wanted.split(":", 1)
            if n.startswith(fam + ":") and tag in n:
                return True
    return False


def check_clementine_tree(root: Path) -> list[tuple[bool | None, str, str]]:
    rows: list[tuple[bool | None, str, str]] = []
    if not root.exists():
        rows.append((False, "Clementine root", f"missing: {root}"))
        return rows
    rows.append((True, "Clementine root", str(root.resolve())))

    server = root / "clementine" / "server.py"
    if not server.exists():
        # allow pointing at the clementine/ package itself
        alt = root / "server.py"
        server = alt if alt.exists() else server
    if server.exists():
        text = server.read_text(encoding="utf-8", errors="replace").strip()
        if text in {"RESTORE_ME", "PLACEHOLDER"} or len(text) < 40:
            rows.append((
                False,
                "clementine/server.py",
                f"stub only ({len(text)} bytes: {text[:32]!r}) — "
                "master is unrunnable until restored",
            ))
        else:
            rows.append((True, "clementine/server.py", f"{len(text)} bytes"))
    else:
        rows.append((False, "clementine/server.py", "not found"))

    companion = root / "clementine" / "crystalcore" / "companion.py"
    if not companion.exists():
        companion = root / "crystalcore" / "companion.py"
    rows.append((companion.exists(), "crystalcore/companion.py",
                 str(companion) if companion.exists() else "not found"))

    for name in ("verify_consent.py", "verify_audit.py"):
        p = root / "clementine" / name
        if not p.exists():
            p = root / name
        rows.append((p.exists(), name, "present" if p.exists() else "missing"))

    return rows


def check_memory_dir(path: Path) -> list[tuple[bool | None, str, str]]:
    rows: list[tuple[bool | None, str, str]] = []
    if not path.exists():
        rows.append((None, "memory dir", f"not present yet ({path})"))
        return rows
    rows.append((True, "memory dir", str(path.resolve())))
    audit = path / "audit.jsonl"
    if audit.exists():
        n = sum(1 for _ in audit.open(encoding="utf-8", errors="replace"))
        rows.append((True, "audit.jsonl", f"{n} lines"))
    else:
        rows.append((None, "audit.jsonl", "none yet"))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default=DEFAULT_HOST,
                    help=f"Ollama base URL (default {DEFAULT_HOST})")
    ap.add_argument("--model", default=DEFAULT_CHAT_MODEL,
                    help=f"Expected chat model (default {DEFAULT_CHAT_MODEL})")
    ap.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL,
                    help=f"Expected embed model (default {DEFAULT_EMBED_MODEL})")
    ap.add_argument("--probe", action="store_true",
                    help="Send a tiny generate request and report measured latency")
    ap.add_argument("--clementine-root", type=Path, default=None,
                    help="Path to Clementine-ai-companion (or clementine/ package)")
    ap.add_argument("--memory-dir", type=Path, default=None,
                    help="Path to clementine_memory/ if known")
    ap.add_argument("--clementine-api", default=CLEMENTINE_API,
                    help=f"Clementine HTTP API (default {CLEMENTINE_API})")
    ap.add_argument("--json", action="store_true",
                    help="Emit machine-readable JSON as well as the human report")
    args = ap.parse_args()

    host = args.host.rstrip("/")
    report: dict[str, Any] = {
        "when": datetime.now(timezone.utc).isoformat(),
        "ollama_host": host,
        "destination": destination_of(host),
        "expected_chat_model": args.model,
        "expected_embed_model": args.embed_model,
    }
    print(f"Clementine / Ollama diagnostic")
    print(f"when (UTC): {report['when']}")
    print(f"OLLAMA_HOST: {host}  ({report['destination']})")
    print()

    exit_code = 0
    findings: list[str] = []

    ok_cli, cli_detail = check_cli()
    findings.append(line(ok_cli, "ollama CLI", cli_detail))
    report["ollama_cli"] = {"ok": ok_cli, "detail": cli_detail}

    ok_tcp, tcp_detail = check_port(host)
    findings.append(line(ok_tcp, "Ollama TCP", tcp_detail))
    report["ollama_tcp"] = {"ok": ok_tcp, "detail": tcp_detail}

    status, tags, ms, err = http_json(f"{host}/api/tags", timeout=5.0)
    ollama_up = status == 200 and isinstance(tags, dict)
    findings.append(line(
        ollama_up,
        "GET /api/tags",
        f"{ms:.0f} ms" if ollama_up else err or f"status={status}",
    ))
    names = model_names(tags) if ollama_up else []
    report["ollama"] = {
        "ok": ollama_up,
        "latency_ms": round(ms, 1),
        "error": err,
        "models": names,
    }
    if not ollama_up:
        exit_code = 1
        findings.append(line(False, "chat model", f"{args.model} — skipped (Ollama down)"))
        findings.append(line(False, "embed model", f"{args.embed_model} — skipped (Ollama down)"))
    else:
        if names:
            findings.append(line(True, "models pulled", ", ".join(names)))
        else:
            findings.append(line(False, "models pulled", "none — run e.g. ollama pull llama3.1:8b"))

        chat_ok = model_present(names, args.model)
        findings.append(line(
            chat_ok,
            "default chat model",
            args.model if chat_ok else f"{args.model} missing — try: ollama pull {args.model}",
        ))
        report["chat_model_present"] = chat_ok
        if not chat_ok:
            exit_code = 2
            # note which recommended ones are present
            present_rec = [m for m in RECOMMENDED_CHAT if model_present(names, m)]
            if present_rec:
                findings.append(line(True, "other recommended chat", ", ".join(present_rec)))

        embed_ok = model_present(names, args.embed_model)
        findings.append(line(
            embed_ok if names else False,
            "embed model (semantic recall)",
            args.embed_model if embed_ok
            else f"{args.embed_model} missing — optional: ollama pull {args.embed_model}",
        ))
        report["embed_model_present"] = embed_ok
        # missing embed is soft — recall degrades; do not fail hard

        ver_status, ver_body, ver_ms, ver_err = http_json(f"{host}/api/version", timeout=3.0)
        if ver_status == 200 and isinstance(ver_body, dict):
            ver = ver_body.get("version") or ver_body
            findings.append(line(True, "Ollama version", f"{ver} ({ver_ms:.0f} ms)"))
            report["ollama_version"] = ver
        else:
            findings.append(line(None, "Ollama version", ver_err or "endpoint absent"))

        if args.probe:
            if not chat_ok:
                findings.append(line(None, "generate probe", "skipped — chat model not pulled"))
            else:
                # Prefer /api/generate — smaller surface than chat.
                p_status, p_body, p_ms, p_err = http_json(
                    f"{host}/api/generate",
                    timeout=120.0,
                    method="POST",
                    body={
                        "model": args.model,
                        "prompt": "Reply with exactly one word: ok",
                        "stream": False,
                        "options": {"num_predict": 8},
                    },
                )
                if p_status == 200 and isinstance(p_body, dict):
                    reply = (p_body.get("response") or "").strip().replace("\n", " ")[:80]
                    total = p_body.get("total_duration")
                    # Ollama reports nanoseconds when present — convert if so.
                    measured = None
                    if isinstance(total, (int, float)) and total > 0:
                        measured = total / 1e6 if total > 1e7 else total
                    detail = f"{p_ms:.0f} ms wall"
                    if measured is not None:
                        detail += f", ollama total_duration≈{measured:.0f} ms"
                    if reply:
                        detail += f', reply={reply!r}'
                    findings.append(line(True, "generate probe", detail))
                    report["probe"] = {
                        "ok": True,
                        "wall_ms": round(p_ms, 1),
                        "reply": reply,
                        "ollama_total_ms": round(measured, 1) if measured else None,
                    }
                else:
                    findings.append(line(False, "generate probe", p_err or f"status={p_status}"))
                    report["probe"] = {"ok": False, "error": p_err}
                    if exit_code == 0:
                        exit_code = 2

    # Clementine HTTP face (only if someone is serving it)
    print()
    c_status, c_body, c_ms, c_err = http_json(
        f"{args.clementine_api}/api/health", timeout=3.0
    )
    if c_status == 200 and isinstance(c_body, dict):
        findings.append(line(True, "Clementine GET /api/health", f"{c_ms:.0f} ms"))
        for key in ("ollama", "model", "model_present", "destination",
                    "ollama_host", "embeddings", "audit_entries"):
            if key in c_body:
                findings.append(line(None, f"  health.{key}", repr(c_body[key])))
        report["clementine_health"] = c_body
    else:
        findings.append(line(
            None,
            "Clementine GET /api/health",
            f"not serving at {args.clementine_api} ({c_err or c_status})",
        ))
        report["clementine_health"] = None

    # Tree checks
    root = args.clementine_root
    if root is None:
        # auto-detect common layouts next to this script / cwd
        here = Path(__file__).resolve().parent
        candidates = [
            here / "Clementine-ai-companion",
            here.parent / "clementine-diag-src",
            Path.cwd() / "Clementine-ai-companion",
            Path.cwd(),
        ]
        for c in candidates:
            if (c / "clementine" / "crystalcore" / "companion.py").exists() or \
               (c / "crystalcore" / "companion.py").exists():
                root = c
                break

    if root is not None:
        print()
        tree_rows = check_clementine_tree(root)
        report["clementine_tree"] = []
        for ok, label, detail in tree_rows:
            findings.append(line(ok, label, detail))
            report["clementine_tree"].append(
                {"ok": ok, "label": label, "detail": detail}
            )
            if ok is False and exit_code == 0:
                exit_code = 2
            if ok is False and "server.py" in label and exit_code == 1:
                # keep ollama-down as primary; still note tree
                pass
    else:
        findings.append(line(None, "Clementine tree",
                             "pass --clementine-root to check server.py / companion"))

    mem = args.memory_dir
    if mem is None and root is not None:
        for candidate in (
            root / "clementine" / "clementine_memory",
            root / "clementine_memory",
            Path.cwd() / "clementine_memory",
        ):
            if candidate.exists():
                mem = candidate
                break
    if mem is not None:
        for ok, label, detail in check_memory_dir(mem):
            findings.append(line(ok, label, detail))

    print()
    for f in findings:
        print(f)

    print()
    if exit_code == 0:
        print("RESULT: ready — Ollama up, expected chat model present.")
    elif exit_code == 1:
        print("RESULT: Ollama unreachable. Install/start it, then re-run.")
        print("  https://ollama.com  →  ollama serve  →  ollama pull", args.model)
    else:
        print("RESULT: partial — see FAIL lines above.")

    if args.json:
        print()
        print(json.dumps(report, indent=2, default=str))

    # Always write a sidecar report next to the script for later comparison.
    out = Path(__file__).resolve().parent / "last-diagnostic.json"
    out.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
