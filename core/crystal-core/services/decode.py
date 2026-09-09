# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""DECODE — validate and normalize crystal.twin.event/1 envelopes.

Belt-Three carried into metering: no fake hydrology → no fake events.
Invalid input is quarantined with a reason, never silently dropped and
never allowed through. Units are normalized so the twin speaks one tongue.
"""

from __future__ import annotations

from datetime import datetime

SCHEMA = "crystal.twin.event/1"

REQUIRED = ("schema", "event_id", "source_did", "h3", "class", "value", "unit", "observed_at")

# canonical unit per class prefix, with accepted conversions
UNIT_RULES = {
    "energy": {"canonical": "kWh", "convert": {"Wh": 0.001, "kWh": 1.0, "MWh": 1000.0}},
    "water": {"canonical": "kL", "convert": {"L": 0.001, "kL": 1.0, "ML": 1000.0}},
    "mobility": {"canonical": "count", "convert": {"count": 1.0}},
}


def decode_event(raw: dict, seen_ids: set[str] | None = None) -> tuple[dict | None, str]:
    """Return (normalized_event, "") or (None, quarantine_reason)."""
    if not isinstance(raw, dict):
        return None, "not an object"
    if raw.get("schema") != SCHEMA:
        return None, f"unknown schema {raw.get('schema')!r} (want {SCHEMA})"
    missing = [f for f in REQUIRED if not str(raw.get(f, "")).strip()]
    if missing:
        return None, f"missing fields: {', '.join(missing)}"

    event_id = str(raw["event_id"])
    if seen_ids is not None and event_id in seen_ids:
        return None, f"replay: event_id {event_id} already seen"

    cls = str(raw["class"])
    domain, _, metric = cls.partition(".")
    if not metric:
        return None, f"class {cls!r} must be domain.metric"
    rules = UNIT_RULES.get(domain)
    if rules is None:
        return None, f"unknown domain {domain!r} (know: {', '.join(UNIT_RULES)})"

    try:
        value = float(raw["value"])
    except (TypeError, ValueError):
        return None, f"value {raw['value']!r} is not numeric"
    if value < 0:
        return None, "negative value"

    unit = str(raw["unit"])
    factor = rules["convert"].get(unit)
    if factor is None:
        return None, f"unit {unit!r} not accepted for {domain!r} (accept: {', '.join(rules['convert'])})"

    observed_at = str(raw["observed_at"])
    try:
        datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError:
        return None, f"observed_at {observed_at!r} is not ISO 8601"

    if seen_ids is not None:
        seen_ids.add(event_id)
    return {
        "schema": SCHEMA,
        "event_id": event_id,
        "source_did": str(raw["source_did"]),
        "h3": str(raw["h3"]),
        "class": cls,
        "value": value * factor,
        "unit": rules["canonical"],
        "observed_at": observed_at,
        "raw_ref": str(raw.get("raw_ref", "")),
    }, ""


def decode_batch(raws: list[dict]) -> tuple[list[dict], list[dict]]:
    """Return (accepted, quarantined). Quarantine entries carry the reason."""
    seen: set[str] = set()
    accepted, quarantined = [], []
    for raw in raws:
        event, reason = decode_event(raw, seen)
        if event:
            accepted.append(event)
        else:
            quarantined.append({"raw": raw, "reason": reason})
    return accepted, quarantined
