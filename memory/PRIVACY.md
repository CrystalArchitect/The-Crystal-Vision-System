# PRIVACY — what never enters this repo's git memory

**Status:** Docs / governance. Binding for every write to this `memory/`
directory. Not a duplicate of any subtree's own privacy file (each subtree
keeps its own — e.g. [`archive/TerAustralis-Incognita/memory/PRIVACY.md`](../archive/TerAustralis-Incognita/memory/PRIVACY.md)
governs that subtree specifically and is not superseded by this file).

## Never write into `memory/` (or any other tracked path in this repo)

- Secrets, API keys, tokens, `.env` contents — this applies directly to
  the `/generate` endpoint work: `ANTHROPIC_API_KEY` is documented by name
  in [`DECISIONS.md`](DECISIONS.md) and the architecture doc, never by
  value. `archive/CrystalCore-OS/backend/.env.example` ships with it blank;
  a real key belongs only in a local, gitignored `.env`.
- Family and household detail, medical/benefit detail, private
  correspondence, private addresses/phone numbers — same floor as every
  subtree in this repo, see any of their own `PRIVACY.md` files for the
  fuller list (they don't disagree with each other on this point).
- Personal data about Crystal Arena-Turner beyond what's already public in
  this repo's own `NOTICE`/`README.md` files.
- Anything a subtree's own `PRIVACY.md` marks protected, if a monorepo-level
  session happens to encounter it while working across `archive/` — this
  file does not loosen any subtree's own floor; it only adds the
  monorepo-specific item above (API keys for the `/generate` endpoint).

## What may be written

- Confirmed facts about this repository's own structure, consolidation, and
  code, with a path on disk (per [`DECISIONS.md`](DECISIONS.md)'s own
  citation discipline)
- Session state about the monorepo itself — what's been imported, what's
  been built, what's still open

When in doubt, omit. Lodge only what is confirmed.

*Non Solus.*
