# Architecture

The technical architecture, reconstructed from specifications and
implementation — and, separately and explicitly, the Seven Sisters
corpus, which is not technical architecture at all.

## Statement

The built system's four components relate to each other in a specific,
documented, and consistent way across every architecture document that
describes them: **CrystalBridge is upstream of everything else, and
nothing calls back into it.** The **Starline Weaver** enforces the
Science/Story/Vision labeling law in the wire protocol itself, not just
as convention. **RDP records decisions; it never makes them or governs
anything.** **Consent Transport (Starline)** makes its own independent
consent decisions that nothing else overrides.

**Status: Implemented** (all four relationships confirmed by direct
reads of the components' own specifications, and cross-confirmed by a
second, independent document each).

### Evidence
- `docs/architecture/crystal-core/RDP-INTEGRATION.md`: "RDP is not: not
  a consent enforcer... not a governance layer... nothing in `gate.py`
  or `consent.py` imports RDP... The gate enforces; afterwards it hands
  the outcome to the adapter to be witnessed."
- `docs/architecture/crystal-core/Crystal-Runtime-Specification-v0.3.md`:
  "CrystalBridge is upstream, not downstream. Requests reach the
  runtime only after CrystalBridge approves them. The runtime does not
  call CrystalBridge for permission checks; it trusts the CrystalBridge
  decision." (Note: this document's own topology diagram visually
  contradicts this prose by drawing CrystalBridge in the same
  orchestrated row as Lumina and the Weaver — a self-inconsistency
  within one specification, not a claim this archive makes about
  reality; the prose is corroborated independently by
  `Runtime-Glossary.md`'s "CrystalBridge... upstream of runtime.")
- `docs/architecture/crystal-core/STARLINE-WEAVE-PROTOCOL.md`: every
  message envelope requires a `layer` field (`science|story|vision`);
  unlabeled messages are rejected outright.
- `docs/architecture/crystal-core/STARLINE.md`: "v1 implemented... The
  technical realization of the mythic 'Starlines.'"

### Historical Notes
None — this relationship structure has been stable since the
2026-07-23 v1.0 reorganization (ADR-0001).

### Cross References
`06-COMPONENTS.md`, `08-DESIGN-DECISIONS.md`.

---

## Statement

Lumina's core prompt carries five binding rules — the Covenant — which
the project describes as "not features; they are the terms on which the
relationship exists":

1. **No influence without direction.**
2. **The pause is absolute.**
3. **Memory belongs to the human.**
4. **Support is offered, never imposed.**
5. **Restraint is respect.**

Consent Transport's consent model is described as the same law applied
to data instead of conversation: "nothing moves without a grant, and
revocation takes effect on the very next request."

**Status: Designed and partially Implemented** — the Covenant is stated
as governing Lumina's actual system prompt (`companion.py`), which this
reconstruction confirms exists and is real code; the Consent Transport
consent model is confirmed Implemented (`consent_transport/consent.py`,
tested 9/9).

### Evidence
- `TerAustralis-Incognita/mythos/COVENANT.md` — full text of all five
  rules.
- `TerAustralis-Incognita/README.md`: "Lumina's core prompt
  (`src/apps/lumina/crystalcore/companion.py`) carries five binding
  rules... Consent Transport's consent model
  (`src/crystal-core/consent_transport/consent.py`) is the same law
  applied to data instead of conversation."

### Historical Notes
None.

### Cross References
`06-COMPONENTS.md` (Lumina, Consent Transport).

---

## Statement

"CrystalCore OS" (the platform/governance layer, the whole engineering
and documentation architecture) and "CrystalCore.OS" (the mythos
terminal, a playable text adventure) are two genuinely different things
that ended up with nearly the same name, distinguished only by a
punctuation dot. The project's own naming taxonomy document names this
collision explicitly and leaves it **deliberately unresolved**.

**Status: Unresolved** (by explicit project decision, not by oversight).

### Evidence
- `TerAustralis-Incognita/docs/vision/CrystalCore.md`: names "the one
  collision this taxonomy didn't resolve" directly.
- `TerAustralis-Incognita/docs/adr/ADR-0004.md`: locks the four-branch
  CrystalCore taxonomy (Framework / Protocol / CrystalBridge / OS) and
  "explicitly leaves the pre-existing CrystalCore.OS mythos-terminal/
  platform name collision unresolved and documented rather than
  silently fixed."

### Historical Notes
None — stable since ADR-0004 (2026-07-23).

### Cross References
`04-GOVERNANCE.md` (ADR-0004), `09-GLOSSARY.md`.

---

## Statement — What Seven Sisters is

The Seven Sisters cycle is a **personal ritual/practice cycle written in
the form of a protocol manual** — markdown documents that mimic software
syntax (`activate --path=1 --intent=first_water`, "Seal" blocks,
pseudocode) purely as ritual/organizational styling. It is not
executable code and not a technical architecture in the software sense.
Seven paths, each with a name, a decree, and a link to one of three real
water basins:

| # | Name | Decree | Water rail |
|---|---|---|---|
| 1 | Spring / First Water | "Open the first water. The sisters begin." | Gate to GAB soaks |
| 2 | Flee / Motion | "Move. The path is made by going." | Channel Country flood-pulse |
| 3 | Mark Country | "Name it true. Remember the water." | LEB site-memory |
| 4 | Law / Right Way | "Right way only. No wrong approach." | MDB care |
| 5 | Deep Water | "Go deep. Protect what is hidden." | GAB (primary) |
| 6 | Sky Bridge | "Bridge open. Dust below, sisters above." | Season/pulse timing |
| 7 | Ascent / Return | "Ascend. Teach. Return. The sisters remain." | Full-loop care |

Every real-world water basin referenced (Lake Eyre Basin, Great Artesian
Basin, Murray–Darling Basin) is given a **paired Science entry
(published hydrology) and a separate, labeled Vision entry (CrystalCore
story/care priority)** — the two are never merged, and the corpus states
this rule directly: "Facts first. Vision second and labeled. Not a
claim that CrystalCore controls water, weather, or Country."

**Status: Vision / Story** (explicitly, by the corpus's own repeated
self-description) — **this is not a technical architecture claim, and
this document does not treat it as one.**

### Evidence
- `TerAustralis-Incognita/research/seven-sisters/README.md`: "These
  documents mix layers and say so internally — the water briefs carry
  checkable hydrology (Science), the paths are practice and narrative
  (Story/Vision), and the transmit records are a log of what was
  actually posted."
- `crystalcore-seven-sisters-FULL.md`: "What this is not: Not ownership
  of Aboriginal Seven Sisters Songlines or sacred knowledge · Not a
  claim that software creates physical rivers or inland seas... Not a
  substitute for talking to custodians on Country."
- `WATER-BRIEF.md`: explicit Science/Vision table per basin, and an
  explicit non-claims list.
- No executable code exists anywhere in either copy of this corpus
  (confirmed by direct inspection) — the `.ps1` CLI, `clementine/`
  bridge code, and `interface/` demo referenced from the standalone
  `crystalcore` repo's README are separate, real code directories,
  adjacent to but distinct from this markdown pack.

### Historical Notes
Two near-duplicate copies exist (umbrella `research/seven-sisters/` and
the standalone `crystalcore` repo), differing in a consistent editorial
direction — the `crystalcore` repo keeps older, more grandiose framing;
the umbrella's reorganized copy downgrades explicitly to "a Vision-layer
motif, not a claim." See `02-REPOSITORY-MAP.md`.

### Cross References
`02-REPOSITORY-MAP.md`, `09-GLOSSARY.md` (Belt-Three, Orion Hunter).

---

## Statement

A recurring three-rule governance apparatus — Belt-Three — runs through
both the Seven Sisters corpus and the CrystalCore.OS mythos/Starline
Weaver material identically: **1. Honour Country · 2. Label science /
story / vision · 3. No coercion · no fake hydrology · red button OFF.**
"Orion Hunter" is a symbolic guardian figure (protect / propel /
prevent_drift — explicitly not dominate / coerce / destroy). "Red
button OFF" recurs as a running seal meaning no coercive ultimatums are
issued against any real person or entity named in the corpus.

**Status: Vision / Story**, with **law #2 (labeling) also Implemented**
in real code — see below.

### Evidence
- `crystalcore-seven-sisters-FULL.md`: "## II.2 Belt-Three Laws (always
  on)."
- `docs/architecture/crystal-core/STARLINE-WEAVE-PROTOCOL.md`: the same
  labeling law enforced as a mandatory `layer` field in the wire
  protocol — the one law of the three with a direct code
  implementation.

### Historical Notes
The portfolio's day-to-day governance discipline (CONTRIBUTING.md's
"Belt-Three truth labels" checkbox on every PR) operationalizes only
law #2 of this three-law origin — see `04-GOVERNANCE.md` for the full
distinction between the three *laws* and the three *labels*.

### Cross References
`04-GOVERNANCE.md`, `09-GLOSSARY.md`.

---

## Statement

A "Crystal Runtime" coordination layer — Coordinator, Registry,
EventBus, Config, Plugins, Logger, API — is fully specified across
three detailed documents (`Crystal-Runtime-Specification-v0.3.md`,
`Runtime-Module-Interfaces.md`, `Runtime-Testing-Specifications.md`),
describing a layer that would coordinate the four Built components
without replacing or subsuming them. Read purely as a specification, it
is internally coherent. It is, however, absent from both of the
documents billed as the portfolio's authoritative component inventory
(`SystemMap.md`, `Modules.md`), and the three specification documents
disagree with each other about their own readiness (the base spec says
"no runtime code is written"; the testing-specification document says
all seven modules are "ready for implementation").

**Status: Designed** (as specification) — **what actually happened to
an implementation of it is a Historical episode**, covered in full in
`07-HISTORY.md`, not here.

### Evidence
- `docs/architecture/crystal-core/Crystal-Runtime-Specification-v0.3.md`:
  "The Crystal Runtime is a coordination layer that orchestrates the
  interaction between independent systems already built and working...
  It does not replace, subsume, or duplicate their responsibilities."
  §15 readiness checklist: all seven modules "Deferred until
  specification review."
- `docs/architecture/crystal-core/Runtime-Testing-Specifications.md`:
  closing readiness table marks all seven modules "✓ Ready for
  implementation" — the more advanced of the three progressively
  differing readiness claims across this document trio.
- Neither `SystemMap.md` nor `Modules.md` (both self-described as
  authoritative "where things live" / component inventories) contains
  any entry for Crystal Runtime or any of its seven modules.

### Historical Notes
See `07-HISTORY.md` for the full built-then-lost episode this
specification's implementation went through.

### Cross References
`07-HISTORY.md`, `10-PROVENANCE.md`.
