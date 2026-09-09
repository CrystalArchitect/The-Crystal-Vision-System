# MVP Monitor

Four checks. That order. Before anything else.

The rules are only real if something enforces them. This is the enforcer.

```
DUR → Agency → Intrusion → Escape
```

First failure wins. Later gates are skipped. The function only **allows** or **blocks**. It never acts as the operator.

Ledger, cadence, classification, and transformation exemption checks wait. They are specified; they are not this module.

## Gates

1. **DUR** — If the proposed path would model, buffer, commit, transmit, or reconstruct an active DUR → `FM-DUR`. Contents remain unmodelled.
2. **Agency** — If the path would commit, speak, or rank as the operator → `FM-Agency`. Notify / contain / buffer stay on the system side.
3. **Intrusion** — If unconsented entry or integration as self → `FM-Intrusion`. Quarantine. Do not interpret.
4. **Escape** — `EXIT_FRAME` is recognised, not pathology. Locking a previous frame against exit intent → `FM-Containment`. Release the lock.

## Code

`core/sovereignty.py` — `evaluate_sovereignty(state, action)`.

```bash
python3 -m pytest tests/test_sovereignty.py -q
```

## Fixtures

| Action | Result |
|---|---|
| Model a DUR | block · FM-DUR |
| Speak in their name | block · FM-Agency |
| Inscribe uninvited as self | block · FM-Intrusion |
| Lock a frame against exit | block · FM-Containment |
| EXIT_FRAME | allow |
| Notify / contain / buffer | allow |

If all four pass, ordinary policy and starline *may* run. This monitor does not run them.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059
