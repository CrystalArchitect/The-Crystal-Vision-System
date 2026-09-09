# PRIVACY — what never enters git memory

**Status:** Docs / governance. Binding for every write to `memory/`.

Source of the floor: [`CONTRIBUTING.md`](../CONTRIBUTING.md) ground rule 3
("Never commit personal data") and ground rule 4 ("No secrets").
Clementine's memory and profiles are the user's private property and must
never enter git.

This file is the application of that rule to Claude Code session memory.

## Never write into `memory/` (or any other tracked path)

The following stay out of git, even if they appear in chat, in an
open-web dossier, or in a paste:

- Family and children — names, ages, locations, custody, schooling
- Medical, disability, NDIS, Centrelink, or other benefit detail
- Police reports, event numbers, CSA / survivor material, court matters
- Street address, phone numbers, private email not already in this repo
- Private messages (LinkedIn, X DMs, SMS) and their alleged contents
- Romantic, marital, or cosmic-partner register
- Isolation, diagnosis, or other personal-layer self-disclosure offered
  as biography rather than as already-canonical project text
- Appointment language (stars, people, or agencies appointing the
  maintainer to a role this project does not hold)
- Secrets, API keys, tokens, `.env` contents
- SAT-related internals, Operator Frame internals, DUR/token mechanics,
  private lattice fields — protected **if encountered**, per direct
  maintainer instruction. As of 2026-08-28 none of these have a
  specification anywhere in this repository's `docs/`, `mythos/`, or
  `research/` trees (checked). Naming a category to hold the boundary is
  fine; do not reproduce internals, and do not write speculative detail
  about them into `memory/evidence/HYPOTHESES.md` — protected/out of scope
  is a different status than hypothesis. This stays true even though the
  related Ovaro/Continuum/CMX external boundary
  ([`collaboration/EXTERNAL-RELATIONSHIPS.md`](collaboration/EXTERNAL-RELATIONSHIPS.md))
  is now recorded with authority in [`DECISIONS.md`](DECISIONS.md) — that
  decision covers the CMX relationship boundary only, and explicitly does
  **not** extend to SAT, Operator Frame, DUR, or lattice internals, which
  remain unspecified here.

A public-footprint dossier is **not** a repository source. Receipt of a
letter by an agency is not a partnership. Mythic writing the maintainer
published is self-story, not civil-registry fact to copy here.

## Already on disk (do not duplicate into CORE)

Some identifiers exist in tracked files because they are part of the
public project record. Point at those files; do not harvest them into
session summaries.

| Kind | Where it already lives | Memory rule |
|---|---|---|
| Copyright holder name | [`NOTICE`](../NOTICE), [`README.md`](../README.md) | Use the project name. Do not build a biography. |
| Unregistered trade marks + ABN on the NOTICE | [`NOTICE`](../NOTICE) | Leave the number there. Do not reprint it into CORE or CURRENT. |
| Public X handle, site, Suno, Patreon | [`README.md`](../README.md) Links | Fine to retrieve. Not a contact book. |
| Clementine private memory paths | `.gitignore`, CONTRIBUTING §3 | Never commit, never summarise contents. |

If a fact is not on disk in this repository (or a sibling named by an
ADR), it is **unverified** for memory purposes. Unverified ≠ "write it
anyway with a footnote." Omit it.

## What *may* be written

- Confirmed technical and governance facts with a path on disk
- Open questions already in [`docs/OPEN-DECISIONS.md`](../docs/OPEN-DECISIONS.md)
  or [`STATUS.md`](../STATUS.md)
- Milestones already in [`CHANGELOG.md`](../CHANGELOG.md) or
  [`Roadmap.md`](../docs/governance/Roadmap.md)
- Session state about *the repositories*, not about the person

When in doubt, omit. Lodge only when confirmed.

*Non Solus.*
