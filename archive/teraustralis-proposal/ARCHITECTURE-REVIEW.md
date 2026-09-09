# Architecture Review — teraustralis-proposal

**Belt: docs-governance.** This is a review, not a pitch document. It is not
part of the numbered document architecture and is not intended to be
forwarded to a partner as-is.

**Reviewer:** Independent pass (no prior review artifact existed for this
repository at the time of writing).
**Date:** 26 August 2026.
**Scope:** repository structure, the numbered/unnumbered document convention,
Belt-Three labelling discipline, claims discipline for outward-facing
material, and the locked-name / Indigenous-knowledge boundary, applied
against this project's own stated conventions.

---

## Summary

This repository is materially more disciplined than its own governing
convention gives it credit for: the "numbered vs unnumbered" risk the project
flags for this repo does not show up here as unmarked legacy content —
every unnumbered file in the repo is explicitly cross-referenced and labelled
in `README.md`, and the Indigenous-knowledge boundary around Songlines is
actively enforced (including against the project's own generated art) rather
than merely asserted. The real findings are narrower: the README's document
index has not kept pace with the live site (Documents 16–21 exist, are
dated, cross-linked, and reachable from the numbered spine, but appear
nowhere in the README table), the Belt-Three self-labelling habit visible in
Documents 09–21 was not retrofitted onto the founding Documents 01–08, and
one load-bearing factual claim in the SpaceX one-pager is unsourced where
every neighbouring claim in the same document is dated and cited.

## Strengths

- **The Songline boundary is enforced, not just stated.** Documents 20 and 21
  don't merely repeat the rule — they apply it against the project's own
  material. Document 21 rejects the project's own generated "Starline Atlas"
  plates for using the word "Dreamlines" and for a wrong globe, and explicitly
  refuses to publish them until corrected (`21-ATLAS.md` §4, §2.2 "Unpublished
  (fail §4)"). Document 20 goes further than simple non-use: it un-compresses
  two previously conflated sources (Turner 2014 vs. a separate Bursill
  conversation reported in Fuller 2020) specifically so a thinner, correctly
  attributed claim survives rather than a stronger, wrong one
  (`20-COUNTRY.md` §2.4). This is the claims-discipline convention
  ("a narrowed claim that survives scrutiny beats a broad one that dies on
  contact") applied to the hardest material in the repo, not just the easy
  commercial claims.
- **Prior-art / self-correction culture is real.** `GEO-BRIEF-ENGINEER.md` §5
  and `08-SPACEX-XAI-ONE-PAGER.md` both flag and correct the author's own
  earlier public error (DARC placed in the Pilbara in a May 2026 op-ed;
  corrected to Exmouth, ~700 km away, with sources). `09-SOUTHERN-NODE-ROADMAP.md`
  records the same correction and dates it. Errors are corrected in place
  and dated rather than quietly edited, matching the project's own
  `docs/governance` practice described in `ABOUT.md`.
- **No unnumbered doc masquerades as canonical.** Every unnumbered file in
  the repo — `15-REVIEW-PACK.md`, `GEO-BRIEF-ENGINEER.md`,
  `EVALUATION-LICENSE.md`, `ABOUT.md`, `sydney-station.html` — is listed in
  `README.md`'s Document Architecture table with an explicit note on why it
  isn't numbered. `15-REVIEW-PACK.md` opens by saying "This is **not**
  document 15"; `GEO-BRIEF-ENGINEER.md` opens "This is not document 06."
  The root-level `catch.html` is a clean, working redirect stub to
  `16-catch.html`, not a stale duplicate. `prototypes.html` is a dated
  withdrawal notice with a working redirect and a stubbed `prototypes.js`
  (`/* Withdrawn 20 August 2026. Browser toys removed. */`) — no dead
  legacy artifact was left behind.
- **Status labelling by site, not by project.** `09-SOUTHERN-NODE-ROADMAP.md`
  grades each candidate site independently (Active / Future scope /
  Speculative) specifically "so each one is judged on its own status, rather
  than borrowing credibility from — or lending risk to — the others," and
  explicitly states the Robotics/Land-Care concept stays unnamed because
  "if pursued at all, this has to be a concept Traditional Owners lead or
  decline on their own terms."
- **Every page naming a third party disclaims partnership.** `job.html`,
  `orbital.html`, `21-ATLAS.md` (re: Gilmour Space Technologies), and the
  `08`/`15` documents all carry explicit "not a partnership / not an
  endorsement / not a contract" language wherever SpaceX, Tesla, xAI,
  Telstra, or Gilmour are named.
- **Locked names hold.** No occurrence of "TerAustralis Incognita",
  "CrystalVision", or "CrystalCore.Lattice" in this repository redefines the
  term, and "Songline"/"songline" is used only as a citation of others'
  knowledge or law (e.g. "no site selection … proceeds over an identified
  sacred site or songline path without FPIC," `16-CATCH.md` §5,
  `06-GEOGRAPHIC-BRIEF.md`), never as a component or technical name.

## Findings

### 1. [High] README's Document Architecture table omits Documents 16–21 entirely

`README.md`'s table stops at Document 14, then lists only dash-marked items
(`15-REVIEW-PACK.md`, `sydney-station.html`, `GEO-BRIEF-ENGINEER.md`,
`EVALUATION-LICENSE.md`, `ABOUT.md`, `LICENSE`). Documents 16 (`16-CATCH.md`),
17 (`17-GATE.md`), 18 (`18-CICH.md`), 19 (`19-SIT.md`), 20 (`20-COUNTRY.md`),
and 21 (`21-ATLAS.md`) do not appear anywhere in `README.md`, nor in
`ABOUT.md`, `LICENSE`, or `NOTICE`. A repo-wide search for `16-`, `17-`, `18-`,
`19-`, `20-`, `21-` across every canonical `.md` file (01 through 15) returns
no hits — none of the "canonical" documents cross-reference this second
block at all.

This isn't a dead branch: it's the live site's actual front door. `index.html`
features `16-catch.html` as the first entry-flow item ("01 · Catch"), the
site's persistent top nav links `16-catch.html` and `job.html` on every page
including all fourteen numbered documents, and the doc-nav footer on
`14-multi-node-brief.html` reads `← What Is Built` / `16 Catch →` — i.e. the
site's own designed reading path treats 01→02→…→14→16→17→18→19→20→21 as one
continuous sequence. Anyone reading the repo from GitHub via `README.md` (the
project's own stated source of truth for "which documents are canonical")
gets a different, truncated picture of the proposal than anyone reading the
live site gets.

**Recommendation:** Extend the README's Document Architecture table (or add
a clearly-separated second table) to list Documents 15–21 with their actual
status lines, so the GitHub-facing index matches the site's designed reading
path. If 16–21 are deliberately meant to sit outside the formal index (their
own headers mark 18–21 "not a homepage item," though 16 and 17 carry no such
disclaimer and one *is* the homepage item), that reasoning should be written
down in README rather than left implicit.

### 2. [Medium] Belt-Three self-labelling was not retrofitted onto Documents 01–08

Documents 09 through 21 consistently open with an explicit status/belt line
(`09-SOUTHERN-NODE-ROADMAP.md`: "**Status: Active proposal focus…**";
`12-FULL-STACK.md`: "**Status:** operating…proposed…"; `16-CATCH.md` through
`21-ATLAS.md`: a "Status:" line under the title naming the document's belt
and what it is not) and 10–12 close with an explicit disclaimer ("*Framework
document — vision and structure, honestly labelled…design intent…no partner
has agreed to them.*").

Documents `01-PROBLEMS.md`, `02-FIRST-PRINCIPLES.md`, `04-PROPOSAL.md`,
`05-TECHNICAL-BRIEF.md`, and `07-INVESTMENT-THESIS.md` carry no belt or
status marking anywhere — not in a header, not in a footer. `03-VISION.md`
is wall-to-wall Vision-belt material ("A single-planet species is a single
point of failure for everything consciousness has become," "Consciousness is
the payload") with no self-declaring label at all, unlike every
Vision-labelled document from 09 onward. A reader who opens
`03-VISION.md` directly on GitHub (a very likely path, since it's a top-level
file) gets none of the "this is designed, not built" framing the project's
own Incognita Rule requires; they get only the README table's one-line gloss,
several clicks upstream.

**Recommendation:** Add a one-line belt/status header to 01–08 mirroring the
convention already adopted from 09 onward — at minimum on `03-VISION.md`,
which is the single most exposed pure-Vision document in the set.

### 3. [Medium] One load-bearing, unsourced claim sits inside an otherwise meticulously-cited document

`08-SPACEX-XAI-ONE-PAGER.md` opens: *"Structural note: SpaceX acquired xAI in
February 2026; as of July 2026, xAI operates as SpaceXAI, a SpaceX
subsidiary (Grok keeps its own name)."* This sentence carries no citation.
Every other factual claim in the same document is dated and sourced with a
URL — the lithium share (USGS, cited), the DARC location and MoU date
(Nautilus Institute / Space Connect, cited), the Varda landing (PRNewswire /
Australian Space Agency, cited), the TSA entry into force (space.gov.au,
cited), even the SpaceX Nasdaq debut. The acquisition claim is used to
justify reframing the entire document's audience and argument ("This is no
longer a two-company pitch"), which makes it more load-bearing than most of
the claims around it, not less.

This reviewer's knowledge cutoff (January 2026) predates the claimed
February 2026 event, so this review cannot independently confirm or refute
it — that is itself worth surfacing rather than silently assuming either
way, per the project's own honesty law.

**Recommendation:** Add a dated source for the SpaceX/xAI structural claim
before this document is next sent externally, matching the sourcing standard
the rest of the document already holds itself to. If no public source exists
yet, downgrade the framing to state it as reported/expected rather than
settled fact.

### 4. [Fixed in this commit] Rights footer inconsistently present across canonical documents

Per the project's own writing convention ("Documents carry the rights
footer") and this repo's README (explicitly stricter than the rest of the
portfolio because it is "the live, outward-facing pitch document set,
actively shared with external partners"):

- `01-PROBLEMS.md`, `02-FIRST-PRINCIPLES.md`, and `03-VISION.md` carry no
  ownership or rights marking anywhere in the file body.
- `16-CATCH.md` through `20-COUNTRY.md` each carry "ABN 70 741 068 059" in
  their header status block, but none restate "All rights reserved" (or any
  rights language) anywhere in the body.
- `21-ATLAS.md` carries neither an ABN nor any rights language anywhere in
  the file.

By contrast, `04-PROPOSAL.md`, `05-TECHNICAL-BRIEF.md`, `06-GEOGRAPHIC-BRIEF.md`,
`07-INVESTMENT-THESIS.md`, `08-SPACEX-XAI-ONE-PAGER.md`, `09-SOUTHERN-NODE-ROADMAP.md`,
`13-WHAT-IS-BUILT.md`, and `14-MULTI-NODE-BRIEF.md` all close with the full
"**All rights reserved.** / TerAustralis Incognita — ABN 70 741 068 059"
block. This is low severity — the repo-root `LICENSE` governs the whole
package regardless of any single file's footer — but worth aligning given
that individual documents in this set (08, `GEO-BRIEF-ENGINEER.md`) are
explicitly written to be read and forwarded as standalone artefacts.

**Fixed:** Added the standard "**All rights reserved.** / TerAustralis
Incognita — ABN 70 741 068 059" footer to `01-PROBLEMS.md`,
`02-FIRST-PRINCIPLES.md`, `03-VISION.md`, and `21-ATLAS.md` in this commit.
`16-CATCH.md` through `20-COUNTRY.md` were left untouched — they already
carry the ABN, and fully restating the rights sentence across five more
files is a smaller-priority consistency pass left for the maintainer rather
than folded into this fix.

### 5. [Fixed in this commit] Spelling inconsistency

`README.md` used "status-labeled" (American, single L) — the only American
spelling found across the entire corpus against 63 instances of British
"labelled" elsewhere in the repo (verified by grep). Corrected to
"status-labelled" in this commit. No other American-spelling variants
(colonize, specialize, utilize, prioritize, optimize, analyzed, summarize,
finalize, centralize, organize, realize) were found in the `.md` corpus.
"Behavior Tree" (`05-TECHNICAL-BRIEF.md`) is intentionally left as-is — it is
the standard name of the architecture pattern in the field, and the
project's own `teraustralis` skill uses the same American spelling for the
same term ("Prefer Behavior Trees over Finite State Machines").

## Open questions for a human / architect

- Should Documents 16–21 be formally folded into the README's Document
  Architecture table (perhaps as a "Sitting" or post-review tier), or are
  they intentionally meant to stay outside that index? If intentional, what
  is the reasoning — worth writing down somewhere it can be found again.
- Is the "SpaceX acquired xAI" (February 2026) claim in
  `08-SPACEX-XAI-ONE-PAGER.md` confirmed and publicly sourceable as of the
  date this proposal is actually sent? This review cannot verify it.
- Do `01-PROBLEMS.md` through `07-INVESTMENT-THESIS.md` need explicit
  Belt/Status headers to match the convention `09-SOUTHERN-NODE-ROADMAP.md`
  onward has already adopted, or is the README table's own one-line gloss
  considered sufficient labelling for the founding documents? This is an
  editorial call about the founding documents' voice, not a mechanical fix,
  and deliberately not made in this review.
- Are `job.html`, `ambition.html`, and `orbital.html` intended to eventually
  receive document numbers and join the numbered spine, or are they meant to
  stay a permanent unnumbered "current-affairs" track running alongside it?
  The answer affects how future contributors should decide what gets a
  number.

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059
