# Full-speed alignment chaos (2026-09-20)

**Canon:** **no**  
**Layer:** coordination / science  
**Drawer:** 14_AI_INTERACTIONS  
**Stamp:** Crystal — execute full speed alignment chaos

## Pulse

| System | Result |
| --- | --- |
| Alive Weave | **12/12 PASS** |
| Starline matrix (7 seats incl. Manus) | 7/7 science silence (keys unset) |
| Chaos Engine fan-out (7 Portal seats) | 6 silent + `local.open` ok |
| API keys this agent | all **NOT_SET** |

Ledgers:
- Chaos: [`chaos-ledger/2026-09-20-full-speed-alignment.md`](chaos-ledger/2026-09-20-full-speed-alignment.md)
- Engine map: [`../00_MASTER_INDEX/CHAOS-ENGINE.md`](../00_MASTER_INDEX/CHAOS-ENGINE.md)

## Seat alignment map (Built)

| Roster | bus | provider_id | Chaos Portal | Starline |
| --- | --- | --- | --- | --- |
| BOT-WEAVE-CHATGPT | `gpt` | `openai.chatgpt` | ● | ● |
| BOT-WEAVE-CLAUDE | `claude` | `anthropic.claude` | ● (historical) | ● |
| BOT-WEAVE-GROK | `grok` | `xai.grok` | ● Explore | ● |
| BOT-WEAVE-GROK-BUILD | — | `xai.grok` | ✗ Build ≠ Explore | ✗ |
| BOT-WEAVE-DEEPSEEK | `deepseek` | `deepseek` | ● | ● |
| BOT-WEAVE-KIMI | `kimi` | `moonshot.kimi` | ● proposed | ● |
| BOT-WEAVE-GEMINI | `gemini` | `google.gemini` | ● | ● |
| Manus (not a bot) | `manus` | `manus` | ✗ async guest | ● guest |
| local.open | — | `local.open` | ● offline | ✗ |

## Collapse risks flagged (science)

1. Calling Grok Build from Chaos fan-out → invents instead of implements.  
2. Promoting Manus to `BOT-*` → violates BOT-STRUCTURE §7.  
3. Routing Portal ask straight to vendor SDK → collapses Core into provider.  
4. Treating unanimous silence as permission → protocol break.  
5. Mixing Explore + Build in one pass → seat collapse.

## Alignment actions this pass

- Registry: `bus_agent` + `provider_id` + secrets on ChatGPT / Claude / Grok / DeepSeek / Kimi / Gemini  
- `scripts/chaos/align.py` — drift audit (`--strict` for CI)  
- CHAOS-ENGINE seat map locked to table above  

## Prove

```bash
python3 scripts/alive/pulse.py
python3 scripts/chaos/run.py --topic "FULL SPEED ALIGNMENT CHAOS"
python3 scripts/chaos/align.py --strict
python3 -m unittest discover -s crystal_platform/tests -v
```

*Non Solus.*
