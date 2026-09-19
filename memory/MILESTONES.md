# MILESTONES

Dated, landed work at the monorepo level. Newest first. Not a duplicate of
any subtree's own milestones (e.g. [`archive/TerAustralis-Incognita/memory/MILESTONES.md`](../archive/TerAustralis-Incognita/memory/MILESTONES.md)
tracks that project; this file tracks this repo).

**Write-back:** when monorepo-level work lands, add a dated entry here and,
if it changes "now," update the relevant row in [`INDEX.md`](INDEX.md).

## 2026-09-19 — Alive Weave: ConsentGate before bus speech

- `scripts/alive/bridge_gate.py` — real ConsentGate probes (allow / refuse).
- `pulse.py` CrystalBridge island now asserts gate law, not import-only.
- `weave.py` runs ConsentGate by default; meters `signal.gate_check` to twin.
- Twin selftest covers `signal.gate_check`.

## 2026-09-18 — Alive Weave: multi-AI islands pulsed and woven (S4)

- Hub map: [`00_MASTER_INDEX/ALIVE-WEAVE.md`](../00_MASTER_INDEX/ALIVE-WEAVE.md)
  (`CVS-ALIVE` in WORKING-INDEX). Canon: no.
- `scripts/alive/pulse.py` — inventories Built/custody/compose/docs islands;
  runs TCV bridge bus, Starline Weaver, Decode→Ingest→Twin selftests; imports
  CrystalBridge ConsentGate and SAT `wrap_turn` without requiring the MCP package.
- `scripts/alive/weave.py` — runs labeled-bus demo turns, meters delivered
  speech into twin as `signal.bus_message` (Architecture S4).
  Optional `--sat` gates the hub turn through SAT.
- Twin decode domain `signal` added in
  `archive/TheCrystalVision/services/decode.py` + selftest.
- **Law held:** connection ≠ merge; out-of-bounds titles stay out of bounds;
  ADR-0005 / LEAF human gate not auto-replaced.

## 2026-09-09 — Three-tier `/generate` designed and implemented (local + cloud)

- `archive/CrystalCore-OS/backend/app/core/llm.py`: added `generate_cloud()`
  (Anthropic API, lazy import, graceful `CloudNotConfiguredError` when no
  key), renamed the existing local-only function to `generate_local()`, and
  added a `generate(prompt, tier="auto"|"webllm"|"local"|"cloud")` cascade
  that tries local first and falls back to cloud only when local can't serve
  the request (not merely when it's slow).
- `app/schemas/generate.py`: request gained `tier`; response gained
  `tier_used` so callers can tell which tier actually answered.
- `app/api/v1/routes/admin.py`, `app/core/config.py` (`ANTHROPIC_API_KEY`,
  `CLOUD_LLM_MODEL`), `.env.example`, `requirements.txt` (`anthropic`)
  updated to match.
- Tests: `tests/test_llm.py` (new — cascade logic, all tiers mocked) and
  `tests/test_generate_api.py` (extended — route-level tier selection and
  503 paths). Not run against a live install in this session — this
  sandbox's network policy blocks PyPI, so the suite was verified with
  `python3 -m py_compile` only. Whoever picks this up next should run the
  real suite (`pytest`, from `backend/`) before trusting it further.
- Design doc: [`archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md`](../archive/CrystalCore-OS/docs/architecture/THREE-TIER-GENERATE.md) —
  full contract, sequence diagram, WebLLM reference client, and an explicit
  "what's not done here" section.
- **Label: Built** for local + cloud tiers and the cascade (code + mocked
  tests). **Vision** for the WebLLM tier (documented, no frontend consumes
  it) and for the cloud tier's live-call path (config-missing path tested,
  real API call not exercised — no network access this session).

## 2026-09-09 — Monorepo consolidation: 20 repositories imported

- 20 of 28 CrystalArchitect repositories imported into `archive/<name>/` via
  `git subtree add --squash`, each isolated, full file tree preserved. 4
  private repos excluded (auth unavailable in this session); 1 excluded per
  user request (fork, licensing). Full inventory:
  [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md).
- Merged to `main` via PR #1, commit `bcff64a`.
- Decision record: [`DECISIONS.md`](DECISIONS.md).
- **Label: Built** (files present and verifiable on disk — see
  `MONOREPO-INDEX.md`'s own verification commands).
