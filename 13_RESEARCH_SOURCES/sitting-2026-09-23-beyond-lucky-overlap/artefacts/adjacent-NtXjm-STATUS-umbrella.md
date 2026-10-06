# STATUS

Last updated: 2026-08-20

Full knowledge-base reconstruction: `knowledge-base/00-INDEX.md` in
CrystalCore.OS-the-Crystal-Architecture-Archive.

This file describes the state of this repository, not the ambition of
the system. Same ledger, same categories as the system ledger in
CrystalCore.OS-the-Crystal-Architecture-Archive. This is the umbrella:
canon, governance, mythos, research. The code moved out under the
Migration Plan, and the ledger reflects that.

## Running
Executes, or can be opened and used by someone other than me.

- mythos/crystalcore-os/crystalcore_os.py — the CrystalCore.OS mythos
  terminal boots, plays to the open First Gate, and saves/resumes from a
  fresh clone, stdlib-only, verified 2026-07-27
  (`python3 mythos/crystalcore-os/crystalcore_os.py`). Before this pass
  it exited 1 at import when run as a script (relative import with no
  parent package).
- research/prototypes/story-library — self-contained HTML prototype;
  no build step; renders in a headless browser, verified 2026-07-24.
- CI on main is green (run of 2026-07-23), with honest scope: the
  src/tests-dependent steps skip themselves because those trees now
  live in TerAustralis-Incognita-Code.

## Built, not currently running
Code exists and is complete enough to run. No runtime here exercises it.

- dbt/crystalcore_emotion_warehouse — a full dbt project (staging and
  mart models, macros, tests). No warehouse is configured anywhere, no
  CI runs it, and it was not executed this session.
- archive/ code (legacy/crystalcore-app; 2026/local-snapshot-2026-07-17
  with crystalcore-v0.13 and clementine.py) — quarantined by
  archive/README on purpose: provenance, not production.

## Exists as a document
The repository's actual product.

- docs/ — ADRs, the governance stack (Project-Boundaries.md,
  Migration-Plan.md, licensing), and the crystal-core architecture
  canon (Blueprint v0.3, Runtime Specification v0.3, module
  interfaces, testing specifications).
- mythos/ — content, art, crystalcore-os, teraustralis, and the
  prompt kits under mythos/tools.
- research/seven-sisters (WATER-BRIEF), CHANGELOG, the licensing and
  conduct files at root.

## Designed, not built
- Story Library production components — the prototype above is the
  reference implementation; the SvelteKit/React components it
  specifies for the live site do not exist yet.
- The workflows the mythos/tools prompt kits describe (daily-digest,
  signal-scanner) — written as kits, wired to nothing.
- The Runtime Testing Specifications describe more suite coverage than
  the code tree carries; the four passing suites are the built subset.

## Concept only
Nothing new at this tier in this repository; see the system ledger.

## Known unknowns

- What the domain serves. CNAME claims www.teraustralis.com.au, but
  the latest Pages run deployed nothing — the deploy job skipped, by
  design, because src/site is no longer in this repo, and deploy.yml's
  own notice records that the site was never in git history here. Has
  the SvelteKit site ever been live at that domain, and what is there
  now? Unverified (egress blocked from the session container).
  **Answered 2026-07-28: the site is live and serving the SvelteKit
  build.** The Code repo's `Publish site` workflow ends by probing
  `https://www.teraustralis.com.au/crystalcore-os` — a path that exists
  only in the build, chosen precisely because the failure mode it
  guards renders the README at `/` and returns 200 there. Runs at
  20:28, 20:33 and 20:39 UTC all succeeded, so that probe returned 200
  each time. The Pages source race was fixed in that repo the same day
  (#24, "Set the Pages source in code so the race stops happening").
  This entry's premise — that the latest Pages run deployed nothing —
  described `TerAustralis-Incognita`, which correctly deploys nothing;
  the site is published from `TerAustralis-Incognita-Code`, which owns
  the CNAME.

  **Re-measured 2026-08-20 (this session, from outside):**
  `https://teraustralis.com.au` returns GitHub Pages **301** to
  `https://www.teraustralis.com.au/`; www returns **200** with the
  SvelteKit build (`_app/immutable/*`, last-modified 2026-08-18).
  Code Pages settings: `cname=www.teraustralis.com.au`,
  `build_type=workflow`, TLS covers both apex and www. Apex is not a
  404 today. The remaining public collision was this umbrella's
  leftover Jekyll Pages at
  `https://crystalarchitect.github.io/TerAustralis-Incognita/`
  (`build_type=legacy`, `cname=null`) rendering the README with the
  drifted double-*a* GitHub description. `index.html` at this repo
  root now points at www instead.

  A caution recorded from getting this wrong once: PR #70's link check
  hit that same URL at 20:36 and got a 404, midway through the 20:33
  deploy. A GitHub Pages swap can 404 briefly, so a single link-check
  failure against this domain is not evidence the page is gone — the
  deploy probe, which retries twelve times, is the authority. And
  link-checking it from a session container is never valid: the agent
  proxy answers 403 to CONNECT and 403 is in `aliveStatusCodes`, so
  every URL on the domain reports alive locally regardless of truth.
- publish-packages.yml and test-packages.yml — corrected 2026-07-24:
  not dormant, removed outright at Stage 2 (commit `60a20df`,
  2026-07-23), after confirming neither had ever had a git tag to fire
  on. This line previously said "dormant by drift rather than by
  decision," contradicting Migration-Plan.md's own Stage 2 record.
  Removal was a decision, not drift.
- examples/README.md commands target src/ paths that moved to the code
  repo (the file says so itself); the index awaits re-pointing.
- teraustralis-final.html — corrected 2026-07-24: no longer presumed to
  live in an archived repo. A full six-repo search (filename, content-
  grep, and git history, including archive/ and local-snapshot
  directories) found zero copies anywhere in the portfolio. Detail in
  the Archive repo's knowledge-base.
