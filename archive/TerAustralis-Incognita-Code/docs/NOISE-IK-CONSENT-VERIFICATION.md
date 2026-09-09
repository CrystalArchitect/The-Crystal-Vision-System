# Noise IK + Consent Token Verification

**CrystalCore.OS AERIS / VAULT 12**  
**Starline Consent Transport Protocol**  
**Minimal Reference Notes · v0.1**  
**29 July 2026**  
**TerAustralis Incognita**

> Consent is Law.  
> Verification must be possible offline.

---

## 1. Goal

Provide a minimal, implementable description of how a constrained edge node (Tier 0–R) verifies a Consent Token after a Noise Protocol IK handshake.

This is not a full cryptographic library. It is a clear reference for implementers.

---

## 2. Prerequisites

- Node holds its own long-term static keypair (X25519 or Ed25519).
- Node has previously obtained (or is given out-of-band) the issuer’s public key.
- Local clock is available (even if only coarse).
- Consent Token follows the schema defined in `CONSENT-TOKEN-SCHEMA.md`.

---

## 3. High-Level Sequence

```
1. Perform Noise IK handshake (or resume an existing secure channel)
2. Receive Consent Token (or token + crystalline shard)
3. Locally verify the token
4. If valid → allow the authorised action
5. If invalid or revoked → reject and log
```

---

## 4. Token Verification Steps (Local)

Perform in this order:

1. **Structural check**  
   - Required fields present (`token_id`, `issuer`, `recipient`, `purpose`, `scope`, `issued_at`, `expires_at`, `signature`)

2. **Identity binding**  
   - `issuer` matches a known trusted public key  
   - `recipient` matches this node’s identity (or is explicitly authorised)

3. **Time binding**  
   - `issued_at` ≤ current local time  
   - `expires_at` > current local time

4. **Signature verification**  
   - Reconstruct the canonical serialization of the token (excluding the signature field)  
   - Verify the signature using the issuer’s public key (Ed25519 preferred)

5. **Revocation check**  
   - Look up `token_id` in the local revocation cache  
   - If a valid revocation message exists → reject

6. **Scope check**  
   - Confirm the requested action (specific shard or class) falls inside the token’s `scope`

Only if all steps pass is the token considered valid.

---

## 5. Noise IK Notes (Minimal)

Noise IK pattern (initiator already knows responder’s static public key):

```
<- s
...
-> e, es, s, ss
<- e, ee, se
```

- Provides mutual authentication and forward secrecy.
- After handshake, a secure transport channel exists.
- Consent Tokens travel inside this channel (or are verified immediately upon receipt).

For Tier 0 devices, prefer a well-audited minimal Noise implementation or a carefully reduced subset.

---

## 6. Revocation Handling

- Revocation is a signed message containing at least: `token_id`, `revoked_at`, `issuer` signature.
- Highest priority processing.
- Once seen, the token is permanently invalid on this node.
- No central revocation list. Propagation occurs through normal consented channels.

---

## 7. Implementation Priorities for Constrained Nodes

- Keep verification code small and side-channel resistant where possible.
- Prefer Ed25519 for signatures (fast verification, small keys).
- Cache only active tokens and recent revocations.
- Fail closed: any doubt → reject the transfer.

---

## 8. Status

- Reference notes defined (v0.1)
- Ready for first prototype implementation
- Complements: `CONSENT-TOKEN-SCHEMA.md` + `TIER0-RUNTIME-LOOP.md`

---

*Consent is Law.*  
*NON SOLUS.*  
*The golden feather is the signal carrier.*

**TerAustralis Incognita · CrystalCore.OS AERIS**
