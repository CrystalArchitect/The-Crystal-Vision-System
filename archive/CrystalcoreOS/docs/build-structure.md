# CrystalCore — Build Structure (living document)

> **Living document.** This is the single-page map of what CrystalCore *is right now*:
> what's built, what's planned, where it lives, and how it's organised. Update it whenever
> the structure or status changes. Last updated: **2026-07-03**.
>
> **Repository:** `github.com/teraustralisincognita-svg/CrystalCore`
> CrystalCore is maintained as its own project, separate from
> [TerAustralis Incognita](https://github.com/teraustralisincognita-svg/TerAustralis-Incognita) (which it
> underpins) — kept apart deliberately to avoid confusing the two.

## What it is (one paragraph)

CrystalCore is a sovereign, local-first **edge AGI framework** designed to run fully offline
on constrained hardware (Raspberry Pi, older laptops, embedded systems). It is built around
three non-negotiable, mechanically enforced properties — **Consent** (fail-closed),
**Coherence**, and **Provenance** — and is engineered for real personal/family/advocacy use,
not as a cloud service or research toy.

## Status at a glance

| Item | State |
| --- | --- |
| Core layers (Memory · Flow · Evolve · Mind) | ✅ **Built**, integrated |
| CrystalSensor (external input, optional) | ✅ **Built**, integrated ([`SENSOR-LAYER-ARCHITECTURE.md`](./SENSOR-LAYER-ARCHITECTURE.md)) |
| CrystalLattice (relational substrate, air-gapped default) | ✅ **Built** v1 ([`LATTICE-ARCHITECTURE.md`](./LATTICE-ARCHITECTURE.md)); real transports planned |
| Test suite | ✅ **140 passing**, 0 failed (stdlib runner, zero required deps) |
| Property-based invariants | ✅ 7 properties under randomized inputs |
| End-to-end demos | ✅ 3 (`examples/`) |
| Standalone landing page | ✅ `index.html` |
| Wisdom Layer | 🟦 **Design only** — not implemented ([`wisdom-layer.md`](./wisdom-layer.md)) |
| CrystalAudit (decision logging/reports) | 🟦 Planned |
| Integration & deployment (CLI, web UI, Pi packaging) | 🟦 Planned |
| Self-replicating space probes | 🌌 Vision — not built |

## Directory structure

```
CrystalCore/                      (repo root — was crystalcore/ inside TerAustralis)
├── README.md                     canonical overview + per-layer reference
├── LICENSE                       AGPL-3.0
├── pyproject.toml                packaging metadata
├── run_tests.py                  stdlib-only test runner (no framework needed)
├── index.html                    self-contained framework landing page
├── .gitignore
│
├── src/                          ── the framework ──
│   ├── __init__.py
│   ├── crystal_memory.py         LAYER 1 · sparse, quantized, consent-aware substrate
│   ├── crystal_flow.py           LAYER 2 · autograd + inspectable symbolic reasoning
│   ├── crystal_evolve.py         LAYER 3 · population-based evolution of hybrid genomes
│   ├── crystal_mind.py           LAYER 4 · four non-autonomous reasoning stances
│   ├── crystal_sensor.py         external input abstraction (text/audio/env/device), optional
│   ├── crystal_lattice.py        relational substrate: consent-gated handoffs, air-gap default
│   └── policy_rules.py           substantive policy-drafting rules for CrystalMind
│
├── tests/                        ── 140 tests, stdlib only ──
│   ├── test_crystal_memory.py    33 tests
│   ├── test_crystal_flow.py      22 tests
│   ├── test_crystal_evolve.py    24 tests
│   ├── test_crystal_mind.py      17 tests
│   ├── test_crystal_sensor.py     9 tests
│   ├── test_crystal_lattice.py   13 tests
│   ├── test_policy_rules.py      15 tests
│   ├── test_properties.py         7 property-based invariants
│   └── property_harness.py       dependency-free Hypothesis fallback
│
├── examples/                     ── end-to-end demos ──
│   ├── family_decision_pipeline.py   "power of three" family decision (Memory→Evolve→Flow)
│   ├── policy_council.py             CrystalMind council drafting a position from evidence
│   └── example_sensor_to_action.py   CrystalSensor→Memory→Flow→Mind/Guardian→action
│
└── docs/                         ── design & living docs ──
    ├── build-structure.md        THIS FILE — the living map
    ├── wisdom-layer.md           planned Wisdom Layer design sketch
    ├── infrastructure.md         where it runs + training-burst topology
    ├── philosophy.md             worldview & principles
    ├── SENSOR-LAYER-ARCHITECTURE.md  CrystalSensor design + integration pattern
    └── LATTICE-ARCHITECTURE.md   CrystalLattice design: nodes, gates, LLM comms layer
```

## The six built layers

An auditable **reason → remember → improve** loop. Trust flows down to the substrate;
conclusions flow back up carrying provenance.

1. **CrystalMemory** (`src/crystal_memory.py`) — sparse, 8-bit-quantized tensors with
   coherence/consent/priority metadata, durable payloads, RAM-aware pruning, and atomic
   SHA-256-checksummed JSON persistence.
2. **CrystalFlow** (`src/crystal_flow.py`) — minimal scalar autograd + inspectable symbolic
   reasoning chains; **consent fail-closed**; coherence propagates as `min(inputs) × rule_strength`;
   provenance on every derived conclusion.
3. **CrystalEvolve** (`src/crystal_evolve.py`) — population-based training of hybrid genomes
   (numeric params + symbolic rule chains); closed rule registry; gated fitness; deterministic,
   seeded runs; Lamarckian + Baldwinian inheritance.
4. **CrystalMind** (`src/crystal_mind.py`) — four named, **non-autonomous** stances:
   **TruthSeeker** (high evidence bar), **Guardian** (safety reviewer with a veto),
   **Visionary** (explores; outputs marked speculative), **Creator** (synthesises artifacts).
   Agents act only when invoked — no loops, no self-invocation.
5. **CrystalSensor** (`src/crystal_sensor.py`, optional) — external input abstraction for
   text/audio/environment/device readings; processes the external world only, never brain
   data; each `SensorReading` carries confidence, consent, and provenance and flows into
   CrystalMemory → CrystalFlow → CrystalMind/Guardian through the same fail-closed machinery
   as everything else. See [`SENSOR-LAYER-ARCHITECTURE.md`](./SENSOR-LAYER-ARCHITECTURE.md).
6. **CrystalLattice** (`src/crystal_lattice.py`) — relational/connective substrate linking
   this core to other devices, humans (Sovereign Node Mesh), and external LLMs. Consent-gated
   `HandoffEnvelope`s (fail-closed, SHA-256 provenance-hashed), **air-gapped by default**
   (zero network code; external sends need `allow_external=True` + an injected transport),
   inbound replies coherence-capped as low-trust. The technical foundation of the
   ecosystem-wide Incognita Lattice. See [`LATTICE-ARCHITECTURE.md`](./LATTICE-ARCHITECTURE.md).

### Three properties flow through every layer
- **Consent** — a consumer sees only what its permissions allow; forbidden input → refuse, log, write nothing.
- **Coherence** — a conclusion is never more confident than its weakest input, and decays over time.
- **Provenance** — every derived item links back to its inputs and the rule that produced it.

## Planned layers (not built)

- **Wisdom Layer** — neutral, non-dogmatic knowledge atop CrystalMind (philosophy, emotional
  regulation, mythology, and consent-pending cultural knowledge), held as inspectable,
  provenance-tagged, consent-flagged sources — never hardcoded belief. See
  [`wisdom-layer.md`](./wisdom-layer.md).
- **CrystalAudit** — full decision logging and exportable reports.
- **Integration & deployment** — CLI, simple web UI, Raspberry Pi packaging.

## Where it runs

Live system runs **24/7 on a modest always-on Linux server** (core reasoning + memory,
fully local). Heavy training/evolution bursts to a separate GPU workstation or
Google Colab via API, returning an improved genome. Core reasoning/memory never leave the
server. Full detail + the sovereignty boundary: [`infrastructure.md`](./infrastructure.md).

## Why it's built this way

Wisdom-first and truth-anchored; consent/coherence/provenance as non-negotiables; sentience
treated as a possible *side effect*, not a goal; cultural/Indigenous content kept
**consent-pending** until custodian partnership exists; auditable foundation as the
precondition for any future BCI horizon. Full worldview: [`philosophy.md`](./philosophy.md).

## How to run

```bash
python3 run_tests.py        # 140 tests, stdlib only — expected: all passing
python3 examples/family_decision_pipeline.py
python3 examples/policy_council.py
python3 examples/example_sensor_to_action.py
```

## Roadmap (next)

1. **CrystalAudit** — exportable decision reports.
2. **Raspberry Pi packaging** — CLI + simple web UI; on-device RSS profiling.
3. **Wisdom Layer** — implement the design in [`wisdom-layer.md`](./wisdom-layer.md), starting
   with the curation/attribution process and the consent workflow for cultural content.

## Maintaining this document

Keep it honest and current:
- When a layer or doc is added/changed, update the **structure tree** and the **status table**.
- When tests change, update the **counts** (run `python3 run_tests.py` for the totals).
- Keep the **built vs planned** line crisp — never describe a planned thing as if it exists.
- Bump the **Last updated** date at the top.
