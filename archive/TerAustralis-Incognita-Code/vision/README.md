# Crystal Vision — the user-facing application

Per the boundary charter
([`Project-Boundaries.md`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/governance/Project-Boundaries.md),
[`ADR-0011`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/adr/ADR-0011.md)),
this area holds Crystal Vision: user-facing applications, interfaces, and the companion. Crystal Vision may depend on Crystal Core; Crystal Core never imports Crystal Vision.

| Path | Component |
|---|---|
| `apps/clementine/` | **Clementine** — the front-of-house voice of the sovereign AI companion, Ollama-backed (local-first, memory-aware, configurable LLM provider) · terminal, Flask API, Svelte webapp, browser voice · drives `crystalcore.mind` under `core/` · **being retired: the authoritative copy is [Clementine-ai-companion](https://github.com/CrystalArchitect/Clementine-ai-companion), whose companion passes every model call through a consent gate — this one does not** |
| `apps/voicebox/` | Voice layer HTTP server (TTS/STT interfaces) |
| `apps/crystal-interface/` | **Demo shell** — simulated data, Authority held (not production) |
| `apps/vision-web/` | **Demo shell** — simulated data, Authority held (not production) |
| `site/` | teraustralis.com.au — SvelteKit public frontend (prerendered, static hosting) |

## Prove it

```bash
# From the vision/apps/clementine-discord directory
cd vision/apps/clementine-discord
python -m pytest tests/
```

The embedded core suite (`tests/test_core.py`, 16 tests) passes in this
layout — memory/recall math, the condense boundary, JSON persistence with
corrupt-file safety, and profile isolation. It is the only test suite
present; integration, performance, and end-to-end coverage don't exist yet.

## The dependency rule

**Crystal Vision may depend on Crystal Core; Crystal Core never imports Crystal Vision.** Vision apps that need Core features import them explicitly (e.g., Clementine imports `crystalcore.mind`). Core services reach Vision data *by configured data path at runtime* — the bridge serves the companion without importing it.

---

Imported from the umbrella repository's branch
`claude/crystalcore-boot-visual-jau1bk` @ `32692fd` (Migration-Plan
Stage 1, PR 2 — user-facing app). Directory names preserved; `src/apps/` became `apps/` and `src/site/` became `site/`.
