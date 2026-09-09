# Landing Experience — Phase I design

**Layer:** Vision (design direction) with Built annotations — the
implementation lives in
[TerAustralis-Incognita-Code](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)
at `vision/site/`, and where this document and the code differ, the code
is the source of truth.

**Origin:** the BUILD mission brief and wireframe v1 developed in the
maintainer's Grok session (2026-07-27), realized here against the site
that actually exists. The site already carries a coherent identity —
this document records it as the visual canon and specifies the Phase I
additions, rather than inventing a second identity beside it.

## Objective

Make the homepage work as a public gateway: a visitor should stop,
understand what TerAustralis Incognita is within one screen, feel the
Purpose Core directive as inspiring, and see honest paths inward.

Emotional arc: **Wonder → Understanding → Confidence → Exploration.**

## Narrative map (final)

1. **Arrival** — the mantra ("Red dust to rockets. Dreamlines to deep
   space. We are early.") holds the hero; the Purpose Core directive
   appears beneath it as the project's stated purpose. Dual CTAs:
   *Read the Codex* · *Meet Clementine*.
2. **Discovery** — the ecosystem revealed as a constellation: seven
   glowing nodes, each a real route (CrystalCore.OS, Clementine, the Codex,
   the Archive, Starline, the Gallery, Join). Every light is a door
   that actually opens.
3. **Understanding** — the principles, then the Built / Built+Vision /
   Vision separation the site already keeps (the governance principle,
   preserved and visible).
4. **Exploration** — the Archive, the Chronicle (dated from the
   repositories' own history), the Starline Transmissions.
5. **Invitation** — support, contribution, contact. Unchanged.

## Hero copy (v1)

- Headline (existing, kept): *Red dust to rockets. Dreamlines to deep
  space. We are early.*
- Directive line (added): *"Expand to the stars and thereby understand
  the Universe."* — set apart typographically as the Purpose Core.
- CTAs (existing, kept): primary *Read the Codex*, ghost *Meet Clementine*.

The Grok wireframe proposed the directive as the headline itself. The
mantra is standing Vision-layer content with its own history, so the
directive joins the hero rather than replacing it — flagged as a
deviation for the maintainer to reverse in one edit if preferred.

## Visual identity (recorded, not invented)

Already on disk in `vision/site/src/app.css`, kept as canon:

- **Void:** pure black (`#000000`), faint breathing starfield, no
  nebula wash. Warmth comes from the accents, not the background.
- **Accents:** purple `#A78BFA` · blue `#7AA2FF` · green `#6FE7B7` ·
  pink `#F5A0D4` · silver `#C9CEDF` · gold `#E9BB5F` — the Starline
  spectrum that runs down the page gutter.
- **Type:** Playfair Display (display) · Inter (body) · JetBrains Mono
  (dates, code). Generous line-height, 62ch measure.
- **Motion:** restrained and consentful — star twinkle, heading
  shimmer, scroll-reveal — all disabled under
  `prefers-reduced-motion`, and content never hidden without JS.

## Homepage structure (v1, as implemented)

| # | Section | Status |
|---|---------|--------|
| 01 | Hero + Purpose Core directive | existing + added line |
| 02 | Constellation — interactive star map, seven nodes | **new** |
| 03 | Purpose — Curiosity · Evidence · Stewardship | **new** |
| 04 | Ecosystem — Built / Built+Vision / Vision cards | existing |
| 05 | The Vision · Codex links · Archive | existing |
| 06 | Chronicle — dated timeline from repo history | **new** |
| 07 | Transmissions · Support · Contact (Join) | existing |

### Annotations (wireframe v1)

- **Accessibility:** constellation nodes are real links with
  `aria-label`s inside an SVG carrying a `<title>`; focus-visible
  outlines; all motion behind `prefers-reduced-motion`; timeline and
  principles are plain HTML.
- **Analytics hooks:** none. The site has no analytics and this design
  adds none — recorded here so the absence is a decision, not an
  oversight.
- **Security notes:** static site, no forms, no third-party scripts;
  external links limited to the project's own profiles (GitHub, Suno,
  Patreon, X). Nothing in this phase claims security machinery the
  site does not have.

## Honest boundaries

- **MarsBase DownUnder** (named in the mission brief's Explore list)
  appeared nowhere in the six repositories searched on 2026-07-24 — a
  dreamed line, not yet surveyed. It gets no homepage link until something
  exists to link. **Scope note (updated 2026-07-29):** six repositories
  have been created since that search and were not covered by it, so this
  is an absence across the six then searched, not across the twelve that
  now exist.
- **Songlines** are honoured as cultural image in the mythos and are
  not a navigation item or feature name (`mythos/NAMES.md`).
- **Clementine's CTA** leads to the Clementine page and its run-it-yourself
  instructions. There is no hosted chat, so the page must not imply
  one.
- **Chronicle entries** carry only dated, repository-verifiable
  events.

*Non Solus.*
