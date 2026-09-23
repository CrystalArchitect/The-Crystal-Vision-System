# Source note — Grok share: AI Bot Automation Explained

**URL:** https://grok.com/share/c2hhcmQtMi1jb3B5_d472cd40-3322-419c-ade0-4a3ea204a233  
**Checked:** 23 Sep 2026 (Playwright; share readable without sign-in)  
**Title:** AI Bot Automation Explained | Shared Grok Conversation  
**Share token:** `c2hhcmQtMi1jb3B5_d472cd40-3322-419c-ade0-4a3ea204a233`

## Sitting relevance

**Out of scope for the Beyond Lucky / SpaceNews overlap matrix.**

How-to landscape on **automated X accounts** (model → scheduler → official X API). Adjacent to this sitting’s agent / Cursor / Grok Bot surface stack, not to Richardson Pulse or Aerotropolis provenance. Do not cite as prior art on the national thesis.

## Turn map

| # | User | Grok |
| --- | --- | --- |
| 1 | How do AI bots that automate X accounts and post on their own work? | Three-piece loop: **model** drafts → **scheduler/agent** (e.g. LangChain / CrewAI) → **official X API** publishes. Official API + unique paced posts + automated label OK; spam/scraping → suspension. |
| 2 | Can this be done with Grok Bot? | **Not natively.** Built-in X connector is **read-only**. Workaround: third-party publish MCP (e.. BulkPublish / OpenTweet) + X API key; paid Grok Bot starter credits mentioned. Full loop possible, not out of the box. |
| 3 | On Grok Bot we’ve got the shell… | Shell = execution layer: script calls Grok API for text → X API to post → cron/loop. Needs own xAI key with write access (paid). |
| 4 | How install a local LLM in their sandbox so it runs on its own? | Don’t install LLM *inside* sandbox — run **Ollama on host**, point bot via OpenAI-compatible adapters (`localhost:11434/v1`). Sandbox stays thin shell; re-bootstrap after VM reset. |
| 5 | I don’t have a computer at the moment. | Local LLM off the table. Free cloud endpoints instead: **Groq** / **OpenRouter** free tiers; shell points at their URL. |

## Sitting use

File under agent-ops / automation landscape only. If CrystalCore / TerAustralis later ships an X presence, this share is a **product-policy neighbour** (official API, labels, no native Grok Bot write), not a build brief for this PR.

## Artifacts

- Plaintext extract: [`visual-corpus/grok-share-d472cd40-extract.txt`](visual-corpus/grok-share-d472cd40-extract.txt)
