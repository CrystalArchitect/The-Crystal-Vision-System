#!/usr/bin/env python3
"""Alive weave — run labeled buses and meter speech into the twin (Architecture S4).

Does not merge Songline into CVS. Does not auto-orchestrate without human gate.
Optional ``--sat`` wraps the hub opening intent through SAT wrap_turn (veto grammar).

    python3 scripts/alive/weave.py
    python3 scripts/alive/weave.py --sat
    python3 scripts/alive/weave.py --topic "first water" --turns 2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TCV = ROOT / "archive/TheCrystalVision"
STAR_ROOT = ROOT / "archive/TerAustralis-Incognita-Code/core/crystal-core"
SAT_ROOT = ROOT / "archive/Synthetic-Affect-Theory"
WEAVE_H3 = "weave.hub"
SIGNAL_CLASS = "signal.bus_message"


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _event_id(bus: str, entry: dict) -> str:
    raw = f"{bus}:{entry.get('id', '')}:{entry.get('from', '')}:{entry.get('cycle', 0)}"
    return "bus-" + hashlib.sha256(raw.encode()).hexdigest()[:16]


def transcript_to_events(bus_name: str, transcript: list[dict]) -> list[dict]:
    """Map delivered bus speech → crystal.twin.event/1 signal.bus_message."""
    events = []
    for e in transcript:
        if not e.get("delivered"):
            continue
        if e.get("cycle", 0) < 0:
            continue  # closing / red-button notices still count if delivered+cycle>=0
        sender = e.get("from") or e.get("sender") or "unknown"
        events.append({
            "schema": "crystal.twin.event/1",
            "event_id": _event_id(bus_name, e),
            "source_did": f"did:crystal:bus:{bus_name}:{sender}",
            "h3": WEAVE_H3,
            "class": SIGNAL_CLASS,
            "value": "1",
            "unit": "count",
            "observed_at": _iso(float(e.get("ts") or datetime.now(tz=timezone.utc).timestamp())),
            "raw_ref": f"layer:{e.get('layer', '')}|to:{e.get('to', '')}",
        })
    return events


def _sat_allow(intent: str = "reply") -> tuple[bool, dict]:
    """Gate the hub turn through SAT wrap_turn (same shape as SAT tests)."""
    sys.path.insert(0, str(SAT_ROOT))
    try:
        from core.host import wrap_turn
        from core.local_state import steady

        live = {"active_durs": [], "exit_intent": False, "isolated": False, "link_trusted": True}
        verdict = wrap_turn(live, steady(), {"id": "weave-hub", "intent": intent})
        return bool(verdict.get("model_called", verdict.get("allowed", True))), dict(verdict)
    except Exception as exc:  # noqa: BLE001
        return False, {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        if str(SAT_ROOT) in sys.path:
            sys.path.remove(str(SAT_ROOT))


def _run_songline(topic: str, turns: int) -> list[dict]:
    sys.path.insert(0, str(TCV))
    try:
        from clementine.bridge.agents import ClementineHub, EchoAgent, SevenSistersAgent
        from clementine.bridge.bus import SonglineBus
        bus = SonglineBus(ClementineHub(), [EchoAgent(), SevenSistersAgent()])
        return bus.run(topic, turns)
    finally:
        if str(TCV) in sys.path:
            sys.path.remove(str(TCV))


def _run_starline(topic: str, turns: int) -> list[dict]:
    sys.path.insert(0, str(STAR_ROOT))
    try:
        from bus.agents import BusHub, EchoAgent, SevenSistersAgent
        from bus.bus import StarlineWeaver
        weaver = StarlineWeaver(BusHub(), [EchoAgent(), SevenSistersAgent()])
        return weaver.run(topic, turns)
    finally:
        if str(STAR_ROOT) in sys.path:
            sys.path.remove(str(STAR_ROOT))


def _meter(events: list[dict], db_path: Path) -> dict:
    sys.path.insert(0, str(TCV))
    try:
        from services.decode import decode_batch
        from services.ingest import connect, ingest_events
        from services.twin import flows
        accepted, quarantined = decode_batch(events)
        conn = connect(db_path)
        written = ingest_events(conn, accepted)
        report = flows(conn, h3=WEAVE_H3, cls=SIGNAL_CLASS)
        conn.close()
        return {
            "accepted": len(accepted),
            "quarantined": len(quarantined),
            "quarantine_reasons": [q.get("reason") for q in quarantined[:5]],
            "written": written,
            "twin_flows": report,
        }
    finally:
        if str(TCV) in sys.path:
            sys.path.remove(str(TCV))


def main() -> int:
    parser = argparse.ArgumentParser(description="Alive weave — bus → twin (S4)")
    parser.add_argument("--topic", default="all alive — one but many")
    parser.add_argument("--turns", type=int, default=2)
    parser.add_argument("--sat", action="store_true", help="Gate hub turn through SAT wrap_turn")
    parser.add_argument("--db", type=Path, default=None, help="Twin SQLite path (default: temp)")
    args = parser.parse_args()

    print("Alive weave — Songline + Starline → twin")
    print(f"Topic: {args.topic!r} · turns={args.turns}")
    print("")

    if args.sat:
        allowed, verdict = _sat_allow("reply")
        print(f"SAT wrap_turn: allowed={allowed} inspect={json.dumps(verdict, default=str)[:200]}")
        if not allowed:
            print("HALT — SAT vetoed the weave turn (human/authority gate).")
            return 2

    song = _run_songline(args.topic, args.turns)
    star = _run_starline(args.topic, args.turns)
    print(f"Songline delivered: {sum(1 for e in song if e.get('delivered'))}/{len(song)}")
    print(f"Starline delivered: {sum(1 for e in star if e.get('delivered'))}/{len(star)}")

    events = transcript_to_events("songline", song) + transcript_to_events("starline", star)
    db = args.db or Path(tempfile.mkdtemp(prefix="alive-weave-")) / "twin.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    meter = _meter(events, db)

    print("")
    print(f"S4 meter → {db}")
    print(f"  events={len(events)} accepted={meter['accepted']} "
          f"quarantined={meter['quarantined']} written={meter['written']}")
    if meter["quarantine_reasons"]:
        print(f"  quarantine sample: {meter['quarantine_reasons']}")
    print(f"  twin flows @ {WEAVE_H3}/{SIGNAL_CLASS}: {meter['twin_flows']}")

    if meter["accepted"] == 0 or meter["written"] == 0:
        print("FAIL — twin received no bus signal events")
        return 1
    if meter["quarantined"]:
        print("WARN — some events quarantined (visible, not silent)")
    print("")
    print("PASS — weave spoke; twin recorded decoded signal.bus_message events.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
