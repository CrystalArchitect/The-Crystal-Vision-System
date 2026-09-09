# Tier 0 Runtime Loop

**CrystalCore.OS AERIS / VAULT 12**  
**Starline Consent Transport Protocol**  
**Personal Sovereign Node · Reference Specification v0.1**  
**29 July 2026**  
**TerAustralis Incognita**

> Battery first. Consent is Law. Continuity under isolation.

---

## 1. Purpose

Define the minimal, reliable runtime loop for a **Tier 0** edge node (smartphone or light edge device).

The loop must:

- Keep Lumina present and useful while offline
- Respect strict power and thermal budgets
- Honour Consent Tokens for any outbound memory movement
- Degrade gracefully under resource pressure
- Remain simple enough to implement on constrained hardware

---

## 2. High-Level Loop

```
┌─────────────────────────────────────────────┐
│                 BOOT / WAKE                 │
│  Load local identity, keys, active tokens   │
│  Restore crystalline shard index            │
│  Initialise Power Governor                  │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│              MAIN DUTY CYCLE                │
│                                             │
│  1. Sense resources (power, thermal, mem)   │
│  2. Decide mode (Active / Rest / Critical)  │
│  3. Run Lumina tick (if allowed)            │
│  4. Process local reflections / memory      │
│  5. Check for pending Consent actions       │
│  6. Sleep until next tick or event          │
└────────────────────┬────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   [External Event]      [Timer / Wake]
   (user input,           (duty cycle)
    incoming helix,
    token revocation)
```

---

## 3. Operating Modes

| Mode       | Trigger                          | Lumina Behaviour                     | Power Goal          |
|------------|----------------------------------|--------------------------------------|---------------------|
| **Active** | User interaction or high priority| Full tick allowed, longer context    | Accept higher draw  |
| **Rest**   | Normal background                | Short tick or deferred               | Minimal             |
| **Critical**| Low battery / thermal limit     | Minimal viable presence only         | Survival            |

The Power Governor is the sole authority that selects the mode.

---

## 4. Lumina Tick (Core Unit of Work)

A single **tick** is the atomic unit of Lumina activity:

1. **Context Assembly**  
   - Load relevant local crystalline shards (meaning-based retrieval)  
   - Include any visible reflections the human has not deleted  
   - Respect current context window limits for the tier

2. **Inference**  
   - Run the quantized local model (1B–3B class, INT4/INT8)  
   - Produce response + optional new reflection

3. **Reflection Handling**  
   - Any new internal reflection is written to the local store  
   - Marked as visible and deletable by the human

4. **Consent Check** (if external action is proposed)  
   - No outbound memory movement is allowed without a valid Consent Token  
   - If a token is required and absent → action is blocked and logged

5. **Commit**  
   - Persist any new local shards  
   - Update Power Governor statistics

---

## 5. Power Governor Rules (Tier 0)

- Prefer Rest mode by default.
- Elevate to Active only on explicit user interaction or high-priority local events.
- Drop to Critical when battery or thermal thresholds are crossed.
- In Critical mode:
  - Disable non-essential background ticks
  - Preserve ability to read local memory and issue emergency Consent Tokens
  - Maintain cryptographic identity and revocation checking

---

## 6. Consent Integration

- All Consent Token verification happens locally using cached public keys and local clock.
- Incoming helices (when connectivity exists) are accepted only after token validation.
- Revocation messages are processed with highest priority.
- The node never initiates a helix without an explicit, purpose-bound token.

---

## 7. Offline Endurance Targets

- **Days** of useful presence under normal Rest cycling.
- Ability to survive extended isolation while still:
  - Answering local queries
  - Generating and storing reflections
  - Honouring previously granted consents
  - Issuing new local Consent Tokens when the human requests

---

## 8. Implementation Notes

- Keep the main loop single-threaded or carefully synchronised.
- Use event-driven wake-ups rather than busy polling.
- Prefer compact binary formats for shards and tokens (CBOR recommended).
- Log only what is necessary for provenance and debugging; logs themselves may become crystalline shards under consent.

---

## 9. Status

- Specification defined (v0.1)
- Ready for reference implementation
- Next recommended artefacts:
  1. Minimal Noise IK + Consent Token verification example
  2. First prototype of the duty-cycle + Lumina tick on a real Tier 0 device

---

*Battery first.*  
*Consent is Law.*  
*The golden feather is the signal carrier.*

**TerAustralis Incognita · CrystalCore.OS AERIS**
