# Consent Token Spec v0.1

**Label: Vision — new design proposal, not implemented as code.** This
document defines a schema and state machine that do not exist anywhere
in this project yet. It is written for [90-Day Public Roadmap
deliverable #2](../../../memory/projects/90-Day-Roadmap/PLAN.md)
("Consent Token Spec v0.1: `consent_token.json` + state diagram +
2-min kill-switch demo failing closed"). This document delivers the
**spec** — schema and state diagram. It does **not** deliver the demo;
see "What this document does not deliver" below.

## What already exists (grounding, not invention)

Per [`ARCHITECTURE.md`](ARCHITECTURE.md) and the [2026-07-23
architecture survey](../../reviews/2026-07-23-architecture-survey.md),
two real components already do the work this token would formalize —
both live in `TerAustralis-Incognita-Code`, not this repository:

- **CrystalBridge** (`src/crystalcore/`) — a fail-closed MCP server:
  guest AIs (`claude`, `grok`, `cursor`) reach Clementine only through a
  `ConsentGate` with scoped tools (`status`, `recall`, `teach`,
  `message`). **Known gap, not repeated as settled:** the 2026-07-23
  survey found the module's own docstring claims four checks (approval
  · permission · scope · provenance) while the code implements exactly
  two, with zero test coverage. This spec assumes all four checks as
  the *design intent* CrystalBridge itself states, not as a claim that
  all four are currently enforced in code.
- **The Starline Weaver** (`clementine/bridge` in `src/crystal-core/`)
  — a labeled multi-agent message bus with a real, tested kill switch:
  7/7 self-tests passing per the same survey. This is the one piece of
  "kill switch" that is genuinely Built today, not proposed here.

This spec's job is to give both of these a shared, inspectable token
format — something neither currently has on its own terms (the survey
found no `consent_token`-shaped artifact anywhere in the codebase).

## `consent_token.json` — v0.1 schema

```json
{
  "token_id": "ct_2026-09-03T00:00:00Z_a1b2c3",
  "schema_version": "0.1",
  "issuer": "clementine-core",
  "subject": {
    "guest_id": "grok",
    "guest_kind": "ai-agent"
  },
  "scope": {
    "tools": ["status", "recall"],
    "denied_tools": ["teach", "message"]
  },
  "permission_level": "read-only",
  "provenance": {
    "requested_by": "operator:crystal",
    "request_ref": "session_abc123",
    "chain_ref": "rdp:hash-chain:0x..."
  },
  "state": "active",
  "issued_at": "2026-09-03T00:00:00Z",
  "expires_at": "2026-09-03T01:00:00Z",
  "revoked_at": null,
  "revocation_reason": null
}
```

**Field notes:**

- `subject.guest_kind` is deliberately open (`"ai-agent"` today) so a
  future non-AI caller (a script, a second Clementine instance) doesn't
  need a new token shape — see `OPEN-QUESTIONS.md`'s "Multi-instance
  Clementine" entry, still undesigned.
- `scope.denied_tools` is explicit, not merely the complement of
  `scope.tools` — a fail-closed gate should be able to state a denial
  even if the tool list changes later, per the Constitution's
  fail-closed principle already claimed for CrystalBridge.
- `provenance.chain_ref` points at the real RDP hash-chained audit
  kernel (31/31 self-tests per the survey) rather than reinventing
  audit logging — this token format assumes RDP as its audit backend,
  it doesn't replace it.

## State diagram

```
                 ┌──────────┐
   issue()       │          │
  ───────────────▶  issued  │
                 │          │
                 └────┬─────┘
                      │ activate()
                      ▼
                 ┌──────────┐        expire (t > expires_at)
                 │          ├─────────────────────────────┐
                 │  active  │                              │
                 │          ├──────────────┐               │
                 └────┬─────┘              │               │
                      │                    │               │
        kill_switch() │      revoke()      │               │
                      ▼                    ▼               ▼
                 ┌──────────┐        ┌──────────┐    ┌──────────┐
                 │  killed  │        │ revoked  │    │ expired  │
                 └──────────┘        └──────────┘    └──────────┘
```

- **`killed`** is reached only via `kill_switch()` — a distinct
  terminal state from `revoked`, so a public kill-switch demo can prove
  it hit *this* path specifically, not an ordinary revocation.
- All three terminal states (`killed`, `revoked`, `expired`) deny every
  tool call — a token is checked for `state == "active"` before its
  `scope` is consulted at all. This is what "failing closed" means
  concretely: an unrecognized or terminal state denies by default,
  it does not fall through to an allow.
- No transition leads back to `active` from a terminal state. A killed
  or revoked guest needs a *new* token via `issue()`, not a reactivation
  path — this is a deliberate asymmetry: killing should cost something
  to undo.

## What the 2-minute kill-switch demo would need to show

Per the roadmap's success metric ("Public Gist/repo + Loom. One
external person can read/run it"):

1. A guest AI (e.g. `grok`) holding an `active` token successfully
   calls a granted tool (e.g. `status`).
2. The operator triggers `kill_switch()` on that token.
3. The same guest AI, same tool call, is denied — shown failing
   *closed* (an explicit deny response), not timing out or erroring
   ambiguously.
4. The token's `state` field, inspected directly, reads `"killed"`.

## What this document does not deliver

- **No running code.** This repository holds no application code by
  design ([`SystemMap.md`](../SystemMap.md#where-the-code-actually-lives));
  a `consent_token.json` implementation, the actual kill-switch wiring,
  and the 2-minute demo recording all belong in
  `TerAustralis-Incognita-Code`, which is outside this session's repo
  scope.
- **No fix to CrystalBridge's known 2-of-4 check gap.** That's a real,
  logged discrepancy in a different repository's code, not something a
  documentation session resolves by writing a spec.
- **No claim that this schema is final.** It's v0.1 — a starting shape
  for review, not a frozen interface.

## Next step (not this document)

Implementing `consent_token.json` issuance/validation against this
schema, wiring `kill_switch()` to the Starline Weaver's existing tested
kill switch, and recording the 2-minute Loom demo — all in
`TerAustralis-Incognita-Code`.

*Non Solus.*
