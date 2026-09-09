# Crystal Core — Full Stack Blueprint v0.2 → v0.3
## Decode · Ingest · Upgrade

**Layer label: VISION with engineering targets.** This is the aspirational full-stack
blueprint for the Crystal universe, captured as canon. For what is actually built
and running today, see `ARCHITECTURE.md` — the two documents must never be confused.

**Single sentence:** A sovereign mesh where nodes own data, a digital twin meters real
flows, credits pay for services, CORE aligns incentives, GitHub + chain govern change —
with Decode / Ingest / Upgrade as the data lifecycle.

---

## 0. DECODE (thread → system role)

| Thread | Decoded meaning | System role |
|--------|-----------------|-------------|
| CrystalCore | Sovereign kernel / reactor | Protocol + runtime identity, stake, receipts |
| Crystal Vision | Shared sight | Twin UI, layered flows, public specs |
| TerAustralis Incognita | Uncharted frontier | Expansion regions, pilot deployments, epoch narrative |
| Seven Sisters spine | Mythic geometry + story epochs | Federation corridors, release calendar (cultural governance required) |
| 4 layers | Mythic → Physical → Economic → Governance | Bounded contexts in architecture |
| Burn-and-mint + credits | Stable UX + token incentives | Payments + settlement service |
| RFC-001 | Identity + ServiceReceipt | Crypto + metering contract |
| Starline Budapest | Reference physical node | Mobility/energy twin + launch template for hubs |

## 1. INGEST (unified system map)

Experience (Vision UI · Starline hub · mobile) → Edge (libp2p node · SQLite/CRDT ·
sensors · agents) → **DECODE → INGEST → TWIN** → RECEIPT engine → ECON burn/mint →
Governance (GitHub RFCs · sim reports · on-chain params · slash), with an UPGRADE
service closing the loop.

## 2. UPGRADE (v0.1 → v0.2)

| Area | v0.1 | v0.2 |
|------|------|------|
| Data path | Implied metering | Explicit Decode → Ingest → Twin → Receipt |
| Identity | RFC draft | `did:crystal` + agent sub-DIDs + capability macaroons |
| Economics | Formulas | `parameters.yaml` + batch receipt roots on-chain |
| Mobility | Starline visuals | Starline Budapest as canonical pilot region pack |
| Mythic | Metaphor | Epoch gates: no production mythic strings without council flag |
| Ops | Phases | Monorepo + K8s + one Helm chart per region |
| AI nodes | Open question | Agent bond + scoped receipts, parent liability DID |

## 3. Full stack (by layer)

- **Clients:** Twin web UI (layered flows, deck.gl/MapLibre), mobile offline-first,
  Tauri operator desktop, shared design tokens (navy / cyan / gold).
- **Edge & mesh:** libp2p (QUIC, gossipsub), SQLite + Litestream, Automerge CRDT,
  Rust/Go node agent, OPA policy sidecar.
- **Core services:** api-gateway · decode (schema/units/dedupe/fraud) · ingest
  (stream, partitioning, backpressure) · twin-api (PostGIS + TimescaleDB) ·
  receipt-engine (RFC-001, dual-sig, Merkle batch roots) · econ (double-entry
  credits + chain worker) · governance-api · upgrade (governance-gated GitOps) · search.
- **Digital twin:** H3 spatial index, TimescaleDB series (water, energy, egress,
  GPU-s), CloudEvents → `twin.event/1`, IPFS checkpoints, Flink simulation (later).
- **Economic:** app-chain (Cosmos SDK or OP Stack L2), stake/slash/ReceiptRoot/
  BurnMint/treasury contracts, off-chain credits ledger, cadCAD/Mesa sims.
- **Governance:** GitHub RFCs + CODEOWNERS; on-chain votes/timelock; auditor guild
  attestations (IPFS CID); off-chain cultural council charter.
- **Observability & security:** Prometheus/Grafana, Loki, OTel, Vault/KMS,
  GitHub Actions → Argo CD, K8s cloud + K3s edge.

## 4. Pipeline service specs

### DECODE
Input: raw mesh frames, MQTT, HTTP, file drops → Output: `crystal.twin.event/1`;
invalid → quarantine topic.

```json
{
  "schema": "crystal.twin.event/1",
  "event_id": "uuid-v7",
  "source_did": "did:crystal:...",
  "h3": "8abe...",
  "class": "energy.kwh",
  "value": "12.4",
  "unit": "kWh",
  "observed_at": "ISO8601",
  "raw_ref": "bafy..."
}
```

Rules: JSON Schema, unit conversion, monotonic meter checks, replay window.

### INGEST
Partition by `h3 + class`, write time-series store, emit receipt windows, fan out to
Vision WebSocket. SLA: p95 < 2s cloud path; 72h edge offline buffer.

### UPGRADE
Input: approved RFC + on-chain timelock → rolling node updates, schema migrations,
epoch parameter push, blue/green API. **Hard rule:** economic param changes require
an attached sim report artifact CID.

## 5–8. Monorepo, API, Budapest, build order

Monorepo: `apps/` (vision-web, mobile, operator, starline-budapest) · `services/` ·
`node/crystal-agent` · `chain/` · `packages/` (crypto, receipts, schemas, ui-tokens) ·
`sim/` · `spec/rfc/` · `deploy/helm + regions + argocd`.

MVP API: `POST /v1/decode/preview` · `POST /v1/ingest/events` ·
`GET /v1/twin/flows?h3=&layer=` · `POST /v1/receipts` + `/confirm` ·
`POST /v1/econ/burn` · `GET /v1/econ/credits` · `GET /v1/gov/rfc` ·
`POST /v1/upgrade/epochs/{id}/apply`. Auth: node DID challenge + capability
macaroon; humans via OIDC → wallet link.

Starline Budapest pilot: 3–10 edge operator nodes; region cloud runs decode/ingest/
twin/vision; first receipt class `mobility.checkin` or `energy.kwh` at hub.

Build order: S1 crypto+receipts → S2 agent gossip → S3 decode+ingest+store →
S4 twin+UI → S5 receipts → S6 testnet econ+sim → S7 upgrade+GitOps+Budapest Helm →
S8 security audit gate → pilot.

---

# v0.3 — Gap fill (the skin, nerves, and legal skeleton)

Honest checklist of what v0.2 lacked:

| Gap | Why it matters |
|-----|----------------|
| Threat model & trust zones | Sovereign mesh = attack surface at every node |
| Human journeys | No onboarding = no network |
| Fiat / payments / treasury | Credits need real rails |
| Compliance | Energy, water, money, PII = licenses |
| Interop standards | Utilities don't speak "custom JSON" |
| Federation & charters | "No hierarchy" still needs rules to join |
| Data lifecycle & erasure | Sovereignty = delete/export, not slogans |
| AI agents (full subsystem) | Bond, liability, receipts, rate limits |
| Dispute & slash courts | Economics without arbitration = griefing |
| SRE: SLO, DR, chaos | Pilots fail on ops, not whiteboards |
| DX: local dev, SDK, sandboxes | Builders need a 15-minute start |
| Testing pyramid | Contract, sim, load, Byzantine drills |
| Schema registry & versioning | Upgrade path must be explicit |
| Privacy / selective disclosure | Twin data is sensitive |
| Cultural governance (operational) | Seven Sisters can't be decoration |
| Product ↔ brand map | Vision vs Core vs TerAustralis vs Starline |
| Commercial model | Who pays whom, when, in what jurisdiction |

**A. Product map:** TerAustralis = holding narrative · Crystal Vision = product UX ·
Crystal Core = protocol/runtime/economics · Starline Budapest = reference region pack ·
21st Europe Starline = external reference, integrate via partner/API, never rebrand.

**B. Trust zones:** Z0 device (user keys) → Z1 edge mesh (peer-attested) → Z2 region
cloud (charter) → Z3 global (governance) → Z4 partners (contractual). Threats & answers:
sybil → stake + peer diversity; fake receipts → dual-sig + auditor lottery + meter hash
chain; collusion mint → caps + anomaly detection; slash griefing → dispute bonds +
appeals; key theft → hardware + rotation + short-lived macaroons; eclipse →
multi-bootstrap + IPFS checkpoints; governance capture → stake caps + timelock;
AI-agent abuse → sub-DID bond + scoped caps + parent slash liability; cultural harm →
council veto on mythic assets.

**C. Human journeys:** citizen (install → credits → grant capability → consume →
export/erase) · operator (keys → stake → run agent → earn mint → unbond 14d) ·
builder (clone → `make dev` → RFC PR with sim → staged deploy) · auditor (beacon
selection → evidence CIDs → attestation → mint release or slash ticket).

**D. Federation charters:** signed charter doc (IPFS CID) + stake threshold; per-class
min stake, auditor set size, allowed receipt classes, mythic epoch only if
`council_approved: true`, named dispute court. Budapest = first charter template.

**E. Integrations:** energy IEC 61850/Modbus/MQTT · water SCADA/OPC-UA · mobility
OCPI/GTFS-rt · payments PSP webhooks · gov OpenAPI adapters · GitHub webhooks ·
identity OIDC/eIDAS. **Adapter contract: all adapters emit `crystal.twin.event/1`
only — never bypass decode.**

**F. Payments & treasury:** fiat→credits via PSP webhook; CORE burn→credits via
indexer; operator payout via mint + optional off-ramp; enterprise invoices via
treasury multisig; nightly PSP⟷ledger⟷chain reconciliation. **Legal note: token +
credits may trigger MiCA / e-money rules — engage counsel before any public sale.**

**G. Data lifecycle / GDPR:** export = signed archive of twin+receipt CIDs; erase =
revoke macaroons + tombstone PII (chain stays hash-only); retention per class
(raw 90d, aggregates 7y, charter-tunable); minimization = DIDs + hashes, never names;
sovereignty default = primary copy on node, cloud replica opt-in.

**H. AI agents:** identity `did:crystal:parent#agent-N`; parent-staked slashable bond;
macaroon-scoped classes and daily caps, no governance keys; parent co-sign for mint;
parent liability on fraud; per-agent rate limits in decode.

**I. Dispute court:** bonded dispute within window → evidence packet (receipt + twin
CIDs + auditor report) → markdown docket court repo → release/slash/ban → one appeal
at higher quorum. GitHub is process; chain executes after timelock.

**J. SRE:** ingest 99.5% MVP / 99.9% prod; decode→twin p95 < 2s; RPO 1h / RTO 4h;
Litestream + PG PITR; secondary-region DR (mesh survives cloud loss); chaos drills
(kill ingest, 72h mesh buffer); public status page; per-region FinOps.

**K. DX (15-minute start):** `git clone && make dev && make seed-budapest && make test
&& make sim`; `@crystal/sdk` (TS), `@crystal/cli`, sandbox testnet with faucet, Pact
contract tests between decode ↔ ingest ↔ twin.

**L. Testing pyramid:** unit (crypto/receipts/schema) → contract (OpenAPI+Pact) →
integration (compose e2e) → sim (cadCAD sybil/bear) → load (k6) → Byzantine (malicious
libp2p nodes) → red team. **Gate: no mainnet without external audit + chaos weekend.**

**M. Schema registry:** `packages/schemas/` with `registry.json` compatibility matrix;
breaking change → new major + migration job; nodes advertise `supported_schemas[]`;
decode rejects unknown majors unless epoch-flagged.

**N. Privacy roadmap:** MVP hashes+DIDs → v1 SD-JWT selective disclosure → v2 ZK
proof-of-SLA research spike.

**O. Cultural governance (operational):** `MYTHIC_SPINE.md` (core draft) +
`CULTURAL_PROTOCOL.md` (council approval required); CI check on
`council_approved: true` before any epoch name ships; block list — no sacred secret
material, no unapproved Songline commercial use. **Seven Sisters in software: only as
epoch codenames inside approved charters.**

**P. Commercial & org:** revenue = credit-sale margin (treasury+ops), burn fees
(protocol/stakers), enterprise contracts (60% operators / 25% buy-burn / 15% treasury),
grants via RFC awards. Phase gates: Seed = mesh MVP + RFC-001 + sim published;
Series A = Budapest pilot 50 nodes + audited testnet; Scale = second federation +
licensed payments.

**R. Monorepo additions:** `integrations/` · `services/{dispute-court,agent-runtime,
payments-ledger,schema-registry}` · `security/THREAT_MODEL.md` ·
`compliance/{GDPR_ROPA,LICENSING_CHECKLIST}.md` · `courts/templates/` ·
`sdk/{typescript,cli}` · `tests/{e2e,byzantine,load}`.

**S. Toward v0.4:** full OpenAPI 3.1 · compose+Makefile scaffold · RFC-002 governance/
upgrade binding · RFC-003 federation charter + dispute · Budapest sample data
(1000 events + 50 receipts) · MiCA legal memo outline · sequence diagrams
(burn, mint, slash, launch day).

---

*Blueprint captured as canon · VISION labeled · the runnable spine lives in `services/`*
