#!/usr/bin/env python3
"""Prove what the consent gate does, including what it will not do.

Run it: python3 verify_consent.py

Every case here is one the gate is supposed to get right. The protected-source
cases are the ones worth re-running after any change, because they encode a
rule this project does not have standing to relax — see PROTECTED_SOURCES in
crystalcore/consent.py.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crystalcore.audit import AuditLog                      # noqa: E402
from crystalcore.consent import (ConsentGate, ConsentRefused,  # noqa: E402
                                 Request, Verdict, protected_reason)

LOCAL = "http://127.0.0.1:11434/api/chat"
GOOGLE = "https://aiplatform.googleapis.com/mcp/generate"

passed = failed = 0


def check(label: str, got, want) -> None:
    global passed, failed
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"          got  {got!r}\n          want {want!r}")
    passed, failed = passed + ok, failed + (not ok)


always_yes = lambda r: Verdict(True, "test says yes", remember=True)

print("\nLocal calls proceed, remote calls need a yes")
gate = ConsentGate(asker=None)
check("local is allowed", gate.check(Request("chat", LOCAL, "llama3.1:8b")).approved, True)
check("remote with no asker is refused",
      gate.check(Request("chat", GOOGLE, "gemini")).approved, False)

gate = ConsentGate(asker=always_yes)
check("remote with a yes is allowed",
      gate.check(Request("chat", GOOGLE, "gemini")).approved, True)
check("second call reuses the session yes",
      gate.check(Request("chat", GOOGLE, "gemini")).reason, "approved earlier this session")

print("\nProtected sources: refused everywhere, by everyone")
gate = ConsentGate(asker=always_yes)          # an asker that always says yes
for where, url in (("remote", GOOGLE), ("local", LOCAL)):
    v = gate.check(Request("chat", url, "m", source="mythos/content/RED-DUST-AXIS.md"))
    check(f"mythos/ refused even {where}, even with a yes-man asker", v.approved, False)
    check(f"  and says why ({where})", "custodial" in v.reason, True)

v = gate.check(Request("chat", GOOGLE, "m", source="/home/u/repo/mythos/art/x.jpeg"))
check("absolute paths are caught too", v.approved, False)
check("non-mythos source is unaffected",
      gate.check(Request("chat", LOCAL, "m", source="notes/todo.md")).approved, True)
check("no source at all is unaffected",
      gate.check(Request("chat", LOCAL, "m")).approved, True)
check("a session yes cannot be reused to smuggle mythos/",
      gate.check(Request("chat", GOOGLE, "m", source="mythos/x.md")).approved, False)

print("\nprotected_reason() in isolation")
check("mythos/ prefix", protected_reason("mythos/a.md") is not None, True)
check("mythos nested", protected_reason("x/mythos/a.md") is not None, True)
check("./mythos", protected_reason("./mythos/a.md") is not None, True)
check("windows separators", protected_reason(r"repo\mythos\a.md") is not None, True)
check("mythosaurus is not mythos/", protected_reason("mythosaurus/a.md"), None)
check("None source", protected_reason(None), None)

print("\nRefusals reach the audit log, with the path and without the content")
with tempfile.TemporaryDirectory() as tmp:
    audit = AuditLog(Path(tmp) / "audit.jsonl")
    gate = ConsentGate(audit=audit, asker=always_yes)
    try:
        gate.require(Request("chat", GOOGLE, "gemini", chars=4096,
                             source="mythos/content/APOCRYPHON.md"))
        check("require() raised", False, True)
    except ConsentRefused as exc:
        check("require() raised ConsentRefused", True, True)
        check("  reason names the rule", "custodial" in exc.reason, True)

    entries = [ln for ln in (Path(tmp) / "audit.jsonl").read_text().splitlines() if ln]
    check("one entry written", len(entries), 1)
    entry = entries[0]
    check("recorded as refused", '"outcome": "refused"' in entry, True)
    check("records the source path", "APOCRYPHON" in entry, True)
    check("records the size", '"chars": 4096' in entry, True)
    ok, problems = audit.verify()
    check("chain still verifies", ok, True)

print(f"\n{passed} passed, {failed} failed\n")
sys.exit(1 if failed else 0)
