# GitHub Commit Instructions

A short quick-reference for getting a change committed cleanly. The full rules
live in [`CONTRIBUTING.md`](../../CONTRIBUTING.md) — read that first; this page
just collects the commands.

> **Status (2026-08-20):** this repository is the umbrella — docs, ADRs,
> mythos. There is no `src/` here. The GitHub slug is
> `CrystalArchitect/TerAustralis-Incognita` (one *a*). Python self-tests
> belong in
> [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code).
> CI on this repository is markdown lint and link check, not the Python
> suites below.

## One-time setup

```bash
git clone https://github.com/CrystalArchitect/TerAustralis-Incognita.git
cd TerAustralis-Incognita
```

## Before you push: run the checks CI runs

CI (`.github/workflows/ci.yml`) runs on every push and pull request, and its
"Python syntax + self-tests" job must pass. Run the same checks locally first —
either with one command:

```bash
scripts/maintenance/check.sh
```

or step by step:

```bash
# Python syntax across the source tree
python -m compileall -q src tests archive

# Self-tests (from src/crystal-core/)
cd src/crystal-core
python -m bus.selftest      # Starline Weaver
python -m services.selftest               # Decode → Ingest → Twin pipeline
pip install -r requirements-consenttransport.txt
python -m consent_transport.selftest               # Starline
python -m rdp.selftest                    # RDP record kernel
cd ../..

# Test suites
python -m pytest vision/apps/clementine/tests -q
python -m pytest tests -q
```

If you changed the website, build it too:

```bash
cd src/site && npm install && npm run build && cd ../..
```

## Commit and open a PR

Direct pushes to `main` are the maintainer's; everyone else works on a branch
and opens a pull request (see [`CONTRIBUTING.md`](../../CONTRIBUTING.md)):

```bash
git checkout -b your-feature-branch
git add path/to/changed/files          # stage specifically, not `git add -A`
git commit -m "Clear, present-tense summary of the change"
git push -u origin your-feature-branch
```

Then open a pull request against `main` on GitHub. CI runs automatically — get
it green before merging.

## Never commit

Enforced by `.gitignore`, but worth knowing (the full list is in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md)):

- **Generated output** — `.svelte-kit/`, `src/site/build/`, `dist/`,
  `node_modules/`, `__pycache__/`
- **Personal data** — Clementine memory and profiles, Starline identity/keys,
  CrystalBridge audit logs
- **Secrets** — API keys, `.env` files

*Non Solus.*
