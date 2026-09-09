# Crystal Interface — the operator shell

The operator-facing **demo shell** for Crystal Vision / Core / Starline Budapest.
A single static copy — open it locally or serve it as static files (no build
step). The citizen-facing surface is the separate, slimmer
[`../vision-web`](../vision-web).

**🔭 Crystal universe — which repo is this?**  
Corrected 2026-07-24 — six repos exist today, not the three implied
below originally: **TerAustralis-Incognita** (umbrella — governance,
ADRs, canon, mythos, no app code) · **TerAustralis-Incognita-Code**
(this repo, this file's actual home — the engine at `core/` and the
vision app at `vision/`; CrystalBridge lives here, at
`core/crystalcore/`, not in the umbrella as previously stated) ·
**CrystalCore.OS-the-Crystal-Architecture-Archive** (the fleet-wide
status ledger) · three frozen-provenance repos, none touched since
2026-07-17: **The-Crystal-Vision** (codex site + the companion's
ancestor), **crystal-vision** (this shell's interface-demo ancestor),
and **crystalcore** (frozen protocol sketches, sealed 2026-07-17 — not a living component). Full map: the
umbrella's `docs/governance/Project-Boundaries.md`, "Repositories,
today."  
**License:** CC BY-NC-ND 4.0 — see `LICENSE` (portfolio-wide, per ADR-0013)

**Not production.** Every number is illustrative and **simulated in the browser**;
this shell makes **no backend calls**. Authority **HOLD**.

## Open

```bash
cd vision/apps/crystal-interface
# any static server, or:
python -m http.server 8090
# → http://127.0.0.1:8090
```

Or open `index.html` directly in a browser.

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

## The real pipeline (separate — not wired to this shell)

This shell is static and simulated; it does not call a backend. The actual data
pipeline is a real, tested package in the monorepo and runs independently:

```bash
cd ../../../core/crystal-core
python -m services.selftest      # the real ingest → decode → twin pipeline, with tests
```
