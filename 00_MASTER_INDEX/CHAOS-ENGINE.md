# Chaos Engine

**Canon:** **no**  
**Drawer:** 00_MASTER_INDEX (map) · 14_AI_INTERACTIONS (ledger) · `crystal_platform/chaos/` (Built)  
**Updated:** 2026-09-20  
**Stamp:** Crystal — **Chaos Engine is a go**

## One line

Multi-seat fan-out over the live stack: one question → N intelligence seats → **cross-compare counts**. Not a verdict. Not Canon. Human publishes.

## Law

| Rule | Meaning |
| --- | --- |
| Models think | Seats are intelligence providers |
| TAI acts | EchoAgent (or later agents) execute turns |
| CrystalCore governs | Every seat turn goes through Core permission + route |
| Portal is gateway | Optional `/v1/gateway/chaos` + CLI |
| Counts ≠ verdicts | Unanimous silence is not permission |
| Connection ≠ merge | Seats stay separate; Manus ≠ roster bot |
| Core ≠ TAI | Chaos Engine is hub harness, not the OS |

## Built ● / Vision ○

| Piece | Status | Where |
| --- | --- | --- |
| HTTP providers + live stack | ● | `crystal_platform/intelligence/`, `orchestration.py` |
| ChaosEngine fan-out | ● | `crystal_platform/chaos/engine.py` |
| CLI | ● | `scripts/chaos/run.py` |
| Portal `/v1/gateway/chaos` | ● | `backend/portal/gateway.py` |
| Ledger drawer | ● | `14_AI_INTERACTIONS/chaos-ledger/` |
| Keyed live diverge | ○ | needs Secrets in a new Cloud Agent |
| Manus in Portal fan-out | ○ forbidden sync | Starline bus guest only |

## Default seats

| provider_id | bus | Roster |
| --- | --- | --- |
| `openai.chatgpt` | `gpt` | BOT-WEAVE-CHATGPT |
| `anthropic.claude` | `claude` | BOT-WEAVE-CLAUDE (historical) |
| `xai.grok` | `grok` | BOT-WEAVE-GROK (Explore only) |
| `deepseek` | `deepseek` | BOT-WEAVE-DEEPSEEK |
| `moonshot.kimi` | `kimi` | BOT-WEAVE-KIMI (proposed) |
| `google.gemini` | `gemini` | BOT-WEAVE-GEMINI |
| `local.open` | — | offline stub |

**Not in Portal fan-out:** Manus (Starline guest), BOT-WEAVE-GROK-BUILD (Build ≠ Explore).

## Run

```bash
python3 scripts/chaos/run.py --topic "Where is each seat?"
python3 scripts/chaos/align.py --strict
python3 -m unittest discover -s crystal_platform/tests -v
```

## Related

- Opening check: `14_AI_INTERACTIONS/2026-09-20-CHAOS-OPENING-WEAVE-CHECK.md`
- Increment 1: `14_AI_INTERACTIONS/2026-09-20-CHAOS-GO-INCREMENT-1.md`
- Stack: `00_MASTER_INDEX/STACK-SURFACE.md`
- Alive Weave: `00_MASTER_INDEX/ALIVE-WEAVE.md`

*Non Solus.*
