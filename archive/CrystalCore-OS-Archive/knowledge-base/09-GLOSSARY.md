# Glossary

Canonical definitions, each citing its source. Where a term has more
than one sense in use across the portfolio, both are given and
distinguished — never conflated.

**Belt-Three** — Two senses. (1) *Three laws*, the original form:
Honour Country · Label science/story/vision · No coercion, no fake
hydrology, red button off (`research/seven-sisters/crystalcore-seven-
sisters-FULL.md`). (2) *Three labels*, the operational, PR-facing form
used everywhere in day-to-day process: Science / Story / Vision
(`CONTRIBUTING.md`) — this is law #2 of the three-law origin,
operationalized. See `04-GOVERNANCE.md` for the full distinction.

**Clementine** — Two unrelated senses, both renamed away 2026-07-21.
(1) The original name for the AI companion persona, born in
`The-Crystal-Vision` (2026-07-15); renamed **Lumina** in the current
canon. (2) The original name for the multi-AI message-bus persona
("Clementine Singularity Bridge"), born in the `crystalcore` repo
(2026-07-17); renamed **Starline Weaver** in the current canon. The
`clementine/bridge/` code path is retained as the module name for sense
(2) even after the persona itself was renamed. Only the frozen
`crystalcore` repository still uses "Clementine" natively for sense (2).

**Flagged stale, 2026-08-26 — not yet re-verified against the source
repository, per `12-CONTRIBUTING.md`.** This entry's sense (1) may
itself now be superseded rather than merely historical: `11-CORRECTIONS.md`
Part 20 (filed 2026-08-05) records `The-Crystal-Vision` now carrying the
GitHub name `Clementine---Local-Soveriegn-Edge-AGI`, and this file's own
`00-INDEX.md` (2026-08-08 settled-state note) lists that repository as
public under that name — both suggesting "Clementine" is live and
public-facing again, not "renamed away." See
`ARCHITECTURE-REVIEW-2026-08-26.md` Finding 1 for the evidence trail.
Left as a dated note rather than rewritten, because this archive has not
re-read `TerAustralis-Incognita-Code` directly to confirm it.

**Covenant, the** — Lumina's five binding rules: no influence without
direction; the pause is absolute; memory belongs to the human; support
is offered, never imposed; restraint is respect. `mythos/COVENANT.md`.

**CrystalBridge** — The fail-closed MCP consent gate letting a guest AI
meet Lumina. `TerAustralis-Incognita-Code/core/crystalcore/`. See
`06-COMPONENTS.md`.

**CrystalCore** — A locked four-branch naming taxonomy (ADR-0004): the
**Framework** (Lumina's embedded brain/memory package), the **Protocol
pack** (Starline Weaver + pipeline + Consent Transport + RDP), **
CrystalBridge**, and **CrystalCore OS** (the platform/governance
architecture as a whole). A fifth "CrystalCore-something" is explicitly
barred by the ADR.

**CrystalCore OS vs. CrystalCore.OS** — An acknowledged, deliberately
unresolved naming collision. "CrystalCore OS" (no dot) is the platform/
governance architecture — the whole engineering and documentation
structure. "CrystalCore.OS" (with dot) is the mythos terminal, a
playable text adventure (`mythos/crystalcore-os/crystalcore_os.py`).
`docs/vision/CrystalCore.md` names this as "the one collision this
taxonomy didn't resolve."

**Incognita Rule, The** — The project's core evidence doctrine: "always
mark which lines are dreamed and which are surveyed, and never let a
dreamed line pretend it was measured." `docs/governance/The-Incognita-
Rule.md`. Quoted in full in `00-INDEX.md`.

**Lumina** — The AI companion. Formerly "Clementine" (see above);
renamed 2026-07-21. `TerAustralis-Incognita-Code/vision/apps/lumina/`.
**Flagged stale, 2026-08-26** — see the note under **Clementine** above
and `ARCHITECTURE-REVIEW-2026-08-26.md` Finding 1; whether "Lumina" is
still the companion's current name is unconfirmed by this archive, not
reaffirmed.

**Non Solus** — Latin, "Not Alone." The project's universal sign-off/
motto, appearing across dozens of documents and also printed as a
literal confirmation string by the `crystalcore_os.py` terminal.

**Orion Hunter** — A symbolic guardian figure in the Seven Sisters
corpus: protect / propel / prevent_drift — explicitly not dominate /
coerce / destroy.

**RDP** — Reciprocal Dawn Protocol. A tamper-evident hash-chained
record layer and decision kernel; records, never governs. Full name
found in exactly one place across the entire portfolio (`core/crystal-
core/rdp/README.md`) — the portfolio's own terminology glossary never
expands the acronym. See `06-COMPONENTS.md`.

**Seven Sisters** — A ritual/narrative practice cycle (seven paths,
each linked to a real water basin), written in protocol-manual style.
Not a technical architecture. See `03-ARCHITECTURE.md`.

**Songline** — Reserved exclusively for Aboriginal culture, per
`mythos/NAMES.md`: "'Songline' is not used for any of these — it
belongs to the First Peoples of this land, not to a piece of software."
Formerly used for the software message bus (now Starline Weaver) before
the 2026-07-21 rename; only the frozen `crystalcore` repository still
uses it for the software.

**Starline / Consent Transport** — The peer-to-peer, consent-gated
memory-exchange protocol. Renamed from "Starline" to `consent_transport`
2026-07-21 "so the built layer carries a plain, literal name" — the old
name lives on only as a documented, deprecated import alias
(`core/crystal-core/starline/__init__.py`) and in the mythic sense
(`mythos/` — "Starlines are the map"). See `06-COMPONENTS.md`.

**Starline Weaver** — The multi-AI message bus, `clementine/bridge/`.
Formerly "Songline Bus" / "Clementine Singularity Bridge"; renamed
2026-07-21. See `06-COMPONENTS.md`.

**Starlines / Dreamlines** — The mythic framing behind Starline Weaver
and Consent Transport: "Starlines are the map. Dreamlines are the
traveller of the map." `mythos/NAMES.md`.

**Crystal Runtime** — A specified, once-implemented, now-lost
coordination layer. See `07-HISTORY.md` for the full episode.

**Per-repository short names used in this archive:**
- The umbrella = `TerAustralis-Incognita`
- The Code repo = `TerAustralis-Incognita-Code`
- This repo / the Archive = `CrystalCore.OS-the-Crystal-Architecture-Archive`
- The three frozen repos = `The-Crystal-Vision`, `crystalcore`,
  `crystal-vision`
