# CrystalArchitect Monorepo Index

**Status**: Consolidated (20 repositories imported as git subtrees)  
**Last Updated**: 2026-09-09  
**Archive Location**: `/archive/` subdirectories

---

## Overview

This monorepo consolidates 20 of the 28 total CrystalArchitect repositories using git subtrees. Each repository occupies its own isolated `/archive/<repo-name>/` folder, preserving all files and directory structures without any modifications to the original repositories on GitHub.

**Key Facts**:
- **Imported**: 20 repositories (squashed history)
- **Failed/Excluded**: 4 repositories (private, auth unavailable) + 1 (the-algorithm, fork exclusion per user)
- **Total Scope**: 25 accessible repositories (3 additional repos outside session scope)
- **Branch**: `claude/github-repos-llm-endpoint-0qeomr`
- **Consolidation Method**: Git subtree add with `--squash` (single commit per repo)

---

## Repository Inventory

### Active Implementation Repos (6)

| Repo | Location | Type | Branch | Status |
|------|----------|------|--------|--------|
| CrystalCore.OS | `archive/CrystalCore-OS/` | Backend/LLM | main | ✅ |
| TheCrystalVision | `archive/TheCrystalVision/` | Multi-AI Bridge | main | ✅ |
| TerAustralis-Incognita-Code | `archive/TerAustralis-Incognita-Code/` | Implementation | main | ✅ |
| Clementine-ai-companion | `archive/Clementine-ai-companion/` | Companion AI | master | ✅ |
| discord-ai-agent | `archive/discord-ai-agent/` | Discord Bot | main | ✅ |
| ContextGate | `archive/ContextGate/` | Context Tool | main | ✅ |

### Documentation & Knowledge Repos (5)

| Repo | Location | Type | Branch | Status |
|------|----------|------|--------|--------|
| TerAustralis-Incognita | `archive/TerAustralis-Incognita/` | Umbrella Governance | main | ✅ |
| TerAustralis-Incognita-Canon-Gallery | `archive/TerAustralis-Incognita-Canon-Gallery/` | Canon Archive | main | ✅ |
| CrystalCore-Canon | `archive/CrystalCore-Canon/` | Canon Reference | main | ✅ |
| The-Library | `archive/The-Library/` | Knowledge Base | main | ✅ |
| TerAustralis-Proposal | `archive/TerAustralis-Proposal/` | Proposal Docs | main | ✅ |

### Specialized Tools & Frontends (5)

| Repo | Location | Type | Branch | Status |
|------|----------|------|--------|--------|
| sat-landing | `archive/sat-landing/` | Landing Page | main | ✅ |
| starfleet-au-kangaroo-pack | `archive/starfleet-au-kangaroo-pack/` | UI/Tool | main | ✅ |
| nostos | `archive/nostos/` | Tool | main | ✅ |
| CrystalCore-Starlines-Dreamlines | `archive/CrystalCore-Starlines-Dreamlines/` | Reference | main | ✅ |
| TerAustralis-V2-Presentation | `archive/TerAustralis-V2-Presentation/` | Presentation | master | ✅ |

### Archive & Variants (4)

| Repo | Location | Type | Branch | Status |
|------|----------|------|--------|--------|
| CrystalCore.OS-the-Crystal-Architecture-Archive | `archive/CrystalCore-OS-Archive/` | Archive | main | ✅ |
| TerAustralis-Incognita-V2 | `archive/TerAustralis-Incognita-V2/` | Archive | main | ✅ |
| TerAustralis-Independent-POC | `archive/TerAustralis-Independent-POC/` | POC | main | ✅ |
| Synthetic-Affect-Theory | `archive/Synthetic-Affect-Theory/` | Theory | main | ✅ |

---

## Failed Imports & Exclusions

### Private Repos (Auth Unavailable) — 4 repos

These repositories require authentication credentials not available in non-interactive session:

1. **CrystalCore.OS-Aeris-Vault12** — Authentication blocked
2. **CrystalCore-AERIS** — Authentication blocked
3. **CrystalCore** — Authentication blocked
4. **TerAustralis-Incognita-** — Authentication blocked

**Recovery Path**: Re-run consolidation in interactive session with `gh auth` or SSH keys configured.

### Excluded Repos — 1 repo

1. **the-algorithm** — Fork of external recommendation system code (licensing, not included per user request)

---

## Monorepo Structure

```
AUS-Monorepo/
├── 00_MASTER_INDEX/          [Pre-existing CVSC structure]
├── 07_CELESTIAL_PORTAL/
├── 10_ORIGINAL_CREATIVE/
├── 13_RESEARCH_SOURCES/
├── 99_UNRESOLVED/
├── codex/
├── docs/
├── handoff/
├── memory/
│   ├── CORE.md
│   ├── INDEX.md
│   ├── DECISIONS.md
│   ├── MILESTONES.md
│   ├── OPEN-QUESTIONS.md
│   ├── PRIVACY.md
│   └── README.md
├── STRUCTURE.md
├── README.md
│
└── archive/                   [Monorepo consolidation]
    ├── CrystalCore-Canon/
    ├── CrystalCore-OS/
    ├── CrystalCore-OS-Archive/
    ├── CrystalCore-Starlines-Dreamlines/
    ├── Clementine-ai-companion/
    ├── ContextGate/
    ├── Synthetic-Affect-Theory/
    ├── TerAustralis-Incognita/
    ├── TerAustralis-Incognita-Canon-Gallery/
    ├── TerAustralis-Incognita-Code/
    ├── TerAustralis-Incognita-V2/
    ├── TerAustralis-Independent-POC/
    ├── TerAustralis-Proposal/
    ├── TerAustralis-V2-Presentation/
    ├── The-Library/
    ├── TheCrystalVision/
    ├── discord-ai-agent/
    ├── nostos/
    └── starfleet-au-kangaroo-pack/
```

---

## Individual Repository Status

### Separation & Isolation

✅ **All 20 imported repositories are fully separated and individualized**:

- Each repo occupies its own `/archive/<repo-name>/` subdirectory
- Full file structure preserved (no flattening, no file conflicts)
- Original directory layouts intact and unmodified
- No cross-repo symlinks or file sharing
- Git subtree metadata ensures independent tracking

### Verification

To verify repo contents:

```bash
# List all archived repos
ls -la archive/

# Check a specific repo's files
ls -la archive/CrystalCore-OS/

# View commit history of archived repo
git log --oneline archive/TheCrystalVision/ | head -10

# Confirm subtree isolation
git show archive/TerAustralis-Incognita:memory/CORE.md
```

### Original Repositories

All original repositories remain **untouched** on GitHub:
- No files deleted or modified
- No branches altered
- No tags rewritten
- All history preserved

---

## Git Subtree Details

**Consolidation Method**: `git subtree add --prefix archive/<name> <URL> <branch> --squash`

**Effect of `--squash`**:
- Merges all remote history into a single commit
- Reduces monorepo size (no redundant history)
- Simplifies pull tracking
- Each repo appears as one commit in main monorepo history

**To access original commit history** (if needed):
- Fetch from original GitHub repo
- OR restore from local clones (all available in `/home/user/`)

---

## Next Steps

1. **Verify Separation**: Run verification commands above to confirm isolation
2. **Push Branch**: `git push -u origin claude/github-repos-llm-endpoint-0qeomr`
3. **Create PR**: Draft PR documenting monorepo consolidation
4. **Optional: Import Private Repos**: Run in interactive session with auth configured
5. **Design LLM Endpoint**: Begin three-tier `/generate` endpoint (WebLLM → local → cloud)

---

## User Context

**User Email**: MC_MUSK@icloud.com  
**Project**: CrystalArchitect multi-repo consolidation  
**Decision**: Use existing "AUS-Monorepo" repo as monorepo base  
**Rationale**: Preserve original repos, consolidate discovery in single location  

---

## Notes

- This index is authoritative for monorepo inventory but defers to individual repo `CLAUDE.md` files for repo-specific guidance
- Memory system: See `memory/projects/Code/` in TerAustralis-Incognita umbrella for per-repo state
- Locked canon (Constitution, locked names) is **not** editable without Crystal's explicit approval
- Incognita Rule applies: surveyed (built) vs. dreamed (vision) distinctions must be preserved

---

**Non Solus.**
