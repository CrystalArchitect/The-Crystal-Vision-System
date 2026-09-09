# Push to GitHub

Remote: `https://github.com/CrystalArchitect/TerAustralis-Incognita`

Local git has the full tree. GitHub may lag until a full push.

## Option A — GitHub CLI (recommended for full sync)

```powershell
$env:Path = "C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;" + $env:Path
cd C:\Users\cryst\.grok\downloads\TeraAustralis-Incognita

# Interactive browser login (one time)
gh auth login
# GitHub.com → HTTPS → Login with browser → yes git credential

# First-time remote tracking if needed
git fetch origin
git push -u origin main
```

## Option B — Personal access token

```powershell
$env:GITHUB_TOKEN = "ghp_..."   # repo scope
python scripts/push-github-tree.py
```

## Option C — MCP / partial

Grok can push batches via `github__push_files` while the GitHub MCP is connected.
That is **not** a full monorepo mirror — prefer Option A after `gh auth login`.

## Verify

```powershell
gh repo view CrystalArchitect/TeraAustralis-Incognita
gh api repos/CrystalArchitect/TeraAustralis-Incognita/contents/src
```
