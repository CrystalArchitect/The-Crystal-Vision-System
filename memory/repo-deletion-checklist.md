# Original-repository deletion checklist

**Status:** Reference for the repository owner. Not an instruction to any
session to execute — see [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) "Deletion
of the 20 original source repositories" for why this stays a checklist, not
an action. No session has delete-repository access to these repos through
this project's current GitHub tooling; deletion has to happen by hand in
GitHub's own UI (Settings → Danger Zone → Delete this repository, per repo).

Sourced from [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md), all under the
`CrystalArchitect` GitHub org. **Read the two warnings below before deleting
anything** — they cover the sharpest ways this list could go wrong.

## ⚠️ Warning 1 — two similarly-named repos are not the same repo

- `TerAustralis-Incognita` (no trailing hyphen) — **imported**, safe to
  consider once its checkbox below is checked.
- `TerAustralis-Incognita-` (trailing hyphen) — **NOT imported** (private,
  auth-blocked this session). Its content exists **only** on GitHub right
  now. Deleting it would be a real, unrecoverable loss with nothing in this
  monorepo to fall back on. Do not delete it under this consolidation.

## ⚠️ Warning 2 — `archive/` does not preserve everything

Each imported repo's files and directory structure are preserved via
`git subtree --squash` (see [`DECISIONS.md`](DECISIONS.md)). What is **not**
preserved in `archive/`:

- Original commit history (squashed to one commit per repo on import)
- Issues, pull requests, GitHub Discussions
- Stars, watchers, forks (of that repo, not counting this monorepo itself)
- Wiki pages, if any repo had one
- GitHub Pages sites served directly from that repo (a couple of these repos
  reference `crystalarchitect.github.io/<name>/` live demos in their own
  READMEs — check each repo's actual Pages settings, not just this list,
  before deleting one that might be serving a live URL someone links to)

If any of that matters for a given repo, save it out (e.g. export
issues, note the Pages URL and where else it's linked from) before deleting.

## The 20 imported repos — files preserved in `archive/`

Check a box only after you've personally confirmed (not delegated) that
nothing in the "not preserved" list above matters for that repo.

- [ ] `CrystalCore.OS` → `archive/CrystalCore-OS/`
- [ ] `TheCrystalVision` → `archive/TheCrystalVision/`
- [ ] `TerAustralis-Incognita-Code` → `archive/TerAustralis-Incognita-Code/`
- [ ] `Clementine-ai-companion` → `archive/Clementine-ai-companion/`
- [ ] `discord-ai-agent` → `archive/discord-ai-agent/`
- [ ] `ContextGate` → `archive/ContextGate/`
- [ ] `TerAustralis-Incognita` → `archive/TerAustralis-Incognita/` — **no trailing hyphen; see Warning 1**
- [ ] `TerAustralis-Incognita-Canon-Gallery` → `archive/TerAustralis-Incognita-Canon-Gallery/`
- [ ] `CrystalCore-Canon` → `archive/CrystalCore-Canon/`
- [ ] `The-Library` → `archive/The-Library/`
- [ ] `TerAustralis-Proposal` → `archive/TerAustralis-Proposal/`
- [ ] `sat-landing` → `archive/sat-landing/`
- [ ] `starfleet-au-kangaroo-pack` → `archive/starfleet-au-kangaroo-pack/`
- [ ] `nostos` → `archive/nostos/`
- [ ] `CrystalCore-Starlines-Dreamlines` → `archive/CrystalCore-Starlines-Dreamlines/`
- [ ] `TerAustralis-V2-Presentation` → `archive/TerAustralis-V2-Presentation/`
- [ ] `CrystalCore.OS-the-Crystal-Architecture-Archive` → `archive/CrystalCore-OS-Archive/`
- [ ] `TerAustralis-Incognita-V2` → `archive/TerAustralis-Incognita-V2/`
- [ ] `TerAustralis-Independent-POC` → `archive/TerAustralis-Independent-POC/`
- [ ] `Synthetic-Affect-Theory` → `archive/Synthetic-Affect-Theory/` — **name unverified**: `archive/CrystalCore-OS/README.md` names the canonical home `CrystalArchitect/Synthetic-Affect-Theory-` (trailing hyphen, rename "still pending" as of that README). Confirm the exact current GitHub name before deleting — do not delete a guess.

## NOT in `archive/` — do not delete without a separate decision

These are not represented anywhere in this monorepo. Deleting them is a
straight, unrecoverable loss, not a cleanup of something already kept:

- [ ] *(no action — listed for completeness)* `CrystalCore.OS-Aeris-Vault12` — private, auth-blocked this session
- [ ] *(no action — listed for completeness)* `CrystalCore-AERIS` — private, auth-blocked this session
- [ ] *(no action — listed for completeness)* `CrystalCore` — private, auth-blocked this session
- [ ] *(no action — listed for completeness)* `TerAustralis-Incognita-` — private, auth-blocked this session (see Warning 1)
- [ ] *(no action — listed for completeness)* `the-algorithm` — excluded on purpose (fork of external code, licensing), not this project's to delete

## After deleting (if you proceed)

Update [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md) and
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) to record which repos were actually
deleted and when — this checklist itself should not silently go stale once
acted on.
