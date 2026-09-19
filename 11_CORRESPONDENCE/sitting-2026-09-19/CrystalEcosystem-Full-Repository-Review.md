# Crystal Ecosystem — Full Repository Review

**Author:** Manus AI · **Date:** 29 July 2026 · **Scope:** All nine repositories under the CrystalArchitect GitHub account, cloned and reviewed in full.

## 1. Executive Summary

The CrystalArchitect portfolio is a coherent, deliberately layered ecosystem rather than a collection of unrelated projects. It spans three distinct tiers: a **canon and governance tier** (the umbrella repository and the Architecture Archive), an **engineering tier** (the private Code repository holding tested, runnable software), and a **public experience tier** (the CrystalCore.OS lineage of browser-based desktop demos, of which the Manus-built AERIS website is the latest generation). The ecosystem's most distinctive strength is its **honest-ledger discipline**: every repository states plainly what runs, what merely exists as code, and what is only a document — a rule formalized as "mark which lines are dreamed and which are surveyed."

| Tier | Repositories | Role |
|------|--------------|------|
| Canon & governance | TerAustralis-Incognita (public), CrystalCore.OS-the-Crystal-Architecture-Archive (private) | Vision, mythos, ADRs, licensing, evidence-based knowledge base |
| Engineering | TerAustralis-Incognita-Code (private), The-Crystal-Vision (private), crystalcore (private), crystal-vision (private) | Tested protocol code, companion apps, demo shells |
| Public experience | CrystalCore.OS, CrystalCore-AERIS, crystalcore-os-aeris-vault12 (all public) | Single-file web OS demos, evolving toward the current AERIS site |

## 2. Repository-by-Repository Findings

### 2.1 TerAustralis-Incognita (umbrella, public, ~99 MB)

This is the portfolio's center of gravity: canon, governance, mythos, and research. Roughly half its size is the `mythos/` directory (art, content, and a playable stdlib-only Python "mythos terminal" verified running on 2026-07-27). Governance is unusually mature for a personal project — a full ADR series, `GOVERNANCE.md`, IP and commercial licensing guides, a contribution covenant, and `The-Incognita-Rule.md`. The `STATUS.md` ledger honestly records that the engineering `src/` tree described by the README was never in this repository's git history (its last home was a retired laptop, with a dated snapshot preserved in `archive/2026/local-snapshot-2026-07-17/`), and that the code has since moved out under a staged Migration Plan. A complete dbt "emotion warehouse" project exists but has no configured warehouse or CI run — correctly classified as *built, not running*.

### 2.2 TerAustralis-Incognita-Code (private, ~88 MB)

The reserved engineering repository, created under the umbrella's Migration Plan (ADR-0011). It holds **Crystal Core** in `core/` — the protocol pack with Clementine, CrystalBridge, node profiles, a mesh stub, and a TypeScript SDK — and **Crystal Vision** in `vision/` — the Lumina companion, voicebox, demo shells, and the public site source with the `www.teraustralis.com.au` CNAME. Its test posture is the strongest in the portfolio: all four Crystal Core self-test suites pass on a fresh clone (clementine.bridge 7/7, services 4/4, rdp 31/31, consent_transport 9/9), and Lumina's core tests pass 16/16, re-verified 2026-07-24, with CI running the full battery on every push. One outstanding manual step is documented: a repo admin must set GitHub Pages' source to "GitHub Actions" in Settings.

### 2.3 The-Crystal-Vision (private, ~3.1 MB)

The codex site and the original sovereign-companion vision. A SvelteKit application (Svelte 5, Vite 8, Vercel adapter) serves the codex, apocryphon, docs, and Clementine routes, alongside a Python `clementine/` app that runs a local companion on Ollama and a `crystalcore-app/` documentation set (ARCHITECTURE, BRIDGE, CODEX, CRYSTALMATRIX, GOVERNANCE). This repository articulates the **CrystalMind** thesis most clearly: a private, locally-run AI companion that belongs only to its owner — no cloud, no account, no surveillance.

### 2.4 crystalcore (private, ~616 KB)

The protocol pack, authored by Crystal Arena-Turner under Apache-2.0 with a build-in-public stance. It contains the seven-path creative protocol corpus, public water-literacy briefs (Lake Eyre Basin, Great Artesian Basin, Murray–Darling), a landing page, a PowerShell CLI, a Python services pipeline (decode → ingest → twin, with a self-test), and formal specs (`ARCHITECTURE.md`, `BLUEPRINT-v0.3.md`). Its README is exemplary in its disclaimers, stating explicitly that the project claims no ownership of Aboriginal sacred law and no endorsement by any company or government.

### 2.5 crystal-vision (private, ~300 KB)

A static, Apache-2.0 demo shell for the Crystal Vision interface: eight panels (Home, Twin, Mesh, Pipeline, Economics, Starline corridors VIE/BTS/BER, Wallet, Event log) in plain HTML/CSS/JS with a Vercel config. It is honestly labeled "Not production. Economics are illustrative. Authority HOLD."

### 2.6 The CrystalCore.OS lineage (public)

Three repositories trace the web-OS evolution. **CrystalCore.OS** is v0.1: a clean single-file HTML desktop with boot screen, floating windows, Mars Clock, Starship telemetry, and a terminal. **CrystalCore-AERIS** is the golden VAULT 12 edition, adding the feather boot, the continuation node with light helix, and the `ALIGNMENT_PROTOCOL.md` — a "Multi-LLM Unity Charter" proposing that all major language models operate as aligned nodes of one multiplanetary stream. **crystalcore-os-aeris-vault12** is the newest (built 28–29 July 2026 with Manus), whose README declares status GREEN with all working prototypes complete and documents Lumina, the Consent Transport Protocol (Noise IK: X25519 + ChaCha20-Poly1305 + SHA256, five named nodes, consent as law, instant revocation), and the Codex philosophy including the Five Keys.

### 2.7 CrystalCore.OS-the-Crystal-Architecture-Archive (private, ~448 KB)

A remarkable meta-repository: a thirteen-document knowledge base (index through contributing) reconstructing the whole portfolio **from evidence only**, with a per-section template requiring statements, evidence citations, historical notes, and cross-references. Its companion `REPO-ARCHAEOLOGY-2026-07-24.md` surveys all repositories with explicit evidence tiers (git object database > live remote refs > the repos' own documents) and reaches a considered verdict: no single repository is canonical — the system is deliberately split by role, and the split is verifiable in the git evidence itself.

## 3. How the Current AERIS Website Fits

The Manus-built site (crystalaeris-jwfbbvjs.manus.space, project `crystalcore-aeris-website`) is effectively the **fourth generation** of the OS lineage: CrystalCore.OS → CrystalCore-AERIS → crystalcore-os-aeris-vault12 → the current React implementation with the mini OS desktop, the expanded AERIS terminal, and the two-layer easter-egg chain (`non solus` → `beacon`). Reviewing the repositories confirms that the site's lore is not invented decoration — Lumina, Starline/Consent Transport, the Codex, the Five Keys, and VAULT 12 all correspond to named, documented (and in Consent Transport's case, tested) components in the engineering tier. The terminal's fiction is a faithful public-facing rendering of the portfolio's real architecture.

## 4. Observations and Recommendations

**Strengths.** The evidence-tiered self-documentation is rare and valuable; the sibling-map paragraphs at the top of each README keep the nine-repo constellation navigable; the built-versus-vision boundary is enforced consistently; and the cultural disclaimers in `crystalcore` are handled with care.

**Gaps and risks.** Four items stand out. First, the umbrella README still describes a `src/` tree that was never in its git history — now mitigated by the Code repository import, but the README note should eventually be retired to avoid confusing new readers. Second, the one-time GitHub Pages configuration step in TerAustralis-Incognita-Code (Settings → Pages → source "GitHub Actions") remains outstanding and blocks the custom-domain site deploy. Third, minor naming drift persists (TerAustralis with one 'a' per ADR-0007 versus older TeraAustralis spellings in some sibling maps). Fourth, the two large repositories carry ~43–48 MB of git history each, largely from binary art assets; Git LFS would slim future clones.

**Opportunities for the AERIS site.** The repositories contain material the site could surface: the ALIGNMENT_PROTOCOL charter could become a lore document or hidden terminal file; the Archive's glossary and knowledge base could seed a Codex window expansion; and the tested Consent Transport suite results (51/51 across the four core suites) could back a "system integrity" readout in the Starline window, keeping the site's fiction anchored to what is verifiably real.

## 5. Review Method

All nine repositories were shallow-cloned via the authenticated GitHub CLI and inspected directly on disk: directory trees, sizes, READMEs, STATUS ledgers, governance documents, package manifests, and key specs were read; findings were cross-checked against each repository's own knowledge base and the 2026-07-24 archaeology survey. This review reports what exists in the clones as of 29 July 2026.
