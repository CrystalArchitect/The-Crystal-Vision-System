# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for the Decode → Ingest → Twin spine.

    python3 -m services.selftest
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from .decode import decode_batch, decode_event
from .ingest import connect, ingest_events
from .twin import flows


def _event(**kw) -> dict:
    base = {
        "schema": "crystal.twin.event/1", "event_id": "e1",
        "source_did": "did:crystal:hub-budapest", "h3": "8abe100",
        "class": "energy.kwh", "value": "12.4", "unit": "kWh",
        "observed_at": "2026-07-17T10:00:00Z",
    }
    base.update(kw)
    return base


def test_decode_accepts_and_normalizes():
    event, reason = decode_event(_event(value="1200", unit="Wh"))
    assert reason == "" and event is not None
    assert event["value"] == 1.2 and event["unit"] == "kWh", "Wh must normalize to kWh"


def test_decode_quarantines_bad_input():
    cases = [
        (_event(schema="wrong/9"), "schema"),
        (_event(value="lots"), "not numeric"),
        (_event(unit="bananas"), "unit"),
        (_event(observed_at="yesterday"), "ISO"),
        ({k: v for k, v in _event().items() if k != "h3"}, "missing"),
        (_event(**{"class": "weather.control"}), "unknown domain"),
    ]
    for raw, expect in cases:
        event, reason = decode_event(raw)
        assert event is None and expect.lower() in reason.lower(), (raw, reason)


def test_replay_is_rejected_in_batch():
    accepted, quarantined = decode_batch([_event(), _event()])
    assert len(accepted) == 1 and len(quarantined) == 1
    assert "replay" in quarantined[0]["reason"]


def test_ingest_is_idempotent_and_twin_aggregates():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "twin.db"
        conn = connect(db)
        events, _ = decode_batch([
            _event(event_id="a", value="10"),
            _event(event_id="b", value="5"),
            _event(event_id="c", **{"class": "mobility.checkin"}, value="1", unit="count"),
        ])
        assert ingest_events(conn, events) == 3
        assert ingest_events(conn, events) == 0, "second ingest must write nothing"
        result = flows(conn, h3="8abe", cls="energy.kwh")
        assert len(result) == 1 and result[0]["events"] == 2 and result[0]["total"] == 15.0
        assert len(flows(conn)) == 2
        conn.close()


def main() -> int:
    tests = [
        test_decode_accepts_and_normalizes,
        test_decode_quarantines_bad_input,
        test_replay_is_rejected_in_batch,
        test_ingest_is_idempotent_and_twin_aggregates,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. The twin only speaks decoded truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
