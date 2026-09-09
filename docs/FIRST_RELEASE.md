# First Production Release Guide

> **Status note (2026-07-23):** none of this ever happened — the `packages/`
> structure this guide assumes ready for release never landed in this
> repository's git history. Kept for provenance. See
> [SystemMap: where the code actually lives](architecture/SystemMap.md#where-the-code-actually-lives).

This guide walks through publishing the first version of TeraAustralis packages to PyPI.

## Current State

All 7 packages are at **v1.0.0** and ready for release:
- ✅ Code merged to main
- ✅ CI/CD workflows configured
- ✅ Documentation complete
- ⏳ PyPI publishing setup (your step)

## Step 1: Setup PyPI Account & Token

### Create PyPI Account (if needed)
1. Go to https://pypi.org/account/register/
2. Create account with organization email
3. Enable 2FA for security

### Generate API Token
1. Login to https://pypi.org/manage/account/tokens/
2. Click "Add API token"
3. Name: `teraaustralis-ci-release`
4. Scope: Entire account (for all packages)
5. Copy token (you'll only see it once)

**Token Format:** `pypi-AgEIcHlwaS5vcmc...` (starts with `pypi-`)

## Step 2: Add Token to GitHub Secrets

### Via GitHub Web UI

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: (paste your token from Step 1)
5. Click "Add secret"

### Via GitHub CLI

```bash
gh secret set PYPI_API_TOKEN
# Paste your token when prompted
```

### Verify Secret Added

```bash
gh secret list
# Should show: PYPI_API_TOKEN   actions  Updated 2026-07-23
```

## Step 3: Test Build Locally (Optional)

Before releasing, test building locally:

```bash
# Install build tools
pip install build twine

# Test build a single package
cd packages/clementine
python -m build
ls dist/

# Check distribution
twine check dist/*
cd ../..
```

Expected output:
```
teraaustralis-clementine-1.0.0.tar.gz
teraaustralis_clementine-1.0.0-py3-none-any.whl
✓ Check passed
```

## Step 4: Create Release Tags

### Option A: Release All Packages (Synchronized)

Tag version applies to all packages:

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Initial release: all 7 packages"

# Push to trigger CI/CD
git push origin v1.0.0
```

### Option B: Release Individual Packages

Release packages at different times:

```bash
# Release Clementine
git tag -a clementine-v1.0.0 -m "Clementine 1.0.0 - Local-first AI companion"
git push origin clementine-v1.0.0

# Later: Release RDP
git tag -a rdp-v1.0.0 -m "RDP 1.0.0 - Decision kernel"
git push origin rdp-v1.0.0

# etc.
```

### Recommended: Phased Release

Release high-maturity packages first:

1. **Week 1:** `clementine-v1.0.0` (most stable)
2. **Week 2:** `rdp-v1.0.0`, `consent-v1.0.0`
3. **Week 3:** `starline-v1.0.0`, `ei-v1.0.0`
4. **Week 4:** `bridge-v1.0.0` (requires license review), `mythos-v1.0.0`

## Step 5: Monitor CI/CD Pipeline

After pushing tag:

1. Go to Actions: https://github.com/CrystalArchitect/teraaustralis-incognita/actions
2. Look for "Publish Packages to PyPI" workflow
3. Watch for:
   - ✅ Build phase (creates wheel + sdist)
   - ✅ Check phase (validates distribution)
   - ✅ Publish phase (uploads to PyPI)

Example workflow run:
```
publish-packages / publish (matrix)
├── Set up Python 3.10
├── Install build tools
├── Build package
├── Check distribution
└── Publish to PyPI ✓
```

## Step 6: Verify on PyPI

After workflow succeeds:

1. Check PyPI package page:
   - https://pypi.org/project/teraaustralis-clementine/
   - https://pypi.org/project/teraaustralis-rdp/
   - etc.

2. Verify package details:
   - Version: 1.0.0
   - License: AGPL-3.0 (or correct license)
   - Description: Correct
   - Files: .tar.gz and .whl present

3. Install from PyPI to verify:
```bash
pip install teraaustralis-clementine
python -c "from teraaustralis.clementine.crystalcore import Clementine; print('✓ Clementine installed from PyPI')"
```

## Step 7: Announce Release

### Update Project Status

1. Update root README.md:
```markdown
## Packages on PyPI

All packages are now available on PyPI:

- **Clementine** — [`teraaustralis-clementine`](https://pypi.org/project/teraaustralis-clementine/) (AGPL v3)
- **RDP** — [`teraaustralis-rdp`](https://pypi.org/project/teraaustralis-rdp/) (AGPL v3)
- ...
```

2. Create GitHub Release:
```bash
gh release create v1.0.0 \
  --title "TeraAustralis 1.0.0 - First Production Release" \
  --notes "All 7 packages now available on PyPI. See PUBLISHING.md for details."
```

3. Social Media Announcement (template):
```
🎉 TeraAustralis 1.0.0 is live on PyPI!

7 production-ready packages for multi-AI coordination:
- Clementine: Local-first AI companion
- RDP: Decision kernel & reasoning
- Consent Transport: Privacy-respecting data exchange
- CrystalBridge: Enterprise safety gateway
- Starline: Multi-AI message bus
- CrystalCore-EI: Emotion intelligence + uncertainty
- Mythos: Universe lore & narrative

Get started: pip install teraaustralis-clementine
Docs: https://teraaustralis.dev

#OpenSource #Python #AI #MultiAI
```

## Troubleshooting

### CI/CD Workflow Fails

**Error: "Authentication Failed"**
- Verify PYPI_API_TOKEN secret is set correctly
- Check token hasn't expired
- Try regenerating token

**Error: "This project already exists on PyPI"**
- Verify package names are correct (check pyproject.toml)
- Check spelling matches exactly
- May need to wait if name was recently deleted

**Error: "Invalid dist files"**
- Check `twine check dist/*` passes locally
- Verify pyproject.toml syntax is valid
- Ensure all files in dist/ are present

### Local Build Issues

**Error: "package directory doesn't exist"**
```bash
# Fix: Check setuptools.packages in pyproject.toml
# Should be: packages = ["teraaustralis.{package}"]
# Not: packages = ["teraaustralis.{shortname}"]
```

**Error: "importError when building"**
```bash
# Fix: Missing dependencies
cd packages/{package}
pip install -e . -q
cd ../..
```

## Post-Release Checklist

- [ ] All packages published to PyPI successfully
- [ ] PyPI package pages display correctly
- [ ] Installation works: `pip install teraaustralis-clementine`
- [ ] README and docs updated with PyPI links
- [ ] GitHub Releases created
- [ ] Social media announcement posted
- [ ] Support emails configured and tested
- [ ] Commercial licensing portal live (if applicable)
- [ ] First customer/license acquired
- [ ] Monitor PyPI statistics daily for first week

## Future Releases

For version 1.0.1+ releases, repeat this process:

1. Update version in package pyproject.toml
2. Update CHANGELOG.md
3. Commit version bump
4. Create git tag
5. Push tag to trigger CI/CD
6. Announce release

**Tag Format Reminder:**
- All packages: `git tag v1.0.1`
- Single package: `git tag clementine-v1.0.1`

## Support

- CI/CD Issues: Check GitHub Actions logs
- PyPI Issues: See https://pypi.org/help/
- Token Issues: Regenerate at https://pypi.org/manage/account/tokens/
- Package Issues: Check pyproject.toml syntax and dependencies

---

**You are here:** Ready to push first tags ✨

**Next:** `git tag -a clementine-v1.0.0 -m "Clementine 1.0.0 release" && git push origin clementine-v1.0.0`
