# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""INGEST — write decoded events into the twin store (SQLite).

Partitioned by (h3, class); idempotent on event_id, so replays at the
storage layer are also harmless.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent / "twin.db"

DDL = """
CREATE TABLE IF NOT EXISTS twin_events (
    event_id    TEXT PRIMARY KEY,
    source_did  TEXT NOT NULL,
    h3          TEXT NOT NULL,
    class       TEXT NOT NULL,
    value       REAL NOT NULL,
    unit        TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    raw_ref     TEXT NOT NULL DEFAULT '',
    ingested_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_twin_partition ON twin_events (h3, class, observed_at);
"""


def connect(db_path: Path | str = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.executescript(DDL)
    return conn


def ingest_events(conn: sqlite3.Connection, events: list[dict]) -> int:
    """Insert decoded events; return how many were newly stored."""
    now = time.time()
    written = 0
    with conn:
        for e in events:
            cur = conn.execute(
                "INSERT OR IGNORE INTO twin_events "
                "(event_id, source_did, h3, class, value, unit, observed_at, raw_ref, ingested_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (e["event_id"], e["source_did"], e["h3"], e["class"], e["value"],
                 e["unit"], e["observed_at"], e.get("raw_ref", ""), now),
            )
            written += cur.rowcount
    return written
