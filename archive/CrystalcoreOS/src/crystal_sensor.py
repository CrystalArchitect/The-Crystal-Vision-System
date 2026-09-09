#!/usr/bin/env python3
"""
CrystalSensor - External Input Abstraction Layer for CrystalCore

Core principle: this processes the EXTERNAL WORLD only. The mind is
inviolable. CrystalSensor is NOT a brain-reading layer and NOT a Neuralink
simulation — it is a principled way to ingest legitimate external data
(text, audio, environment, device state) and reason about it while keeping
CrystalCore's sovereignty, consent, and provenance guarantees intact.

Pipeline this module feeds:

    EXTERNAL WORLD -> CrystalSensor -> CrystalMemory -> CrystalFlow
                                                       -> CrystalMind/Guardian
                                                       -> ACTION

Key pieces:
    SensorType          - the kind of external signal a reading represents
    SensorReading        - one captured observation + its consent/provenance metadata
    SensorInputHandler   - registers sensor sources and captures readings
    MockSensors          - safe, deterministic sensor simulations (no hardware needed)

"Intent simulation" (MockSensors.mock_intent_simulation) infers intent only
from external, voluntarily-provided signals (typed/spoken text, visible
environment, device state, time of day) — never from brain signals.

Dependencies: standard library only.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import hashlib
import json
import time


# --------------------------------------------------------------------------- #
# Sensor types
# --------------------------------------------------------------------------- #
class SensorType(Enum):
    AUDIO = "audio"
    TEXT = "text"
    ENVIRONMENTAL = "environmental"
    DEVICE = "device"
    MOCK_INTENT = "mock_intent"


# --------------------------------------------------------------------------- #
# Sensor reading
# --------------------------------------------------------------------------- #
@dataclass
class SensorReading:
    """One captured observation of the external world, with full metadata.

    consent_required is a bitmask (same convention as CrystalMemory's
    consent_flags): bit 0 = user, bit 1 = family, etc. It travels unchanged
    into CrystalMemory.encode(consent_flags=reading.consent_required) so the
    reading is only ever visible to consumers it was captured for.
    """
    sensor_type: SensorType
    raw_data: Dict[str, Any]
    confidence: float = 0.9
    consent_required: int = 0b1
    provenance_note: str = ""
    source_id: str = ""
    device_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_type": self.sensor_type.value,
            "raw_data": self.raw_data,
            "confidence": self.confidence,
            "consent_required": self.consent_required,
            "provenance_note": self.provenance_note,
            "source_id": self.source_id,
            "device_id": self.device_id,
            "timestamp": self.timestamp,
        }

    def hash_provenance(self) -> str:
        """Deterministic fingerprint of this reading's content + origin.

        Two readings with identical data, source, device and timestamp hash
        identically; changing any of those changes the hash. Used as a
        provenance anchor when the reading is stored in CrystalMemory.
        """
        canonical = json.dumps(
            {
                "sensor_type": self.sensor_type.value,
                "raw_data": self.raw_data,
                "source_id": self.source_id,
                "device_id": self.device_id,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Sensor input handler
# --------------------------------------------------------------------------- #
class SensorInputHandler:
    """Registers sensor sources and turns their output into auditable
    SensorReading objects. Holds no opinions about what the data means —
    that is CrystalFlow's job, downstream and consent-checked."""

    # Reasonable default confidences per sensor type when the caller doesn't
    # supply one. Directly-typed text is trusted most; inferred intent least.
    _DEFAULT_CONFIDENCE = {
        SensorType.TEXT: 0.98,
        SensorType.AUDIO: 0.85,
        SensorType.ENVIRONMENTAL: 0.9,
        SensorType.DEVICE: 0.95,
        SensorType.MOCK_INTENT: 0.6,
    }

    def __init__(self, device_id: str = "edge_node_1"):
        self.device_id = device_id
        self.sensors: Dict[str, Callable[..., Dict[str, Any]]] = {}
        self.readings: List[SensorReading] = []

    def register_sensor(self, source_id: str, handler_fn: Callable[..., Dict[str, Any]]) -> None:
        """Register a sensor source. `handler_fn` takes arbitrary kwargs and
        returns a plain dict of raw observations (a mock or a real backend)."""
        self.sensors[source_id] = handler_fn

    def capture_reading(
        self,
        sensor_type: SensorType,
        source_id: str,
        consent_bitmask: int = 0b1,
        provenance_note: str = "",
        confidence: Optional[float] = None,
        **handler_kwargs: Any,
    ) -> SensorReading:
        """Capture one reading from a registered sensor source.

        Raises KeyError if `source_id` was never registered — captures never
        silently invent data for an unregistered source.
        """
        if source_id not in self.sensors:
            raise KeyError(f"no sensor registered for source_id={source_id!r}")

        raw_data = self.sensors[source_id](**handler_kwargs)
        reading = SensorReading(
            sensor_type=sensor_type,
            raw_data=raw_data,
            confidence=confidence if confidence is not None else self._DEFAULT_CONFIDENCE.get(sensor_type, 0.8),
            consent_required=consent_bitmask,
            provenance_note=provenance_note,
            source_id=source_id,
            device_id=self.device_id,
        )
        self.readings.append(reading)
        return reading

    def list_readings(self, sensor_type: Optional[SensorType] = None) -> List[SensorReading]:
        if sensor_type is None:
            return list(self.readings)
        return [r for r in self.readings if r.sensor_type == sensor_type]


# --------------------------------------------------------------------------- #
# Mock sensors — safe, deterministic, no hardware required
# --------------------------------------------------------------------------- #
class MockSensors:
    """Deterministic simulations of real sensors, for development and testing
    without hardware. None of these ever touch brain/neural data — only
    external, voluntarily-provided signals."""

    @staticmethod
    def mock_audio(duration_s: float = 2.0) -> Dict[str, Any]:
        return {
            "transcript": "<simulated speech audio>",
            "duration_s": duration_s,
            "volume_db": 42.0,
        }

    @staticmethod
    def mock_text_input(text: str = "") -> Dict[str, Any]:
        return {"text": text, "input_method": "keyboard"}

    @staticmethod
    def mock_environment() -> Dict[str, Any]:
        return {
            "temperature_c": 21.5,
            "humidity_percent": 38.0,
            "light_level_lux": 12.0,
            "time_of_day": "evening",
        }

    @staticmethod
    def mock_device_state() -> Dict[str, Any]:
        return {
            "battery_percent": 78,
            "cpu_percent": 22,
            "memory_mb": 184,
            "kitchen_lights_hub": "connected",
            "kitchen_lights_state": "off",
        }

    @staticmethod
    def mock_intent_simulation(query: str) -> Dict[str, Any]:
        """SAFE intent inference: pattern-matches the user's own typed/spoken
        text plus visible context. NOT brain-reading — it only ever sees what
        the user deliberately provided or what is externally observable."""
        lower = query.lower()
        if "turn on" in lower:
            inferred = "activate_device"
        elif "turn off" in lower:
            inferred = "deactivate_device"
        else:
            inferred = "unknown"
        return {
            "inferred_intent": inferred,
            "basis": ["user_text_input", "visible_context"],
            "source_query": query,
        }


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sensor = SensorInputHandler(device_id="demo_node_1")
    sensor.register_sensor("text_input", MockSensors.mock_text_input)
    sensor.register_sensor("env_sensors", MockSensors.mock_environment)
    sensor.register_sensor("device_state", MockSensors.mock_device_state)

    reading = sensor.capture_reading(
        sensor_type=SensorType.TEXT,
        source_id="text_input",
        consent_bitmask=0b11,
        provenance_note="User typed this command",
        text="turn on the kitchen lights",
    )
    print("Captured reading:", reading.to_dict())
    print("Provenance hash :", reading.hash_provenance())
