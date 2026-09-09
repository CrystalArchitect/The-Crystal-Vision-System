# Architecture overview

What actually runs, how the pieces relate, and where the honest edges are.
Directory-level layout is in [`SystemMap.md`](SystemMap.md); per-component
status and test commands are in [`Modules.md`](Modules.md).

## The built system

Four components run and are tested today:

| Component | Role | Lives at |
|---|---|---|
| **Clementine** | Local-first sovereign companion — terminal, Flask API, Svelte webapp, layered memory, Ollama-backed | `vision/apps/clementine/` |
| **Starline Weaver** | Multi-AI message bus; every message must carry a Belt-Three truth label or it is not heard; red-button halt; matrix mode | `src/crystal-core/bus/` |
| **Starline** | Peer-to-peer consent-gated memory exchange over a real Noise Protocol handshake | `src/crystal-core/consent_transport/` |
| **CrystalBridge** | Fail-closed MCP consent gate for guest AIs — five doors in order: revocation → approval → provenance → permission → scope; append-only audit | `src/crystalcore/` |

Supporting pieces: the **Decode → Ingest → Twin pipeline**
(`src/crystal-core/services/` — validate events, quarantine bad ones, store
in a SQLite twin), the **RDP record kernel** (`src/crystal-core/rdp/` —
tamper-evident hash chain plus an explainable decision engine), the
**SvelteKit site** (`src/site/`), an **in-process mesh stub**
(`src/node/mesh/`), and a **TypeScript SDK scaffold** (`src/sdk/typescript/`).

## How they relate

```
   guest AI ──MCP──▶ CrystalBridge ──gated──▶ Clementine's memory
                        (consent law)             │
                                                  │ one human, one companion
   many AIs ◀──bus──▶ Starline Weaver             │
              (truth labels enforced)             ▼
   peer A ◀═══ Starline (Noise handshake, consent receipts) ═══▶ peer B
                        │
                        ▼ witnessed, never governed
                  RDP record chain
```

One law repeats at every boundary: **nothing moves without explicit,
revocable consent, and refusal is the default.** The Covenant
([`mythos/COVENANT.md`](../../mythos/COVENANT.md)) states it for
conversation; `consent_transport/consent.py` applies it to data;
`src/crystalcore/gate.py` applies it to guest access. RDP *records* what the
others decide — it never decides for them
([`crystal-core/RDP-INTEGRATION.md`](crystal-core/RDP-INTEGRATION.md)).

Control of the *constellation* (nineteen repositories, identity loop,
incoming X/foreign variety) is mapped in
[`CYBERNETICS-VSM.md`](CYBERNETICS-VSM.md) — VSM, second-order identity,
information diet. Model, not a new OS mode.

## The dreamed edges

Marked as Vision, per the
[Incognita Rule](../governance/The-Incognita-Rule.md):

- **CrystalCore.Lattice** — the multi-AI substrate (weave map, memory deltas,
  activation gates) was designed and never built. See
  [`Lattice.md`](Lattice.md).
- **CrystalVision** — the sensing/dreaming/directing interface exists as demo
  shells on simulated data. See [`CrystalVision.md`](CrystalVision.md).
- **The mainnet mesh** — `src/node/mesh/` is an in-process stub shaped like a
  future libp2p host, deliberately on hold.
- **The full-stack blueprint** —
  [`crystal-core/BLUEPRINT-v0.3.md`](crystal-core/BLUEPRINT-v0.3.md) is a
  live draft; its grounded counterpart is
  [`crystal-core/ARCHITECTURE.md`](crystal-core/ARCHITECTURE.md).

## Historical specs

Older architecture snapshots are kept, labeled by their version:
[`Full-Stack-v0.5.md`](Full-Stack-v0.5.md) (demo surfaces + mesh stub + TS
client). They describe the state of their moment, not the present.
