# WHAT-RUNS.md — CrystalCore.OS

**Freeze:** `crystalcore-os-0.3-freeze-2026-09-11`  
**Rule:** If it is not in this file as *runs*, it does not run. Vision stays vision.

Belt tags follow the product’s own law: **science** = executes or is read from an API; **docs-gov** = how the call was made; **vision** = designed, not built.

---

## A. Runs today (science)

These can be opened or started by someone other than the author, given the tree.

### A1. Web shell — CrystalCore.OS v0.3

| | |
|---|---|
| Path | `The-Crystal-Vision-System/archive/CrystalCore-OS/index.html` (~32 KB, single file) |
| How | Open `index.html` in a browser. No build step. |
| What you get | Belted kernel-log boot, glass windows, drag, Mars clock, Starship panel, news window, terminal |
| Terminal that is real | `help`, `clear`, `mars`, `starship`, `status`, `news`, `about`, `reboot`, `belt`, `verify`, `boot`, `panel` |
| Measured at boot | `navigator.hardwareConcurrency`, `window.isSecureContext`, viewport, DPR, timezone, `performance.now()` — type `verify` |
| What it is not | A kernel. No syscalls, no process table, no disk driver. |
| Live demos | Advertised `ccos-os-demo.vercel.app` and GitHub Pages were 404 / unrestored on 2026-09-11. Local file still runs. |

### A2. Product backend — FastAPI generate stack

| | |
|---|---|
| Path | `archive/CrystalCore-OS/backend/` |
| How | `pip install -r requirements.txt` then run `app/main.py` as documented in `backend/README.md` |
| Surfaces | `/api/v1` router, `auth`, `admin`, generate schemas, LLM core, session DB stub, error middleware |
| Tests in tree | `backend/tests/test_admin_api.py`, `test_generate_api.py`, `test_llm.py` |
| Related spec | `docs/architecture/THREE-TIER-GENERATE.md` (WebLLM → local → cloud) |
| Honesty | This is an application backend, not an OS kernel. Admin/auth exist as code. Independent pass/fail not re-run on freeze day. |

### A3. July 2026 “complete” snapshot (Drive)

| | |
|---|---|
| Artifact | Drive file `CrystalCore-OS-complete.zip` (`1NLqxEqy8lnVy_u5aN-6zdcS2YPpjLtyG`), dated 2026-07-01, 195 KB |
| Payload | `src/crystal_mind.py`, `crystal_memory.py`, `crystal_flow.py`, `crystal_evolve.py`, `policy_rules.py` + tests + `run_tests.py` + HTML shells |
| How | Unzip; `python run_tests.py` |
| Note | Older than the monorepo v0.3 tree. Keep as provenance snapshot, not as the SKU head. |

### A4. Companion (Clementine) — product surface, separate tree

| | |
|---|---|
| Historical path | `Clementine-ai-companion` / `vision/apps/clementine/` |
| How (as last published) | Ollama + `clementine.py` or `server.py` + Svelte webapp |
| Status 2026-09-11 | Standalone GitHub repo 404 from this environment; copy expected under monorepo `archive/Clementine-ai-companion/` |
| Label | First companion living on CrystalCore. Product feature, not a second product name. |

### A5. Mythos terminal — executable theatre

| | |
|---|---|
| Historical path | `TerAustralis-Incognita/mythos/crystalcore-os/crystalcore_os.py` |
| How | `python3 mythos/crystalcore-os/crystalcore_os.py` then `boot` / `launch` / `visit` |
| Label | **Science as a program. Vision as a claim.** It prints lattice/network panels. Those panels are story state, not telemetry. |

---

## B. Built, not proven running on freeze day (science, dormant)

Include in the tag. Do not demo as live.

- Starline Weaver bus, RDP record kernel, consent_transport (Noise IK + ML-KEM-768 *claimed*), CrystalBridge fail-closed gate — last mapped in TerAustralis-Incognita-Code. Maintainer-reported 137–158 tests passing 2026-08-10. **Not re-run 2026-09-11.**
- CrystalCore.OS-APP (Flask multi-provider chat) — archived 2026-08-08. Dead release.
- Seldon / psychohistory-lite ledger JSON in the product tree — small data file, not a runtime.
- `synthetic-affect/` inside CrystalCore.OS — **retired pointer**. Canonical home is the SAT repo after the 2026-08-14 split.

---

## C. Does not run (vision / docs-gov)

Do not put these on a product slide as features.

- CrystalCore.Lattice as a running substrate
- `/core/prism` as a mount point
- “47+ star systems”, galactic mesh, photon routing, 100% lattice lock as measurement
- Any AI chat reply to `Boot CrystalCore.OS` — authority weight zero (AI Boot Panel, 2026-08-08)
- Constitution names used as if they were processes

---

## D. Product bill of materials for the freeze tag

Minimum tree to hash:

```
CrystalCore.OS/
  README.md                 # already honest about v0.3 and belts
  LICENSE                   # replace per 03-LICENSE-SPLIT after stamp
  LICENSE-CODE
  LICENSE-MYTHOS
  NOTICE
  WHAT-RUNS.md              # this file
  index.html                # web shell
  vercel.json
  backend/                  # FastAPI + tests
  docs/architecture/
  seldon/                   # keep, labelled docs
  synthetic-affect/         # keep as pointer only
```

Companion, protocol modules, and umbrella ADRs are **linked artifacts**, listed in an `ATTRIBUTIONS-AND-TREES.md` inside the tag, not silently merged.

---

## E. One-sentence product definition (use this)

CrystalCore.OS v0.3 is a **belted web shell plus a local generate/companion backend**, with protocol sketches and a mythos terminal as adjacent artifacts. It is the product of TerAustralis Incognita. It is not a kernel.
