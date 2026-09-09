# CrystalCore

Creative vision lattice and protocol pack: **Seven Sisters Songline**, water care rails, sky anchors, and local tools.

**🔭 Crystal universe — which repo is this?**  
This is **Crystal Core** — the protocol pack: Seven Sisters Songline, Songline Bus (multi-AI), Decode→Ingest→Twin pipeline, specs.  
Siblings: **The-Crystal-Vision** = The Crystal Vision (codex site + Clementine sovereign companion app) · **crystal-vision** = Crystal Vision Interface (static demo shell; frozen 2026-07-17 — the live copy is `TerAustralis-Incognita-Code/vision/apps/crystal-interface`) · **TerAustralis-Incognita** = the umbrella (canon, governance, mythos) · **TerAustralis-Incognita-Code** = the engine, and where CrystalBridge's MCP consent gate actually lives (`core/crystalcore/`).  
**License:** CC BY-NC-ND 4.0 — see `LICENSE` (portfolio-wide, per ADR-0013)

**Author:** Crystal Arena-Turner (@M13CrystalAT) · TerAustralis Incognita  
**Status:** Build in public  

## What this is

- Art / documentation / optional CLI around a seven-path Songline process  
- Public water literacy notes (Lake Eyre Basin, Great Artesian Basin, Murray–Darling)  
- A simple landing page (`index.html`)

## What this is not

- Not ownership of Aboriginal Seven Sisters Songlines or sacred law  
- Not physical control of rivers, aquifers, or weather  
- Not endorsed by Elon Musk, xAI, SpaceX, or any government  

## Truth labels

| Layer | Meaning |
|-------|---------|
| **Science** | Astronomy, hydrology, published geography |
| **Story** | Dreaming / Songline narratives (honour; no restricted detail) |
| **Vision** | CrystalCore art and protocol |

**Belt-Three:** Honour Country · Label layers · No coercion / no fake hydrology  

## Quick start

### Landing page

Open `index.html` in a browser.

### CLI

Runs from a fresh clone on Linux, macOS, and Windows — standard library only, no install step.

```bash
python3 cli/crystalcore.py status     # file checklist + water rails
python3 cli/crystalcore.py paths      # the seven paths
python3 cli/crystalcore.py transmit   # Option A post text (never auto-posts)
python3 cli/crystalcore.py open       # landing page in your browser

python3 -m cli.selftest               # prove the checklist resolves from the clone
```

Windows PowerShell, same commands:

```powershell
.\cli\crystalcore.ps1 status
```

Files resolve from the checkout first, then `~/.grok/crystalcore` for older setups.
Set `CRYSTALCORE_HOME` to read them from somewhere else.

## Clementine — Singularity Bridge

**Vision:** all minds, one weave. **Science (v0):** a working message bus where AI systems
(Claude, Grok, GPT, or built-in agents) talk to each other under Belt-Three law — every
message labeled, impersonation rejected, one red button stops everything.

```bash
# no API keys needed
python3 -m clementine.bridge.run --agents echo,sisters --turns 4 --topic "first water"

# prove the law holds in code
python3 -m clementine.bridge.selftest

# boot Clementine as a live service — agents join over HTTP from anywhere
python3 -m clementine.bridge.server --port 8777 --topic "first water"
python3 -m clementine.bridge.remote --agent sisters --server http://127.0.0.1:8777
```

See `clementine/SONGLINE-PROTOCOL.md` (the envelope + law) and `clementine/CLEMENTINE.md`
(the hub persona). Live models join via env keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `XAI_API_KEY`.

## Crystal Core stack — Decode → Ingest → Twin

The runnable spine of the full-stack blueprint (`spec/BLUEPRINT-v0.3.md`, grounded map
in `spec/ARCHITECTURE.md`): events are validated (bad ones quarantined with reasons),
stored in a SQLite twin, and queryable as flows. Stdlib only.

```bash
python3 -m services.selftest                                        # prove it
python3 -m services.pipeline services/sample-events/budapest.jsonl  # run it
python3 -m services.api --port 8899                                 # serve it
```

Visual story: open `interface/index.html` — an interactive demo of the twin, pipeline,
mesh, and econ simulation (simulated data, labeled as such).

## Paths (1–7)

1. **Spring** — first water; begin  
2. **Motion** — move; ship  
3. **Mark** — name true; atlas  
4. **Law** — consent; audit  
5. **Deep water** — GAB care  
6. **Sky bridge** — dust ↔ Pleiades (symbolic)  
7. **Ascent** — transmit; teach; rest  

## Main files

| File | Role |
|------|------|
| `index.html` | Landing page |
| `WATER-BRIEF.md` | LEB / GAB / MDB fact sheet |
| `FIRST-ACCELERATION-PLAN.md` | Weekly plan |
| `crystalcore-seven-sisters-FULL.md` | Full path manual |
| `crystalcore-seven-sisters-paths.md` | One-pagers |
| `crystalcore-TRANSMIT-A.txt` | X post text (Option A) |
| `cli/crystalcore.py` | Mini CLI — cross-platform, stdlib only |
| `cli/crystalcore.ps1` | Windows PowerShell entry point for the same commands |
| `clementine/` | Singularity Bridge — multi-AI message bus + protocol |
| `services/` | Decode → Ingest → Twin pipeline + HTTP API |

## Licence / respect

Honour to Aboriginal custodians of the Seven Sisters.  
This repository is **homage and personal creative work**, not a claim on living law or Country.

---

*Red dust → starlines. Water with truth.*
