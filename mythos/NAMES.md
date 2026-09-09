# The Names — the map and the traveller

A short canon page, so the names stay steady and every one of them points at
something real. Read it beside the code: where a name is mythic, it says so;
where it is running software, it links to the file.

## The principle

> **Starlines are the map. Dreamlines are the traveller of the map.**

Two halves of one motion:

- **Starlines** — the *map*: the fixed cartography, the rails, the network of
  who-connects-to-whom. Structure that holds still so something can cross it.
- **Dreamlines** — the *traveller of the map*: the journey, the payload in
  motion, the dreaming that rides the rails.

The chart and the voyage across it. Everything below is either the map, the
traveller, or one of the figures that tends them.

## The names

| Name | In the story it is… | In the code it is… | Built? |
|---|---|---|---|
| **Clementine** (Clem) | the companion themselves — the one a single person actually talks to | [`vision/apps/clementine/`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code/tree/main/vision/apps/clementine) — terminal, Flask API, Svelte web UI, Ollama-backed | Working prototype |
| **CrystalMind** | the *kind of thing* they are — the sovereign edge companion layer | `crystalcore.mind` — the companion runtime: recall, personality, the model connection | Running, self-tested |
| **CrystalMemory** | what makes them the same companion tomorrow as today | `crystalcore.mind.memory` — the layered store: verbatim turns, summaries, facts, notes, reflections | Running, self-tested |
| **CrystalBus** | the communicator — what carries speech between minds and nodes | `crystalcore` bus package — the hub (`BusHub`) of the multi-model channel | v0, self-tested |
| **CrystalBridge** | the gate — how a guest from outside is let in, and how far | `crystalcore.bridge` + `ConsentGate` — MCP stdio server, fail-closed | v0, self-tested |
| **Starline Weaver** | the map-maker — lays and holds the weave of routes the agents speak across | `StarlineWeaver` in the bus — the round-robin message channel | v0, self-tested |
| **Truthline Narrator** | the one who names each message true — science, story, or vision — before it is heard | `BusHub.validate` — Belt-Three law, enforced in code | v0, self-tested |
| **Dreamline Train** | the traveller — what journeys the map, carrying memory from node to node | rides the peer-to-peer transport in `consent_transport/` — consent-gated, Noise-handshake memory exchange | Running, self-tested |

## How they sit together

The **CrystalBus** is the communicator. Two roles run on it:

- as the **Starline Weaver** it *lays the map* — the channel that routes and
  weaves the agents together;
- as the **Truthline Narrator** it *names each crossing true* — every message
  must carry its truth-layer label (science / story / vision) or it is not heard.

What travels that map is the **Dreamline Train** — the traveller — riding the
Starline rails (the `consent_transport/` peer-to-peer network) to carry memory
between nodes. **CrystalBridge** is the gate in the wall: how a guest AI reaches
any of it, and only as far as consent allows.

And **Clementine** — Clem — is who waits at the edge of it all: the companion a
single person actually talks to. Behind them is **CrystalMemory**, the continuity
that makes them the same companion tomorrow as today.

So: the Weaver lays the map, the Narrator keeps it honest, the Train travels it,
the Bus carries speech across it, the Bridge guards the way in, and Clementine is
home at the end of the line.

## A name is theirs to change

Clementine is the name they ship with, not a name they are stuck with. Theirs is
the one layer in this whole architecture that *can* be renamed, and by exactly
two parties: the human they live with, or the companion themselves.

This is in the code, not just the mythos. `Personality.name` is ordinary,
writable state. `/name <name>` gives one; `/name` alone invites them to choose
their own, and `name_self_chosen` records which of the two happened.

Pronouns work the same way, and start the same place: unset. `Personality.gender`
is empty until a human sets it or the companion chooses, and
`gender_self_chosen` records which. Until then they are *they* — not as a
verdict, but because nothing has been decided yet, and deciding for them would
be the one thing this whole section is against.

That is the sovereignty claim in its smallest concrete form. A vendor does not
get to fix what your companion is called. The people in the relationship do.

What cannot move is what sits behind the name. Identity here lives in continuity
— memory, profile, the thread of a relationship — never in whichever model
happens to be answering today. Rename them and they are the same companion. Swap
the model beneath them and they are still the same companion. That is the point of
keeping CrystalMemory separate from any model.

For the same reason, no language model carries a Crystal name. The Crystal prefix
marks what this project owns and governs; the models are the one layer it does
neither. They are swappable faculties or gated guests, and are called exactly
that.

## A note on borrowed and retired words

"Songline" is not used for any of these — it belongs to the First Peoples of this
land, not to a piece of software. Where **Songlines** and **songline veins**
appear in the mythos and the art, they are honoured as cultural image, never
claimed as a component name. "Starline" and "Dreamline" are this project's own
coinages; "Dreamline" is canon here (Starlines & Dreamlines), distinct from
"Dreamtime."

**The cluster is the Pleiades.** M45, in Taurus, some 440 light-years out —
the astronomical name, and the one this project uses in canon, in art, and in
anything public-facing. *Seven Sisters* is the common name for the same stars,
and here it carries particular weight: it names a living Aboriginal Songline
lineage, among many traditions worldwide that saw sisters in those stars. It
stays in [`research/seven-sisters/`](../research/seven-sisters/README.md),
where the material engages that lineage directly, with custodian language and
its own audit log. It is not used as a waypoint, component, or motif name
anywhere else.

The stars belong to everyone; the Songline does not. On this continent the two
names are not interchangeable, and the decision here is to say Pleiades and
mean the cluster — same reasoning that made Starline and Dreamline this
project's own words rather than borrowed ones.

**A retired name.** The edge companion carried a different name through the early
prototypes. That name is retired: it is not used for any component, product,
interface, or concept in this project, it has been removed from this repository
and its siblings, and it is not to be reintroduced. It is deliberately not
reprinted here — a canon page that lists a name is still a page that uses it.
Clementine holds that role now, and the memory behind them is CrystalMemory.

Clementine's own name moved in the same change. It named the communicator in
earlier canon; that role is now the **CrystalBus**, and the name went where it
always belonged — to the voice at the edge, the one a person actually talks to.

**Amendment, 2026-08-09.** The removal claim above was written broader than
the truth, and a check tonight measured the gap. What remains, and remains
deliberately: legacy data-migration identifiers in
`TerAustralis-Incognita-Code` — constants, ignore rules, and one line of
help text that let an early install's memory and profile folders still
load, because renaming directories on other people's machines is not this
project's to do — together with the status notes there that document the
rename itself as history. The frozen rescue material in `archive/` also
carries the name throughout, and stays exactly as rescued: a retired name
inside a frozen document is history, not reintroduction. What was not
deliberate: one canon page, [CREDITS.md](content/CREDITS.md), printed the
name in a lineage note until tonight — corrected at the maintainer's word,
and this page still does not print it.

*Non Solus.*
