# OPEN QUESTIONS

Live gates at the monorepo level — not yet resolved. Not a duplicate of any
subtree's own open questions (e.g. [`archive/TerAustralis-Incognita/memory/OPEN-QUESTIONS.md`](../archive/TerAustralis-Incognita/memory/OPEN-QUESTIONS.md)).

**Write-back:** when a gate closes, move the resolution to
[`DECISIONS.md`](DECISIONS.md) and strike the row here.

## Held open

| Gate | What is actually open | Label |
| --- | --- | --- |
| Deletion of the 20 original source repositories | Raised as a next step after consolidation. Needs explicit per-repo confirmation from the repository owner before any deletion; this session's GitHub access has no delete-repository capability regardless — deletion has to happen by hand in GitHub's UI. Checklist: [`repo-deletion-checklist.md`](repo-deletion-checklist.md). See below. | Decision-pending |
| 4 auth-blocked private repos not imported | `CrystalCore.OS-Aeris-Vault12`, `CrystalCore-AERIS`, `CrystalCore`, `TerAustralis-Incognita-` — need an interactive session with `gh auth` or SSH keys to import. Recovery path recorded in [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md). | Blocked on credentials |
| `STRUCTURE.md` drawer-name mismatch | [`STRUCTURE.md`](../STRUCTURE.md) row 00_MEMORY maps to `` `00_MEMORY/` `` in this repo, but the actual directory this session found and wrote to is `memory/` (2 files existed before this session: `CORE.md`, `INDEX.md`; now 6). Logged, not silently renamed — a drawer-naming call is Crystal's, not a default of noticing the mismatch. | Vision/logged, not fixed |
| Cloud tier (`/generate`, tier 3) real-call verification | `generate_cloud()` in `archive/CrystalCore-OS/backend/app/core/llm.py` has not been exercised against a live `ANTHROPIC_API_KEY` — this session's sandbox has no network access to verify it. Config-missing path is tested; the real HTTP call and its error handling (rate limits, timeouts) are not. | Untested, not Unknown |
| WebLLM tier (`/generate`, tier 1) frontend | Documented as a reference client in [`archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md`](../archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md), not implemented as running code anywhere in this repo. No admin-panel frontend exists here to wire it into. | Vision |
| pytest suite for the `/generate` changes | Written (`tests/test_llm.py`, extended `tests/test_generate_api.py`) but not executed in this session — PyPI installs are blocked by this sandbox's network policy. Verified with `python3 -m py_compile` only (syntax, not behavior). | Needs a real run |

## Deletion of the original repositories — what would need to be true first

Recorded here rather than acted on, per this session's own risk posture
(irreversible, account-wide action) and this project's "silence is not
permission" rule ([`CORE.md`](CORE.md)):

1. Confirmation, from Crystal directly, of the exact list of repository
   names to delete — not inferred from `MONOREPO-INDEX.md`'s "Imported"
   table by an agent.
2. Confirmation that `archive/` in this repo is accepted as sufficient
   preservation of file content — it is **not** a preservation of original
   commit history, stars, issues, wikis, or GitHub Pages sites tied to those
   repos, per `MONOREPO-INDEX.md`'s own `--squash` note ("reduces monorepo
   size (no redundant history)").
3. A decision on the 4 auth-blocked repos and `the-algorithm` (fork,
   excluded on purpose) — these are not represented in `archive/` at all, so
   deleting the originals would lose them entirely, not just their history.
4. Confirmation this session (or whichever session executes it) actually has
   delete-repository access for the target repos — not assumed from having
   read/write access to `the-crystal-vision-system`.
