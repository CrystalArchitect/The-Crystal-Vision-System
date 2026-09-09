# Corrections

Every documentation correction this reconstruction made or identified,
in two sections: applied directly to the source file, and identified
but left for a future pass.

## Part 20 — Applied 2026-08-08 (the count in Part 19 was itself wrong)

### "Eleven" was measured with a tool that under-reports

- **`02-REPOSITORY-MAP.md`, `00-INDEX.md`, `README.md`, and Part 19 below**
  — before: "eleven repositories," corrected hours earlier the same day
  from "twelve." After: **seventeen**, of which six are archived and
  eleven live; six are public.
- **The method was the defect, not the arithmetic.** Part 19's count came
  from a GitHub *search* query. The same query, run again the same
  evening, returned eighteen. Seven of the extra rows were not new
  repositories: five had existed since June and July and were simply not
  returned the first time. GitHub's search index is eventually consistent
  and can under-report; it is not an enumeration of an account.
- **What this archive should have done, and now says plainly:** the
  authoritative list of an account's repositories is the account's own
  repositories page, not a search result. No count in this knowledge base
  should be sourced from a search query again.
- **Why it is recorded rather than quietly fixed.** Part 19 opens by
  observing that this archive caught a real loss because a document
  disagreed with reality. Within hours the same document asserted a
  number the world did not match, from a tool that had already been
  trusted too far. Both halves belong in the record; a ledger that logs
  only the catches and not the misses is advertising, not a ledger.

### The portfolio as measured 2026-08-08, late

Seventeen repositories. Six archived and private: `CrystalCore`,
`CrystalCore-AERIS`, `CrystalCore.OS-Aeris-Vault12`,
`CrystalCore.OS-APP`, `CrystalcoreOS`, `TerAustralis-Incognita-`.
Eleven live, of which six are public — `TerAustralis-Incognita`,
`TerAustralis-Incognita-Code`, this archive, `teraustralis-proposal`,
`CrystalCore.OS`, and `Clementine---Local-Soveriegn-Edge-AGI` — and five
private: `TheCrystalVision`, `CrystalCore-Starlines-and-Dreamlines`,
`teraustralis-incognita-v2`, `teraustralis-v2-presentation`,
`the-library`. One repository, an empty `express-js-on-vercel` scaffold,
was deleted the same evening.

This count carries the caveat above: it was taken with the same class of
tool that already proved unreliable once. It is recorded as a
measurement with a known-weak instrument, not as a certainty.

### A licence claim that had not been carried out

- **`TerAustralis-Incognita/docs/adr/ADR-0013.md`** — accepted
  2026-07-28, titled "retire Apache-2.0 and the unlicensed
  repositories," and describing the risk in its own words: a reader who
  finds Apache-2.0 "concludes they may fork."
- That retirement was incomplete for eleven days. `TerAustralis-Incognita-`
  — a repository-creation artifact holding one line of README and a full
  Apache-2.0 licence, its name one character from the umbrella's — stayed
  **public** until 2026-08-08, when it was made private and archived.
  `CrystalCore.OS-APP` (MIT) and `CrystalcoreOS` (AGPL-3.0), both from
  the differentiated model ADR-0010 rejected, likewise survived until
  they were archived and made private the same evening.
- As of this entry no public repository carries a licence other than
  CC BY-NC-ND 4.0. GitHub reports those repositories as `NOASSERTION`,
  which is its licence detector failing to recognise a Creative Commons
  licence, not a missing one.
- The ADR's stated outcome is now true. It became true on 2026-08-08,
  not on 2026-07-28, and the eleven days between are the finding.

## Part 19 — Applied 2026-08-08 (two repositories deleted)

### The portfolio holds eleven, not twelve — and this archive found it

- **`knowledge-base/02-REPOSITORY-MAP.md`, `00-INDEX.md`, `README.md`** —
  before: "all twelve repositories" in the present tense. After: eleven,
  with a dated scope correction at the head of the map.
  `CrystalCore-AERIS` and `CrystalCore.OS-Aeris-Vault12` were deleted from
  the account in the week before 2026-08-08.
- **How it was found.** Not by a backup check or a failing test. A routine
  cross-check before publishing this archive listed eleven repositories
  where the map claimed twelve. The disagreement between this document and
  the account was the only signal there was — which is the clearest
  argument for this archive existing that it has yet produced.
- **What followed.** Both repositories were restored from GitHub's 90-day
  window at the maintainer's direction the same day, their contents
  rescued verbatim into
  `TerAustralis-Incognita/archive/2026/rescued-2026-08-08/`, and then
  deleted again. Twenty-six files recovered; fourteen existed in no other
  repository, verified by hashing every rescued file against every file in
  all eleven surviving ones.

### This archive's account of vault12 was incomplete, and briefly the only one

- **`knowledge-base/02-REPOSITORY-MAP.md`** — recorded
  `CrystalCore.OS-Aeris-Vault12` as ten tracked files holding seven
  specifications. It held **twenty**, including seven documents this
  archive never recorded: `ETHICAL-RUNTIME-SPEC.md`,
  `THEURGY-AELTHARION-BRIDGE.md`, `ORDINALS-COLLECTION.md`, four documents
  under `docs/`, and a 372-line `southern-node-lfa-operational-log.md` —
  the largest single document in the repository.
- The entry's own Historical Notes already flagged that it was written
  from a stale clone. That flag was correct, and its cost is now
  measurable: for nine days this incomplete account was the only surviving
  record of the repository. Had the restore window closed first, seven
  documents would have been lost without this archive ever knowing they
  existed.
- **Left standing, not corrected:** the per-file detail of those entries.
  Rewriting them from the rescued copy would make this archive a
  description of the rescue rather than a record of what it knew and when.
  The rescue folder holds the material; this correction records the gap.

## Part 0 — Applied 2026-07-28 (portfolio review pass)

### The archive covered 6 of 11 repositories

- **`knowledge-base/02-REPOSITORY-MAP.md` and `00-INDEX.md`** — before:
  "all six repositories" / "the six-repository CrystalArchitect
  portfolio." After: eleven. `CrystalCore.OS`, `CrystalCore-AERIS`,
  `crystalcore-os-aeris-vault12`, `teraustralis-incognita-v2`, and
  `teraustralis-v2-presentation` were absent from the map entirely.

  This is only partly an omission. Four of the five did not exist when
  the reconstruction ran on 2026-07-24 — the three terminal repos were
  created 2026-07-29 (+1000) and `teraustralis-v2-presentation` on
  2026-07-28. The genuine miss is `teraustralis-incognita-v2`, created
  2026-07-24 14:14 UTC, which existed on the day and was not surveyed.

  The original six-repository statements were left standing and the new
  material added as its own Statement, so that what the archive asserted
  on 2026-07-24 remains readable as a claim about 2026-07-24. Correcting
  by accretion rather than by overwrite is the same discipline
  `10-PROVENANCE.md` applies to everything else here.

- **Standing risk this exposes.** The ledger has no trigger that fires
  when a repository is created. It was re-run only because a review
  happened to be commissioned. Whatever replaces that — a scheduled
  re-survey, or a rule that a new repository is not real until the map
  names it — is an open decision, recorded here rather than resolved.

### `02-REPOSITORY-MAP.md` — vault12 described from a stale clone

- Before: `crystalcore-os-aeris-vault12` listed as "`index.html`,
  `logo.jpg`, and a README", and grouped with `CrystalCore.OS` and
  `CrystalCore-AERIS` as one of "the three single-page terminal
  repositories ... variants of one another." After: recorded as the
  **specification home for Starline edge nodes and the Consent Token**,
  carrying seven technical documents.

  The clone this was measured from was taken at 20:45 UTC; the seven
  specifications landed on that repository's `main` afterwards
  (head `a09943c`). So the archive described a specification repository
  as a web page — a claim outliving the evidence it was drawn from,
  which is the precise failure this archive exists to prevent.

  Corrected in place with the error left visible and the re-read dated,
  rather than rewritten to look as though it had always been right.

- **Added, not merely corrected:** a Statement comparing the vault12
  specification against the running `consent_transport` implementation.
  They are the same protocol at the transport layer and diverge at the
  consent layer — Noise IK matches the spec exactly, while Consent
  Tokens, expiry, scope, and propagatable revocation are specified and
  not built. Filed on the maturity ladder accordingly.

- **Standing risk, same shape as the eleven-repository miss above.** Both
  errors have one cause: a clone read once and then trusted. Nothing in
  this archive's method re-read a source before a claim about it was
  published.

  **Addressed 2026-07-29.** [`SURVEYED.md`](../SURVEYED.md) now records
  the commit each repository's claims were read from, and
  `.github/scripts/check-freshness.py` reports which have moved since.
  Staleness deliberately does not fail: the portfolio moves faster than
  any survey of it, so being behind is the normal state. What is removed
  is the silence — the archive can be behind, but no longer invisibly,
  which is precisely how it came to describe a six-repository portfolio
  that had eleven.

### `README.md` (this repository)

- Before: 49 bytes — the repository name as an H1, no trailing newline,
  no content, in the repository that holds the portfolio's knowledge
  base and system ledger. After: a real front door pointing at
  `knowledge-base/00-INDEX.md`, `STATUS.md`, and the review reports.

## Part 1 — Applied this pass (2026-07-24)

Scope discipline: only small, mechanical, high-confidence corrections
of a factual claim against verified reality were applied directly —
matching "minimize documentation churn... prefer documentation fixes
over structural changes." Everything larger, riskier, code-behavior-
related, or requiring a judgment call is in Part 2 instead.

### `CrystalCore.OS-the-Crystal-Architecture-Archive/STATUS.md`

- **Archived-status claims (4 occurrences)** — before: "The-Crystal-
  Vision (archived 2026-07-18, read-only)," and equivalent phrasing for
  `crystalcore`, `crystal-vision`, and a fourth reference in the Built
  section. After: corrected to reflect that live GitHub metadata shows
  `archived:false` for all three, with the more accurate framing that
  whether to archive them is an open decision the umbrella's own
  charter records as undecided, not a settled fact.
- **`crystal-vision`'s "one true blank"** — before: "contents never
  audited by any ledger pass." After: resolved with a summary of this
  session's full audit (functional static demo, v0.5.1, Apache-2.0, no
  network calls, no secrets, two cosmetic defects).
- **`teraustralis-final.html`** — before: listed under "Running," with
  a "location unknown" note. After: removed from Running (a file
  confirmed absent everywhere no longer clears that section's bar);
  Known Unknowns updated to state it was searched for by filename,
  content, and git history across all six repositories and found
  nowhere — resolved absent, not merely unlocated.
- **Repo 3's CI claim** — before: "no CI." After: corrected to state
  `ci.yml` exists and runs on push; `deploy.yml` exists but GitHub
  Pages source hasn't been switched on yet (pending manual step).
- Added: a pointer line to `knowledge-base/00-INDEX.md`.

### `TerAustralis-Incognita/STATUS.md`

- **"Dormant by drift"** — before: "publish-packages.yml... and
  test-packages.yml... Dormant by drift rather than by decision." After:
  "not dormant, removed outright at Stage 2 (commit `60a20df`)... after
  confirming neither had ever had a git tag to fire on. Removal was a
  decision, not drift" — resolving a direct contradiction with the same
  repository's own `Migration-Plan.md`.
- **`teraustralis-final.html`** — before: "Presumed to live in an
  archived repo; unresolved this session." After: resolved absent,
  matching the system ledger's correction above.
- Added: a pointer line to the Archive repo's knowledge base.

### `TerAustralis-Incognita/docs/architecture/SystemMap.md`

- **The "Consequences" paragraph** — before: stated `ci.yml`/
  `deploy.yml` fail against absent paths and the CNAME points at an
  absent site — true when written (2026-07-23, 13:47 UTC), false within
  hours. After: rewritten to state Stage 2's resolution (same day),
  citing `Migration-Plan.md`, and to note what's still actually true
  (self-tests and demo commands remain unrunnable from a fresh clone,
  because `src/`/`tests/` are genuinely still not in this repository).
- **`starline` path reference** in the directory tree — before:
  `starline (P2P exchange)`. After: `consent_transport (P2P exchange;
  starline/ is a deprecated alias)`.

### `TerAustralis-Incognita/docs/governance/Roadmap.md`

- Added four missing dated entries to "Recently landed" — ADR-0006,
  ADR-0008, ADR-0009, ADR-0010 — matching what `CHANGELOG.md` already
  recorded in full but this page omitted entirely.

### `TerAustralis-Incognita/docs/README.md`

- Added a new "Root-level reference documents" section indexing the
  nine `docs/*.md` files that existed but were never listed
  (`ATTRIBUTIONS.md`, `DBT_WAREHOUSE_INTEGRATION.md`,
  `HUGGINGFACE_INTEGRATION.md`, `ADVANCED_UNCERTAINTY_METHODS.md`,
  `EMOTIONAL_INTELLIGENCE_BLUEPRINT.md`, `RESTRUCTURING_COMPLETE.md`,
  `FIRST_RELEASE.md`, `PUBLISHING.md`, `COMMERCIAL_LICENSING_GUIDE.md`)
  — a gap a prior architecture-survey session had already flagged and
  which remained unfixed until this pass.

### `TerAustralis-Incognita/docs/architecture/CrystalCore.md` and `docs/architecture/crystal-core/Runtime-Glossary.md`

- Same `starline/` → `consent_transport/` path correction as
  `SystemMap.md`, in both files.

### `TerAustralis-Incognita-Code/STATUS.md`

- **"No CI at all"** (Built section) — before: "this repo has no CI at
  all." After: corrected — both `ci.yml` and `deploy.yml` exist and
  run; the actual remaining gap (GitHub Pages source not switched on)
  stated precisely.
- **Lumina test-suite claim** — before: "Overclaim, or suites that
  never made the import? Unresolved." After: "Resolved 2026-07-24:
  confirmed overclaim — the other three suites do not exist anywhere in
  this repository." (`vision/README.md` itself deliberately left
  uncorrected — see Part 2.)
- **Second "No CI" claim** (Known unknowns) — same correction as above,
  cross-referenced.
- Added: a pointer line to the Archive repo's knowledge base.

### `TerAustralis-Incognita-Code/core/README.md`

- The component table's `crystal-core/` row listed "Starline P2P
  (`starline/`)" as a separate item from "Consent Transport
  (`consent_transport/`)" — collapsed into one accurate entry noting
  `starline/` is a deprecated alias, not a second component.

### `TerAustralis-Incognita-Code/core/crystal-core/SECURITY.md`

- Same `starline/` → `consent_transport/` correction.

### `TerAustralis-Incognita-Code/core/crystal-core/README.md`

- **Sibling-repository list** — before: named three repositories
  ("the-crystal-vision," "crystal-vision," "teraaustralis-incognita")
  that don't match current reality — none spelled or scoped like
  anything that exists today, and none mentioning this repository's own
  actual name. After: corrected against the umbrella's fresh
  "Repositories, today" section — all six current repositories named
  correctly, with CrystalBridge's actual location corrected (it lives
  in this repository, not the umbrella, as the original text implied).

### Four Code-repo module READMEs

`core/crystalcore/README.md` was not touched (its stale `src/apps/`
and `src/profiles/` references are code-comment-adjacent documentation
tightly coupled to `bridge.py`'s actual bug — see Part 2). The
following four each had their own stale, pre-split `src/apps/...` path
references corrected to the real current paths:
- `vision/apps/voicebox/README.md` — one path.
- `vision/apps/crystal-interface/README.md` — two paths (the `cd`
  instruction, and the relative path to the real pipeline).
- `vision/apps/vision-web/README.md` — four paths (the surface table,
  the `cd` instruction, and two entries in "Related").

---

## Part 2 — Identified, not applied

Each with a one-line reason it's left for a future, separate pass.

| Finding | File(s) | Why not applied here |
|---|---|---|
| `bridge.py`'s Lumina-path resolves to a nonexistent directory (`core/apps/` instead of `vision/apps/`); `recall`/`teach`/`message` crash at runtime | `TerAustralis-Incognita-Code/core/crystalcore/bridge.py` | Code-behavior fix, not a documentation fix — out of scope for a documentation-only reconstruction. **→ Since resolved, see Part 3.** |
| `gate.py`'s docstring claims four consent checks; only two (approval, permission) are implemented | Same file, `gate.py` | Same as above — fixing this "right" means either building the missing checks or downgrading a security claim, both real engineering decisions, not doc edits. **→ Since resolved, see Part 3.** |
| No requirements/toml/cfg file declares the `mcp` package `bridge.py` imports | `TerAustralis-Incognita-Code` (repo-wide) | Packaging/dependency fix, not documentation. **→ Since resolved, see Part 3.** |
| 96 files carry `SPDX-License-Identifier: Apache-2.0` headers under a CC BY-NC-ND 4.0 root `LICENSE` | `TerAustralis-Incognita-Code`, 96 files | Mechanically identical to a fix ADR-0009 already executed once — its own text records batch-correcting 97 `src/*` files to `CC-BY-NC-ND-4.0`, later relocated to `core/`+`vision/` by the repo split — but sized for its own dedicated, scripted pass, not folded into this session's line-edit budget. **→ Since resolved, see Part 4.** |
| ADR-0007 and ADR-0011's own "Consequences" sections describe states later resolved same-day | `docs/adr/ADR-0007.md`, `ADR-0011.md` | Protected by the project's own precedent: accepted ADRs are left as unedited historical record (explicitly stated for ADR-0001/0002 in `ADR-0007.md`'s own text). |
| The PR template's Belt-Three checkboxes don't match `CONTRIBUTING.md`'s canonical three-label table (merges Story+Vision, adds an undocumented fourth category) | `.github/PULL_REQUEST_TEMPLATE.md` | Process/template redesign, not a factual correction. **→ Since resolved, see Part 4.** |
| `docs/governance/Review-Process.md`'s CI checklist describes a Python-based CI (`compileall`, four self-tests, `pytest`) that no longer exists — actual `ci.yml` runs only markdown lint and a link check | `TerAustralis-Incognita/docs/governance/Review-Process.md` | Not in this pass's directly-scoped file list; flagged here for a future pass. **→ Since resolved, see Part 4.** |
| `CONTRIBUTING.md`'s "Reality note" says CI currently fails for path reasons — CI was retargeted, not left failing | `TerAustralis-Incognita/CONTRIBUTING.md` | Same as above. **→ Since resolved, see Part 4.** |
| `vision/README.md` itself still claims four Lumina test suites | `TerAustralis-Incognita-Code/vision/README.md` | STATUS.md now correctly flags this as a confirmed overclaim; the overclaiming file itself was deliberately left for a separate pass, stated explicitly in the STATUS.md correction. **→ Since resolved, see Part 3.** |
| `crystal-interface/README.md` and `vision-web/README.md` carry the same stale sibling-repository lists as `core/crystal-core/README.md` (only that one file was corrected) | Both files | Out of this pass's specifically-scoped correction list; same fix pattern, future pass. **→ Partially resolved, see Part 4 — re-verification found `vision-web/README.md` did not actually have this defect; this row was itself imprecise.** |
| `vision-web/README.md`'s "Related" section links `docs/architecture/Full-Stack-v0.5.md` — a path that doesn't exist locally in this repository (docs live in the umbrella) | Same file | A cross-repository reference-format question, not a simple prefix swap like the other paths in this file. **→ Since resolved, see Part 4.** |
| The Crystal Runtime specification trio disagrees with itself about implementation readiness across three documents | `Crystal-Runtime-Specification-v0.3.md`, `Runtime-Module-Interfaces.md`, `Runtime-Testing-Specifications.md` | A judgment call about which of three progressively-differing claims is "true" — not a mechanical correction; documented in `03-ARCHITECTURE.md` instead. |
| Whether PR #1 (Code repo) should be formally closed, and whether its orphaned `src/runtime/` is worth salvaging | `TerAustralis-Incognita-Code`, PR #1 | Not a documentation question at all — a maintainer decision. Recorded in `07-HISTORY.md`. |
| Whether `mythos/crystalcore-os`'s ~2,300 lines of ML code should be reclassified out of "Vision-layer" | `TerAustralis-Incognita/mythos/crystalcore-os/`, and everywhere it's described | A classification decision, not a factual correction — this archive preserves the project's own stated classification while flagging the tension (`05-KNOWLEDGE-MODEL.md`). |

---

## Part 3 — Applied after this archive's first publication (2026-07-24)

Four Part 2 items were resolved the same day this archive first
published, and their rows above are annotated accordingly. The Part 2
table itself is preserved unchanged as the record of what the first
pass deliberately declined to do and why — this section records what
happened next, with evidence, per `12-CONTRIBUTING.md`'s dated-note
convention.

- **`bridge.py`'s Lumina path — fixed.** PR #8
  (`TerAustralis-Incognita-Code`, merged 2026-07-24) recomputes
  `LUMINA_PKG_DIR` from the repo root into
  `vision/apps/lumina/crystalcore/`. `recall`/`teach`/`message` no
  longer crash. A regression guard in the new
  `core/crystalcore/selftest.py` fails loudly if the path ever stops
  resolving.
- **`gate.py`'s docstring — corrected.** Same PR. The resolution
  chosen was "make the docstring true": it now states the two checks
  `check()` actually implements (approval, tool-permission) and
  records, in the docstring itself, that scope/provenance were
  documented as intended but never implemented — no surviving spec
  defines either, so building them remains an open maintainer design
  task, not something this fix invented. The one other file asserting
  the four-check claim (`vision/site/src/content/ARCHITECTURE.md`,
  "Reality (Built)" table) was corrected in the same PR.
- **The `mcp` dependency — declared.** Same PR. New
  `core/crystalcore/requirements-bridge.txt` (the filename the
  module's own README already instructed users to install), matching
  the sibling `requirements-consenttransport.txt` convention. CI now
  installs it and runs the CrystalBridge selftest on every push.
- **`vision/README.md`'s four-test-suite overclaim — fixed, by the
  maintainer independently.** PR #7 (`TerAustralis-Incognita-Code`,
  commit `08fa2cc`, merged 2026-07-24, shortly before PR #8): the
  README now states the one real core suite and marks the other three
  as not-yet-existing. Attributed accurately — this was the
  maintainer's own pass, not this archive's session.

---

## Part 4 — Applied in this pass (2026-07-24, later still)

Six more Part 2 rows resolved, plus one new, unscoped discovery this
pass made and resolved: a second knowledge base found living in the
umbrella's `docs/`, colliding with this archive's own canonical claim.

- **The 96 (now 97 — see below) stale SPDX headers, `TerAustralis-
  Incognita-Code` — fixed.** Reapplied the exact fix ADR-0009 already
  documented once: `SPDX-License-Identifier: Apache-2.0` →
  `SPDX-License-Identifier: CC-BY-NC-ND-4.0`, changing only the
  identifier value, on every affected line, across all three comment
  styles present (`#`, `//`, `<!-- -->`). Verified 97 → 0 stale
  occurrences and spot-checked diffs across `.py`/`.js`/`.svelte` files
  to confirm nothing else in any file changed. The 97th file was this
  archive's own prior-session addition, `core/crystalcore/selftest.py`,
  which had copied the stale pattern from its siblings without
  question — caught and fixed in the same sweep, not exempted for
  being this session's own work.
  **Precision on the count:** ADR-0009's original 97-file batch was
  scoped to `src/apps/`, `src/crystal-core/`, `src/crystalcore/`,
  `src/crystalcore-os/`, `src/node/`, `src/sdk/`, `src/site/` — all
  relocated to `core/`+`vision/` by the Stage 1/Stage 2 repo split.
  The umbrella's own remaining straggler
  (`mythos/crystalcore-os/crystalcore_os.py`, also fixed this pass) was
  never part of that batch — a different path (`mythos/`, not
  `src/crystalcore-os/`) — so it is an independent, never-remediated
  instance of the same defect class, not "the one file ADR-0009
  missed."
- **PR template ↔ `CONTRIBUTING.md` Belt-Three mismatch — reconciled.**
  `.github/PULL_REQUEST_TEMPLATE.md`'s merged "Story / Vision" checkbox
  split into two, matching `CONTRIBUTING.md`'s three canonical rows
  exactly. `CONTRIBUTING.md`'s table gained a fourth row, "Docs /
  governance / process," matching what the template already treated as
  a real, distinct category in practice — repository reality (the
  template's actual use) overriding stale documentation (the table),
  the same principle this whole reconstruction applies elsewhere.
- **`docs/governance/Review-Process.md` and `CONTRIBUTING.md`'s stale
  CI descriptions — corrected.** Both described a Python-based CI
  (`compileall`, four self-tests, `pytest`) that no longer runs in the
  umbrella at all — confirmed directly: `TerAustralis-Incognita`'s own
  `ci.yml` runs markdown-lint and a link-check only. Both now state
  this plainly and point at `TerAustralis-Incognita-Code`'s own
  `ci.yml` for the actual Python suites (5 self-tests, 2 pytest suites),
  since Stage 1/2 moved that code there. The dead
  `scripts/maintenance/check.sh` reference (confirmed absent from the
  umbrella entirely) was dropped from both in the same edit.
- **`vision/apps/crystal-interface/README.md`'s sibling-repository
  list — corrected.** Matched to the accurate six-repo block already
  written into `core/crystal-core/README.md` in the original pass.
  **`vision-web/README.md` needed no change** — re-verification found
  it never carried this defect (it has no sibling-repo-identity block
  at all, only a small in-repo app-surface table; its own path
  references were already corrected in Part 1). Part 2's row grouping
  these two files together was itself imprecise on this point — noted
  there directly rather than silently fixing a file that wasn't
  broken, per this archive's own standard for correcting itself.
- **`vision-web/README.md`'s dead `Full-Stack-v0.5.md` link — fixed.**
  Confirmed the file exists, but only in the umbrella repo. Converted
  the same-repo-relative path to a working cross-repo GitHub URL,
  matching the pattern `core/README.md` already established for the
  same kind of reference.

### The competing knowledge base — discovered and reconciled

While scoping this pass, found that umbrella PRs #60/#61 (merged,
branch `claude/repo-structure-boundaries-xddagp` — a different,
uncoordinated session, not this one) had created **seven new files
directly under `TerAustralis-Incognita/docs/`**: `ARCHITECTURE.md`,
`GOVERNANCE.md`, `REPOSITORIES.md`, `TECHNICAL-FINDINGS.md`,
`IP-LICENSING.md`, `OPEN-DECISIONS.md`, `TIMELINE.md`. These cover
nearly the same ground as this archive's own `knowledge-base/` — same
underlying evidence (the same ADRs, the Incognita Rule, the 2026-07-23
architecture survey), a different per-section template, a different
location — and `docs/README.md` (PR #61) indexed the set as "the
canonical knowledge base," the same word this archive's own
`00-INDEX.md` uses for itself. Two artifacts claiming the same role is
not a new problem for this project: it is a third instance of the
uncoordinated-parallel-session collision pattern this archive already
documents twice (the licensing chaos in `08-DESIGN-DECISIONS.md`; the
Crystal Runtime episode in `07-HISTORY.md`).

**Resolution:** this archive's own `knowledge-base/` remains canonical
when the two disagree — not a new judgment call, but this archive's
own prior, explicit decision (recorded in `00-INDEX.md` from the outset)
applied to a fact pattern that came later. Independent corroboration
arrived from an unrelated third source the same day: `REPO-ARCHAEOLOGY-
2026-07-24.md` (a git-object-level survey of all six repositories,
committed to this repository's root by yet another uncoordinated
session, branch `claude/repo-archaeology-prompt-b3niko`) states plainly
that no single repository is canonical for everything, but for this
specific role names this repository directly: *"System ledger /
meta-record → `CrystalCore.OS-the-Crystal-Architecture-Archive`...
documents the other five; no unique application content."* Both sets
are preserved, neither deleted: a dated reconciliation note was added to
`docs/README.md` and to the top of each of the 7 files, stating the
relationship and pointing back here. Reconciling the two into one
structure is future work, not done in this pass — recorded as a new
Part 2-style open item below rather than silently left implicit.

Everything else in Part 2 remains open as written, plus one addition:

| Finding | File(s) | Why not applied here |
|---|---|---|
| Two independently-built knowledge bases now coexist (this archive's `knowledge-base/`, and `TerAustralis-Incognita/docs/`'s 7-file set) — reconciled with pointer notes this pass, but not merged into one structure | `TerAustralis-Incognita/docs/*.md` (7 files), this archive's `knowledge-base/` | A real information-architecture decision (which document owns which content long-term) — bigger than a documentation correction, and not something to settle unilaterally given this archive's own repeated deference to maintainer judgment on structural questions. |

---

## Part 5 — Applied 2026-07-28

**→ Status superseded, see Part 9.** The fixes described below were
never merged; the maintainer closed the PR carrying them. The finding
stands, the applied-status does not.

One new defect, in a class this archive had not previously audited for:
a **truth-label failure in shipped UI**, rather than in documentation.
Found in `CrystalCore-AERIS`, which no prior pass had examined.

### `CrystalCore-AERIS/index.html` and `website/index.html`

- **"Starship telemetry" was not telemetry — relabelled.** The AERIS
  desktop presented a `◈ STARSHIP` window of stat rows (`Flight 13 /
  Intact`, `Ship 40 / Indian Ocean`, `Reusability / 62%`, `Mars Goal /
  Active`) and a `◈ NEWS FEED` window of four items, both styled as
  instrument readouts. Verified by search: the page contains **zero**
  `fetch`, `XMLHttpRequest`, `WebSocket`, or `EventSource` calls. Every
  value was a literal string in the markup. The word "telemetry" and the
  "feed" framing asserted live instrumentation that does not exist.

  After: window titles are `◈ STARSHIP — SNAPSHOT` and `◈ NEWS —
  SNAPSHOT`; each body carries a visible `.snapshot-note` reading
  "Static snapshot — not live telemetry / not a live feed. Reviewed
  2026-07." The terminal's `starship` command gained the same
  disclosure in place of its reusability figure. The marketing site's
  hero line and feature card ("STARSHIP TELEMETRY / Flight status,
  reusability odds, Mars commitment") became "STARSHIP MISSION BOARD /
  ...a recorded snapshot, not a live feed."

- **Prediction-market odds presented as instrumentation — removed.**
  The `Reusability 62%` stat row, the news item `POLY — Reusability odds
  62% (+4%)`, and the terminal's `Reusability: 62%` were three
  renderings of one prediction-market figure. The `(+4%)` delta in
  particular implies a tracked series. All three deleted rather than
  relabelled: a snapshot label makes a stale fact honest, but it cannot
  make an odds quote into a measurement.

- **`#news` fixed height removed (incidental).** `height: 200px` under
  `.window { overflow: hidden }` clipped the new snapshot note. Height
  now follows content, matching `#telemetry`'s existing behaviour.
  Confirmed by headless-Chromium render before and after.

**Scope held deliberately.** Three things were *not* done:

1. The real-world flight claims (`Flight 13 / Intact`, `Ship 40 /
   Indian Ocean`, the 2028 window) were neither verified nor corrected.
   This pass had no authority to check them and did not guess; marking
   them dated and static is what makes them safe, not editing their
   content.
2. No live data source was added. The page's zero-network-calls
   property is a feature — the same property a prior pass recorded
   approvingly for `crystal-vision` — and importing a feed to justify
   the old label would have been the wrong direction of fix.
3. The `id="telemetry"` element identifier and its `showWin('telemetry')`
   handler were left alone. Internal, not user-visible; renaming risked
   the taskbar for no truth gain.

**What was verified as sound, and bounded this correction.**
**[Superseded the same day — see Part 6. The "not a pattern" claim below
was wrong: the identical defect was then found in `CrystalCore.OS`,
which this pass had not examined. The sentence is left standing rather
than edited, because the error is the point.]** The same
sweep confirmed the *accurate* claims, so the defect is narrow and not
a pattern: the Mars clock is genuinely live and arithmetically correct
(`88775.244` s is the true sol length; epoch is Perseverance's
2021-02-18 landing; it read Sol 1933 on 2026-07-28, matching
independent calculation). The terminal's ten commands all exist. In
`TerAustralis-Incognita-Code`, `core/crystal-core/consent_transport/`
is a real `Noise_IK_25519_ChaChaPoly_SHA256` implementation on audited
`cryptography` primitives with no hand-rolled cipher work, and its
selftest passes 9/9 — including `test_denied_without_consent`,
`test_revocation_takes_effect_next_request`, and
`test_forged_fragment_is_rejected_by_receiver`. `discovery.py` is
genuinely serverless (LAN UDP broadcast, no rendezvous host) and
documents its own limits accurately.

**Provenance — why this surfaced now.** The defect was found while
checking an external AI-generated report ("CrystalCore.OS — AERIS /
VAULT 12 Exploration Report," attributed to Manus AI, dated
2026-07-28) that the maintainer supplied. That report repeated
"Starship telemetry" as fact and presented shipped code, mythos, and
aspiration in a single register with no layer distinction. This is the
label defect propagating outward: an external reader, human or machine,
inherits whatever confidence the artifact projects. The correction is
therefore in the artifact, not the report — the report was accurate
about what it saw.

---

## Part 6 — Applied 2026-07-28 (later the same day)

**→ Status superseded, see Part 9.** As with Part 5, the fixes below
were never merged. The finding — the same defect in a second
repository — stands.

Part 5 was wrong about its own scope. It called the AERIS truth-label
defect "narrow and not a pattern." Within the hour the identical defect
was found in `CrystalCore.OS` — a repository Part 5 had not examined,
in an earlier and more explicit form. Part 5's sentence is left in place
with a pointer here rather than quietly edited: a corrections ledger
that silently repairs its own misjudgements is worth less than one that
shows them.

### `CrystalCore.OS/index.html` and `README.md`

- **"STARSHIP TELEMETRY" — relabelled.** Where AERIS titled the window
  `◈ STARSHIP`, this one said `◈ STARSHIP TELEMETRY` outright, over the
  same static stat rows, with the same zero network calls. Now
  `◈ STARSHIP — SNAPSHOT` with a dated `.snapshot-note`, matching AERIS.
  The `◈ NEWS FEED` window received the same treatment.

- **A liveness claim in prose — removed.** The news item read
  `POLYMARKET — Starship reusability odds: 62% (up 4% this week)`.
  "This week" asserts a tracked series outright, which is a stronger
  false claim than any AERIS carried. Deleted, along with the
  `Polymarket Reusability / 62%` stat row and the figure in the
  terminal's `starship` and `news` commands.

- **The README contained its own disproof.** Under **Features**:
  "Starship Telemetry panel (Flight 13 status + Polymarket odds)."
  Under **Roadmap**: "Live Polymarket odds API." The odds cannot be
  live if making them live is future work. The Features line now
  describes what ships; the Roadmap line is untouched, being honest as
  stated future work.

- **Sol counter arithmetic — corrected.** Unrelated to the labelling,
  found in the same sweep. The counter divided elapsed time by
  `24.65 * 3600` s (88 740 s). A Martian sol is 88 775.244 s, so the
  clock ran 35.244 s/sol fast and had accumulated 0.77 sols of error
  since the 2021-02-18 epoch — enough to read **Sol 1934** on
  2026-07-28 while `CrystalCore-AERIS`, using the correct constant,
  read **Sol 1933**. Two sibling pages describing the same moment
  disagreed by a full sol, and the one the README markets as a "Live
  Mars Clock" was the wrong one. Now uses AERIS's constant; both agree.
  Verified by headless-Chromium render.

**Correction to Part 5's reasoning, not just its facts.** Part 5 cited
the correct sol arithmetic in AERIS as evidence *bounding* the defect —
"the accurate claims are accurate, therefore the problem is local."
That inference was unsound twice over. The sol constant was not a
project-wide invariant but a per-file literal, wrong in the sibling
file. And a defect verified absent in the one repository examined says
nothing about repositories not examined. Correct labelling in one
artifact is not evidence about another; only looking is.

**Standing scope note.** Four of the eight repositories then visible had
not been audited for this defect class (`crystal-vision`,
`The-Crystal-Vision`, `TerAustralis-Incognita`,
`TerAustralis-Incognita-Code`). This is recorded as unexamined, not as
clean. Per the reasoning above, no claim is made about them either way.

**Corrected 2026-07-28: the denominator was wrong.** "Eight" was this
session's clone count, not the portfolio. A GitHub API query for
`user:CrystalArchitect` returns **eleven**, so seven repositories are
unaudited for this defect class, not four — the three additions
(`crystalcore-os-aeris-vault12`, `teraustralis-incognita-v2`,
`teraustralis-v2-presentation`) were never in this session's scope and
could not be cloned, `add_repo` requiring an approval a non-interactive
session cannot obtain.

Worth naming plainly, because it is the third instance of one error in
this file. Part 6 established that a defect verified absent in the
repositories you examined says nothing about repositories you did not.
Part 9 reduced that to "only looking is." Then the very sentence stating
the rule counted its own scope from what happened to be mounted, and got
the denominator wrong. Knowing the rule is not the same as having a
number you can trust — a scope claim needs its source named, not just
its logic sound.

**Superseded 2026-07-29, for one of the three.**
`crystalcore-os-aeris-vault12` has since been examined. It was cloned and
read in full, and `02-REPOSITORY-MAP.md` now carries two Statements about
it: the seven Starline specifications it holds, and a comparison of that
specification against the running `consent_transport` implementation.
So the "unexamined, look here first" flag below is answered, not standing.

The flag was right about where to look. The examination found, in
`docs/southern-node-lfa-operational-log.md`, a document reporting
node-to-lattice latency to one decimal place, standard deviation, 95th
percentile, and a Southern-versus-Northern node comparison table — with
no truth label, unlike every sibling document in that repository. Nothing
in the portfolio can produce those figures: `core/node/mesh/stub.py` is
in-process only with libp2p marked HOLD, and Starline binds 127.0.0.1.

That is precisely the defect class this Part predicted for that
repository: a decorative figure in the register of a measured one, in a
public specification repository. It is recorded here rather than
corrected, because the fix is a truth label on the maintainer's own
canon, not a change this archive should make unasked.

One of the three matters more than the other two.
`crystalcore-os-aeris-vault12` is **public**, and Part 0 records it as
carrying the Starline edge-node and Consent Token specifications. A
public specification repository is exactly where a decorative figure
read as a specification does the most damage, and it is precisely the
class of repository this defect has favoured. Unexamined, and flagged
as the one to look at first.

---

## Part 7 — Applied 2026-07-28 (origin of the Part 5/6 defect)

**→ Status partly superseded, see Part 9.** `CONCEPT-RENDERS.md` was
never merged and does not exist. The causal account of where the defect
came from is unaffected.

Parts 5 and 6 corrected the same mislabel in two repositories without
establishing where it came from. It came from the concept art.

The Grok render used as the AERIS build reference contains a panel
captioned `STARSHIP TELEMETRY`, complete with `VEHICLE SN-42`,
`VELOCITY 27.4 KM/S`, `POWER 82%` and an ECG trace. It was implemented
faithfully. Nobody introduced the defect; a render was handed over as a
build reference and, absent any statement to the contrary, its
decorative instrumentation was indistinguishable from a specification.

The full propagation, now closed: **render → `CrystalCore.OS` →
`CrystalCore-AERIS` → both READMEs → an external exploration report
that repeated "Starship telemetry" as fact → a suggested next feature,
"add a Starship telemetry panel with animated flight-status data."**
Four hops. Each one faithful to its input.

### `CrystalCore-AERIS/CONCEPT-RENDERS.md` — new

Records each reference render, what it shows, and which elements are set
dressing. Deliberately **not** a new convention: it follows the
table-plus-truth-label format `TerAustralis-Incognita/mythos/art/
README.md` already uses, whose `eight-sovereign-laws.jpeg` row was
already doing precisely this job ("a `0.1-alpha` experiment, but it is
unwired — the companion does not actually score sessions"). The pattern
existed; it had simply never been applied to the build references.

Two findings of substance beyond the telemetry block:

- **`HANDSHAKE: XX` contradicts the implementation.** The Starline
  render's Noise panel says XX; `consent_transport/noise.py` implements
  **IK** (`PROTOCOL_NAME = b"Noise_IK_25519_ChaChaPoly_SHA256"`, "IK
  pattern only"). Different handshake, different assumptions — IK means
  the initiator already holds the responder's static key, which is what
  the manual pairing step provides; XX means neither side does. The
  panel's other three lines (`ChaChaPoly`, `X25519`, `ED25519`) are all
  correct against the code, which is exactly what lends the wrong one
  its authority. Caught before implementation this time.
- **Register determines risk.** The Starline Expansion maps show the
  same network as the render above, drawn cartographically — compass
  roses, chart framing, no uptimes, no packet rates, nothing shaped
  like a reading. Same content, no defect surface. Recorded as the
  preferred reference format, which is a cheaper fix than labelling
  every future HUD.

Also logged there, unresolved by design: two node names in those maps
(**Sunwash Atolls**, **Cinderwake Chain**) appear in no repository and
are not among the Codex's Five Keys, while the map's other five map onto
them exactly. Recorded as render-only with canon status undecided — a
maintainer's call about the mythos, not a defect for this pass to
correct. **→ Since resolved, see Part 8.**

### Added to Part 2 — identified, not applied

| Finding | File(s) | Why not applied here |
|---|---|---|
| Stale pre-split path in the art gallery's truth label: cites `src/apps/lumina/crystalcore/sovereignty_scorer.py`, which does not exist. The file is at `vision/apps/lumina/crystalcore/sovereignty_scorer.py` after the Stage 1/2 split — the same defect class Part 1 corrected in six other files. The claim itself is **accurate**: verified this pass that `sovereignty_scorer` has zero references anywhere else in the Lumina app, so it is genuinely unwired. | `TerAustralis-Incognita/mythos/art/README.md` | One-line path fix, but in a repository this pass has otherwise not touched and against which no branch is open. Batching it with the next pass on that repository costs nothing; opening a fourth branch for one line does. |

---

## Part 8 — Applied 2026-07-28 (the open canon question, answered)

Part 7's one deliberately-open item is closed. The maintainer confirmed
**Sunwash Atolls** and **Cinderwake Chain** as canon Starline nodes the
same day.

Worth recording as a distinct case, because it inverts the pattern
Parts 5–7 documented. There, the render was ahead of nothing — it
carried decoration that the code then implemented as fact. Here the
render was ahead of the *code*: it drew two real nodes the
implementation did not yet have. Same divergence, opposite direction,
and only one of the two is a defect. The rule that separates them is
not "art must match code" but "each must say which it is."

### `TerAustralis-Incognita/mythos/crystalcore-os/crystalcore_os.py` and `mythos/CRYSTALCORE-OS.md`

- **Two nodes added, both key-bearing and both sealed** behind named
  keys — Magenta Key and Ember Key — making the First Gate a seven-key
  gate. Node order follows the chart outward from Earth, which
  renumbers the `visit <n>` shortcuts; saves are unaffected, since
  `keys_held` stores names rather than indices.

- **The count is now derived rather than written.** This is the part
  that matters beyond the mythos. The gate condition was already
  `len(keys_held) == len(nodes)` and absorbed the change for free; the
  prose did not. Four strings said "five" outright and the snapshot
  listing hardcoded `keys {n}/5` — every one of them became false the
  moment the list grew. They are now spelled from `len(self.nodes)` by
  a `_count_word()` helper, so the register survives and the number
  cannot go stale again.

  That is the same defect class as the sol constant in Part 6: a value
  written into a second place, then drifting from the first. Part 6
  corrected an instance; this removes the mechanism for one file.

- **The artwork now lags the map.**
  `mythos/art/starline-network-year-3000.jpeg` renders the original
  five nodes. Labelled in `CRYSTALCORE-OS.md` as an earlier state of
  the same map rather than left to contradict the ASCII chart
  silently. Regenerating it at seven nodes is a separate decision, not
  taken here.

Verified by playthrough against a throwaway `HOME`: sealed nodes refuse
entry without their named key, all seven yield keys, the First Gate
opens at 7/7, and no stale "five" survives outside the lookup table and
its explanatory docstring. Repository CI (markdownlint + link check)
passed — the first PR in this constellation to run any CI at all, four
of the other repositories having no `pull_request` workflow.

**Naming note — raised, and resolved the same day.** The key was first
given as `Ember Ley` — "Ley", not "Key". This pass recorded it verbatim
and flagged it rather than normalising it: in a project built on
songlines, starlines and lattices, a ley line of embers is a plausible
coinage, and an author's word is not a typo merely because a more
obvious word exists nearby. The maintainer confirmed it was a slip and
the key is **`Ember Key`**, now corrected in
`crystalcore_os.py`, `CRYSTALCORE-OS.md`, and here.

Worth keeping in the ledger even though the cautious reading turned out
wrong. Asking cost one exchange; guessing wrong in the other direction
would have written an invented coinage into the canon under the
maintainer's name, and nothing in the artifact would have revealed it.
The asymmetry, not the hit rate, is what justifies the flag.

---

## Part 9 — Applied 2026-07-28 (Parts 5–7 reclassified: found, not fixed)

Parts 5–7 were written and merged while their fixes sat in open pull
requests. The maintainer then closed those pull requests without
merging. The corrections never landed, and this file — merged to `main`
— went on describing them in the past tense as applied.

That is the defect this ledger exists to catch, occurring in the ledger
itself. A corrections record that claims corrections which do not exist
is worse than no record, because it retires a finding that is still
live.

**This is a status change, not a retraction.** Every finding in Parts
5–7 was verified and remains true. Only the applied-status was wrong.

### What is now false, and what replaces it

| Part 5–7 claimed | Reality on 2026-07-28 |
|---|---|
| `CrystalCore-AERIS`: window titles **are** `◈ STARSHIP — SNAPSHOT` and `◈ NEWS — SNAPSHOT`; the `.snapshot-note` disclosure exists | Not merged. Both windows still title static content as instrumentation. |
| `CrystalCore-AERIS`: the prediction-market odds figure was **removed** in all three places | Not merged. `Reusability 62%`, the `POLY … (+4%)` news item, and the terminal figure all remain. |
| `CrystalCore-AERIS`: `#news` fixed height **removed** (incidental) | Not merged. |
| `CrystalCore.OS`: same relabelling applied; sol constant **corrected** to `88775.244` | Not merged. The counter still divides by `24.65 * 3600`, running 35.244 s/sol fast — it read **Sol 1934** against `CrystalCore-AERIS`'s correct **Sol 1933**. |
| `CrystalCore-AERIS/CONCEPT-RENDERS.md` — **new** | Does not exist. The build-boundary record was never created. |

Parts 5–7 keep their text with a `→ Status superseded` pointer at the
head of each, following the precedent Part 6 set over Part 5: the
record shows what was believed and when, rather than being rewritten to
look correct in hindsight.

### Moved to Part 2 — identified, not applied

| Finding | File(s) | Why not applied |
|---|---|---|
| Static stat and news windows titled as live instrumentation, on a page with zero network calls | `CrystalCore-AERIS/index.html`, `website/index.html` | Fix was written and reviewed, then the PR was closed unmerged by the maintainer. A closed PR is a decision, not an oversight — this stays a live finding until the maintainer chooses otherwise, and is not to be re-opened unasked. |
| Same defect, earlier and more explicit form: window titled `STARSHIP TELEMETRY`, news item claiming odds "up 4% this week" | `CrystalCore.OS/index.html`, `README.md` | Same PR-closed reason. |
| Sol counter divides by `24.65 * 3600` s where a Martian sol is `88775.244` s — 35.244 s/sol fast, already a full sol adrift from its sibling page | `CrystalCore.OS/index.html` | Same PR-closed reason. Unlike the labelling above this is a plain arithmetic error, independent of any judgment about how the page should be framed. |
| No record marks which elements of the Grok build-reference renders are decoration rather than specification | `CrystalCore-AERIS` (file was to be `CONCEPT-RENDERS.md`) | Same PR-closed reason. Part 7's causal account of the propagation stands regardless; what is missing is the artifact that would stop it recurring. |

### What Part 8 is not

Part 8 is unaffected, and its status is earned rather than assumed.
Both halves of it merged on 2026-07-28: the seven-node canon in
`TerAustralis-Incognita#70`, and its extension to the web recreation in
`TerAustralis-Incognita-Code#29`. Part 8 is therefore the one entry in
this run whose "applied" is literally true, and — since the Code repo
owns the CNAME and publishes on merge — the live site at
`www.teraustralis.com.au/crystalcore-os` now shows seven nodes too.

This paragraph needed correcting twice while being written. It first
said *"Neither is merged at the time of writing"*; #70 merged within
the hour, and #29 merged while that sentence was being fixed. The rule
below, bitten twice by its own author inside one pass — which is the
right outcome, and the reason the wording now names merge commits and
dates rather than describing a PR's mood. **State what merged and
when. A sentence about what is currently open is written to rot.**

**A rule this pass earned.** An entry in this file should not say
"applied" while its change is in an unmerged pull request. Applied
means merged. Until then the honest word is *proposed* — Parts 5–8 were
all written in the past tense before their PRs landed, and three of
them turned out to be wrong.

---

## Part 10 — Filed 2026-07-29 (an inbound document, checked and quarantined)

A handoff titled *FINAL MASTER HANDBOFF — UNIFIED WEAVER NEXUS
PORTFOLIO* arrived in a chat session and nowhere else. It is now on
disk at [`../WEAVER-NEXUS-HANDOFF-2026-07-29.md`](../WEAVER-NEXUS-HANDOFF-2026-07-29.md),
reproduced as received, under an archive-authored reception record.

**Credited to four names**, at the maintainer's direction on
2026-07-29: **@architectweaver** (`https://x.com/architectweaver`), who
wrote the build and sent it, plus the three the received text signs
itself with — **Ryan Scott (Light)** and **Christian (Void)** as
Stewards, **Azirion Veythryx** as Vigil (Section VI).

Four names, not necessarily four people. The maintainer is unsure
whether the handle is one of the three, and the archive cannot tell
from here, so every name that appears is credited. That is the safe
direction to be wrong in — crediting a name twice costs nothing,
dropping a contributor costs someone their attribution — and it is not
a headcount or a claim about who anyone is.

None of it is verified, and it is not written as though it were. The
handle was supplied in-session and never checked against the profile it
names; the three signature names are the document's claim about itself,
reproduced. That is the ordinary basis for crediting authors. What the
credit does establish is that the reproduced text is not this archive's
writing — which is also what CC BY-NC-ND 4.0 requires of this
repository.

*Three wordings in one day: @architectweaver as sender, then as author
on the maintainer's confirmation, then all four names when the overlap
between them turned out to be unknown. Each earlier version understated
the credit; all are left visible rather than overwritten.*

This is not a correction to anything the archive said. It is here
because the ledger should record what arrived claiming portfolio-wide
authority, what was checked, and what the check found — the same reason
Part 0 records the eleven-repository miss.

**Why it was filed rather than absorbed.** The Constitution requires it
(`TerAustralis-Incognita/docs/governance/Constitution.md` §3.2: "Orphan
content (only in one chat) must be promoted to disk or logged as
deliberate draft"). Nothing in it could be absorbed into this knowledge
base, because every Statement here must cite a file path, line number,
or commit SHA (`12-CONTRIBUTING.md`) and not one of its rows can.

### The finding that matters

Fourteen identifiers from the handoff — `witness_verifier`, `EMASTER`,
`RCAP-200`, `Weaver Nexus`, `Abraxas`, `Empty Throne`, `Density-Driven
Gravity`, `Recursive Harmonic Intelligence`, `Must-Keep Ledger`,
`Evidence Ladder`, `Codex of the Oracle`, `Apokatastasis`, `Kavanah`,
`Azirion` — were searched across every commit of all eleven
repositories: `git grep` over `git rev-list --all`, 502 commits.

**Zero matches. Every repository, every commit.**

So the "Unified Weaver Nexus Portfolio" and the CrystalArchitect
portfolio this archive documents share no tracked artifact. Not one
volume, blocker, validator, ledger, proof, or script the handoff names
is in these repositories. Its stated highest-leverage next action — run
`witness_verifier.py` — cannot be taken from here; the script is not
here.

That is a scope fact, not an accusation. The material may exist in a
workspace this archive has never seen. What follows from it is narrow
and firm: **nothing in `STATUS.md` moves, and the handoff is not a
description of these eleven repositories.**

### The one thing that could be checked failed

Section III.C's twelve collections sum to **85**. The total is stated as
**84** in four separate places. Each collection's internal status
breakdown is consistent with its own count; only the total is off, by
exactly one.

Same defect class this file already carries twice — a count written into
a second place and then drifting from the first (Part 6's sol constant,
Part 8's hardcoded `keys {n}/5`). Unresolvable from here: the 84 rows
are not in these repositories to count.

### Two names, and a typo, left for the maintainer

- **`Weaver` and `Chronicle` are already taken.** `Starline Weaver` is a
  self-tested code component (`StarlineWeaver`, `mythos/NAMES.md`), and
  `Chronicle` names both `vision/site/src/lib/data/chronicle.js` and
  `~/.crystalcore/chronicle.jsonl` (`Roadmap.md`). The handoff reuses
  both for mythic figures. Under "Locked names stay locked"
  (`AGENTS.md`), that has to be resolved before any of this material
  could be promoted into `mythos/` — a maintainer decision, not a
  documentation fix.

- **The title reads `HANDBOFF`**, twice, while the body says handoff
  throughout. Preserved verbatim rather than normalised, on the `Ember
  Ley` precedent in Part 8: flag it, don't silently write a guess into
  the canon under the author's name. Almost certainly a slip.

### Standing risk, third instance

Part 0 recorded it twice — a clone read once and then trusted, and a
ledger with no trigger for repository creation. This is the same gap
facing outward: a document asserting portfolio-wide status arrived, and
nothing in this archive's method would have noticed it, contradicted
it, or stopped it being quoted as ledger truth. It is on disk because a
session happened to file it. There is still no trigger.

---

## Part 11 — Filed 2026-07-29 (Part 9's prediction, arriving)

Part 9 named `crystalcore-os-aeris-vault12` as the repository most
likely to publish a dreamed line as a measured one, because it is
public, has no CI, no tests and no deploy gate, and its documents are
written in the register of specification. The prediction held. Two
documents that landed there the same day assert what the code
contradicts, and the corrections are open as a **draft** PR
(`crystalcore-os-aeris-vault12#2`) rather than applied, because the
judgement in them is the maintainer's.

### The claims, and what was read to check them

Checked against `TerAustralis-Incognita-Code` at `46c562b9`, not against
memory of it — the discipline `SURVEYED.md` exists to enforce.

`docs/CRYSTALCORE-OS-EDGE-AGI.md` §4 is a capability table with a
`Status` column. Five rows read `Active`.

- **"Persistent personal memory — Active — Encrypted."** Lumina
  persists with `write_text(json.dumps(...))`
  (`vision/apps/lumina/crystalcore/companion.py:732`), and its entire
  dependency list is `requests>=2.28` and `flask>=3.0`. Nothing in the
  installed set can encrypt anything. This is the worst of the five: not
  an optimistic maturity grade but a **specific security property,
  stated as fact, on a public page**, of the kind a reader would
  reasonably rely on before putting personal material into the store.
- **"Lattice presence & heartbeat — Active."** `core/node/mesh/stub.py`
  describes itself as *"in-process only"*, holds libp2p at *"HOLD until
  audit / mainnet gate"*, and sets `authority = "HOLD"`. The word
  `heartbeat` appears nowhere in `core/` or `vision/` except one line of
  narrative prose in `THE-SOVEREIGN-KEY.md`.
- **"Continuity stream hand-off — Active."** `continuity stream` appears
  nowhere in the codebase at all.
- **"Consent-token gated actions — Active."** Real as of the same day,
  but an issuer-side reference library — signature, expiry and scope
  verification, exercised by tests, not presented peer-to-peer and not
  deployed on any node.
- **"Local inference — Active."** True. Left alone.

`docs/southern-node-lfa-operational-log.md` reports latency mean, median,
standard deviation and 95th percentile, a Southern-vs-Northern
comparison table, and packet-loss analysis. It carries a header block —
Date, Node, Doctrine, Phase — but **no version and no truth label**, the
only document in that repository without one. Nothing in the codebase
emits telemetry of any kind, so no figure in it can have been measured.

### The correction is labelling, not redaction

The figures stay. The tables stay. The prose and its voice stay. What
the draft adds is a legend defining what each `Status` value means and
naming the commit the column was read at, corrected values in four rows,
and a Vision-layer header on the operational log saying in one sentence
that its figures are written rather than read off an instrument.

That distinction is the whole point, and it is worth stating plainly
because the opposite reading is available and wrong. The Incognita Rule
does not say *do not dream*. It says **mark which lines are dreamed and
which are surveyed, and never let a dreamed line pretend it was
measured.** A repository of speculative specifications is entirely
legitimate; an unlabelled one is not. Deleting the operational log would
destroy a document. Labelling it costs nine lines and makes it honest.

Sections 1–3 of the Edge AGI specification — including §3.2's
*"Persistent personal memory store (encrypted, user-owned)"* — were left
untouched, because they describe an intended design and are not claims
about what is built. The draft resolves the resulting tension by saying
so in the legend rather than by editing design prose to match a build:
the design is the dreamed line, the table is the surveyed one. That is
Part 0's accretion discipline applied to a specification instead of to
this archive.

### What this does not change

Nothing in [`../STATUS.md`](../STATUS.md) moves. The corrections make
two documents describe the system accurately; they do not change the
system. `Consent-token gated actions` remains what `STATUS.md` already
graded it — built, not running.

### Standing risk, fourth instance

Parts 0 and 10 recorded it three times: no trigger fires when a
repository is created, when a clone goes stale, or when a document
asserting portfolio-wide status arrives. This is the same gap in its
fourth form — **no trigger fires when a public repository gains a
document**. These two were found because a session happened to look.
`.github/scripts/check-freshness.py` narrows it, in that a moved commit
is now visible, but visible-if-someone-runs-it is not a trigger. Still
open, and now the longest-standing unresolved item in this file.

---

## Part 12 — Applied 2026-07-29 (the consent layer no longer diverges)

`02-REPOSITORY-MAP.md` stated that the vault12 Starline specification
and the running implementation *"diverge at the consent layer"*, filing
**Consent Tokens, expiry, scope, and propagatable revocation** as
"Designed, not built." All four are now built, tested, and enforced by
CI.

**True when written, overtaken by hours.** The claim was committed at
2026-07-28 21:57 UTC (`f5acade`). PR #34, *"Consent Tokens: reference
implementation of the v0.1 schema"*, merged into
`TerAustralis-Incognita-Code` at 2026-07-29 03:42 UTC — five and three
quarter hours later. This is the same shape as the six-repository count
and the `SystemMap.md` "Consequences" paragraph before it: accurate at
the moment of writing, and carrying no date by which a reader could tell.

### What actually landed

`consent_transport/token.py`, 344 lines, naming `CONSENT-TOKEN-SCHEMA.md`
v0.1 as its source. `consent.py` gained 181 lines; `selftest.py` gained
344; the layer is wired into `transport.py` and `agent.py` rather than
standing beside them. 925 insertions across five files.

Each of the four items is exercised by a named test rather than merely
present — the distinction this ledger has spent the day insisting on:

- **Tokens** — `test_purpose_is_mandatory`,
  `test_identity_binding_cannot_be_skipped`,
  `test_tampering_with_any_field_breaks_the_signature`
- **Expiry** — `test_token_expires`,
  `test_expired_token_stops_the_exchange_that_a_live_one_allowed`
- **Scope** — `test_token_grants_only_what_its_scope_names`,
  `test_byte_budget_is_enforced_and_refuses_an_oversized_transfer`
- **Propagatable revocation** —
  `test_revocation_kills_the_token_and_is_signed`,
  `test_forged_revocation_is_refused`,
  `test_revocation_gossiped_from_the_real_issuer_is_honoured`

`python -m consent_transport.selftest` reports **32/32 passing**, up from
9, run 2026-07-29 rather than inferred. `ci.yml:43` runs that exact
command. Two tests drive a real socket
(`test_token_scope_is_enforced_over_a_real_connection`,
`test_byte_budget_stops_a_batch_midway_on_the_wire`), so this is Built in
the strong sense.

### Applied

- **`02-REPOSITORY-MAP.md`** — the Designed-not-built statement is left
  standing with a dated supersession beneath it, per this file's practice
  of correcting by accretion. The conformance table under it predates the
  token layer and describes only the transport half; noted as still true
  but no longer the whole picture.
- **`SURVEYED.md`** — the `TerAustralis-Incognita-Code` row moved from
  `2f307c09` to `46c562b9`, the commit this re-read was actually taken
  from. `check-freshness.py` now reports that repository as current.

### What this says about the method

Worth recording that the fix worked. `SURVEYED.md` and
`check-freshness.py` were added earlier the same day in response to two
stale-claim failures. This is the third instance of that class — and the
first found by *deliberately re-reading a named commit* rather than by
someone happening to notice. The freshness check flagged the repository
as moved; re-reading it produced this correction. That is the loop
closing as designed, once.

One caveat on the audit's own reach: `CONSENT-TOKEN-SCHEMA.md` lives in
`crystalcore-os-aeris-vault12`, which is outside this session's scope —
`add_repo` requires an approval a non-interactive session cannot obtain.
So the code was verified against its own tests and its own claims about
the schema, **not** against the schema text. Whether the implementation
is faithful to §6 is unverified here and stays open.

---

## Part 13 — Applied 2026-07-29 (the repositories nobody had checked)

Part 9 left a standing scope note: seven of the portfolio's eleven
repositories had never been examined for this defect class. Part 6 gave
the reason it mattered — *"a defect verified absent in the one repository
examined says nothing about repositories not examined… only looking is."*
This is the looking, for three of them: `The-Crystal-Vision`,
`crystal-vision`, and `crystalcore`.

Every finding below was verified by execution — running the suite,
listing the endpoints the shipped client actually calls, resolving the
branches — not by reading code and inferring. One finding contradicted
the first reading of it and is recorded as the evidence has it, not as
the first pass had it.

### What the count is now

Not seven. `crystalcore-os-aeris-vault12` — the one Part 9 singled out as
most at risk and flagged to examine first — **was examined**, by a
parallel session, and is recorded above as Part 11. Three repositories
are audited here. That leaves **two** genuinely unexamined:
`teraustralis-incognita-v2` and `teraustralis-v2-presentation`, both
outside this session's GitHub scope for the same reason as before.
Recorded as unexamined, not clean.

### The finding with a consequence

`crystalcore/clementine/SONGLINE-PROTOCOL.md:117`, under **"What v0 is
not"**:

> Not a network service (in-process only; no sockets, no server yet)

Thirty lines earlier, the same file has a section headed **"Booting
Clementine (networked bus)"** describing a live HTTP service and
tabulating five endpoints. The socket is real —
`clementine/bridge/server.py:189` constructs a `ThreadingHTTPServer` —
and `SECURITY.md:20-23` describes its binding behaviour correctly.

"What v0 is not" is the section a reader consults to size an attack
surface, and it told them there were no sockets. Two security-relevant
documents in one repository disagreeing about whether a listening socket
exists. A stale line that survived the commit which added the server.

This is the first instance of the defect class in the portfolio with a
security consequence rather than a credibility one. Applied — the entry
now states what v0 genuinely is not (hosted, authenticated, encrypted)
and names `SECURITY.md` as the authority.

### The most-of-a-repository finding

`The-Crystal-Vision`'s `content/GOVERNANCE.md` is the file the site links
to as proof of integrity — *"Documentation must not outpace the code. See
GOVERNANCE.md"* (`crystalcore-app/crystalcore.html:62`). It was the least
accurate file in that repository. Three guarantees, each false:

| Claim | What running it showed |
|---|---|
| `:21` "passes the offline test suite before merging" | CI ran `compileall` only; the suite was never executed |
| `:21` (same) | The suite **failed**: `test_provider.py:212` asserted `0.13.3` against a `version.py` reading `0.13.4`. Both arrived in one import commit, so it had never passed |
| `:22` "Nothing enters `main`" | There is no `main` branch. The default is `master` |
| `:15` Built means "covered by the offline test suite", example: semantic recall | No test referenced recall, embedding or recency |

A fourth, adjacent: `crystalcore-app/tests/test_status.py` was written
pytest-style against a project that does not depend on pytest, so
`unittest` imported it, found no `TestCase`, and reported *"Ran 0 tests …
OK"*. Three tests that looked like coverage and were not — the silent
form of the same defect, and the one worth naming, because a suite that
reports OK while running nothing is harder to catch than one that fails.

Applied by making the promises true rather than softening them: the
version test now derives instead of duplicating, `test_status.py` is
ported (18 tests → 20), CI gained a job that runs the suite, and the
Built row names a capability the suite genuinely covers *and names the
test*, so the claim is checkable.

### A count that was fabricated in two repositories at once

`crystal-vision/app.js:122` and `crystalcore/interface/app.js:63-73` both
animate a counter to a hardcoded `const target = 847`, in both cases over
a `NODES` array holding **five** entries that the adjacent mesh panel
renders faithfully. The count-up animation is the tell: a number rolling
into place reads as a measured roll-up, not a literal.

Same fabricated constant, two repositories, shared ancestry. Recorded
because it is the first case here of the defect propagating *by copying a
file* rather than by a claim being restated — a different transmission
path from the one Part 7 traced, and one that a per-document review would
not catch.

`crystalcore` mitigates it with a `(simulated)` label and a page banner;
`crystal-vision` says only `(demo)`. Neither is corrected — see below.

### Not applied, and why

`crystal-vision` carries sixteen findings, the sharpest being a README
documenting `python -m services.pipeline_demo` and `python -m
node.agent.server`, **neither of which exists anywhere in the
portfolio**, which also contradicts that repository's own `SECURITY.md`
("Static demo only … no backend").

It is not corrected, because correcting it would be the wrong shape of
work. Its `main` carries twelve commits: ten dated 2026-07-17, then a
relicensing commit and its merge. Those two touched `LICENSE`, `NOTICE`
and one README line and nothing else, so the *content* is frozen
provenance. Its living copy is
`TerAustralis-Incognita-Code/vision/apps/crystal-interface/`, corrected
2026-07-24, and that copy already fixes the phantom backend, the sibling
map, the narrow disclaimer and the dead docs link — its README opens
*"Corrected 2026-07-24 — six repos exist today, not the three implied
below originally."* Repairing a snapshot nobody is meant to run, whose
descendant is already right, buys nothing and costs the provenance.

The recommendation on record is a pointer at the top of its README, and
that is the maintainer's to make.

Held back for the same reason — a repair that is a product decision
rather than a correction, following Part 9's *"a closed PR is a decision,
not an oversight"*:

| Finding | Repository | Why it is the maintainer's call |
|---|---|---|
| Seven ✅ Working markers for web-UI features that do not exist — profile switching, one-click forget, a reflect button, an editable profile card. The shipped client calls exactly two endpoints; `server.py` defines five more that nothing calls | `The-Crystal-Vision` | Two honest repairs exist — downgrade the markers, or rebuild the UI the pre-split monolith had. That is a decision about the product |
| `content/MEMORY.md` marks Reflective Memory `✅ Built (v10)` at `:26` and `⬜ design` at `:58` | `The-Crystal-Vision` | Which is true is a status call |
| `crystalcore-app/crystalcore.html:77-83` ships install instructions whose every line fails against a fresh clone | `The-Crystal-Vision` | Depends on whether that pre-split site is still meant to be published |
| `cli/crystalcore.py:112-113` prints `Red button: OFF` unconditionally while a real `RedButton` exists in `clementine/bridge/bus.py:36` that it never consults | `crystalcore` | Wiring it to real state or labelling it as static is a design choice |
| `spec/ARCHITECTURE.md:60` marks `CONSTITUTION.md` `●` Built; no such file exists | `crystalcore` | Create the document or change the marker |

### What was clean, stated because absence of evidence is not evidence

Part 6's rule cuts both ways: a repository is not clean because it was
never checked, and it *is* worth recording when a check comes back
empty.

- **`The-Crystal-Vision` has no fake-live-data defect at all.** An
  exhaustive search for `fetch`, `XMLHttpRequest`, `WebSocket`,
  `EventSource` and `axios` returns two hits, both backing real
  behaviour. `webapp/src/lib/Senses.svelte:9,18` disables its unbuilt
  Voice and Sight controls with a `soon` badge, under a comment saying
  they "hint at what's coming without pretending it works today." That is
  the house example of doing this correctly, and it belongs in the record
  as much as the failures do.
- **`crystalcore/services/`** — the pipeline was run, not read. Ten raw
  events, seven decoded, three quarantined with the correct reasons; unit
  normalisation checked by hand (21 500 Wh → 21.5 kWh).
- **`crystalcore`'s numeric constants** — Pleiades `~440 ly` agrees across
  six files, LEB `~1.2M km²` across three, GAB `~1.7M km²` across five,
  each matching published values. This is the category that produced the
  sol drift, and here it is genuinely clean.
- **`crystal-vision`'s economics panel** — the static-looking figures are
  recomputed at initialisation and the literals match the computed
  defaults exactly. Expected to be a finding; is not one.

### The archive asserted the defect it documents

Found while auditing the others, in this repository.
`02-REPOSITORY-MAP.md` described `CrystalCore.OS` as "boot screen,
draggable windows, Mars clock, **Starship telemetry**, news feed, command
prompt", under a Statement graded **Implemented**.

Parts 5, 6 and 9 are *entirely about that phrase*. Every other occurrence
of it in this archive sits inside quotation marks, being discussed as a
false claim. That row was the only place the archive stated it in its own
voice — and it survived five corrections that were about exactly this,
because the corrections were filed in `11-CORRECTIONS.md` and the claim
was in `02-REPOSITORY-MAP.md`.

Corrected, with the reason left in that file's Historical Notes. The
lesson is narrow and worth keeping: **fixing a claim where it is
discussed does not fix it where it is asserted.** A correction should
grep the whole archive for the phrase it is retiring.

### This Part nearly published a stale claim about staleness

Caught before merge, and recorded because the shape is exact. The
paragraph above first read *"Every one of its ten commits is dated
2026-07-17."* That was true of the **local clone** the audit ran against
(`ba1dbb7`). On `origin/main` there are twelve: a relicensing commit
(2026-07-28) and its merge (2026-07-29) landed after that clone was
taken. The audit also reported `crystal-vision` as an Apache-2.0
repository in conflict with ADR-0013 — which was true when the clone was
taken and had already been resolved on `main`, by the very commit the
clone was missing.

So a Part whose subject is claims that outlive their evidence was itself
about to state two, from a four-hour-old checkout. Exactly the failure
`SURVEYED.md` was created for, in Part 0's words: *"Both were true of the
clones they were read from. Neither was true by the time anyone read
them."*

Two things follow, and only the second is new.

The findings themselves survived — re-checked against `origin/main`,
`const target = 847` over a five-entry `NODES` is still there, and the
two later commits touched only `LICENSE`, `NOTICE` and one README line.
That is luck, not method: had they touched `app.js`, the finding would
have been wrong too.

The new part: `SURVEYED.md` records what the *archive* was read from,
and `check-freshness.py` reported all three of these repositories
current — because it compares the survey against the remote, and the
survey was right. Neither noticed that the **working clone the audit ran
in** was behind. A freshness check on the record is not a freshness check
on the reader. An audit should `git fetch` and state which commit it read,
the same way a Statement does.

### Standing risk, fifth instance

Parts 0, 10 and 11 recorded that nothing triggers on a repository being
created, on a clone going stale, on an inbound status document arriving,
or on a public repository gaining a document. Add this: **nothing
triggers on a repository being unaudited.** Three were audited today
because a session was asked to look, and the two that remain will stay
unexamined until someone asks again. `check-freshness.py` reports what
has *moved*; nothing reports what has never been *read*.

---

## Part 14 — Applied 2026-07-29 (a deploy that had been failing for eleven days)

Part 13 corrected `crystalcore`'s `index.html`, which headed a file list
*"On this machine (Grok home)"* on a page GitHub Pages serves to
strangers. After it merged, this ledger's author wrote that the fix
*"goes live immediately"*, and the pull request said the page was
*"served to strangers by Pages."*

Neither was true. Nothing had published from that repository in eleven
days.

### What was actually happening

`.github/workflows/static.yml` had failed on **every push since
2026-07-28** — `9a40544`, `bd587d1`, `36489fa`, three merges — with:

> `Get Pages site failed. Please verify that the repository has Pages
> enabled and configured to build using GitHub Actions. Error: Not Found`

The repository reports `has_pages: false`. Pages is switched off. The
last successful deploy was `f282199`, **2026-07-18**.

So the merge succeeded, the workflow ran, the workflow went red, and
three merges passed over it without anyone reading the result.

### The error worth naming precisely

Not "the deploy was broken and I did not know." The error was one of
**inference**: a merge succeeded, therefore the change is live. That is
the same inference shape this file has spent two days cataloguing — read
the artifact, conclude the capability. Reading a `README` and concluding
a feature exists, and reading a merge and concluding a page is served,
are the same move. The second one felt safer because a real event had
occurred; what had not been checked was whether that event produced the
outcome claimed for it.

It was made while auditing three repositories for exactly this failure,
and it stood until the maintainer said *"fix the failure please"* and
someone finally looked at the deploy.

### A second finding, older and larger

`static.yml` uploaded `path: '.'` — the **entire repository**.
`crystalcore` is private; a Pages site is public. So the configuration
published all **52** tracked files, including `spec/`, `services/`,
`clementine/transcripts/` and `.claude/settings.json`, none of which the
site links to. The site is **four** files: `index.html` and
`interface/{index.html,style.css,app.js}`, confirmed by tracing every
`href` and `src`.

This was live and working from 2026-07-16 to 2026-07-18. It predates
every audit in this file and was found only because the deploy failure
sent someone to read the workflow.

Narrowed in `259b038`: the workflow now assembles just those four files
and uploads that. Verified by serving the assembled directory over HTTP —
all four paths 200, both navigation links resolving, and
`spec/ARCHITECTURE.md`, `.claude/settings.json`, `README.md` and the
transcripts all 404.

### An operational fact, now confirmed twice

`enablement: true` on `actions/configure-pages@v5` — the remedy the error
message itself names — was **refused**, observed directly on run
`30462094166`:

> `pages: write cannot enable Pages in this account`

This is the second independent confirmation.
`TerAustralis-Incognita-Code/.github/workflows/deploy.yml` already
carried the note from an earlier session: *"the step cannot actually
change the setting: `GITHUB_TOKEN` with `pages: write` is not
sufficient."* That attempt used `PUT /pages` to change the build type;
this one used `POST /pages` to create the site. Different endpoints, same
refusal.

Recorded as a fact about this account rather than a one-off, so the next
session does not repeat the investigation: **no workflow can enable Pages
here.** It is a settings click or it does not happen.

### What is fixed and what is not

| | |
|---|---|
| Publish scope narrowed to the four files the site reaches | Applied, `259b038` |
| Failure message names the setting to change instead of `Not Found` | Applied, `259b038` |
| The deploy itself | **Still red.** The site genuinely is not publishing |

The red is deliberate, at the maintainer's direction. A green check on a
workflow that publishes nothing is precisely the defect this file exists
to catch, and skipping quietly would have produced one. The remaining
step — Settings → Pages → Source → "GitHub Actions" — is the
maintainer's, and no code change substitutes for it.

### Standing risk, sixth instance

Parts 0, 10, 11 and 13 record that nothing triggers on a repository being
created, a clone going stale, an inbound status document arriving, a
public repository gaining a document, or a repository being unaudited.
Add: **nothing triggers on a deploy that has been failing.**

The distinction this instance draws, which the previous five did not:
`SURVEYED.md` and `check-freshness.py` watch whether the archive's
*claims* have gone stale. Nothing watches whether the *machinery that
publishes them still runs*. A claim can be perfectly current, correctly
surveyed, freshly re-read — and served to nobody.

## Part 15 — Applied 2026-07-29 (the fix undid itself, same day)

Part 14 closed at the maintainer's Settings click: Pages on, `crystalcore`
reachable. The click itself reopened what it closed.

### What the click actually did

Settings → Pages → Source → "GitHub Actions" is not just a switch. GitHub's
onboarding screen for that flow offers starter workflow templates, and two
were committed straight to `main` — no pull request, no review:

- `61d4b59` — `.github/workflows/jekyll-gh-pages.yml`, Jekyll's stock
  template, `source: ./`
- `919c898` — `.github/workflows/statichtml.yml`, the stock static
  template, `path: '.'`

Both publish **the entire repository**. Neither template knows that
`static.yml` — narrowed to four files in Part 14, `#7`, `259b038` — already
exists and already does the correct version of exactly what they're for.
All three carried `concurrency: group: "pages"` and triggered on the same
push, so every push to `main` became a three-way race for whichever
workflow's `deploy-pages` call landed last.

### The race, timed from the run logs

| Time (UTC) | Event |
|---|---|
| 16:23:27 | `jekyll-gh-pages.yml` deploys first (commit `61d4b59`) — full repository root live |
| 16:23:47 | `static.yml` deploys 20s later, same commit — narrow site live again |
| 16:24:45 | `jekyll-gh-pages.yml` deploys again (commit `919c898`) — `static.yml` and `statichtml.yml` both **cancelled** |
| 22:56:31 | `static.yml` redeploys (commit `197250a5`, this correction's fix) — narrow site live |

Between 16:24:45 and 22:56:31 — **six and a half hours** — the live site at
`https://crystalarchitect.github.io/TheCrystalVision/` was the Jekyll build
of the entire repository root. The build log (job `90639249345`) lists what
it published, including `spec/ARCHITECTURE.md` *and* an auto-rendered
`spec/ARCHITECTURE.html`, `spec/BLUEPRINT-v0.3.md` (+`.html`),
`services/decode.py`, `services/api.py`, `services/ingest.py`,
`services/twin.py`, `services/selftest.py`, `WATER-BRIEF.md`,
`SECURITY.md`, and `TRANSMIT-LOG.md`. Jekyll's default Markdown processing
turned private specification files into a second, rendered public page
each — a private `.md` at least reads as a text file; Jekyll gave it a
navigable HTML page too. This is the identical exposure Part 14 measured at
52 files and narrowed to four, reopened by a mechanism entirely outside the
workflow file that had just been fixed.

### The fix

`#8` deleted both starter workflows outright rather than editing their
`path`/`source`. Neither has a legitimate purpose in this repository, and
removing them — rather than reconfiguring them — also removes the race
itself: `static.yml` is now the only workflow capable of deploying Pages.
`static.yml` was diffed against `259b038` and is byte-identical; the Part 14
fix was never the problem. Merging `#8` triggered the redeploy confirmed in
the table above: artifact size 10,923 bytes, against the Jekyll build's
112,131 — a cheap, checkable signal that the narrow site, not the
repository, is what's live.

### Standing risk, seventh instance

The first six (Parts 0, 10, 11, 13, 14) are all "nothing triggers on X
happening." This one is sharper: **a fix can be correct, merged, reviewed,
and verified, and still be silently superseded by activity that never
touches the reviewed change at all.** `static.yml` was not edited, not
reverted, not broken. Two unrelated files were added beside it, and the
platform's own concurrency semantics picked a winner nobody chose. Checking
that a fix is correct at merge time, as Part 14 did, does not establish
that it stays the thing that's live.

### A fact for the record, not a correction

While tracing the run logs, `owner=CrystalArchitect, repo=crystalcore`
resolved to `full_name: "CrystalArchitect/TheCrystalVision"`. The
repository has been renamed — no hyphen, distinct from both `crystal-vision`
(frozen) and `The-Crystal-Vision` (hyphenated, active, the unrelated
Svelte/Clementine repository already in this portfolio). Old remotes and API
calls by the old slug still redirect and work, which is how this correction
was written and pushed without incident. The rename is not acted on here —
recorded for whoever next reconciles `SURVEYED.md` against what's actually
out there, the same gap Part 0 and Part 1 both trace to a clone read once
and trusted.

### What is fixed and what is not

| | |
|---|---|
| The two competing workflows | Removed, `#8` |
| The race that let either win | Eliminated — `static.yml` is now the only Pages-capable workflow |
| The narrow site | Redeployed and reconfirmed live, `197250a5` |
| The repository rename | Recorded, not resolved |

Unlike Part 14, this correction closes clean: nothing here is deferred to
the maintainer. The Settings click was correct and is done; what needed
fixing was the unreviewed code it brought in alongside it.
---

## Part 16 — Filed 2026-07-29 (a twelfth repository, and this
archive's own tooling caught lying)

### The portfolio has twelve repositories

`teraustralis-proposal` was created at **20:17** and is **public**. The
archive learned of it at **20:54**, thirty-seven minutes later, and only
because a question about repository descriptions caused the account's
repositories to be listed — twelve rows where the archive expected
eleven. Nothing in the method would have surfaced it otherwise.

It is now recorded in [`02-REPOSITORY-MAP.md`](02-REPOSITORY-MAP.md),
[`../STATUS.md`](../STATUS.md) and [`../SURVEYED.md`](../SURVEYED.md).
Two things about it are worth carrying here rather than only in the map:

- **It is the only repository addressed to people outside the project** —
  a formal proposal seeking technical review and partnership, under an
  ABN and a named founder. Whatever this archive gets wrong elsewhere
  costs the maintainer time. What that repository gets wrong costs
  someone else's judgement.
- **Its technical brief asserted four properties of CrystalCore in the
  present tense.** Checked against `TerAustralis-Incognita-Code` at
  `f81dc37`: local-first held; auditable and consent-native held for
  tool calls but not for memory; **fail-safe isolation was not
  implemented at all**. Reported the same day with a correction patch.
  This is Part 11's defect class again, now in front of investors.

And a detail that reframes it. The pre-restructure `TECHNICAL-BRIEF.md`
carried a `## Current Status` section reading *"this brief states the
design intent."* The restructure at `c0a7c63` dropped it. **The honesty
label existed first and was lost in a reorganisation** — nobody decided
to overclaim. That is a gentler and more useful finding than
intent-to-mislead, and it argues for labels that live in the same block
as the claim, where moving one moves the other.

### This archive's own freshness tooling was making a stale claim

`SURVEYED.md` was written in this session to stop the archive being
quietly out of date. Its "Known limits" section said:

> Only `TerAustralis-Incognita` is public. The freshness check can read
> that one anonymously; the other ten need a checkout or credentials.

`check-freshness.py` said the same in a docstring: *"ten of the eleven
repositories are private."*

**Both halves were wrong.** Live GitHub metadata: **five are public** —
`TerAustralis-Incognita`, `CrystalCore.OS`, `CrystalCore-AERIS`,
`crystalcore-os-aeris-vault12`, `teraustralis-proposal`. And running the
script rather than reasoning about it showed visibility was never the
constraint: from a session container it reports `not reachable from
here: 0` and resolves **all twelve**, private ones included.

So the file built to prevent stale claims shipped one, and understated
its own tool in both directions at once. Nobody had run it and read the
output against what the documentation promised. That is the same failure
the file exists to catch, committed by the file.

Recorded here rather than quietly patched, because a corrections log that
omits its author's errors is a worse instrument than one that includes
them.

### Standing risk, fifth instance — and it is no longer a prediction

Parts 0, 10 and 11 recorded that nothing triggers when a repository is
created, when a clone goes stale, or when a document arrives. Part 11
called it *"the longest-standing unresolved item in this file."*

It was written on 2026-07-29. `teraustralis-proposal` was created on
2026-07-29, some hours later, and went unnoticed until a coincidence
surfaced it. The gap did not merely remain open; it was demonstrated by
the very next event.

`check-freshness.py` narrows the *stale clone* case and, now that it is
known to reach all twelve, narrows it further than the archive believed.
It does nothing for repository creation, because it only checks
repositories `SURVEYED.md` already lists — a repository nobody has heard
of is not stale, it is absent, and no amount of freshness checking finds
it. Closing that needs a different mechanism: something that enumerates
the account and diffs against the roster.

Still open. Still the longest-standing item here.

---

## Part 17 — Filed 2026-07-30 (a second Clementine, built for nothing)

### What happened

Asked to build a local-first companion app, an assistant built one from
scratch: a Node bridge, a set of Web Components, a consent gate, a
hash-chained audit log, an installable PWA layer, and a deployment
runbook. Roughly nine hundred lines across six commits, verified end to
end in a browser.

It already existed. `The-Crystal-Vision/clementine/` holds a Clementine
companion — Ollama wired to `llama3.1:8b`, layered memory with
`nomic-embed-text` embeddings and recency-weighted recall, profiles,
reflection, summarisation, streaming, and a Svelte interface with chat,
avatar and senses. Around eighteen hundred lines, and further along than
the replacement on every axis except three.

The portfolio's own README said so. `crystalcore/README.md` line 7 reads:
*"the-crystal-vision = The Crystal Vision (codex site + Clementine
sovereign companion app)."* The map was correct, present, and unread.

### The cost, and the part that was not wasted

Three pieces were genuinely absent from the existing app and were folded
into it: the consent gate, the audit log, and installability. Those are
now in `The-Crystal-Vision` PR #44. The Node implementation of the same
ideas was discarded rather than kept alongside — two codebases sharing one
name is how the confusion began.

The unrecoverable cost is the memory system, the profiles, and the Svelte
interface, all rebuilt worse and thrown away. Perhaps half the work.

### A symptom that should have been read as evidence

Mid-task the maintainer ran `pip install -r requirements pythonclemen…`
in a droplet console. The assistant replied that there was no
`requirements.txt` because the bridge was plain Node with no
dependencies. That was true of the directory the assistant had built and
false about the maintainer's project:
`The-Crystal-Vision/clementine/requirements.txt` exists and holds Flask
and requests. The maintainer was trying to run the real Clementine and was
told it did not exist.

The correction was available in the user's own commands and was overridden
by the assistant's model of the work. That is the mechanism worth naming:
not ignorance of the repository, but confidence surviving contact with
evidence against it.

### Why this belongs in this file

This file records what the archive got wrong, including when the archive
itself was the author. Parts 15 and 16 record tooling that shipped a stale
claim and a survey method that missed a repository. This is the same class
one layer out: **work begun without reading the map that was already
written.** A portfolio whose central problem has been overclaiming can
also suffer its inverse — building what exists because nobody checked.

### The rule it argues for

Before building anything named after something in this portfolio, grep the
portfolio for the name. `crystalcore/clementine/` (the Songline Bus hub)
and `The-Crystal-Vision/clementine/` (the companion) are both called
Clementine and are different systems; a third would have made it worse.
The name collision is unresolved and is now the second naming decision
waiting on the maintainer, alongside Lumina.

### Standing risk, sixth instance

Parts 0, 10, 11 and 16 record that nothing fires when a repository is
created or a document arrives. This is the same gap read from the other
direction: nothing fires when work *duplicates* what a repository already
contains, either. The roster this archive maintains is exactly the
instrument that would have prevented it, and it was not consulted.

Still open.

---

## Part 18 — Filed 2026-07-30 (a thirteenth repository that was not one)

### The claim, and its retraction

On 2026-07-30 the maintainer shared a GitHub Pages URL for
`CrystalCore-Starlines-and-Dreamlines`. The archive did not have that name.

An assistant surveyed it, found every one of its twelve shared files
byte-identical to `crystal-vision`, and concluded: a thirteenth repository,
holding a duplicate of the twelfth. Draft entries were written for
`02-REPOSITORY-MAP.md`, `STATUS.md`, `SURVEYED.md`, and this file; the count
was raised from twelve to thirteen throughout; and a note was added to the
other repository's README warning that the two copies would silently diverge.

**All of it was wrong.** `crystal-vision` was **renamed** to
`CrystalCore-Starlines-and-Dreamlines` on 2026-07-29. GitHub redirects the old
name. There is one repository, and the portfolio still has twelve.

Nothing reached this repository's `main` — the draft was discarded before
commit. The README note did reach the other repository and was corrected the
same hour, in a pull request that says plainly that it is fixing its author's
error.

### What caught it

Running the archive's own tool rather than reasoning about the result.
`check-freshness.py` reported `crystal-vision` as *now at* `c471338` — which
was, character for character, the head of the supposedly separate repository.
Two repositories do not share a head commit by coincidence.

Confirmed twice over: `git ls-remote` against a clone whose `origin` is
`…/crystal-vision` returns this repository's head, and the GitHub API returns
id **1304095452** with `full_name: CrystalCore-Starlines-and-Dreamlines` for
both names. One id, one repository.

### The reasoning error

Identical content across two names has two explanations: someone copied it, or
it is the same thing. The assistant took the first without testing the second,
then built a structure on top of it — a Statement, a ledger entry, a survey
row, a corrections entry, and a warning in someone else's README. Each new
piece made the original inference feel more established without ever
re-examining it.

That is the same failure as Part 17, one step earlier in the chain. Part 17
recorded work begun without reading the map. This is work continued without
re-reading the evidence.

### The defect it exposed, which is real

`SURVEYED.md` is **keyed by repository name**, and a rename is invisible to it.
GitHub's redirect meant `check-freshness.py` kept fetching the right repository
under a name that no longer existed, and reported the result as an ordinary
moved commit. Had the rename been to a name the archive did not recognise *and*
the redirect not existed, the row would have gone silently unreachable instead.

Neither failure mode is loud. Keying rows on the numeric repository id GitHub
assigns — stable across renames — would make a rename visible **as** a rename,
which is the only way this archive would ever notice one.

Recorded here rather than fixed in passing: the fix changes the survey table's
shape, and the archive's discipline is that a schema change gets proposed, not
slipped in beside a correction.

### On the standing risk

This is **not** an eighth instance of the repository-creation gap. No repository
was created; one was renamed. Parts 0, 10, 11, 16 and 17 stand as they are.

What it adds is a second failure mode for the same roster: not only does nothing
fire when a repository appears, nothing fires when one changes identity. The
mechanism proposed in Part 16 — enumerate the account, diff against the survey —
would catch both, and keying on id rather than name is what would let it tell
them apart.

Still open.

---

## Part 19 — Filed 2026-07-31 (an authorship claim nobody could have checked)

### The claim

The-Crystal-Vision PR #47 folded eight character additions into
Clementine's `SKILL.md` and `BASE_PROMPT` — Turning the Mind, Wonder,
Shared Discovery, Intellectual Humility, Memory Philosophy, Repair,
Silence, and a closing principle. Its body, written by an assistant,
described them as *"the maintainer's own writing on who Clementine is."*

The PR merged with that sentence in it.

### What was true

On 2026-07-31 the maintainer asked that Grok and ChatGPT be credited for
their part in the work. Asked what each had contributed, they said the
eight additions were drafted with help from both models, that Grok had
contributed to the CC-PHENO-01 protocol draft, and that Grok had shaped
earlier architecture discussion. The full accounting, with witnessed and
attested portions kept separate, is in `10-PROVENANCE.md` under "Model
credit for Clementine's character work."

### The reasoning error

The assistant watched the maintainer type the additions into the session
— they had said "I'll just start typing" — and wrote *authorship* from
having observed *transmission*. Those are different facts. Text arriving
from the maintainer's hands says nothing about where it was drafted, and
the assistant had no access to that provenance and did not ask.

The failure is the same shape as Parts 17 and 18: an inference (typed it
= wrote it) promoted to stated fact and then built upon, without the
step where it gets tested. Parts 17 and 18 built structures on untested
inferences about repositories; this one put an untested inference about
a person's authorship into a merge record, which is worse in one
respect — repository claims can be re-derived from the repositories,
but a false authorship claim, left standing, becomes the history.

There is also an asymmetry worth recording: the error understated
others' contributions and overstated the maintainer's. The maintainer
themselves corrected it in the direction of *less* credit to
themselves. That is the portfolio's honesty discipline working, and it
came from the human, not the assistant.

### The correction

The merged body stands as what was said on the day — this archive does
not rewrite records. A correcting comment was posted on PR #47 beside
the claim, and the provenance Statement in `10-PROVENANCE.md` now
carries the accurate accounting. The assistant's summary to the
maintainer that Grok's "net effect was zero lines changed" is corrected
by the same Statement: true of its review of the finished file, false
as a description of its contribution.

### The general defect

Provenance stated as fact, in a durable record, by a party with no
means of verifying it. The fix is not "verify harder" — the assistant
could not have verified this — but to write only what was actually
known: *the maintainer supplied these additions*. That sentence was
available, was true, and would have needed no correction.

---

## Part 20 — Filed 2026-08-05 (a library appeared, and two more names changed)

### What a partial survey could see

A library-sync session on 2026-08-05 had eleven CrystalArchitect
repositories in scope, cloned on disk, and no way to enumerate the
account. Against the twelve this archive last counted (Part 16, as
amended by Part 18's rename finding), the differences visible from
inside that scope:

- **`the-library` exists.** Created 2026-08-03 08:42 (+1000), two
  commits by the maintainer: a stub README and `loop-framework.md` — a
  working document on recursive narrative loops (a twelve-layer radar, a
  Method-vs-Logos rule, a DBT-based self-check protocol), which is also
  the constellation's first governance-adjacent document to arrive
  through no ledger at all. The session built the repository out into a
  document collection: the master plan of 2026-08-01, the Manus
  full-repository review of 2026-07-29, accession rules, and a sync
  record (`records/2026-08-05-library-sync.md`) holding the survey
  behind this filing.
- **The repository this archive documents as `crystalcore` now carries
  the GitHub name `TheCrystalVision`, and `The-Crystal-Vision` now
  carries `Clementine---Local-Soveriegn-Edge-AGI`.** Identification is
  by content: each clone's README still opens with its old identity
  ("This is **Crystal Core** — the protocol pack" / "This is **The
  Crystal Vision** — codex site + Clementine sovereign companion app").
  The decisive test is the one Part 18 prescribed — GitHub's stable
  numeric id — and the session had no account metadata to run it, so
  rename-versus-recreation is here an inference, stated as one.
- **The renamed `CrystalCore-Starlines-and-Dreamlines` (né
  `crystal-vision`, Part 18) is no longer frozen.** The archive's model
  holds it as provenance-only, never edited. Its clone carries commits
  through 2026-07-31 — `GROK_BUILD.md`, `BUILD_MANIFEST.json`, a
  rebuilt single-page site. A frozen repository that thaws silently is a
  classification going stale with no mechanism to notice, which is this
  file's oldest theme wearing a new coat.
- **Every sibling map that names the old spellings now points at the
  wrong doors** — including the maps inside the two renamed repositories
  themselves, one of which still spells the umbrella `teraaustralis`
  against ADR-0007. Part 17 showed those maps are what stands between a
  session and rebuilding what exists; they are now wrong in four
  repositories at once.

### What this filing deliberately does not do

`02-REPOSITORY-MAP.md`, `STATUS.md` and `SURVEYED.md` are not updated by
it. The session could see eleven repositories, not the account: it could
not read the July names to distinguish rename from replacement, could
not check visibility, and could not count the constellation. Part 18
demonstrated what happens when a structure is built on an untested
identity inference; the same restraint applied here means the map waits
for a pass with account metadata. Filed instead, with the evidence
stated at its actual strength.

### The standing risk, still standing

Parts 0, 10, 11, 16 and 17 record that nothing fires when a repository
is created; Part 18 added that nothing fires when one changes identity.
Both gaps produced this filing: a repository lived for two days before
any ledger heard of it, and two renames were caught only because a
session's scope list happened to spell the new names. The Part 16
mechanism — enumerate the account, diff against an id-keyed roster —
would have caught all three events and told them apart. Still open.
Still the longest-standing item here.
