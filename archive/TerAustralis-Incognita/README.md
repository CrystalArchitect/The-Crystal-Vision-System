# TerAustralis Incognita

**Collective intelligence with individual sovereignty.**

This repository is the **umbrella**: governance, architecture, the mythos, research, and the archive. The working software lives in sibling repositories, chiefly **[`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)**.

> **System map:** see the **[Crystal Architecture Archive](https://github.com/CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive/blob/main/knowledge-base/00-INDEX.md)** — a single source of truth for the whole constellation, which repos hold which pieces, and the runnable state of each. This umbrella repo contains canon, ADRs, and vision; the Archive ledger answers "what's running, what's built but dormant, and what's designed only."

## What you can run right now

Two things execute from this repository alone (stdlib-only, no dependencies):

```bash
# CrystalCore.OS — the mythos as a terminal you can fly
python3 mythos/crystalcore-os/crystalcore_os.py

# Story Library prototype — self-contained HTML
# (open in a browser, e.g. from research/prototypes/story-library/)
```

**Everything else** — Clementine, the Starline Weaver, Consent Transport, RDP, CrystalBridge — lives in **[`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)** with its own quick start, tests, and security spec.

## What's in this repository

| Folder | What it is | Status |
|---|---|---|
| `docs/` | ADRs, governance stack, architecture canon | Built (docs) |
| `mythos/` | Content, art, the Codex, the Apocryphon, Starline Transmissions, CrystalCore.OS terminal | Vision (narrative + runnable shell) |
| `research/` | Exploratory work, Story Library prototype, Seven Sisters cycle | Built (prototype only) |
| `archive/` | Legacy code, provenance only — do not build on | Built (superseded) |

**The Incognita Rule** (governing principle): we mark which lines are surveyed (code that runs and tests pass) and which are dreamed (story, vision, design). They are kept honestly separate — see [`The-Incognita-Rule.md`](docs/governance/The-Incognita-Rule.md).

## The working system

See the **[CrystalCore.OS Architecture Archive](https://github.com/CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive)** for:
- A ledger of what's Running, Built-not-running, Documented, Designed, or Concept-only
- Wire protocols (Starline Weaver, Consent Transport, RDP)
- Security specs for the consent gate and message bus
- Quick start commands that actually work (they're in the code repo)

For this repository's governance, roadmap, and decisions, see:
- **[Roadmap](docs/governance/Roadmap.md)** — what's in progress or blocked
- **[ADRs](docs/adr/)** — why architecture choices were made
- **[Project Boundaries](docs/governance/Project-Boundaries.md)** and **[Migration Plan](docs/governance/Migration-Plan.md)** — how the repos are split

## Repository structure

**In this repo:**

| Path | What it is |
|---|---|
| `docs/` | ADRs, governance, architecture canon, guides, contributing rules |
| `mythos/` | Crystal universe canon (Codex, Apocryphon, Starline Transmissions, 88 pieces of art), CrystalCore.OS terminal, outer-world lore |
| `research/` | Exploratory work: Story Library prototype, Seven Sisters cycle, research notes |
| `archive/` | Legacy code (crystalcore-v0.13, local-snapshot-2026-07-17) — frozen for provenance |
| `dbt/` | The emotion-warehouse dbt project (not executed; see [`docs/DBT_WAREHOUSE_INTEGRATION.md`](docs/DBT_WAREHOUSE_INTEGRATION.md)) |

**In [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)** (the actual running system):

| Component | What it is |
|---|---|
| Clementine | Local-first AI companion (Ollama-backed, JSON memory, Flask + Svelte UI) |
| Starline Weaver | Multi-AI message bus with Belt-Three consent law enforced in code |
| Consent Transport | Peer-to-peer sovereign memory exchange (Noise Protocol + ML-KEM-768 spec) |
| RDP | Tamper-evident record kernel + decision ledger |
| CrystalBridge | MCP consent gate (fail-closed by design) |
| SvelteKit site | Production website deployed to teraustralis.com.au |
| Client SDK | TypeScript/Node.js bindings |

**Why `mythos/` sits at the top level instead of under `docs/`:** code and
content are administratively separate license areas — `LICENSE-CONTENT.md`
for `mythos/`, `LICENSE` for everything else — even though both currently
carry the same CC BY-NC-ND 4.0 terms ([`ADR-0008`](docs/adr/ADR-0008.md)).
Folding canon into `docs/` would blur that boundary. Keeping it a peer of
`src/` and `docs/` makes the split visible from the directory listing alone,
with no need to open a file to find out which rule applies. Full reasoning:
[`ADR-0002`](docs/adr/ADR-0002.md).

## The Covenant

Clementine's core rules are written in [`mythos/COVENANT.md`](mythos/COVENANT.md): no influence without explicit direction, an absolute and instant pause, memory that belongs entirely to the human, support that's offered rather than imposed, and restraint as its own form of respect. Consent Transport applies the same law to data instead of conversation — nothing moves without a grant, and revocation takes effect on the very next request. See the **[Code repo's SECURITY.md](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code/blob/main/core/crystal-core/SECURITY.md)** for implementation detail.

## Mythos

Start with [`mythos/content/THE-SOVEREIGN-KEY.md`](mythos/content/THE-SOVEREIGN-KEY.md)
and [`mythos/content/STARLINE-TRANSMISSIONS.md`](mythos/content/STARLINE-TRANSMISSIONS.md).
The full visual canon is in [`mythos/art/`](mythos/art/README.md).

## AI collaboration

Several AI tools work on this repository under defined roles — the model is
documented in [`docs/ai/`](docs/ai/AI-Workflow.md), the rules in
[`docs/governance/AI-Governance.md`](docs/governance/AI-Governance.md), and
every PR names the tools that helped produce it.

## How to contribute

**In this repository:**
- **Docs** — architecture notes, governance clarity, guides for the system as a whole
- **Mythos** — the Codex, the Apocryphon, the Starline Transmissions, visual art, outer-world lore
- **Design** — diagrams, interface concepts, visual storytelling

**In [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code):**
- **Code** — Clementine, the Starline Weaver, Consent Transport, RDP, CrystalBridge: features, fixes, tests
- **Architecture** — protocol design, security review, benchmarking

## Contributing, security, license

- **Contributing:** [`CONTRIBUTING.md`](CONTRIBUTING.md) — branch rules, the
  Belt-Three truth labels, and what never gets committed (generated files,
  personal memory data, secrets). Command quick-reference:
  [`docs/guides/GitHub-Commit-Instructions.md`](docs/guides/GitHub-Commit-Instructions.md).
- **Security:** [`SECURITY.md`](SECURITY.md) for this repo overall;
  [`core/crystal-core/SECURITY.md`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code/blob/main/core/crystal-core/SECURITY.md)
  (now in `TerAustralis-Incognita-Code`, per `ADR-0011`) for the protocol
  pack's specific guarantees (Starline Weaver, pipeline quarantine, Starline's
  consent gating).
- **License:** Everything in this repository — `src/`, `packages/`, and
  mythos content (lore, art, the Codex, the Apocryphon) alike — is
  uniformly **CC BY-NC-ND 4.0** (`LICENSE`, `LICENSE-CONTENT.md`): share
  with credit, no commercial use, no derivatives; commercial licensing by
  negotiation — see [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md). A
  differentiated per-package model (AGPL v3 / Proprietary / Dual /
  CC BY-NC-ND) was implemented in `packages/` and then deliberately
  reverted in favour of this uniform, simpler license — see
  [`ADR-0010`](docs/adr/ADR-0010.md).
- **Roadmap:** [`Roadmap.md`](docs/governance/Roadmap.md) — what's built,
  what's in progress, and what hasn't started yet.
- **Changelog:** [`CHANGELOG.md`](CHANGELOG.md) — repository milestones.
- **Code of conduct:** [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — expected
  behavior and how to report a problem.

## Links

- **Website:** [teraustralis.com.au](https://www.teraustralis.com.au)
- **Music:** [Suno](https://suno.com/@m13crystalat)
- **Support:** [Patreon](https://patreon.com/CrystalCore91)
- **Contact:** [@M13CrystalAT on X](https://x.com/m13crystalat)

---

*Non Solus.*
