# CrystalBridge

MCP consent gate for guest access to companion memory.

See repository docs for full architecture, and
`docs/CONSENT-GATE-SPEC.md` for the gate's specification.

## Config

Guest grants in `profiles/<name>/bridge_config.json`.

Add a guest by adding a key under `guests`. Nothing is granted by default.
Each grant carries two independent consent axes: `read_scope`/`write_scope`
name the visibility classes (`private`/`shared`), and
`read_types`/`write_types` name the memory layers.

### Durable revoke / reinstate

```bash
python3 -m crystalcore --revoke claude --reason "session ended"
python3 -m crystalcore --reinstate claude --reason "restored"
```

Appends to `profiles/<name>/revocations.jsonl` (append-only, latest record
per guest wins). Takes effect on the guest's next request — no restart —
and survives every restart. Reinstate restores the standing grant; it mints
no token. A ledger that cannot be read refuses **all** guests until
repaired: a gate that cannot know who is revoked must not guess. Every
revocation and reinstatement is mirrored into the audit log.

### Memory type-gates

`read_types` / `write_types` are subsets of `{episodic, semantic,
reflective}` (summaries / notes+facts / reflections — the documented
taxonomy; the memory structure *is* the taxonomy). Working memory (the live
conversation) is never guest-readable and deliberately not grantable.
Missing type fields load as `[]` and refuse with a reason that says what to
add (breaking, fail-closed). Unknown type names stop startup.

Today only the semantic layer (notes and facts) is actually served to
guests, because it is the only layer with per-entry visibility consent;
episodic and reflective grants gain content only when per-entry sharing
reaches those layers — until then a grant for an unserved layer refuses
honestly rather than returning silence. The default profile grants the
full guests all three read types (forward consent) and semantic write;
`restricted` reads semantic only.

### The observable ask

`pending.jsonl` records each ask *before* evaluation (`status: received`),
so a request is on disk even when fulfilment never happens — and an ask
that cannot be recorded refuses rather than acting unobservably. The audit
decision line and the refusal payload a guest sees carry the same
`request_id`, joining ask to answer. `interactive_approval` remains a
reserved hook for a future hold-for-approval mode; the pending record's
`status` field is where that mode will live.

## Tools

| Tool | What it does | Touches the companion's memory? |
|---|---|---|
| `status` | Reports the calling guest's identity, granted tools and memory types | No |
| `recall` | Returns what the companion remembers, optionally filtered by a query (wraps the existing `_memory_block`) | Read-only, semantic layer |
| `teach` | Tells the companion something to remember permanently (wraps the existing `remember`) | Writes, semantic layer |
| `message` | Leaves a note for the human | No — written to `profiles/<name>/messages.jsonl`, deliberately **not** folded into the companion's memory automatically |

`message` is kept separate from `teach` on purpose: a note left by a guest
AI shouldn't silently become one of the companion's permanent memories
without a human choosing that.

## Audit trail

Every decision — allowed or refused — is appended to
`profiles/<name>/audit.jsonl`, one JSON object per line: timestamp, guest,
tool, arguments (long text fields truncated), decision, reason, and the
`request_id` of the ask it answers. Guest messages land in the separate
`profiles/<name>/messages.jsonl`. None of these runtime files is committed
to git (see `.gitignore`) — they're real conversation content, not config.

## Prove it

```bash
cd core && python3 -m crystalcore.selftest
```

24 checks; the gate keeps five doors — revocation, approval, provenance,
permission, scope (visibility × memory types).
