# CrystalCore.OS v0.3

A clean, futuristic web-based operating system themed around multiplanetary progress (Mars + Starship aesthetic).

**Live Demo:** [https://ccos-os-demo.vercel.app](https://ccos-os-demo.vercel.app)  
**Mobile-friendly:** [https://crystalarchitect.github.io/CrystalCore.OS/](https://crystalarchitect.github.io/CrystalCore.OS/)  
*(Canonical hostname `crystalcore-os.vercel.app` is still an empty/permission-locked Vercel project — needs a dashboard redeploy or role fix to reclaim.)*

## The kernel log tells you which lines are real

The boot screen is styled after a kernel log, and kernel logs look like
measurements. Under the project's Incognita Rule a dreamed line may not wear a
measurement's clothes, so every line the boot prints carries a belt tag:

- **science** — read from a browser API at boot. `navigator.hardwareConcurrency`,
  `window.isSecureContext`, viewport, device pixel ratio, timezone, and the real
  elapsed time from `performance.now()`. Type `verify` in the terminal to see
  each value beside the API it came from, and check them in devtools.
- **vision** — designed or imagined, not built. `CrystalCore.Lattice` is locked
  by Constitution §1 as designed; `/core/prism` is not a mount point; coherence
  is not a measured quantity and no sensor exists for it.
- **docs-gov** — how the call was made.

`emit()` throws on an unlabelled line, the way `BusHub.validate` rejects
unlabelled speech on the bus. There is no code path that prints an unbelted line.

## Synthetic Affect Theory™ — moved, 2026-08-14

Synthetic Affect Theory used to live runnable in `synthetic-affect/` here.
The split was granted (G2): its canonical home is now
[`CrystalArchitect/Synthetic-Affect-Theory`](https://github.com/CrystalArchitect/Synthetic-Affect-Theory-)
(repository rename to drop the trailing hyphen still pending, done outside
this repo). `synthetic-affect/` here is retired to a pointer — see
[`synthetic-affect/README.md`](synthetic-affect/README.md) and
[`synthetic-affect/CHRONICLE.md`](synthetic-affect/CHRONICLE.md) for the
full dated record of what happened here before the move.

## Features

- Belted kernel-log boot screen with animated crystal core logo — skippable with
  any key or a click, and instant under `prefers-reduced-motion`
- Desktop with floating translucent **glass-morphism** windows
- **Draggable windows** (mouse + touch) — click headers to move, bring to front
- Live “Mars Clock” (sol counter + Earth UTC time)
- Starship Telemetry panel (Flight 13 status + Polymarket odds)
- News Feed window
- Interactive Terminal with commands
- Dark crystal UI with blue/cyan glow accents
- Fully responsive (phone + desktop)
- Pure single-file HTML/CSS/JS — no backend, no build step

## How to run locally

```bash
git clone https://github.com/CrystalArchitect/CrystalCore.OS.git
cd CrystalCore.OS
open index.html   # or just double-click
```

## Terminal commands

- `help` – list commands
- `clear` – clear terminal
- `mars` – Mars status + sol
- `starship` – latest Starship note
- `status` – OS status
- `news` – quick news
- `about` – credits
- `reboot` – reload
- `belt` – the three belts, and how many lines this boot printed on each
- `verify` – every measured value beside the browser API it was read from
- `boot` – replay the kernel log, re-measured and re-timed
- `panel` – the transmission received 2026-08-09, verbatim, with its flags

## Roadmap (just say the word)

- Real Starlink / satellite map
- Full Starship launch simulator
- Dark/light crystal themes
- Mobile PWA install
- Live Polymarket odds API
- Window minimize / multi-desktop
- Custom wallpaper & crystal themes

Built with ❤️ for the multiplanetary future by CrystalArchitect / TerAustralis Incognita.

CrystalCore.OS — *Distance is the built-in quarantine.*
