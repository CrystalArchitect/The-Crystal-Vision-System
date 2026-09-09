# Grok Build — Crystal Interface / Crystal Vision

> **Corrected 11 August 2026.** This handoff had gone stale in ways that would
> misdirect whoever followed it: it named 8 files when the repository tracks 25,
> pointed at the repository's former name, named a Vercel project that is not
> the one deploying, and gave a `cd` path that does not exist. Those are fixed
> below. Whether this Grok Build workflow is still in use has **not** been
> decided here — the document is repaired, not retired.

**Sync phrase:** Sync Crystal Vision from `GROK_BUILD.md` and
`BUILD_MANIFEST.json` — bump version, update CHANGELOG, redeploy.

## What this tree is

Two things, side by side, and the second is not part of the first.

**The operator demo shell** — the original contents of this repository:

| File | Role |
|------|------|
| `index.html` | Panels, wallet modal, nav |
| `app.js` | Mesh, pipeline, receipts, econ, init |
| `styles.css` | Obsidian / cyan / gold theme |
| `vercel.json` | Static config — see the cleanUrls warning below |

**The Celestial Overlay** — `celestial/`, added since. Its own page, its own
tests, no build step and no dependencies. Eleven files; see the README table
and `npm test`. Not a panel in the shell and not reachable from its nav.

Plus the ordinary repository furniture: `README.md`, `CHANGELOG.md`,
`BUILD_MANIFEST.json`, this file, `LICENSE`, `NOTICE`, `SECURITY.md`,
`package.json`, `.gitignore`, `.github/workflows/static.yml`.

**Authority: HOLD.** Not production. Not mainnet.

## Local serve

From the root of a clone of this repository — there is no `apps/` prefix, and
`apps/crystal-interface` does not exist:

```sh
python -m http.server 8090
# shell:   http://127.0.0.1:8090
# overlay: http://127.0.0.1:8090/celestial/overlay.html
```

The shell also opens straight from disk. **The overlay does not** — it imports
ES modules, and browsers refuse module loads from a `file://` origin.

## After a build session

1. Bump `version` in `BUILD_MANIFEST.json`
2. Append `CHANGELOG.md`
3. Run `npm test` if anything under `celestial/` changed
4. Push to `CrystalArchitect/CrystalCore-Starlines-and-Dreamlines`

There is no "ensure all 8 files are present" step any more. Publication is
whole-repository: `.github/workflows/static.yml` uploads `path: '.'` to GitHub
Pages, so a curated file list has nothing to be curated against.

## Publication

- **GitHub Pages**, from `main`, by `.github/workflows/static.yml` —
  https://crystalarchitect.github.io/CrystalCore-Starlines-and-Dreamlines/
- **Vercel** still builds pull-request previews under the project
  **`aeris-protocol`**, whatever the README says about `vercel.json` being
  leftover. The former project name `crystal-vision` is not the one deploying.
  Observed from PR deployment notifications, not from a Vercel API call.

### One trap worth keeping in this file

`vercel.json` sets `cleanUrls` with `trailingSlash: false`. A page named
`index.html` inside a subdirectory therefore loses its directory segment —
`celestial/index.html` would be served at `/celestial`, at which point every
`./module` import resolves against the site root and 404s, giving a blank page
with nothing on it to explain why. GitHub Pages serves the same file correctly,
so the failure appears only where people click and not where you look.

That is why the overlay page is `celestial/overlay.html` and not
`celestial/index.html`.

## Not verified

Recorded as open rather than repaired with a guess:

- The former manifest named a monorepo at `TeraAustralis-Incognita` —
  misspelled; the repository is **TerAustralis-Incognita**. Its recorded path
  `apps/crystal-interface` has no counterpart in the checkout available here.
- A citizen shell was referenced at `../vision-web/`. No such directory exists
  in any checkout here.
