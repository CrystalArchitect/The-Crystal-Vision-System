# Modules

Per-component inventory: what it is, its status, and the command that proves
it. Status labels follow [`Roadmap.md`](../governance/Roadmap.md) — if this
table and the roadmap ever disagree, the roadmap wins and this table has a
bug.

> **Repository status:** the paths and "Prove it" commands below refer to
> the code tree, which is not in this repository — they are not runnable
> from a fresh clone. See
> [SystemMap: where the code actually lives](SystemMap.md#where-the-code-actually-lives).

| Module | Path | What it is | Status | Prove it |
|---|---|---|---|---|
| Clementine | `vision/apps/clementine/` | Local-first companion: terminal, Flask API, Svelte webapp, layered memory | Working prototype | `python -m pytest vision/apps/clementine/tests -q` |
| Starline Weaver | `src/crystal-core/bus/` | Multi-AI bus, Belt-Three law in code, matrix mode | v0, self-tested | `cd src/crystal-core && python3 -m bus.selftest` |
| Pipeline | `src/crystal-core/services/` | Decode → Ingest → Twin over SQLite, quarantine with reasons | v0, self-tested | `cd src/crystal-core && python3 -m services.selftest` |
| Starline | `src/crystal-core/consent_transport/` | P2P consent-gated memory exchange, Noise handshake | Running, self-tested | `cd src/crystal-core && python3 -m consent_transport.selftest` |
| RDP | `src/crystal-core/rdp/` | Tamper-evident record chain + explainable decision kernel | Running, self-tested | `cd src/crystal-core && python3 -m rdp.selftest` |
| CrystalBridge | `src/crystalcore/` | Fail-closed MCP consent gate, append-only audit | Built (reconstructed spec) | `python -m compileall -q src/crystalcore` + gate checks exercised via guests |
| Mythos terminal | `src/crystalcore-os/` | The Crystal universe as a playable terminal — Vision-layer code | Runs (a story, not infrastructure) | `python3 src/crystalcore-os/crystalcore_os.py` |
| Mesh stub | `src/node/mesh/` | In-process, libp2p-shaped transport stub | Stub only — no real networking | `python -m pytest tests -q` |
| TS SDK | `src/sdk/typescript/` | Client scaffold for a local agent API | Scaffold, no consumer | — |
| Site | `src/site/` | SvelteKit site for teraustralis.com.au | Deployed via Pages | `cd src/site && npm install && npm run build` |
| Demo shells | `src/apps/crystal-interface/`, `src/apps/vision-web/` | Interface concepts on simulated data, Authority HOLD | Demos, not production | open `index.html` |
| Voicebox | `src/apps/voicebox/` | Local MCP server that speaks text aloud | Utility | run per its README |

Component docs live in [`crystal-core/`](crystal-core/) (specs for the
Weaver, Starline, RDP integration, the blueprint) — moved out of the source
tree per the "docs are not code" rule, with pointers left in each module's
README.
