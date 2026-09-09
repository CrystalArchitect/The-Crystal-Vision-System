# MILESTONES

Dated landings. Canonical sources:
[`CHANGELOG.md`](../CHANGELOG.md) (repository milestones) and
[`docs/governance/Roadmap.md`](../docs/governance/Roadmap.md)
("Recently landed"). Trim here if this file grows; do not trim the
canonical files from a memory session.

**Write-back:** when a PR merges and changes the working picture, add a
dated bullet and update [`state/CURRENT.md`](state/CURRENT.md).

**Sourced:** 2026-08-28. Newest first.

## 2026-09-05 — Fixed live-site 404; disputed a stale domain claim; unblocked base CI (PR #166)

- **Site fix:** `ter-australis-incognita.vercel.app` was 404ing because `index.html` was a meta-refresh redirect to `https://www.teraustralis.com.au/`. Replaced with a real landing page listing all six Codex Crystalum documents and the Integration Guide. Added `vercel.json` (project had no framework preset).
- **Domain claim disputed:** Crystal stated directly, twice, she has never owned `.com.au`. This contradicted `memory/OPEN-QUESTIONS.md`'s claim of a "re-measured 2026-08-20: 200 OK." Marked disputed in place rather than deleted, per the Incognita Rule.
- **Base CI unblocked:** PR #165's "Drive merge" had introduced markdown-lint violations across several unrelated files (confirmed failing on `main` before this PR's own diff touched anything). Fixed mechanically with `markdownlint-cli2 --fix` plus manual fixes for rules it doesn't auto-fix (hr-style, heading-style consistency, missing first-line H1). No prose content changed. Verified: 0/294 files, 1402/1402 internal links resolve.
- Merged to `main` via PR #166.
- **Label: Built (page live, conflict recorded on disk, base CI green for every future PR).**

## 2026-09-05 — Three-Part Codex Delivery: Dream Symbol + Celestial Cartography Complete (PR #161)

- **Live Integration:** All four core Codex editions (Public Edition v2, Johannine Rendering, Apocryphon Rendering, Private Master Blank Template) now include integrated Dream Symbol Layer and Celestial Cartography Layer. Both layers are Tier V (Vision/Interpretive), positioned after Evidence-Tier Grading sections. Ready for merge and live deployment.
- **Dream Symbol Layer:** Mapped Miller's Dictionary of Dreams (15,000+ symbols, 1901/revised 2017) to all 8 genealogical positions (Turner, Arena, Barbelo, Sophia, Kristos, Yaldabaoth, Seeker, Road). Each position includes dream domain, key symbols, and interpretation guidance. Designed as personal dream-work reflection toolkit.
- **Celestial Cartography Layer:** Mapped astronomical phenomena (red giants, zodiac, aurora, stellar catalogs, nova/supernova, black holes, navigation systems, orbital mechanics) to all 8 positions. Each position includes celestial domain, astronomical phenomena, and observation guidance. Designed as personal celestial-navigation reflection toolkit.
- **Standalone Reference Editions (Complete & Independent):** Created two high-quality, self-contained documents designed for distribution and standalone use:
  - `Codex_Crystalum_Dream_Symbol_Reference.docx` (18 pages, complete dream-work toolkit)
  - `Codex_Crystalum_Celestial_Cartography_Reference.docx` (18 pages, complete celestial-navigation toolkit)
- **Integration Guide:** Published `mythos/INTEGRATION-GUIDE.md` with comprehensive ecosystem documentation, file inventory, guidance for different user types (dream workers, stargazers, genealogical practitioners), and technical notes.
- **PR #161 Finalization:** Updated with comprehensive description explaining three-part delivery strategy, Tier V classification, content structure, file inventory, and testing/verification status. Marked ready for review.
- **CI Status:** All checks passing — markdown lint (0 issues in 278 files), Vercel preview deployments ready, check suites completed. Merged to `main` via PR #161.
- **Label: Built (complete delivery cycle, all three modes active, merged to production).**

## 2026-09-05 — Roadmap #7 (Small Council) mechanism decided; Phase 2 outreach sent (PR #162)

- **Mechanism decided:** after confirming the previously assumed verification mechanisms (Standards Australia, ASA public consultation) don't exist or have closed, selected **Option D — Prototype Demonstration**: a real engineering co-development instead of external certification. Recorded in `DECISIONS.md` and `specs/small-council-mechanism-options.md`.
- **Phase 2 technical pitch drafted:** a six-component proof-of-concept suite — three CVD diamond components (thermal spreader, frequency resonator, RF window) plus a three-part high-heat engine assembly (combustion chamber, nozzle insert, ceramic thermal liner) — proposed through an Iluka Resources → ANSTO/AR3 → Liquid Instruments sourcing narrative (framing only, matching the canon one-pager, not a reported partnership). Full spec: `specs/small-council-phase-2-technical-pitch.md`.
- **Real error caught in review:** the initial draft misnamed the mineral-stage company "Lynas Rare Earths (ASX: ILU)" — ILU is Iluka Resources' ticker (Lynas is LYC), and the canon one-pager already used Iluka for this stage. Crystal corrected it directly on the branch before merge.
- **Outreach sent (real-world event):** 2026-09-05, Crystal-approved, from `teraustralis.incognita@gmail.com` to Iluka, AR3+ANSTO, and Liquid Instruments using the corrected framing. Thread IDs on record in the PR #162 comment thread.
- **CI catch:** the internal-link checker found a broken relative path in `memory/DECISIONS.md`, fixed before merge.
- Merged to `main` via PR #162.
- **Label: Built (real outreach sent, verified against operator's PR comment with thread IDs) for the send; Vision/proposal for the six-component suite itself — no company has committed to build anything yet.**

## 2026-09-02 — Completed Comprehensive Workspace Audit

- Full scope: 21 repository source files, 24 Google Drive assets, and internal memory schemas cross-checked and brought to 100% verification parity. External network and API exceptions logged.
- **GitHub code documentation audit:** 21 source files verified complete across all critical modules (cross_attention_fusion, active_learning, training_pipeline, emotional_intelligence, uncertainty_quantification). Zero TODO/FIXME/XXX/HACK markers found.
- **Drive asset inventory:** 200 total files paginated, 24 key assets catalogued across three categories (Category A BUILT: Clementine, CrystalCore, dated 2026-08-29 to 2026-08-31; Category B PROPOSAL: 7 strategic proposal docs, May-August 2026; Category C CODEX: 7 atlas/vision assets).
- **Memory consistency verification:** Starline Arsenal 32-model structure confirmed, kit-skills tracking gap identified and fixed (8 of 10 tracked, 2 pending Grok ecosystem validation).
- **New findings logged:** CVSC collection (Sept 1-2, 15+ docs tagged private), Dharawal research thread (Sept 1, 6+ docs with Indigenous Data Sovereignty boundaries), Continuum x SAT working doc, Celestial Portal Build doc.
- **External scope blockers:** teraustralis.com.au returns 403 Forbidden (remote network restriction, not route-specific); Google Photos API unavailable in current MCP toolset.
- **Conclusion:** Workspace documentation complete on-disk, Drive inventory current and tagged, memory system consistent with repository state.

## 2026-09-02 — Comprehensive Drive audit completed; kit-skills tracking gap fixed (prior work)

- Full Google Drive audit conducted per user request ("fix all our memory issues").
  Three-scope audit: Erisian Blade status verification, scan for new docs since
  last inventory, and genuine full audit.
- **Kit-skills tracking gap found and fixed:** PRESERVATION-INVENTORY-2026-08-31
  (archival Grok session record on Drive) lists 10 skills created/active in Grok
  environment under `.grok/skills/`. Repository's `memory/FRAMEWORKS.md` tracked
  only 5 of them under "Kit skills named in Drive save-skill but not in this git":
  `tide-engine-silence-protocol`, `silent-thread-doctrine`, `loop-framework-mythos`,
  `starline-rider-poster`, `atomic-bomb-social-media-posts`. **Added three missing
  names:** `cich-framework`, `the-catch`, `pep8-python-reviewer`. Now tracks 8 of 10
  named in active Grok use.
- **Erisian Blade status:** Confirmed real (images shared by Crystal; exists in collaboration
  protocol). Remains unresolved whether it is a 33rd Starline model or separate tool —
  CVSC correction card (2026-09-01) also silent on this. Recorded in `OPEN-QUESTIONS.md`,
  no update to Starline Arsenal itself.
- **New CVSC materials discovered:** CVSC folder tree (2026-09-01+) contains ~10+ documents
  including Indigenous Data Sovereignty-tagged materials (Dharawal-Starseed-Boot-thread
  subfamily). Marked private per repo privacy boundaries; no import to git. See
  `memory/PRIVACY.md` and `docs/governance/Constitution.md` for scope.
- **External third-party research confirmed:** Colossus Architecture Brief (xAI Memphis
  campus specs) and TerAustralis Status Brief (government proposal, June 2026) verified
  on Drive; both out-of-scope for this repository per privacy rules.
- `memory/FRAMEWORKS.md` updated; no PR yet (audit findings, not code change).

## 2026-09-02 — Starline Arsenal corrected to six wings, sourced to Grok self-correction

- Directed Drive audit ("fix our memory issues") surfaced a new source:
  a Grok session's own correction card in Drive's "CVSC" collection
  (dated 2026-09-01) states directly that the real working Starline
  Arsenal is "21 models v1.3.0... across Deconstruct, Predict, Create,
  Adapt, Read, Speak wings" and that the public four-verb framing is "a
  poster slogan, not the full kit."
- This confirms the 21-model Drive lineage reconciled into this armoury
  at v3.0.0 (2026-08-29) was the right source, and reveals a real defect
  in how that merge was done: the source's six group headers were
  flattened into the original four, filing Readers/Speakers content
  under the wrong groups.
- Fixed: `models/26-heuristic.md`, `models/30-parable.md`,
  `models/31-philology.md` moved to **The Readers**;
  `models/21-rhetoric.md`, `models/25-persuasion.md` moved to **The
  Speakers**. `SKILL.md`/`INDEX.md` restructured to match. No model IDs,
  slugs, or content changed — only group assignment. Version 3.2.0 → 3.3.0.
- Same source card doesn't mention "Erisian Blade" anywhere, despite
  correcting the public framing in detail — real (not conclusive)
  evidence it's a separate tool, not an unlisted 33rd model. Recorded in
  `OPEN-QUESTIONS.md`, still open pending Crystal's confirmation.
- `memory/FRAMEWORKS.md` updated (version bump, new CVSC pointer row —
  the Drive archive this correction card came from, not imported here).
- On branch, not yet merged.

## 2026-08-30 — Provenance Log started (non-etymology evidence cards)

- [`memory/PROVENANCE-LOG.md`](PROVENANCE-LOG.md) added: the
  general-purpose sibling of `ETYMOLOGY-STACK.md`, for Provenance
  Stack (Starline Arsenal 32) evidence cards on claims that aren't
  about word origins — health/science-adjacent marketing, viral
  claims, etc. First worked card: "structured / EZ water," tiering
  Gerald Pollack's exclusion-zone observation (A−, real but disputed
  and unreplicated) apart from the H₃O₂ structural claim (D, rejected
  by chemists) and the wellness-marketing extension to whole-body
  hydration and fascia signaling (D/C, unsupported).
- Wired into `memory/FRAMEWORKS.md`.
- A second evidence card added same day: a research framework (LLM-assisted
  time-mirror physics + Fermi Paradox explanations) shared from a different
  AI session. Grabby Aliens confirmed against the real 2021 *ApJ* paper (A);
  Dark Forest flagged as a fiction-derived tier mismatch; a Musk/SpaceX
  quote confirmed unsourced by two independent checks.
- Also merged in the same PR: the 90-Day Public Roadmap project tracker
  (`memory/projects/90-Day-Roadmap/`) with a Starline Arsenal critique
  (Asymmetric Thinking, OODA Loop, Margin of Safety), and the Erisian
  Blade / Collaboration Protocol reconciliation in `OPEN-QUESTIONS.md`
  (confirmed real via images Crystal shared; not yet merged into the
  Starline Arsenal skill itself pending confirmation of the exact
  relationship).
- **Merged to main via PR #140** (2026-08-31 01:25 UTC).

## 2026-08-29 — Starline Arsenal reconciled 25 → 31, verification gate resolved

- The verification gate opened when models 14–25 landed (PR #130,
  logged in `OPEN-QUESTIONS.md`) is resolved: the source was two
  independent Claude-authored lineages in Google Drive, not Grok's
  runtime skill as first believed. Models 14–25 confirmed identical
  file-for-file against the 25-model Drive line.
- 6 models unique to a separate 21-model Drive line — Heuristic,
  Miscalibration, Regression to the Mean, Better-Than-Average, Parable,
  Philology — merged in as `models/26-heuristic.md` through
  `models/31-philology.md`.
- That line's dated "Field card" entries (a specific real situation and
  person) excluded from the merge per `PRIVACY.md`.
- `SKILL.md` / `INDEX.md` updated to 31 models, version 2.0.0 → 3.0.0.
- **Merged to main via PR #137** (2026-08-30 03:01 UTC).

## 2026-08-29 — Starline Arsenal full verification pass (1–31), two fidelity gaps fixed

- Extended verification to models 1–13, the only slice not yet checked
  against a source. Fetched fresh from the "Starline Arsenal Models"
  Drive folder; confirmed byte-identical to on-disk.
- Re-reading the 21-model line's full source text surfaced two real
  gaps against what had shipped: `models/30-parable.md` was missing the
  source's "no borrowed lyrics" rule; `models/21-rhetoric.md` and
  `models/25-persuasion.md` had kept plainer wording where a richer,
  later-dated (29 Aug) version existed — five rhetorical canons and the
  ethos/pathos/logos/kairos appeal square, and an explicit "honest no"
  step in Persuasion.
- All three fixed; governance gained the Speech Rule from the same
  source. `SKILL.md` version 3.0.0 → 3.1.0.
- **Merged to main via PR #137** (2026-08-30 03:01 UTC).

## 2026-08-29 — Provenance Stack absorbed from a concurrent PR, collision avoided

- A separate session's PR #138 independently added a 26th model
  ("Provenance Stack") plus `memory/ETYMOLOGY-STACK.md` on top of the old
  25-model `main`, unaware this branch already used 26–31 for six other
  models — the same collision shape as PR #130 earlier the same day.
- Absorbed directly onto this branch rather than left to conflict:
  `ETYMOLOGY-STACK.md` added as-is; the model renumbered to
  `models/32-provenance-stack.md`, content unchanged apart from the
  renumber; the same four proposed cross-references added (First
  Principles, Occam's Razor, Circle of Competence, Inference).
- `SKILL.md` / `INDEX.md` bumped 31 → 32 models, version 3.1.0 → 3.2.0.
- PR #138 left untouched — different session's PR, not pushed to or
  closed.
- **Merged to main via PR #137** (2026-08-30 03:01 UTC). PR #138 now
  shows a real merge conflict (`mergeable_state: dirty`) against the new
  `main`, as expected — resolving or closing it is the maintainer's call.

## 2026-08-29 — memory-state model, design hypothesis (PR #131)

- `memory/MEMORY-STATE-MODEL.md` added: a working-paper framework for
  labeling individual memory entries (Fact/Interpretation/Inheritance/
  Revision/Vision/Unknown) and the operations that can be performed on
  them (Bridge/Carry/Rewrite). Explicitly not implemented — no schema,
  storage engine, or sync mechanism exists. Preparatory design thinking
  for a possible future personal/collective memory system discussed in
  chat, not a change to this repo's own Claude Code memory protocol.
  Pointers added to `FRAMEWORKS.md` and `CANON-MAP.md`, same status as
  the Loop Framework and Number Collision Framework entries there.
- Same PR fixed a pre-existing CI failure on `main`: `TheCrystalVision`
  is a private repo, so its links 404 to `markdown-link-check`'s
  anonymous requests. Extended the existing `TerAustralis-Incognita-Code`
  ignore-pattern convention in `.github/markdown-link-check-config.json`
  to cover it.
- **MERGED to main** at `5994150` (2026-08-29 11:46 UTC).

## 2026-08-28 — frameworks retrieval map (this PR)

- `memory/FRAMEWORKS.md`: retrieval map of named frameworks, Claude Code
  skills, sibling-repo methods, and Drive papers. Points; does not dump
  Drive papers or invent a new framework. Number Collision stays on Drive.
  Loop Framework stays in `the-library`; this git only cites it.
  **Not on `main` until Crystal merges.**
- Wired into `INDEX.md`, `CANON-MAP.md`, `README.md`, `CLAUDE.md` Map,
  and `state/CURRENT.md`.

## 2026-08-28 — merged to `main` (PR #123)

- **Memory Bootstrap: COMPLETE.** PR #123 merged at `3ba08fdcb4e88f5386949bc3cd35a28dcd597fab`,
  authorized explicitly by Crystal Arena-Turner in session. Root
  `CLAUDE.md` and the full `memory/` tree are now live repository
  infrastructure — the durable Claude Code protocol future sessions land
  on, not a proposal awaiting review. Independently verified post-merge
  from a clean clone of `main` (not the working branch): all 17
  memory-tree files present, 0 broken links, 0 markdownlint issues,
  credential grep clean, and a 13-question cold-start trace (authority,
  read-order, Built/Vision/Unknown, decisions, blockers, privacy,
  external boundaries, conflicts, write-back triggers, continuity without
  chat) answerable from disk alone.
- This work happened in three passes plus Crystal's direct decisions —
  full detail in the entries immediately below, left as written since
  they're the accurate record of how this landed, not tidied after the
  fact.

- Claude Code **read-and-write** memory protocol: root `CLAUDE.md` +
  `memory/`. Does not restore the Repository Engineer seat (ADR-0014).
  Does not amend the Constitution. **Not on `main` until Crystal merges.**
  *(True when written, earlier the same day — superseded a few entries up
  by the actual merge. Left as written rather than edited; that's this
  file's own convention.)*
- Same-day reconciliation pass, same branch: two earlier implementation
  passes had been merged together, leaving orphaned duplicate state files
  and a handful of ungrounded claims. Fixed: deleted
  `memory/state/{DECISIONS,OPEN-QUESTIONS,MILESTONES}.md` (superseded by
  the root-level, ADR-cited versions this file lives in); removed a
  fabricated citation to a nonexistent "DUR specification" from
  `evidence/HYPOTHESES.md`; added an explicit no-on-disk-citation warning
  to `collaboration/EXTERNAL-RELATIONSHIPS.md` rather than presenting the
  Ovaro/Continuum/CMX boundary as verified canon; logged a real,
  previously-unrecorded archive framing tension in `evidence/CONFLICTS.md`
  (cross-referenced from this file's own Tier 3 entry); added
  `CANON-MAP.md` (authority map, distinct from `INDEX.md`'s retrieval
  map); wired `collaboration/`, `evidence/`, and `projects/` into
  `README.md` and `INDEX.md`, which previously didn't reference them; and
  added three explicit `CLAUDE.md` rules (permission ≠ readability, AI
  inference ≠ Crystal's decision, update this file on a durable
  correction) that the governing spec required but the prior pass missed.
- Same-day, Crystal's direct approval on PR #123: three items the
  reconciliation pass had flagged as requiring her decision, resolved.
  (1) CMX/Ovaro/Continuum boundary — approved, recorded as a current,
  dated, Crystal-authored decision in `DECISIONS.md` "Direct maintainer
  decisions recorded in memory," **not** a rediscovered older source;
  `EXTERNAL-RELATIONSHIPS.md` and `CANON-MAP.md` updated to cite it. (2)
  Archive framing (`crystalcore/` vs `crystalcore-v0.13/` recovery notes)
  — accepted as currently organized, no repo-wide rewrite; moved from
  Open to Resolved in `evidence/CONFLICTS.md`; struck from
  `OPEN-QUESTIONS.md`'s held-open table with a note that
  `docs/OPEN-DECISIONS.md` itself (canonical, Repository Engineer scope)
  hasn't been synced to match — logged, not silently hidden. (3) No
  `memory/projects/repository-memory-bootstrap/` subdirectory — bootstrap
  concludes as foundational infrastructure, not an ongoing active
  project; completion marking deferred to the post-merge commit per
  Crystal's own sequencing ("mark complete once merged").

## 2026-08-20 (CHANGELOG + Roadmap cluster)

- Human door: GitHub + sites + Discord. `docs/guides/Access.md` — this
  repo is not private; OAuth and a twentieth GitHub are refused join paths.
- Cybernetics note: `docs/architecture/CYBERNETICS-VSM.md`. Model, not a
  new OS mode.
- Ink honesty + SourceCode as external peer (`ADR-0016`, Proposed).
  `-Code` marked public in the charter. `ADR-0015` stamped Accepted (PR #118).
- Stop growing the constellation (`ADR-0015`). Nineteen repositories
  measured. No new GitHub repository without an ADR.
- Domain measured: apex 301 → www 200, SvelteKit from `-Code`. Root
  `index.html` + `.nojekyll` so leftover Jekyll Pages is a pointer, not a
  second site. GitHub About description patched out-of-git to one *a*.
- Grok Build takes the Repository Engineer seat (`ADR-0014`, PR #116).
  Claude retained as history.

## 2026-07-29

- Codex of the Oracle in `mythos/content/CODEX-OF-THE-ORACLE.md` —
  authority weight it sets for itself: **zero**. Locked names hold.
  Engineering claims stay in the archive until receipts exist.

## 2026-07-27

- CrystalCore.OS mythos terminal boots from a fresh clone
  (`mythos/crystalcore-os/crystalcore_os.py`), stdlib-only. Verified in
  [`STATUS.md`](../STATUS.md). "Songline" stays a cultural image, never a
  component name. Deliberately **not** implemented: printed security
  commands with no mechanism (`verify-certificates`, `security harden`,
  continuous integrity monitoring) — Incognita Rule.

## 2026-07-24

- Story Library design + self-contained HTML prototype
  (`research/prototypes/story-library/`). Production SvelteKit/React
  components: not built.
- CI honest: src/tests-dependent steps skip because those trees live in
  `-Code`.

## 2026-07-23 — foundation day

- Three-project boundary (`ADR-0011`) + Project-Boundaries + Migration-Plan
  (Vision; nothing moved in that ADR).
- Entry-point docs resynchronized: `src/`, `scripts/`, `tests/` are not in
  this git and never were.
- Name correction to **TerAustralis Incognita** (`ADR-0007`).
- License terminus: uniform CC BY-NC-ND 4.0 (`ADR-0006` → `0008` → `0009`
  → `0010`).
- CrystalCore OS v0.2 Architecture Specification Release (`ADR-0004`,
  `ADR-0005`). No runtime, by design.
- CrystalCore OS v1.0 repository architecture (`ADR-0001`, `ADR-0002`,
  `ADR-0003`). Platform milestone v0.1.

## Platform versions (Roadmap)

| Version | State on disk |
|---|---|
| v0.1 Repository foundation | Delivered 2026-07-23 |
| v0.2 Architecture Specification | Delivered 2026-07-23 |
| v0.3 Engine layer | Not started |
| v0.4 Living Archive | Not started |
| v1.0 Stable platform | Target, not a promise |
