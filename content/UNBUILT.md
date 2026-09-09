# Unbuilt

*A register of what is described, promised, or implied here but does not
exist. Opened 10 August 2026.*

`ARCHITECTURE.md` opens by saying it is "a design overview, not a description
of currently deployed software." That sentence is honest, and it is also the
only place the distance between the design and the build is acknowledged.
Nowhere does the repository say *which* parts are the unbuilt ones.

This file is that list. It exists because the same rule that governs the maps
governs the product: a dreamed line may be drawn, but it may not be drawn in
the same ink as a surveyed one. A gap nobody has written down is a gap that
gets described as a feature by accident.

Entries are removed when the thing is built, not when it is planned.

---

## 1. The interface a person opens reaches almost none of the companion

**Status: closed but for two conveniences. Opened at 4 of 14 on 10 August
2026; 12 of 14 as of 11 August 2026.**

> The ratio is no longer counted by hand. `tests/test_reachability.py`
> measures it and fails when the set changes in either direction, because
> counting it by hand got it wrong twice — once low, once high. The second
> time was a substring search: `/api/profile` is a substring of
> `/api/profile/meta`, so wiring up the identity panel silently marked
> listing and switching companions as reached too. Update that test and this
> entry in the same commit.

The server declares **17 routes**. Setting aside the three that describe the
service rather than provide it (`/api`, `/api/openapi.json`, and the static
asset handler), **14 are functional. The webapp now calls 12.**

| Reachable from the interface | Reachable only over HTTP |
|---|---|
| `POST /api/chat/stream` | `POST /api/teach` |
| `GET /api/status` | `POST /api/reflect` |
| `GET /api/health` | |
| `GET /api/audit` — the whole record | |
| `GET /api/memories` | |
| `POST /api/forget` | |
| `GET /api/export` | |
| `POST /api/import` | |
| `POST /api/profile/meta` | |
| `GET /api/profile` | |
| `POST /api/profile` | |
| `POST /api/profile/delete` | |

The original entry, kept below unedited, argued that what was unreachable was
"most of what the word *sovereign* is doing in this project". That is no
longer the case, and the change is in kind rather than only in count: seeing
what is held, deleting one memory, leaving with everything, and reading the
consent record are all now in the window.

What remains is a different class of thing, and the register should say so
rather than let a shrinking number imply the rest is merely more of the same:

- `teach` and `reflect` are conveniences. Both are already reachable by
  talking to the companion, which is what the window is for.
- ~~The three remaining `profile` routes.~~ **Built, 11 August 2026.**
  Listing, going to a companion, beginning one, and deleting one. Deleting
  did *not* get restore's copy-aside treatment, and that is the decision
  worth recording: being replaced happens to somebody who did not ask for
  it, so a copy is a kindness; being deleted is asked for, by name, so a
  copy is a betrayal dressed as a safety feature. The backup is offered
  before the fact — as a route, since a companion can only be exported while
  you are with them and only deleted while you are not — and never taken
  after.

`import` was the last destructive operation and is now built, on an endpoint
hardened first: it had answered `{"ok": true}` while replacing a companion
with an empty one, and now refuses a damaged file before writing and copies
what it replaces aside. The identity surface (`profile/meta`) is built too,
which is what finally made the pronoun law reachable by both parties over the
web rather than only in a terminal.

Two follow-ups recorded elsewhere in conversation belong here too, because
both are format-level and neither is a UI question:

- ~~**Stable memory identifiers.**~~ **Built, 11 August 2026.** Notes and
  reflections now carry identifiers that keep meaning the same memory, and
  `forget` removes what it was asked for or nothing at all. Companions that
  predate them are migrated on load, hand-edited entries are given one, and
  the numbered handles the terminal prints still work. The interface's three
  guards were kept but are no longer load-bearing — the entry is left here
  struck through rather than deleted, because a register that erases the
  problems it solved cannot show what it cost to solve them.
- ~~**An anchor outside the audit file.**~~ **Re-scoped and largely closed,
  11 August 2026.** The item was misnamed: an anchor *outside the machine*
  would mean publishing the log's head, which is a network call the human
  never chose and leaks that they use this and how often — the thing the gate
  exists to refuse. An anchor stored locally is no better, since whoever can
  truncate the log can edit a sidecar too. So the anchor is the person's own
  backup: every export now carries the record's length and its last hash, and
  any later log can be checked against it. It closes the hole as far back as
  the last backup and no further, and that boundary is stated wherever the
  answer is shown rather than left to be discovered.

### The original finding, as written on 10 August 2026

Preserved in its original tense rather than quietly updated. A register of
unbuilt work that rewrites its own history each time something ships stops
being evidence of anything — the value is in seeing what was true before, and
what it took to change it.

**All five items below are now built**, as of 11 August 2026: seeing what
is held, deleting one memory, reading the consent record, leaving with
everything and coming back, and — last, because it was the easiest to mistake
for finished — pronouns chosen by either party, over the web as well as in a
terminal.

Building that last one showed the same law half-kept for the *name*:
`choose_name` let the companion name itself over HTTP while nothing let the
human do it, and the attempt answered `{"ok": true}`. That is fixed with it.

#### Why this is not a missing settings panel

That is how it was first described, including by the person writing this
note, and the description was wrong. Counting the routes changed the finding.

What is unreachable is not preference and decoration. It is most of what the
word *sovereign* is doing in this project:

- **A person cannot see what the companion remembers about them.**
  `/api/memories` has no interface. The memory is on their own disk, in their
  own file, and the program they open will not show it to them.
- **A person cannot delete a memory.** `/api/forget` has no interface. The
  right to be forgotten by your own companion is currently exercised through
  a terminal or a `curl` command.
- **A person cannot take their memory with them.** `/api/export` and
  `/api/import` have no interface. Portability that requires a developer is
  not portability; it is a promise with an audience test attached.
- **A person cannot read the consent log.** The interface calls
  `/api/audit?limit=1` and reports two things: how many entries exist and
  whether the hash chain verifies. So it says *"nothing has been tampered
  with"* while showing none of what it is vouching for. That is the weakest
  form of the claim — trust restored by assertion, which is the thing the log
  was built to replace.
- **Neither party can set pronouns.** The law names two who may decide, the
  human and the companion. `/api/profile/meta` now serves both (August 2026),
  and no interface calls it.

Name, avatar, description and model are also unreachable. Those genuinely are
settings, and they are the least of it.

### The shape of the problem

The API is not the gap. Every capability above exists, is described in
`api_surface.py`, is checked against Flask's route table in both directions,
and is covered by tests. Someone building this surface should need to invent
no new endpoints, and should be suspicious of any urge to.

The gap is that the audit of *reachability* was never run. Each endpoint was
built and tested; nothing asked whether a person who does not use a terminal
could get to it. Tests answer "does this work when called." Nothing answered
"can anyone call it."

### Not decided here

Whether this should be built, and in what order. This note records the gap
and its size; it does not argue for a solution, and the sequencing is a
product decision rather than a technical one.

One observation for whoever takes it: the memory and consent items
(`memories`, `forget`, `export`, `audit`) are a different class from the
profile items. The first group is the project's central claim made operable.
The second group is a preferences screen.

---

## 2. `ARCHITECTURE.md` is largely design, and does not say which parts

**Status: acknowledged, unenumerated.**

The document declares its own status in its opening line, which is more than
most such documents do. But a reader cannot tell from it which described
components run today and which are intended. `SOVEREIGNTY.md` was filed
partly to have one document whose claims are all currently true; the
complement — marking the design document's unbuilt sections — has not been
done.

This entry is deliberately thin. Enumerating it properly is an audit, and
nobody has run one. Recording that it has not been run is the honest state.
