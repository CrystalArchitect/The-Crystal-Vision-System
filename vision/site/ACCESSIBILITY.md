# Accessibility checks — www.teraustralis.com.au

Target: WCAG 2.2 AA on the published SvelteKit site.
Last updated: 2026-08-25.

This file is a maintainer test. It is not a public page. It was renamed
from `A11Y.md` so the filename is not a personal handle. `a11y.css` and
Svelte `a11y_*` ignores stay — those are toolchain names, not this document.

The VoiceOver expected list below matches the **Observatory homepage**
(`src/routes/+page.svelte` as published). It replaces the pre-Observatory
script (h1 “Recovery, refurbishment and fuel.”, quiet “Proposal documents”
nav, unnamed hero/split/more). That page is gone.

This list is inferred from live HTML on 2026-08-25. It has **not** been
confirmed on iPhone VoiceOver. Walk it and correct the rotor names if
Safari says them differently. Do not treat this file as a pass.

## iOS VoiceOver — Landmarks rotor

Device: iPhone. Browser: Safari. Page: https://www.teraustralis.com.au/

### Turn VoiceOver on

1. Settings → Accessibility → VoiceOver → On.
2. Optional: Settings → Accessibility → Accessibility Shortcut → VoiceOver, then triple-click the side button to toggle.
3. First use: VoiceOver → Rotor. Enable **Landmarks** and **Headings**.

Safari cache will serve the old homepage. Hard-refresh (pull down, or close the tab and open a private tab) before testing.

### Walk Landmarks

1. Open the page with VoiceOver on.
2. Two-finger rotate on the screen until the Rotor says **Landmarks**.
3. Flick up or down to move through the list. Double-tap a name to jump there.

### Expected list (homepage, source order)

Safari usually says **Footer**, not “contentinfo”. That is the same region.
Safari may say **TerAustralis Incognita** for the banner wordmark or the h1
region — check which stop you landed on.

The four homepage `<section>`s have `aria-labelledby`, so they are **named
regions** inside Main. They should appear. Unnamed sections must not.

| Rotor should say (or close) | HTML |
|---|---|
| Banner | `<header class="site observatory-header">` |
| Navigation, Primary navigation | header `<nav id="primary-nav" aria-label="Primary navigation">` |
| Main | `<main id="main">` |
| TerAustralis Incognita (region) | `<section class="observatory-hero" aria-labelledby="page-title">` |
| Choose a field of view. (region) | `<section class="map-section" aria-labelledby="map-heading">` |
| The map does not make the claim. (region) | `<section class="boundary-band" aria-labelledby="boundary-heading">` |
| From the observatory. (region) | `<section class="observatory-index" aria-labelledby="index-heading">` |
| Footer | `<footer class="site">` after `</main>` |

There is no second `<nav>` inside main. The three doors (Built / Proposal /
Codex) are SVG links on `ObservatoryMap`, not a landmark.

### Pass

- One Banner, one Primary navigation, one Main, one Footer.
- Four named regions whose names match the four headings below (Safari wording may truncate).
- One Footer, not nested inside Main.
- Jumping to Main lands on the heading “TerAustralis Incognita”.
- Jumping to Footer lands on the Traditional Custodians paragraph, not on the index cards.

### Fail

- Two Footers.
- Footer listed as part of Main.
- An unnamed landmark (a region called hero, map-section, or similar class name).
- A leftover “Proposal documents” navigation (that nav is gone).
- Primary navigation unlabelled.
- Main landing on “Recovery, refurbishment and fuel.” (that heading is gone).

### Headings rotor (separate check)

Rotate to **Headings**. Expected on the homepage:

1. TerAustralis Incognita (heading level 1)
2. Choose a field of view. (heading level 2)
3. The map does not make the claim. (heading level 2)
4. From the observatory. (heading level 2)

Index card titles (Working software, Southern systems proposal, Celestial
Atlas) must not appear as headings. They are `<strong>` inside links.

### Skip link (keyboard / Bluetooth)

With an external keyboard, Tab once. Focus must show **Skip to main content**. Activate it. Focus moves to `main`.

## Lighthouse CI

Accessibility-only Lighthouse CI runs on pull requests and `main` against the **local** SvelteKit build (`vision/site/build`), not against production. Named routes: `/`, `/atlas`, `/atlas-ten`, `/crystalcore-os`, `/codex`, `/apocryphon`, `/footer-audit`.

It asserts three audits as errors (`label-content-name-mismatch`, `heading-order`, `link-in-text-block`) and warns if the accessibility category is below 0.9. It does not publish a site-wide score, does not replace this VoiceOver test, and does not rewrite `/footer-audit`.

Config: `lighthouserc.json`. Workflow: `.github/workflows/lighthouse.yml`.

## Related

- `src/lib/styles/a11y.css` — skip link, 44px targets, unclipped focus.
- `src/routes/+layout.svelte` — skip, `main`, site `Footer` after `main`.
- `src/routes/+page.svelte` — Observatory homepage sections and headings.
- `src/lib/components/Header.svelte` — `aria-label="Primary navigation"`.
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- APG landmarks: https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
- Lighthouse CI: https://github.com/GoogleChrome/lighthouse-ci
