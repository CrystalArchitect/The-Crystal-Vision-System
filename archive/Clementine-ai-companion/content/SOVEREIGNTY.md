# Sovereignty — TerAustralis Incognita

This document describes a property the companion enforces, not one it intends
to. Unlike `ARCHITECTURE.md`, which is a design overview of a system still
largely in concept, everything below is verifiable against code that runs and
is covered by tests.

**Date:** 10 August 2026 · **Status:** Internal reference ·
**Related:** Clementine architecture, consent gate, local-first principles

## 1. The claim

Clementine is an existence proof for the stricter end of the personal-AI design
space: an agent that can be useful while remaining unable to send private
context to a model without recorded consent.

The design question it answers is not *"should personal AI be widely
available"* — it is *"where does the control boundary sit"*. Clementine places
it at the **runtime**, rather than at the policy or product layer.

## 2. What that means concretely

| Principle | Implementation |
|---|---|
| Locus of control | Local-first runtime; core function must not require the cloud |
| Trust model | Architectural consent gate. Calls **leaving the machine** are refused unless explicitly allowed; local calls proceed uninterrupted and are recorded |
| Memory | Stays on-device. Embeddings computed locally regardless of chat provider. Export and import are user-initiated |
| Default when unsure | Fail closed — and fail early, at startup rather than at first use |
| Customisation | Name and pronouns unset until **the human *or the companion*** chooses. The record distinguishes which |
| Verification | A suite that can be run. As of 10 August 2026: 112 tests in the companion, 74 for the bot — including tests written by deliberately breaking the implementation to prove they fail |

The consent gate, local embeddings, explicit memory-path requirements, and
refusal of silent fallbacks are not product preferences. They are the technical
expression of the claim that a companion with access to a person's memory and
the ability to act must remain under that person's continuing control.

## 3. Two details that carry more weight than their size

**Pre-authorisation is not a blanket grant.** The `--remote-model-ok` flag
returns a verdict with `remember=False`, so the gate is consulted on *every*
call and each is audited separately. The human authorises a posture, not a
session.

**The address the gate judges is the address the request uses** — one
attribute, read by both, with the same discipline applied to the model name. A
gate that approved one destination while the request reached another would not
merely fail to protect; it would write a false statement into the audit log,
which is worse than recording nothing.

## 4. Boundaries of the claim

The claim in §1 is precise, and the precision matters:

- **It governs model calls.** Chat, embeddings, summary, reflection — each
  passes the gate and lands in the audit log.

- **It does not govern interface channels.** Running the Discord bot relays
  conversation to Discord's servers. That is the human's choice, but it is not
  gated and does not appear in the audit log.

- **It assumes loopback binding.** `--host 0.0.0.0` exposes the API to anyone
  who can reach the port; the server warns, but the property then rests on an
  authenticating proxy rather than on the gate.

- **Some material is refused regardless.** Content under `PROTECTED_SOURCES`
  cannot be sent to *any* model, local included, and there is deliberately no
  prompt — the person at the keyboard has no standing to consent on custodians'
  behalf.

---

*Naming the boundaries in §4 is not a weakening of the claim. A guarantee whose
edges are stated can be relied on; one that implies more than it enforces
cannot.*

---

## Appendix — deferred comparison

A version of this note comparing Clementine's position against a publicly
distributed-access framing of personal superintelligence exists in draft. It is
**not filed**, because it characterises a third party's public argument from a
source that has not been read.

That comparison can be added once the original has been retrieved, read, and
checked for fair representation. Until then this note stands on what is
verifiable against the code, which is all of it.
