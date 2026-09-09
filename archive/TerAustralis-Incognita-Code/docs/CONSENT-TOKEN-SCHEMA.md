# Consent Token Schema

**CrystalCore.OS AERIS / VAULT 12**  
**Starline Consent Transport Protocol**  
**Version 0.1 · 29 July 2026**  
**TerAustralis Incognita**

> Nothing moves without explicit, revocable permission.  
> Revocation takes effect instantly.

---

## 1. Purpose

A **Consent Token** is the atomic unit of permission in Starline.  
It authorises the movement of one or more crystalline memory shards (or a defined class of shards) between two specific nodes for a bounded purpose and time.

No data leaves a node unless a valid, non-revoked Consent Token is presented and verified.

---

## 2. Token Structure (Canonical)

```json
{
  "version": "0.1",
  "token_id": "uuid-v4",
  "issuer": "node_public_key_or_id",
  "recipient": "node_public_key_or_id",
  "purpose": "string (human + machine readable)",
  "scope": {
    "shard_ids": ["optional list of specific shard UUIDs"],
    "shard_class": "optional class label (e.g. 'reflection', 'memory', 'telemetry')",
    "max_bytes": 0
  },
  "issued_at": "ISO-8601 UTC",
  "expires_at": "ISO-8601 UTC",
  "revocable": true,
  "revocation_endpoint": "optional local or helix path",
  "constraints": {
    "one_time_use": false,
    "requires_ack": true,
    "max_transfers": 1
  },
  "signature": "ed25519 or equivalent over canonical serialization"
}
```

### Field Notes

| Field | Required | Description |
|-------|----------|-------------|
| `token_id` | Yes | Globally unique identifier (UUID v4 recommended) |
| `issuer` | Yes | Public key or stable node ID of the granting node |
| `recipient` | Yes | Public key or stable node ID of the receiving node |
| `purpose` | Yes | Short, explicit statement of why the transfer is allowed |
| `scope` | Yes | What may be transferred (specific shards, class, or size limit) |
| `issued_at` | Yes | Issuance timestamp |
| `expires_at` | Yes | Hard expiry. After this time the token is invalid |
| `revocable` | Yes | Always `true` in current design |
| `signature` | Yes | Cryptographic signature by the issuer |

---

## 3. Cryptographic Binding

- **Signature algorithm**: Ed25519 (preferred) or the static key already used in the Noise IK handshake.
- Canonical serialization (deterministic field order + no whitespace) is signed.
- The token is bound to both the issuer’s and recipient’s long-term identities.
- A token is only valid when verified against the issuer’s known public key.

---

## 4. Lifecycle

1. **Creation** — Issuer (usually the data owner) constructs and signs the token.
2. **Transmission** — Token travels with or ahead of the crystalline shard via a Noise IK helix.
3. **Verification** — Recipient checks signature, expiry, scope, and revocation status.
4. **Use** — Data is transferred only while the token remains valid.
5. **Revocation** — Issuer can revoke at any time. Revocation is immediate and must be honoured by any node that has seen the token.
6. **Expiry** — Hard wall-clock expiry. No extension without a new token.

---

## 5. Revocation Mechanics

- Revocation is a signed message containing the `token_id` and a revocation timestamp.
- Any node that receives a valid revocation must treat the token as dead.
- On power- or connectivity-constrained nodes, revocation is checked:
  - At token presentation
  - Periodically while a helix is open
  - On any new connection that might carry revocation gossip
- There is no central revocation list. Revocation propagates through the same consent-bound channels.

---

## 6. Design Rules (Non-Negotiable)

- **No ambient authority** — A token grants permission only between the named issuer and recipient.
- **Purpose binding** — The `purpose` field is mandatory and should be human-readable.
- **Time binding** — Every token has a hard `expires_at`.
- **Instant revocation** — The design assumes revocation can take effect as soon as it is known.
- **Minimal size** — Tokens must remain small enough for Tier 0 and Tier R devices.
- **No silent renewal** — Extension requires a new token.

---

## 7. Implementation Notes for Constrained Nodes

- Prefer compact binary encoding (CBOR or similar) over JSON for wire transfer.
- Keep the signed payload under a few hundred bytes whenever possible.
- On Tier 0 / Tier R devices, cache only active tokens and recent revocations.
- Verification must be possible offline using only the issuer’s public key and local clock.

---

## 8. Status

- Schema defined (v0.1)
- Ready for reference implementation and test vectors
- Next: reference Tier 0 runtime loop + minimal Noise IK + token verification example

---

*Consent is Law.*  
*The golden feather is the signal carrier.*  
*Light helix bridges the realms.*

**TerAustralis Incognita · CrystalCore.OS AERIS**
