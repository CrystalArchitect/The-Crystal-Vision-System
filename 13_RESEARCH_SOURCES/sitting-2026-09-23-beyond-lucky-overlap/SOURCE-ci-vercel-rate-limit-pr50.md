# Source note — PR #50 CI: Vercel deploy rate limit (not app failure)

**Checked:** 23 Sep 2026  
**PR:** [#50](https://github.com/CrystalArchitect/The-Crystal-Vision-System/pull/50)  
**Failing checks:**
1. `Vercel – crystal-tiktok-remakes`
2. `Vercel – tiktok-remakes`

## Root cause

Both are **Vercel Git commit statuses**, not GitHub Actions. Deploys never started.

Message: **Deployment rate limited — retry in 24 hours**  
URL: `https://vercel.com/ter-australis-incognita?upgradeToPro=build-rate-limit`

Team **TerAustralis Incognita** is on **Hobby**. Hobby caps deployments/day (~100/24h team-wide). Multiple remake projects wired to the same repo (`crystal-tiktok-remakes`, `tiktok-remakes`, plus orphans `tiktok-remakes-fixed-017d` / `tiktok-remakes-personal`) → every push burns multiple slots. Research-only markdown commits were still triggering remake hubs → quota exhausted.

**Not** a `vercel.json` / HTML / rewrite bug. Live hub https://crystal-tiktok-remakes.vercel.app can still serve the last good deploy.

## In-repo mitigation (this sitting)

| Change | Why |
| --- | --- |
| `tiktok-replica/vercel.json` → `ignoreCommand` | Skip build when hub folder unchanged |
| `scripts/vercel-ignore-tiktok-replica.sh` | Same rule for dashboard Ignored Build Step (repo-root path) |

## Dashboard / API mitigation applied (23 Sep 2026, agent)

Via Vercel MCP (`update_project` / `pause_project`, **no** `teamId`/`slug` — those 404):

| Project | Action |
| --- | --- |
| `crystal-tiktok-remakes` (`prj_i76Zx9NfG3B66TbdKQVcwkNvXGOH`) | `previewDeploymentsDisabled: true` · Ignored Build Step → `bash scripts/vercel-ignore-tiktok-replica.sh` · **keep** live hub |
| `tiktok-remakes` (`prj_iNOdEFQoJcnEdc7jgGucj2zHCOvr`) | `previewDeploymentsDisabled: true` · Ignored Build Step → `exit 0` · pause attempted |
| `tiktok-remakes-fixed-017d` | pause attempted |
| `tiktok-remakes-personal` | pause attempted |

**Why this clears PR reds:** Hobby rate-limit failures are commit statuses on the push that tried to create preview deploys. With preview deploys off, a new PR head should not get new `Vercel – *` failure statuses. Old failures stay on old SHAs only.

## Still useful (human)

1. Confirm orphans disconnected in dashboard if pause did not stick  
2. After Hobby lockout clears (~24h from last burn) **or** Pro: re-enable previews on `crystal-tiktok-remakes` only if PR preview URLs are needed  
3. Do not treat red Vercel statuses as “Academy broken”

## Current red checks

Prior HEAD failed under rate lock. Fix path = stop preview burn + new commit. Unlock for intentional remake deploys still needs wait or Pro.

*Pipe ≠ product. Quota ≠ code.*

## Follow-up (merge to main) — 23 Sep 2026

After PR #50 merged, production Git deploys on `main` failed:

1. **`crystal-tiktok-remakes`** — `ENOENT` / exit 127: dashboard Ignored Build Step ran `bash scripts/vercel-ignore-tiktok-replica.sh` with Root Directory = hub folder → script path missing. Treats ignore-step crash as deploy **ERROR**.
2. **`tiktok-remakes`** — `BLOCKED` from skip/`exit 0` (GitHub surfaces as failure).

**Fix:** local `tiktok-replica/scripts/vercel-ignore.sh` + `vercel.json` `ignoreCommand` relative to Root Directory; force one successful production rebuild to clear commit statuses; keep duplicate project from burning quota after green.
