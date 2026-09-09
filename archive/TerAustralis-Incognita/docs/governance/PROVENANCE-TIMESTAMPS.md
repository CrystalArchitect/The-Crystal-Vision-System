# Provenance Timestamps — anchoring the work to Bitcoin

**Status:** anchored to Bitcoin on 2026-07-31, twice on 2026-08-07, and
three times on 2026-08-08 via the GitHub Actions workflow — six proofs,
each archived beside the manifest it attests; a workflow re-run on
2026-08-08 also upgraded the fifth proof to its complete Bitcoin
attestation, recorded in the archived pair. The sixth proof covers the
218-file manifest carrying the Quantum Lattice page and its case study.
Awaiting a fresh stamp after the latest change on 2026-08-08.

The manifest changed three times on 2026-07-31 as the work moved (a
recording removed, then the catalogue corrected), twice on 2026-08-07 —
first when new evidence about the Suno subscription dates resolved two
rows in [`mythos/music/README.md`](../../mythos/music/README.md) from
unresolved to settled, then when four artworks were added to
[`mythos/art/`](../../mythos/art/README.md) — and three times on 2026-08-08: first
when seven recordings were added (six Suno "Remaster" takes and Story
as Bridge) and five files were renamed to carry their generation
dates, then when two further new works arrived (Random Topic, Ferry
Slip) alongside a custody note recording that the platform copies of
the non-commercial tracks were deleted, leaving this repository their
only home. A third change the same day added one Vision-layer canon
page (the Quantum Lattice, entered at the maintainer's direction), a
fourth added its checkable companion — a case study with the four code
versions of the lattice metaphor that were delivered, run once each, and
reported that day — and a fifth added the Sovereign Vectors credit
ledger, recording three dated, evidenced consents to public credit. Each
superseded proof is archived in
[`mythos/proofs/`](../../mythos/proofs/) beside the exact manifest it
attests — a pair for every state the work has been in, not just the
latest one. Each remains a true statement about the date it was made.

The current manifest has no proof yet. Run the workflow to take one.

Three attempts have now been made from the environment this tooling was built
in — two on 2026-07-31, one on 2026-08-07 — and all three failed identically:
`need at least 2 attestations but received 0`, because that environment's
network policy rejects CONNECT to all four calendar pools with HTTP 403. The
failure is the sandbox, not the tool or the manifest.

**Anywhere with ordinary internet access will work, including GitHub's own
runners** — which is why the stamping is also wired as a workflow that can be
triggered from a phone browser. See *Running it* below.

### What stands in until then

Nothing here is a substitute, and this section exists so nobody mistakes one
for the other.

GitHub records, server-side, when each commit was **pushed** — a timestamp
written by a party other than the author. That is genuinely better than a git
commit date, which the author sets and can set to anything. It is the floor
this repository currently sits on.

It is a poor ceiling. GitHub is a single company that could alter or lose those
records; the timestamps are not cryptographically verifiable by a stranger; and
they prove receipt by one service rather than existence in the world. A
Bitcoin anchor has none of those weaknesses, which is the entire reason for
preferring it.

So: the work is *evidenced* today and becomes *provable* the moment somebody
taps Run workflow.

## What problem this solves

This repository can already prove *what* it contains. Git hashes every object,
and the archive's hash-chained audit log makes edits detectable.

Two things it cannot do:

1. **Prove when.** Git commit dates are written by whoever makes the commit
   and can be set to any value. They are a claim, not evidence.
2. **Prove it to someone who does not trust the author.** The whole history
   could be rebuilt from scratch by the person who holds the repository.

For a body of creative work — 142 artworks, eleven recordings and the written
canon — those two gaps are the whole question of priority. *I made this, and I made it
first* is currently a claim resting on the author's word.

Anchoring closes both, for free.

## How it works

[`mythos/tools/provenance.py`](../../mythos/tools/provenance.py) walks the
creative work, hashes every file with SHA-256, and writes one sorted manifest
to `mythos/MANIFEST.sha256`. The manifest is deterministic: the same files
produce a byte-identical manifest on any machine, so anyone can rebuild it and
compare.

That single manifest file is then stamped with
[OpenTimestamps](https://opentimestamps.org), which aggregates it into a
Merkle tree with thousands of other submissions and commits the tree root to
the Bitcoin blockchain. One proof covers every file in the manifest.

**No cryptocurrency is involved.** No wallet, no token, no purchase, no
transaction fee. OpenTimestamps calendars pay the Bitcoin fees themselves and
batch submissions; the service is free to use. This matters here because
[the Ordinals licence grant](ORDINALS-LICENCE-GRANT.md) states plainly that
the project issues no token, and nothing in this scheme contradicts that.

## Running it

Regenerate the manifest whenever the work changes:

```sh
python3 mythos/tools/provenance.py
```

Check that the committed manifest still matches the files (useful in CI, and
it names exactly what drifted):

```sh
python3 mythos/tools/provenance.py --check
```

Stamp it. **This step needs network access to the calendar servers**, which
some sandboxed environments block. There are two ways, and the first needs no
computer at all.

### From a phone — the GitHub Actions workflow

GitHub's runners can reach the calendars. `.github/workflows/stamp.yml` does
the whole thing there and commits the proof back:

> **Actions** tab → **Stamp the manifest** → **Run workflow**

That is the entire procedure. No terminal, no laptop, nothing to type. It
refuses to run against a stale manifest, and it runs again every Monday to
upgrade the proof once its Bitcoin block is mined — doing nothing once the
proof is complete.

**One setting can block it.** The workflow needs to push the proof it creates.
If the run fails at the last step with a `403`, the repository is configured to
give Actions read-only access. Fix it once at
**Settings → Actions → General → Workflow permissions → Read and write
permissions**, then re-run. Nothing else about the workflow needs changing.

### From a terminal

One command, same guarantees:

```sh
bash mythos/tools/stamp.sh
```

Run it again an hour later and it upgrades the proof instead of making a new
one. The equivalent by hand:

```sh
pip install opentimestamps-client
ots stamp mythos/MANIFEST.sha256
```

That writes `mythos/MANIFEST.sha256.ots`. Commit it beside the manifest.

The proof is *incomplete* for the first hour or so — the calendars return an
attestation immediately but the Bitcoin block it depends on has not been mined
yet. Upgrade it later, once, and commit the result:

```sh
ots upgrade mythos/MANIFEST.sha256.ots
```

Verify at any time:

```sh
ots verify mythos/MANIFEST.sha256.ots
```

`ots verify` needs to check a Bitcoin block header. It will use a local
Bitcoin node if you have one, or fall back to a public block explorer.

## What the proof says, and what it does not

**It says:** these exact bytes existed no later than the time of Bitcoin block
*N*. That is checkable by anyone, forever, without trusting the author, this
repository, GitHub, or any company — including OpenTimestamps itself, whose
job ends once the hash is in a block.

**It does not say:**

- **Who made the work.** A timestamp proves existence, not authorship. Anyone
  can timestamp anything, including someone else's file.
- **That the work is original.** Stamping something copied from elsewhere
  proves only that you had a copy by that date.
- **Anything about the files themselves.** The proof covers the manifest; the
  manifest covers the files by hash. Change one byte of one artwork and that
  file no longer matches — which is the point, but it means the manifest must
  be regenerated and re-stamped after every change to the work.

That last constraint is a feature, and the tooling now enforces it.

Each stamp is a dated snapshot. When the work changes,
[`provenance.py`](../../mythos/tools/provenance.py) archives the superseded
proof into [`mythos/proofs/`](../../mythos/proofs/) **together with the
manifest it attests** — a proof alone is unverifiable, so the pair is the unit
that has to be kept — and clears the way for a fresh stamp.

Both the workflow and `stamp.sh` refuse to *upgrade* a proof whose attested
hash does not match the current manifest, and say what to run instead. That
guard exists because the alternative failure is the worst kind available here:
a repository that looks anchored while its current state is not. Evidence that
has quietly stopped describing the thing it names is worse than no evidence,
because it is trusted.

## What is covered

The roots are listed at the top of
[`provenance.py`](../../mythos/tools/provenance.py) — the art, the music, the
written canon, the covenant and the names. Build output, dependencies and
generated site trees are deliberately excluded: they are derived from the
sources and would make the manifest churn on every rebuild while proving
nothing about authorship.

Adding a new kind of work means adding its path to `ROOTS`, regenerating and
re-stamping.

## A note on what this is for

Where the work is model-generated — and much of the art and all of the audio
is — copyright may not attach to it at all, since copyright generally requires
a human author. A timestamp does not fix that, and should not be mistaken for
a substitute.

What it does is narrower and still worth having: it establishes that this
particular body of work, in this particular arrangement, existed on a date.
For a project whose value is the coherence of a canon rather than the
exclusivity of any single file, that is the relevant fact to be able to prove.

---

*Not legal advice. This document describes what a cryptographic timestamp
demonstrates, which is a narrower thing than a legal claim to a work.*
