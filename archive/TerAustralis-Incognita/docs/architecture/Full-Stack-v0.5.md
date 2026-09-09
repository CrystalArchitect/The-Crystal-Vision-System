# Crystal Core Full Stack v0.5 — Surfaces & Mesh

**Version:** 0.5.0  
**Status:** Demo surfaces + mesh stub + TS client — **not mainnet**  
**Builds on:** v0.3 full-stack gap-fill · v0.4 OpenAPI / Budapest seed · crystal-interface UI

---

## Purpose

v0.3–0.4 closed the **architecture skeleton**. v0.5 ships **touchable surfaces** and a **replaceable mesh API**:

| Artifact | Path | Role |
|----------|------|------|
| Operator shell | `src/apps/crystal-interface/` | Twin, mesh, pipeline, econ, receipts |
| Citizen shell | `src/apps/vision-web/` | Credits, capability, personal twin, privacy stubs |
| Mesh stub | `src/node/mesh/` | libp2p-shaped in-process fabric |
| TS SDK | `src/sdk/typescript/` | Client for local agent `:8787` |
| OpenAPI | `docs/openapi.yaml` | Contract (still 0.3.x paths; bump when agent gains mesh routes) |

---

## Product map (unchanged rule)

| Brand | Facing |
|-------|--------|
| **Crystal Vision** | Users / citizens → `vision-web` |
| **Crystal Core** | Operators / builders → `crystal-interface` + node agent |
| **TerAustralis + Starline** | Investor / pilot narrative |

Cultural firewall: Seven Sisters / Songline = collaborative metaphor only.

---

## Mesh phase plan

| Phase | Transport | Gate |
|-------|-----------|------|
| **P1 (now)** | `MeshStub` in-process | Tests + agent wiring optional |
| **P2** | Real libp2p (noise + yamux + gossipsub) LAN | Security review of identify |
| **P3** | Region bootstrap + capability-gated topics | Federation charter |
| **P4** | Cross-region stake bridge | **Mainnet still HOLD** |

Protocols (draft):

- `/crystal/manifest/1.0.0`
- `/crystal/receipt/1.0.0`
- `/crystal/twin-delta/1.0.0`

---

## Citizen journey (Vision)

1. Open Vision shell  
2. Hold hybrid credits (demo balances)  
3. Grant short-lived capability (15m demo)  
4. Consume → dual-attested receipt (local)  
5. Export / erase request stubs → `compliance/GDPR_ROPA.md`

---

## Operator journey (Core UI)

1. Run pipeline DECODE→…→UPGRADE  
2. Select mesh node, inspect manifest JSON  
3. Create / confirm ServiceReceipt  
4. Burn CORE → credits (sim only)  
5. Epoch select (timelock narrative)

---

## Explicit non-goals (v0.5)

- No on-chain deploy  
- No real PSP / bank rails  
- No production key custody  
- No claiming Indigenous IP or Songline ownership  
- No silent mainnet enablement  

Authority remains **NONE/HOLD** until audit + governance vote.

---

## Runbook

```powershell
# UI (both apps under /apps)
cd apps
python -m http.server 8090
# Vision:  http://127.0.0.1:8090/vision-web/
# Core UI: http://127.0.0.1:8090/crystal-interface/

# Node agent
python -m node.agent.server --port 8787

# Mesh tests
python -m pytest tests/test_mesh_stub.py -q

# Full tests
python -m pytest tests -q
```

---

## v0.6 candidates

- Agent routes: `GET /mesh/peers`, `POST /mesh/publish` backed by `MeshStub`
- Vision shell → fetch receipts from agent when CORS open  
- Capability macaroon prototype (offline verification)  
- ArgoCD app-of-apps for `budapest-starline` staging only  

---

## Changelog (v0.5)

- Crystal Vision citizen shell  
- libp2p-shaped mesh stub + tests  
- TypeScript SDK scaffold `@crystal-core/sdk`  
- This roadmap document  
