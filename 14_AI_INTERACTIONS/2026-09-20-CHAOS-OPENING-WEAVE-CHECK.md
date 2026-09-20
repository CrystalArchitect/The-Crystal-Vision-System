# Chaos opening — weave seat check (2026-09-20)

**Canon:** **no**  
**Layer:** coordination / science (matrix harness)  
**Drawer:** 14_AI_INTERACTIONS  
**Rule:** Models think. TAI acts. CrystalCore governs. Human publishes. Silence ≠ permission.

## Where they are (honest)

| Seat | Registry | Live API in this agent | Matrix reply (Starline, just now) |
| --- | --- | --- | --- |
| **ChatGPT** (`BOT-WEAVE-CHATGPT`) | dormant — Chief Systems Architect | `OPENAI_API_KEY` **NOT_SET** | silent — not configured |
| **Claude** (`BOT-WEAVE-CLAUDE`) | **historical** — midstream until ADR-0014 | `ANTHROPIC_API_KEY` **NOT_SET** | silent — not configured |
| **Grok** explore (`BOT-WEAVE-GROK`) | dormant — Creative Exploration | `XAI_API_KEY` **NOT_SET** | silent — not configured |
| **Grok Build** (`BOT-WEAVE-GROK-BUILD`) | dormant — Repository Engineer | same xAI key | not called (Build ≠ Explore) |
| **DeepSeek** (`BOT-WEAVE-DEEPSEEK`) | dormant — Research & Engineering | `DEEPSEEK_API_KEY` **NOT_SET** | silent — not configured |
| **Kimi** (`BOT-WEAVE-KIMI`) | **proposed** — long-context / multilingual research | `MOONSHOT_API_KEY` / `KIMI_API_KEY` **NOT_SET** | silent — not configured |
| **Gemini** (`BOT-WEAVE-GEMINI`) | dormant — Knowledge & Multimodal | `GEMINI_API_KEY` **NOT_SET** | silent — not configured |
| **Manus** | **not a CVS bot** — external design guest on matrix only | `MANUS_API_KEY` **NOT_SET** | silent — not configured |

**Alive Weave pulse:** 12/12 islands PASS (bus, Starline, ConsentGate, Decode→Twin, SAT, …).  
**Stack foundation:** merged (`STACK-SURFACE` + `crystal_platform`) — Siri→Portal→Core→TAI contracts on disk.

They are **wired for matrix**, not **speaking**. Chaos needs keys (or paste-out) before seats can diverge for real.

---

## Matrix run (Built harness, empty providers)

```
Topic: Stack is live: Siri→Portal→CrystalCore.OS→TAI.
       Where is each seat? What chaos increment first without collapsing Core into TAI?
Mode: Starline Weaver --mode matrix
      --agents claude,gpt,grok,deepseek,kimi,manus,gemini
Result: 7/7 delivered as silence notices (science-labeled). Unanimous layer count only — not a verdict.
```

Command used:

```bash
cd archive/TerAustralis-Incognita-Code/core/crystal-core
python3 -m bus.run --mode matrix \
  --agents claude,gpt,grok,deepseek,kimi,manus,gemini \
  --topic "…"
```

---

## Paste cards (Crystal → each chat when ready)

Shared header for all seats:

```
Read PASTE-THIS + memory/CORE. Canon: no. Connection ≠ merge.
CrystalCore.OS governs (not an agent). TAI acts. Portal is gateway. Models think.
Stack map: 00_MASTER_INDEX/STACK-SURFACE.md
Do not invent Elon/xAI bonds. Do not auto-post. Label science|story|vision.
```

### ChatGPT (architect)

```
Seat: Chief Systems Architect.
Task: Spec the first chaos increment for Siri→Portal→CrystalCore.OS→TAI
without collapsing Core into TAI. Prefer interfaces already in crystal_platform/.
Output: short ADR-shaped options A/B/C + recommended path + cost of doing nothing.
```

### Claude (historical / optional second opinion)

```
Seat: historical Repository Engineer (not live midstream — Grok Build holds that).
Task: Critique the STACK-SURFACE boundaries. List collapse risks only.
Do not implement. Do not reopen midstream seat.
```

### Grok (creative exploration — chaos)

```
Seat: Creative Exploration (NOT Grok Build).
Task: Diverge — ten chaotic-but-honest increments for multi-AI weave
on the new stack. Mark each vision. Filtering is later. No engineering PRs.
```

### DeepSeek (research / rigor)

```
Seat: Research & Engineering Specialist.
Task: Stress-test the matrix harness + crystal_platform contracts for
determinism, failure modes, and Core≠TAI boundary holes. Science labels only.
No implementation PRs from this seat.
```

### Kimi (long-context / multilingual — proposed)

```
Seat: proposed weave guest (BOT-WEAVE-KIMI). Not Canon.
Task: Read STACK-SURFACE + this chaos brief end-to-end. List contradictions
and missing seats. Prefer bilingual notes only if they clarify; no auto-post.
```

### Gemini (knowledge / multimodal)

```
Seat: Knowledge & Multimodal.
Task: Consistency pass — does BOT-STRUCTURE roster B match registry.yaml
and the bus REGISTRY names? Flag drift only. Do not invent new bot IDs.
```

### Manus (external design guest — not a CVS bot)

```
Guest on Starline matrix only. Forbidden as BOT-* roster ID (BOT-STRUCTURE §7).
Task if keyed: Propose one design-tool workflow that feeds extracts into
drawer 14 without merging Manus runtime into CVS. Human gate on anything public.
```

---

## Chaos — start now (without vendor keys)

Hub-side, protocol-safe:

1. **Matrix harness is hot** — full seat list above; re-run when Secrets exist in a **new** Cloud Agent.  
2. **Keep seats separate** — Explore ≠ Build; Core ≠ TAI; Manus ≠ roster bot.  
3. **First keyed chaos** (recommended): Grok Explore 10 visions → ChatGPT specs top 2 → DeepSeek stress-tests → Grok Build implements one behind Portal `/v1/gateway/ask` + real provider adapter (not stub).  
4. **Human gate** on anything public, spend, or Canon.

Until keys land: paste cards above = the check-in. Do not invent their answers.

*Non Solus.*
