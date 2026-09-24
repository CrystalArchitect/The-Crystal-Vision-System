# DECISIONS

Confirmed decisions about **this repository** (the monorepo/connective
layer). Not a duplicate of any subtree's own decision log — see
[`README.md`](README.md) scope note. Sourced from files already on disk in
this repo; nothing here is invented.

**Write-back:** when a monorepo-level decision is made and merged, add a
dated row. Do not silently overwrite an existing entry — a reversed
decision gets a new entry that says so.

**Agreement check:** plain read
[`00_MASTER_INDEX/NEEDS-YOUR-YES.md`](../00_MASTER_INDEX/NEEDS-YOUR-YES.md)
· agent map [`AGREEMENT-WORKFLOW.md`](../00_MASTER_INDEX/AGREEMENT-WORKFLOW.md)
· `python3 scripts/agreement/status.py --plain`

## 2026-09-19 — Naming: Starline

Decision (Crystal): the name is **Starline** (Consent Transport, Starlines map, Starline Weaver).
*Spread the bird, not the word — because the bird is the word.*
Living Indigenous Country law stays with custodians (homage only).

Plain-language law: [`00_MASTER_INDEX/NAMING-STARLINE.md`](../00_MASTER_INDEX/NAMING-STARLINE.md)  
Index: `CVS-STARLINE` · fence: `CVS-OOB-LINE`  
Hub PR: #32 / #59


## 2026-09-19 — Alive Weave: CrystalBridge ConsentGate in the pulse/weave path

Decision: guests speak on the Alive Weave only after the real CrystalBridge
`ConsentGate` allows (fail-closed). Hub runners call archive `ConsentGate`
(not a stub): allow+token / refuse provenance / refuse approval are pulsed;
weave meters decisions as `signal.gate_check` alongside `signal.bus_message`.
Default on; `--no-gate` opt-out. Still connection ≠ merge; no MCP bridge server
required for this path.

## 2026-09-18 — Alive Weave: connect AI islands; do not merge them

Decision: stand up hub-level **Alive Weave** coordination so the TCV labeled
bridge bus, Starline Weaver, CrystalBridge (ConsentGate), Decode→Ingest→Twin,
and SAT `wrap_turn` can be pulsed and woven from this repo **without**
collapsing named systems into one product.

- Map: [`00_MASTER_INDEX/ALIVE-WEAVE.md`](../00_MASTER_INDEX/ALIVE-WEAVE.md)
- Runners: [`scripts/alive/`](../scripts/alive/) (`pulse.py`, `weave.py`)
- Architecture S4 (bus as event source into decode): **Built** via
  `signal.bus_message` domain in
  [`archive/TheCrystalVision/services/decode.py`](../archive/TheCrystalVision/services/decode.py)
  and hub `weave.py` — hub titles stay Starline / labeled-bus only;
  forbidden legacy labels remain out of bounds (see naming decision
  2026-09-19 / [`NAMING-STARLINE.md`](../00_MASTER_INDEX/NAMING-STARLINE.md)).

Does **not** repeal connection ≠ merge, ADR-0005 (human recommend-then-approve
orchestrator stays docs-first), or LEAF human veto. Celestial Portal docker
compose and live cloud `/generate` remain separate gates.

## 2026-09-09 — Use existing "The-Crystal-Vision-System" repo as the monorepo base

Decision, recorded in [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md): consolidate
discovery of the CrystalArchitect repository portfolio into this existing
repo rather than creating a new one — per [`OPEN-QUESTIONS.md`](../archive/TerAustralis-Incognita/memory/OPEN-QUESTIONS.md)'s
own portfolio-wide rule (ADR-0015, "no new GitHub repository without an
ADR"), also cited from this session. Rationale on disk: preserve the
original repos untouched, consolidate discovery in one location.

## 2026-09-09 — Consolidation method: git subtree `--squash`, one isolated folder per repo

20 of 28 CrystalArchitect repositories imported via
`git subtree add --prefix archive/<name> <URL> <branch> --squash`. Effect:
each repo lands as one commit, full file tree preserved, no cross-repo
symlinks or flattening, isolated under its own `archive/<name>/`. Full
inventory, and the 4 auth-blocked + 1 licensing-excluded repos left out:
[`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md). Original repositories were not
modified, deleted from, or branch-altered by this — the subtree add reads
from GitHub, it does not write back.

Merged to `main` via PR #1 (`claude/github-repos-llm-endpoint-0qeomr`
branch), commit `bcff64a`.

**This does not repeal the root [`README.md`](../README.md) "do not merge
those repos" rule.** The rule is about *canon* — CrystalCore, Clementine,
SAT, Starlines, Dreamlines, TerAustralis, Celestial Portal each keep their
own authority and are not to be treated as collapsed into one project just
because their files now sit in one git history. Subtree import is a
file-custody decision (kept trail vs. staging, per root `README.md` point
4), not a canon decision. See [`README.md`](README.md) scope note for what
this means for memory specifically.

## 2026-09-09 — Three-tier `/generate` endpoint: local + cloud built here; WebLLM documented, not wired

`POST /api/v1/admin/generate` in `archive/CrystalCore-OS/backend/` extended
from single-tier (local llama.cpp only) to a three-tier cascade — webllm
(client-side) → local → cloud (Anthropic API fallback). Full design:
[`archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md`](../archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md).

**Labeled honestly, per this project's own Built/Vision convention** (see
[`archive/TerAustralis-Incognita/memory/README.md`](../archive/TerAustralis-Incognita/memory/README.md)
"Labels" table, and CrystalCore.OS's own belt-tag system in its root
`README.md`):

- **Built:** local tier (pre-existing), cloud tier (new — `generate_cloud()`
  in `app/core/llm.py`), the cascade/fallback logic, and unit + route-level
  tests for all of it (mocked; no live model weights or API key needed to
  run them).
- **Not exercised this session:** the cloud tier's real HTTP call to
  Anthropic — no network access in this sandbox to verify a live request.
  Only the config-missing path is tested.
- **Vision, not Built:** the WebLLM client. No frontend in this repo calls
  `/generate` at all yet (CrystalCore.OS's `index.html` is the unrelated
  OS-desktop demo), so tier 1 has nowhere to run. A reference client is
  documented, not shipped as running code.

## 2026-09-09 — Original (pre-consolidation) repositories: not deleted this session

Deletion of the 20 individual source repositories on GitHub was raised as a
next step in the same session that did the consolidation. **Decision:
deferred, pending explicit per-repo confirmation from the repository
owner.** Deleting a GitHub repository is irreversible and this session's
GitHub access does not include a delete-repository capability in any case
(confirmed against the available tool set). Asked directly; the owner asked
for a checklist rather than execution, produced as
[`repo-deletion-checklist.md`](repo-deletion-checklist.md) — includes two
flagged risks (a same-named-minus-a-hyphen private repo not to confuse with
the imported one, and what `archive/` does and doesn't preserve). See
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) for the live gate.

## 2026-09-18 — Backlog pick: Thread 3 axiom-grounding extract (hub only)

From [`00_MASTER_INDEX/OPEN-BACKLOG.md`](../00_MASTER_INDEX/OPEN-BACKLOG.md)
suggested order: Drive 16–20 and stub delete/adopt remain Crystal-gated.
Default agent connection work without rewriting forks: file Thread 3 extract
and bead links (drawers 16/19/20 + `00_MEMORY`), refresh Thread 3 status in
[`CROSS-DOMAIN-THREADS.md`](../00_MEMORY/CROSS-DOMAIN-THREADS.md). Canon: **no**.
Satellite audit experiments stay outside this decision.

## 2026-09-18 — Hub extracts for Threads 1, 2 (stub), 4, 5

Continues the Thread 3 connection pass: file remaining cross-domain beads in
`00_MEMORY/` and link drawers 16–20 without rewriting fork-mirrors. Thread 2
remains a stub until a combined-detector architecture is chosen. Drive 16–20
and naming still Crystal-gated. Canon: **no**.

## 2026-09-18 — Decision packets; stubs/UK gone on live inventory

Filed [`00_MASTER_INDEX/CRYSTAL-DECISIONS-PENDING.md`](../00_MASTER_INDEX/CRYSTAL-DECISIONS-PENDING.md).
Live `gh repo list` shows **65** public / **0** private; former stubs and
`UK-MonoRepo` are absent. Documented as GONE pending Crystal confirm — agents
do not recreate or delete further. Canon: **no**.

## 2026-09-18 — Naming interim + auth-blocked privates gone + Portal drawer

Documented dual `memory/` (protocol) vs `00_MEMORY/` (research) without
renaming (packet B option 1). Former auth-blocked private import targets also
absent from live list. Expanded `07_CELESTIAL_PORTAL/README.md`. Drive MCP
auth timed out — packet A unchanged. Canon: **no**.


