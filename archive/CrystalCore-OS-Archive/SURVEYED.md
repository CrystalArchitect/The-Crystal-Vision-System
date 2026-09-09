# Surveyed

The commit of each repository that this archive's claims were read from.

This file exists because of a specific failure, twice in one session.
On 2026-07-28 this archive stated that the portfolio had six
repositories, and described `crystalcore-os-aeris-vault12` as
"`index.html`, `logo.jpg`, and a README." Both were true of the clones
they were read from. Neither was true by the time anyone read them.
Nothing in the method re-read a source before publishing a claim about
it, so a four-hour-old clone produced an archive that read as current
and was not.

A stale claim and a wrong claim are indistinguishable to a reader. This
file makes the difference visible: every claim here is a claim about a
named commit, and `.github/scripts/check-freshness.py` reports which of
those commits have since moved.

**Staleness is not an error.** The portfolio moves faster than any survey
of it, so drift here is expected and the check does not fail on it. What
it removes is the *silence* — the archive can no longer be quietly out of
date, only visibly behind.

## How to use it

    python3 .github/scripts/check-freshness.py

Re-survey a repository, then update its line. The diff on this file is
the record of what the archive was re-read against, and when.

## The survey

| Repository | Surveyed at | Read |
|---|---|---|
| `TerAustralis-Incognita` | `e9268832dc0cbc0b71943f3415a5879d40c4f212` | 2026-07-29 |
| `TerAustralis-Incognita-Code` | `46c562b9d06204923f19ec1b94697ec4ef0e900d` | 2026-07-29 |
| `CrystalCore.OS-the-Crystal-Architecture-Archive` | `f2414aea539b2e798a977b89a68c0217d17215c2` | 2026-07-29 |
| `The-Crystal-Vision` | `0f3cb8e60ab360f5c94d5772f5d2cc8903ab9959` | 2026-07-29 |
| `crystalcore` | `bd587d1ee3a55d4349f1a98ff957f8dc19a57473` | 2026-07-29 |
| `CrystalCore-Starlines-and-Dreamlines` | `6364d0daa8f98553c4b565357c73933e1ecb11db` | 2026-07-30 |
| `CrystalCore.OS` | `ded3bc1116e2c1b9033c74f6c414a38383fd6ffe` | 2026-07-29 |
| `CrystalCore-AERIS` | `24bb8a9391073e106a7bf7cfee21cb80034de209` | 2026-07-29 |
| `crystalcore-os-aeris-vault12` | `430cce13b1bce6e09a781981db9940df402c85d3` | 2026-07-29 |
| `teraustralis-incognita-v2` | `8d5f4c1ce1a024cc69740fa3e690cc85dc8edce3` | 2026-07-29 |
| `teraustralis-v2-presentation` | `7b58f4f69f623dd68165647592ac0a7533371265` | 2026-07-29 |
| `teraustralis-proposal` | `829156b3935dc736673203468a7e2f296f3cd62b` | 2026-07-29 |

## Known limits of this file

- **It records that a repository was read, not which claims came from it.**
  A moved commit means "something this archive describes may have
  changed", not "this specific Statement is now wrong". Narrowing that
  would mean per-Statement provenance, which is a larger change to the
  documentation template.
- **It is keyed by name, and a rename is invisible to it.** `crystal-vision`
  was renamed to `CrystalCore-Starlines-and-Dreamlines` on 2026-07-29.
  GitHub redirects the old name, so `check-freshness.py` kept resolving the
  old row and reported it as *moved* — indistinguishable from an ordinary
  commit. The row was still fetching the right repository under a name that
  no longer existed. Nothing in this file records a repository's identity
  independently of what it is currently called; keying on the numeric id
  GitHub assigns would fix that, and would also make a rename visible as a
  rename. See `11-CORRECTIONS.md` Part 18.
- **Reachability was described wrongly, twice over.** This section used to
  read: "Only `TerAustralis-Incognita` is public. The freshness check can
  read that one anonymously; the other ten need a checkout or credentials,
  so the check reports them as unverifiable rather than guessing."

  Both halves were false. **Five of the twelve are public**, not one —
  `TerAustralis-Incognita`, `CrystalCore.OS`, `CrystalCore-AERIS`,
  `crystalcore-os-aeris-vault12`, `teraustralis-proposal`. And visibility
  turns out not to be the limit at all: run from a session container with
  the git proxy configured, the check resolves **all twelve**, private
  ones included — `not reachable from here: 0`. The seven private
  repositories need credentials only when the script is run somewhere
  that lacks them.

  So a file written to stop the archive making stale claims was carrying
  one, and it understated its own tool in both directions. Corrected
  2026-07-29 against live GitHub metadata and against the script's actual
  output — recorded in `11-CORRECTIONS.md` Part 15 rather than quietly
  fixed.
