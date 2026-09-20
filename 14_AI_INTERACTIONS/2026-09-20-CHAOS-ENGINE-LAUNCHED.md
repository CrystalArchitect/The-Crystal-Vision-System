# Chaos Engine — LAUNCHED (2026-09-20)

**Canon:** **no**  
**Status:** **LIVE**  
**HTTP:** `http://0.0.0.0:8765` (Cloud Agent tmux session `chaos-engine`)

## Cleared

```
align: DRIFT NONE — launch cleared
```

## Surfaces

| Surface | Command / URL |
| --- | --- |
| CLI launch | `python3 scripts/chaos/launch.py` |
| HTTP serve | `python3 scripts/chaos/launch.py --serve --port 8765` |
| Health | `GET /health` → `{"status":"launched","engine":"chaos"}` |
| Fan-out | `POST /v1/gateway/chaos` `{"text":"..."}` |
| Portal (full app) | `POST /v1/gateway/chaos` when Portal is up |

## First live HTTP run

- **run_id:** `27250572-e13f-4dd3-bf3e-8cc6f68ca9a8`
- **asked:** 7 · **ok (keyed):** 0 · **silent:** 6 · **local.open:** speaking
- Keys: all NOT_SET — silence is correct, not a hang

CLI ledger: [`chaos-ledger/2026-09-20-LAUNCH.md`](chaos-ledger/2026-09-20-LAUNCH.md)

## Law

Models think · TAI acts · CrystalCore governs · Human publishes · Counts ≠ verdicts · Core ≠ TAI

*Non Solus.*
