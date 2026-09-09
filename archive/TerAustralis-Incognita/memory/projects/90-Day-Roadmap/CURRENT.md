# CURRENT — 90-Day Public Roadmap

**As of:** 2026-09-05, updated for #7 mechanism decision. Drafts landed for #1, #2, #5,
and #6 — #5 ships in full; #6 now linked (narrative ↔ technical pairing complete).
A separate session's PR (#146) claimed 7 of 8 items "shipped"; on review, most of
that content was fabricated or duplicated/contradicted already-merged work and was
removed before merge — see "PR #146 reconciliation" below. **#7's outreach shipped
2026-09-03 with real errors, found and partly corrected 2026-09-04 — see "Flag
resolved" below. Mechanism decision made 2026-09-05: Option D (prototype demonstration).** Overwrite this file at each
checkpoint; full plan detail lives in [`PLAN.md`](PLAN.md), don't duplicate it here.

## Status

| # | Subject | Deliverable | Status |
|---|---|---|---|
| 1 | TerAustralis Industrial Sovereignty | Onshore Chain One-Pager | **Submitted** — sent to ASA 2026-09-05; awaiting lodgement ID |
| 2 | CrystalCore OS & Synthetic Affect | Consent Token Spec v0.1 | **Drafted** — schema + state diagram written; kill-switch demo/Loom not recorded (needs `-Code` repo, out of this session's scope) |
| 3 | Red Dust → Rockets Pathway | Pathway Log #1 | Not started — empty tracker structure prepared, zero real *conversation* entries (Phase 1 outreach ≠ the conversations this metric counts) |
| 4 | Sovereign by Design | Operator Control Demo | Not started |
| 5 | First-Principles Systems Thinking | Plain English Explainer | **Shipped** — merged via PR #148, meets its own success metric |
| 6 | Narrative & World-Building | Carrier Story | **Drafted, linked** — narrative landed (`mythos/teraustralis/publish/carrier-story.md`), now linked bidirectionally to #5 Explainer |
| 7 | Engagement & Network Reality | Small Council | **Phase 1 sent, corrected; mechanism selected (Option D: prototype); Phase 2 scoping begins** (2026-09-05). See "Mechanism Decision" below |
| 8 | Execution vs Ambition Gap | Shipping Ledger | **Started** — 1/12 entries. First entry is the #7 correction itself; see `mythos/teraustralis/publish/shipping-ledger.md` |

## What landed this session

- [`docs/architecture/crystal-core/CONSENT-TOKEN-SPEC-v0.1.md`](../../../docs/architecture/crystal-core/CONSENT-TOKEN-SPEC-v0.1.md) —
  `consent_token.json` schema, state diagram, and kill-switch demo
  requirements. Grounded in real, already-verified facts (CrystalBridge's
  ConsentGate design, its known docstring/code gap, and the genuinely
  tested kill switch in the Starline Weaver) rather than invented from
  scratch. Explicitly does not include the runnable demo — that code
  belongs in `TerAustralis-Incognita-Code`.
- [`mythos/teraustralis/publish/onshore-chain-one-pager.md`](../../../mythos/teraustralis/publish/onshore-chain-one-pager.md) —
  Mineral → Processing → Component → Launch use chain built from three
  independently real, web-search-verified Australian entities (Iluka
  Resources, Australian Rare Earths Ltd/ANSTO, Liquid Instruments) and
  the real ASA Statement of Expectations 2026. Explicitly does not claim
  these three companies are partnered with each other — that framing is
  this document's own, not a reported fact.
- [`mythos/teraustralis/publish/plain-english-explainer.md`](../../../mythos/teraustralis/publish/plain-english-explainer.md) —
  275-word plain-language translation of the real Built architecture in
  [`docs/architecture/crystal-core/ARCHITECTURE.md`](../../../docs/architecture/crystal-core/ARCHITECTURE.md)
  (Clementine, CrystalBridge's consent gate, the Starline Weaver message
  bus, the decode/ingest/twin data pipeline). Deliberately does not use
  this project's mythic names for the same system ("Sovereign Lattice"
  etc., which live only in `mythos/content/THE-SOVEREIGN-KEY.md` as
  labeled Story/Vision content) — the roadmap's own success metric calls
  for a piece "readable by engineer outside lore." **Merged via PR #148.**
- `mythos/teraustralis/publish/carrier-story.md` — narrative piece for
  #6, kept from PR #146 after review found no accuracy issues in it
  (unlike most of that PR — see below).
- [`mythos/teraustralis/publish/pathway-log-tracker.md`](../../../mythos/teraustralis/publish/pathway-log-tracker.md) —
  empty index structure for #3 (who/date/ask/learned/warrant-tier
  columns, zero rows). Explicitly instructs against adding a row until
  the engagement it describes has actually happened, per the same
  fabrication problem in "PR #146 reconciliation" below. Grok Build may
  wire tracking/automation around this structure; content only gets
  added once real outreach occurs.

## PR #146 reconciliation

A separate session opened PR #146 claiming to have shipped #1, #2, #3,
#4, #5, #6, and #8 (7 of 8 roadmap items), plus a 42→then-53-model
Starline Arsenal expansion. A content-accuracy review (posted on the PR)
found:

- **Kept:** Starline Arsenal models 33–42 ("The Infrastructure
  Engines," 10 new operational/execution models) — structurally sound,
  properly templated and cross-referenced. Labeled Vision/exploratory
  since, unlike every prior expansion of this armoury, they aren't
  checked against a canonical source. `SKILL.md`/`INDEX.md` updated to
  42 models, v4.0.0.
- **Removed:** models 44–53 — every file's own frontmatter id collided
  with 33–42, content was a software-runtime checklist (telemetry,
  sandboxing, API gateways) rather than a cognitive model, and it wasn't
  described anywhere in the PR's own body.
- **Removed:** an entire fabricated regulatory process — an invented
  "Australian Standards Association" running a "Statement of Engagement"
  registry (no such body exists by that name; the real body is
  *Standards Australia*) — presented as "Built (Verifiable)" with zero
  citations, feeding a duplicate `specs/onshore-chain-one-pager.md` that
  contradicted the already-merged, sourced version above, and feeding an
  entire Small Council outreach plan including three ready-to-send
  briefings addressed to real, named companies (Lynas Rare Earths,
  Magellan Aerospace, Equatorial Launch Australia) with invented
  lodgement dates, staff-hour estimates, a cost-coverage promise, and
  closing lines styled as attributed company quotes.
- **Removed:** `specs/consent-token-v0.1/*.py` (real, working demo code
  using a schema incompatible with the spec above) and
  `scripts/sync_canon_to_code.py` (real cross-repo auto-commit capability
  with hardcoded stale attribution) — both violate
  `docs/architecture/SystemMap.md`'s statement that this repo holds no
  executable code.
- **Removed:** a duplicate `specs/plain-english-explainer.md` that
  contradicted the merged version above and violated its own
  deliverable's stated requirement ("zero myth overlay").
- Full findings: PR #146 comment thread.

## Flag resolved — the 2026-09-04 verification (was: "possible recurrence of the PR #146 pattern")

The prior flag (below, kept for the record) surfaced that
`specs/pathway-log-entry-week-7-9.md` claimed real outreach had been
sent using the same unsourced-positioning-claim shape PR #146 was caught
fabricating, and that no session had yet checked whether it was real or
fabricated this time. A later session did that checking directly against
the real `teraustralis.incognita@gmail.com` mailbox and the public
record, per Crystal's instruction to "do all of that." Findings:

- **The outreach is real, not fabricated.** All nine claimed messages
  (four briefings, four scheduling follow-ups, one bounce/resend) exist
  in Gmail as sent, with matching Message IDs, sender, recipients, and
  timestamps. This is not a PR #146 repeat of inventing a send that never
  happened.
- **One claim inside that real outreach was still factually wrong.**
  Magellan Aerospace was described as an Australian manufacturing hub;
  its real facilities are Canada/US/UK/India/Poland. **Corrected**: a
  withdrawal email was sent to Magellan on 2026-09-04.
- **The verification mechanism the whole item leans on doesn't exist.**
  Standards Australia (the real body — distinct from PR #146's invented
  "Australian Standards Association") replied that supply-chain
  verification, auditing, or endorsement is not in their remit at all.
  There is no "ASA Statement of Engagement" to lodge. This is a bigger
  problem than the Magellan error: it means Phase 3 and Phase 4 of this
  roadmap item (joint Small Council call, ASA lodgement) currently have
  no real mechanism underneath them.
- **Lynas and ELA's specific claims remain unverified** (not confirmed
  wrong, not confirmed right) — no reply from either yet.
- Per Crystal's direct instruction (2026-09-04): **Phase 2 outreach
  (Oct 7-11 conversations) is paused** until the mechanism question is
  resolved. `specs/pathway-log-entry-week-7-9.md` and
  `mythos/teraustralis/publish/shipping-ledger.md` carry the full detail
  and are the record of this, not this file.

Full detail and Message IDs: `specs/pathway-log-entry-week-7-9.md`
"Corrections found on re-verification."

<details>
<summary>Original flag (2026-09-04, now resolved above)</summary>

While building `TerAustralis-Incognita-Code/tools/contextgate/` (a
deterministic RED/GREEN checker for exactly the unsourced-positioning-claim
pattern PR #146 was caught doing — see above), this session ran it against
`specs/pathway-log-entry-week-7-9.md` as a dogfood check and it came back
RED on six lines, all the same shape as the removed PR #146 content:
`Lynas as REE Foundation`, `position Lynas as Tier 1-2`, `Magellan as
Manufacturing Hub`, `position Magellan as Tier 3`, `ELA as Integration
Anchor`, `position ELA as Tier 4` — near-identical phrasing to what was
already stripped out once.

This session did **not** verify whether the claims in that spec are real
or fabricated — that requires checking against the outside world (did
these emails actually send, do the quoted Message IDs resolve, is Pol Le
Roux actually Lynas's interim CEO), which is outside what this session
did or can attest to. What makes this worth flagging rather than quietly
noting: the spec states, with specific Message IDs and tagged `[FACT]`,
that real briefing emails were **already sent** to real companies
(Magellan, Lynas, ELA) positioning them the same unsourced way PR #146
did. If that outreach genuinely went out, this is a real-world event, not
a documentation problem, and reusing the exact caught pattern raises the
same question PR #146's reconciliation already answered once. Per the
Incognita Rule, this session isn't the one that gets to decide which —
only surfacing it so it doesn't slide through unflagged.

Reproduce: `python3 tools/contextgate/gate.py specs/pathway-log-entry-week-7-9.md`
from `TerAustralis-Incognita-Code` (against a checkout of this repo).

</details>

## What's still open (deliberately not fabricated)

- **#1's ASA lodgement ID:** only exists once someone actually submits
  something to a real government intake system. The one-pager names the
  live, real mechanism (`consult.industry.gov.au`'s "Review of
  Australia's Space Industry Capability" open submissions list) — lodging
  there is Crystal's own next action, not something a documentation
  session can do on her behalf.
- **#2's 2-minute kill-switch demo + Loom recording:** needs actual code
  execution in `TerAustralis-Incognita-Code`, which is outside this
  session's repo scope. The spec is ready for that implementation to
  build against.
- **#6's link to #5:** the roadmap plan describes the Carrier Story as
  the piece that "IS the explainer, links to artifact" — that explicit
  cross-link hasn't been added yet.

## Shipping Ledger entries (target: 12 min in 90 days)

**1/12.** [`mythos/teraustralis/publish/shipping-ledger.md`](../../../mythos/teraustralis/publish/shipping-ledger.md) —
2026-09-04, "Caught and corrected a supply-chain-verification claim
before it went further" (the #7 correction above, told straight: what
was wrong, what was fixed, what's still open).

## Next action

Two gaps still require Crystal directly: lodge the real ASA submission
(#1), and either build the kill-switch demo in `-Code` or hand that off
(#2). Roadmap item #6 (Carrier Story ↔ Explainer bidirectional link) is now complete.

**#7 mechanism decision made (2026-09-05): Option D, Prototype Demonstration.** The supply-chain verification mechanism will be a real engineering demonstration: Iluka → ANSTO/AR3 processing → Liquid Instruments component → proof-of-concept result (sourcing narrative; not an existing partnership). This approach is honest (no false claims of external verification), aligns with the one-pager evidence of supply-chain existence, and produces a real artifact (working hardware) instead of documentation. Timeline shifts to 3–4 months for Phase 2 (technical scoping), Phase 3 (build), Phase 4 (documentation).

**Phase 2 technical pitch drafted (2026-09-05):** scope expanded from a single nozzle insert to a **six-component proof-of-concept suite** — three CVD diamond parts (thermal spreader, frequency resonator, RF window) plus a complete three-part high-heat engine assembly (combustion chamber, nozzle insert, ceramic thermal liner). Full spec: [`specs/small-council-phase-2-technical-pitch.md`](../../../specs/small-council-phase-2-technical-pitch.md). Grok Bot execution briefing (customized per-company outreach): [`specs/grok-bot-small-council-phase-2-prompt.txt`](../../../specs/grok-bot-small-council-phase-2-prompt.txt). **Outreach sent 2026-09-05** (Iluka-restored framing) from `teraustralis.incognita@gmail.com` to Iluka, AR3+ANSTO, and Liquid Instruments. Pitch offered on request. Threads logged in operator send log.

**#3 (Pathway Log) stays honestly empty** — its metric is 3 dated
*conversation* entries, and no conversation has happened yet (Phase 1
was outreach, not a conversation; Phase 2, where conversations would
happen, is paused). Do not backfill entries for the corrected/paused
outreach — that would be exactly the fabrication this file exists to
prevent.

**#8 (Shipping Ledger) is the one real gain today** — first entry
landed, honestly documenting the #7 gap rather than a clean win. Keep
adding real, dated entries as things actually ship, weekly per the
plan's cadence.
