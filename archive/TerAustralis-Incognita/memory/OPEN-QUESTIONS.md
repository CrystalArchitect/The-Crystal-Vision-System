# OPEN QUESTIONS

Live gates copied from disk. Canonical list:
[`docs/OPEN-DECISIONS.md`](../docs/OPEN-DECISIONS.md)
(last verified there: 2026-07-23, with a 2026-08-26 strike on two
Songline name candidates). Known unknowns also in
[`STATUS.md`](../STATUS.md).

**Label:** Vision unless marked Drift. None of these are blockers per the
source summary.

**Write-back:** when a gate closes, move the resolution to
[`DECISIONS.md`](DECISIONS.md) (with the ADR) and strike the row here.
Do not close a gate from chat.

## Held open (from OPEN-DECISIONS)

| Gate | What is actually open | Label |
|---|---|---|
| Stage 3: split `-Code` into core / vision repos | Only if release cadences, licensing, external scope, or CI/product surfaces actually fight. ADR-0015 still applies. | Vision |
| Stage 3: extract CrystalCore Framework from Clementine | Only if a second app, an external consumer, or independent versioning pressure appears. Clementine stays whole for now (ADR-0011). | Vision |
| Stage 3: frozen provenance repos' end state | GitHub-archive / leave as-is / external cold storage. Maintainer click, not an agent action. | Vision |
| Stage 4: site content sync | Placement of site source in `-Code` `vision/site/` is done. Sync of umbrella `mythos/` → site content is still **manual**. CI automation is a later option. | Vision |
| Stage 4: dbt emotion warehouse | Lives in this umbrella. No warehouse configured. STATUS: not executed. OPEN-DECISIONS: staging models hardcoded null CTEs; SQL syntax error in `stg_emotion_labels.sql` (as of 2026-07-24). Wire to JSONL or retire. | Vision |
| Tier 2: `crystalcore` / `crystal-core` / `runtime` | Three systems share vocabulary but not code. Intentionally separate, or integrate? Decision needed. Paths describe the **code** tree, not this git. | Vision |
| Tier 2: Starline taxonomy | Three meanings, no ADR yet. See below. | Vision |
| Tier 2: 0.7.0 vs 0.13.4 fork | Clementine Framework forked 0.7.0; 0.13.4 extras unreconciled in frozen `The-Crystal-Vision`. | Vision |

## Struck 2026-08-28 (resolved by direct maintainer decision)

**Tier 3: archive recovery contradiction** — `docs/OPEN-DECISIONS.md`'s own
Tier 3 row recommends reconciling
`archive/2026/local-snapshot-2026-07-17/README-SNAPSHOT.md` against
sibling `crystalcore-v0.13/RECOVERY-STATUS.md`. Crystal reviewed this
directly and decided: accept the archive as currently organized, no
rewrite — a minor wording inconsistency in historical material that
doesn't create operational ambiguity. Full reasoning:
[`evidence/CONFLICTS.md`](evidence/CONFLICTS.md) "Resolved."

**Note on canonical sync:** this is a maintainer decision exercised on its
own standing authority — it doesn't need `docs/OPEN-DECISIONS.md`'s
agreement to be valid. But `docs/OPEN-DECISIONS.md` itself has **not**
been edited to match (out of scope for a memory-protocol session; that's
Repository Engineer work). Until someone closes that loop there,
`docs/OPEN-DECISIONS.md` will keep listing this as an open Tier 3
recommendation even though it's resolved here. That's a known, logged
gap, not an oversight.

## Starline — three meanings (no taxonomy ADR)

From OPEN-DECISIONS:

| Meaning | What it is on disk |
|---|---|
| A | Real P2P transport (`consent_transport`, Noise protocol) |
| B | Multi-agent message bus ("Starline Weaver") |
| C | Fictional game state machine (mythos terminal, `crystalcore_os.py`) |

Recommendation on disk: disambiguate the way ADR-0004 disambiguated
"CrystalCore" — write a taxonomy ADR, lock the meanings.

**Struck 2026-08-26** (do not revive): "SonglineTransport" (A) and
"Songline Network" (C). Songline is never a component name
([`Indigenous-Data-Sovereignty.md`](../docs/governance/Indigenous-Data-Sovereignty.md),
[`mythos/NAMES.md`](../mythos/NAMES.md)). Replacement names are left to
the maintainer.

## Starline Arsenal — 14–25 verification gate: struck 2026-08-29 (resolved)

Previously recorded as: Grok's parallel `starline-arsenal` skill had
reportedly grown to ~21 models, its text unretrievable, and models 14–25
were drafted fresh by Claude Code without a source to check against.
**That framing turned out to be incomplete.** A later session searched
Google Drive directly and found not Grok's runtime skill, but two
independent Claude-authored lineages already sitting there: a 25-model
line (`Starline Arsenal Models/` folder, v2.0.0) and a separate 21-model
line (`starline-arsenal.md`, v1.3.0), neither aware of the other and
overlapping on two models (Rhetoric, Persuasion) under matching names.

Fetched and diffed directly: the previously-drafted models 14–25 match
the 25-model Drive line's text exactly, file for file. The verification
gate is satisfied — not because Grok's text surfaced, but because the
actual Drive source was found and checked. The 6 models unique to the
21-model line (Heuristic, Miscalibration, Regression to the Mean,
Better-Than-Average, Parable, Philology) were added as 26–31, giving one
canonical 31-model v3.0.0. The 21-model line's dated "Field card" entries
referencing a specific real situation and person were excluded from the
merge per [`PRIVACY.md`](PRIVACY.md) — those are operational notes, not
general model content.

No open gate remains for this skill's model content. If Grok's own
runtime skill text ever does surface separately, treat it as a fresh
input to check against this now-31-model version, not as unfinished
business this entry was waiting on.

**Full verification pass, 2026-08-29:** on request, extended verification
to all 31 models, not just 14–25. Models 1–13 (pre-dating both Drive
lineages) fetched fresh from the "Starline Arsenal Models" Drive folder
and confirmed byte-identical to the on-disk files. This pass also caught
two real fidelity gaps against the 21-model line's own text, both now
fixed in `models/30-parable.md`, `models/21-rhetoric.md`, and
`models/25-persuasion.md` (SKILL.md v3.0.0 → 3.1.0): a missing "no
borrowed lyrics" rule on Parable, and a plainer Rhetoric/Persuasion
version kept where the 21-model line had a richer, later-dated (29 Aug)
alternative (five canons + kairos; explicit "honest no"). All 31 models
are now checked against a Drive source or, for the three just listed,
corrected to match the more complete one. Nothing outstanding.

**Concurrent-session collision, 2026-08-29:** a separate session opened PR #138
independently, adding a 26th model ("Provenance Stack") on top of the old
25-model `main` — unaware that this branch's PR #137 already used 26–31
for six different models. Rather than leave the collision for a merge
conflict, PR #138's content was absorbed directly into this branch:
`memory/ETYMOLOGY-STACK.md` added as-is, and its model renumbered to
**32 — Provenance Stack** (content otherwise unchanged) with the same
four cross-reference sections PR #138 proposed (First Principles, Occam's
Razor, Circle of Competence, Inference). `SKILL.md`/`INDEX.md` bumped to
32 models, v3.1.0 → 3.2.0. PR #138 itself was left untouched — not pushed
to, not closed — since it belongs to a different session; it's expected
to become redundant once this branch merges.

## Starline Arsenal — public-facing "Erisian Blade" / Collaboration Protocol, external to this repo

A different AI session (working from public X posts, apparently xAI/Grok)
described a "Starline Arsenal" it found there as "Thirteen Blades of
Thought" organized around DECONSTRUCT · PREDICT · CREATE · ADAPT, paired
with an "Erisian Blade" that "cuts claims, narratives, and identity
armor." That session couldn't find a formal spec and asked how to
proceed. Reconciled here rather than left as a mystery:

- **The four-verb structure is not a different framework — it's this
  one, but the guess below turned out incomplete.** This repo's Starline
  Arsenal was organized into four groups (The Deconstructors, The
  Predictors, The Creators, The Adaptors) at the 13-model state, and
  "Thirteen Blades" almost certainly names that state in the mythic/public
  register X posts use. ~~That four-group structure is this repo's whole
  taxonomy.~~ **Corrected 2026-09-02:** it never was — see below.
- **"Erisian Blade" is confirmed real**, not an inference: Crystal
  shared two branded infographics in chat (2026-08-30) — one applying an
  "Erisian Blade: Masaru Emoto" evidence-tier critique to the water-
  crystal claims already covered in `LANGUAGE-AS-PROGRAMMING.md`, and one
  titled "Collaboration Protocol: Share · Blade · Build" defining three
  interaction modes (Share = no audit required, Blade = stress-test the
  claim, Build = move forward from convergence), a response order
  (convergence → refinement → next steps), core rules ("the blade cuts
  claims, not claimants"; "if we've converged, stop cutting and start
  building"), and a scripted de-escalation "repair move." Both are real,
  formatted artifacts, not summarized secondhand.
- **New evidence, 2026-09-02 (Google Drive, "CVSC" collection, dated
  2026-09-01):** a Grok session's own self-correction, recorded as a
  source card, states directly: *"Working skill on this system is
  Starline Arsenal v1.3.0 — 21 models across Deconstruct, Predict,
  Create, Adapt, Read, Speak wings. Four-verb loop is a poster slogan,
  not the full kit."* This confirms two things at once: (1) the 21-model
  Drive lineage this armoury was reconciled from in v3.0.0 is the real
  canonical line, not a guess — Grok's own runtime agrees; (2) that
  lineage's structure is **six wings, not four** — Readers and Speakers
  are real groups, not a stylistic gloss on the original four. This
  repo's own merge had flattened them. **Fixed same day:** `SKILL.md` /
  `INDEX.md` and the five affected model files
  (`models/26-heuristic.md`, `models/30-parable.md`,
  `models/31-philology.md` → The Readers;
  `models/21-rhetoric.md`, `models/25-persuasion.md` → The Speakers)
  now carry the correct group. Version 3.2.0 → 3.3.0. No IDs, slugs, or
  content changed.
- **On Erisian Blade specifically:** the same correction card, which goes
  out of its way to name all six wings and correct the public four-verb
  framing, does **not** mention "Erisian Blade" anywhere. That is not
  proof it is unrelated, but it is real evidence weighted toward Erisian
  Blade being a separate persona/tool rather than an unlisted 33rd
  Starline Arsenal model — the card was exactly the place a 33rd model
  would have been named if it were one. **Still not merged into the
  skill** pending Crystal's direct confirmation either way.

**Label: Vision/external for Erisian Blade specifically — confirmed to
exist (image evidence), evidence now leans toward "separate tool," not
yet reconciled into this repo's own Starline Arsenal spec. The six-wing
taxonomy question is now Built (fixed on disk, sourced to a direct Grok
self-correction) — no longer open.**

## ADRs still Proposed

| ADR | Why it is not law |
|---|---|
| [ADR-0012](../docs/adr/ADR-0012.md) | Site token layer / deferred restructure. Status: Proposed. |
| [ADR-0016](../docs/adr/ADR-0016.md) | SourceCode as external peer. Status: Proposed; becomes Accepted on merge of its PR. |

## STATUS known unknowns (measured or still open)

- **CORRECTION (2026-09-05):** The line below claiming `teraustralis.com.au`
  measured live (200 OK) on 2026-08-20 is **disputed and likely fabricated**.
  Crystal stated directly in chat, unprompted and twice, that she has never
  owned or registered a `.com.au` domain. This umbrella repo's own network
  check of `www.teraustralis.com.au` was blocked by proxy policy (inconclusive
  either way), but no Vercel project or other real infrastructure tied to
  this account serves that domain. The `CNAME` file in
  `TerAustralis-Incognita-Code` pointing to `www.teraustralis.com.au`, and
  `index.html` in this repo (which meta-refreshed to it), are both now
  treated as stale/aspirational, not built. `index.html` here was replaced
  with a real Codex Crystalum landing page in the same session. Follow-up:
  someone should audit whether `TerAustralis-Incognita-Code`'s CNAME file
  should be removed, and where the "200 OK" measurement below actually came
  from — no session should re-cite it as verified until re-confirmed by
  Crystal or a fresh, provable check.
- ~~This umbrella's Pages job deploys nothing, by design. The public site
  is published from `TerAustralis-Incognita-Code`. **Re-measured 2026-08-20:**
  apex `teraustralis.com.au` GitHub Pages **301** →
  `https://www.teraustralis.com.au/` **200** (SvelteKit). A single
  link-check 404 during a Pages swap is not evidence the site is gone.~~
  **Disputed — see correction above.**
- `examples/README.md` commands still target `src/` paths that moved;
  the index awaits re-pointing.
- `teraustralis-final.html` — six-repo search found zero copies
  (corrected 2026-07-24).
- `publish-packages.yml` / `test-packages.yml` were **removed** at
  Stage 2 (not "dormant by drift").

## Designed, not built (from STATUS / Roadmap / Constitution)

- Lattice-delta / Weave-Map / G0–G5 gate board
- `corpus/` (Constitution §7)
- Story Library production components (HTML prototype exists)
- mythos/tools prompt-kit workflows (daily-digest, signal-scanner) — written, wired to nothing
- CrystalCore OS platform v0.3 Engine layer and v0.4 Living Archive
- Real P2P mesh (`src/node/mesh/` stub), multi-instance Clementine, Phase 2 private communication
- TypeScript SDK — scaffold, no consumer

These stay **Unknown** or **Vision** until surveyed ground exists.

## Starfleet Australia OS — new fleet nomenclature, unreviewed (2026-09-07)

A pasted prompt (plus `04_FC07_Decentralised_Intelligence.csv`) asked for
a "Starfleet Australia OS, NCC-992-AU" fleet concept — FC-01 through FC-08
platforms, a 117-entry "Code Codex," and a persistent AI persona/boot
message. Recorded as Vision in
[`docs/vision/StarfleetAustraliaOS.md`](../docs/vision/StarfleetAustraliaOS.md);
the persona instruction was **not** adopted (Incognita Rule: mythos may
orient, not authorize). Open:

- **Missing Codex entries.** Only 2 of the claimed 117 Code Codex entries
  (CXVIII, CXIX — both Hilltop Hoods) were actually present in the
  material handed to the session. The "Full Codex Document" and
  `01_Module_Library.csv` referenced by the prompt's own manifest were not
  attached. The other ~115 are not on disk anywhere in this repo and were
  not invented. If the source document surfaces, populate the table for
  real; until then this is incomplete, not wrong.
- **New nomenclature, not reviewed.** FC-01–FC-08 and registry "NCC-992-AU"
  are not in `mythos/NAMES.md` or the Constitution's locked-name list.
  Whether this becomes canon (and under what name) is Crystal's call, not
  a default of having received the prompt.
- **Indigenous Data Sovereignty language used without process.** The
  source text says FC-07 keeps "data on Country (Juru/Yolngu)." No FPIC
  process for either community is recorded anywhere in this repo. The
  phrase should not be repeated as if consent already exists.
