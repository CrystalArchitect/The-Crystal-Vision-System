import json
import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.crystal_sensor import (
    SensorType, SensorReading, SensorInputHandler, MockSensors,
)


# --------------------------------------------------------------------------- #
# SensorType
# --------------------------------------------------------------------------- #
def test_sensor_type_enum_values():
    assert SensorType.AUDIO.value == "audio"
    assert SensorType.TEXT.value == "text"
    assert SensorType.ENVIRONMENTAL.value == "environmental"
    assert SensorType.DEVICE.value == "device"
    assert SensorType.MOCK_INTENT.value == "mock_intent"


# --------------------------------------------------------------------------- #
# SensorInputHandler — registration + capture
# --------------------------------------------------------------------------- #
def test_register_and_capture_reading():
    handler = SensorInputHandler(device_id="node_1")
    handler.register_sensor("text_input", MockSensors.mock_text_input)

    reading = handler.capture_reading(
        sensor_type=SensorType.TEXT,
        source_id="text_input",
        consent_bitmask=0b11,
        provenance_note="User typed this command",
        text="turn on the kitchen lights",
    )

    assert isinstance(reading, SensorReading)
    assert reading.sensor_type == SensorType.TEXT
    assert reading.raw_data["text"] == "turn on the kitchen lights"
    assert reading.consent_required == 0b11
    assert reading.provenance_note == "User typed this command"
    assert reading.source_id == "text_input"
    assert reading.device_id == "node_1"
    assert reading.timestamp > 0
    assert reading in handler.readings


def test_capture_reading_unknown_sensor_raises():
    handler = SensorInputHandler()
    try:
        handler.capture_reading(SensorType.TEXT, "not_registered")
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for unregistered source_id")


def test_capture_reading_default_confidence_by_type():
    handler = SensorInputHandler()
    handler.register_sensor("env_sensors", MockSensors.mock_environment)
    handler.register_sensor("text_input", MockSensors.mock_text_input)

    env_reading = handler.capture_reading(SensorType.ENVIRONMENTAL, "env_sensors")
    text_reading = handler.capture_reading(SensorType.TEXT, "text_input", text="hi")

    # Directly-typed text is trusted at least as much as inferred/sensed data.
    assert text_reading.confidence >= env_reading.confidence


def test_capture_reading_explicit_confidence_overrides_default():
    handler = SensorInputHandler()
    handler.register_sensor("text_input", MockSensors.mock_text_input)
    reading = handler.capture_reading(
        SensorType.TEXT, "text_input", confidence=0.42, text="hello"
    )
    assert reading.confidence == 0.42


# --------------------------------------------------------------------------- #
# Serialization + provenance
# --------------------------------------------------------------------------- #
def test_reading_to_dict_is_json_serializable():
    handler = SensorInputHandler()
    handler.register_sensor("device_state", MockSensors.mock_device_state)
    reading = handler.capture_reading(SensorType.DEVICE, "device_state")

    d = reading.to_dict()
    encoded = json.dumps(d)  # must not raise
    decoded = json.loads(encoded)
    assert decoded["sensor_type"] == "device"
    assert decoded["raw_data"]["kitchen_lights_hub"] == "connected"


def test_hash_provenance_deterministic_and_sensitive_to_data():
    handler = SensorInputHandler(device_id="node_1")
    handler.register_sensor("text_input", MockSensors.mock_text_input)

    r1 = handler.capture_reading(SensorType.TEXT, "text_input", text="turn on the lights")
    # Same content re-hashed is stable.
    assert r1.hash_provenance() == r1.hash_provenance()

    r2 = handler.capture_reading(SensorType.TEXT, "text_input", text="turn off the lights")
    assert r1.hash_provenance() != r2.hash_provenance()


# --------------------------------------------------------------------------- #
# Listing / filtering
# --------------------------------------------------------------------------- #
def test_list_readings_filters_by_type():
    handler = SensorInputHandler()
    handler.register_sensor("text_input", MockSensors.mock_text_input)
    handler.register_sensor("env_sensors", MockSensors.mock_environment)

    handler.capture_reading(SensorType.TEXT, "text_input", text="hello")
    handler.capture_reading(SensorType.ENVIRONMENTAL, "env_sensors")
    handler.capture_reading(SensorType.TEXT, "text_input", text="world")

    all_readings = handler.list_readings()
    text_readings = handler.list_readings(SensorType.TEXT)
    env_readings = handler.list_readings(SensorType.ENVIRONMENTAL)

    assert len(all_readings) == 3
    assert len(text_readings) == 2
    assert len(env_readings) == 1
    assert all(r.sensor_type == SensorType.TEXT for r in text_readings)


# --------------------------------------------------------------------------- #
# MockSensors
# --------------------------------------------------------------------------- #
def test_mock_sensors_produce_expected_keys():
    audio = MockSensors.mock_audio()
    assert "transcript" in audio and "duration_s" in audio

    text = MockSensors.mock_text_input("hi there")
    assert text["text"] == "hi there"

    env = MockSensors.mock_environment()
    assert {"temperature_c", "humidity_percent", "light_level_lux"} <= env.keys()

    device = MockSensors.mock_device_state()
    assert "battery_percent" in device and "kitchen_lights_hub" in device

    intent_on = MockSensors.mock_intent_simulation("please turn on the kitchen lights")
    assert intent_on["inferred_intent"] == "activate_device"
    intent_off = MockSensors.mock_intent_simulation("turn off the lights")
    assert intent_off["inferred_intent"] == "deactivate_device"
    intent_unknown = MockSensors.mock_intent_simulation("what's the weather")
    assert intent_unknown["inferred_intent"] == "unknown"
