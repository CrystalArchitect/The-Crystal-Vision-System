# The Library

**Licence:** All rights reserved — see [LICENSE](LICENSE).

The shared reading room of the TerAustralis Incognita / CrystalCore
constellation: whole documents, accessioned with their provenance on the
cover, kept where every strand of the project — and every AI session
working on it — can find them.

The shelves hold **documents**: the umbrella repository
(`TerAustralis-Incognita`) holds canon and law; the Archive
(`CrystalCore.OS-the-Crystal-Architecture-Archive`) holds the
evidence-reconstructed knowledge base and the governing repository map; the
Library is where consolidated plans, reviews, frameworks and records are
shelved whole, so they stop living only in chat threads and upload folders.
`app/` holds the one piece of software that belongs here: The Library's own
front door — Clementine's Study and Rex's Post.

By the steward's decision of 2026-08-05: **The Library is the public
face; MemoryCore stays the vault name** — the archive people and AIs
visit is The Library, and MemoryCore is the canonical store beneath it
(the master plan §6 question, answered; recorded in the sync record's
A.9).

## Shelves

| Shelf | Holds |
|---|---|
| [`frameworks/`](frameworks/) | Operating tools — provisional Method, kept falsifiable |
| [`plans/`](plans/) | Consolidated plans and hand-off documents |
| [`reviews/`](reviews/) | Reviews of the constellation, by humans or models |
| [`records/`](records/) | The Library's own ledger — accessions and sync records |
| [`notes/`](notes/) | Working notes and session logs, kept as provenance |
| [`transmissions/`](transmissions/) | Starline Transmissions — the project's recorded works, stored as ordinary git blobs (steward's decision, A.13) |
| [`gallery/`](gallery/) | Artworks — catalogued in [`gallery/CATALOGUE.md`](gallery/CATALOGUE.md), which scales where this table should not |
| [`index/`](index/) | The curated index outward — external citations, in [`index/CATALOGUE.md`](index/CATALOGUE.md) |
| [`app/`](app/) | The Library's interface — two rooms, two implementations |

## Catalogue

| Holding | Document date | Source | Label |
|---|---|---|---|
| [`frameworks/loop-framework.md`](frameworks/loop-framework.md) | 2026-08-04 (committed) | human (steward) | Method — provisional and revisable by its own §8; every element deliberately falsifiable |
| [`plans/2026-08-01-teraustralis-master-plan.md`](plans/2026-08-01-teraustralis-master-plan.md) | 2026-08-01 | steward-supplied consolidation (model-assisted) | Docs-governance — a plan and decision record; individual lines span surveyed fact and Vision and are tiered by their own wording |
| [`reviews/2026-07-29-crystal-ecosystem-full-repository-review.md`](reviews/2026-07-29-crystal-ecosystem-full-repository-review.md) | 2026-07-29 | model (Manus AI) | Claim — accurate to its date; partly overtaken by later renamings, see the sync record |
| [`records/2026-08-05-library-sync.md`](records/2026-08-05-library-sync.md) | 2026-08-05 | model (Claude, session record) | Docs-governance — accession and survey record, amended by accretion the same day |
| [`reviews/2026-07-28-aeris-vault12-exploration-report.md`](reviews/2026-07-28-aeris-vault12-exploration-report.md) | 2026-07-28 | model (Manus AI) | Claim — the AERIS site as deployed; part of that build's only durable provenance here |
| [`notes/aeris-mini-os-notes-and-assets.md`](notes/aeris-mini-os-notes-and-assets.md) | c. 2026-07-28 (inferred) | human + model (Manus session note) | Docs-governance — working spec; asset paths are Manus-side |
| [`notes/aeris-build-task-log.md`](notes/aeris-build-task-log.md) | late July 2026 (inferred) | human + model (Manus task log) | Claim — completions asserted by the log, not re-verified here |
| [`transmissions/red-dust-axis.mp3`](transmissions/red-dust-axis.mp3) | undated ID3 (no title frames found) | human (steward upload) — a canon Starline Transmission | Work (audio, 5.2 MB, 64 kbps stereo) — **licensing unverified**: master plan flags Suno tracks after 6 June 2026 as non-commercial-only until subscription status is confirmed |
| [`.claude/skills/taskmarket/`](.claude/skills/taskmarket/SKILL.md) | 2026-08-05 (skill version 2026-07-20) | verified external (Daydreams Systems), steward-redistributed — see [NOTICE](NOTICE) | Tooling, active for AI sessions in this repository — an on-chain USDC marketplace operator whose own safety contract governs money-moving actions; installing it created no wallet and touched no funds (A.11) |
| [`app/python/`](app/python/) | 2026-08-05 | human (steward upload), verbatim | Code as received — FastAPI + xai-sdk, two presences; **not executed in this session**; review notes in the sync record's addendum; `static/chat.html` not yet supplied |
| [`app/next/`](app/next/) | 2026-08-05 | human (steward upload), verbatim | Next.js 14 project taking shape across deliveries: shell + App Router pages (layout, home, entry card, global styles — the archive face, implementing the master plan §5 design language token-for-token). Still missing: `lib/` (supabase, grok), `scripts/check-key.js`, and the search/browse/entry/steward/api routes |
| [`reviews/2026-08-26-the-library-architecture-review.md`](reviews/2026-08-26-the-library-architecture-review.md) | 2026-08-26 | model (Claude, independent architecture review) | Claim — a fresh review of this repository itself (not derived from a prior Grok review); one small, safe fix applied alongside it (`app/python/main.py` CORS credentials) |

## Accession rules

Every holding gets an **accession plate** at the top of its file — or, where
a document predates the shelves and is left byte-identical (the Loop
Framework), a catalogue row here instead. The plate says when the document
entered, where it came from (`human` / `model` / `verified_external`), and
which layer it sits on (Science / Vision / Docs-governance — the Incognita
Rule as practised across the constellation: always mark which lines are
dreamed and which are surveyed). Below the plate's rule, the text is
**verbatim as received** — the Library does not edit its holdings.

Corrections happen **by accretion**: a new record in `records/`, a new
catalogue row, never a silent overwrite. Removal, if it ever happens, leaves
a tombstone row with a written reason.

Model-generated content never enters as fact. It is labelled by source and
tier, and it passes the steward gate: a pull request that only the steward
merges. This README came through that gate too.

## Open items

- ~~Whether The Library is the public face of the MemoryCore design~~ —
  **decided by the steward, 2026-08-05**: The Library is the public face;
  MemoryCore stays the vault name (sync record A.9).
- ~~This repository carries no `LICENSE` file~~ — **decided by the
  steward, 2026-08-05**: All rights reserved, in the constellation's
  existing wording — see [LICENSE](LICENSE) (sync record A.10).
- ~~A third-party `taskmarket` skill held at the gate~~ — **cleared by
  the steward, 2026-08-05**: repository named and redistribution rights
  confirmed, so it is installed at `.claude/skills/taskmarket/` with its
  attribution in [NOTICE](NOTICE) (sync record A.7 → A.11).

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059
