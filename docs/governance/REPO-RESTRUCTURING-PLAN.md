# TeraAustralis Repository Restructuring Plan

> **Status note (2026-07-28).** This plan proposes the `packages/` split.
> That split was **not adopted**: [`ADR-0010`](../adr/ADR-0010.md) chose
> uniform CC BY-NC-ND 4.0 over differentiated per-package licensing, and
> [`ADR-0011`](../adr/ADR-0011.md) adopted the three-repository boundary
> model instead. No `packages/` tree exists in this repository. References
> to it below are shown as plain paths rather than links, because there is
> nothing to link to. Kept for provenance.

> **Superseded (2026-07-23).** This plan's `packages/` split was reverted
> by [`ADR-0010`](../adr/ADR-0010.md) and its layout never landed in this
> repository's git history; its "Apache-2.0 for everything" premise never
> matched the actual `LICENSE`. The operative restructuring proposal is
> now [`Migration-Plan.md`](Migration-Plan.md) under
> [`ADR-0011`](../adr/ADR-0011.md). Kept as reference.

**Splitting seven products into independent, cleanly-imported packages.**

---

## Current State (Problems)

```
teraaustralis-incognita/
├── src/
│   ├── apps/clementine/                    # Product 1
│   ├── crystal-core/
│   │   ├── clementine/                 # Product 2 (Starline)
│   │   ├── consent_transport/          # Product 3 (Consent)
│   │   ├── rdp/                        # Product 4 (RDP)
│   │   └── starline/
│   ├── crystalcore/                    # Product 5 (CrystalBridge)
│   ├── crystalcore-os/                 # Product 6 (EI)
│   └── ...
├── mythos/                             # Product 7 (Story/Art)
├── docs/
├── LICENSE                             # ⚠️ Apache-2.0 for everything!
└── README.md
```

**Problems:**
- ❌ All products under single Apache-2.0 license
- ❌ Unclear which code belongs to which product
- ❌ Hard to release packages independently
- ❌ Circular dependencies between products
- ❌ Single monolithic version number
- ❌ Can't have different licensing per product

---

## Target State (Organized)

```
teraaustralis-incognita/                    # Main monorepo (umbrella)
├── packages/
│   ├── clementine/                            # Package 1: Companion
│   │   ├── teraaustralis/clementine/
│   │   ├── LICENSE.md                     # AGPL v3
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── starline/                          # Package 2: Message Bus
│   │   ├── teraaustralis/starline/
│   │   ├── LICENSE.md                     # AGPL v3
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── consent-transport/                 # Package 3: P2P Memory
│   │   ├── teraaustralis/consent/
│   │   ├── LICENSE.md                     # AGPL v3
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── rdp/                               # Package 4: Record Kernel
│   │   ├── teraaustralis/rdp/
│   │   ├── LICENSE.md                     # AGPL v3
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── crystalbridge/                     # Package 5: Consent Gate
│   │   ├── teraaustralis/bridge/
│   │   ├── LICENSE.md                     # PROPRIETARY
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   ├── crystalcore-ei/                    # Package 6: Emotion Intelligence
│   │   ├── teraaustralis/ei/
│   │   ├── LICENSE.md                     # Dual (MIT + Commercial)
│   │   ├── COMMERCIAL_LICENSE.md
│   │   ├── setup.py
│   │   └── pyproject.toml
│   │
│   └── mythos/                            # Package 7: Story/Art
│       ├── teraaustralis/mythos/
│       ├── LICENSE.md                     # CC BY-NC-ND
│       └── pyproject.toml
│
├── scripts/                               # Helper scripts
│   ├── install-all.sh                     # Install all packages in dev mode
│   └── publish-all.sh                     # Publish to PyPI
│
├── docs/
├── .github/                               # GitHub Actions for each package
│   └── workflows/
│       ├── package-clementine.yml
│       ├── package-starline.yml
│       └── ...
│
├── README.md                              # Points to individual packages
├── LICENSE.md                             # Umbrella (explains package licenses)
└── pyproject.toml                         # Monorepo config (poetry, uv)
```

---

## Phase-by-Phase Breakdown

### PHASE 1: Prepare Structure (Week 1)

#### Step 1.1: Create package directories
```bash
mkdir -p packages/{clementine,starline,consent-transport,rdp,crystalbridge,crystalcore-ei,mythos}
mkdir -p packages/clementine/teraaustralis/clementine
mkdir -p packages/starline/teraaustralis/starline
# ... etc for all packages
```

#### Step 1.2: Create package configuration files

**`packages/clementine/pyproject.toml`:**
```toml
[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "teraaustralis-clementine"
version = "1.0.0"
description = "Local-first sovereign AI companion"
readme = "README.md"
license = {text = "AGPL-3.0-or-later"}
authors = [{name = "CrystalArchitect"}]
requires-python = ">=3.10"
dependencies = [
    "flask>=2.0",
    "ollama>=0.1",
    # ...
]

[project.scripts]
clementine = "teraaustralis.clementine:main"

[project.urls]
repository = "https://github.com/CrystalArchitect/teraaustralis-clementine"
documentation = "https://teraaustralis.dev/clementine"
```

**`packages/clementine/setup.py`:**
```python
from setuptools import setup, find_packages

setup(
    name="teraaustralis-clementine",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "teraaustralis.clementine": ["templates/*", "static/*"],
    },
)
```

**`packages/clementine/LICENSE.md`:**
```
AGPL-3.0-or-later License

[Full AGPL v3 text here]
```

**`packages/clementine/README.md`:**
```markdown
# Clementine – The Sovereign Companion

Local-first AI companion with consent-driven memory.

## License
AGPL v3 – See LICENSE.md

## Installation
pip install teraaustralis-clementine

## Contributing
See CONTRIBUTING.md
```

#### Step 1.3: Create top-level umbrella README

**`README.md` (updated):**
```markdown
# TeraAustralis Incognita

Collective intelligence with individual sovereignty.

## 📦 Products (Separately Licensed)

| Package | License | Purpose |
|---------|---------|---------|
| `packages/clementine` | AGPL v3 | Sovereign AI companion |
| `packages/starline` | AGPL v3 | Multi-AI message bus |
| `packages/consent-transport` | AGPL v3 | P2P sovereign memory |
| `packages/rdp` | AGPL v3 | Record kernel & decisions |
| `packages/crystalbridge` | Proprietary | AI safety consent gate |
| `packages/crystalcore-ei` | Dual (MIT + Commercial) | Emotion intelligence |
| `packages/mythos` | CC BY-NC-ND | Story, art, canon |

## 🚀 Quick Start

Install all packages:
```bash
pip install -e packages/clementine
pip install -e packages/starline
# ... or use install-all.sh
```

## 📚 Documentation

- [Licensing Strategy](LICENSING-STRATEGY.md)
- [Repo Restructuring](REPO-RESTRUCTURING-PLAN.md)
- `packages/`
```

---

### PHASE 2: Move Code (Week 2-3)

#### Step 2.1: Move Clementine
```bash
# Current: vision/apps/clementine/
# Target: packages/clementine/teraaustralis/clementine/

cp -r vision/apps/clementine/* packages/clementine/teraaustralis/clementine/
```

**Create `packages/clementine/teraaustralis/__init__.py`:**
```python
# Namespace package marker
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
```

#### Step 2.2: Move Starline
```bash
# Current: src/crystal-core/clementine/ + src/crystal-core/starline/
# Target: packages/starline/teraaustralis/starline/

cp -r src/crystal-core/clementine/* packages/starline/teraaustralis/starline/
cp -r src/crystal-core/starline/* packages/starline/teraaustralis/starline/
```

#### Step 2.3: Move Consent Transport
```bash
# Current: src/crystal-core/consent_transport/
# Target: packages/consent-transport/teraaustralis/consent/

cp -r src/crystal-core/consent_transport/* packages/consent-transport/teraaustralis/consent/
```

#### Step 2.4: Move RDP
```bash
# Current: src/crystal-core/rdp/
# Target: packages/rdp/teraaustralis/rdp/

cp -r src/crystal-core/rdp/* packages/rdp/teraaustralis/rdp/
```

#### Step 2.5: Move CrystalBridge
```bash
# Current: src/crystalcore/
# Target: packages/crystalbridge/teraaustralis/bridge/

cp -r src/crystalcore/* packages/crystalbridge/teraaustralis/bridge/
```

#### Step 2.6: Move CrystalCore.OS EI
```bash
# Current: src/crystalcore-os/
# Target: packages/crystalcore-ei/teraaustralis/ei/

cp -r src/crystalcore-os/* packages/crystalcore-ei/teraaustralis/ei/
```

---

### PHASE 3: Fix Imports (Week 3-4)

#### Step 3.1: Update internal imports

**Before (old import path):**
```python
from src.crystalcore import CrystalCore
from src.crystal_core.clementine import Clementine
from src.crystal_core.consent_transport import ConsentTransport
```

**After (new import path):**
```python
# In Clementine
from teraaustralis.clementine import Clementine

# In Starline
from teraaustralis.starline import Starline
from teraaustralis.starline.clementine import Clementine

# In Consent Transport
from teraaustralis.consent import ConsentTransport
```

#### Step 3.2: Add cross-package dependencies

**When Clementine uses Starline:**

`packages/clementine/pyproject.toml`:
```toml
dependencies = [
    # ...
    "teraaustralis-starline>=1.0",  # Reference other package
]
```

**Install in dev mode:**
```bash
pip install -e packages/clementine
pip install -e packages/starline
# Clementine can now import from Starline
```

#### Step 3.3: Update package __init__.py files

**`packages/clementine/teraaustralis/clementine/__init__.py`:**
```python
from .clementine import Clementine
from .companion import Companion
from .api import create_app

__version__ = "1.0.0"
__all__ = ["Clementine", "Companion", "create_app"]
```

---

### PHASE 4: Testing & Documentation (Ongoing)

#### Step 4.1: Update CI/CD

**`.github/workflows/test-clementine.yml`:**
```yaml
name: Test Clementine
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install -e packages/clementine[dev]
      - run: pytest packages/clementine/tests/
```

#### Step 4.2: Add license headers to source files

**Every `.py` file in `packages/clementine/`:**
```python
"""
Clementine – The Sovereign Companion
Copyright (c) 2026 CrystalArchitect

Licensed under the GNU Affero General Public License v3.0 or later.
See LICENSE.md for details.

This module: [Brief description]
"""
```

#### Step 4.3: Individual package documentation

Each package gets:
- ✅ `README.md` (quick start, features, installation)
- ✅ `LICENSE.md` or `COMMERCIAL_LICENSE.md`
- ✅ `CONTRIBUTING.md` (how to contribute)
- ✅ `CHANGELOG.md` (version history)
- ✅ `docs/` folder (detailed guides)

---

## File Move Summary

| Product | Old Path | New Path | Size | License |
|---------|----------|----------|------|---------|
| Clementine | `vision/apps/clementine/` | `packages/clementine/teraaustralis/clementine/` | ~2MB | AGPL v3 |
| Starline | `src/crystal-core/clementine/` + `starline/` | `packages/starline/teraaustralis/starline/` | ~1.5MB | AGPL v3 |
| Consent | `src/crystal-core/consent_transport/` | `packages/consent-transport/teraaustralis/consent/` | ~800KB | AGPL v3 |
| RDP | `src/crystal-core/rdp/` | `packages/rdp/teraaustralis/rdp/` | ~600KB | AGPL v3 |
| CrystalBridge | `src/crystalcore/` | `packages/crystalbridge/teraaustralis/bridge/` | ~1MB | Proprietary |
| CrystalCore.OS EI | `src/crystalcore-os/` | `packages/crystalcore-ei/teraaustralis/ei/` | ~400KB | Dual (MIT + Commercial) |
| Mythos | `mythos/` | `packages/mythos/teraaustralis/mythos/` | ~5MB | CC BY-NC-ND |

**Total**: ~11MB → distributed across 7 independent packages

---

## Helper Scripts

### `scripts/install-all.sh`
```bash
#!/bin/bash
set -e

echo "Installing all TeraAustralis packages in dev mode..."

for package in packages/*/; do
    if [ -f "${package}pyproject.toml" ]; then
        echo "Installing $(basename $package)..."
        pip install -e "$package"
    fi
done

echo "✅ All packages installed!"
```

### `scripts/publish-all.sh`
```bash
#!/bin/bash
set -e

echo "Publishing all packages to PyPI..."

for package in packages/*/; do
    if [ -f "${package}pyproject.toml" ]; then
        echo "Publishing $(basename $package)..."
        cd "$package"
        python -m build
        python -m twine upload dist/*
        cd - > /dev/null
    fi
done

echo "✅ All packages published!"
```

---

## Dependency Graph

After restructuring, dependencies will be explicit:

```
clementine
  ├─→ starline (imports Clementine)
  ├─→ consent-transport (imports ConsentTransport)
  └─→ crystalcore-ei (imports EI for emotion detection)

starline
  (no dependencies on other packages)

consent-transport
  (no dependencies on other packages)

rdp
  (no dependencies on other packages)

crystalbridge
  (no dependencies - proprietary)

crystalcore-ei (EI)
  (no dependencies on other packages)

mythos
  (no dependencies - story/art)
```

---

## Timeline

| Phase | Weeks | Tasks | Owner |
|-------|-------|-------|-------|
| **Prepare** | 1 | Create structure, config files | You |
| **Move Code** | 2-3 | Copy code, organize files | Automated + Review |
| **Fix Imports** | 3-4 | Update all import paths, add dependencies | Automated + Review |
| **Test & CI** | 4 | Update tests, add GitHub Actions | CI/CD work |
| **Publish** | 4+ | Publish to PyPI, create separate repos (optional) | Release process |

**Total**: ~1 month for complete restructuring

---

## Rollback Plan

If restructuring causes issues:
1. Keep old `src/` structure in git (don't delete)
2. Create feature branch for restructuring
3. If problems arise, revert and try incremental approach
4. Once verified, delete old `src/` structure

---

## Success Criteria

✅ Each package installs independently via pip  
✅ Imports work: `from teraaustralis.clementine import Clementine`  
✅ Each package has own LICENSE.md  
✅ Each package has own version number  
✅ CI/CD tests pass for each package  
✅ Documentation is clear for each package  
✅ Dependency graph is clean (no circular deps)  
✅ Can publish each package to PyPI separately  

---

*TeraAustralis – Clean Architecture for Sustainable Innovation*
