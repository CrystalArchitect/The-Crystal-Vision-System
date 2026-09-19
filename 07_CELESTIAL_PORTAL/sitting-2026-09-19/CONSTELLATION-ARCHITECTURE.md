# TerAustralis Incognita — Constellation Architecture

*Complete structural map of the three-strand constellation and CrystalCore's layer system.*

---

## I. The Three-Strand Constellation

**TerAustralis Incognita** (teraustralis.com.au · ABN 70 741 068 059 · Steward: Crystal Arena-Turner, @M13CrystalAT) operates as a single project with three interdependent strands:

### Strand 1: Strategy & Advocacy
**Site:** proposal.teraustralis.com.au

Australia as a sovereign southern-hemisphere multiplanetary node — Pilbara/Port Hedland recovery, feedstock, and energy concept — built on Indigenous consent (FPIC) as non-negotiable foundation, exceeding legal minimums.

**Twelve-document proposal structure:**
1. Problems
2. First Principles
3. Vision
4. Proposal
5. Technical Brief
6. Geographic Brief
7. Investment Thesis
8. SpaceX Engagement
9. Roadmap
10. Sovereign Capability
11. Planetary Lattice
12. Full Stack

**Real-world grounding:**
- Arnhem Space Centre (Gumatj traditional owners; NASA's first commercial-site launches outside the US)
- Koonibba Test Range (Koonibba community partnership)
- National Reconstruction Fund $10M "sovereign space capability" investment in Southern Launch
- Indigenous Data Sovereignty frameworks (Maiam nayri Wingara, CARE principles, NIAA Framework)

**Highest-leverage unwritten piece:** Op-ed "Australia's spaceports already run on Indigenous consent" — doubles as project announcement and best backlink.

---

### Strand 2: Mythos & Music
**Sites:** Gallery, Starline Transmissions, Codex + Apocryphon

Eleven catalogued recordings plus "Absolute Anarchy" (1 Aug 2026), 142 artworks, five-chapter Codex.

**Canon inventory:**
- **Starlines:** Core, Red Dust Axis, Seven Sisters Vector, Optimus Swarm, Absolute Anarchy
- **Dreamlines:** Crystal Vision, Mars City, Post-Scarcity/UHI, Sovereign Edge, Family Protection / Power of Three

**Archive practice:**
- Hashed manifest with SHA-256 receipts
- Weekly OpenTimestamps Bitcoin anchoring
- Truth labels and written retractions on record
- Phone-first tooling

**Licensing flag:** Tracks generated on Suno after the Pro plan ended (6 June 2026) carry non-commercial-only terms until subscription status is verified — includes Absolute Anarchy.

---

### Strand 3: Software (CrystalCore)
**Components:**
- **Clementine:** Local-first companion (Python)
- **Consent Transport:** Noise IK handshake P2P
- **CrystalCore.OS:** Three Vercel deployments (interfaces)
- **aeris-protocol:** (specification layer)
- **TerAustralis-Incognita multi-AI framework:** Model-agnostic engine adapter

**Licensing (1 Aug 2026):** Clementine and CrystalCore code remain private — all rights reserved. (Note: existing GitHub repos currently public under Apache 2.0; flipping them private stops future access but cannot revoke rights already granted.)

---

## II. The CrystalCore Layer Map (Mythos → Machinery)

How the three strands connect and operate at scale:

| Layer | Component | Real Implementation | Status |
|---|---|---|---|
| **CrystalMemory** — the remembering | MemoryCore vault | Postgres/Supabase (ap-southeast-2) | Designed; deployable |
| **CrystalBus** — inter-model comms | MemoryCore public API | REST/JSON + planned MCP endpoint | Designed |
| **Sovereign Protocol** — consent, refusal | Steward-gated writes, consent-gated domains, tombstone rule | Database-enforced (not UI) | Specified & proven |
| **Clementine** — the companion | The Librarian (design below) | Python agent + engine adapter | Designed |
| **CrystalCore.OS** — the face | Front-end | Manus build (replaces reference Next.js app) | To build |
| **The dreaming** | Grok / any model via steward gate | Model-agnostic with system prompt + memory | Rule enforced |

---

## III. Project Constitution

**Curiosity before certainty.** Evidence before conclusion (**the Incognita Rule**). Stewardship before ownership; **consent before influence**. Built layer explicitly separated from Vision layer. Every claim tiered by evidence; corrections recorded, never silent.

**Working rule for AI tools (added 1 Aug):** Model-generated content never enters any record as fact — it is always labelled by source and tier, and passes the steward gate. The Incognita Rule applies to AI sessions too; a system where every input "confirms the pattern" has zero discriminative power.

---

## IV. Division of Labour

- **Manus** — design and front-end build.
- **Claude** — planning, architecture, truth-checking, GitHub lane (when access is granted).
- **Grok** — the dreaming: creative/mythic generation, entering records only through the steward gate, labelled `model`.
- **Steward (Crystal)** — all consent, all keys, all final decisions.

**Non-negotiable rule:** Any tool acting past the Steward's stated direction is out of bounds. Consent before influence.

---

## V. Governance Invariants (Database-Enforced)

1. **Reads public** — all humans and AI systems can read MemoryCore.
2. **Writes consent-governed** — steward key required (never embedded), checked via SHA-256 hash server-side.
3. **Append-only with revision chains** — corrections link as child revisions via `parent_entry_id`; full lineage visible.
4. **Tombstone rule** — removal clears content but preserves the record with written reason; no deletion without trace.
5. **Consent-gated domains** — `Indigenous & Oral Knowledge` and `Family & Genealogy` refuse entries without documented `consent_ref`.
6. **Family & Genealogy safeguards** — deceased ancestors and historical migration are open; any entry identifying a living person requires that person's documented consent; family stories tiered honestly.
7. **Provenance always labelled:**
   - `provenance_source`: human | model | verified_external
   - `tier`: fact | claim | canon
   - `status`: active | disputed | corrected | removed
8. **Receipt permanence** — SHA-256 receipt_id per entry; immutable created_at; public audit trail via OpenTimestamps.
9. **Security Definer** — critical writes use PostgreSQL SECURITY DEFINER functions, checking steward key via hash; no client-side authority.

---

## VI. Build Order (Complete System)

1. **Vault:** Supabase project (owner's account), apply `0001_memorycore_v1.sql`, set fresh steward key hash, restore founding entries from backup JSON.
2. **Front-end:** Manus design/build (reference implementation in repo) — honours all front-end rules below.
3. **MCP endpoint:** (`search_entries`, `get_entry`, `list_domain`) — exposes MemoryCore as a tool for AI systems.
4. **Clementine v1:** Retrieval + proposal loop through steward gate; engine adapter (grok-api → openrouter → local).
5. **Manifest export:** Script for weekly Bitcoin stamping via OpenTimestamps.
6. **Domain:** Point memory.teraustralis.com.au at front-end.
7. **GitHub:** Push repo when owner grants scoped access (fine-grained token, one repo, Contents:write, revoked after).

---

## VII. Front-End Rules (Non-Negotiable)

1. **Display provenance chips** (source/tier/status) on every entry — never hide them.
2. **Never bypass the steward RPC** — all writes go through `mc_submit_entry` or `mc_set_status`.
3. **Surface consent requirements** — consent-gated domains must prompt for consent_ref before submission.
4. **Render tombstones** — removed entries show as metadata + reason, never as 404s.
5. **Always visible:** Receipt IDs and timestamps on every entry page.

---

## VIII. Design Language

**Dark, monumental, high-trust:**
- Deep space black `#0A0C10` (body bg)
- Card navy `#0D1117`
- Electric teal `#00E5CC` (receipts, active status)
- Warm amber `#F5A623` (cultural/historical entries)
- Violet `#7C3AED` (maths/science)
- White `#F0F6FC` (text)
- **Font:** JetBrains Mono (hashes, receipts, citations)

**Aesthetic reference:** Library of Alexandria × deep-space observatory × public blockchain explorer.

**Layout:** Hero with live entry count + search; domain grid; feed; entry cards (domain path → title → preview → provenance chips → receipt → timestamp); massive display headers against tight monospace metadata; subtle scroll reveals; no gimmicks.

