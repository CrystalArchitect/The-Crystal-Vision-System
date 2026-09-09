# Architecture review — teraustralis-incognita-v2

**Label: mixed.** The findings below are Science (grep/read evidence against
files in this repository and its siblings, cited by path). The severity
judgements are this reviewer's Docs-governance opinion, applying the
project's own written conventions. No Vision content is presented as fact.

**Date:** 2026-08-26
**Reviewer:** Independent architecture pass (fresh, no prior Grok review to
build from — none exists in this repository or its git history)
**Scope:** `teraustralis-incognita-v2` at commit `54742b1` (branch `main`),
cross-checked against `TerAustralis-Incognita` (umbrella/canon) and
`TerAustralis-Incognita-Code` (engine) as of the same date.

---

## Summary

`teraustralis-incognita-v2` is a small, self-contained React 19 + Vite
marketing/mythos website (hero, feature cards, a Codex reader for narrative
chapters) — it contains none of the CrystalBus/CrystalBridge/ConsentGate/
consent-transport engine code that lives in `TerAustralis-Incognita-Code`.
It is **not** a v2 of that engine, and canon does not treat it as one: the
umbrella repository's own `docs/adr/ADR-0015.md` (accepted 2026-08-19)
already surveys it and states plainly, "`teraustralis-incognita-v2` is not a
fourth OS and not a successor. It is stalled. Resume there only by
maintainer decision. Default for new engineering is `-Code`." So the
big cross-repo question this review was asked to chase — is this silent,
undocumented drift from canon — has an existing, dated answer: it isn't
silent. It's a documented, stalled, parallel experiment. What canon has
*not* yet reconciled is a handful of concrete details inside this repo
itself: broken in-app navigation, a production asset pipeline with a silent
external dependency, and unlabelled technical claims on the marketing copy.
Those are this review's real findings.

## What "v2" actually is (and isn't)

- **Not a successor repo.** `ADR-0015.md` (`TerAustralis-Incognita/docs/adr/ADR-0015.md`,
  lines 35, 74-76) lists it in the "Private, living" table as
  `2026-08-05 | Stalled 15 days. A second tree, not a successor` and states
  in the Decision section: *"`teraustralis-incognita-v2` is not a fourth OS
  and not a successor... Default for new engineering is `-Code`."*
  `docs/architecture/CYBERNETICS-VSM.md` (line 85-86) repeats the same
  classification.
- **Licensing was already reconciled, at the canon level.** `ADR-0013.md`
  (`TerAustralis-Incognita/docs/adr/ADR-0013.md`, lines 76-82, 107-108)
  documents that this repo shipped no `LICENSE` at all and declared
  `"license": "MIT"` in `package.json` with no MIT text anywhere — "an
  unbacked claim" — and mandated the fix. That fix is visible in this
  repo today: `package.json:5` reads `"license": "CC-BY-NC-ND-4.0"`,
  and `LICENSE`/`NOTICE` at the root match the portfolio-wide text and
  cite ADR-0013 by name. **This part of the cross-repo relationship is
  healthy** — a real ADR named the problem and the repo shows the fix.
- **What's actually in the repo**: `client/` (React 19 + wouter + shadcn/ui
  marketing site), `server/` (a four-line Express static-file server,
  `server/index.ts`), `shared/const.ts` (two unused constants). No backend
  logic, no consent gate, no bus, no P2P transport — none of the locked
  component names' actual implementations exist here, nor should they
  per the repo's own scope.
- **The repo's own docs already flag one specific piece of drift
  correctly**, in the Incognita Rule's own voice:
  `docs/TARGET-APP-STRUCTURE-2026-08-05.md` (lines 1-9) labels itself
  "Vision" up front and explains that a newer local build's `App.tsx`
  (with `/crystalcore-os`, `/gallery`, `SoundscapeProvider`) was supplied
  from *outside* this repository's git history and has not been synced in
  — "the router actually in `client/src/App.tsx` is the surveyed state...
  the two must not be confused." This is exactly the labelling discipline
  the project asks for, and it is the one existing doc that already does
  the cross-repo-drift bookkeeping this review was asked to check for.

## Strengths

- **The Incognita Rule is followed, not just known, in at least one doc.**
  `docs/TARGET-APP-STRUCTURE-2026-08-05.md` explicitly marks a
  externally-supplied file as Vision and states the delta against the
  surveyed router in a table — the right pattern, and worth repeating
  elsewhere in this repo (see Finding 4).
- **CI actually gates the build.** `.github/workflows/ci.yml` runs
  `pnpm install --frozen-lockfile`, `pnpm run check` (`tsc --noEmit`), and
  `pnpm run build` on every push/PR to `main` — a real, if thin, safety net,
  and its comments explain *why* each choice was made (no explicit pnpm
  version because `packageManager` already pins one; `--frozen-lockfile`
  specifically to catch lockfile drift).
- **The editor-tooling gate on `vitePluginManusRuntime` is done right.**
  `vite.config.ts` (lines 206-224) gates the 367 KB Manus runtime script on
  Vite's `command === "serve"` rather than `process.env.NODE_ENV`, with a
  comment explaining exactly why that distinction matters for "third-party
  JavaScript running for every visitor." This is competent, documented
  hygiene — which makes Finding 3 below (an *adjacent* piece of scaffold
  that got the same treatment only halfway) a real regression against the
  standard this same file sets for itself.
- **An `ErrorBoundary` wraps the whole app** (`client/src/App.tsx:32`,
  `client/src/components/ErrorBoundary.tsx`), so a render crash produces a
  recoverable screen instead of a blank page.
- **No hard violations of the two brightest lines.** No locked name
  (TerAustralis Incognita, CrystalVision, CrystalCore.Lattice) is
  redefined anywhere in this repo, and "Songline" is never used as a
  component, route, or variable name in code — only as mythos prose (see
  Finding 5 for the one place this gets close).

## Findings

### Finding 1 — Primary navigation is broken; three of four nav links and the homepage's main CTA 404 (High)

`client/src/components/Navbar.tsx` (lines 20-23) links to `/codex`,
`/starline`, `/gallery`, `/archive`. `client/src/pages/Home.tsx` (lines
107-112) links "LAUNCH TERMINAL" to `/crystalcore-os`. But the live router,
`client/src/App.tsx` (lines 12-23), only registers `/`, `/codex`,
`/codex/:collection/:chapter`, and `/404` — every unmatched path falls
through to the final wildcard `<Route component={NotFound} />` (line 20).
So `/starline`, `/gallery`, `/archive`, and `/crystalcore-os` all resolve to
a 404 page today. Two buttons compound this: "INITIALIZE BOOT"
(`Home.tsx:43-46`) and "BOOT OS" (`Navbar.tsx:27-29`) are `<Button>`
elements with no `onClick` at all — they render but do nothing.

This is exactly the gap `docs/TARGET-APP-STRUCTURE-2026-08-05.md` already
describes as future work (a `Terminal` and `Gallery` page, a
`/crystalcore-os` route) — but that doc doesn't mention `/starline` or
`/archive`, and the shipped `Navbar` links to both anyway. So even against
the repo's own stated target, `/starline` and `/archive` are additional,
undocumented dead links.

**Recommendation:** Either stop linking to routes that don't exist yet
(comment them out or gate behind a "coming soon" state) or build the
`Terminal`/`Gallery`/`Archive`/`Starline` pages per the target doc. Wire
the two dead buttons to at least scroll-to or route to something. This is
the single most visible defect a visitor would hit in the first 30 seconds
on the site.

### Finding 2 — Hero, footer logo, and terminal-preview images depend on a dev-only proxy to an external SaaS storage backend, with no production path (High — also an architecture-constraint violation)

`Home.tsx` references `/manus-storage/hero-bg_0d7db17d.png` (line 16),
`/manus-storage/terminal-view_e65fbd0c.png` (line 94), and
`/manus-storage/logo_d35dd45c.png` (line 124; also in `Navbar.tsx:10`).
None of these files exist anywhere in the repository — `client/public/`
contains only `.gitkeep` and the `__manus__/` debug script (confirmed by
directory listing). The only thing that ever resolves `/manus-storage/*`
is `vitePluginStorageProxy` in `vite.config.ts` (lines 153-204), which
proxies each request to `process.env.BUILT_IN_FORGE_API_URL` (an external
"Forge" storage API) using `process.env.BUILT_IN_FORGE_API_KEY` — and that
plugin is registered only under `configureServer`, which Vite runs for the
dev server, never for a production build (`vite.config.ts`'s own comment on
line 217-218 says as much for the neighbouring debug collector: "hang off
`configureServer`, which never runs during a build").

`server/index.ts`, the production server, is a plain
`express.static(dist/public)` file server with a catch-all that serves
`index.html` for anything unmatched (lines 19-24) — there is no
`/manus-storage` route in it. So in a production deployment, a request for
`/manus-storage/hero-bg_0d7db17d.png` returns `index.html` (HTML, status
200) instead of an image: the hero background, the footer logo, and the
CrystalCore terminal screenshot are all broken in any real deployment of
this build, and the failure mode (HTML masquerading as an image, not a
404) makes it easy to miss in casual QA.

This is also a direct hit against the project's own written architecture
constraints (Section 6 of the `teraustralis` skill / project conventions):
*"Local-first — core function does not require continuous external
links"* and *"Sovereignty is the default — silent dependency and soft
lock-in are architectural failures."* A visitor's browser (in production)
would not even attempt the external call — the images are just gone — but
the *authoring/build* pipeline for this repo's core visual identity is
silently coupled to a third-party vendor's live API, undocumented anywhere
in `README.md` or `docs/`.

**Recommendation:** Commit the actual image assets into `client/public/`
(or another checked-in location) and reference them by a stable local
path, removing the runtime dependency on `BUILT_IN_FORGE_API_URL` entirely.
If the images must stay externally hosted for size reasons, add a real
production route/CDN redirect for `/manus-storage/*` and document the
external dependency explicitly, rather than leaving it to be discovered by
a broken hero section.

### Finding 3 — Debug/session-recording script ships as a reachable static file in production, half-gated (Low)

`client/public/__manus__/debug-collector.js` is 800+ lines of console,
network (fetch/XHR, request+response bodies), and full UI-event (click,
input value, scroll, navigation) capture, reporting to `/__manus__/logs`
every 2 seconds. Injection into `index.html` *is* correctly gated to
non-production (`vitePluginManusDebugCollector.transformIndexHtml`,
`vite.config.ts` lines 81-84: `if (process.env.NODE_ENV === "production")
return html;`), so it does not auto-run for site visitors. But because the
file lives under `client/public/`, Vite copies it verbatim into
`dist/public/__manus__/debug-collector.js` regardless of environment — it
is a publicly fetchable static file on the deployed site, and its own
report endpoint (`/__manus__/logs`) is not wired up in production either
(the plugin's `configureServer` handler is dev-server-only, per Finding 2's
same mechanism), so the residual risk is "dormant unless someone links to
it," not "silently active." Given the file's stated purpose is full session
replay including input values, and the project's convention treats
"consent as a runtime property, not a policy document," a leftover capture
script — even inert — sitting in the production static tree is worth
cleaning up rather than trusting the injection gate alone.

**Recommendation:** Exclude `client/public/__manus__/` from the production
`vite build` output (e.g. move it out of `public/` into a dev-only asset
path, or filter it in the build step) so it isn't shipped as a static file
at all when `NODE_ENV=production`.

### Finding 4 — No Belt-Three labelling anywhere on the live site; one feature card states a specific technical claim this repo does not implement (Medium)

Unlike the canon repositories — `TerAustralis-Incognita/README.md`'s
explicit "What's real vs. what's vision" table, and this repo's own
`docs/TARGET-APP-STRUCTURE-2026-08-05.md` — nothing in the rendered site
(`Home.tsx`, `Navbar.tsx`, `client/src/data/mythos.ts`) distinguishes
Science from Vision/Story for a visitor. That's defensible for the mythos
chapters themselves (`mythos.ts`) — they read as story and are filed under
`category: "codex" | "transmissions" | "archive"`, which is itself a kind
of labelling. It's less defensible for the feature grid on the homepage,
which reads as a capabilities list:

> "**Starline Protocol** — P2P decentralized communication using Noise IK
> handshakes for secure, unbought interaction." (`Home.tsx`, lines 74-77)

"Noise IK handshakes" is a specific, checkable technical claim (Belt: 
Science, if true). It *is* true of the umbrella project — real, per
`TerAustralis-Incognita-Code/README.md` line 41, in
`core/crystal-core/consent_transport/` — but nothing in this repository
implements it, links to it, or notes that it lives elsewhere. A visitor
reading this card on `teraustralis-incognita-v2` has no way to tell this
apart from the "Emotion Warehouse" card next to it, which is unambiguously
a design concept with no implementation anywhere in the portfolio that this
review found. Per the project's own test ("can this be executed or checked
against the world?"), the Starline Protocol card should either link to
where it's real (`TerAustralis-Incognita-Code`) or drop the specific
protocol detail if this page is meant purely as mythos.

**Recommendation:** Add a one-line status/label convention to the feature
grid (even something as small as a "Built in `-Code`" vs. "Vision" tag per
card), matching the discipline `TARGET-APP-STRUCTURE-2026-08-05.md` already
uses for the router delta.

### Finding 5 — "Songline Dividers" proposed as a named UI element in `ideas.md`; not implemented, but a live risk if it is (Medium — process, not yet a violation)

`ideas.md` line 43 proposes, under "Signature Elements": *"**Songline
Dividers**: Animated, glowing lines that separate sections instead of flat
borders."* Grep across `client/`, `server/`, and `shared/` (`.tsx`/`.ts`
files) confirms this was never implemented — no component, class, or
variable named `Songline*` exists in code today. The two other uses of
"Songline" in this repo are narrative prose, not component names —
`client/src/data/mythos.ts:80` ("Between the Songlines and the
Starlines") and `Home.tsx:39` ("Bridging ancient Songlines with the reach
for the deep black") — which the project's own convention treats as
acceptable ("honoured as cultural image, never claimed"), so those two are
not findings.

The design doc line is different in kind: it names a *UI component* after
Songlines, which is precisely the thing the project's Indigenous Data
Sovereignty boundary rules out — "Songline" is never a component name,
full stop, regardless of intent. It was not carried into code, so this is
not yet a violation, but `ideas.md` is a live design-ideas document in this
same repo, one implementation pass away from becoming one.

**Recommendation:** Rename the "Songline Dividers" idea to a project
coinage (e.g. "Starline Dividers" — consistent with the rest of this same
doc's "Starline Violet" accent and "Dreamline curves" language two lines
above it) before anyone builds it.

### Finding 6 — LICENSE references files that don't exist in this repository (Low)

Root `LICENSE` (lines 26-29) reads: *"EXCEPTIONS — The following material
is licensed separately: `mythos/` directory: CC BY-NC-ND 4.0 (see
`LICENSE-CONTENT.md`); Concepts inspired by MemClaw: Acknowledge MemClaw's
Apache 2.0 license (see `docs/ATTRIBUTIONS.md`)."* This repo has no
`mythos/` directory (its mythos content is `client/src/data/mythos.ts`), no
`LICENSE-CONTENT.md`, and no `docs/ATTRIBUTIONS.md` — confirmed absent by
directory search. Byte-diffing against `TerAustralis-Incognita/LICENSE`
shows this file is an exact copy of the umbrella repo's `LICENSE`, which
*does* have a `mythos/` directory and a real `docs/ATTRIBUTIONS.md`
(MemClaw attribution). The portfolio-wide licence text applying here is
correct per ADR-0013; the repo-specific "Exceptions" paragraph is stale
boilerplate that doesn't describe this repository.

**Recommendation:** Either remove the two dangling exception references
(if this repo has no MemClaw-derived code and no separately-licensed
content) or add the missing files if the exception genuinely applies.

### Finding 7 — Miscellaneous scaffold cruft (Low)

- `README.md` referenced a file, `TERAUSTRALIS_V2_COMPLETE_SOURCE.md`,
  that does not exist anywhere in the repository or its git history
  (confirmed by `find`). Left as-is per this review's scope (not touched
  in the accompanying commit — flagging rather than deciding whether the
  file should be restored or the reference removed).
- `client/src/const.ts` exports `getLoginUrl()`, building an OAuth
  redirect against `VITE_OAUTH_PORTAL_URL`/`VITE_APP_ID`; grep across
  `client/` and `server/` finds zero callers, and `server/index.ts` has no
  `/api/oauth/callback` route to receive the redirect it constructs. This
  is unused generator scaffolding.
- `vitest` is a `devDependency` (`package.json` line 89) with zero test
  files anywhere in the repo (`find . -iname "*.test.*" -o -iname
  "*.spec.*"` returns nothing). Either add tests or drop the dependency.
- **Already fixed, noted for completeness:** the README's literal `\n`
  escape-sequence corruption (the whole file was one line with literal
  backslash-n characters instead of real newlines) is fixed in the commit
  accompanying this review — a pure formatting fix, no content changed.

## Open questions for a human/architect

1. **Is `teraustralis-incognita-v2` still meant to resume, per ADR-0015's
   "resume there only by maintainer decision," or has that decision now
   been made either way?** This review found no ADR or commit message
   updating that status since ADR-0015 (2026-08-20); the repo's last
   content commit (`d8c4549`, installing the `web-os-easter-eggs` skill and
   shelving the target-app-structure doc) is dated in that same window and
   reads as continued, if slow, investment — worth reconciling with the
   "stalled" label rather than guessing which is current.
2. **Should this repo's homepage even carry a "Starline Protocol" feature
   card describing `-Code`'s implementation (Finding 4), or was that
   supposed to be removed/genericized when v2 was declared "not a
   successor"?** Not answered by anything this review found — flagging
   rather than assuming.
3. **Is the `manus-storage` proxy (Finding 2) intentional for a
   Manus-hosted deployment target** (i.e., is this site only ever deployed
   *inside* the Manus platform, where the proxy or an equivalent exists
   server-side, rather than via the checked-in `server/index.ts`)? If so,
   the finding's severity changes from "broken in production" to
   "undocumented deployment assumption," but this review found nothing in
   `README.md`, `docs/`, or `package.json` scripts confirming or denying
   that.
4. **Does the `web-os-easter-eggs` skill's planned consumer, the
   `/crystalcore-os` Terminal page (Finding 1 / `TARGET-APP-STRUCTURE-2026-08-05.md`),
   have an owner and timeline**, or is it also stalled alongside the rest
   of the repo per ADR-0015?

---

*Non Solus.*
