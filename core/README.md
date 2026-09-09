# Crystal Core — the engine

Per the boundary charter
([`Project-Boundaries.md`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/governance/Project-Boundaries.md),
[`ADR-0011`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/adr/ADR-0011.md)),
this area holds Crystal Core: the runtime, protocols, APIs, and shared
libraries — what other software imports and calls. No user interfaces
live here.

| Path | Component |
|---|---|
| `crystal-core/` | The protocol pack — Starline Weaver on the **CrystalBus**, the AI-comms channel (`bus/`) · Decode→Ingest→Twin pipeline (`services/`) · Consent Transport / Starline (`consent_transport/`; `starline/` is a deprecated backward-compatibility alias, not a second component) · RDP record kernel (`rdp/`) · Host trust (`host_trust/`; persist refuse wired on `consent_transport`, CrystalBridge grants, companion `memory.json` atomic replace, audit/ask/revocation append, StarlineAgent home mkdir, and PeerStore atomic replace; fragments stay RAM) |
| `crystalcore/` | CrystalBridge — the fail-closed MCP consent gate |
| `profiles/` | CrystalBridge profile configs (runtime data such as audit logs is gitignored) |
| `node/mesh/` | In-process mesh stub (libp2p-shaped; no real networking yet) |
| `sdk/typescript/` | TypeScript client SDK scaffold (no consumer wired up yet) |
| `tests/unit/` | Repo-level test suite for components without an embedded `tests/` dir (currently: the mesh stub) |

## Prove it

```bash
cd core/crystal-core
python3 -m bus.selftest
python3 -m services.selftest
python3 -m rdp.selftest
python3 -m host_trust.selftest
pip install -r requirements-consenttransport.txt && python3 -m consent_transport.selftest

cd .. && PYTHONPATH=. python3 -m pytest tests -q   # mesh stub
```

## The dependency rule

Crystal Vision may depend on Crystal Core; **Crystal Core never imports
Crystal Vision.** (CrystalBridge reaches the companion's memory *by configured
data path at runtime* — it serves the companion without importing it.)

---

Imported from the umbrella repository's branch
`claude/crystalcore-boot-visual-jau1bk` @ `32692fd` (Migration-Plan
Stage 1, PR 1 — engine first). Directory names preserved; only the
`src/` prefix became `core/`.
