# Changelog — crystal-interface

## Unreleased — celestial/ (branch `claude/first-real-world-process-eknlk9`)

Added the **Celestial Overlay**: a separate layer beside the demo shell, with
the Incognita Rule enforced in the structure rather than remembered.

- `atlas.js` — the shape. Seven modes **computed** as rotations of the major
  scale, so the wheel's order follows from the intervals. Throws on an entry
  with no belt, a star with no source, a reading filed as surveyed, a work that
  both enters and refuses a territory, a duplicate work, an undated rehearing
- `stars.js` — 28 stars from the Yale Bright Star Catalogue 5th ed., equinox
  J2000 epoch 2000.0. A **committed extract**: the page makes no network call,
  and `extract-stars.js` rebuilds it as a deliberate act with a reviewable diff.
  The layer stood empty until a catalogue was reachable
- `readings.js` — six works read onto the wheel, all dreamed. `collisions()`,
  `resolution()` and `frontier()` report what the vocabulary *cannot* do
- `wheel.js`, `overlay.html` — the drawing and the page. Every wheel carries
  *dreamed line — not an astronomical chart* on its face
- `cycle.js` — a 29-day cycle chart after Connie Kaplan's Dream Chart, with the
  credit drawn above the wedges. Edition unconfirmed and recorded as such
- `PRECEDENTS.md` — Apian 1524, and the word *atlas* 1595
- `VISION-Four-Pillars.md` — an organising frame, filed as Vision
- `package.json` — declares ES modules so `node --test` can read the files. No
  dependencies and no build step; the site still opens by pointing a browser at
  `index.html`

54 tests. Notable fixes along the way: a NUL byte that made `atlas.js` invisible
to ripgrep, a page name that would have 404'd its own imports under `cleanUrls`,
a duplicate reading reported as a finding, and a citation that named an edition
nobody had verified.

## 0.5.1 — 2026-07-17

- Linked GitHub (`CrystalArchitect/crystal-vision`) and Vercel preview in `BUILD_MANIFEST.json`
- Added `GROK_BUILD.md` sync phrase and redeploy notes
- Added `vercel.json` for static preview
- Packaged 8-file deploy tree

## 0.5.0 — 2026-07-17

- Receipts table, wallet modal, mesh select, epoch, full init wiring
- Operator shell panels: home, twin, mesh, pipeline, econ, starline, journey, log
