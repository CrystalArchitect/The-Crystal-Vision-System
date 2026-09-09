"""TWIN — flow queries over the twin store.

The twin only ever reports what passed decode. That is the whole point.
"""

from __future__ import annotations

import sqlite3


def flows(conn: sqlite3.Connection, h3: str = "", cls: str = "") -> list[dict]:
    """Aggregate flows, optionally filtered by h3 prefix and/or class."""
    where, params = [], []
    if h3:
        where.append("h3 LIKE ?")
        params.append(h3 + "%")
    if cls:
        where.append("class = ?")
        params.append(cls)
    clause = ("WHERE " + " AND ".join(where)) if where else ""
    rows = conn.execute(
        f"""SELECT h3, class, unit, COUNT(*), SUM(value), MIN(value), MAX(value),
                   MIN(observed_at), MAX(observed_at)
            FROM twin_events {clause}
            GROUP BY h3, class ORDER BY h3, class""",
        params,
    ).fetchall()
    return [
        {
            "h3": r[0], "class": r[1], "unit": r[2], "events": r[3],
            "total": round(r[4], 6), "min": r[5], "max": r[6],
            "first_observed": r[7], "last_observed": r[8],
        }
        for r in rows
    ]
