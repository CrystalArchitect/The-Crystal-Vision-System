# Architecture Review — 2026-08-26

An independent review of this repository, `CrystalCore.OS-the-Crystal-
Architecture-Archive`, run at the maintainer's request to keep the
project's architecture sound. This is a fresh pass, not a follow-up to
any prior AI-generated review — no such review of this specific
repository existed on disk before this file. Scope is this repository
only: its own labelling discipline, its Belt-Three and locked-name
compliance, and whether its own numbered, "canonical" documents could
mislead a reader about what is current.

**Snapshot:** local clone of this repository at `9a1383b` (branch
`main`), read in full — every top-level file and all thirteen
`knowledge-base/` documents. No other repository in the portfolio was
cloned for this pass; where a claim below needs one (Finding 1), that
limit is stated rather than guessed past, per this archive's own
`12-CONTRIBUTING.md` (*"verify the new reality directly against the
repository — not against a chat session's memory"*).

**Evidence tiers**, matching the scheme this repository already uses in
`FULL-REVIEW-2026-07-28.md`:
- **Tier A — executed.** Not used in this review; nothing here runs.
- **Tier B — content-addressed / mechanically resolved.** Grep results,
  exact quotes, line numbers.
- **Tier C — read.** A file was read and is cited or quoted.

All findings below are Tier B/C. This is a documentation review of a
documentation repository — there is no code to execute.

---

## What this repository actually is

This is **not** an archive in the sense of frozen, superseded material —
it is the portfolio's actively maintained **system ledger**: a running
`STATUS.md` (last touched 2026-08-20), a thirteen-document
`knowledge-base/` reconstruction, and a self-correction log
(`11-CORRECTIONS.md`) that the repository's own README and
`12-CONTRIBUTING.md` describe as an ongoing discipline, not a closed
project. `README.md` states this plainly: *"This repository holds no
application code. It documents the other [repositories]"* — and unlike
most of the portfolio's other repositories, `STATUS.md` (line 10)
counts this one among the **6 public living** repositories, not the
6 archived ones. The name "Archive" describes its *function*
(a ledger of record) more than its *state* (it is not read-only, not
frozen, and takes pull requests — PR #38 merged the same day as its
last `STATUS.md` update).

That framing matters for how to read the findings below. The risk this
review was asked to check for — old material being mistaken for current
canon — does not show up here as a frozen legacy document sitting
unlabelled next to a numbered one (the pattern the project's own
`proposal` repo convention warns about). It shows up as a subtler
version of the same failure mode: **numbered, "canonical" documents
(`06-COMPONENTS.md`, `09-GLOSSARY.md`, `02-REPOSITORY-MAP.md`) that were
written once, on 2026-07-24, and describe a fact that has since moved —
with the correction, when it exists at all, buried in `11-CORRECTIONS.md`
rather than reflected where a reader would actually look.** This
repository's own documentation template (Statement / Evidence /
Historical Notes / Cross References) is designed to prevent exactly
this, by carrying a Historical Notes field on every entry — the
findings below are cases where that field was not used when it needed
to be.

---

## Summary

This repository is unusually disciplined for what it is: every
factual claim follows a fixed Statement/Evidence/Historical
Notes/Cross-References template, evidence tiers are used consistently,
and the project holds itself to its own Belt-Three law harder than most
documentation repositories hold themselves to anything
(`00-INDEX.md` §2, `12-CONTRIBUTING.md`). The Indigenous Data
Sovereignty boundary around "Songline" is handled correctly everywhere
it was checked. The one substantive problem found is internal
staleness in exactly the class of file this project's own conventions
say must be trustworthy: the numbered `knowledge-base/` documents assert,
as current canon, a companion name ("Lumina") that this archive's *own*
later-dated evidence (Part 20 of `11-CORRECTIONS.md`, filed
2026-08-05; `00-INDEX.md`'s 2026-08-08 settled-state note) contradicts.
A second, smaller instance of the same pattern affects the bus
validator's name. Both are documented below with a dated flag added to
the glossary in this same change, following this archive's own
prescribed correction process rather than a silent rewrite.

## Strengths

- **The evidence discipline is real, not decorative.** Every
  `knowledge-base/` Statement cites a file, line, commit, or test count
  a reader can independently check (`00-INDEX.md` §2, the "four-question
  test"). Spot-checking several citations (e.g. `06-COMPONENTS.md`'s
  Lumina entry citing `vision/apps/lumina/crystalcore/__init__.py:
  __version__ = "0.7.0"`) found them precise enough to verify, which is
  the actual bar this repository sets for itself.
- **The Indigenous Data Sovereignty boundary is enforced, not just
  stated.** Every occurrence of "Songline" found in this repository is
  either (a) a historical fact about an early prototype's actual old
  name, correctly labelled as retired (`knowledge-base/09-GLOSSARY.md:74`:
  *"Songline — Reserved exclusively for Aboriginal culture"*;
  `knowledge-base/07-HISTORY.md:13`: the 2026-07-21 rename sweep that
  reserved the word), or (b) a quoted violation found in *inbound*
  material and explicitly flagged as such rather than adopted —
  `STATUS.md:101` and `AI-BOOT-PANEL-2026-08-08.md:80-82,218,232,500`
  all identify "Songline" used as a component name by outside AI
  responses and label it a naming-law breach on sight. No file in this
  repository proposes or normalises "Songline" as a component name.
  This is the check this review was specifically asked to run, and it
  passes cleanly.
- **Locked names are not redefined.** `TerAustralis Incognita`,
  `CrystalVision`, and `CrystalCore.Lattice` appear only in ways
  consistent with Constitution §1 — e.g. `AI-BOOT-PANEL-2026-08-08.md:657`:
  *"CrystalCore.Lattice is a Constitution §1 locked name and is
  designed, not built"* — and the same discipline is applied to
  received/inbound documents that get it wrong
  (`GROK-REX-MYTHOS-EXPORT-2026-08-07.md`, Finding 1: a Grok-authored
  line claiming "Lattice integrity: 100%" is flagged, not repeated as
  fact).
- **Received AI-generated material is handled correctly.** The Grok
  "Rex" mythos export, the Weaver Nexus handoff, and the AI Boot Panel
  are each filed with an explicit "authority: none" framing, a
  reception record ahead of the text, and — critically — a policy of
  checking claims against actual commits rather than trusting them
  (`GROK-REX-MYTHOS-EXPORT-2026-08-07.md`: *"a search of all 502
  commits ... found none of them"*). This is the Incognita Rule applied
  correctly to the exact kind of material — confident, dreamed,
  fluent — it exists to catch.
- **The repository is honest about its own staleness in general terms.**
  `00-INDEX.md`'s scope note and `SURVEYED.md` both state plainly that
  the knowledge base was built once, from six repositories, and that
  the portfolio has since grown; `check-freshness.py` exists precisely
  to make drift visible rather than silent. The findings below are
  about that general honesty not yet reaching two specific entries, not
  about the absence of the mechanism.

## Findings

### Finding 1 — HIGH: the companion's canonical name is asserted stale, and the archive's own later evidence contradicts it

**Statement.** `knowledge-base/09-GLOSSARY.md`, `06-COMPONENTS.md`, and
`02-REPOSITORY-MAP.md` all currently assert that the companion's name is
**Lumina**, and that **Clementine** "renamed away 2026-07-21" and is
retained only in a frozen legacy repository. This is presented as
current canon in three of this archive's numbered, "start here" files,
not flagged as historical-only.

**Evidence.**
- `knowledge-base/09-GLOSSARY.md:15-23` (before this review's edit):
  *"Clementine — Two unrelated senses, both renamed away 2026-07-21.
  (1) The original name for the AI companion persona ... renamed
  Lumina in the current canon. ... Only the frozen `crystalcore`
  repository still uses 'Clementine' natively."*
- `knowledge-base/09-GLOSSARY.md:53-54`: *"Lumina — The AI companion.
  Formerly 'Clementine' ... renamed 2026-07-21."*
- `knowledge-base/06-COMPONENTS.md:7-14`: a full "Lumina" component
  entry, **Status: Implemented**, with no mention of Clementine as a
  live alternative.
- `knowledge-base/02-REPOSITORY-MAP.md:250`: *"persona sweep —
  Clementine (companion) → Lumina."*

**Against this archive's own later evidence:**
- `knowledge-base/11-CORRECTIONS.md` Part 17 (filed 2026-07-30, line
  1726): describes the Clementine/companion name collision as *"the
  second naming decision waiting on the maintainer, alongside
  Lumina"* — i.e., as of 2026-07-30, this archive itself still treated
  the choice as **open**, not settled in Lumina's favour.
- `knowledge-base/11-CORRECTIONS.md` Part 20 (filed 2026-08-05, lines
  1903-1908): *"`The-Crystal-Vision` now carries
  `Clementine---Local-Soveriegn-Edge-AGI`. ... each clone's README
  still opens with its old identity ('This is The Crystal Vision —
  codex site + Clementine sovereign companion app')."*
- `knowledge-base/00-INDEX.md:143-147` (2026-08-08, "Settled state"):
  lists **`Clementine---Local-Soveriegn-Edge-AGI`** by name as one of
  the six repositories now public and checkable.

None of this is presented anywhere as a reversal of the Lumina naming —
it sits in the correction log and the index's visibility table, never
folded back into the Statement in `09-GLOSSARY.md` or `06-COMPONENTS.md`
that a reader would actually consult to answer "what is the companion
called." A reader following this archive's own suggested navigation
order (`00-INDEX.md` §3: read `06-COMPONENTS.md` before
`11-CORRECTIONS.md`) would come away certain of exactly the wrong
answer, sourced to this archive's own numbered canon.

**Severity and why.** High, not Medium: this is the project's most
frequently-cited component name, it appears in a public-facing repo
slug the project itself now uses, and the archive's own historical
notes show the "correct" answer flipped at least twice
(Clementine → Lumina on 2026-07-21, per `07-HISTORY.md:13`; then some
signal of Clementine live again by 2026-08-05/08). A reader has no way
to tell from the numbered docs alone that the ground moved.

**Recommendation.** A future session with access to
`TerAustralis-Incognita-Code` should re-verify the companion's current
name directly against that repository (not against this file, per
`12-CONTRIBUTING.md`'s own rule), then update the Statement in
`09-GLOSSARY.md`, `06-COMPONENTS.md`, `02-REPOSITORY-MAP.md`, and the
mentions in `01-SYSTEM-OVERVIEW.md` and `03-ARCHITECTURE.md`
consistently, with a Historical Notes line recording both renames. This
review does not attempt that rewrite — it cannot verify the live
repository from here. As an interim, small, safe measure, this same
change adds a dated flag to the two `09-GLOSSARY.md` entries pointing
here, following this archive's own prescribed process
(`12-CONTRIBUTING.md`: *"add a dated note ... rather than deleting the
old claim outright"*).

### Finding 2 — MEDIUM: "Dreamline Narrator" does not match either current locked name for the bus validator, and has no glossary entry of its own

**Statement.** Two files describe the 2026-07-21 rename as producing
"Starline Weaver + Dreamline Narrator" as the two successor names for
the old Songline Bus. "Starline Weaver" checks out consistently
elsewhere in this archive. "Dreamline Narrator" does not appear as its
own `09-GLOSSARY.md` entry anywhere, and does not match either of the
locked pair the project currently uses for these two distinct roles —
a message-truth validator and a memory-transport traveller, kept as two
separate names in current usage rather than one compound.

**Evidence.**
- `knowledge-base/07-HISTORY.md:13`: *"'Songline Bus → Starline Weaver +
  Dreamline Narrator'."*
- `knowledge-base/02-REPOSITORY-MAP.md:251`: repeats the same phrase.
- `knowledge-base/09-GLOSSARY.md`: has entries for **Starline Weaver**
  (line 88) and **Starlines / Dreamlines** (line 92, the mythic framing)
  but none for "Dreamline Narrator" as a component — a reader cannot
  look the term up in the one document built to define it.

**Severity and why.** Medium, not High: this name appears in only two
places, both historical-chronology entries rather than a component's
own Statement, so the practical exposure is lower than Finding 1. It is
the same class of defect — a name frozen at the moment of a 2026-07-24
reconstruction, never re-squared against later naming decisions.

**Recommendation.** Whoever resolves Finding 1 should also confirm the
correct current pair of names for the validator and transport roles
that the 2026-07-21 rename produced, add a `09-GLOSSARY.md` entry for
whichever term is current, and correct or annotate the two citations
above.

### Finding 3 — LOW: the portfolio's repository count drifts across this repository's own three "start here" documents

**Statement.** `README.md`, `00-INDEX.md`, and `STATUS.md` — the three
files this repository's own README table points a new reader to first —
give three different counts of the portfolio's size, with no
cross-reference reconciling them.

**Evidence.**
- `README.md:3-4`: *"This repository holds no application code. It
  documents the other ten [repositories]."* (implies eleven total,
  including this one)
- `knowledge-base/00-INDEX.md:4`: *"The portfolio has seventeen
  (2026-08-08, late ...)"*
- `STATUS.md:10-11`: *"Constellation: 19 repositories under
  CrystalArchitect (6 public living, 7 private living, 6 archived)."*
  (dated 2026-08-20, the most recent of the three)

**Severity and why.** Low: `STATUS.md` is explicit that it is the most
current count and explains its own provenance, and a careful reader
following the README's link to `STATUS.md` will get the right number.
The risk is narrow — a reader who stops at the README's own opening
paragraph, without following its own link, walks away with a number
that has been wrong since well before this repository's most recent
commit.

**Recommendation.** Point `README.md`'s repository count at `STATUS.md`
by reference (*"documents the other repositories — see `STATUS.md` for
the current count"*) rather than stating a number in the README itself,
so this can't drift again the same way.

## Open questions for a human / architect

1. **What is the companion actually called right now?** This review
   could not check `TerAustralis-Incognita-Code` directly. Finding 1's
   evidence trail is entirely internal to this repository and is
   suggestive, not conclusive — it shows this archive's own confidence
   in "Lumina" eroding over time, not a confirmed final answer. Someone
   with access to that repository at its current HEAD should settle
   this and update the four files named in Finding 1's recommendation.
2. **Is "Dreamline Narrator" a typo for one of the two current locked
   names, or a third, now-abandoned name from between the 2026-07-21
   sweep and whatever produced the current pair?** This archive alone
   cannot distinguish those two possibilities.
3. **Should the numbered `knowledge-base/01-10` documents be
   re-reconstructed wholesale**, now that the portfolio has grown from
   the six repositories they were built from to nineteen, or should the
   current model — a frozen reconstruction plus an append-only
   `11-CORRECTIONS.md` — continue indefinitely? The append-only model is
   transparent about what it is, but Finding 1 shows it can let a
   contradiction sit unresolved for weeks in the exact files a reader is
   directed to first. That is a scaling question for the maintainer, not
   something this review can resolve by itself.
4. **Does the project want a lightweight rule that a `09-GLOSSARY.md`
   entry may not be treated as reaffirmed just because it was written
   once** — e.g., a "last confirmed" date on load-bearing entries like
   component names, separate from the entry's original write date? That
   would have caught Finding 1 mechanically rather than requiring a
   manual review to notice it.

---

*This review changed one file besides itself: `knowledge-base/09-GLOSSARY.md`,
where dated flags were added to the Clementine and Lumina entries per
this archive's own `12-CONTRIBUTING.md` process. No other content in
this repository was rewritten — per this review's own brief, correctness
fixes requiring re-verification against other repositories are left to
a future pass with access to them, listed above as open questions.*
