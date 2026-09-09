# System map

The authoritative "where things live" for the CrystalCore OS v1.0 repository
architecture (adopted 2026-07-23, [`ADR-0001`](../adr/ADR-0001.md)).

## Where the code actually lives

**Repository status (2026-07-23), measured against git history:**

- **In this repository (git):** `docs/`, `mythos/`, `research/`, `dbt/`,
  `examples/`, `assets/`, `archive/`, `.github/`, and the root legal and
  entry-point files. That is the complete list.
- **Described below but not in this repository:** `src/`, `scripts/`, and
  `tests/` — and, referenced elsewhere in the docs, `packages/` and
  `corpus/`. None of these paths exist in this repository's git history on
  any branch (`git log --all -- src/` returns nothing). That tree lived in
  the maintainer's working copy on a laptop; a dated copy is preserved in
  `archive/2026/local-snapshot-2026-07-17/`.
- **Update (2026-07-23, maintainer's report):** the laptop is gone — no
  local working copy exists. The tree's current location is being
  re-established (leading candidate: the maintainer's DigitalOcean
  droplet); until it is found, the `archive/` snapshots are the only
  git-verified code, and they hold the earlier app era, not the
  post-reorg v1.0 components. The search-and-recovery procedure is
  [`Migration-Plan.md` Stage 1.0](../governance/Migration-Plan.md).
- **Consequences, corrected 2026-07-24:** this paragraph said the CI
  workflow (`ci.yml`) and the Pages deploy (`deploy.yml`) ran against
  absent `src/`/`tests/` paths and both failed, and that the root
  `CNAME` pointed Pages at an absent site. True when written (2026-07-23,
  13:47 UTC); resolved within hours by Stage 2 of
  [`Migration-Plan.md`](../governance/Migration-Plan.md) (same day):
  `ci.yml` here was retargeted to docs-only checks (markdownlint +
  external link check), and `deploy.yml` + `CNAME` moved to
  `TerAustralis-Incognita-Code`, where `vision/site/` actually lives —
  Pages source still needs a manual admin switch there, no API path to
  do it from a session. The two `packages/*` workflows named below were
  not left dormant either — Stage 2 removed them outright, after
  confirming neither had ever had a git tag to fire on. What's
  unchanged: commands quoted in this documentation (self-tests, demos,
  `scripts/maintenance/check.sh`) remain unrunnable from a fresh clone
  of this repository, because `src/` and `tests/` are still not here.

The tree below is retained as the description of that working tree and of
the intended layout — the layout decision (`ADR-0001`) is real; its
`src/` half was simply never pushed here. Entries marked ✱ are in that
described-but-not-present category.

Where each component belongs, and the staged plan for closing this gap:
[`Project-Boundaries.md`](../governance/Project-Boundaries.md) ·
[`Migration-Plan.md`](../governance/Migration-Plan.md)
([`ADR-0011`](../adr/ADR-0011.md)).

```
TerAustralis-Incognita/
│
├── README.md · LICENSE · LICENSE-CONTENT.md · NOTICE · CHANGELOG.md
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md · AGENTS.md
│
├── .github/            workflows (CI, Pages deploy), issue/PR/discussion
│                       templates, CODEOWNERS
│
├── docs/               documentation — never executable code
│   ├── vision/         why: mission, the CrystalCore name map, future,
│   │                   Southern Pillar strategy
│   ├── architecture/   how: overview, system map, modules, AI weave,
│   │                   Lattice; component specs under crystal-core/ and
│   │                   lattice/
│   ├── governance/     rules: Constitution, Incognita Rule, principles,
│   │                   review process, standards, roadmap
│   ├── ai/             which AI tools contribute and what each is for
│   ├── agents/         operating instructions per AI agent
│   ├── guides/         task how-tos (commit, push, guest access)
│   └── adr/            Architecture Decision Records
│
├── src/ ✱              executable code only
│   ├── apps/           clementine (companion) · voicebox (MCP TTS) ·
│   │                   crystal-interface + vision-web (demo shells)
│   ├── crystal-core/   protocol pack: bus (Starline Weaver) ·
│   │                   services (pipeline) · consent_transport (P2P
│   │                   exchange; `starline/` is a deprecated alias) ·
│   │                   rdp (record kernel) · interface, cli, index.html
│   ├── crystalcore/    CrystalBridge — the MCP consent gate
│   ├── crystalcore-os/ the mythos terminal (Vision-layer code)
│   ├── node/mesh/      in-process mesh stub (libp2p-shaped)
│   ├── sdk/typescript/ client SDK scaffold
│   ├── site/           SvelteKit site for teraustralis.com.au
│   └── profiles/       CrystalBridge profile configs (runtime data such as
│                       audit logs is gitignored)
│
├── research/           exploratory work — not production software
│   └── seven-sisters/  the seven-path Songline cycle: paths, water briefs,
│                       transmit records
│
├── mythos/             the Crystal universe canon — content, not code
│   ├── content/        Codex, Apocryphon, Sovereign Key, Transmissions…
│   ├── art/            the visual canon
│   ├── teraustralis/   outer-world lore + publish drafts
│   └── tools/          prompt tools (text, not software)
│
├── archive/            superseded material kept for provenance
│   ├── legacy/         crystalcore-app (pre-monorepo application)
│   └── 2026/           dated local snapshots
│
├── assets/             project-level branding/diagrams (see its README —
│                       mythos art is canon content and stays in mythos/)
│
├── dbt/                crystalcore_emotion_warehouse — the emotion-warehouse
│                       dbt project (docs/DBT_WAREHOUSE_INTEGRATION.md)
│
├── scripts/ ✱          developer utilities (check.sh mirrors CI)
│
├── tests/ ✱            repo-level test suites (unit/)
│                       component tests live beside their component
│                       (vision/apps/clementine/tests/, the crystal-core selftests)
│
└── examples/           runnable demos, curated (see its README)
```

✱ = described here, but not in this repository — see
["Where the code actually lives"](#where-the-code-actually-lives) above.

## Rules that keep the map honest

1. `src/` contains only executable code; documentation lives in `docs/`.
2. `research/` is not production; promotion into `src/` is a deliberate,
   reviewed act.
3. `archive/` is provenance — never build on it.
4. `mythos/` is Vision-layer content under its own license
   (`LICENSE-CONTENT.md`); it may point at code, never speak for it.
5. Structural changes to this map get an ADR
   ([`../governance/Decision-Records.md`](../governance/Decision-Records.md)).

Two deliberate deviations from a "pure" layout, recorded in
[`ADR-0003`](../adr/ADR-0003.md): `src/profiles/` holds CrystalBridge's
config because the code anchors to it by relative path, and component
READMEs / runtime data (bridge transcripts, sample events, RDP vectors) stay
beside their code.
