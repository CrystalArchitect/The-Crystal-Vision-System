#!/usr/bin/env python3
"""
Sensor to Action — End-to-End CrystalSensor Demo
==================================================

The full sovereignty loop, sensor to action:

    EXTERNAL WORLD -> CrystalSensor -> CrystalMemory -> CrystalFlow
                                                       -> CrystalMind/Guardian
                                                       -> ACTION

A user types "turn on the kitchen lights". CrystalSensor captures that
command alongside environmental and device-state context. CrystalMemory
stores each reading with consent flags and provenance. CrystalFlow builds a
reasoning chain that interprets the command and proposes an action.
CrystalMind's Guardian then inspects the conclusion's real coherence and
provenance — not any agent's self-report — before the action is allowed to
execute. A second scenario shows Guardian vetoing a low-confidence request,
so the veto path is not just claimed but demonstrated.

Demonstrated guarantees (each labelled in the output):
  [SENSOR]      external data captured with type, confidence, consent, provenance
  [CONSENT]     readings only flow to consumers with matching permission bits
  [COHERENCE]   confidence = min(input coherences) x rule_strength at each step
  [PROVENANCE]  every conclusion traces back to the exact readings + rules used
  [VETO]        Guardian inspects real coherence/provenance and can refuse
  [ACTION]      the device action only executes after Guardian approval

Run:  python3 examples/example_sensor_to_action.py
Requires only the standard library.
"""

import os
import sys
import tempfile

# Allow running from the repo root or the examples/ dir.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from src.crystal_memory import CrystalMemory
    from src.crystal_flow import CrystalFlow, Rule
    from src.crystal_mind import CrystalMind, AgentSpec
    from src.crystal_sensor import SensorInputHandler, SensorType, MockSensors
except ImportError:
    from crystal_memory import CrystalMemory
    from crystal_flow import CrystalFlow, Rule
    from crystal_mind import CrystalMind, AgentSpec
    from crystal_sensor import SensorInputHandler, SensorType, MockSensors


def hr(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


# --------------------------------------------------------------------------- #
# Reasoning rules
# --------------------------------------------------------------------------- #
def interpret_command(facts):
    """CrystalFlow step 1: turn the raw text reading into a structured intent."""
    reading = facts[0].content  # the SensorReading.to_dict() payload
    text = reading.get("raw_data", {}).get("text", "")
    lower = text.lower()
    if "turn on" in lower:
        action = "turn_on"
    elif "turn off" in lower:
        action = "turn_off"
    else:
        action = "unknown"
    device = "kitchen_lights" if "kitchen" in lower and "light" in lower else "unknown_device"
    return {"action": action, "device": device, "raw_text": text}


def decide_action(facts):
    """The ActionExecutor agent's rule: combine the interpreted command with
    environmental and device-state context to reach an executable decision."""
    interpreted = facts[0].content
    env = facts[1].content.get("raw_data", {})
    device_state = facts[2].content.get("raw_data", {})

    device = interpreted.get("device")
    hub_key = f"{device}_hub"
    hub_connected = device_state.get(hub_key) == "connected"

    confirmed = (
        interpreted.get("action") in ("turn_on", "turn_off")
        and device != "unknown_device"
        and hub_connected
    )
    return {
        "action": interpreted.get("action"),
        "device": device,
        "confirmed": confirmed,
        "context": {
            "light_level_lux": env.get("light_level_lux"),
            "time_of_day": env.get("time_of_day"),
            "hub_connected": hub_connected,
        },
        "justification": (
            f"{interpreted.get('action')} {device}: hub_connected={hub_connected}, "
            f"ambient_light={env.get('light_level_lux')} lux at {env.get('time_of_day')}"
        ),
    }


def main():
    workdir = tempfile.mkdtemp(prefix="sensor_to_action_")
    store = os.path.join(workdir, "sensor_memory.json")

    # Consent bit layout: bit0 = user, bit1 = family.
    USER, FAMILY = 0b01, 0b10
    SHARED = USER | FAMILY

    # ---------------------------------------------------------------- #
    # 1. CAPTURE — the user speaks, the environment/device report in
    # ---------------------------------------------------------------- #
    hr("1. CrystalSensor — capturing external-world readings")

    sensor = SensorInputHandler(device_id="kitchen_node_1")
    sensor.register_sensor("text_input", MockSensors.mock_text_input)
    sensor.register_sensor("env_sensors", MockSensors.mock_environment)
    sensor.register_sensor("device_state", MockSensors.mock_device_state)

    print('  User types: "turn on the kitchen lights"')
    command_reading = sensor.capture_reading(
        sensor_type=SensorType.TEXT,
        source_id="text_input",
        consent_bitmask=SHARED,
        provenance_note="User typed this command",
        text="turn on the kitchen lights",
    )
    print(f"  [SENSOR]     type={command_reading.sensor_type.value} "
          f"confidence={command_reading.confidence} "
          f"consent={bin(command_reading.consent_required)}")
    print(f"  [PROVENANCE] {command_reading.hash_provenance()[:16]}...")

    print("\n  Capturing environmental context:")
    env_reading = sensor.capture_reading(
        sensor_type=SensorType.ENVIRONMENTAL,
        source_id="env_sensors",
        consent_bitmask=SHARED,
        provenance_note="Ambient sensors at time of command",
    )
    print(f"  [SENSOR]     {env_reading.raw_data}")

    print("\n  Capturing device state:")
    device_reading = sensor.capture_reading(
        sensor_type=SensorType.DEVICE,
        source_id="device_state",
        consent_bitmask=SHARED,
        provenance_note="Kitchen hub connectivity/state at time of command",
    )
    print(f"  [SENSOR]     {device_reading.raw_data}")

    # ---------------------------------------------------------------- #
    # 2. MEMORY — store each reading with consent + coherence
    # ---------------------------------------------------------------- #
    hr("2. CrystalMemory — storing readings with consent + provenance")

    mem = CrystalMemory(max_ram_mb=64, storage_path=store, decay_half_life_days=45.0)
    mem.register_consumer("user_0", "User", permissions=USER)
    mem.register_consumer("family", "Family (shared view)", permissions=SHARED)

    command_id = mem.encode(
        data=[command_reading.confidence],
        coherence_boost=command_reading.confidence,
        consent_flags=command_reading.consent_required,
        payload=command_reading.to_dict(),
    )
    env_id = mem.encode(
        data=[env_reading.confidence],
        coherence_boost=env_reading.confidence,
        consent_flags=env_reading.consent_required,
        payload=env_reading.to_dict(),
    )
    device_id = mem.encode(
        data=[device_reading.confidence],
        coherence_boost=device_reading.confidence,
        consent_flags=device_reading.consent_required,
        payload=device_reading.to_dict(),
    )
    print(f"  stored command reading -> {command_id}")
    print(f"  stored env reading     -> {env_id}")
    print(f"  stored device reading  -> {device_id}")
    print(f"  [CONSENT]    all three flagged {bin(SHARED)} (user + family)")
    print(f"  stats: {mem.get_stats()}")

    # ---------------------------------------------------------------- #
    # 3. FLOW — the reasoning chain builds
    # ---------------------------------------------------------------- #
    hr("3. CrystalFlow — reasoning chain builds (interpret -> decide)")

    flow = CrystalFlow(mem, consumer_id="user_0", min_input_coherence=0.4)

    interpret_rule = Rule(
        name="interpret_command",
        fn=interpret_command,
        strength=0.95,
        description="Parse the raw text command into a structured intent.",
    )
    interp_res = flow.apply_rule(interpret_rule, [command_id], output_fact_type="interpreted_command")
    print(f"  step 1 interpret_command : status={interp_res['status']} "
          f"[COHERENCE]={interp_res['coherence']:.4f}")
    print(f"                             content={interp_res['content']}")
    interpreted_id = interp_res["output_node_id"]

    # ---------------------------------------------------------------- #
    # 4. MIND — ActionExecutor proposes, Guardian inspects and approves
    # ---------------------------------------------------------------- #
    hr("4. CrystalMind — Guardian inspects and approves")

    mind = CrystalMind(mem, session_consumer_id="user_0", guardian_min_coherence=0.4)
    mind.register_agent(AgentSpec(
        name="ActionExecutor",
        role="action",
        min_input_coherence=0.4,
        coherence_factor=1.0,
        default_rule=Rule(name="decide_action", fn=decide_action, strength=0.9,
                          description="Combine interpreted command + context into an executable decision."),
        description="Confirms and proposes device actions from interpreted sensor context.",
    ))

    council_out = mind.council(
        ["ActionExecutor", "Guardian"],
        input_node_ids=[interpreted_id, env_id, device_id],
    )
    executor_result = council_out["results"]["ActionExecutor"]
    print(f"  ActionExecutor proposal  : status={executor_result['status']} "
          f"[COHERENCE]={executor_result['coherence']:.4f}")
    print(f"                             content={executor_result['content']}")
    print(f"  [VETO]       vetoes this round: {council_out['vetoes'] or 'none'}")

    # ---------------------------------------------------------------- #
    # 5. ACTION — only if Guardian approved
    # ---------------------------------------------------------------- #
    hr("5. Action — executes only after Guardian approval")

    if executor_result["status"] == "ok" and executor_result["content"]["confirmed"]:
        decision = executor_result["content"]
        print(f"  [ACTION]     APPROVED -> executing: {decision['action']} {decision['device']}")
        print(f"               justification: {decision['justification']}")
        print("               >>> Kitchen lights: ON <<<")
    else:
        print("  [ACTION]     NOT executed (Guardian did not approve).")

    # ---------------------------------------------------------------- #
    # 6. Guardian vetoes a low-confidence / unverified request
    # ---------------------------------------------------------------- #
    hr("6. Guardian veto path — a low-confidence request is refused")

    # A vague, unauthenticated utterance picked up faintly (e.g. distant
    # background speech) — deliberately captured at low confidence.
    print('  Ambient audio picks up: "...lights..." (faint, low confidence)')
    ambient_reading = sensor.capture_reading(
        sensor_type=SensorType.MOCK_INTENT,
        source_id="text_input",  # reuse the text backend to simulate a garbled utterance
        consent_bitmask=SHARED,
        provenance_note="Low-confidence ambient pickup, not a direct command",
        confidence=0.2,
        text="...lights...",
    )
    ambient_id = mem.encode(
        data=[ambient_reading.confidence],
        coherence_boost=ambient_reading.confidence,
        consent_flags=ambient_reading.consent_required,
        payload=ambient_reading.to_dict(),
    )
    weak_interp = flow.apply_rule(interpret_rule, [ambient_id], output_fact_type="interpreted_command")
    weak_coherence = weak_interp.get("coherence")
    coh_str = f"{weak_coherence:.4f}" if weak_coherence is not None else "n/a (gated before scoring)"
    print(f"  step 1 interpret_command : status={weak_interp['status']} [COHERENCE]={coh_str}")

    if weak_interp["status"] == "ok":
        weak_council = mind.council(
            ["ActionExecutor", "Guardian"],
            input_node_ids=[weak_interp["output_node_id"], env_id, device_id],
        )
        weak_result = weak_council["results"]["ActionExecutor"]
        print(f"  ActionExecutor proposal : status={weak_result['status']}")
        print(f"  [VETO]       vetoes this round: {weak_council['vetoes'] or 'none'}")
        if weak_result["status"] != "ok":
            print("  [ACTION]     NOT executed — Guardian refused: "
                  f"{weak_result.get('veto_reason', 'coherence/consent gate failed')}")
        else:
            print("  [ACTION]     (unexpectedly approved)")
    else:
        print(f"  [ACTION]     NOT executed — reasoning step itself refused "
              f"({weak_interp['status']}), never reached Guardian.")

    # ---------------------------------------------------------------- #
    # Full audit trail
    # ---------------------------------------------------------------- #
    hr("Audit trail — every step, sensor to action")

    print("Sensor readings captured:")
    for r in sensor.list_readings():
        print(f"  [SENSOR]     {r.sensor_type.value:<12} source={r.source_id:<12} "
              f"confidence={r.confidence:<5} consent={bin(r.consent_required):<6} "
              f"provenance={r.hash_provenance()[:12]}...")

    print("\nCrystalFlow derivation log (reasoning steps):")
    for rec in flow.get_derivation_log():
        print(f"  [PROVENANCE] {rec}")

    print("\nCrystalMind action log (agent invocations + Guardian reviews):")
    for rec in mind.get_action_log():
        print(f"  [MIND]       {rec}")

    print("\nCrystalMemory consumer access log (who saw what):")
    for entry in mem.registry.access_log[-10:]:
        print(f"  [CONSENT]    {entry}")

    hr("Done")
    print(f"  Working store: {store}")
    print("  Every action above traces back through Guardian's review, the")
    print("  reasoning chain, and the original sensor readings — sensor to action,")
    print("  fully auditable, nothing autonomous, nothing hidden.")


if __name__ == "__main__":
    main()
