# CrystalCore.OS

**Sovereign Edge AGI Framework**
*Local-first, auditable intelligence for constrained hardware — built for truth, consent, and real deployment.*

> CrystalCore is the sovereign-edge foundation beneath the longer-horizon
> [TerAustralis Incognita](https://github.com/teraustralisincognita-svg/TerAustralis-Incognita) vision.
> It is being extracted into its own repository at
> `github.com/teraustralisincognita-svg/CrystalCore`. A self-contained landing page
> for the framework ships here as [`index.html`](./index.html) and is also served by
> the TerAustralis site at `/builders`.

## Vision

CrystalCore is a minimal, sovereign edge AGI framework designed to run reliably
on constrained devices such as Raspberry Pi, older laptops, and embedded
systems. It prioritises:

- Full offline operation, with no required external dependencies
- Radical auditability and provenance
- Consent and family ("power of three") protection as first-class concerns
- Truth/coherence anchoring over sanitised outputs
- Graceful degradation under tight RAM/storage constraints

It is **not** a research toy or cloud-scale system. It is engineered for
real-world personal, family, and advocacy use in low-connectivity or sovereign
environments.

## Core Principles

- **Sovereignty** — everything stays local; you control the data and reasoning.
- **Auditability** — every conclusion carries provenance, consent flags, and
  coherence metadata.
- **Consent-first** — reasoning fails closed on a forbidden input.
- **Edge realism** — designed for <300 MB RAM, microSD storage, and ARM CPUs.
- **Transparency** — no black-box behaviour; all components are inspectable.
- **Family focus** — built-in "power of three" protection and multi-user consent.
- **Determinism where it counts** — evolutionary runs reproduce from a seed.

## Architecture — four layers

CrystalCore is four composable layers. Each is independently useful; together
they form an auditable reason → remember → improve loop. Data and trust flow
downward to the substrate; conclusions flow back up with provenance.

```
   +--------------------------------------------------------------+
   |  CrystalMind     four named reasoning-policy agents           |
   |  (TruthSeeker, Guardian, Visionary, Creator; non-autonomous)  |
   +---------------+---------------------------+------------------+
                   | invokes (synchronous)     | conclusions (with provenance)
                   v                           ^
   +--------------------------------------------------------------+
   |  CrystalEvolve   population-based training of hybrid genomes  |
   |  (numeric params + symbolic rule chains; gated, seeded)       |
   +---------------+---------------------------+------------------+
                   | scores genomes via        | persists survivors
                   v                           v  (high priority)
   +--------------------------------------------------------------+
   |  CrystalFlow     autograd + inspectable symbolic reasoning    |
   |  (consent- & coherence-aware; provenance on every step)       |
   +---------------+---------------------------+------------------+
                   | reads facts (consent +    | writes conclusions
                   v  effective coherence)     v  (derived nodes)
   +--------------------------------------------------------------+
   |  CrystalMemory   sparse, quantized, consent-aware substrate   |
   |  (atomic + checksummed persistence; RAM-aware pruning)        |
   +--------------------------------------------------------------+
```

Three properties flow through all layers: **consent** (a consumer sees only what
its permissions allow), **coherence** (confidence propagates as `min(inputs) ×
rule_strength` and decays over time), and **provenance** (every derived item
links back to its inputs and the rule that produced it).

### 1. CrystalMemory (foundation)
- Hierarchical sparse tensors with 8-bit (configurable) quantization
- Coherence, provenance, consent flags, family priority, and temporal metadata
- Durable `payload` field (str/dict) for non-numeric content that survives reloads
- RAM-aware weighted pruning and graceful symbolic fallback
- Atomic JSON persistence with SHA-256 checksum validation and best-effort recovery

### 2. CrystalFlow (computation & reasoning)
- Minimal scalar autograd (`Value` nodes with a full backward pass)
- Symbolic first-principles reasoning chains
- Consent fail-closed enforcement; chains stop at the first denial
- Coherence propagation (`min(input coherences) × rule_strength`)
- Numeric<->symbolic bridge: rules may consume an evolved parameter vector
- Provenance tracking for every derived conclusion

### 3. CrystalEvolve (learning & optimisation)
- Population-based evolutionary training of hybrid genomes
- Closed rule registry for safe, inspectable symbolic mutation
- Gated fitness: symbolic validity is a hard pass/fail; valid genomes ranked by
  `squash(numeric_score) × symbolic_coherence`
- Lamarckian and Baldwinian inheritance modes (exploit vs. explore)
- Deterministic, seeded runs
- High family-priority survivor protection under pruning pressure

### 4. CrystalMind (agents)
- Four named reasoning policies: **TruthSeeker**, **Guardian**, **Visionary**,
  **Creator** — each a concrete stance (evidence bar + confidence factor), not a
  personality label
- **Non-autonomous by design**: agents act only when invoked; no agent triggers
  another, no background loops, no self-invocation
- **Guardian veto**: inspects a conclusion's *real* coherence and provenance
  (not the producing agent's self-report) and removes it from memory when it
  stands on insufficient ground
- A thin orchestration layer over CrystalFlow — it adds orchestration only, not
  new trust assumptions; the safety model is inherited wholesale
- Substantive policy-drafting rules ship in `src/policy_rules.py`

### 5. CrystalSensor: External Input Abstraction

CrystalCore includes a clean, principled layer (`src/crystal_sensor.py`) for
ingesting external sensory data (text, audio, environment, device state)
while maintaining full sovereignty and consent.

**Key principle:** this processes the EXTERNAL WORLD only. The mind is
inviolable. Not brain-reading, not a Neuralink simulation.

- `SensorReading` — type, raw data, confidence, consent bitmask, provenance
  note, source/device id, timestamp
- `SensorInputHandler` — registers sensor sources and captures readings
- `MockSensors` — deterministic, dependency-free simulations (text, audio,
  environment, device state, safe intent inference) so the pipeline is fully
  testable without hardware
- Readings flow into CrystalMemory, then CrystalFlow, then CrystalMind's
  Guardian — the same consent/coherence/provenance guarantees as every other
  layer, nothing new

See [`docs/SENSOR-LAYER-ARCHITECTURE.md`](./docs/SENSOR-LAYER-ARCHITECTURE.md)
for the full architecture and [`examples/example_sensor_to_action.py`](./examples/example_sensor_to_action.py)
for a runnable sensor-to-action demo:

```python
from src.crystal_sensor import SensorInputHandler, SensorType, MockSensors

sensor = SensorInputHandler()
sensor.register_sensor("text", MockSensors.mock_text_input)
reading = sensor.capture_reading(SensorType.TEXT, "text", text="turn on the kitchen lights")
print(reading)
```

### 6. CrystalLattice: Relational / Connective Substrate

CrystalLattice (`src/crystal_lattice.py`) is the "surround" that links a
CrystalCore instance to other devices, to humans in the Sovereign Node Mesh,
and to external LLMs — the technical foundation of the ecosystem-wide
**Incognita Lattice** gate layer.

- **Nodes** — registered participants (`local_core`, `device`, `human`,
  `external_llm`), each with a consent permission bitmask; local nodes carry
  auto-detected platform info for provenance
- **HandoffEnvelope** — every cross-node transfer is consent-flagged,
  SHA-256 provenance-hashed, and coherence-tagged; consent is fail-closed at
  creation *and* re-checked at send time
- **Air-gapped by default** — the module ships zero network code; external
  sends require both `allow_external=True` and an explicitly injected
  transport function, so a lattice can never leak by accident
- **Sovereign LLM Communication Layer** — the standardized, consent-gated
  envelope protocol for handoffs to external models (Grok, Claude, ...);
  inbound replies are integrity-checked and re-enter at *capped* coherence,
  so external confidence must earn trust through Guardian review
- Every attempt — allowed or refused — lands in an auditable transfer log

See [`docs/LATTICE-ARCHITECTURE.md`](./docs/LATTICE-ARCHITECTURE.md) for the
full design.

### Planned layers
- **Wisdom Layer** — a neutral, *non-dogmatic* knowledge layer atop CrystalMind
  (philosophy, emotional regulation, mythology, and consent-pending cultural
  knowledge), represented as inspectable, provenance-tagged, consent-flagged
  sources — never hardcoded belief. See [`docs/wisdom-layer.md`](./docs/wisdom-layer.md).
- **CrystalAudit** — full decision logging and exportable reports
- **Integration & deployment** — CLI, simple web UI, Raspberry Pi packaging

## Documentation

The per-layer reference lives in this README (above). Deeper design and operational
notes live in [`docs/`](./docs/):

- [`docs/build-structure.md`](./docs/build-structure.md) — the living map of the whole
  project: structure, built-vs-planned status, layers, and test counts. Start here.
- [`docs/SENSOR-LAYER-ARCHITECTURE.md`](./docs/SENSOR-LAYER-ARCHITECTURE.md) —
  CrystalSensor design and integration pattern.
- [`docs/LATTICE-ARCHITECTURE.md`](./docs/LATTICE-ARCHITECTURE.md) — CrystalLattice
  design: nodes, consent-gated handoffs, the air-gap default, and the Sovereign
  LLM Communication Layer.
- [`docs/wisdom-layer.md`](./docs/wisdom-layer.md) — design sketch for the planned
  Wisdom Layer (status: design, not built).
- [`docs/infrastructure.md`](./docs/infrastructure.md) — where CrystalCore runs and how
  heavy training is offloaded, with the sovereignty boundary made explicit.
- [`docs/philosophy.md`](./docs/philosophy.md) — the worldview and principles the
  framework is built to serve.

## Installation & quick start

```bash
git clone https://github.com/teraustralisincognita-svg/CrystalCore.git
cd CrystalCore
# NumPy is optional (faster array ingestion) and NOT needed for the example below.
# pip install numpy
```

```python
from src.crystal_memory import CrystalMemory

memory = CrystalMemory(max_ram_mb=256)

# Encode data with consent and priority.
nid = memory.encode(
    data=[1.5, 2.3, 0.0, 4.8],
    coherence_boost=0.9,
    consent_flags=3,           # bit 0 = user, bit 1 = family
    family_priority=1.2,
)

result = memory.retrieve(nid)
print(result)
```

Three end-to-end demos ship in `examples/`, each labelling the guarantees
(`[CONSENT]`, `[COHERENCE]`, `[PROVENANCE]`, `[DURABLE]`, `[PRUNING]`, `[VETO]`,
`[SENSOR]`, `[ACTION]`) in its output:

- `examples/family_decision_pipeline.py` — a "power of three" family decision
  exercised through Memory → Evolve → Flow, with a private note that fails
  closed for members who lack permission.
- `examples/policy_council.py` — the CrystalMind council (TruthSeeker, Creator,
  Guardian) drafting a position from a body of evidence using the substantive
  rules in `src/policy_rules.py`.
- `examples/example_sensor_to_action.py` — CrystalSensor → CrystalMemory →
  CrystalFlow → CrystalMind/Guardian → action, ending with a full audit
  trail; a second scenario shows Guardian refusing a low-confidence request.

## Testing

No external test framework is required (important for a bare Raspberry Pi):

```bash
python3 run_tests.py          # stdlib-only runner
```

This discovers and runs all eight test files. Expected: **140 passing** across
`test_crystal_memory.py`, `test_crystal_flow.py`, `test_crystal_evolve.py`,
`test_crystal_mind.py`, `test_crystal_sensor.py`, `test_crystal_lattice.py`,
`test_policy_rules.py`, and `test_properties.py`.
Operational log lines such as `Evicted ...` during the pruning tests are normal.

The property-based suite (`test_properties.py`) checks seven cross-cutting
invariants across many randomized inputs. It uses [Hypothesis](https://hypothesis.readthedocs.io/)
when installed and otherwise falls back to the bundled, dependency-free
`tests/property_harness.py` — preserving the zero-dependency guarantee on a bare
device while letting a developer machine use the full tool.

If you prefer pytest, the same files also run under it:

```bash
python3 -m pytest tests/ -v
```

Coverage includes:
- Quantization edge cases (empty, constant, extreme range, variable bit-width)
- Consent enforcement (per-consumer access, fail-closed reasoning, revocation)
- Coherence propagation and the gating sign-bug regression guard
- RAM pruning under pressure (priority-weighted eviction)
- Persistence, atomic writes, checksum validation, and corruption recovery
- Durable payload round-trips and backward compatibility with older files
- Deterministic evolution and both inheritance modes
- Agent stances, the Guardian veto, and the policy-drafting rule set
- Sensor capture, consent bitmasks, serialization, and provenance hashing
- Lattice handoffs: fail-closed consent, the air-gap default, envelope
  integrity/tamper detection, revocation at send time, and low-trust receipt
- Cross-cutting invariants (consent fail-closed, coherence ≤ weakest input,
  high-priority survival, payload round-trips) under randomized inputs

## Hardware & platform support

CrystalCore is **hardware-agnostic by design**: pure standard-library Python
(3.8+), zero required dependencies, no compiled extensions. It runs wherever
CPython runs — including hardware most frameworks have abandoned. The
Raspberry Pi is the *reference constraint target* (if it runs well there, it
runs well anywhere), not a requirement.

| Platform | Status | Notes |
| --- | --- | --- |
| Old laptops (Linux/Windows/macOS) | ✅ Runs | Any CPython 3.8+; often the best home for a family node |
| Raspberry Pi 4/5 | ✅ Reference target | Tested design constraint: <256 MB working set (see below) |
| Android | ✅ Runs | Via Termux or Pydroid 3 (both ship CPython) |
| iPhone / iPad | ✅ Runs | Via Pythonista, Pyto, or a-Shell; persistence needs an app-writable path |
| Servers (x86/ARM) | ✅ Runs | e.g. the live i5 node in `docs/infrastructure.md` |
| Embedded (MicroPython etc.) | ⚠️ Untested | Needs full CPython stdlib (`json`, `hashlib`, `dataclasses`) |
| Future hardware | ✅ By construction | No architecture assumptions; `detect_platform()` records the runtime for provenance |

Graceful degradation is runtime behaviour, not configuration: `max_ram_mb`
enforces a real measured budget on any device, memory pressure triggers
weighted pruning and symbolic (hash-only) fallback, and
`crystal_lattice.detect_platform()` records what hardware produced each
conclusion — for provenance, never for gatekeeping.

### Reference constraint target: Raspberry Pi (4/5)

- **Tested design target:** <256 MB working set. Use `max_ram_mb` (accepts a
  float) to enforce a hard limit; pruning triggers on *real* measured size.
- **Storage:** JSON persistence is atomic (`.tmp` + `os.replace` + `fsync`) and
  checksum-protected, safe for microSD. Put the store on the most resilient
  writable mount available.
- **Observability:** monitor with `get_stats()`; the consumer access log gives a
  basic audit trail (CrystalAudit will extend this).
- **`python3 -O`:** disables `assert` statements and `__debug__` blocks. The
  memory effect is negligible and it is **not** a tuning lever; it removes one
  internal guard, so treat it as optional and skip it if in doubt.
- **Production:** consider OS-level tooling — a `systemd` service, log rotation,
  and a watchdog.

### On-device memory profiling (optional)

Unit tests verify the eviction *mechanism*, not true resident memory. For that,
profile RSS on the Pi itself. `psutil` is optional and on-device only:

```python
import os, psutil
proc = psutil.Process(os.getpid())
# ... encode a workload ...
print(proc.memory_info().rss / 1024 / 1024, "MB RSS")
```

Watch that RSS plateaus rather than climbing without bound — that confirms
pruning is keeping pace with ingestion on your specific hardware.

### Performance note

`CrystalMemory._estimate_size()` recomputes the full node-graph size on every
`encode()` (O(n)). This is accurate but will slow down with thousands of nodes;
when it becomes a bottleneck, switch to an incremental size counter with a
periodic full recompute to correct drift.

## Project status

**Current:** CrystalMemory + CrystalFlow + CrystalEvolve + CrystalMind complete
and integrated, plus the optional CrystalSensor external-input layer and the
CrystalLattice relational substrate (consent-gated handoffs, air-gapped by
default), with three end-to-end demos. Zero required dependencies,
hardware-agnostic.

Alongside the `src/` core, the **`crystallcore/` package** carries the
SCES-aligned constitutional layers, delivered in five verified phases:

1. **Incognita Lattice** (`civilisation_one/lattice/`) — coordinate identity
   (Layer:Agent:Session:Version + SHA-256), routing, graph visualisation.
2. **Governance** (`crystallcore/governance/`) — SCES v11.0: 12 constitutional
   volumes (explicit authority grants, 7-stage evidence maturity, witness
   discipline, consent + coherence bounds, immutable audit trail, penalties,
   transitions, ratification) plus enforcement decorators.
3. **Topology** (`crystallcore/topology/`) — Q64.64 fixed-point arithmetic,
   12-ring Fibonacci topology, 256-D chiral manifold, dreamline router,
   starline hub (geographic anchors incl. Uluru).
4. **Sovereign Node Mesh** (`crystallcore/mesh/`) — governed messaging
   (four fail-closed gates: activation → consent → coherence → route) and
   ring-by-ring witnessed boot.
5. **Swarm** (`crystallcore/swarm/`) — evolutionary racing on crystal_evolve
   genomes: Pareto multi-objective fitness, closed-registry mutation,
   persistence-gated coherence reinforcement, audited generations.

Full suite: **175 passing tests** under the stdlib runner (plus a
pytest-based lattice suite), zero required dependencies.

**Next:** CrystalAudit (exportable decision reports), real lattice transports
(device-to-device and external-LLM backends), and packaging.

## Related vision & foundation

CrystalCore.OS is one of two core layers beneath the TerAustralis Incognita umbrella
vision — a sovereign, multiplanetary vision for Australian space capability.

- **TerAustralis Incognita** — the public-facing vision, coordination, and advocacy layer.
- **CrystalCore.OS** (this repo) — the sovereign-edge technical layer: local-first,
  auditable intelligence for constrained hardware.
- **Sovereign Node Mesh** — the human coordination layer: vetting and onboarding aligned
  collaborators, outreach protocols, first principles.
- **Incognita Lattice** — the overarching relational/gate layer that connects all of the
  above (tech, human, and pillars), handling consent, provenance, and interoperability.
  Its technical foundation inside this repo is **CrystalLattice**
  (`src/crystal_lattice.py`, [`docs/LATTICE-ARCHITECTURE.md`](./docs/LATTICE-ARCHITECTURE.md)).

CrystalCore's work sits within three cross-cutting thematic pillars shared across the
ecosystem: Starlines (origin narrative), Red Dust to Rockets (industrial/materials
capability), and Dreamlines (media and stakeholder engagement).

### Radical inclusivity

The ecosystem's guiding principle is *leave no one behind* — in hardware
(see the platform matrix above: old laptops and phones are first-class
citizens, not afterthoughts) and in knowledge. The planned Wisdom Layer
([`docs/wisdom-layer.md`](./docs/wisdom-layer.md)) is designed to hold the
full breadth of human perspective — religious and spiritual traditions
(including Gnostic texts such as the Nag Hammadi library's Apocryphon of
John, and concepts such as the Akashic Records), philosophical schools,
psychological and psychiatric frameworks, mathematical systems from sacred
geometry to conventional science, Indigenous knowledge (strictly
consent-pending until custodian partnership exists), and lived experience.

The mechanism is the point: every source enters as an inspectable,
provenance-tagged, consent-flagged perspective — never hardcoded belief,
never forced blending, never dominance of any one tradition. Claims still
pass through the same coherence and truth-seeking machinery as everything
else; inclusion means every voice is *held and attributable*, not that every
claim is asserted as fact.

Sovereign Futures Manifesto — the ethical and philosophical foundation for CrystalCore
(truth as anchor, individual/family agency, consent in the BCI/AI age). Maintained
separately and linked from the main TerAustralis project.

See also [`docs/philosophy.md`](./docs/philosophy.md) for how that worldview maps
onto the framework's design.

## Contributing

Contributions are welcome via fork and pull request — see
[`CONTRIBUTING.md`](./CONTRIBUTING.md) for the workflow, the project's
non-negotiables (stdlib-only, consent fail-closed, tests required), and
guidance on culturally respectful contributions.

## License

GNU AGPL-3.0 — see the `LICENSE` file. You are free to use, modify, and deploy
this framework; anything you build on it (including software offered as a
network service) must remain open under the same terms. This keeps the commons
sovereign: no one can take this work and close it off.

---

Repository: https://github.com/teraustralisincognita-svg/CrystalcoreOS
Built with a focus on truth, consent, and real-world sovereignty.
