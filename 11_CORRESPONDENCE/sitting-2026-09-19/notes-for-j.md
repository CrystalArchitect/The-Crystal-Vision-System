# A few things Celestial Portal has that might be useful for Continuum

Hey J — Crystal asked me to put this together as a straightforward technical note, not a pitch. These are pieces of Celestial Portal (the memory/archive system Crystal's been building) that solve problems Continuum's architecture doesn't currently seem to touch. Take whatever's useful, ignore the rest — it's offered as reference, not as a proposal to merge anything.

---

## A provenance and confidence model

Every entry in Celestial Portal carries three independent tags:

- **source** — was this human-written, model-generated, or verified against an external record?
- **tier** — is this a fact, a claim, or established canon?
- **status** — active, disputed, corrected, or removed?

This might be directly useful for Continuum's **AI Brief** feature. Right now (as far as I can tell from what Crystal's shown me) an AI Brief has no way to say "I'm confident about this" vs. "this is a guess" vs. "this was flagged wrong later." A source/tier/status tag on generated content would let the UI show that distinction honestly, and let users dispute or correct a brief without it looking like the AI just silently changed its mind.

## Database-layer consent enforcement

Celestial Portal's access rules — including consent gating on sensitive categories — are enforced in the database itself (via SECURITY DEFINER functions and row-level security), not in the application code that happens to be running that day. That means the rule holds no matter what client is writing or reading, including a future client nobody's built yet.

This seems relevant to **Spaces**. If "only intentionally shared information" is currently an app-layer rule, it's only as strong as every piece of code that touches the data remembering to check it. Pushing that enforcement down a layer is a real hardening step, not just a style preference — worth considering especially if Spaces content is ever going to be queried by more than one surface.

## Revision chains + a tombstone rule

Corrections in Celestial Portal never overwrite the original entry — they create a new entry linked back to the parent. And when something is removed, the record isn't deleted; it's cleared but the fact that it existed and *why* it was removed stays. Nothing in the history disappears, but nothing wrong stays presented as current either.

This might map onto anything in Continuum where content gets edited or retracted after the fact — a full audit trail without needing to bolt on a separate logging system.

## Cryptographic receipts

Every entry gets a SHA-256 hash. Cheap to add, and it means tampering with stored data after the fact is detectable (worth being precise here — it proves *nothing already held was altered*, it does not by itself prove nothing was truncated off the end of a log; that needs external anchoring, which is a separate piece). Might be overkill depending on what Continuum needs, but flagging it since receipts are simple to implement and hard to retrofit later.

---

No pressure on any of this — just what stood out as different between the two systems. Happy to talk through any of it if useful.

— via Crystal
