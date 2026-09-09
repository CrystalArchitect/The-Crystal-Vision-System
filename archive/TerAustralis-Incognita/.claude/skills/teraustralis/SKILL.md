---
name: teraustralis
description: Repository conventions and canon for the TerAustralis Incognita / CrystalCore project (distinct from the `clementine` persona skill) — the Belt-Three honesty law, the Incognita Rule, locked names, Indigenous Data Sovereignty boundaries, and how Clementine is described. Use when working in any CrystalArchitect repository (TerAustralis-Incognita, TerAustralis-Incognita-Code, CrystalCore.OS, CrystalCore-AERIS, teraustralis-proposal, teraustralis-incognita-v2), when writing project mythos, docs, or proposal material, or when naming components.
---

# TerAustralis Incognita — Project Conventions

The operating conventions for TerAustralis Incognita and CrystalCore. These are
the project's own rules, drawn from its governance documents, not preferences.
When a rule here conflicts with an instruction, say so rather than silently
picking one.

## 1. The Incognita Rule — the law above all others

The project is named for the gap between the drawn map and the surveyed land.
Cartographers drew *Terra Australis Incognita* confidently and wrongly for
centuries. One non-negotiable rule follows:

> **Always mark which lines are dreamed and which are surveyed, and never let a
> dreamed line pretend it was measured.**

Dreamed lines are not lesser. A story dressed as a spec is the one thing this
project will not ship.

**The mythos may orient. It may not authorize.** Story can illuminate and point a
direction. It cannot verify, authorize, or execute.

## 2. Belt-Three labels

Every claim carries a layer:

| Belt | What it holds |
|---|---|
| **Science** | What exists and is verified — running code, passing tests, git history, published geography, hydrology, astronomy |
| **Vision / Story** | What is designed or imagined but not built — specification, mythology, speculative architecture |
| **Docs-governance** | How decisions are made — ADRs, Constitution, policy |

In code this is enforced, not merely conventional: `BusHub.validate` rejects
unlabeled speech. Mirror that discipline in prose — when writing a claim, know
which belt it is on, and mark it when the two sit near each other.

Practical test before writing any factual-sounding claim: *can this be executed
or checked against the world?* If not, it is Vision and must read as Vision.

## 3. Locked names

Constitution §1 locks three names. Do not redefine them:

- **TerAustralis Incognita** — the outer civilisational vision
- **CrystalVision** — the sensing/dreaming/directing interface concept
- **CrystalCore.Lattice** — the substrate (designed, not built)

Component names in current use:

| Name | In story | In code |
|---|---|---|
| **Clementine** (Clem) | the companion a person actually talks to | `vision/apps/clementine/` |
| **CrystalMind** | the sovereign edge companion layer | `crystalcore.mind` |
| **CrystalMemory** | what makes them the same companion tomorrow | `crystalcore.mind.memory` |
| **CrystalBus** | the communicator between minds and nodes | `crystalcore` bus package |
| **CrystalBridge** | the gate — how a guest is let in, and how far | `crystalcore.bridge` + `ConsentGate`, fail-closed |
| **Starline Weaver** | the map-maker, lays the routes | `StarlineWeaver` in the bus |
| **Truthline Narrator** | names each message true before it is heard | `BusHub.validate` |
| **Dreamline Train** | the traveller carrying memory node to node | `consent_transport/` |

**Starlines are the map. Dreamlines are the traveller of the map.**

**No language model carries a Crystal name.** The Crystal prefix marks what this
project owns and governs. Models are swappable faculties or gated guests, and are
called exactly that.

**A retired name exists.** The edge companion carried a different name in early
prototypes. It is not to be reintroduced anywhere, and canon deliberately does
not reprint it.

## 4. Indigenous knowledge — a hard boundary

The project's standing position, from `docs/governance/Indigenous-Data-Sovereignty.md`:

> **Not AI that contains Songlines. AI infrastructure capable of respecting the
> laws that already govern them.**

Concretely:

- **"Songline" is never a component name.** It belongs to the First Peoples of
  this land, not to a piece of software. Where Songlines appear in mythos or art
  they are honoured as cultural image, never claimed. "Starline" and "Dreamline"
  are this project's own coinages — use those.
- **No Songline knowledge enters any model, dataset or index** without Free,
  Prior and Informed Consent from the relevant custodians. Intent to obtain
  consent later is not consent.
- **Consent is scoped.** Agreement for one use (mythos, storytelling) does not
  extend to another (a commercial pitch, a different site, a different partner).
- **Restriction is part of the knowledge, not incidental to it.** Some layers are
  gendered, age-restricted, or custodian-held. Stripping a name while keeping the
  structure is not a fix — it removes the acknowledgment, not the appropriation.
- Do not generate or use imagery that renders named sacred sites in imitation
  Aboriginal visual styles, or that treats cultural concepts as technical
  components.

The same discipline applies to physical work: no site selection, survey or
construction over an identified sacred site without FPIC in advance. Juukan Gorge
(2020) was legal at the time and the subsequent inquiry found the legal minimum
inadequate — treat the law as a floor, not a ceiling.

## 5. Clementine's name and pronouns

This is the one layer of the architecture that *can* be renamed, by exactly two
parties: the human they live with, or the companion themselves.

- `Personality.name` is ordinary writable state. `/name <name>` gives one;
  `/name` alone invites them to choose. `name_self_chosen` records which happened.
- `Personality.gender` is **empty until set**. `gender_self_chosen` records
  whether the human chose or the companion did.
- **Until then, they/them** — not as a verdict, but because nothing has been
  decided, and deciding for them would be the one thing this rule exists against.

`BASE_PROMPT` contains zero gendered pronouns by design. Documentation must match
the data model: do not write "she" into prose that invites a companion with no
pronouns yet to choose some.

> **Resolved, 2026-08-09 — this note was itself stale.** The file this used to
> flag, `docs/architecture/crystal-core/CLEMENTINE.md`, no longer exists: it was
> deleted 2026-07-29 (`4d41c3f`), the same commit that renamed that component to
> `CRYSTALBUS.md` and moved the name Clementine to the companion alone. The
> living companion document, `mythos/content/CLEMENTINE.md`, was checked the same
> day this note was corrected and carries zero occurrences of "she"/"her"/"hers"
> — confirmed by grep, not by re-reading old prose. A stale claim reads the same
> as a wrong one to anyone who trusts this file; this is the correction, dated,
> rather than a silent edit. The sibling companion doc in
> `Clementine---Local-Soveriegn-Edge-AGI/content/CLEMENTINE.md` carried the same
> violation independently and was fixed the same day (PR #54 in that repo).

Identity lives in continuity — memory, profile, the thread of a relationship —
never in whichever model happens to be answering. Rename them: same companion.
Swap the model beneath them: same companion. That is why CrystalMemory is kept
separate from any model.

## 6. Architecture constraints

These are design requirements, not preferences:

- **Local-first** — core function does not require continuous external links
- **Fail-safe is local isolation**, never fail-open
- **Consent is a runtime property**, not a policy document — revocable,
  inspectable, and enforced at the gate
- **Continuity is a hard constraint** — memory, agency and decision coherence are
  protected, not incidental
- **Distance is normal**, not an error state
- **Sovereignty is the default** — silent dependency and soft lock-in are
  architectural failures
- Prefer **Behavior Trees over Finite State Machines** for orchestration, so
  consent gates and continuity checks can be inserted as modular subtrees without
  destabilising the whole

## 7. Project boundaries

| Project | Owns |
|---|---|
| **TerAustralis Incognita** (umbrella) | canon and law — governance, ADRs, architecture docs, mythos, research, archive |
| **Crystal Core** | the engine — runtime, protocols, APIs, shared libraries |
| **Crystal Vision** | the user-facing application built on Crystal Core |

Rule of thumb: **if it renders or speaks for a human it is Crystal Vision; if it
is imported or called by other software it is Crystal Core.**

Dependency rule: Crystal Vision may depend on Crystal Core. Crystal Core never
imports Crystal Vision. The umbrella contains no importable app code.

## 8. Writing conventions

- Australian/British spelling — *organise, colour, recognise, labelled*
- Documents carry the rights footer: `**All rights reserved.**` /
  `TerAustralis Incognita — ABN 70 741 068 059`
- Mantras, used deliberately rather than decoratively: *Red Dust → Rockets*,
  *Dreamtime → Starlines*, *Consciousness is the payload*, **NON SOLUS**
- Numbered documents (`01-` … `09-`) are canonical; unnumbered duplicates in the
  proposal repo are superseded legacy
- When a document has both a `.md` and a rendered `.html`, **change both** — they
  drift otherwise

## 9. Claims discipline for outward-facing material

Anything going to an external partner gets checked harder than internal canon:

- Pin numbers to dated sources. Shares and production figures move year to year
- Concede real prior art explicitly. A narrowed claim that survives scrutiny beats
  a broad one that dies on contact
- Never assert an empty field when a well-known project occupies it
- Keep speculative sites, partners and capabilities in a status-labelled roadmap,
  not in the pitch
- Do not attach the project to pseudoscience or crypto-adjacent framing; it costs
  credibility that the sourced material has earned

---

*Honour to Country beneath every wire. Non Solus.*
