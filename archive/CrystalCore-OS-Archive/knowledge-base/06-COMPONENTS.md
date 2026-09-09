# Components

Every subsystem, individually, with its evidence. This is also where
component-level technical debt is documented — as evidence-backed fact
about each component, not as a separate report.

## Lumina

### Statement
Lumina is the local-first AI companion: a terminal, a Flask JSON API
(127.0.0.1 only), a Svelte webapp, and an embedded "CrystalCore
Framework" (`companion.py` — the brain; `memory.py`; `profiles.py`;
`sovereignty_scorer.py`). Framework version `0.7.0`. Forked from
`The-Crystal-Vision`'s companion lineage at the 0.7.0 line specifically
— not the later 0.13.4 rescue.

**Status: Implemented.**

### Evidence
- `TerAustralis-Incognita-Code/vision/apps/lumina/README.md`:
  "Everything in this folder runs on your own machine. Nothing leaves
  it."
- `vision/apps/lumina/crystalcore/__init__.py`: `__version__ = "0.7.0"`.
- 16/16 `tests/test_core.py` pass, re-verified 2026-07-24 per
  `STATUS.md`.

### Historical Notes
`vision/README.md` claims four Lumina test suites (test_core,
test_integration, test_performance, test_end_to_end); only
`tests/test_core.py` exists anywhere in the repository — confirmed
overclaim this pass (`vision/README.md` itself left uncorrected; see
`11-CORRECTIONS.md`). `sovereignty_scorer.py` is an explicitly unwired
0.1-alpha sketch, not in use. The "nothing leaves the machine" framing
holds only under the default Ollama configuration — `companion.py`
reads `XAI_API_KEY` and has a live, reachable path to a remote endpoint
when that key is set.

### Cross References
`02-REPOSITORY-MAP.md` (0.13.4 lineage question), `09-GLOSSARY.md`.

---

## Starline Weaver (Clementine)

### Statement
The multi-AI message bus. `ClementineHub` (`clementine/bridge/`) routes
and validates messages between agents (built-in `echo`/`sisters`, or
live `claude`/`gpt`/`grok` via env-key adapters). Every message requires
a `layer` field (science/story/vision) or is rejected outright — Belt-
Three enforced in code, not convention. A "red button" halts every
agent at once. "Matrix mode" fans one question to every agent
independently and counts agreement — explicitly "a count, not a
verdict."

**Status: Implemented.** 7/7 self-tests pass.

### Evidence
- `docs/architecture/crystal-core/STARLINE-WEAVE-PROTOCOL.md`,
  `docs/architecture/AI-Weave.md`.
- `core/crystal-core/clementine/bridge/{server,bus,adapters,agents,
  remote,run,selftest}.py` — confirmed present, matching the spec's
  module list exactly.

### Historical Notes
Born as "Clementine Singularity Bridge" / "Songline Bus" in the
standalone `crystalcore` repo (2026-07-17); renamed to Starline Weaver
in the umbrella's canon on 2026-07-21. The old names persist,
un-renamed, only in the frozen `crystalcore` repository.

### Cross References
`07-HISTORY.md` (the rename), `09-GLOSSARY.md`.

---

## Consent Transport (Starline)

### Statement
Peer-to-peer, consent-gated memory exchange between two locally-running
Lumina agents, over a real Noise Protocol handshake
(`Noise_IK_25519_ChaChaPoly_SHA256`). Pull-based, strict 1:1 (no group/
mesh in v1). Binds `127.0.0.1` by default. Revocation takes effect on
the next request, but cannot retroactively delete a fragment a peer
already legitimately received — an explicitly stated, honest limit, not
a bug.

**Status: Implemented.** 9/9 self-tests pass (needs
`requirements-consenttransport.txt`).

### Evidence
- `docs/architecture/crystal-core/STARLINE.md`: "Status: v1 implemented."
- `core/crystal-core/consent_transport/{identity,noise,peers,consent,
  fragment,protocol,transport,discovery,agent,run,selftest}.py` — all
  11 files confirmed present.
- `core/crystal-core/starline/__init__.py`, read in full (38 lines): a
  deprecated backward-compatibility alias, its own docstring stating
  the transport was renamed "so the built layer carries a plain,
  literal name (the mythic 'Starlines' live on in `mythos/`, not
  here)... deprecated and will be removed in a future release."

### Historical Notes
Renamed from "Starline" to `consent_transport` on 2026-07-21 (the same
rename sweep as Starline Weaver). Four separate authoritative-sounding
documents (`docs/architecture/CrystalCore.md`, `Runtime-Glossary.md`,
`core/README.md`, `core/crystal-core/SECURITY.md`) still cited the
deprecated `starline/` alias path as primary before this pass —
corrected 2026-07-24, see `11-CORRECTIONS.md`. `core/README.md`
additionally miscast the alias as a second, separate component
("Starline P2P") alongside Consent Transport, also corrected.
Identity private keys are gitignored and never leave the device;
not encrypted at rest — an explicitly stated, known limit.

### Cross References
`09-GLOSSARY.md`, `11-CORRECTIONS.md`.

---

## RDP (Reciprocal Dawn Protocol)

### Statement
A tamper-evident, hash-chained record layer plus a deterministic,
four-tier decision kernel. Records what other components decide; it
does not govern them, gate anything, or make its own decisions about
consent. The full name — Reciprocal Dawn Protocol — appears in exactly
one place across everything read in this reconstruction; the
portfolio's own terminology glossary, whose stated purpose is to be
authoritative, never expands the acronym.

**Status: Implemented**, v0.2. 31/31 self-tests pass.

### Evidence
- `core/crystal-core/rdp/README.md`, line 1: "Reciprocal Dawn Protocol
  (RDP)."
- `docs/architecture/crystal-core/RDP-INTEGRATION.md`: "RDP records and
  decides; the gates enforce; the Covenant is the law they keep... An
  earlier RDP handoff described a frozen reference kernel and a
  conformance fixture suite to match. Those files never actually
  existed — only the prose did."

### Historical Notes
An explicit, self-disclosed prior overclaim (the "frozen reference
kernel" that never existed) is documented in the component's own
README — a positive signal of the project's honesty discipline, not a
current defect.

### Cross References
`09-GLOSSARY.md`.

---

## CrystalBridge

### Statement
A fail-closed MCP stdio server letting a guest AI (Claude, Grok,
Cursor) meet Lumina with only explicitly granted access. Explicitly
described, in its own module README, as reconstructed from an
incomplete trace — the original design doc was lost with the machine
this project was first built on. As of 2026-07-24 (PR #8,
`TerAustralis-Incognita-Code`): Lumina's package path resolves
correctly to `vision/apps/lumina/crystalcore/` (all four tools work,
not just `status`); the `mcp` dependency is declared
(`core/crystalcore/requirements-bridge.txt`); the consent gate's
docstring truthfully describes the two checks it implements (approval,
tool-permission); and a 7-test `selftest.py` runs in CI on every push.

**Status: Implemented** (the three defects the first pass of this
archive documented here were fixed the same day it published — see
Historical Notes). Still open, unchanged: implementing real
scope/provenance checks remains a future design task (**Designed**, at
most — no spec for either survives anywhere in the repository), and
the module's live dynamic import of Lumina's package remains in
tension with the documented "Crystal Core never imports Crystal
Vision" rule (**Unresolved** — flagged for a maintainer decision, not
touched by the fix).

### Evidence
- `core/crystalcore/README.md`: "config.py and bridge.py were rebuilt
  from scratch — the machine this project was originally written on is
  gone."
- PR #8, `TerAustralis-Incognita-Code`, merged 2026-07-24: the path
  fix in `core/crystalcore/bridge.py` (anchors at the repo root,
  reaches into `vision/`), the new
  `core/crystalcore/requirements-bridge.txt` (declares `mcp>=1.2`,
  matching the sibling `requirements-consenttransport.txt`
  convention), the corrected `gate.py` class docstring, and
  `core/crystalcore/selftest.py` — 7 tests covering the path (a
  regression guard that fails loudly if `LUMINA_PKG_DIR` stops
  resolving) and the gate's real two-check behavior.
- `.github/workflows/ci.yml`: two steps added by PR #8 ("Install
  CrystalBridge dependencies," "CrystalBridge self-test") — the module
  is no longer absent from CI.
- Verified before merge: 7/7 selftest pass under both dependency
  conditions (with `requests` present, the full Lumina framework
  import loads and exposes `Lumina`; without it, the import sub-check
  skips gracefully while the path regression guard still runs).

### Historical Notes
Dated record, per this archive's convention — found and fixed the same
day, 2026-07-24:
- **Found (this archive's first pass):** `bridge.py:35-36` computed
  Lumina's package path as `core/apps/lumina/crystalcore` —
  `core/apps/` never existed; the Stage 1/2 repo split had moved
  Lumina to `vision/apps/` while CrystalBridge went to
  `core/crystalcore/`, and the path math still assumed one shared
  root. `recall`, `teach`, and `message` crashed at runtime; only
  `status` worked. `gate.py:31`'s docstring claimed "Four checks
  fail-closed: approval, permission, scope, provenance" while
  `check()` implemented exactly two — no scope or provenance logic
  existed anywhere in the module, and `GuestGrant` had no field to
  build them on. No file anywhere declared the `mcp` package
  `bridge.py:30` imports, so the module could not run on a fresh
  clone. Zero test coverage; absent from `ci.yml`.
- **Fixed (PR #8, same day):** all three, as described in the
  Statement. The gate fix deliberately corrected the docstring to
  match reality rather than inventing unspecified security semantics —
  the fuller four-check gate is recorded in the docstring itself as a
  separate, deliberate design task for the maintainer.
This was the least-tested, most security-relevant module in the
portfolio; it now has the same selftest-in-CI standing as the four
`crystal-core` protocol-pack components.

### Cross References
`11-CORRECTIONS.md` (Part 3).

---

## Mesh stub

### Statement
An in-process, libp2p-shaped transport stub (`core/node/mesh/`) — Phase
1 of a planned real mesh. No real multiaddrs on the wire. Status table
in its own README: gossipsub/noise/yamux/bootstrap+mDNS all "planned";
mainnet mesh explicitly "HOLD."

**Status: Designed** (the real mesh) / **Implemented** (the stub, as a
stub — it is exactly what it says it is, nothing more).

### Evidence
- `core/node/mesh/README.md`: "Mesh transport stub (libp2p-shaped)...
  no real multiaddrs on the wire."

### Historical Notes
None.

### Cross References
None.

---

## TypeScript SDK

### Statement
A client scaffold for a local node agent. "v0.5 scaffold. No npm
publish. Mainnet HOLD." No consumer wired up against it.

**Status: Designed** (scaffold only).

### Evidence
- `core/sdk/typescript/README.md`.

### Historical Notes
None.

### Cross References
None.

---

## Demo shells (Crystal Interface, Vision-Web)

### Statement
Two static, browser-only demo UIs, explicitly labeled not-production,
Authority HOLD, making no backend calls: `crystal-interface` (operator-
facing) and `vision-web` (citizen-facing, "not a copy of
crystal-interface... a separate, slimmer citizen surface"). Both self-
describe their own economic simulation honestly: "'credits' is a
single in-memory balance — the dual-currency framing is illustrative,
not implemented."

**Status: Implemented** (as demos — they render and work exactly as
documented; nothing about them overclaims production-readiness).

### Evidence
- `vision/apps/crystal-interface/README.md`,
  `vision/apps/vision-web/README.md`, both read in full.

### Historical Notes
Both READMEs' own runnable instructions cited stale, pre-split `src/
apps/...` paths — corrected 2026-07-24, see `11-CORRECTIONS.md`.
`vision-web/README.md`'s own closing note is a good precedent this
archive follows: "Earlier drafts linked docs/journeys/README.md and
compliance/GDPR_ROPA.md; those don't exist in the repo, so they've been
removed rather than left dead."

### Cross References
`11-CORRECTIONS.md`.

---

## Voicebox

### Statement
A tiny local MCP server giving Claude Code a spoken voice via the OS's
own text-to-speech. Stdlib Python only, no cloud, binds `127.0.0.1`.
Separate from Lumina's own browser-based voice.

**Status: Implemented.**

### Evidence
- `vision/apps/voicebox/README.md`, read in full;
  `vision/apps/voicebox/server.py` confirmed present.

### Historical Notes
One stale `src/apps/lumina/` path reference, corrected 2026-07-24.

### Cross References
`11-CORRECTIONS.md`.

---

## Site (teraustralis.com.au)

### Statement
A SvelteKit site, `vision/site/`, that builds to static output and is
deployed via `deploy.yml` to GitHub Pages, fed by `CNAME`
(`www.teraustralis.com.au`). Content is a hand-copied mirror of the
umbrella's `mythos/` — not the canon directly.

**Status: Implemented** (the build/deploy mechanism) — **Unresolved**
whether the domain is actually currently serving this content, because
that is not independently verifiable from this reconstruction's
environment (egress proxy blocks the domain; confirmed directly, not
assumed).

### Evidence
- `vision/site/`, `deploy.yml`, `CNAME` (both root and
  `vision/site/static/`) all confirmed present in
  `TerAustralis-Incognita-Code`.
- GitHub Pages source for this repository has not been switched to
  "GitHub Actions" — confirmed via live GitHub metadata
  (`has_pages:false` for this repository) — a pending manual admin
  step.

### Historical Notes
Pages/CNAME/`deploy.yml` moved here from the umbrella at Migration-Plan
Stage 2. See `02-REPOSITORY-MAP.md` for the full canon→site pipeline
and its live drift instance.

### Cross References
`02-REPOSITORY-MAP.md`.

---

## mythos/crystalcore-os

### Statement
Ten Python files, 2,860 lines total, at `TerAustralis-Incognita/mythos/
crystalcore-os/`. Only one file, `crystalcore_os.py` (563 lines), is
what every document describing this component says it is: a
self-contained text-adventure terminal rendering the Crystal universe
as an interactive command line — 16 documented commands (boot, launch,
burn, network, explore, visit, keys, getkey, starline, song, jump, map,
status, reset, help, exit). That same file also contains a second,
**undocumented** command surface (`detect`, `learn`, `breathe`, `feel`,
`datasets`, `correct`, `learning_status`, `multimodal`, `uncertainty`)
wired to the other nine files. Those nine files are a real, coherent
applied-ML system: `emotional_intelligence.py` (keyword-lexicon emotion
detection), `huggingface_trainer.py` (DistilBERT/GoEmotions fine-
tuning), `cross_attention_fusion.py` (real PyTorch multimodal fusion),
`multimodal_emotion.py`, `uncertainty_quantification.py` (entropy /
least-confidence / margin / Bayesian MC-dropout), `active_learning.py`,
`training_pipeline.py`, `dbt_integration.py` (writes JSONL for the
`dbt/crystalcore_emotion_warehouse` project — its actual, if
undocumented, data producer).

**Status: Implemented** (`crystalcore_os.py`, matching its
documentation exactly) **and Implemented-but-undocumented** (the other
nine files — real, structurally coherent source, not executed as part
of this read-only reconstruction, so runtime correctness beyond
"imports and structure are coherent" was not verified).

### Evidence
- Direct line-count and full read of all 10 files.
- `mythos/CRYSTALCORE-OS.md`: documents only the 16-command surface,
  none of the ML commands.
- Cross-check: no reference to `active_learning`, `cross_attention_
  fusion`, `dbt_integration`, `emotional_intelligence`,
  `huggingface_trainer`, `multimodal_emotion`, `training_pipeline`, or
  `uncertainty_quantification` anywhere in `docs/governance/Roadmap.md`,
  `docs/architecture/Modules.md`, or `docs/vision/CrystalCore.md`.
- `docs/EMOTIONAL_INTELLIGENCE_BLUEPRINT.md`,
  `docs/HUGGINGFACE_INTEGRATION.md`,
  `docs/ADVANCED_UNCERTAINTY_METHODS.md`,
  `docs/DBT_WAREHOUSE_INTEGRATION.md` — the only documents whose
  pseudocode matches this code closely, none cross-referenced from any
  architecture/module/roadmap page. Newly indexed in `docs/README.md`
  this pass (see `11-CORRECTIONS.md`).

### Historical Notes
`ADR-0001` records the intent to move this file, singular
(`mythos/crystalcore_os.py`), to `src/crystalcore-os/` — that move
never happened; the file stayed under `mythos/` and grew into a
directory holding far more than the ADR anticipated.

### Cross References
`05-KNOWLEDGE-MODEL.md` (the Built/Vision classification tension),
`11-CORRECTIONS.md`.

---

## Crystal Runtime

### Statement
A specified, once-implemented, now-lost coordination layer. Fully
covered as a Historical episode, not summarized again here to avoid
duplication.

**Status: Historical.**

### Evidence
See `07-HISTORY.md`.

### Historical Notes
See `07-HISTORY.md`.

### Cross References
`03-ARCHITECTURE.md` (as specified), `07-HISTORY.md` (what happened to
it), `10-PROVENANCE.md` (the commit-level trace).

---

## dbt Emotion Warehouse

### Statement
A structurally professional dbt project (`dbt/crystalcore_emotion_
warehouse/`) — staging and mart models, macros, a GoEmotions-to-Goleman
emotional-intelligence mapping — that is not currently runnable: a
staging model has a genuine SQL syntax error (a dangling `union all`
immediately before a CTE's closing parenthesis), the project config
uses a dbt key removed in dbt ≥1.0, and its one package dependency does
not exist under the name declared. No warehouse is configured anywhere
to run it.

**Status: Designed** (the schema and models are real work) —
**Unresolved** whether it was ever intended to run standalone or was
always meant to be fed by `mythos/crystalcore-os/dbt_integration.py`
(its actual, undocumented producer — see above).

### Evidence
- `dbt/crystalcore_emotion_warehouse/models/staging/
  stg_emotion_labels.sql`, line 32: dangling `union all` before the
  CTE's closing `)`.
- `dbt_project.yml`: uses `data-paths` (removed in dbt ≥1.0).
- `packages.yml`: requires `dbt-labs/expectations` — no such Hub
  package exists under that name.

### Historical Notes
None.

### Cross References
None.
