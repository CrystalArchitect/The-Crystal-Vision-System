# Project boundaries — the umbrella, Crystal Core, Crystal Vision

**Status:** standing governance charter, adopted by
[`ADR-0011`](../adr/ADR-0011.md). The "what exists today" statements on
this page are **Science** (git-verifiable); the component→project
assignments are **adopted policy**, amendable only by a new ADR. Nothing on
this page moves a file — execution lives in
[`Migration-Plan.md`](Migration-Plan.md), stage by stage, with the
maintainer's approval as the gate.

## The three projects

| Project | Owns | Does not own |
|---|---|---|
| **TerAustralis Incognita (umbrella)** | Canon and law: governance, architecture documentation, ADRs, the mythos, research, the archive, and references to the engineering repositories | Main app code |
| **Crystal Core** | The engine: runtime, protocols, APIs, and shared libraries — what other software imports and calls | User interfaces |
| **Crystal Vision** | The user-facing application built on Crystal Core — what a human opens, reads, and steers | Engine internals |

Rule of thumb at the boundary: **if it renders or speaks for a human, it
is Crystal Vision; if it is imported or called by other software, it is
Crystal Core.** The edges where that rule needs judgment are flagged in
the map below, not papered over.

## Locked names, respected

The Constitution ([§1](Constitution.md)) locks three names, quoted exactly:

> | **TerAustralis Incognita** | Outer civilizational vision — the Unknown Southern Land awakening |
> | **CrystalVision** | Sensing / dreaming / directing interface (Crystal ↔ Lattice) |
> | **CrystalCore.Lattice** | Substrate — multi-AI weave, memory, ontology, activation |

This charter redefines none of them:

- **CrystalVision** (locked) is the interface *concept* — the lens through
  which a human watches and steers the Lattice. **Crystal Vision** (the
  project) is the engineering home where that concept and its kin (the
  companion, the shells, the public site) get built. A container, not a
  redefinition; when the real CrystalVision surface exists, it will live
  inside the Crystal Vision project.
- **Crystal Core** (the project) *contains* the
  [ADR-0004](../adr/ADR-0004.md) taxonomy branches — CrystalCore
  Framework, CrystalCore Protocol, CrystalBridge. The taxonomy itself is
  untouched: the CrystalCore OS *platform* remains the umbrella's
  repository-and-governance architecture, the CrystalCore.OS *mythos
  terminal* remains Vision-layer story software, and their near-collision
  stays ADR-0004's honestly-unresolved case.
- **CrystalCore.Lattice** (locked) is designed-not-built
  ([`Lattice.md`](../architecture/Lattice.md)); it remains umbrella canon
  until an engineering decision deliberately brings it into Crystal Core.

## Component → project map

Paths are the *described* homes (the code tree lives in the maintainer's
local working copy — see
[SystemMap](../architecture/SystemMap.md#where-the-code-actually-lives)).

| Component | Described home today | Project | Note |
|---|---|---|---|
| **Clementine** — the sovereign companion, including its embedded **CrystalCore Framework** package | `vision/apps/clementine/` (framework at `core/crystalcore/mind/`) | **Crystal Vision** | Flagship user-facing product, whole — per maintainer directive. The Framework keeps its ADR-0004 name while traveling with Clementine; split criteria are operationalized in [Migration-Plan §Stage 3](Migration-Plan.md). |
| **CrystalCore Protocol pack** — Starline Weaver, Decode→Ingest→Twin pipeline, Consent Transport / Starline, RDP | `src/crystal-core/` | **Crystal Core** | The protocol machinery other components call. |
| **CrystalBus** — the channel coordinating comms between AI systems | `bus/` inside the protocol pack (card: [`CRYSTALBUS.md`](../architecture/crystal-core/CRYSTALBUS.md)) | **Crystal Core** — *logical component* | A named component, not a repository — per maintainer directive. Carried the name Clementine before that name moved to the companion. |
| **CrystalBridge** — the fail-closed MCP consent gate, plus its profile configs | `src/crystalcore/`, `src/profiles/` | **Crystal Core** | Integration/API layer. |
| **Mesh stub** | `src/node/mesh/` | **Crystal Core** | Shared transport library (stub only today). |
| **TypeScript SDK** | `src/sdk/typescript/` | **Crystal Core** | Client API scaffold. |
| **Demo shells** — `crystal-interface` (operator), `vision-web` (citizen) | `src/apps/crystal-interface/`, `src/apps/vision-web/` | **Crystal Vision** | Applications on simulated data; their **Authority HOLD** labels travel with them. *Divergence note:* [`Full-Stack-v0.5.md`](../architecture/Full-Stack-v0.5.md) branded `crystal-interface` under Crystal Core (operator-facing); this charter supersedes that mapping — brand-facing is not code ownership, and the operator/citizen distinction survives in the shells' own descriptions. |
| **Voicebox** — local MCP text-to-speech server | `src/apps/voicebox/` | **Crystal Vision** | Judgment call at the boundary rule's edge (called via MCP, but its output is speech for a human). Low stakes; revisitable by ADR. |
| **CrystalCore.OS mythos terminal** | `src/crystalcore-os/` | **Umbrella (mythos area)** | Canon-as-code: a playable story, not infrastructure ([taxonomy](../vision/CrystalCore.md)). Placement revisitable at Migration-Plan Stage 1. |
| **Site** — teraustralis.com.au | `src/site/` | **Open decision point** | Recommendation in [Migration-Plan §Stage 4](Migration-Plan.md): Crystal Vision (it is the public face), with the Pages/CNAME mechanics solved in Stage 2. |
| **dbt emotion warehouse** | `dbt/crystalcore_emotion_warehouse/` (in this repository) | **Open decision point** | Recommendation in Migration-Plan §Stage 4: Crystal Core's data layer, eventually. |
| **Documentation, governance, ADRs** | `docs/` | **Umbrella** | Including this charter. |
| **Mythos content and art** | `mythos/` | **Umbrella** | Its own license area (`LICENSE-CONTENT.md`); may point at code, never speaks for it. |
| **Research** — the Seven Sisters cycle | `research/` | **Umbrella** | Not production; promotion into an engineering repo is a deliberate, reviewed act. |
| **Archive** | `archive/` | **Umbrella** | Provenance only. |
| **Assets, examples index** | `assets/`, `examples/` | **Umbrella** | Runnable demos live with their code; the index stays here. |
| **`corpus/`** | Named in Constitution §7; never built | **Umbrella** (when built) | Recorded in the Migration-Plan debts register; fixing the §7 row itself requires a §8 amendment. |

Vision-layer *concepts* that are not yet artifacts — the CrystalVision
interface, CrystalCore.Lattice, the mainnet mesh — are umbrella canon until
a reviewed engineering decision builds them, at which point they land in
the project this charter assigns.

## The dependency rule

1. **Crystal Vision may depend on Crystal Core.** That is the direction
   "built on top" points.
2. **Crystal Core never imports Crystal Vision.** No engine code reaches
   into an interface.
3. **Clementine, living inside Crystal Core, must not depend on Crystal
   Vision** — an orchestration layer that imported an app would invert
   the whole model.
4. **The umbrella contains no importable app code.** Both engineering
   projects obey umbrella canon: the Covenant as product spec, the
   Incognita Rule's honesty labels, the Belt-Three law.

## Repositories, today

*(Rewritten 2026-07-24 from a same-day survey of all six repositories —
the original section predated Stage 1 and still called `-Code` "empty by
design." Science layer: every row below was verified against the actual
trees and git histories.)*

**The living system:**

| Repository | Role |
|---|---|
| `CrystalArchitect/TerAustralis-Incognita` (this repo) | The umbrella: governance, ADRs, architecture docs, research, provenance mirrors under `archive/`, and `mythos/` — **the** canon home (Codex, Apocryphon, The First Remembering, the crystalcore-os terminal). |
| `CrystalArchitect/TerAustralis-Incognita-Code` (public) | The software, per Migration-Plan Stages 1–2: `core/` (engine — protocol pack with Clementine, CrystalBridge, mesh stub, SDK) and `vision/` (application — Clementine, voicebox, demo shells, **the site source**). Full CI; carries the Pages deploy and `CNAME`. |
| `CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive` | The system ledger: one fleet-wide `STATUS.md` — state, receipts, known unknowns across all repositories. Deliberately small. |

**Frozen provenance** — checkpointed 2026-07-17 (the laptop hand-off),
deliberately left unarchived, never edited; their code lives on as
ancestors of the `-Code` tree:

| Repository | Was | Lives on as |
|---|---|---|
| `The-Crystal-Vision` (tag `vision-safe-2026-07-17`) | Codex site + Clementine companion; holds the complete **crystalcore v0.13.4 bytecode rescue** and the laptop snapshot | Ancestor of Clementine's embedded framework (which forked the earlier 0.7.0 line — see open decisions) |
| `crystalcore` (tag `crystalcore-safe-2026-07-17`) | The Songline protocol pack | Direct ancestor of `core/crystal-core` (SonglineBus → Starline Weaver) |
| `crystal-vision` | Static demo shell (Grok build) | Direct ancestor of `vision/apps/crystal-interface` |

**How canon reaches the public site** — the one cross-repo pipeline:

```
mythos/ (umbrella, canonical)
   → copied by hand into vision/site/src/content/ (-Code)
   → built by deploy.yml → GitHub Pages → www.teraustralis.com.au
```

The site renders *copies*, not the canon directly — a known,
deliberate drift risk: new canon is not public until its copy step
happens.

**Open decisions this map records rather than resolves:**

- **Stage 3 repo count** — whether `core/`/`vision/` split into two
  repositories (Migration-Plan criteria; deliberately not decided here).
- **0.13.4 lineage** — Clementine's framework forked the 0.7.0 line; the
  0.13.4 rescue's extras (SpaceXAI provider, `node.py`, `status.py`,
  CLI) sit unreconciled in `The-Crystal-Vision`.
- **Frozen repos' end state** — GitHub-archive (read-only flag) the
  three provenance repos, or leave them as-is.
- **Site copy of new canon** — The First Remembering is canonical but
  not yet copied into the site content set.

## Repositories, 2026-08-20

The six-repo survey above is the 2026-07-24 measurement and is left as
written. GitHub search `user:CrystalArchitect` on 2026-08-20 returned
**19** repositories (6 public living, 7 private living, 6 archived).
The landing table and the "no new repository" gate are
[`ADR-0015`](../adr/ADR-0015.md).
External peer (not in the 19): [`SourceCode`](../architecture/peers/SourceCode.md)
([`ADR-0016`](../adr/ADR-0016.md)) — recognition, not a twentieth repo. This charter's Stage 3 open decision
(whether to split `-Code`) is unchanged; creating the split still takes
that ADR *and* ADR-0015.

## Amendment

Changes to this charter take a new ADR
([`Decision-Records.md`](Decision-Records.md)). Locked names move only via
Constitution §8. Renames that would resolve the ADR-0004 collision need
their own ADR, as ADR-0004 already requires.
