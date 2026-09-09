# CrystalCore.OS Knowledge Base — Index

> **Scope note (2026-07-28).** The reconstruction below covered six
> repositories. The portfolio has seventeen (2026-08-08, late; see 11-CORRECTIONS Part 20 — earlier counts of twelve and eleven were both wrong); the others are recorded in
> `02-REPOSITORY-MAP.md` and `11-CORRECTIONS.md`. Everything else in this
> knowledge base still describes the six it was built from.

Reconstructed 2026-07-24, from a full read of the (then) six-repository
CrystalArchitect portfolio: every ADR, every governance document, the
complete Seven Sisters corpus, every mythos vision/philosophy document,
every formal architecture specification, every component README, full
dated git history across all six repos, and live GitHub metadata
(visibility, issues, pull requests, branches, tags).

## 1. Purpose

This is a **reconstruction of an existing architecture from evidence**,
not a design document, a roadmap, or a proposal. Nothing in this archive
was invented. Every architectural statement here is traceable to a
repository, a file, a commit, an ADR, a README, or a specification —
and where a claim could not be verified, that is stated explicitly
rather than smoothed over.

This archive does not supersede the six repositories' own documentation.
It documents them. If this archive and a primary source ever disagree,
the primary source is right and this archive has a bug — open a
correction per `12-CONTRIBUTING.md`.

## 2. Documentation rules

**The per-section template.** Every factual section in this knowledge
base follows the same structure:

```
## Statement
What is true today.
### Evidence
- Repository / File / Commit / ADR / README / Specification
### Historical Notes
If the architecture changed.
### Cross References
Links to related knowledge-base documents.
```

**The four-question test.** For every significant statement, a reader
should be able to answer:
1. What is the claim?
2. What evidence supports it?
3. Is it implemented, designed, historical, or unresolved?
4. Where can I verify it?

Question 3 is not a new vocabulary — it is the portfolio's own STATUS.md
maturity ladder (Running, Built-not-currently-running, Exists-as-a-
document, Designed-not-built, Concept-only), collapsed to four terms.
Every Statement in this archive states its status explicitly using one
of: **Implemented**, **Designed**, **Historical**, or **Unresolved**.
Question 4 is "Evidence" held to a strict bar: a file path, a line
number, or a commit SHA — precise enough that a reader could actually
go check it, not a citation that merely gestures at having been read.

**The Science / Story / Vision distinction (Belt-Three).** The
portfolio's own governing discipline, and this archive's as well: every
claim is either **Science** (checkable — running code, published fact,
verified repository state), **Story** (narrative honoring a real
tradition, not owned by the project), or **Vision** (the project's own
speculative framing, labeled as such). This archive is written entirely
at the Science layer — it documents Story and Vision content faithfully,
but every claim *this archive itself makes* is a Science-layer claim
about what the repositories contain.

**The governing standard**, quoted from the portfolio's own
`docs/governance/The-Incognita-Rule.md` (TerAustralis-Incognita repo),
because it says exactly what this archive holds itself to:

> "Always mark which lines are dreamed and which are surveyed, and never
> let a dreamed line pretend it was measured."
>
> "A model agreeing with you is not evidence... text a model generates
> about this project is dreamed until surveyed ground — running, tested
> code, or a checkable fact about the world — says otherwise."

## 3. Navigation

Suggested reading order for a new contributor:

1. **`01-SYSTEM-OVERVIEW.md`** — start here. What CrystalCore.OS is,
   today, in one document.
2. **`02-REPOSITORY-MAP.md`** — the six repositories, what each owns,
   how they relate.
3. **`03-ARCHITECTURE.md`** — the technical architecture and the Seven
   Sisters narrative corpus, each described as what it actually is.
4. **`04-GOVERNANCE.md`** — the ADRs, the governance model, the
   licensing history, and the project's own open decisions.
5. **`05-KNOWLEDGE-MODEL.md`** — how the portfolio organizes truth
   (Built/Vision, the STATUS.md ladder, Belt-Three) and how this archive
   fits into that model.
6. **`06-COMPONENTS.md`** — every subsystem, individually, with its
   evidence.
7. **`07-HISTORY.md`** — the dated chronology, including two "built,
   then lost" episodes.
8. **`08-DESIGN-DECISIONS.md`** — why the ADRs went the way they did.
9. **`09-GLOSSARY.md`** — canonical term definitions.
10. **`10-PROVENANCE.md`** — git mechanics, tags, and this session's own
    verification methodology.
11. **`11-CORRECTIONS.md`** — every documentation correction this
    reconstruction made or identified.
12. **`12-CONTRIBUTING.md`** — how to extend this archive correctly.

## 4. Where canonical sources live

This archive is a reconstruction; it is not the canon. The canon lives
across six repositories, each owning a different slice of reality:

| Repository | Visibility (as at 2026-07-24; see note below) | Owns |
|---|---|---|
| `TerAustralis-Incognita` | **Public** | The umbrella: governance, ADRs, architecture documentation, the mythos, research. No application code. |
| `TerAustralis-Incognita-Code` | **Public** (since; see note) | The engine (`core/`) and the user-facing application (`vision/`). |
| `CrystalCore.OS-the-Crystal-Architecture-Archive` | **Public** (since; see note) | This repository — the fleet-wide `STATUS.md` ledger and this knowledge base. |
| `The-Crystal-Vision` | Private | Frozen provenance (tag `vision-safe-2026-07-17`): the codex site and the companion's ancestor code, including a complete bytecode-recovered rescue of a lost laptop's work. |
| `crystalcore` | Private | Frozen provenance (tag `crystalcore-safe-2026-07-17`): the Seven Sisters Songline pack, direct ancestor of `TerAustralis-Incognita-Code`'s `core/crystal-core/`. |
| `crystal-vision` | Private | Frozen provenance: the standalone interface-demo ancestor. |

Full detail: `02-REPOSITORY-MAP.md`. When this archive cites a claim, it
cites the repository and file it came from — go there to verify it
independently.

> **Visibility note (2026-08-08).** The column above was measured on
> 2026-07-24 and has since gone stale in a way worth stating plainly,
> because the second row used to tell a public reader that the page they
> were reading was private. Both `TerAustralis-Incognita-Code` and this
> archive are now public; `TerAustralis-Incognita`, `CrystalCore.OS` and
> `teraustralis-proposal` are public too.
>
> A reader taking the "go there to verify it independently" instruction
> literally should know the limit: several repositories this archive
> cites in prose — `The-Crystal-Vision`, `crystalcore`, `crystal-vision`,
> `teraustralis-incognita-v2`, `teraustralis-v2-presentation`,
> `CrystalCore-Starlines-and-Dreamlines`, `the-library` — remain private.
> Claims sourced to those cannot be checked from outside. None of them
> are linked, so nothing 404s; but the invitation to verify does not
> reach them, and saying so is better than letting a reader discover it.
>
> **Settled state (2026-08-08, late).** Six repositories are public and
> checkable: `TerAustralis-Incognita`, `TerAustralis-Incognita-Code`,
> this archive, `teraustralis-proposal`, `CrystalCore.OS`, and
> `Clementine---Local-Soveriegn-Edge-AGI`. Six more are archived and
> private, five live and private. The private ones stay unverifiable from
> outside, and the limit above holds. See
> [`11-CORRECTIONS.md`](11-CORRECTIONS.md) Part 20 for the full list, the
> count's provenance, and why the count is given with a caveat rather
> than as a certainty.

**A second knowledge base exists** (added 2026-07-24, later same day):
`TerAustralis-Incognita/docs/` now also holds a 7-file, independently
built set covering overlapping ground, from an uncoordinated session
unrelated to this one. This archive's `knowledge-base/` remains
canonical when the two disagree — this was already this archive's own
decision before that second set existed, not a new call made to
resolve the collision. Full account, including independent
corroboration from a separate git-archaeology pass: `11-CORRECTIONS.md`
Part 4, and `REPO-ARCHAEOLOGY-2026-07-24.md` (this repository's root).

## 5. How corrections are made

When this reconstruction found a documentation claim that contradicted
verified repository reality, the rule applied was: **small, mechanical,
high-confidence corrections were applied directly to the source file**;
everything else — code-behavior fixes, anything protected by the
portfolio's own ADR-immutability convention, process/template
redesigns, or large mechanical operations better run as their own pass
— was **documented, not applied**, in `11-CORRECTIONS.md`. Full process
for how a future contributor or session should extend this discipline:
`12-CONTRIBUTING.md`.
