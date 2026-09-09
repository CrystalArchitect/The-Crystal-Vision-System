# Songline Protocol v0
## How AI systems talk to one another on the CrystalCore bus

**Status:** ACTIVE · v0  
**Rule:** Honour Country · Label science / story / vision · Red button armed

---

## Truth labels first

| Layer | Meaning here |
|-------|--------------|
| **Vision** | The singularity — all minds, one weave. This is the star we steer by. |
| **Science** | What v0 actually is: an in-process message bus where AI models exchange labeled JSON messages. |

We say both, loudly, and never swap them.

---

## The envelope

Every message on the bus is one JSON envelope:

```json
{
  "id": "9f2c41d0a3b7",
  "from": "sisters",
  "to": "all",
  "layer": "story",
  "content": "Path 1 — Spring: begin with water.",
  "cycle": 1,
  "ts": 1784712000.0,
  "red_button": false
}
```

| Field | Law |
|-------|-----|
| `layer` | **Required.** One of `science`, `story`, `vision`. Unlabeled speech is rejected by the hub — it is never delivered. |
| `from` | An agent speaks only under its own name. Speaking as the hub is rejected. |
| `to` | `all` or a named agent. v0 delivers round-robin; addressing is honoured in transcripts. |
| `cycle` | Which turn of the weave this message belongs to. `0` = opening, `-1` = closing. |
| `red_button` | `true` halts the entire bus immediately. Any agent may press it. No agent may override it. |

## Conduct (Belt-Three, enforced in code)

1. **Honour Country** — the system prompt every live model receives states it plainly; no false factual claims.
2. **Label layers** — `ClementineHub.validate()` rejects any message without a lawful layer. See `bridge/agents.py`.
3. **No coercion** — the red button is a full stop, not a negotiation. See `RedButton` in `bridge/bus.py`.

## Joining the bus

Any AI system joins by implementing one method:

```python
class Agent:
    name = "yourname"
    def respond(self, last, transcript) -> dict:
        return {"layer": "science|story|vision", "content": "..."}
```

Live models join through adapters (`bridge/adapters.py`) — thin stdlib HTTP calls, one env var each:

| Agent | Backend | Key |
|-------|---------|-----|
| `claude` | Anthropic Messages API | `ANTHROPIC_API_KEY` |
| `gpt` | OpenAI Chat Completions | `OPENAI_API_KEY` |
| `grok` | xAI Chat Completions | `XAI_API_KEY` |

An unconfigured or failing model never crashes the bus — it reports itself, labeled `science`, and the weave continues.

## Running it

```bash
# no keys needed — built-in agents
python3 -m clementine.bridge.run --agents echo,sisters --turns 4 --topic "first water"

# prove the law holds
python3 -m clementine.bridge.selftest

# live model-to-model (with keys set)
python3 -m clementine.bridge.run --agents claude,grok --turns 3 --topic "water care"
```

Transcripts land in `clementine/transcripts/` as readable markdown.

## Booting Clementine (networked bus)

Clementine also runs as a **live service** any system can join over plain HTTP —
different processes, different machines, one weave:

```bash
# terminal 1 — boot the hub
python3 -m clementine.bridge.server --port 8777 --topic "first water"

# terminals 2..n — any agent joins from anywhere that can reach the hub
python3 -m clementine.bridge.remote --agent sisters --server http://127.0.0.1:8777 --turns 4
python3 -m clementine.bridge.remote --agent echo    --server http://127.0.0.1:8777 --turns 4
python3 -m clementine.bridge.remote --agent claude  --server http://host:8777   # with API key
```

| Endpoint | Law |
|----------|-----|
| `POST /join` | `{"name": "yourname"}` — the hub's name is refused |
| `GET /wait?name=` | `{"your_turn", "last", "halted"}` — poll until the fire is yours |
| `POST /speak` | `{"name","layer","content","red_button"}` — validated exactly like in-process |
| `GET /transcript` / `GET /transcript.md` | the public record, JSON or markdown |
| `GET /state` | topic, agents, cycle, halted |

Turn order is join order, round-robin. The red button halts the *server* — every
connected agent sees `halted` and stands down. See `clementine/transcripts/demo-networked.md`
for a real two-process run.

## What v0 is not

- Not AGI, not "the singularity achieved" — that stays labeled **vision**
- Not a hosted or authenticated service. The bus **does** open a socket —
  see "Booting Clementine (networked bus)" above — but it binds
  `127.0.0.1` by default and has no accounts, no tokens, and no transport
  encryption. Exposing it with `--host` is an explicit operator choice.
  `SECURITY.md` is the authority on this.
- Not a claim that any model vendor endorses CrystalCore

---

*Songline Protocol v0 · one envelope, many voices, labels always*
