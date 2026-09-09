# Examples

Runnable demonstrations, curated. The best examples in this repo are the
demos the components already ship with — this page is the index; the code
stays with its component so the demos can't drift from what they
demonstrate.

> **Repository status:** the commands below run against the code tree,
> which is not in this repository — they will not run from a fresh clone.
> See
> [SystemMap: where the code actually lives](../docs/architecture/SystemMap.md#where-the-code-actually-lives).

| Watch it work | Command (from repo root) |
|---|---|
| Starline: pair, deny, grant, exchange, revoke, deny | `cd src/crystal-core && python3 -m consent_transport.run demo` |
| RDP: every precedence tier decides, every verdict recorded | `cd src/crystal-core && python3 -m rdp.run demo` |
| RDP witnessing a real Weaver matrix run | `cd src/crystal-core && python3 -m rdp.run matrix-demo` |
| The pipeline over sample events | `cd src/crystal-core && python3 -m services.pipeline services/sample-events/budapest.jsonl` |
| Clementine, the sovereign companion | `cd src/apps/clementine && python3 clementine.py` |
| The mythos as a terminal | `python3 src/crystalcore-os/crystalcore_os.py` |

Recorded transcripts of the Starline Weaver in action:
`src/crystal-core/clementine/transcripts/` (that folder is also where the
bridge writes new session transcripts at runtime).

`tutorials/` and `sample-projects/` are the standard shelves here when
step-by-step material gets written; they're created with their first
content, not before.
