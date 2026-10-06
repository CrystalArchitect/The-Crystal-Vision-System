# Needs your yes (plain read)

**Canon:** no  
**For:** Crystal  
**Buddy file (agents):** [`AGREEMENT-WORKFLOW.md`](AGREEMENT-WORKFLOW.md)

This page is the readable version. Skip the YAML. Skip the long tables.

## What the words mean (short)

| Word | Plain meaning |
| --- | --- |
| Waiting on you | Not decided yet |
| Working for now | Agents may follow this, but you have not sealed it |
| You already said yes | Coordination agreed; still usually not Canon |
| Canon | You raised it to sealed truth |
| Story only | Creative filing — not a decision |

Saying **yes** to coordination is not the same as making something **Canon**.

## Waiting on you

### DEC-C — Gone repos
Confirm those missing stub / UK / CrystalCore private repos were deleted on purpose?

**Recheck 2026-10-06:** still GONE (84 public repos, 0 private; API 404).

Reply: `AGREE DEC-C — yes, intentional` or `REJECT DEC-C — …`

### DEC-D — Stewards
Name stewards for drawers 16-20 and Product when ready.

Reply: `AGREE DEC-D — names: …` when you appoint them.

## Working for now (optional stamp later)

### DEC-B — Two memory folders
Keeping both `memory/` and `00_MEMORY/` for now.

Reply later if you want a rename: `CANON DEC-B — keep both` or pick another option in the pending packet.

### DEC-E — MemoryCore tracks
Agents treat local companion memory and optional archive vault as **separate** (E1).

Reply when you pick E1-E4: `AGREE DEC-E — E1` (or E2/E3/E4).

### AGR-STACK-SURFACE — Stack map
Siri to Portal to CrystalCore.OS to TAI is on disk as the layer map. Not Canon yet.

## You already said yes (still not Canon)

- **DEC-A** — Drive folders 16–20 created 2026-10-06; URLs in `STRUCTURE.md`  
- Alive Weave: connect islands; do not merge  
- ConsentGate before guest speech  
- This repo is the filing hub  
- Chaos Engine is a go (counts are not verdicts)  
- Do not build Starfleet OS  
- **AGR-ICANN-TSG-GROK** — Grok Bot may use the ICANN TSG paste card as a **research desk** only (26 Sep `Ok stamp`; Canon still no)  

## Story only (not a decision)

- AHS Lemuria sandbox  
- Fermi's Silent Line poster / song  

## How to answer (copy/paste)

```
AGREE DEC-C — yes, intentional
CANON DEC-B — keep both memory folders
INTERIM DEC-E — stay on E1
```

After you reply, an agent updates the ledger. You should not have to edit YAML.

## Check from a terminal (optional)

```bash
python3 scripts/agreement/status.py --plain
```

*Non Solus.*
