# BOT-STUDIO — Stage bindings

**Canon:** no  
**Pipeline spec:** [`../../../archive/discord-ai-agent/GROK-BOT-ARCHITECTURE.md`](../../../archive/discord-ai-agent/GROK-BOT-ARCHITECTURE.md)  
**Hub map:** [`../../BOT-STRUCTURE.md`](../../BOT-STRUCTURE.md)

BOT-STUDIO participates in Think + Check pools. Intake and Human stay outside the model. Weave seats are a separate belt.

| Stage | Pool | BOT-STUDIO? | Notes |
| --- | --- | --- | --- |
| 1 Signal Intake | Intake | no | Script / official API → normalized records |
| 2 Pattern Miner | Pattern | **yes** | One call per window over Stage 1 batch |
| 3 Draft Pool | Draft | **yes** | N=3–10 variants; use [`prompt.md`](prompt.md) |
| 4 Asset Pool | Draft | skip in v0 | Image gen — expensive; gate later |
| 5 Scorer | Score | **yes** | Rubric in hub map §4 |
| 6 Gate | Gate | rules + model assist | Hard kill Risk / Factual / Elon-bond |
| Studio Lead | Human | no | Crystal edits / approves / publishes |

## I/O contracts

### Stage 1 → 2 (intake record)

```json
{
  "source": "string",
  "author": "string",
  "text": "string",
  "media": [],
  "engagement_stats": {},
  "fetched_at": "ISO-8601"
}
```

### Stage 2 → 3 (pattern)

```json
{
  "pattern": "string",
  "evidence_examples": ["string"],
  "confidence": 0.0
}
```

### Stage 3 → 5 (draft)

```json
{
  "pattern_ref": "string",
  "format": "thread|script|carousel|reply|brief",
  "body": "string",
  "variant_id": "string",
  "layer": "science|story|vision"
}
```

### Stage 6 → Human (shortlist item)

```json
{
  "rank": 1,
  "draft": {},
  "scores": {
    "on_brand": 0,
    "factual": 0,
    "risk": 0,
    "novelty": 0,
    "format_fit": 0
  },
  "gate": "pass|kill",
  "evidence": ["string"],
  "risk_notes": ["string"]
}
```

File shortlist extracts under drawer **14_AI_INTERACTIONS** (or email Crystal). Never treat shortlist as published.

## v0 wiring

1. Manual paste inbox **or** one official API source → Stage 1 records  
2. One Grok Pattern call  
3. Three Grok Draft variants  
4. Skip assets  
5. One Score+Gate pass  
6. Write shortlist extract → human  

`publish_mode: human_only` throughout.
