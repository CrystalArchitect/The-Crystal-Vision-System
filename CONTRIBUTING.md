# Contributing to TerAustralis Incognita

Welcome. This is the canonical monorepo of the Crystal universe — the
narrative, the companion, the protocol, and the bridge all live here.
Contributions are welcome; here's what to know before you open a PR.

Before opening a PR, also read [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) —
short, and specific to how this project actually works. For the exact
clone / check / commit / push commands, see
[`docs/guides/GitHub-Commit-Instructions.md`](docs/guides/GitHub-Commit-Instructions.md);
the full review process is
[`docs/governance/Review-Process.md`](docs/governance/Review-Process.md).

## Ground rules

1. **Work on a branch, propose via pull request.** Direct pushes to `main`
   are reserved for the maintainer.
2. **Never commit generated files.** `.svelte-kit/`, `dist/`, `build/`,
   `node_modules/`, and `__pycache__/` are all ignored — if `git status`
   shows hundreds of files after running a dev server, stop and check
   `.gitignore` before staging.
3. **Never commit personal data.** Clementine's memory and profiles
   (`clementine_memory*`, `clementine_profiles/`) are the user's private
   property and must never enter git — the `.gitignore` enforces this;
   don't work around it.
4. **No secrets.** API keys live in environment variables only. `.env`
   files are ignored and stay that way.
5. **CI must pass.** This repository's own `ci.yml` checks markdown
   lint and links only — no Python runs here (Stage 2 of the migration
   retargeted CI to docs-only checks once `src/`/`tests/`/`scripts/`
   moved out; see
   [`docs/architecture/SystemMap.md`](docs/architecture/SystemMap.md#where-the-code-actually-lives)).
   Run the same checks locally first:
   ```bash
   npx markdownlint-cli2 "**/*.md" "#node_modules" "#archive"
   ```
   The Python syntax check, the crystal-core self-tests
   (`clementine.bridge.selftest`, `services.selftest`,
   `consent_transport.selftest`, `rdp.selftest`, `crystalcore.selftest`),
   and the pytest suites this note used to describe now run in
   [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)'s
   own `ci.yml` — that's where `core/` and `vision/` actually live.

## The Belt-Three law (labels)

Everything in this project carries one of three truth labels:

| Layer | Meaning |
|-------|---------|
| **Science** | Astronomy, hydrology, published geography, running code |
| **Story** | Dreaming / Songline narratives (honour; no restricted detail) |
| **Vision** | CrystalCore art, mythos, and protocol fiction |
| **Docs / governance / process** | ADRs, policy, review process, this file — not itself Science/Story/Vision content, but carries its own honesty obligation (a process doc can misdescribe reality same as any other claim) |

Added the fourth row 2026-07-24: `.github/PULL_REQUEST_TEMPLATE.md`
already carried it as a real, distinct checkbox — this table just
hadn't caught up. Keep them straight. Code claims must be true; mythos must be labeled as
mythos; no real-world coercion or fake hydrology, ever. Where real people
appear in Vision-layer content, it is storytelling only — no affiliation or
endorsement implied.

The *why* behind these labels — and the rest of the project's honesty
discipline — is written out in
[`The-Incognita-Rule.md`](docs/governance/The-Incognita-Rule.md):
mark which lines are dreamed and which are surveyed, and never let a dreamed line
pretend it was measured.

## Licensing — read before reusing content

This repo is dual-licensed:

- **Code & Specifications** (everything under `src/`, `docs/`, plus `tests/` and `scripts/`):
  **CC BY-NC-ND 4.0** — see `LICENSE`. Non-commercial use only; attribution required. 
  Commercial licensing available by negotiation with the copyright holder.
- **Content** (`mythos/` — the Crystal universe canon, the TerAustralis
  lore, the art): **CC BY-NC-ND 4.0** — see `LICENSE-CONTENT.md`. You may
  share it with credit; you may **not** remix it or use it commercially.
  Contributions to the mythos are accepted under the same terms.

**Note:** Architectural patterns referenced from MemClaw are credited under
Apache 2.0 terms (see `docs/ATTRIBUTIONS.md`). The *application* of those
patterns in CrystalCore OS is CC BY-NC-ND 4.0.

The reasoning behind this licensing — and the project's wider IP principles
(stewardship, attribution, identity, commercial future) — is recorded in
[`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

## Map of the repo

> **Repository status:** the `src/` paths below describe the code tree,
> which is not in this repository — see
> [SystemMap: where the code actually lives](docs/architecture/SystemMap.md#where-the-code-actually-lives).

The full map is [`docs/architecture/SystemMap.md`](docs/architecture/SystemMap.md);
the short version:

| Path | What it is |
|------|-----------|
| `vision/apps/clementine/` | The sovereign companion (CrystalCore framework, Flask API, Svelte webapp) |
| `src/apps/voicebox/` | Local MCP text-to-speech server |
| `src/apps/crystal-interface/`, `src/apps/vision-web/` | Demo shells (simulated data, Authority HOLD) |
| `src/crystal-core/` | Protocol pack — Starline Weaver, Decode→Ingest→Twin pipeline, Starline, RDP |
| `src/crystalcore/` | CrystalBridge MCP consent gate (fail-closed) |
| `src/site/` | SvelteKit site for teraustralis.com.au |
| `docs/` | Documentation — architecture, governance, AI collaboration, guides, ADRs |
| `research/` | Exploratory work — not production |
| `mythos/` | The canon — Codex, Apocryphon, Covenant, the Book of the Sovereign Key, art |
| `archive/` | Legacy copies kept for provenance — do not build on these |

See [`Roadmap.md`](docs/governance/Roadmap.md) for what's built, in
progress, or not yet started across these paths.

## AI-assisted contributions

AI tools are first-class contributors here, under rules:
[`docs/governance/AI-Governance.md`](docs/governance/AI-Governance.md).
The short version — every PR names the AI tools that helped produce it,
AI claims follow the same evidence rule as everyone else's, and the
maintainer keeps the veto.

## Attribution & intellectual property

### Cite external sources

When your contribution draws on external work (papers, articles, open-source projects, documented systems), cite the source:

1. **In your PR description:** Link to the source and explain what inspired your design.
2. **In the code:** Add a comment with a link to the source or paper.
3. **In this repo:** If the contribution is significant, propose an entry in [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

Example:
```python
# Registry pattern inspired by MemClaw's multi-agent governance
# See: https://github.com/caura-ai/caura-memclaw (Apache 2.0)
class Registry:
    ...
```

### Licensing & redistribution

CrystalCore OS is CC BY-NC-ND 4.0 (non-commercial). If you use or redistribute this work:

1. **Non-commercial use only.** CrystalCore OS code and specifications are for non-commercial use.
   Commercial use requires explicit permission from the copyright holder.
2. **Retain attribution.** ATTRIBUTIONS.md and copyright notices must stay in place.
3. **Do not modify and redistribute.** CC BY-NC-ND prohibits derivative redistribution; you may only
   share unmodified versions.
4. **Link back.** In your documentation or credits, link to the original CrystalCore OS repository.
5. **Never rebrand.** You cannot remove attribution or falsely claim original authorship.

**Commercial licensing:** If you want to use CrystalCore OS commercially, commercialize derivatives,
or commercialize products built on it, contact the copyright holder for a commercial license agreement.

**MemClaw attribution:** The architectural patterns referenced from MemClaw remain under Apache 2.0
(their license). Acknowledge MemClaw in any work you create; see [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

### Contribution licensing (why pull requests still work under a No-Derivatives license)

Read literally, "no derivative redistribution" (above) and "propose changes
via pull request" (`Ground rules` §1) pull in different directions — a PR
is a modification, and GitHub hosting it is a redistribution. This section
resolves that: **the outbound license (CC BY-NC-ND 4.0) governs what the
public can do with this repository; it does not govern what you grant the
project by contributing to it.**

By submitting a pull request, you grant the maintainer a perpetual,
worldwide license to use, modify, merge, and relicense your contribution as
part of this project — including under terms broader or different from
CC BY-NC-ND 4.0, such as a future commercial license. This is the standard
"inbound greater than or equal to outbound" structure many commercially
licensed projects use: contributors give the project room to work with
their change; the public redistribution terms stay exactly as strict as
`LICENSE` says. It does not change your attribution rights (`Cite external
sources`, above) or require you to give up authorship credit.

## The Covenant applies to code too

Clementine's Sovereignty Covenant (`mythos/COVENANT.md`) is not just
lore — it's the product spec. Changes to the companion must preserve:
local-first operation, opt-in cloud, absolute pause, full memory
ownership, and support that is offered, never imposed.

*Non Solus — Not Alone.*
