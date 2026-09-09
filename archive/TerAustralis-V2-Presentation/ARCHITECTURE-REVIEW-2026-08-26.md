# Architecture review — teraustralis-v2-presentation

**Label: mixed.** The findings below are Science (grep/read evidence against
files in this repository and its named siblings, cited by path — every
sibling-repo claim was independently re-verified in this session, not taken
on trust from any other review). The severity judgements are this reviewer's
Docs-governance opinion, applying the project's own written conventions. No
Vision content is presented as fact.

**Date:** 2026-08-26
**Reviewer:** Independent architecture pass (fresh — no prior review exists
in this repository or its git history; confirmed by `find` and `git log`)
**Scope:** `teraustralis-v2-presentation` at commit `7b58f4f` (branch
`master`), a 13-slide HTML deck plus a speaker script and two duplicate
speaker-notes files. Cross-checked against `teraustralis-incognita-v2` (the
website the deck describes), `teraustralis-incognita-code` (the CrystalCore
engine), `TerAustralis-Incognita` (umbrella/canon), and `TheCrystalVision`
(a same-org but unrelated repo, checked because the deck names it).

This repo is treated as outward-facing pitch/proposal material per the task
brief, not application code — the review below weighs claims discipline and
labelling accordingly, over code style.

---

## Summary

This is a competently built, self-contained 13-slide HTML deck ("Source Code
Deep Dive") narrating the architecture of a sibling repository,
`teraustralis-incognita-v2`. Most of its concrete technical claims about that
site — React 19, Vite, Tailwind CSS 4, Framer Motion, Wouter, the OKLCH
palette, the Playfair Display/Space Grotesk/Inter font stack, the
`App.tsx`/`Navbar.tsx`/`mythos.ts`/`Codex.tsx`/`CodexReader.tsx` file layout —
check out against that repo's actual `package.json` and source, which is a
real strength worth naming. But the deck's single "Architectural Foundations"
slide and its "Landing Page" slide launder two real capabilities that exist
only in *other, unconnected* portfolio repositories (a Python Noise-IK
transport in `teraustralis-incognita-code`, a dbt emotion-warehouse in
`TerAustralis-Incognita`) into what reads as the shipped architecture of the
specific website being walked through — which has no P2P, ML, or network code
of any kind, only a four-line static-file Express server. Layered on top: the
closing slide names a wrong, private, and unrelated GitHub repository while
calling the work "open-source" under a license that structurally cannot be
open source, and asserts a version string that appears nowhere in the actual
codebase. These are the review's four high-severity findings, all under the
project's own Belt-Three and claims-discipline rules.

## Strengths

- **Most of the frontend stack claims are accurate and independently
  verified**, not just plausible-sounding. `architecture.html` claims React
  19, Tailwind CSS 4, Framer Motion, Wouter, and OKLCH; `teraustralis-incognita-v2/package.json`
  confirms `react@^19.2.1`, `tailwindcss@^4.1.14`, `framer-motion@^12.23.22`,
  `wouter@^3.3.5`. `design_aesthetic.html`'s font claims (Playfair Display /
  Space Grotesk / Inter) match `client/index.html`'s Google Fonts `<link>`
  and `client/src/index.css`'s `--font-serif`/`--font-mono` tokens exactly.
- **The file-level walkthrough is real, not invented.** `App.tsx`,
  `Navbar.tsx`, `mythos.ts`, `Codex.tsx`, `CodexReader.tsx` all exist at the
  paths the deck implies, and `app_structure.html`'s
  `ErrorBoundary > ThemeProvider > TooltipProvider > Router` nesting matches
  `client/src/App.tsx` line for line.
- **The one slide that is explicitly forward-looking is honestly labelled.**
  `future_directions.html` uses "Future Directions & Vision" as its title and
  future-tense language throughout ("We plan…", "Deployment of…", "Continued
  refinement of…") for the OS-terminal integration, the D3.js visualizations,
  and the sovereign-AI roadmap — none of which this review found built. That
  is exactly the Belt-Three discipline (mark the dreamed line as dreamed) the
  rest of the deck's "Architectural Foundations" slide (Finding 1) fails to
  apply to *current*-tense claims.
- **No locked-name redefinition and no "Songline" component-naming** anywhere
  in this repository's own files (verified by grep across every `.html`,
  `.md`, and `.json` file) — the one hard line the brief asked to check
  hardest against is clean in this specific repo.
- **The prior PR (#1, `581d2e5`) already did real security hygiene**: it
  removed two unused, unpinned CDN `<script>` tags (d3, Chart.js) present on
  every slide with zero actual usage, and added the missing `LICENSE`/`NOTICE`
  pair per ADR-0013. That work holds up under a second look — both scripts
  are confirmed absent from every slide today, and the license text matches
  the portfolio-wide standard.

## Findings

### Finding 1 — "Architectural Foundations" and the landing-page feature grid present two other repositories' real capabilities as this website's own shipped architecture (High — Belt-Three)

`architecture.html` lists six items under one undifferentiated
"Architectural Foundations" heading:

> React 19 (Vite) · Tailwind CSS 4 · Framer Motion · Wouter · OKLCH Color
> Space · **Noise Protocol (Noise_IK): Secure P2P communication architecture**

The first five are real, current, in-tree dependencies of
`teraustralis-incognita-v2` (verified above). The sixth is not — that
repository has no networking code beyond a four-line
`express.static()` file server (`server/index.ts`, confirmed in full), no
P2P library, no cryptography dependency, and no `noise`-related import
anywhere in `client/` or `server/` (confirmed by repo-wide grep). "Noise IK"
*is* real, current code — but in a completely different repository,
`teraustralis-incognita-code/core/crystal-core/consent_transport/`
(`noise.py`, `protocol.py`, `transport.py`, documented in that repo's
`README.md` line 41 as "Starline P2P: Noise IK + ML-KEM-768"). The same
pattern repeats on `landing_page.html`, which reproduces `Home.tsx`'s
"Emotion Warehouse — Local-first active learning models for data
sovereignty" card: no ML/active-learning code exists anywhere in
`teraustralis-incognita-v2` (confirmed by grep), but an "Emotion Warehouse"
*does* exist for real, as a dbt data-warehouse project with an
`active_learning` mart, in the umbrella repo
(`TerAustralis-Incognita/dbt/crystalcore_emotion_warehouse/`).

The project's own test is "can this be executed or checked against the
world?" Both claims pass that test individually — but only against a
repository this deck never names, while being presented, on a slide titled
"Architectural Foundations" of *this* website, as if they were part of the
same build as React and Tailwind. A reader has no way to tell "Noise_IK" and
"OKLCH Color Space" apart on that slide — one is this site's real dependency,
the other is a different Python project's protocol with zero call path into
the site being described. That is the Incognita Rule's exact failure mode:
a dreamed (or at least *elsewhere-built*) line, standing next to surveyed
ones with no seam visible.

**Recommendation:** Split the slide, or add a one-line qualifier per item —
e.g. "Noise Protocol (Noise_IK) — implemented in `crystal-core`, not yet
wired into this site" — matching the labelling discipline
`teraustralis-incognita-v2/docs/TARGET-APP-STRUCTURE-2026-08-05.md` already
uses for its own router-drift table. Do the same for "Emotion Warehouse" on
`landing_page.html`.

### Finding 2 — Closing slide names a nonexistent/wrong GitHub repository, then calls the (private, no-derivatives) work "open-source" (High — claims discipline)

`q_and_a.html` and `TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md` §13 both state:

> "REPOSITORY: CrystalArchitect/The-Crystal-Vision" / "Our work is
> open-source, available on the CrystalArchitect/The-Crystal-Vision
> repository, and we're currently on LATTICE_SYNC v2.0.0-STABLE."

Three independent problems, each checked directly:

1. **`CrystalArchitect/The-Crystal-Vision` does not exist.** The org's real
   repo list (`list_repos`) has `CrystalArchitect/TheCrystalVision` (no
   hyphens) — a *different string* than the one printed on the slide.
2. **Even the correctly-spelled repo is the wrong one.** `TheCrystalVision`
   contains `clementine/`, `campaigns/`, `asset-packs/`, `operator-card/`,
   `cli/` — none of the files this deck walks through (`App.tsx`,
   `mythos.ts`, `Codex.tsx`, `CodexReader.tsx`) exist there (confirmed by
   `find`). Those files live in `teraustralis-incognita-v2`, whose own
   `README.md` explicitly cross-links "the presentation repository" as
   `github.com/CrystalArchitect/teraustralis-v2-presentation` — this repo —
   not `TheCrystalVision`.
3. **Neither candidate repository is public.** `list_repos` shows both
   `teraustralis-incognita-v2` and `TheCrystalVision` as `"visibility":
   "private"`. This repository's own `LICENSE` is CC BY-NC-ND 4.0 — "No
   derivative redistribution" — which is not an OSI-approved open-source
   license by definition (the Open Source Definition requires deriv­ative
   works be permitted). "Open-source" is therefore incorrect on two
   independent grounds: the named repo can't be reached, and the license on
   the actual code forbids what open-source licensing requires.
4. **`LATTICE_SYNC v2.0.0-STABLE` has no source.** `teraustralis-incognita-v2/package.json`
   reports `"version": "1.0.0"`; there are no git tags in that repo
   (`git tag -l` returns nothing); the string `LATTICE_SYNC` does not appear
   anywhere in `teraustralis-incognita-v2`, `teraustralis-incognita-code`, or
   `TerAustralis-Incognita` (repo-wide grep, zero hits). This is a specific,
   dated-sounding status claim with no backing artifact anywhere this review
   could find.

**Recommendation:** Point the slide at the correct, real, currently-linked
repo (`CrystalArchitect/teraustralis-v2-presentation` and/or
`teraustralis-incognita-v2`, whichever the team wants public); drop "open-
source" unless a public, permissively-licensed mirror actually exists; drop
or re-source the version string. This is the single most consequential
finding for a live pitch — an engaged audience member typing the printed
name will get a GitHub 404.

### Finding 3 — Broken image references on 5 of 13 slides; no image asset ships in this repository (High — presentation-breaking)

`title_slide.html`, `q_and_a.html`, `navigation.html`, and `landing_page.html`
(twice) all reference `/manus-storage/...png` as an absolute root path:

```
<img src="/manus-storage/logo_d35dd45c.png" alt="TerAustralis Incognita Logo" class="logo" />
<img src="/manus-storage/hero-bg_0d7db17d.png" alt="Hero Background" class="hero-preview">
<img src="/manus-storage/terminal-view_e65fbd0c.png" alt="Terminal View" class="terminal-preview">
```

No `.png`/`.jpg`/`.svg`/`.webp` file exists anywhere in this repository
(confirmed by `find`). `/manus-storage/` is an authoring-tool-only proxy path
(the same mechanism flagged as Finding 2 in the sibling
`teraustralis-incognita-v2` architecture review dated the same day — that
proxy is dev-server-only there too). Opened as plain files, from a clone, or
served by any static host other than the original authoring session, five of
these thirteen slides render with a broken-image icon where the logo, hero
background, and terminal screenshot should be — including the title slide
and the closing Q&A slide, the two moments a live audience is most likely to
be looking at the screen.

**Recommendation:** Export the actual image assets from the authoring tool
and commit them into this repository (e.g. an `assets/` directory), then
point the five `<img>` tags at the relative, checked-in path. Not fixed in
this review's commit — no source image was available to fetch, and guessing
a placeholder would misrepresent the deck's real visual content.

### Finding 4 — Two duplicate speaker-notes files number the same 13 slides in a different, non-presentation order than the deck itself (Medium — doc drift)

Three files carry the same 13-slide narration: `TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md`,
`slide_notes.md`, and `slide_notes.json`. `TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md`'s
numbering (1 Introduction → 2 Overview → 3 Architecture → … → 13 Q&A)
matches the deck's actual sequence in `slide_state.json`'s `outline` array
exactly. `slide_notes.md`/`slide_notes.json`, however, number the identical
13 blocks in **alphabetical-by-filename order** instead (`1 = app_structure`,
`2 = architecture`, `3 = design_aesthetic`, … `13 = title_slide`) — so "slide
1" in this pair of files is actually the deck's *4th* slide, and "slide 13"
is its *1st* (the title slide). A presenter who picks up `slide_notes.md`
instead of the script and reads notes by number against the visual deck
would be reading the wrong notes against nearly every slide.

**Recommendation:** Either delete `slide_notes.md`/`slide_notes.json` as
superseded duplicates of the correctly-ordered script (they add no content
the script lacks), or re-key both by the deck's actual `pageNum` from
`slide_state.json` so all three files agree.

### Finding 5 — American spelling in visible, audience-facing slide text (Low — writing convention; two instances fixed in this commit)

The project's own convention (teraustralis skill, §8) specifies Australian/
British spelling ("organise, colour, recognise"). Two rendered, on-slide
instances used American spelling instead:

- `design_aesthetic.html` — visible section heading "**Color** Philosophy
  (OKLCH)" and its HTML comment `<!-- Color Philosophy -->`.
- `architecture.html` — visible body text "Perceptually uniform **color**
  for consistent aesthetics."
- `mythos_data.html` — visible body text "Data is **organized** into
  high-level collections" (a third instance, left unfixed — see below).

**Fixed in this commit:** the first two (`design_aesthetic.html`,
`architecture.html`) — pure spelling corrections (Colour/colour), no wording
or layout change, so within the "small and obviously safe" bar for an
in-review fix. **Left as a flagged finding, not fixed:** `mythos_data.html`'s
"organized," and the same American spellings repeated in
`TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md`, `slide_notes.md`, and
`slide_notes.json` ("We organize this data…", "This organization allows…") —
left for the same reason Finding 4 recommends not hand-editing the
duplicate-notes files individually: fix once, at the source, when Finding 4
is resolved, rather than three more times over.

### Finding 6 — No rights footer on the standalone script document (Low — writing convention; fixed in this commit)

Per the project's writing convention, documents carry a two-line rights
footer: `**All rights reserved.**` / `TerAustralis Incognita — ABN 70 741
068 059` (seen verbatim in, e.g.,
`TerAustralis-Incognita/research/closed-loop-embodiment.md`).
`TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md` ended only with "**Non Solus — Not
Alone.**" — no rights line. The repository's `NOTICE` file already carries
copyright and licensing text, so this is a minor, single-document gap, not a
missing-license problem. **Fixed in this commit** — the standard two-line
footer is appended below the existing mantra line; no other content changed.
Not applied to the 13 individual slide HTML fragments, since each is a
self-contained visual layout and adding a new footer element there is a
design change this review's brief reserves for human sign-off, not a
same-commit fix — flagged instead in the recommendation below.

**Recommendation (not actioned here):** Add a small ABN/copyright line to
the visual footer treatment of at least the title and closing slides when a
human next revises the deck's design, consistent with the HTML footer
pattern used elsewhere in the portfolio (e.g.
`Clementine-ai-companion/archive/crystalcore-app/codex.html`'s `<footer>`).

### Finding 7 — "Engage with the Crystal Vision" loosely conflates the umbrella pitch with the locked, narrower "Crystal Vision" project-boundary term (Low — locked-name adjacency)

`TERAUSTRALIS_V2_PRESENTATION_SCRIPT.md` §13 and both notes duplicates close
with: "We invite you to explore, contribute, and engage with the Crystal
Vision." Constitution/project-boundary convention defines **Crystal Vision**
specifically as "the user-facing application built on Crystal Core" — one
named layer of the architecture — while the pitch as a whole is titled
*TerAustralis Incognita v2*. Using "the Crystal Vision" as a stand-in for
"this whole project/pitch" doesn't redefine the locked term outright, but it
blurs the boundary the convention draws between the umbrella vision and the
one architectural layer that specifically carries that name.

**Recommendation:** Prefer a phrase that names the actual thing being
pitched — e.g. "engage with TerAustralis Incognita" or "engage with the
Incognita Lattice" — reserving "Crystal Vision" for contexts specifically
about that application layer.

### Finding 8 — Minor route-detail inaccuracy on `app_structure.html` (Low — technical accuracy)

The slide's code panel footer reads `// Routes: /, /codex, /codex/:id`.
`teraustralis-incognita-v2/client/src/App.tsx` (lines 14-16) actually
registers `/`, `/codex`, `/codex/:collection/:chapter`, and `/404`. The
simplification of a two-segment param to a single `:id` is a minor
inaccuracy, not a Belt-Three issue (it doesn't assert an unbuilt capability),
included here only because the brief asked for a hard technical
cross-check. Not fixed in this commit — pitch-content wording, reserved for
human sign-off per the task brief.

## Open questions for a human/architect

1. **Is a public mirror of `teraustralis-incognita-v2` (or this presentation
   repo) actually planned?** That determines whether Finding 2's fix is
   "correct the repo name" or "drop the open-source claim entirely until one
   exists." This review found no ADR or doc answering that either way.
2. **Should the "Architectural Foundations" and landing-page feature-grid
   slides describe `teraustralis-incognita-v2` alone, or the wider
   CrystalCore/TerAustralis portfolio it draws its mythos copy from?** If the
   deck is meant to pitch the *portfolio's* vision using this one site as a
   worked example, Finding 1's fix is a labelling/scoping change, not a
   content cut — but that intent isn't stated anywhere in this repo today.
3. **Where should the actual `/manus-storage/*` image assets be sourced
   from for Finding 3?** This review had no access to the original
   authoring session's exported files and did not want to guess placeholder
   imagery for a pitch deck's visual identity.
4. **Is `LATTICE_SYNC v2.0.0-STABLE` an internal designation tracked
   somewhere this review didn't have access to** (e.g., a deployment
   dashboard, a private changelog), or should the deck simply cite
   `teraustralis-incognita-v2`'s actual `package.json` version (currently
   `1.0.0`) instead?

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059

*Non Solus.*
