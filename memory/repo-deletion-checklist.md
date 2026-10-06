# Original-repository deletion checklist

**Status:** Reference for the repository owner. **Live recheck 2026-10-06:**
the 20 imported source repo names below are **already absent** from
`gh repo list CrystalArchitect` (API 404). Checkboxes remain for Crystal to
confirm intentional deletion and that Pages/issues loss is acceptable — this
is not an instruction to delete again. See [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md)
"Deletion of the 20 original source repositories".

Sourced from [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md), all under the
`CrystalArchitect` GitHub org. **Read the two warnings below before deleting
anything** — they cover the sharpest ways this list could go wrong.

## ⚠️ Warning 1 — two similarly-named repos are not the same repo

- `TerAustralis-Incognita` (no trailing hyphen) — **imported** into
  `archive/`; live GitHub name **GONE** as of 2026-10-06 recheck.
- `TerAustralis-Incognita-` (trailing hyphen) — **NOT imported**. Also
  **GONE** on live inventory (2026-09-18 and 2026-10-06). Confirm via
  packet C before treating as intentional — content is not in this monorepo.

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

**Live GitHub names:** all listed below returned **404** on 2026-10-06
(`gh api repos/CrystalArchitect/<name>`). Checkboxes = Crystal personal
confirm that Pages/issues loss is acceptable, not “still need to delete.”

- [ ] `CrystalCore.OS` → `archive/CrystalCore-OS/` — **GONE live**
- [ ] `TheCrystalVision` → `archive/TheCrystalVision/` — **GONE live**
- [ ] `TerAustralis-Incognita-Code` → `archive/TerAustralis-Incognita-Code/` — **GONE live**
- [ ] `Clementine-ai-companion` → `archive/Clementine-ai-companion/` — **GONE live**
- [ ] `discord-ai-agent` → `archive/discord-ai-agent/` — **GONE live**
- [ ] `ContextGate` → `archive/ContextGate/` — **GONE live**
- [ ] `TerAustralis-Incognita` → `archive/TerAustralis-Incognita/` — **no trailing hyphen; GONE live**
- [ ] `TerAustralis-Incognita-Canon-Gallery` → `archive/TerAustralis-Incognita-Canon-Gallery/` — **GONE live**
- [ ] `CrystalCore-Canon` → `archive/CrystalCore-Canon/` — **GONE live**
- [ ] `The-Library` → `archive/The-Library/` — **GONE live**
- [ ] `TerAustralis-Proposal` → `archive/TerAustralis-Proposal/` — **GONE live**
- [ ] `sat-landing` → `archive/sat-landing/` — **GONE live**
- [ ] `starfleet-au-kangaroo-pack` → `archive/starfleet-au-kangaroo-pack/` — **GONE live**
- [ ] `nostos` → `archive/nostos/` — **GONE live**
- [ ] `CrystalCore-Starlines-Dreamlines` → `archive/CrystalCore-Starlines-Dreamlines/` — **GONE live**
- [ ] `TerAustralis-V2-Presentation` → `archive/TerAustralis-V2-Presentation/` — **GONE live**
- [ ] `CrystalCore.OS-the-Crystal-Architecture-Archive` → `archive/CrystalCore-OS-Archive/` — **GONE live**
- [ ] `TerAustralis-Incognita-V2` → `archive/TerAustralis-Incognita-V2/` — **GONE live**
- [ ] `TerAustralis-Independent-POC` → `archive/TerAustralis-Independent-POC/` — **GONE live**
- [ ] `Synthetic-Affect-Theory` → `archive/Synthetic-Affect-Theory/` — both `Synthetic-Affect-Theory` and `Synthetic-Affect-Theory-` **GONE live**

## NOT in `archive/` — do not delete without a separate decision

These are not represented anywhere in this monorepo. Live recheck 2026-10-06:
all four CrystalCore*/trailing-hyphen names below are also **GONE** (404).
Confirm intentional via packet C — absence is unrecoverable either way.

- [ ] *(no action — listed for completeness)* `CrystalCore.OS-Aeris-Vault12` — **GONE live**; confirm packet C
- [ ] *(no action — listed for completeness)* `CrystalCore-AERIS` — **GONE live**; confirm packet C
- [ ] *(no action — listed for completeness)* `CrystalCore` — **GONE live**; confirm packet C
- [ ] *(no action — listed for completeness)* `TerAustralis-Incognita-` — **GONE live**; confirm packet C (see Warning 1)
- [ ] *(no action — listed for completeness)* `the-algorithm` — excluded on purpose (fork of external code, licensing), not this project's to delete

## After deleting (if you proceed)

Update [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md) and
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) to record which repos were actually
deleted and when — this checklist itself should not silently go stale once
acted on.
