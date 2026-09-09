# CrystalCore — the engineering side

The taxonomy — canonical names, the tree, the naming rule for anything new —
is in [`docs/vision/CrystalCore.md`](../vision/CrystalCore.md) and
[`ADR-0004`](../adr/ADR-0004.md). This page covers the three *built*
branches of that tree and how they divide the work.

## The Framework (`core/crystalcore/mind/`)

The sovereign-companion framework Clementine runs on:

- `companion.py` — the brain: memory layers, recall, chat, and the Covenant
  carried in the core prompt
- `memory.py` — the data model (Personality, Memory)
- `profiles.py` — multiple isolated companions, each with its own memory
- `sovereignty_scorer.py` — an unwired 0.1-alpha sketch of eight sovereignty
  metrics (explicitly not in use)

Local-first by construction: Ollama-backed, JSON storage on the user's own
disk, no account, no cloud requirement. The Covenant
([`mythos/COVENANT.md`](../../mythos/COVENANT.md)) is the product spec here,
not decoration — changes must preserve local-first operation, the absolute
pause, and full memory ownership.

## The Protocol pack (`src/crystal-core/`)

Four components, stdlib-only except where real cryptography is required:

- **Starline Weaver** (`bus/`) — the multi-AI bus. Every
  message must carry a science/story/vision label or it is not heard
  (Belt-Three law, enforced in `agents.py`); a red button halts everything.
  Spec: [`crystal-core/STARLINE-WEAVE-PROTOCOL.md`](crystal-core/STARLINE-WEAVE-PROTOCOL.md).
- **Pipeline** (`services/`) — Decode → Ingest → Twin: validate events,
  quarantine bad ones with reasons, aggregate into a SQLite twin.
- **Starline / Consent Transport** (`consent_transport/`; `starline/` is
  a deprecated backward-compatibility alias re-exporting the same code)
  — peer-to-peer memory exchange over a real Noise handshake; consent
  receipts, instant revocation. Spec:
  [`crystal-core/STARLINE.md`](crystal-core/STARLINE.md). The one component
  with a dependency (`cryptography`) — audited primitives are not something
  to hand-roll.
- **RDP** (`rdp/`) — tamper-evident hash-chained records plus an explainable
  decision kernel. It records what other components decide; it does not
  govern them ([`crystal-core/RDP-INTEGRATION.md`](crystal-core/RDP-INTEGRATION.md)).

## CrystalBridge (`src/crystalcore/`)

CrystalBridge: the MCP stdio server that lets a guest AI meet Clementine —
fail-closed. Every tool call passes five doors in order (revocation →
approval → provenance → permission → scope, `gate.py`) and lands in an
append-only audit log (`audit.py`). Scope is applied after `check()`
allows, inside `require_scope()`, for tools that touch memory. Guest
grants live in `src/profiles/<name>/bridge_config.json`. Guide:
[`docs/guides/MCP-Guest.md`](../guides/MCP-Guest.md). The check-order
that used to print here (approval → permission → scope → provenance) was
a leftover of the two-check era; the code never ran it that way.

## Why three, not one

They answer different trust questions. The framework trusts one human
completely and no one else. The pack mediates between many mutually
untrusting agents. The bridge lets outsiders in through a gate that fails
shut. Merging them would blur exactly the boundaries the project exists to
keep sharp.
