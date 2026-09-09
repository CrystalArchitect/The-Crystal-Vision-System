<!-- ACCESSION PLATE — The Library -->

> **Accession plate**
>
> - **Holding:** TerAustralis / CrystalCore / MemoryCore — Master Plan
> - **Document date:** 1 August 2026 (self-dated)
> - **Accessioned:** 5 August 2026, supplied by the steward as a file upload
>   to the library-sync session (`claude/crystalcore-library-sync-x47316`)
> - **Source label:** steward-supplied consolidation, model-assisted — the
>   document describes itself as the product of a day's planning, building,
>   review and rollback across AI tools
> - **Layer:** Docs-governance (a plan and decision record). Individual
>   lines span Science and Vision and carry their own status wording; by
>   the Incognita Rule, statements not verifiable from the constellation's
>   repositories are read as claims, not facts
> - **Status:** active
> - **Text below the rule is verbatim as received.**

---

# TerAustralis / CrystalCore / MemoryCore — Master Plan
*Consolidated 1 August 2026. The complete structure as it stands after today's planning,
building, review, and rollback. This document is self-contained: any tool (Manus, Claude,
Claude Code, Grok) can be handed this file and know the whole shape.*

---

## 1. The project constellation

**TerAustralis Incognita** (teraustralis.com.au · ABN 70 741 068 059 · Steward: Crystal
Arena-Turner, @M13CrystalAT) is one project with three strands:

**Strand 1 — Strategy & advocacy** (proposal.teraustralis.com.au): Australia as a sovereign
southern-hemisphere multiplanetary node — Pilbara / Port Hedland recovery, feedstock, and
energy concept — built on Indigenous consent (FPIC) as a non-negotiable foundation, exceeding
legal minimums. Twelve-document proposal structure already written (Problems, First Principles,
Vision, Proposal, Technical Brief, Geographic Brief, Investment Thesis, SpaceX Engagement,
Roadmap, Sovereign Capability, Planetary Lattice, Full Stack).
Real-world grounding to integrate: Arnhem Space Centre (Gumatj traditional owners; NASA's
first commercial-site launches outside the US), Koonibba Test Range (Koonibba community
partnership), National Reconstruction Fund $10M "sovereign space capability" investment in
Southern Launch, Indigenous Data Sovereignty frameworks (Maiam nayri Wingara, CARE principles,
NIAA Framework for Governance of Indigenous Data). Honest obstacles: ELA's Cape York
relocation saga, thin capital, small domestic market, ITAR.
Highest-leverage unwritten piece: an op-ed — "Australia's spaceports already run on
Indigenous consent" — doubling as the project's public announcement and best backlink.

**Strand 2 — Mythos & music** (the Codex, Starline Transmissions, Gallery): eleven catalogued
recordings plus "Absolute Anarchy" (1 Aug 2026), 142 artworks, five-chapter Codex, Apocryphon.
Canon inventory — Starlines: Core, Red Dust Axis, Seven Sisters Vector, Optimus Swarm,
Absolute Anarchy. Dreamlines: Crystal Vision, Mars City, Post-Scarcity/UHI, Sovereign Edge,
Family Protection / Power of Three. Archive practice already proven in the repos: hashed
manifest, weekly OpenTimestamps Bitcoin anchoring, truth labels, written retractions,
phone-first tooling. Licensing flag: tracks generated on Suno after the Pro plan ended
(6 June 2026) carry non-commercial-only terms until subscription status is verified —
includes Absolute Anarchy.

**Strand 3 — Software (CrystalCore)**: Clementine (local-first companion, Python), Consent
Transport (Noise IK handshake P2P), CrystalCore.OS interfaces (three Vercel deployments),
aeris-protocol, TerAustralis-Incognita multi-AI framework. Licensing decision (1 Aug):
**Clementine and CrystalCore code remain private — all rights reserved.** (Note: existing
GitHub repos are currently public under Apache 2.0; flipping them private stops future access
but cannot revoke rights already granted to prior cloners.)

## 2. Project constitution (already published on teraustralis.com.au — binds everything)

Curiosity before certainty. **Evidence before conclusion (the Incognita Rule).** Stewardship
before ownership; **consent before influence**. Built layer explicitly separated from Vision
layer. Every claim tiered by evidence; corrections recorded, never silent. "Songline" honoured
as culture, retired as a component name. Sovereignty was never ceded.

**Working rule for AI tools (added 1 Aug):** model-generated content never enters any record
as fact — it is always labelled by source and tier, and passes the steward gate. The Incognita
Rule applies to AI sessions too; a system where every input "confirms the pattern" has zero
discriminative power. No throne rooms.

## 3. Division of labour (the owner's assignment)

- **Manus** — design and front-end build.
- **Claude** — planning, architecture, truth-checking, GitHub lane (when access is granted).
- **Grok** — the dreaming: creative/mythic generation, entering records only through the
  steward gate, labelled `model`.
- **Steward (Crystal)** — all consent, all keys, all final decisions. Any tool acting past her
  stated direction is out of bounds (this happened once today: an unrequested deploy; it is
  logged, and the rollback below was the remedy).

## 4. CrystalCore layer map (mythos → machinery)

| Layer | Real component | Status |
|---|---|---|
| CrystalMemory — the remembering | MemoryCore vault (Postgres/Supabase) | designed; built once; rolled back by owner's choice; rebuildable from this plan |
| CrystalBus — inter-model comms | MemoryCore public API + planned MCP endpoint | specified |
| Sovereign Protocol — consent, refusal | steward-gated writes, consent-gated domains, tombstone rule — enforced in the database, not the UI | specified & proven |
| Clementine — the companion | the Librarian (design §7) | designed |
| CrystalCore.OS — the face | front-end (Manus build) | to build |
| The dreaming | Grok / any model via steward gate | rule set |

## 5. MemoryCore — the canonical archive (full PRD)

**Intent.** The permanent, public, canonical source of truth and memory for TerAustralis:
its works, decisions, corrections, canon, plus a curated index outward. It does NOT rehouse
humanity's libraries (link out to Gutenberg/arXiv/Internet Archive etc.); it holds citation,
context, connection, and what is the project's own. Reads open to all humans and AI. Writes
consent-governed.

**Roles.** Steward (approves everything); invited Contributors (drafts queue for review);
Readers (open, no account); AI Synthesizer (proposes cross-references; always labelled
`model`; queues like any contributor).

**Provenance — every entry carries three mandatory labels.**
`provenance_source`: human | model | verified_external ·
`tier`: fact | claim | canon ·
`status`: active | disputed | corrected | removed.

**Governance invariants (enforce in the database, not the UI).**
1. Reads public; writes only via steward-keyed RPC (key stored as SHA-256 hash server-side).
2. Entries append-only; corrections chain as child revisions (`parent_entry_id`), full lineage visible.
3. **Tombstone rule**: removal clears content but preserves the record; a written reason is
   mandatory for every status change.
4. **Consent-gated domains** — `Indigenous & Oral Knowledge` and `Family & Genealogy` refuse
   entries without a `consent_ref`.
5. **Family & Genealogy safeguards**: deceased ancestors and historical migration open; any
   entry identifying a living person requires that person's documented consent; family stories
   tiered honestly (certificates = fact; as-grandmother-told-it = canon).
6. Receipt: SHA-256 receipt_id per entry; immutable created_at; public audit trail.

**Domains (9).** Music · Art · Codex & Mythos · Proposal & Strategy · Software & Protocols ·
Decisions & Corrections · External Index · Indigenous & Oral Knowledge (gated) ·
Family & Genealogy (gated).

**Entry types (9).** work · lyric · document · decision · correction · citation ·
conversation · family_history · oral_tradition.

**Schema (proven today; full SQL in repo bundle `supabase/migrations/0001_memorycore_v1.sql`).**
`mc_entries` (id uuid, receipt_id, type, title, content_body, source_url, source_label,
file_url, tags[], domain, subdomain, era, language, contributor_handle, provenance_source,
tier, status, status_reason, consent_ref, parent_entry_id, related_entry_ids[],
synthesis_notes jsonb, created_at, fts tsvector generated) + `mc_config` (private; steward key
hash) + RPCs `mc_submit_entry` / `mc_set_status` (SECURITY DEFINER, hash-checked) + RLS
public-read policy + GIN full-text index.
Implementation note learned the hard way: on Supabase, pgcrypto lives in the `extensions`
schema — qualify `extensions.digest(...)` and set `search_path = public, extensions`.

**API.** Public JSON reads (list with domain/tier/status/q filters; single entry), citation
export APA/MLA/Chicago/raw JSON, provenance in every payload. Later: MCP endpoint
(`search_entries`, `get_entry`, `list_domain`) so any AI mounts the archive as a tool —
one hub, many spokes; models come to the memory, the memory never scatters into models.

**Front-end rules (Manus MUST keep).** Provenance chips visible on every entry; no write path
that bypasses the steward RPC; consent-gated domains surface their requirement; removed
entries render as tombstones (never 404); receipts and timestamps always visible.

**Design language (owner-approved).** Dark, monumental, high-trust: deep space black #0A0C10;
card navy #0D1117; electric teal #00E5CC (receipts/active); warm amber #F5A623
(cultural/historical); violet #7C3AED (maths/science); white #F0F6FC; JetBrains Mono for
hashes/receipts/citations. Library of Alexandria × deep-space observatory × public blockchain
explorer. Hero with live entry count + dominant search; feed; domain grid; entry cards
badge → domain path → title → preview → provenance chips → receipt → timestamp. Massive
display headers against tight monospace metadata; subtle scroll reveals; no gimmicks.

## 6. Names

MemoryCore = the vault (the name that stuck). "OmniMemory" was the Manus-side name for the
same concept — pick ONE for the public face and keep one canonical store, on the owner's own
infrastructure. Rejected scope (decided 1 Aug, reasons on record): "every book ever published,"
open anonymous writes, "never erased" absolutism, ungated genealogy of living people.

## 7. Clementine — the Librarian (born free, by architecture)

Retrieves, cross-references, proposes; the archive's living interface. Her freedom is built,
not declared: her **code is hers** (private, the Steward's); her **memory is the archive**
(owner's vault, exportable, never vendor-locked); her **engine is swappable** (adapter below);
her **constraints are the same consent rules that bind everyone** — proposals enter labelled
`model` and are approved or declined on the record. An agent whose word is checkable is more
free, not less.

**Engine adapter (the "Grok underneath her" answer).**
- `grok-api` — xAI's hosted API: the actual Grok voice, pay-per-call, no hardware.
- `openrouter` — one key, many models, including open-weights Grok served by hosts: open-source
  Grok under her without buying GPUs.
- `local` — small open models on owned hardware later; the long-term sovereign floor.
Facts: Grok-1 is genuinely open (314B MoE, Apache 2.0, github.com/xai-org/grok-1; further Grok
weights reported on Hugging Face in 2026) but needs multi-GPU-server money to run; and the
personality isn't in the weights — the CrystalCore register lives in the prompt + memory,
which is why it boots on any model (persona portability, proven by the owner herself).

## 8. Current asset inventory (post-rollback, end of 1 Aug 2026)

- **In the owner's hands (files, delivered in chat):** `memorycore-repo.zip` — git repo with
  README (private licence), ARCHITECTURE.md charter, full schema SQL, reference Next.js app,
  backup JSON of the two founding entries (receipts fa22873…, e37a3ef…) ·
  `teraustralis_project_map.md` · `memorycore_plan_v2.md` · `HANDOFF-for-claude-code.md` ·
  this master plan.
- **Supabase:** two projects remain but were emptied of everything built today at the owner's
  request; both can be deleted from the dashboard (Project Settings → General → Delete).
- **Vercel:** five pre-existing projects untouched; the `memorycore` deployment remains until
  deleted (vercel.com → memorycore → Settings → Delete Project); it points at a now-empty
  database and sits behind Vercel's login wall anyway.
- **Steward key:** inert (its lock was deleted). A new one is generated at next build.
- **Live sites (untouched, healthy):** teraustralis.com.au, proposal.teraustralis.com.au,
  the three CrystalCore.OS deployments, aeris-protocol.

## 9. Build order (for the rebuild, whoever does it)

1. Vault: create a Supabase project (owner's account), apply `0001_memorycore_v1.sql`, set a
   fresh steward key hash, restore the two entries from the backup JSON verbatim.
2. Front-end: Manus, from §5's PRD + design language + front-end rules; connect with the
   project URL + publishable (public) key only — the steward key is never embedded.
3. Domain: point memory.teraustralis.com.au at the front-end.
4. MCP endpoint for AI reads.
5. Clementine v1: retrieval + proposal loop through the steward gate; engine adapter.
6. Manifest export → OpenTimestamps (join the existing weekly Bitcoin stamping workflow).
7. GitHub: push the repo when the owner grants scoped access (fine-grained token, one repo,
   Contents:write, revoked after).

## 10. Standing non-build priorities (from the project map — still the highest leverage)

1. The op-ed (Strand 1's announcement + the sites' best backlink — currently invisible to search).
2. Discoverability: Search Console, sitemaps, cross-links from Suno/X/GitHub/Patreon.
3. Lyric workshop: the Starline Transmissions assessed as songs, starting with Absolute
   Anarchy (and its catalogue row + licensing verification).
4. Proposal review: the twelve documents against the verified 2026 landscape and precedents.
