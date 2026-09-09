# CrystalSensor — External Input Abstraction Layer

## Overview

`src/crystal_sensor.py` is an optional module that gives CrystalCore a clean
abstraction for external sensory data (audio, text, environment, device
state) flowing into the reasoning pipeline.

**Core principle: this processes the EXTERNAL WORLD only. The mind is
inviolable.** It is NOT a brain-reading layer and NOT a Neuralink
simulation. It is a principled way to ingest legitimate external data and
reason about it while keeping CrystalCore's sovereignty, consent, and
provenance guarantees intact.

## Architecture

```
   +--------------------------------------------------------------+
   |  EXTERNAL WORLD                                               |
   |  (User input, audio, environment, device state, sensors)      |
   +---------------------------+------------------------------------+
                                |
                                v
   +--------------------------------------------------------------+
   |  CrystalSensor  (src/crystal_sensor.py)                       |
   |  SensorInputHandler — capture readings, register sources,     |
   |  attach consent flags + provenance, produce SensorReading     |
   +---------------------------+------------------------------------+
                                | reading.to_dict() / hash_provenance()
                                v
   +--------------------------------------------------------------+
   |  CrystalMemory   (persistent storage)                         |
   |  memory.encode(data=[...], coherence_boost=reading.confidence,|
   |                consent_flags=reading.consent_required,        |
   |                payload=reading.to_dict())                     |
   +---------------------------+------------------------------------+
                                | reads permitted nodes
                                v
   +--------------------------------------------------------------+
   |  CrystalFlow    (reasoning engine)                             |
   |  flow.apply_rule(rule, [node_ids], ...) per step;              |
   |  fail-closed on consent; coherence = min(inputs) x strength;   |
   |  every conclusion written back with provenance                |
   +---------------------------+------------------------------------+
                                | conclusion node id(s)
                                v
   +--------------------------------------------------------------+
   |  CrystalMind / Guardian   (veto layer)                         |
   |  mind.council([agent_names], [node_ids]) runs the proposing    |
   |  agent(s), then Guardian inspects each result's REAL           |
   |  coherence + provenance (not the agent's self-report) and      |
   |  may veto — pulling the conclusion back out of memory          |
   +---------------------------+------------------------------------+
                                | approved only
                                v
   +--------------------------------------------------------------+
   |  ACTION / RESPONSE                                             |
   |  (Turn on lights, answer query, send message, etc.)            |
   +--------------------------------------------------------------+
```

## Key concepts

### 1. `SensorReading`

Every piece of external data becomes a `SensorReading` with:

- `sensor_type` — `SensorType.AUDIO | TEXT | ENVIRONMENTAL | DEVICE | MOCK_INTENT`
- `raw_data` — the actual observation (a plain dict)
- `confidence` — how sure are we? (0.0–1.0)
- `consent_required` — bitmask of who may access this data (same convention
  as `CoherenceMetadata.consent_flags`: bit 0 = user, bit 1 = family, ...)
- `provenance_note` — why/how the reading was captured
- `source_id` / `device_id` — which sensor and which edge node
- `timestamp` — when it was captured

`reading.to_dict()` gives a JSON-serializable form; `reading.hash_provenance()`
gives a deterministic fingerprint over the reading's content and origin.

### 2. `SensorInputHandler`

The abstraction that manages sensor sources:

```python
sensor = SensorInputHandler(device_id="my_node_1")
sensor.register_sensor("text_input", MockSensors.mock_text_input)

reading = sensor.capture_reading(
    sensor_type=SensorType.TEXT,
    source_id="text_input",
    consent_bitmask=0b11,             # user + family
    provenance_note="User typed this command",
    text="turn on the kitchen lights",
)

sensor.list_readings(SensorType.TEXT)  # query captured history
```

`capture_reading` raises `KeyError` for an unregistered `source_id` — it
never silently invents a reading.

### 3. `MockSensors`

Safe, deterministic simulations of real sensors, for development and testing
without hardware:

- `MockSensors.mock_audio()` — simulated speech/sound
- `MockSensors.mock_text_input("text")` — simulated user typing
- `MockSensors.mock_environment()` — simulated temperature/humidity/light
- `MockSensors.mock_device_state()` — simulated battery/CPU/memory/hub state
- `MockSensors.mock_intent_simulation("query")` — **SAFE** intent inference

**Important:** intent simulation is NOT brain-reading. It infers intent only
from user text/voice input (deliberately provided) and visible context
(environment, device state, time of day) — all external, auditable,
consensual data. Never brain signals.

## Integration pattern

```python
from src.crystal_sensor import SensorInputHandler, SensorType, MockSensors
from src.crystal_memory import CrystalMemory
from src.crystal_flow import CrystalFlow, Rule
from src.crystal_mind import CrystalMind, AgentSpec

# 1. Capture
sensor = SensorInputHandler(device_id="my_node_1")
sensor.register_sensor("text_input", MockSensors.mock_text_input)
reading = sensor.capture_reading(
    SensorType.TEXT, "text_input",
    consent_bitmask=0b11, text="turn on the kitchen lights",
)

# 2. Store (consent + coherence + provenance travel with the node)
memory = CrystalMemory(max_ram_mb=64, storage_path="sensor_memory.json")
memory.register_consumer("user_0", "User", permissions=0b01)
node_id = memory.encode(
    data=[reading.confidence],
    coherence_boost=reading.confidence,
    consent_flags=reading.consent_required,
    payload=reading.to_dict(),
)

# 3. Reason (fails CLOSED if consent is missing)
flow = CrystalFlow(memory, consumer_id="user_0", min_input_coherence=0.4)
rule = Rule(name="text_to_action", fn=lambda facts: {"action": "..."}, strength=0.95)
result = flow.apply_rule(rule, [node_id])

# 4. Guardian inspects and may veto
mind = CrystalMind(memory, session_consumer_id="user_0")
mind.register_agent(AgentSpec(name="ActionExecutor", role="action", default_rule=rule))
council = mind.council(["ActionExecutor", "Guardian"], [node_id])
if not council["vetoes"]:
    ...  # take the action
```

See `examples/example_sensor_to_action.py` for the full, runnable version of
this loop, including a scenario where Guardian's coherence gate refuses a
low-confidence request.

## Why this design?

**Sovereignty** — no cloud, no third parties, no lock-in; everything runs
locally on the edge node.

**Consent** — every reading carries explicit consent flags; reasoning fails
closed if permission is missing; consent can be revoked at any time via
`CrystalMemory.revoke_consumer`.

**Provenance** — every reading is tagged with source, timestamp, confidence;
every reasoning step chains back to its inputs; full audit trail from sensor
to action via `flow.get_derivation_log()` and `mind.get_action_log()`.

**Safety** — Guardian can veto unsound conclusions using their real
coherence and provenance, not the producing agent's self-report; coherence
tracking prevents false confidence; mock sensors let you test without
hardware.

**Privacy** — no brain data is ever captured; only external, voluntary
inputs are processed; you control what data flows in.

## What this is NOT

- Not a brain-reading system — no EEG, no neural signals
- Not a Neuralink simulation — no mock versions of proprietary tech
- Not an autonomous agent — every action still requires Guardian approval
- Not a chatbot — reasoning over your data, not LLM responses
- Not a replacement for human judgment — Guardian and the human operator can
  always override

## What this IS

A clean, edge-friendly abstraction for external inputs (text, audio,
environment, device state), integrated with CrystalCore's consent and
provenance machinery, testable entirely with mocks, and honest about its
limits.
