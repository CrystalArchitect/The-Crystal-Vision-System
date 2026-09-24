# Agreement workflow

**Canon:** **no**  
**Drawer:** 00_MASTER_INDEX  
**Updated:** 2026-09-24  
**Working-index:** `CVS-AGREE`  
**Ledger:** [`agreement-ledger.yaml`](agreement-ledger.yaml)  
**CLI:** `python3 scripts/agreement/status.py`

## Why this exists

The hub already has several places that *look* like agreement:

| Surface | What it actually is |
| --- | --- |
| [`CRYSTAL-DECISIONS-PENDING.md`](CRYSTAL-DECISIONS-PENDING.md) | Packets waiting for Crystal |
| [`memory/DECISIONS.md`](../memory/DECISIONS.md) | Monorepo decisions recorded on disk |
| [`OPEN-BACKLOG.md`](OPEN-BACKLOG.md) | Open gates + hygiene |
| Working Index `Canon` column | Almost always **no** until Crystal stamps |
| “GO stamp” in sitting notes | Often coordination yes — **not** automatically Canon |

Without one checklist, it is easy to confuse **filed**, **Built**, **Crystal said yes**, and **Canon**.

## Status vocabulary (use these only)

| Status | Meaning | Agents may… |
| --- | --- | --- |
| `proposed` | On disk; Crystal has not answered | Ask; do not execute irreversible acts |
| `interim` | Working assumption; silence ≠ stamp | Operate carefully under it |
| `crystal_confirmed` | Crystal agreed (chat / PR / explicit reply) | Treat as hub law for coordination |
| `canon` | Crystal raised it to Canon | Cite as Canon |
| `rejected` | Crystal said no | Do not revive without new packet |
| `vision_only` | Creative / mythos filing — not a decision | Keep labeled Vision |

**Canon is never inferred.** `crystal_confirmed` can still be Canon: **no**.

## How to confirm (Crystal)

1. Run the ledger:

```bash
python3 scripts/agreement/status.py
# open only:
python3 scripts/agreement/status.py --open
```

2. Pick an `id` from the open list (or from packets A–E).

3. Reply in one of these shapes (chat or PR comment):

```
AGREE <id> — <one-line note>
REJECT <id> — <one-line note>
CANON <id> — <one-line note>
INTERIM <id> — <one-line note>
```

Examples:

```
AGREE DEC-C — stubs/UK gone was intentional
CANON DEC-B1 — keep memory/ and 00_MEMORY/ dual path
REJECT DEC-E3 — do not deprecate cloud vault yet
```

4. Agent (or Crystal) updates:

- [`agreement-ledger.yaml`](agreement-ledger.yaml) status + `confirmed` date + note  
- [`memory/DECISIONS.md`](../memory/DECISIONS.md) if monorepo-level  
- Packet file / backlog row if it closes a gate  
- Working Index Latest Updates one line  

5. Re-run `status.py` — item should leave `--open`.

## How agents use this

Before irreversible work (Drive create, rename, delete, Canon claim, cloud MemoryCore deploy):

1. `python3 scripts/agreement/status.py --id <ID>`  
2. If status is `proposed` or missing → **stop** and ask Crystal.  
3. If `interim` → allowed only as documented; do not upgrade to Canon.  
4. If `crystal_confirmed` or `canon` → proceed within the note’s scope.  
5. Never treat merge to `main` alone as agreement.

## Seed inventory (2026-09-24)

Open / interim packets already on disk are mirrored into the ledger (`DEC-A` … `DEC-E`, plus major coordination stamps). Vision items such as Lemuria stay `vision_only` — playable, not agreement gates.

## Do not

- Invent a second decision tree outside drawer 00 + `memory/`  
- Auto-promote Vision → Canon  
- Execute Drive / delete / rename on silence  
- Collapse CrystalCore / Portal / Clementine because something was “agreed” in chat  

*Non Solus.*
