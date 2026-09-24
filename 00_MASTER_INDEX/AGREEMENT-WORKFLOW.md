# Agreement workflow

**Canon:** **no**  
**Drawer:** 00_MASTER_INDEX  
**Updated:** 2026-09-24  
**Working-index:** `CVS-AGREE`  
**Crystal-first read:** [`NEEDS-YOUR-YES.md`](NEEDS-YOUR-YES.md)  
**Ledger (agents):** [`agreement-ledger.yaml`](agreement-ledger.yaml)  
**CLI:** `python3 scripts/agreement/status.py` · `--plain` for human text

Start with [`NEEDS-YOUR-YES.md`](NEEDS-YOUR-YES.md) if you only want the questions. This file is the longer agent map.

## Why this exists

The hub already has several places that *look* like agreement:

| Surface | What it actually is |
| --- | --- |
| [`CRYSTAL-DECISIONS-PENDING.md`](CRYSTAL-DECISIONS-PENDING.md) | Packets waiting for Crystal |
| [`memory/DECISIONS.md`](../memory/DECISIONS.md) | Monorepo decisions recorded on disk |
| [`OPEN-BACKLOG.md`](OPEN-BACKLOG.md) | Open gates + hygiene |
| Working Index `Canon` column | Almost always **no** until Crystal stamps |
| "GO stamp" in sitting notes | Often coordination yes — **not** automatically Canon |

Without one checklist, it is easy to confuse **filed**, **Built**, **Crystal said yes**, and **Canon**.

## Status vocabulary (use these only)

| Status | Plain | Agents may… |
| --- | --- | --- |
| `proposed` | Waiting on you | Ask; do not execute irreversible acts |
| `interim` | Working for now | Operate carefully; silence is not a stamp |
| `crystal_confirmed` | You already said yes | Treat as hub law for coordination |
| `canon` | Canon | Cite as Canon |
| `rejected` | You said no | Do not revive without a new packet |
| `vision_only` | Story only | Keep labeled Vision |

**Canon is never inferred.** `crystal_confirmed` can still be Canon: **no**.

## How to confirm (Crystal)

1. Read [`NEEDS-YOUR-YES.md`](NEEDS-YOUR-YES.md), or run:

```bash
python3 scripts/agreement/status.py --plain
```

2. Pick an id (`DEC-A`, `DEC-C`, …).

3. Reply in chat or a PR comment:

```
AGREE <id> — <one-line note>
REJECT <id> — <one-line note>
CANON <id> — <one-line note>
INTERIM <id> — <one-line note>
```

Examples:

```
AGREE DEC-C — stubs/UK gone was intentional
CANON DEC-B — keep memory/ and 00_MEMORY/ dual path
REJECT DEC-E — do not change MemoryCore tracks yet
```

4. Agent updates the ledger + decisions/backlog as needed. Crystal should not have to edit YAML.

5. Re-run `--plain` — waiting items should shrink.

## How agents use this

Before irreversible work (Drive create, rename, delete, Canon claim, cloud MemoryCore deploy):

1. `python3 scripts/agreement/status.py --id <ID>`  
2. If status is `proposed` or missing → **stop** and ask Crystal.  
3. If `interim` → allowed only as documented; do not upgrade to Canon.  
4. If `crystal_confirmed` or `canon` → proceed within the note's scope.  
5. Never treat merge to `main` alone as agreement.

## Do not

- Invent a second decision tree outside drawer 00 + `memory/`  
- Auto-promote Vision → Canon  
- Execute Drive / delete / rename on silence  
- Collapse CrystalCore / Portal / Clementine because something was "agreed" in chat  
- Ask Crystal to read YAML to decide  

*Non Solus.*
