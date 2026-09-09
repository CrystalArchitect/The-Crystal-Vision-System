# Architecture Review — CrystalCore-Starlines-and-Dreamlines

**Date:** 2026-08-26
**Reviewer:** Claude (independent architecture pass, no prior Grok review existed to build on)
**Scope:** Full repository at commit `6989a10` (branch `main`), 42 commits, unshallowed for this review.
**Method:** Read every tracked file, ran the test suite (`npm test`, 56/56 passing), read full
`git log`, cross-checked prose claims against code and history.

## Summary

This repository is **not** the CrystalBus/CrystalBridge messaging layer implementation — it is a
static front-end demo shell (`index.html` / `app.js` / `styles.css`) for the Crystal Core operator
UI, plus a second, unrelated static page (`celestial/`) that visualises a personal "mode wheel"
correspondence system inspired by astronomy and music theory. There is no Python, no `ConsentGate`,
no `StarlineWeaver`, no `BusHub`, and no `consent_transport/` anywhere in this repo; the README says
so explicitly and points to the actual bus/pipeline code in a sibling repository. Given that, most
of the architecture-constraint checks this review was asked to run (fail-closed `ConsentGate`,
Behavior-Tree-vs-FSM orchestration, Crystal-Vision import direction) have **no code in this repo to
check** — see "Scope mismatch" below, which is itself the most important finding.

What *is* in this repo is, unusually, an exemplary implementation of the Belt-Three discipline: the
`celestial/atlas.js` module enforces the Science/Vision split at runtime (throwing on unlabelled
entries) rather than leaving it to convention, and a dedicated test enforces the Indigenous
knowledge boundary by scanning the directory's own prose for the reserved word. The operator demo
shell was materially weaker on first pass — it presented illustrative wallet/consent/receipt numbers
with generally good "(demo)" labelling, but the labelling was inconsistent in a few places, and it
referenced files and protocols (RFC-001, `sim/parameters.yaml`, `docs/FULL-STACK-v0.3.md`) that do
not exist in this repository and are not confirmed to exist anywhere. **Update, same PR:** per the
repo owner's direction, Findings 2 and 3 have now been fixed rather than left as recommendations
only — see each finding below — and the README now carries a prominent top-of-file warning that
CrystalBus/CrystalBridge/ConsentGate/StarlineWeaver are not in this repository (closing open
question 4).

## Strengths

1. **Belt-Three is structural, not decorative, in `celestial/`.** `atlas.js` defines `BELT.SURVEYED`
   / `BELT.DREAMED` as the only two values, and `star()`, `correspondence()`, `reading()`, and
   `validate()` all **throw** rather than warn when an entry's belt is missing or wrong
   (`celestial/atlas.js:114-133`, `156-171`, `276-320`, `425-435`). The commit history shows this was
   deliberately modelled on `BusHub.validate` rejecting unlabelled speech
   (`celestial/atlas.js:15`, `421`) even though `BusHub` itself lives in another repository — the
   analogy is stated as an analogy, not claimed as the same code.

2. **The Indigenous knowledge boundary is enforced by an executable test, not just a policy
   sentence.** `celestial/atlas.test.js:568-591` scans every file in `celestial/` for the word
   "songline" (case-insensitive, word-boundary) and fails the suite if it appears anywhere outside
   the one sanctioned explanatory comment. This is exactly the kind of enforcement the project's own
   Indigenous-Data-Sovereignty document asks for, and it is rare to see a documentation *rule*
   implemented as a *regression test*. Ran it locally: `npm test` → 56/56 pass, matching the
   count both README (`celestial/README` table area, README.md:67) and CHANGELOG.md:28 claim.

3. **Provenance discipline extends to citations, not just code.** `celestial/PRECEDENTS.md` and
   `celestial/cycle.js` document two separate cases where an earlier draft stated an inference as a
   fact (an Apian caption compression, and a guessed ISBN) and were caught and corrected, with the
   correction left visible rather than silently edited (`cycle.js:107-109`,
   `PRECEDENTS.md:193-199`). `stars.js` refuses to hold a star position without a named catalogue and
   epoch (`atlas.js:114-133`) and the 28-star extract is a committed, offline, diffable file rather
   than a runtime fetch (`stars.js:1-27`) — directly satisfying "distance/offline is normal, not an
   error state" for this one data dependency.

4. **Self-aware repo hygiene.** `GROK_BUILD.md` opens by admitting its own prior version had gone
   stale (wrong file count, wrong project name, dead path) and corrects each point explicitly rather
   than quietly. `BUILD_MANIFEST.json` has an `"unverified"` section that records claims it could not
   confirm (a misspelled sibling-repo name, a referenced directory that doesn't exist) instead of
   guessing. This is the Incognita Rule applied to project bookkeeping, not just to content.

5. **`revise()`/`history()` in `atlas.js:322-368`** preserve prior "hearings" of a reading rather than
   overwriting them, with a required `asOf` date supplied by the caller (never machine-stamped) — a
   deliberate, tested continuity property for this data model.

## Findings

### Finding 1 — Scope mismatch: the reviewed conventions describe code this repo does not contain
**Severity: High (process/framing, not a code defect) · Belt: Docs-governance**

The review brief assumes this repo is "focused specifically on the CrystalBus messaging layer" and
asks for `ConsentGate` fail-closed checks, `StarlineWeaver`/`BusHub` code review, and Behavior-Tree
vs. FSM orchestration checks. None of that code exists here. `README.md:76-90` states plainly:
"**Not in this repository.** The demo shell is front end only... There is no Python here" and points
to `TerAustralis-Incognita-Code` under `core/crystal-core/services/` for the actual pipeline.
`celestial/atlas.js:6-8` similarly disclaims: "Starlines remain the connecting paths in the bus, and
this is a stellar projection laid over that idea, not a second meaning for the word."

**Recommendation:** Whoever scoped this review (or any future one) should target
`TerAustralis-Incognita-Code` for the `ConsentGate`/`BusHub`/`StarlineWeaver`/orchestration checks —
they cannot be answered from this repo. Flagging this here rather than fabricating findings against
code that isn't present is itself the Belt-Three discipline the brief asks this review to enforce:
treating an assumed architecture as verified when it wasn't measured would be exactly the failure
mode `PRECEDENTS.md` warns about (Apian's unmeasured Empyrean, drawn "in the same ink" as the
measured orbits).

**Mitigation applied in this PR:** the repository's own scope confusion (what led to this finding)
can't be un-created, but the recurrence risk is addressed — README.md now opens with a prominent
warning, immediately below the one-line description, stating plainly that
CrystalBus/CrystalBridge/ConsentGate/StarlineWeaver are not in this repository and naming where they
actually live. This closes former open question 4 below. The underlying scoping decision (Finding 1
itself) is still something for whoever assigns future reviews to act on, not something a README note
can fix on its own.

### Finding 2 — Demo shell's illustrative claims are inconsistently labelled as illustrative
**Severity: Low · Belt: Vision/Story presented adjacent to Science-flavoured UI · Status: FIXED (RFC-001 / `sim/parameters.yaml` items) in this PR**

`index.html` and `app.js` are careful in several places ("Illustrative only... Mainnet HOLD",
`index.html:182`; "Demo balances only", `index.html:18`; footer "not production · authority HOLD",
`index.html:246`). But some UI copy states specific-sounding operational facts with no such
qualifier:

- `app.js:521-524`: clicking "Grant hub capability" logs `"capability grant issued (15m)"` and shows
  a toast reading `"Demo: capability grant issued (15m)"` — the toast says "Demo", but the event-log
  line that persists in the on-page log does not.
- `index.html:134`: "Service receipts (**RFC-001** demo)" — names a specific RFC that is not present
  in this repo and not confirmed elsewhere in this review's scope.
- `index.html:182`: "production uses `sim/parameters.yaml` + dual-sig receipts" — names a file path
  that does not exist in this repository; not verified to exist anywhere.
- `index.html:207`: "H3 / PostGIS (target)" is correctly marked as a target (good practice), but sits
  next to "RFC-001" and `sim/parameters.yaml`, which are not similarly marked.

None of this is a serious violation — the page is saturated with "(demo)"/"HOLD"/"illustrative"
language overall — but a reader skimming only the receipts or wallet panels could walk away
believing a real capability-grant/revocation mechanism and a ratified RFC exist behind the demo.
Given this project's own rule ("never let a dreamed line pretend it was measured"), the specific,
falsifiable-sounding identifiers (RFC numbers, file paths) are the ones most likely to be quoted out
of context later.

**Recommendation:** Either (a) add a one-line "Referenced but not in this repository" note near the
Receipts and Economics panels (mirroring the discipline already used in README.md's "Related
backend" section and `BUILD_MANIFEST.json`'s `"unverified"` block), or (b) drop the specific
identifiers (RFC-001, the `sim/parameters.yaml` path) from UI copy until they are confirmed to exist,
consistent with how `BUILD_MANIFEST.json:24-27` already handles two other unconfirmed references.

**Fix applied in this PR (option b, for the two unconfirmed identifiers only):**
- `index.html:134` — "Service receipts (RFC-001 demo)" → "Service receipts (demo)". The RFC number
  is dropped rather than kept and caveated, since this review could not locate an RFC-001 anywhere in
  scope to link to or confirm.
- `index.html:182` — "production uses `sim/parameters.yaml` + dual-sig receipts" →
  "the real burn/mint pipeline and its parameters are not in this repository", keeping the
  "Illustrative only... Mainnet HOLD" framing either side of it.
- **Not changed:** the `app.js:521-524` capability-grant event-log line (the toast already says
  "Demo:"; only the persisted log line lacks it) was flagged above but was outside the specific scope
  the repo owner asked to be fixed in this pass — left as a recommendation, not applied.
- **Not changed:** `index.html:207` "H3 / PostGIS (target)" was already correctly marked and needed
  no change.

### Finding 3 — Broken relative link in the footer
**Severity: Low · Correctness bug, verified · Status: FIXED**

`index.html:247`: `<a href="../../docs/FULL-STACK-v0.3.md">docs</a>`. `index.html` is served from
the site root (both GitHub Pages at
`https://crystalarchitect.github.io/CrystalCore-Starlines-and-Dreamlines/` and the Vercel PR
preview). Two levels of `../` from a root-level page resolve above the site's own domain root, and
in any case `docs/FULL-STACK-v0.3.md` is not a tracked file in this repository (`git ls-files | grep
FULL-STACK` returns nothing). This link 404s wherever it is clicked. It is the same class of failure
`GROK_BUILD.md:70-80` already documents in detail for `celestial/overlay.html` vs. `cleanUrls` —
worth applying that same care here.

**Fix applied in this PR:** removed the dead link and replaced it with plain text noting the docs are
not part of this repository, matching the pattern already used in README.md's "Related backend"
section. See the diff to `index.html`.

### Finding 4 — Possible naming friction: "Starline Consent Transport Protocol"
**Severity: Info / needs an architect decision · Belt: Vision, flagged for Docs-governance**

`celestial/VISION-Four-Pillars.md:63-66` mentions, as background for why "AERIS" is not this file's
free-standing dream layer: *"AERIS is an edition name — `CrystalCore.OS AERIS / VAULT 12`, heading
the **Starline Consent Transport Protocol**..."* This is reported by that file as an observation
about code/branding elsewhere, not asserted or built here, and the file is correctly filed under
Belt: Vision. But under the project's own convention — Starline is the *map*, Dreamline is the
*traveller carrying memory node to node* — a protocol whose job is *transporting consent* (a payload
moving between nodes) sounds like Dreamline Train territory (`consent_transport/`), not Starline
territory. This repo has no authority over that naming (it isn't built here), so this is recorded as
an open question rather than a finding against this codebase.

**Recommendation:** Whoever owns `CrystalCore.OS AERIS` / `VAULT 12` should confirm whether "Starline
Consent Transport Protocol" is an intentional, distinct third thing, or a naming drift against the
Starline/Dreamline split that should be corrected before it propagates further (it has already
reached this repo's Vision doc as a quoted fact).

### Finding 5 — No violations found in the areas this repo *can* be checked against
**Severity: N/A (negative finding, recorded for completeness)**

- **Locked names:** No redefinition of TerAustralis Incognita, CrystalVision, or
  CrystalCore.Lattice found. `NOTICE:1-2` and `index.html:85-89` use "Crystal Vision" / "CrystalCore"
  consistently with the locked meanings.
- **No LLM carries a Crystal name:** grepped the full repo; no model/provider identifier is prefixed
  or suffixed with "Crystal" anywhere.
- **"Songline":** does not appear anywhere in the repository except the one sanctioned line in
  `celestial/atlas.test.js:570` that names the rule itself (`/\bsonglines?\b/i` matches nothing else;
  confirmed by both the test passing and an independent `grep -rni songline .`).
- **Australian/British spelling:** consistently used throughout `celestial/` ("organise" is not
  present to check, but "colour" appears at `celestial/wheel.js` CSS-adjacent prose and
  `overlay.html` styling comments use "colour"; no American-spelling drift spotted in prose files).

## Open questions for a human architect

These two remain genuinely open — they name decisions that belong to other repositories or to
whoever owns the Vercel project, not something this repository or this review can resolve on its
own:

1. **Is the Vercel `aeris-protocol` project (per `BUILD_MANIFEST.json:19-23` and
   `GROK_BUILD.md:65-67`) still the intended PR-preview target?** Both files note this was "observed
   from PR deployment notifications, not from a Vercel API call" — worth confirming from the Vercel
   dashboard directly rather than carrying the same unverified note forward indefinitely.
2. **Is "Starline Consent Transport Protocol" a confirmed, separate name, or naming drift against the
   Starline/Dreamline split?** See Finding 4 — this needs a decision from whoever owns
   `CrystalCore.OS AERIS`, not this repository.

**Resolved in this PR:**

- ~~Should `RFC-001` and `sim/parameters.yaml` be linked to their real locations, or removed from UI
  copy?~~ Removed from UI copy — see Finding 2.
- ~~Should the README more prominently warn reviewers that the CrystalBus/CrystalBridge
  implementation is not here?~~ Added — see Finding 1's mitigation note and the new banner at the
  top of README.md.

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059
