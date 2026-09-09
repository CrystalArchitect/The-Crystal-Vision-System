# Consent Transport — Technical Architecture

**Status:** v1 implemented — `src/crystal-core/consent_transport/` · `python3 -m consent_transport.selftest`

## Purpose

Consent Transport is the sovereign communication layer between individually
locally-running Clementine agents. It lets two companions exchange
consented memory fragments directly, peer to peer, without routing
through a central server or surrendering data ownership.

It is the technical realization of the mythic "Starlines" in `mythos/` —
pathways of connection that are consensual, encrypted, and owned by the
participants, not by a platform between them.

## Core Design Principles

| Principle | Description | Non-negotiable |
|---|---|---|
| Local-first | All primary data and memory lives on the user's device | Yes |
| Sovereignty | No third party can access, read, or retain another agent's data | Yes |
| Consent-based | No data moves without explicit, revocable permission from the owner | Yes |
| Encrypted | All transit is end-to-end encrypted (Noise Protocol) | Yes |
| Minimal trust | Agents trust cryptographic identity + explicit consent, never a platform | Yes |
| Mythic + technical | The architecture should feel like an extension of Songlines/Starlines | Preferred |

## v1 Scope Decisions

The original draft of this document left three questions open. They're
answered here, with the reasoning, because the reasoning matters more
than the answer for whoever revisits this later:

- **Pull-based, not push.** An agent must request fragments and be
  explicitly approved before anything is sent. Push/broadcast would mean
  receiving *before* consenting to receive — that inverts the consent
  principle. Pull keeps consent strictly ahead of every exchange.
- **Strict 1:1, not group/mesh.** Group memory sharing needs real
  group-key management (what protocols like Signal's MLS exist to
  solve) — that's a separate, harder problem, not a flag to flip later.
  Ship 1:1, learn from real use, revisit groups deliberately.
- **Direct peer-to-peer over Noise, not libp2p or Nostr.** libp2p's
  mesh/pubsub/NAT-traversal machinery is more surface area than a 1:1
  pull protocol needs. Nostr's relay model reintroduces a third party in
  the transport path even with encrypted payloads. The Noise Protocol
  Framework (same primitive family WireGuard and Signal's handshakes use)
  gives mutual authentication and forward secrecy with a two-message
  handshake and nothing else in between.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Consent Transport Layer (crystal-core)           │
├─────────────────────────────────────────────────────────────┤
│ Clementine (local) ◄── Noise IK, TCP ──► Other sovereign agent│
│         │                                          │          │
│         ▼                                          ▼          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           Local Memory Fragments (per agent)             │  │
│  │  episodic · semantic · emotional · mythic                │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components (implemented)

| Module | Responsibility |
|---|---|
| `identity.py` | Ed25519 signing keypair + X25519 DH keypair per agent. Private keys never leave the device; the identity file is gitignored and unrecoverable if lost, by design. |
| `noise.py` | `Noise_IK_25519_ChaChaPoly_SHA256` — a literal, from-spec implementation of the Noise Protocol Framework's `IK` pattern. No custom crypto: X25519, ChaCha20-Poly1305, and SHA256/HMAC come from `cryptography` and the stdlib. |
| `peers.py` | The local "address book" — paired peers and their public keys. Pairing ≠ consent; these are deliberately separate steps. |
| `consent.py` | Signed, timestamped grant/revoke receipts. The most recent receipt for a peer wins; no receipt means no consent — closed by default. |
| `fragment.py` | The `MemoryFragment` — small, typed, signed. Never a bulk memory dump. |
| `protocol.py` | Three message types over the Noise-encrypted channel: `request`, `fragments`, `denied`. |
| `transport.py` | TCP server/client. Binds `127.0.0.1` by default. Consent is checked fresh on every connection, so a revoke takes effect on the very next request. |
| `discovery.py` | Same-LAN UDP broadcast — announces a public key and port, nothing else. Discovery makes a peer *visible*; it never auto-pairs and never grants consent. |
| `agent.py` | `StarlineAgent` (legacy name preserved for backward compatibility) — the high-level API tying all of the above together. |

## Pairing — how two agents find each other (no third party)

1. **Same-LAN**: `agent.announce()` broadcasts a UDP packet with the
   agent's public keys and port; `agent.discover()` on the LAN hears it.
   Either agent then calls `agent.pair(announcement)` — a human-approved
   step, not automatic.
2. **Remote / off-LAN**: manual key exchange — one agent shows a QR code
   or the fingerprint/keys as text, the other scans or pastes it into
   `agent.pair_manual(...)`.

No rendezvous server, no relay, in either path.

## Consent & Revocation — the honest limits

Every fragment exchange requires the receiving human to have explicitly
`grant()`-ed the requesting peer. `revoke()` takes effect immediately on
the next request. But revocation has a limit worth stating plainly:
**it cannot delete a fragment a peer already legitimately received.**
That fragment is now on their own sovereign device — forcing its
deletion would violate the same sovereignty principle protecting your
own data. Revocation means "no more, starting now," not "undo the past."
