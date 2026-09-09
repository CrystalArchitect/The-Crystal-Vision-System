"""
CrystalCore audit: the continuity record.

Every call Clementine makes to a model — allowed or refused — lands here as
one line of JSON, and each line carries the SHA-256 of the line before it.
That chaining is the whole point: an entry cannot be quietly altered and a
line cannot be quietly removed, because either breaks the chain and
`verify()` says so.

It lives beside memory.json in the folder the human owns, because it is
their record, not the application's. Plain text, readable, deletable.

This is deliberately not a debug log. It answers one question — *what left
this machine, when, and did I agree to it* — and nothing else. It stores
sizes and destinations, never the content of what was said.
"""

from __future__ import annotations

import json
from datetime import datetime
from hashlib import sha256
from pathlib import Path

GENESIS = "genesis"


class AuditLog:
    """Append-only, hash-chained record of model calls."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    # ---------- writing ----------

    def record(self, service: str, destination: str, outcome: str,
               **detail) -> str:
        """Append one entry and return its hash.

        service     — what was asked for: "chat", "embed", "summary", ...
        destination — where it was going: "local" or the remote host
        outcome     — "allowed" or "refused"
        detail      — small facts only (sizes, model name, reason). Never
                      the text of a conversation.
        """
        body = {
            "at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "service": service,
            "destination": destination,
            "outcome": outcome,
            **detail,
            "prev": self.head(),
        }
        digest = sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({**body, "hash": digest}) + "\n")
        return digest

    # ---------- reading ----------

    def head(self) -> str:
        """Hash of the most recent entry, or "genesis" if there is none."""
        entries = self.entries()
        return entries[-1]["hash"] if entries else GENESIS

    def entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    # A corrupt line is itself evidence; verify() reports it.
                    out.append({"hash": "", "prev": "", "_unparsable": line[:80]})
        return out

    # ---------- proving ----------

    def verify(self) -> tuple[bool, list[str]]:
        """Recompute the chain. Returns (intact, problems)."""
        problems: list[str] = []
        prev = GENESIS
        entries = self.entries()

        for i, entry in enumerate(entries):
            if "_unparsable" in entry:
                problems.append(f"entry {i}: not valid JSON")
                return False, problems

            body = {k: v for k, v in entry.items() if k != "hash"}
            expected = sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()

            if entry.get("prev") != prev:
                problems.append(
                    f"entry {i}: chain break — expected prev {prev[:12]}, "
                    f"found {str(entry.get('prev'))[:12]}"
                )
            if entry.get("hash") != expected:
                problems.append(f"entry {i}: contents altered after writing")

            prev = entry.get("hash", "")

        return (not problems), problems

    # ---------- witnessing ----------
    #
    # verify() catches an entry altered after writing, an entry cut from the
    # middle, and reordering. It cannot catch entries removed from the *end*:
    # a chain with its tail cut off is a shorter chain that verifies
    # perfectly. Nothing inside a file can prove what is missing from the
    # end of it.
    #
    # The usual answer is an anchor outside the file — publish the head
    # somewhere the machine cannot rewrite. Here that answer is worse than
    # the problem: sending the head anywhere is a network call the human did
    # not choose, and it leaks that they use this, how often, and when. The
    # gate exists to refuse exactly that.
    #
    # So the anchor is the human's own backup. An export carries the head and
    # the count at the moment it was taken, and any later log can be checked
    # against it. It never leaves the machine, it sits in their hands rather
    # than a third party's, and its limit is exact: it witnesses everything
    # up to the backup and says nothing about what came after.

    def witness(self) -> dict:
        """What a backup taken now can testify to later."""
        return {"head": self.head(), "count": len(self.entries())}

    def check_witness(self, witness: dict) -> tuple[bool | None, str]:
        """Does this log still agree with a backup's account of it?

        Returns (verdict, sentence). None means the question does not apply
        — an empty or absent witness testifies to nothing, which is not the
        same as testifying that nothing is wrong.
        """
        head = (witness or {}).get("head") or ""
        count = (witness or {}).get("count") or 0
        if not head or head == GENESIS or not count:
            return None, ("That backup was taken before any calls were "
                          "recorded, so it has nothing to attest to.")

        hashes = [e.get("hash") for e in self.entries()]
        if head not in hashes:
            return False, (
                f"The entry this backup witnessed is no longer in the "
                f"record. It saw {count} calls, ending with "
                f"{head[:12]}…, and that entry is gone.")

        at = hashes.index(head) + 1
        if at != count:
            return False, (
                f"This backup saw that entry as number {count}; it is now "
                f"number {at}. {count - at} earlier entries have been "
                f"removed." if at < count else
                f"This backup saw that entry as number {count}; it is now "
                f"number {at}. Entries have been inserted before it.")

        return True, (
            f"The record still agrees with this backup: the {count} calls it "
            f"witnessed are all present and in the same order. Anything "
            f"recorded after the backup is outside what it can vouch for.")

    def summary(self) -> str:
        intact, problems = self.verify()
        n = len(self.entries())
        if intact:
            return f"chain intact: {n} entries, head {self.head()[:12]}"
        return f"chain BROKEN: {n} entries, {len(problems)} problem(s)"
