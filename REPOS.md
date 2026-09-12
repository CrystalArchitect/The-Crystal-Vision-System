# Repository Inventory

**Last updated**: September 12, 2026  
**Reviewed by**: Claude  
**Branch target**: `claude/build-6i5tgq` (all repos)

---

## Active Repositories

### 1. The-Crystal-Vision-System
**Purpose**: Main monorepo consolidating 20 CrystalArchitect projects  
**Status**: ✅ Production  
**Branch**: `claude/build-6i5tgq` (clean)  
**Recent work**: Merged ukf-tracklist data pipeline (PR #3)

**Key contents**:
- `/archive/` — 20 repos imported as git subtrees
- `/memory/` — Shared memory structure (CORE.md, DECISIONS.md, OPEN-QUESTIONS.md)
- New project: `archive/ukf-tracklist/` — Drum & bass tracklist data pipeline (CSV → normalized JSON)

**Health**: ✅ No uncommitted changes, all work merged  
**Next action**: None immediately required

---

### 2. aeon-atlas
**Purpose**: Autonomous agent tracking the aeon fork ecosystem (forks, skill adoption, divergence patterns)  
**Status**: 🚀 Active but incomplete setup  
**Branch**: `claude/build-6i5tgq` (clean)  
**Model**: claude-opus-4-8 (default)

**Enabled skills** (run on schedule):
- `atlas` — Sunday 04:00 UTC: fetch all public forks of aaronjmars/aeon, regenerate ecosystem map
- `atlas-layers` — Sunday 05:00 UTC: render categorical taxonomy view
- `atlas-improve` — 1st of month 06:00 UTC: find high-impact surprises, open PR
- `heartbeat` — 3× daily: health check

**Outputs** (published to GitHub Pages + feed):
- `/universe/` — Interactive Quartz graph of fork ecosystem
- `docs/atlas.html` — Cytoscape interactive map
- `docs/atlas.md` — Readable digest (top forks, active skills, overlap patterns)
- `atlas.json` — Machine-readable ecosystem data
- `feed.xml` — Atom feed (subscribe at `/aeon-atlas/feed.xml`)

**Gaps**:
- ⚠️ **Notification channels not configured** — Memory says to set up Telegram/Discord/Slack (MEMORY.md lines 24–25)
  - Required: `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`, or `DISCORD_WEBHOOK_URL`, or `SLACK_WEBHOOK_URL`
  - Impact: Skills run but cannot notify on success/changes
- ⚠️ **Memory unconsolidated** — MEMORY.md is in template state; no activity logged yet
- ℹ️ **280+ skills disabled** — Most of aeon.yml is commented out; only the four above are active

**Health**: ✅ Clean working tree; ready to run  
**Next action**: **HIGH PRIORITY** — Configure notification secrets and trigger first `atlas` run

---

## Stub Repositories

These are generic Grok-exported templates with no active development or defined purpose.

### 3. jolly-bolt-flora-lotus
**Status**: 📦 Stub / Unused template  
**Branch**: `claude/build-6i5tgq`  
**Last activity**: "Export from Grok" (2 commits, Sept 11)

**Contains**: Generic Vite + Node.js `app-builder-workspace`  
**Documentation**: ✅ README.md added (explains status and next steps)

**Recommendation**: 
- Delete if no planned use, OR
- Adopt as a project template by adding CLAUDE.md + defining purpose

---

### 4. pilot-horizon-acre-spring
**Status**: 📦 Stub / Unused template  
**Branch**: `claude/build-6i5tgq`  
**Last activity**: "Export from Grok" (1 commit, Sept 11)

**Contains**: Identical generic Vite + Node.js `app-builder-workspace`  
**Documentation**: ✅ README.md added (explains status and next steps)

**Recommendation**: 
- Delete if no planned use, OR
- Adopt as a project template by adding CLAUDE.md + defining purpose

---

## Quick Summary

| Repo | Type | Status | Action |
|------|------|--------|--------|
| The-Crystal-Vision-System | Monorepo | ✅ Production | None |
| aeon-atlas | Autonomous agent | 🚀 Active (incomplete) | Configure notifications + run |
| jolly-bolt-flora-lotus | Stub | 📦 Unused | Delete or adopt |
| pilot-horizon-acre-spring | Stub | 📦 Unused | Delete or adopt |

---

## How to Proceed

### For aeon-atlas (recommended):
```bash
cd aeon-atlas

# Add one of these to your GitHub repo secrets:
# Option 1: Telegram
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-chat-id>

# Option 2: Discord
DISCORD_WEBHOOK_URL=<your-webhook>

# Option 3: Slack
SLACK_WEBHOOK_URL=<your-webhook>

# Then run the atlas skill manually to test
# (or wait for Sunday 04:00 UTC for automatic run)
```

### For stub repos:
```bash
# Option A: Delete (if not needed)
git rm -r jolly-bolt-flora-lotus/
git commit -m "Remove unused Grok template"

# Option B: Activate (if you have a use case)
# 1. Define purpose in a new CLAUDE.md
# 2. Update README.md with project goals
# 3. Begin development
```

---

*This file is maintained as a reference. Update after any repo state changes.*
