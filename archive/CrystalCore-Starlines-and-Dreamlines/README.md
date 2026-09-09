# Crystal Core · Interactive Interface

Local **demo shell** for Crystal Vision / Core / Starline Budapest.

**⚠️ If you came here to review CrystalBus / CrystalBridge / ConsentGate / StarlineWeaver:
they are not in this repository.** This repo is front end only — a static demo shell
(`index.html` / `app.js` / `styles.css`) plus the unrelated `celestial/` overlay page. There is
no Python here and no bus, bridge, gate, or router implementation to review. That code lives in
[`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)
under `core/crystal-core/services/` — see "Related backend" below for how to run it. Treating this
repo as if it contained that implementation was the top finding of the 2026-08-26 architecture
review (`ARCHITECTURE-REVIEW-2026-08-26.md`); this note exists so the next reviewer doesn't repeat it.

**🔭 Crystal universe — which repo is this?**  
This is **CrystalCore-Starlines-and-Dreamlines** — the static demo shell, published to GitHub Pages.  
**Formerly `crystal-vision`**, renamed 2026-07-29. GitHub redirects the old name, so existing clones and links keep working — which also means the two names refer to *one* repository, not two.  
Siblings: **crystalcore** = Crystal Core (protocol pack) · **the-crystal-vision** = The Crystal Vision (codex site + Clementine sovereign companion app) · **teraustralis-incognita** = TerAustralis Incognita (narrative + CrystalBridge).  
**License:** CC BY-NC-ND 4.0 — see `LICENSE` (portfolio-wide, per ADR-0013)

`vercel.json` is left over from the Vercel deployment this repository had
under its previous name. Publication is now via GitHub Pages
(`.github/workflows/static.yml`).

**Not production.** Economics are illustrative. Authority **HOLD**.

## Open

Published to GitHub Pages from `main` by `.github/workflows/static.yml`.

To run it locally, from a clone of this repository:

```sh
python -m http.server 8090
# → http://127.0.0.1:8090
```

Or open `index.html` directly in a browser — it has no build step and no
dependencies.

**`celestial/overlay.html` is the exception: it needs the server.** The shell
uses a plain script tag; the Celestial Overlay imports ES modules, and browsers
refuse module loads from a `file://` origin. Start the server above and open
`http://127.0.0.1:8090/celestial/overlay.html`.

## Panels

| Panel | Content |
|-------|---------|
| Home | Product map + stats |
| Twin | Layered canvas (water / energy / data / mobility) |
| Mesh | Sovereign nodes SVG |
| Pipeline | DECODE→…→UPGRADE interactive steps |
| Economics | Burn rate R, α, wallet demo |
| Starline | Corridor cards VIE/BTS/BER |
| Wallet | Citizen journey |
| Event log | Client-side activity |

## Celestial Overlay

A second, separate thing in this repository: `celestial/`. Not part of the demo
shell above, and not a panel in it — its own page, its own tests, no build step
and no dependencies, the same as everything else here.

| File | Holds |
|------|-------|
| `atlas.js` | the shape. Seven diatonic modes, **computed** as rotations of the major scale; the refusals that keep dreamed and surveyed lines apart |
| `stars.js` · `stars.data.js` | 28 stars from the Yale Bright Star Catalogue 5th ed., **equinox J2000, epoch 2000.0** — a committed extract, so the page makes no network call |
| `extract-stars.js` | rebuilds that extract. A tool run deliberately, never by the page |
| `readings.js` | nine works read onto the wheel, each dreamed and saying so |
| `wheel.js` · `overlay.html` | the drawing, and the page |
| `cycle.js` | a 29-day cycle chart, after Connie Kaplan's Dream Chart |
| `PRECEDENTS.md` | checked historical warrants — Apian 1524, the word *atlas* 1595 |
| `VISION-Four-Pillars.md` | an organising frame, filed as Vision |

```sh
npm test          # 56 tests, node's own runner, no dependencies
```

The one rule the whole directory exists to hold: **always mark which lines are
dreamed and which are surveyed, and never let a dreamed line pretend it was
measured.** It is enforced rather than remembered — an entry without a belt
throws, a star without a catalogue and epoch throws, and the drawn wheel carries
*dreamed line — not an astronomical chart* on its own face.

## Related backend

**Not in this repository.** The demo shell is front end only — `index.html`,
`app.js`, `styles.css` — and `celestial/` is browser JavaScript beside it.
There is no Python here, so nothing below runs from a clone of this repo.

The decode → ingest → twin pipeline lives in
[`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)
under `core/crystal-core/services/`. From a clone of *that* repository:

```bash
cd core/crystal-core
python3 -m services.pipeline services/sample-events/budapest.jsonl
python3 -m services.selftest
```
