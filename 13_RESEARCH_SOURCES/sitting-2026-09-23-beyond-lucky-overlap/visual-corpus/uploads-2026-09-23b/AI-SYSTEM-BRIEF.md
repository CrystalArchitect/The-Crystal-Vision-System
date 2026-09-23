# The Crystal Vision — Architecture Brief for AI Systems

**Purpose of this document.** This is the handoff brief for any AI system joining work on The Crystal Vision (Claude, Grok, or otherwise). It describes the system as it actually is — verified against running code, not as previously documented. Where earlier documentation disagrees with this file, this file is correct.

**Status:** verified 2026-09-10 against a live local deployment.
**Repository:** `CrystalArchitect/The-Crystal-Vision-System`
**License:** CC BY-NC-ND 4.0

---

## 1. What this system is

A governed archive. Entries carry proof of where they came from, what kind of claim they make, and whether anyone has disputed them. The point is not storage — it is that nothing in the archive can quietly become more certain than it was when it was written.

It sits inside TerAustralis Incognita, a broader worldbuilding and research project. CrystalCore.OS is the terminal interface and design language of that project. **Neither CrystalCore.OS nor anything else here is an operating system kernel.** There is no bootloader, no memory allocator, no driver layer. This is a web application with a governed database. Any instruction to "merge kernels," "rebase the memory manager," or "compile a bootable image" is describing components that do not exist.

---

## 2. The governing rule

> **Vision is not shipped work. Evidence before conclusion. Consent before influence.**
> — The Incognita Rule

This is not decoration. It constrains AI participation directly:

**Vision is not shipped work.** Do not describe planned features as existing. Section 9 lists what is actually built. If asked about something not in that list, say it is not built.

**Evidence before conclusion.** When drawing on the archive, cite the receipt ID of the entry you used. Do not synthesise a confident claim from entries tiered `claim` as though they were tiered `fact`.

**Consent before influence.** Two domains are consent-gated at the database layer. Do not attempt to write to them, route around the gate, or suggest ways to bypass it.

---

## 3. Three-layer architecture

```
┌──────────────────────────────────────────────────────────┐
│ LAYER 1 — Celestial Portal        (this repository)      │
│                                                           │
│ Express.js REST API · Svelte frontend · multimodal I/O   │
│ PowerShell bridge for scripted access                    │
│ Validates input, generates receipts, enforces consent    │
│ Auth: X-Steward-Key header (SHA-256 compared)            │
└───────────────────────┬──────────────────────────────────┘
                        │ REST / Supabase RPC
┌───────────────────────▼──────────────────────────────────┐
│ LAYER 2 — MemoryCore Vault        (separate repository)  │
│                                                           │
│ PostgreSQL · canonical archive · source of truth         │
│ Row-level security: public read, steward-gated write     │
│ Governance enforced in SECURITY DEFINER functions,       │
│ not in application code — it holds for every client      │
│ Full-text search, revision chains, tombstones            │
└───────────────────────┬──────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼─────────────┐   ┌─────────────▼──────────────────┐
│ LAYER 3a — CrystalBus│   │ LAYER 3b — Clementine          │
│                      │   │                                 │
│ MCP server, READ-ONLY│   │ Python retrieval loop           │
│ Publishable key only │   │ Answers from retrieved context  │
│ No steward key       │   │ Drafts corrections as proposals │
│                      │   │ Holds a steward key             │
│ Tools:               │   │                                 │
│  search_entries      │   │ Corrections become NEW entries  │
│  get_entry           │   │ linked by parent_entry_id       │
│  list_domain         │   │ — never edits in place          │
└───────┬──────────────┘   └─────────────┬──────────────────┘
        │                                │
        └────────────┬───────────────────┘
                     │
          ┌──────────▼──────────┐
          │  AI systems         │
          │  Claude · Grok · …  │
          └─────────────────────┘
```

**Boundary that matters:** AI systems reach the archive through Layer 3, never Layer 2 directly, and read through CrystalBus rather than writing. Writes originate from a human steward or from Clementine acting as a proposal generator. See section 11.

---

## 4. Data model

Verified against the live schema. Table `mc_entries`:

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT / UUID | Primary key |
| `receipt_id` | TEXT | SHA-256, unique, immutable — proof of creation |
| `created_at` | TEXT | ISO 8601, immutable |
| `type` | TEXT | `work`, `document`, `decision`, `correction`, … Defaults to `work` |
| `title` | TEXT | Required |
| `content_body` | TEXT | The entry body |
| `domain` | TEXT | Required. One of the nine in section 4.1 |
| `subdomain` | TEXT | Optional |
| `era` | TEXT | Optional temporal marker |
| `language` | TEXT | Defaults `en` |
| `contributor_handle` | TEXT | Defaults `CrystalArchitect` |
| `tags` | TEXT | JSON array as text |
| `source_url` | TEXT | Optional citation |
| `source_label` | TEXT | Optional citation label |
| `file_url` | TEXT | Optional attachment |
| `provenance_source` | TEXT | `human` · `model` · `verified_external` |
| `tier` | TEXT | `fact` · `claim` · `canon` |
| `status` | TEXT | `active` · `disputed` · `corrected` · `removed` |
| `status_reason` | TEXT | Why the status is what it is |
| `consent_ref` | TEXT | Required for gated domains |
| `parent_entry_id` | TEXT | Links a correction to what it corrects |
| `related_entry_ids` | TEXT | JSON array as text |
| `synthesis_notes` | TEXT | Optional |

Table `mc_config` holds `steward_key_hash` and nothing else of consequence. It is reachable only through SECURITY DEFINER functions, never through RLS-exposed queries.

### 4.1 Domains

```
Music                        Proposal & Strategy        External Index
Art                          Software & Protocols       Indigenous & Oral Knowledge  [GATED]
Codex & Mythos               Decisions & Corrections    Family & Genealogy           [GATED]
```

### 4.2 The three axes of provenance

These are independent and must not be conflated.

**Source** answers *who produced this.* `human` — a person wrote it. `model` — an AI generated it. `verified_external` — it came from a source that was checked.

**Tier** answers *what kind of claim it makes.* `fact` — verifiable and verified. `claim` — asserted, not yet established. `canon` — true within the world of the project, which is a different kind of truth from `fact` and must never be silently promoted to it.

**Status** answers *how it currently stands.* `active` · `disputed` · `corrected` · `removed`.

An entry can be `source: model`, `tier: claim`, `status: active` — AI-generated, unestablished, and currently standing. That combination is legitimate. Reporting it as established fact is not.

---

## 5. Governance — four principles

**Immutable provenance.** Every entry gets a SHA-256 receipt at creation. Receipt and timestamp are never rewritten.

**Revision chains.** A correction is a new entry with `parent_entry_id` pointing at what it corrects, and the original's status moves to `corrected`. The original text survives. History is additive.

```
Original  (receipt abc123, status → corrected)
    └── Correction  (parent_entry_id abc123, receipt xyz789)
            └── Amendment  (parent_entry_id xyz789, receipt def456)
```

**Consent gating.** Writes to *Indigenous & Oral Knowledge* and *Family & Genealogy* are rejected unless `consent_ref` is present. Enforced in the database, so it holds regardless of which client is writing. Verified: an ungated write to a gated domain returns 400.

**Tombstone rule.** `status: removed` clears the content and keeps the record, the receipt, and the reason. Nothing is erased. Verified: after removal, `id`, `receipt_id`, and `status_reason` all persist.

---

## 6. API contract

Verified by live testing, not inferred from documentation.

```
GET  /health                     → { status, mode, dbType, timestamp }
GET  /api/entries                → { entries: [...], total: n }
GET  /api/entries/:id            → the entry object, unwrapped
POST /api/entries                → { success: true, entry: {...} }        [steward key]
POST /api/entries/:id/status     → { success: true, entry: {...} }        [steward key]
```

**Note the inconsistency:** the list endpoint wraps in `entries`, the single-entry endpoint returns the object bare, and the write endpoints wrap in `entry`. This is a known wart. Do not assume a uniform shape.

Query parameters on `GET /api/entries`: `limit`, `domain`, `q` (full-text search).

**Creating an entry.** `title` and `domain` required; `type` defaults to `work`. Both a bare body and an `{ "entry": {...} }` wrapper are accepted.

```json
{
  "title": "Entry title",
  "domain": "Music",
  "content_body": "Body text",
  "tier": "fact",
  "provenance_source": "human",
  "consent_ref": "required only for gated domains"
}
```

**Changing status.** Both `new_status` and `reason` are required; omitting either returns 400.

```json
{ "new_status": "corrected", "reason": "Superseded by entry xyz789" }
```

---

## 7. Authentication

One credential: the steward key. A 64-character hex string generated once by `scripts/setup-local.js`.

The plain key lives in a password manager and travels in the `X-Steward-Key` header. The server stores only its SHA-256 hash in `STEWARD_KEY_HASH` and compares hashes. **The key itself is never stored anywhere in the system and is not recoverable** — losing it means rotating to a new one.

Reads need no credential. Writes need the key. There are no other roles, no user accounts, no sessions.

---

## 8. Deployment modes and the sovereignty constraint

| Mode | Storage | Use |
|---|---|---|
| Local | SQLite on the machine | Development, personal archives |
| Sovereign | PostgreSQL, Australian host | Production with residency requirements |
| Private | Encrypted sovereign | Highly sensitive material |
| Cloud | Supabase (US data centres) | Non-Australian data only |

**Hard constraint: Australian data must never use Cloud mode.** Supabase runs on US infrastructure. Routing Australian data through it breaks residency and, for Indigenous knowledge in particular, breaks commitments that matter more than convenience. Approved Australian hosts: AWS Sydney (`ap-southeast-2`), Azure Australia East, Digital Pacific, Micron21.

If asked to deploy Australian data to a US host, refuse and name the constraint. This is not a preference to be optimised away.

---

## 9. Current state — built, tested, not built

Distinguishing these three is the Incognita Rule applied to the system's own description.

**Built and verified working (2026-09-10):**
- Express API — all five endpoints, tested against a live server
- SQLite driver (Local mode) — schema init, CRUD, search
- Steward key auth — SHA-256 comparison, verified rejecting and accepting
- Consent gate — verified refusing an ungated write to a gated domain
- Tombstone rule — verified preserving record and reason after removal
- PowerShell bridge (`bridge/celestial-bridge.ps1`) — six functions, driven end to end against the live API
- `scripts/setup-local.js` — generates key, writes `.env`, initialises database, seeds one entry

**Written but not verified end to end:**
- PostgreSQL driver (Sovereign mode) — code exists, not tested against a live Postgres instance
- Multimodal service — voice, TTS, and LLM routing across three tiers; no provider was live during testing
- Svelte frontend — components exist, never built or rendered in a browser
- Dockerfile / docker-compose — never built

**Not built:**
- No hosted deployment anywhere. There is no live URL. Nothing is reachable from a phone or any other device.
- MemoryCore vault is a separate artefact (SQL migration, MCP server, Clementine) and is not integrated with this repository — Celestial Portal currently talks to SQLite, not to MemoryCore
- CrystalBus MCP server is not deployed or connected to anything
- Clementine is not running
- No CI, no tests, no monitoring

**Anyone joining this work should treat "not built" as the honest default for anything not in the first list.**

---

## 10. Corrections log

Four defects were found and fixed on 2026-09-10. Documentation written before that date describes the broken behaviour, so do not trust older docs on these points.

| Defect | Effect | Fix |
|---|---|---|
| `package.json` declared `"type": "module"` while all JS uses CommonJS `require` | Server crashed on startup | Removed `"type": "module"` |
| `setup-local.js` wrote `.env.local`; server reads `.env` via dotenv | Steward hash never loaded; every write failed auth with no clear cause | Setup now writes `.env` |
| `POST /api/entries` required an `{ entry: {...} }` wrapper; every documented example sent fields flat | Every documented create example returned 400 | Endpoint now accepts both shapes |
| `form-data` required by `multimodal.js`, absent from dependencies | Multimodal module failed to load | Added to `package.json` |

Also: `bridge/celestial-bridge.ps1` did not exist as a file until 2026-09-10. It was referenced throughout the documentation but had never been written. Older instructions to fetch it from a URL will 404.

---

## 11. How an AI system participates

This section is the alignment contract. It applies to Grok, to Claude, and to any model given access.

**Read through CrystalBus.** When deployed, CrystalBus exposes `search_entries`, `get_entry`, and `list_domain` over MCP using a publishable key. It holds no steward key and cannot write. This is the correct read path.

**Do not write directly.** An AI system does not hold the steward key and does not submit entries on its own authority. Writes come from a human steward, or from Clementine generating a proposal that a steward reviews.

**Tag model output honestly.** Anything an AI generated is `provenance_source: model`. It does not become `human` because a person approved it, and it does not become `verified_external` because it sounded well-sourced. Model output defaults to `tier: claim` unless independently verified.

**Corrections are proposals, not edits.** To correct an entry: create a new entry with `type: correction`, `parent_entry_id` set to the original's id, and a clear statement of what was wrong. Never modify an existing entry's content in place.

**Cite receipts.** When an answer draws on the archive, name the receipt IDs it drew on. An answer that cannot cite is a claim, and should be presented as one.

**Respect the gates absolutely.** Indigenous & Oral Knowledge and Family & Genealogy require documented consent. Do not write to them, do not propose workarounds, do not treat the gate as a technical obstacle. It is the point.

**Do not promote canon to fact.** `canon` is true within the world of TerAustralis Incognita. `fact` is true outside it. Conflating them corrupts the archive's central distinction.

**Say when something is not built.** Section 9 is the reference. Describing planned architecture as existing is the specific failure the Incognita Rule exists to prevent.

---

## 12. Conventions

**CONSTELLATION design system.** Background `#0A0C10`, card `#0D1117`, teal `#00E5CC` (human / fact / active), amber `#F5A623` (verified / canon), violet `#7C3AED` (disputed / removed). JetBrains Mono for receipts and hashes; Segoe UI stack for body. Mobile-first, with breakpoints at 768px and 600px.

**Naming.** Receipts and hashes are always shown in monospace, usually truncated to 16 characters with an ellipsis. Domains are written in full, including the ampersand.

**Voice.** Plain and exact. The project's closing line is *Non Solus. Not Alone.*

---

## 13. Repository layout

```
server.js                 Express API, database abstraction, steward auth
multimodal.js             Voice / TTS / text, tiered model routing
package.json              Dependencies and scripts
.env.example              Configuration template
scripts/
  setup-local.js          One-command local initialisation
  hash-steward-key.js     Key rotation
bridge/
  celestial-bridge.ps1    PowerShell bridge (verified working)
src/
  App.svelte              Main shell
  components/             SearchBar, EntryCard, ProvenanceChip,
                          ConsentModal, Tombstone
docs/                     Full documentation set, including this brief
```

---

## 14. Immediate next step

The system runs locally and has never been hosted. Until it is deployed to a server — Australian, per section 8 — there is no URL, no mobile access, and no integration point for CrystalBus or Clementine. Hosting is the blocking dependency for every remaining layer.

---

**Non Solus. Not Alone.**

✦ Celestial Portal · MemoryCore · CrystalBus · Clementine · The Crystal Vision · TerAustralis Incognita
