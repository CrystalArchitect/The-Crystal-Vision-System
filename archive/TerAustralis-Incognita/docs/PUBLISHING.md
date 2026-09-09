# Publishing Packages to PyPI

> **Scope note.** This guide describes the `packages/` layout and its
> per-package licensing (AGPL v3 / Proprietary / dual). That model was
> **not adopted** — [`ADR-0010`](adr/ADR-0010.md) chose uniform
> CC BY-NC-ND 4.0 for the whole repository, and
> [`ADR-0013`](adr/ADR-0013.md) extended it across the portfolio. The
> `packages/` tree it refers to does not exist here. Kept for provenance;
> read it as history, not as instructions.

> **Status note (2026-07-23):** the `packages/` structure this guide
> publishes from never landed in this repository's git history, and the
> per-package licensing it assumes was reverted by
> [`ADR-0010`](adr/ADR-0010.md). Kept for provenance. See
> [SystemMap: where the code actually lives](architecture/SystemMap.md#where-the-code-actually-lives).

This guide explains how to publish individual packages from the TeraAustralis repository to PyPI.

## Package List

| Package | Directory | PyPI Name | License |
|---------|-----------|-----------|---------|
| Clementine | `packages/clementine` | `teraaustralis-clementine` | AGPL-3.0 |
| RDP | `packages/rdp` | `teraaustralis-rdp` | AGPL-3.0 |
| Consent Transport | `packages/consent-transport` | `teraaustralis-consent` | AGPL-3.0 |
| CrystalBridge | `packages/crystalbridge` | `teraaustralis-bridge` | Proprietary |
| Starline | `packages/starline` | `teraaustralis-starline` | AGPL-3.0 |
| CrystalCore-EI | `packages/crystalcore-ei` | `teraaustralis-ei` | MIT or Proprietary |
| Mythos | `packages/mythos` | `teraaustralis-mythos` | CC-BY-NC-ND |

## Versioning Scheme

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

## Publishing Process

### Local Publishing (Development)

1. **Build the package:**
```bash
cd packages/{package-name}
python -m build
```

2. **Check distribution:**
```bash
twine check dist/*
```

3. **Test upload (optional):**
```bash
twine upload --repository testpypi dist/*
```

### Automated Publishing (via GitHub Actions)

The repository includes CI/CD workflows for automated publishing:

**Workflow:** `.github/workflows/publish-packages.yml`

#### Trigger by Git Tag

Push a version tag to trigger publishing:

```bash
# Single package release
git tag clementine-v1.1.0
git push origin clementine-v1.1.0

# All packages with same version
git tag v1.1.0
git push origin v1.1.0
```

**Tag Format:**
- `v{version}` — Triggers all packages
- `{package}-v{version}` — Triggers specific package
  - `clementine-v1.1.0`
  - `rdp-v1.2.0`
  - `consent-v1.0.5`
  - `bridge-v2.0.0`
  - `starline-v1.1.0`
  - `ei-v1.3.0`
  - `mythos-v1.0.0`

### Prerequisites for Automation

1. **PyPI API Token:**
   - Create token at https://pypi.org/manage/account/tokens/
   - Add to GitHub Secrets as `PYPI_API_TOKEN`

2. **Package Configuration:**
   - Each package must have `pyproject.toml` with correct metadata
   - Version must be specified in `pyproject.toml`
   - LICENSE.md must be present

## Manual Release Checklist

Before each release:

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md with release notes
- [ ] Run tests locally: `pytest packages/{package}/`
- [ ] Build and check: `python -m build && twine check dist/*`
- [ ] Commit version bump
- [ ] Create git tag: `git tag {package}-v{version}`
- [ ] Push tag: `git push origin {package}-v{version}`

## Managing Multiple Package Releases

### Release All Packages (Synchronized)

Use semantic versioning with `v{version}` tag:

```bash
# Version 1.2.0 for all packages
git tag v1.2.0
git push origin v1.2.0
```

### Release Individual Packages (Asynchronous)

Use package-specific tags:

```bash
# Release Clementine 1.1.0
git tag clementine-v1.1.0
git push origin clementine-v1.1.0

# Release RDP 1.2.0 (different version)
git tag rdp-v1.2.0
git push origin rdp-v1.2.0
```

## License Considerations

### AGPL v3 Packages (Clementine, Starline, Consent, RDP)

- **PyPI:** Published under AGPL-3.0
- **Commercial Use:** Available via commercial licensing
- **Link:** Contact starline-support@teraaustralis.dev

### CrystalBridge (Proprietary)

- **PyPI:** Not published (proprietary)
- **Access:** Only via licensed channels
- **Link:** Contact crystalbridge-sales@teraaustralis.dev

### CrystalCore-EI (Dual: MIT / Commercial)

- **PyPI:** Published under MIT (non-commercial use)
- **Commercial:** $5K–$25K+/year licensing
- **Link:** Contact ei-commercial@teraaustralis.dev

### Mythos (CC-BY-NC-ND)

- **PyPI:** Published under CC-BY-NC-ND-4.0
- **Fan Works:** Encouraged (see README)
- **Commercial:** Contact for licensing

## Troubleshooting

### Build Fails

```bash
# Clear build artifacts
rm -rf build/ dist/ *.egg-info

# Rebuild
python -m build
```

### TOML Parse Error

Check `pyproject.toml` syntax:
```bash
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

### Upload Fails

- Verify PyPI token is set: `echo $PYPI_API_TOKEN`
- Check package name doesn't conflict: https://pypi.org/project/{package-name}/
- Ensure version is new (no duplicates)

## CI/CD Status

Check automated workflows: https://github.com/CrystalArchitect/teraaustralis-incognita/actions

**Workflows:**
- `publish-packages.yml` — Triggered by version tags
- `test-packages.yml` — Runs on every PR/push

## Further Reading

- [Python Packaging Guide](https://packaging.python.org/)
- [twine Documentation](https://twine.readthedocs.io/)
- [PyPI Publishing Docs](https://pypi.org/help/#publishing)
- [The licence that actually governs this repository](../LICENSE) — CC BY-NC-ND 4.0
