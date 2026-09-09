# Rescued 2026-08-08 — two deleted repositories

Two repositories were deleted from the `CrystalArchitect` account in the week
before 2026-08-08. Their contents existed nowhere else. This folder is a
verbatim rescue of both, taken from GitHub's 90-day restore window on the day
the loss was noticed.

| Rescued from | Head at rescue | Last commit | Files |
|---|---|---|---|
| `CrystalArchitect/CrystalCore.OS-Aeris-Vault12` | `32257ca` | 2026-07-29T23:24+10:00 | 20 |
| `CrystalArchitect/CrystalCore-AERIS` | `24bb8a9` | 2026-07-29T08:12+10:00 | 6 |

## How the loss was found

Not by a backup check. The archive repository's own repository map described
both as current, and a routine cross-check before publishing that archive
found the account listed eleven repositories where the map claimed twelve.
The maintainer confirmed the deletion, and confirmed the contents were gone.

That is worth recording plainly: **the ledger caught this, and nothing else
would have.** No alarm fired, no test failed, no CI job went red. A document
that describes the system disagreed with the system, and the disagreement was
the only signal.

## What was actually at risk

Fourteen of the rescued files existed in no other repository — verified by
hashing every rescued file against every file in all eleven surviving
repositories on the day of the rescue. Among them, the seven technical
specifications that `TerAustralis-Incognita-Code` implements:

- `STARLINE-EDGE-SPEC.md` · `STARLINE-EDGE-NODE-ARCHITECTURE.md`
- `CONSENT-TOKEN-SCHEMA.md` · `NOISE-IK-CONSENT-VERIFICATION.md`
- `TIER0-RUNTIME-LOOP.md` · `LATTICE-STATUS-MESSAGES.md` · `AELTHARION-KEEPER.md`

And seven the archive's map never recorded at all, because it described the
repository from a stale clone — including `ETHICAL-RUNTIME-SPEC.md`,
`THEURGY-AELTHARION-BRIDGE.md`, `ORDINALS-COLLECTION.md`, and a 372-line
`southern-node-lfa-operational-log.md`, the largest single document in either
repository.

Three files differ from versions held elsewhere (`README.md`,
`TERAUSTRALIS-FRAMEWORK.md`, `TERAUSTRALIS-INCOGNITA-STORY.md`). They are kept
as they were, as this folder's rules require, rather than reconciled.

## Status of this material

Archive rules apply, and they matter here: nothing in this folder is
maintained, and nothing new should be built on it. Internal paths, statuses
and claims describe the repositories *as they were on 29 July 2026* and are
deliberately left unfixed — the vault12 README's own status table, for
instance, is a claim about that date, not this one.

**Corrected 2026-08-09, the evening after the rescue.** The paragraph that
stood here claimed the retired name recorded in
[`mythos/NAMES.md`](../../../mythos/NAMES.md) was absent from this material,
and called the edge companion's name here current. That was exactly
backwards, and the maintainer caught it. The name this material uses for
the edge companion throughout **is** the retired name: the check behind the
original sentence tested a guess at which string was retired, when the
ledger's own description — the edge companion's early name — pointed
straight at the name on nearly every page here. The material itself stays
exactly as rescued, per this folder's rules: a retired name inside a frozen
29 July document is history, not reintroduction. Current canon: Clementine
holds the role, and the ledger entry — deliberately unprinted there and
here — is the authority.

## One decision this rescue left open — since made

`CONSENT-TOKEN-SCHEMA.md` and `NOISE-IK-CONSENT-VERIFICATION.md` are not
merely historical. `TerAustralis-Incognita-Code` cites them as the
specifications its consent-transport implementation conforms to, and the
archive's knowledge base carries a conformance table checking specific
sections against that code. A specification the running code is measured
against is load-bearing, and load-bearing documents do not belong in a folder
that says "do not build on this".

**Resolved 2026-08-08, at the maintainer's direction.** Both specs were
promoted — byte-identical, verified with `cmp` — to
`TerAustralis-Incognita-Code/docs/`, beside `CONSENT-GATE-SPEC.md`: the
existing precedent that a spec the code implements rides with the code.
The copies here stay exactly as rescued, per this folder's rules; the
promoted copies are the living ones, and any future revision happens
there, under version control, rather than here. One reference travels
with them unresolved: NOISE-IK §8 names `TIER0-RUNTIME-LOOP.md` as a
companion, and that document remains rescue-only, deliberately — nothing
running is measured against it.

## The general lesson, recorded because it will recur

The provenance manifest (`mythos/tools/provenance.py`) covers a fixed list of
paths inside this repository. Everything it covers was safe by construction on
2026-08-08 — hashed, anchored to Bitcoin, recoverable. Everything outside it
had exactly one copy, and two repositories' worth of that material came within
a 90-day window of being gone.

Work is protected by being inside a repository that is hashed and anchored,
not by existing somewhere on GitHub.
