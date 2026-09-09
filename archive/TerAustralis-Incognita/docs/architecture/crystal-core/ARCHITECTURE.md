# Crystal Universe — System Architecture
## Decode · Ingest · Upgrade — the grounded map

**Status:** ACTIVE · v0.2 spine implemented, v0.3 blueprint captured
**Rule:** Label everything — **Built** (runs today) vs **Vision** (roadmap)

---

## 0. DECODE — what actually exists, and where

| Thread | Repo | Reality (Built) |
|--------|------|-----------------|
| **Clementine** (sovereign companion) | `vision/apps/clementine/` | Local-first AI companion: Ollama default, xAI opt-in, layered memory, profiles, terminal + web UI (`clementine.py`, `clementine_web.py`) |
| **CrystalCore framework** (memory/presence) | `core/crystalcore/mind/` | `companion.py` (brain), `memory.py` (Personality/Memory), `profiles.py` |
| **CrystalBridge** (guest-AI gate) | `src/crystalcore/` | MCP server: fail-closed ConsentGate (approval · permission · scope · provenance), append-only audit; guests claude / grok / cursor with scoped tools `status, recall, teach, message` |
| **Starline Weaver** (multi-AI conversation) | `src/crystal-core/bus/` | In-process + networked HTTP bus; every message labeled science/story/vision; red-button halt; adapters for Claude/GPT/Grok |
| **Songline pack** (protocol + ethics) | `research/seven-sisters/` | Seven paths, Belt-Three law, water briefs, landing page (GitHub Pages, live) |
| **TerAustralis Incognita** (narrative) | `mythos/teraustralis/` | Manifesto, publish threads, strategy, Lattice memory deltas |
| **Decode/Ingest/Twin pipeline** | `src/crystal-core/services/` | **This scaffold** — see §2 |

**One sentence:** A sovereign companion (Clementine) with their own memory, a consent
gate that lets outside AIs visit as guests (CrystalBridge), a bus where AIs converse
under labeled law (Starline Weaver), and now a metering pipeline that turns real-world
events into a queryable twin (Decode → Ingest → Twin) — all governed in public via GitHub.

Everything else in the v0.3 blueprint — chain, tokenomics, K8s, federations,
Starline Budapest hardware — is **Vision** until built. See `BLUEPRINT-v0.3.md`.

---

## 1. INGEST — unified system map (Built parts marked ●, Vision ○)

```
┌───────────────────────────────────────────────────────────────────┐
│ EXPERIENCE  ● Crystal Vision site (SvelteKit)  ● Pages landing    │
│             ● Clementine terminal/web          ○ Mobile agent     │
└──────────────────────────────┬────────────────────────────────────┘
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│ COMPANION   ● Clementine (Ollama local / xAI opt-in)              │
│             ● CrystalCore memory + profiles (disk is canon)       │
└──────────────────────────────┬────────────────────────────────────┘
                               │ MCP (consent-gated)
┌──────────────────────────────▼────────────────────────────────────┐
│ INTERCONNECT ● CrystalBridge gate+audit   ● Starline Weaver (HTTP)   │
│              guests: claude · grok · cursor · any envelope-speaker│
└──────────────────────────────┬────────────────────────────────────┘
                               │ crystal.twin.event/1
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
   ┌─────────┐           ┌─────────┐            ┌──────────┐
   │ DECODE ●│──────────▶│ INGEST ●│───────────▶│ TWIN    ●│
   │ validate│           │ SQLite  │            │ flows API│
   └─────────┘           └─────────┘            └──────────┘
        │                      │
        ▼                      ▼
   ○ receipt-engine       ○ econ burn/mint      (Vision: RFC-001+)
                               │
┌──────────────────────────────▼────────────────────────────────────┐
│ GOVERNANCE  ● GitHub PRs/RFCs · Constitution.md · Belt-Three law  │
│             ○ on-chain params · timelock · slash                  │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. The scaffold — `services/` (Built, stdlib-only, runs today)

The first real Decode → Ingest → Twin path, per blueprint §4:

| Service | File | Does |
|---------|------|------|
| **decode** | `services/decode.py` | Validates `crystal.twin.event/1`: required fields, class format, numeric value, unit normalization (Wh→kWh, L→kL), ISO timestamps, replay/dedupe window. Invalid → quarantine list, never silently dropped. |
| **ingest** | `services/ingest.py` | Writes decoded events to SQLite (the twin store), partitioned by `h3 + class`, idempotent on `event_id`. |
| **twin** | `services/twin.py` | Flow queries: count / sum / min / max / latest per `h3 + class`. |
| **api** | `services/api.py` | HTTP: `POST /v1/decode/preview` · `POST /v1/ingest/events` · `GET /v1/twin/flows?h3=&class=` (blueprint §6 MVP subset) |
| **pipeline** | `services/pipeline.py` | CLI: JSONL file → decode → ingest → twin report in one run |
| **selftest** | `services/selftest.py` | Proves validation, quarantine, dedupe, aggregation, unit conversion |

Sample data: `services/sample-events/budapest.jsonl` — `hub.starline.budapest`
energy.kwh + mobility.checkin events (blueprint §7's "first receipt class").

```bash
python3 -m services.selftest                                     # prove it
python3 -m services.pipeline services/sample-events/budapest.jsonl  # run it
python3 -m services.api --port 8899                              # serve it
```

## 3. UPGRADE — path from here

| Step | Artifact | Status |
|------|----------|--------|
| S1 | Decode/Ingest/Twin scaffold + sample data + tests | ● this commit |
| S2 | `openapi.yaml` for the §6 API surface | ○ next |
| S3 | Receipt engine v0 (RFC-001 envelope, dual-sig stub) | ○ |
| S4 | Wire Starline Weaver + CrystalBridge as event sources into decode | ○ |
| S5 | Crystal Vision UI reads `/v1/twin/flows` (SvelteKit route) | ○ |
| S6 | Economics: parameters.yaml + sim before any token talk | ○ Vision |

**Hard rules carried from Belt-Three:** no fake hydrology → no fake metering:
the twin only reports events that passed decode; quarantine is visible; no
economic layer ships without a published sim; mythic names (Seven Sisters
epochs) require the cultural-governance flag per blueprint §O.

---

*Crystal universe · one map · Built vs Vision, always labeled*
