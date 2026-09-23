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

## Dashboard (human / Crystal) — still needed

1. **Disconnect or pause auto-deploy** on dead/orphan projects: `tiktok-remakes`, `tiktok-remakes-fixed-017d`, `tiktok-remakes-personal` — keep only `crystal-tiktok-remakes`  
2. On `crystal-tiktok-remakes`: Git → Ignored Build Step →  
   `bash scripts/vercel-ignore-tiktok-replica.sh`  
   (also set via `tiktok-replica/vercel.json` `ignoreCommand` once unlock allows a deploy that reads it)  
3. After Hobby lockout clears (~24h) **or** upgrade to Pro: push or Redeploy once so ignored-build config is live  
4. Do not treat red Vercel statuses as “Academy broken”

## Current red checks

Cannot turn green while the 24h rate lock is active. Mitigation stops **future** research pushes from re-burning quota; unlock requires wait or Pro.

*Pipe ≠ product. Quota ≠ code.*
