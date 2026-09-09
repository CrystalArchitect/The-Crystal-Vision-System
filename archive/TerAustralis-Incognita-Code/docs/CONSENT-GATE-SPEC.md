# ConsentGate: Scope and Provenance — Design Spec

Status: **implemented and enforced**, 2026-08-12. All five checks live in
`core/crystalcore/gate.py` and are covered by `crystalcore/selftest.py`
(`cd core && python3 -m crystalcore.selftest`). This document began as a
draft argued with the maintainer before anything was built; it is kept as
the record of what was decided and why, and has been moved to past tense
where it once described a system that did not yet exist. The three
"Decisions" at the foot were taken — see that section. Where a section
still describes a "hole", it is a hole this spec **closed**; each says so.

## Why this was built

When this spec was written, `core/crystalcore/gate.py` enforced two checks,
fail-closed: is the guest approved at all, and is it approved for this
specific tool. Both worked and both were tested. The other two checks —
scope and provenance — were documented as intended in
`vision/site/src/content/ARCHITECTURE.md` but *not implemented*: no spec
for what either should concretely mean had survived the loss of the
original design docs. This document wrote that spec, and both checks (plus
a memory-type dimension and durable revocation) are now enforced — the gate
keeps five doors.

As of 2026-07-31 the public Technical Brief
(proposal.teraustralis.com.au/05-technical-brief.html) states that
CrystalCore's contribution is "consent as an enforced runtime primitive
rather than a privacy posture." Approval plus a tool allowlist is ordinary
authorisation; any RBAC system has it. Scope and provenance are the two
checks that make the public claim true. Under the Incognita Rule the gap
had to resolve one of two ways — build them, or amend the claim. It was
resolved by building: this spec specified the two checks, and the gate now
enforces them.

## The two holes this closed (the state before)

Both holes below described `gate.py` *before* this spec was built. Each is
now closed; the closing mechanism is named after it.

**Hole 1 — identity was self-asserted.** The bridge reads guest identity
from the `CRYSTALBRIDGE_GUEST` environment variable
(`core/crystalcore/bridge.py`, `main()`). Whoever launches the process
types the name, and nothing distinguished Claude launched by the
maintainer from any process that set `CRYSTALBRIDGE_GUEST=claude`.
**Closed by provenance:** the name still comes from the environment, but a
guest must now also present a secret whose SHA-256 matches the stored
`token_hash`, compared in constant time (`gate.py`, `hmac.compare_digest`).
A free name without the minted token no longer reaches anything.

**Hole 2 — `recall` reached everything.** Memory is a single store per
profile (`memory.json`), and an approved guest's `recall` ran
`_memory_block(query)` over the whole of it — including memories formed in
private conversation that were never addressed to any guest. Consent to
*talk to* the companion was consent to *read its life*. **Closed by
scope:** `recall` now filters to the guest's `read_scope` classes before
semantic search runs, and private-by-default means an unreviewed memory is
invisible to every guest.

## Definitions

### Scope

> **Scope is consent bounded by what a grant may touch, not merely which
> tool it may call.** Concretely: memories carry a visibility class, and a
> grant names the classes it may read and the classes it may write into.

Mechanism:

- Every memory entry gains a `visibility` field. Two classes at first,
  deliberately no more: `private` (default for everything the companion
  learns in conversation with its human) and `shared` (explicitly marked
  by the human, or taught by a guest through the bridge).
- `GuestGrant` gains `read_scope: list[str]` and `write_scope: list[str]`
  (class names).
- `recall` filters the store to classes in the guest's `read_scope`
  *before* semantic search runs — not after, so nothing outside scope can
  influence even the shape of a result.
- `teach` writes into exactly one class, the first entry of `write_scope`;
  a guest is never able to write `private` memories.
- A grant with an empty or absent scope list can read/write **nothing**
  beyond `status`. Fail-closed: absence of scope is absence of consent,
  not legacy full access.

What scope is *not*, in this design: per-tool argument pattern matching
(brittle, and semantic recall makes argument filtering meaningless — the
query isn't where the exposure happens, the store is).

### Provenance

> **Provenance is evidence, checked at execution time, that a request
> actually comes from the party the grant names — and refusal when that
> evidence cannot be established.** Unverifiable origin is treated exactly
> like absent consent.

Mechanism (v1, honest about its limits):

- Each guest entry in `bridge_config.json` gains a `token_hash` (SHA-256).
  The maintainer mints a per-guest secret once (helper command:
  `python -m crystalcore.bridge --mint-token <guest>`), puts the hash in
  the config, and gives the secret to that guest's launcher configuration
  only.
- The bridge reads `CRYSTALBRIDGE_TOKEN` alongside `CRYSTALBRIDGE_GUEST`.
  `ConsentGate.check()` verifies the token against the stored hash after
  revocation and approval, before permission. No token, wrong token, or
  no stored hash → refuse, with a distinct audit decision
  (`refuse-provenance`). Approval runs first because there is no stored
  hash to compare without a grant.
- The audit record (`audit.jsonl`) gains a `provenance` block: whether the
  token verified, plus the transport (`stdio`) — so the append-only log
  can answer "who was that really?" after the fact.

This is launcher authentication, not cryptographic identity of a remote
model — a static secret proves possession of the secret, nothing more. It
is stated as exactly that. The upgrade path (per-session challenge,
signed requests over the mesh when a real transport exists) is noted in
the fail-safe tie-in below and left unbuilt until the transport it would
authenticate exists. Claiming more now would be the overclaim this
project's own rules forbid.

**Fail-safe tie-in.** The First Principles define fail-safe as local
isolation. Provenance is where that becomes enforceable at the gate: a
request whose origin cannot be established *at the moment of execution*
refuses — it does not degrade to the two-check path, and there is no
"assume the last known identity" fallback. When a future transport is
intermittent, this is the check that makes link loss produce silence
instead of trust.

## Check order

The order below is the order `gate.py` runs, pinned by
`crystalcore/selftest.py`. An earlier draft of this section put
provenance first and omitted revocation; that draft is superseded
(reconciled 2026-08-13 to the code, not the other way around).

Ask-record (`pending.jsonl`) is written *before* any door. It is not a
sixth door — the recorder failing, not consent deciding. A failed write
refuses (decision 4).

1. **Revocation** — has the human withdrawn this guest's consent?
   (`refuse-revoked`). The ledger is read on every check. Unreadable ⇒
   refuse all.
2. **Approval** — is the guest approved at all? (`refuse`)
3. **Provenance** — does the presented token prove this is the named
   guest? (`refuse-provenance`). Approval runs first because there is
   no `token_hash` to compare without a grant. Origin that cannot be
   established still refuses; there is no fallback to the later checks.
4. **Permission** — may it call this tool? (`refuse`)
5. **Scope** — applied after `check()` allowed, inside `require_scope()`,
   for tools that touch memory: visibility classes and memory types.
   (`refuse-scope` when a tool needs a scope or type the grant lacks)

`GateResult.check` names which stage refused, so audit and tests can
distinguish the five (plus `ask-record`).

## Migration and compatibility

- **Existing memories** predate the `visibility` field. On first load
  they are classed `private`. This is a behaviour change: guests that
  could previously recall everything will recall nothing until the human
  shares or re-teaches. That is the fail-closed default working as
  designed, and it is the single most user-visible consequence of this
  spec. A one-time interactive helper
  (`--review-memories`) lets the human mark entries `shared` in bulk.
- **Existing configs** lack `token_hash` and scope lists. Under this
  spec those guests refuse at provenance until tokens are minted — one
  command per guest, a one-time cost. The alternative (enforce only when
  configured) would make the public claim false for every default
  install, so it is rejected.
- `crystalcore_memory` / `lumina_memory` continuity guarantees are
  unaffected; `visibility` is an additive field with a defined default.

## Testing

The gate's suite is `crystalcore/selftest.py` — 23 plain-function tests
(`cd core && python3 -m crystalcore.selftest`), covering the five checks,
fail-closed defaults, the revocation ledger (runtime effect, restart
survival, reinstatement, corrupt-ledger refuse-all), the pending record
(written before evaluation, survives a mid-gate crash, request id joins
ask to answer), and the type dimension (empty types refuse, unserved
layers refuse honestly, unknown names stop startup, layers beyond
semantic never reach guests). An earlier revision of this section cited
suite counts that never matched the file; this one was corrected against
the real suite on 2026-08-12.

## Records beside the profile

- `audit.jsonl` — every decision, allow and refuse alike, append-only.
- `pending.jsonl` — every ask, written **before** evaluation, with a
  `request_id` the decision line repeats. The `status` field (`received`
  today) is where a future hold-for-approval mode will live.
- `revocations.jsonl` — consent withdrawal as an append-only ledger:
  `{timestamp, guest, action: revoke|reinstate, reason, by}`, latest
  record per guest wins, read on every check. Unreadable ⇒ refuse all.

## Decisions taken

All four were resolved with the maintainer and are reflected in the code
described above; each is kept here with its resolution.

1. **Two visibility classes or named partitions?** ~~This spec says two
   (`private`/`shared`) on the argument that classes you can't explain in
   one sentence won't be used correctly. Named partitions (e.g.
   per-project) are a compatible later extension.~~ **Decided, 2026-08-12:**
   two visibility classes stay, and the compatible extension arrived as a
   second, orthogonal dimension — memory *types* (`episodic` / `semantic`
   / `reflective`, the documented taxonomy), enforced at `require_scope`
   and empty-refuses like everything else. Only the semantic layer is
   served to guests today, because only it has per-entry visibility
   consent; a type grant for an unserved layer refuses with a reason
   rather than returning silence.
2. **Strict provenance from day one?** **Decided, yes** — all guests need
   minted tokens immediately, breaking zero-config guest setups once,
   deliberately. The alternative would have made enforcement optional and
   the public claim false by default. `gate.py` refuses at the provenance
   check when a guest has no `token_hash`, and again when the presented
   token does not match.
3. **Private-by-default migration?** **Decided, yes** — memories without a
   `visibility` field are read as `private`, so they are guest-invisible
   until the human shares or re-teaches them. It is the honest default and
   the disruptive one; it landed with the maintainer's explicit yes, not a
   quiet diff.
4. **Unrecordable ask — refuse or proceed?** **Decided, 2026-08-12: both,
   scoped — and the scope is the law.** Two surfaces record asks, and
   until this decision their comments stated opposite absolutes. The rule
   that resolves them: *an ask that cannot be recorded refuses where the
   record is part of the consent chain; it proceeds where the record is
   knock telemetry and the consent chain itself fails closed upstream.*
   - **Guest bridge (this spec, `gate.py`): refuses.** The `pending.jsonl`
     line is part of the consent chain — written before evaluation, its
     `request_id` repeated by the decision line and by the refusal payload
     the guest sees. A guest ask that cannot be recorded is an
     unobservable act by an agent holding write powers, so it does not
     happen. Pinned by `test_unrecordable_ask_refuses`.
   - **Starline (`consent_transport`): proceeds.** The ask-log is knock
     telemetry. Every element of the consent chain on that surface fails
     closed on its own: pairing and peer grant refuse unknowns, token
     verification refuses at presentation, and a spend that cannot be
     recorded denies the transfer (`record_use` failure ⇒ `denied`, per
     the four-bug fix). A telemetry write failure therefore costs one
     knock's visibility, never an unaccounted movement of data — and
     making it refuse would turn a full disk into a peer outage on a
     surface whose consent machinery still works.
   - **Documented limitation, not a promise:** the Starline ask-log
     carries no `request_id`, so an entry cannot be joined to the exact
     denial a peer saw. The guest side can; the peer side cannot, yet.
   The two code comments now cite this decision instead of stating
   rival absolutes.
