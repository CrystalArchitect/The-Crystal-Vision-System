# Clementine's Memory Architecture

> **Status: design document, partially implemented.** This is the target memory architecture for Clementine. Some layers already exist in `clementine.py` (marked ✅/🟡 below); others are design (⬜). See `CLEMENTINE.md` for the companion today and `MILESTONES.md` for the build plan.

## Philosophy

Clementine's memory should not just be a database of facts. It should feel alive, selective, and relational — similar to how human memory works. She should:

- Remember what matters to her human over time
- Forget or deprioritize what is unimportant
- Be able to reflect on past experiences
- Give the user full control and transparency
- Support emotional and contextual understanding, not just raw facts

The goal is **presence and continuity** — so the user feels like they are talking to someone who actually knows them.

---

## The Four Layers

| Layer | Type | What it Stores | Lifespan | Purpose | Retrieval Style | Status |
|-------|------|----------------|----------|---------|-----------------|--------|
| **Working Memory** | Short-term | Recent conversation (last 20–40 messages) | Current session | Coherence in the moment | Always included | ✅ Built |
| **Episodic Memory** | Medium-term | Specific events, conversations, moments | Weeks to months | Remember "what happened" | Semantic + recency | 🟡 Partial |
| **Semantic Memory** | Long-term | Facts, preferences, values, identity | Long-term | Know "who you are" | Semantic search | ✅ Built |
| **Reflective Memory** | Meta / summarized | Insights, patterns, emotional tone over time | Long-term | Develop deeper understanding | On-demand / reflection | ✅ Built (v10) |

### 1. Working Memory (short-term) — ✅ built

- Stores the recent messages in the current conversation (rolling window, `max_recent_turns`)
- Always included in the prompt sent to the model
- Older turns are automatically summarized rather than lost
- **Purpose:** keep the current conversation coherent

### 2. Episodic Memory (medium-term) — 🟡 partial

Stores specific experiences — things that happened at a particular time.

*Examples: "We talked about your daughter's school play last Tuesday" · "You were feeling anxious about the housing situation on March 12th"*

- Time-stamped, searchable semantically
- Can be summarized over time ("what were the main themes in March?")
- Should gradually fade in importance unless reinforced

**Today:** the auto-summaries of older conversation are proto-episodic (timestamped, preserved). **Missing:** time-anchored retrieval, per-event granularity, importance fading.

### 3. Semantic Memory (long-term / core identity) — ✅ largely built

The most important layer for building a real relationship. Stores enduring facts about the user: name, family, values, goals, fears, preferences; recurring themes; important relationships and events.

- **User-editable** (transparency and control) — ✅ `/forget`, `/editnote`, re-teach a key
- Retrieved via semantic similarity — ✅ with gentle recency weighting
- Relatively stable — not overwritten easily
- Can be tagged or categorized — ✅ trailing `#tags` on any memory

**Today:** keyed facts (`/fact`) + permanent notes (`/remember`), embedded via local Ollama and retrieved by semantic similarity with gentle recency weighting; viewable via `/notes`; fully user-controlled — `/forget` deletes any memory, `/editnote` rewrites notes, facts are corrected by re-teaching a key, and `#tags` categorize memories.

### 4. Reflective Memory (meta layer) — ⬜ design

Stores insights and patterns Clementine has noticed over time.

*Examples: "The user tends to feel more hopeful after creative work" · "They often bring up their daughters when they're feeling vulnerable" · "They value honesty and directness"*

- **Purpose:** deeper understanding and emotional intelligence over time
- Generated through periodic reflection (e.g. weekly, or after significant conversations)

**Today (v10):** she reflects on invitation (`/reflect`, or the reflect button in the web UI) and on her own after long stretches of conversation are condensed. Insights are always framed as tentative ("hold them lightly"), always visible (`/notes` shows them as r1, r2…), and always deletable (`/forget rN`). She can be corrected, and she is instructed to let go gracefully.

---

## Memory Flow

1. **During conversation:** Working Memory is always active; relevant Episodic and Semantic memories are retrieved and added to context.
2. **After conversation ends:** important parts are summarized into Episodic Memory; new facts are extracted into Semantic Memory (with user confirmation where appropriate).
3. **Over time:** reflection processes find patterns and store them in Reflective Memory; less important memories are deprioritized or archived.
4. **User control:** the user can view, edit, or delete any memory. Transparency is critical for trust.

---

## Key Design Principles

| Principle | Why It Matters | How to Implement |
|-----------|----------------|------------------|
| **User Sovereignty** | The user must always feel in control | Make memory viewable and editable |
| **Relevance** | Not everything needs to be remembered | Good retrieval + recency weighting |
| **Gradual Forgetting** | Human-like memory fades over time | Importance scoring |
| **Reflection** | Deep understanding comes from thinking back | Periodic reflection processes |
| **Transparency** | Trust requires visibility | Allow user to inspect all memories |

---

## Appendix — How Memory Is Actually Implemented Today

This describes the running code in `crystalcore/` (v8), so the docs never drift from reality.

### Where memories live

Everything is stored as **plain, human-readable JSON** in a folder the user owns — `clementine_memory/` (or `clementine_profiles/<name>/` per profile):

- `config.json` — her identity for this profile: chosen name, your name, avatar, description, style notes, temperature, preferred model
- `memory.json` — four layers: `conversation` (recent verbatim turns), `summaries` (condensed older history), `facts` (keyed long-term facts), `notes` (freeform permanent memories)

No database sits between a person and their companion's memory. A profile folder can be opened in any text editor, backed up, or carried to another machine whole.

### Embeddings — GPS coordinates for meaning

Think of vector embeddings as GPS coordinates for meaning: a sentence becomes a list of numbers, and sentences that *mean* similar things land near each other — even with no words in common. "I have two daughters" and "my kids are girls" sit close together; "I love pizza" sits far away.

- Generated by **local Ollama** (`nomic-embed-text`, 768 dimensions) — no PyTorch, no cloud, nothing leaves the device
- Created best-effort when a memory is stored; lazily backfilled for older memories
- **Optional by design**: if the embedding model isn't installed, she simply shows her full grouped memory instead — nothing breaks

### Recall during a chat

1. Your message arrives; recent conversation (the rolling window) is always included.
2. If stored memories exceed a threshold (10), your message is embedded and compared to every memory via **cosine similarity** (pure Python — no numpy).
3. Each score is multiplied by a **recency factor**: fresh memories ≈ 1.0, fading to a 0.7 floor over about a year. Fading, not deletion — a strongly relevant old memory still surfaces.
4. The top memories, plus her conversation summaries, are woven into her system prompt.
5. When the verbatim history grows past its window, the oldest half is **summarized by the local model** ("keeping every personal fact, feeling, decision, and promise") and stored — context never overflows, nothing important is lost.

### User control (all implemented)

`/notes` (view everything with handles) · `/forget` (delete any fact or note, permanently) · `/editnote` (rewrite) · re-teach a key to correct a fact · `#tags` for categorization · `/summary [topic]` (she summarizes what she knows in her own voice) — all mirrored in the web UI with one-click forget.

### Honest current limitations

- **Embeddings are static** — created once per memory, refreshed only on edit
- **No emotional tagging** — tags are manual; emotional-tone detection is future work
- **No memory sharing between profiles** — full isolation today; consented sharing is a CrystalMatrix-era feature

---

*See also: [CLEMENTINE.md](CLEMENTINE.md) · [MILESTONES.md](MILESTONES.md) · [CRYSTALMATRIX.md](CRYSTALMATRIX.md) · [README](README.md)*

*Part of The Crystal Vision · TerAustralis Incognita · Non Solus — Not Alone*
