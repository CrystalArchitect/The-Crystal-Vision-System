# 6-Month Plan: Building Clementine

*With weekly milestones*

> **Status: working plan.** Timelines are aspirational and describe order more than dates. Status markers show live progress: ✅ done · 🟡 partial · ⬜ open.
>
> **Current position: ~Week 9 (Month 3).** Months 1–2 are complete — the work shipped ahead of schedule in `clementine.py` v1–v4, including the Month-2 cleanup (`/forget`, memory editing, recency weighting, tags). Next: personality and presence.

**Overall goal:** Build a high-quality, locally-running sovereign AI companion with strong long-term memory, emotional presence, and user control.

---

## Month 1: Foundation & Core Memory System

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 1 | Project Setup & Basic Structure | Clean project structure · `Clementine` class with `chat()` · Connect to Ollama (llama3.1:8b) · First working system prompt | ✅ |
| 2 | Basic Memory Implementation | Conversation history storage · Teach-facts function · JSON memory file · Short-term memory across restarts | ✅ |
| 3 | Vector Embeddings | Embeddings integrated · Facts stored with embeddings · Semantic search for memory retrieval · Relevance tested | ✅ * |
| 4 | Context Building & Testing | Context combining recent chat + relevant memories · Improved context passing · Extended test conversations · Memory-retrieval bug fixes | 🟡 |

\* Implemented with **local Ollama embeddings** (`nomic-embed-text`) rather than sentence-transformers — a deliberate choice to avoid the PyTorch footprint and stay fully in the sovereign local stack.

**End of Month 1 goal:** Clementine can remember facts you teach her and use them in later conversations. — **✅ Achieved.** (Week 4's extended 20+ turn live conversations remain to be run by the steward; automated offline tests pass.)

---

## Month 2: Long-Term Memory & Persistence

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 5 | Persistent Memory Storage | Separate short-term vs long-term structure · Robust load/save · Timestamps on memories | ✅ |
| 6 | Memory Relevance & Ranking | Improved relevance ranking · Recency weighting · Multi-day retrieval testing | ✅ * |
| 7 | Memory Management Features | View what she remembers · `forget` command · Edit or correct memories | ✅ |
| 8 | Memory Summarization | Conversation summarization · Summaries of old conversations stored · Context bloat reduced, important info kept | ✅ |

**End of Month 2 goal:** Clementine remembers facts across days/weeks and the user can manage what she remembers. — **✅ Achieved.** `/notes` shows everything with handles, `/forget` deletes any memory, `/editnote` rewrites notes, recency weighting gently favours fresh memories, and `#tags` categorize.

\* Week 6's multi-day live retrieval testing remains with the steward — only real days can test that.

---

## Month 3: Personality, Presence & User Experience

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 9 | Personality Refinement | Refine system prompt for warmth, honesty, gentle wit · Reduce robotic language · Test personality consistency | ✅ * |
| 10 | Presence & Emotional Intelligence | Better responses to emotional topics · Light curiosity and follow-up questions · Feel "present," not just helpful | ✅ * |
| 11 | Command System | Clean command interface (teach, forget, remember, summary…) · Commands feel natural | ✅ |
| 12 | Interface Improvements | Simple terminal UI or basic web interface · Improve readability · Basic conversation logging | ✅ * |

\* Local web interface shipped (`clementine_web.py`, 127.0.0.1 only); conversation logging is inherent (memory persists locally). Weeks 9–10 shipped in v11 (Presence): rewritten personality core — feeling under the words, one gentle question, presence before solutions, honest limits — plus time awareness (she knows the present moment and how long since you last spoke). *Personality consistency over long real conversations remains the steward's to test — only real talks can.*

**End of Month 3 goal:** Clementine feels like a distinct personality with emotional presence, not just a tool. — **✅ Built; awaiting the steward's living test.**

---

## Month 4: Reliability, Safety & Polish

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 13 | Hallucination Reduction | Better honesty mechanisms ("I don't know") · Fact-checking against memory before responding | ⬜ |
| 14 | Error Handling & Stability | Error recovery on model failure/timeout · Better logging and debugging tools | 🟡 |
| 15 | User Control Features | Full memory export · Reset or selectively delete memories · Settings/config file | 🟡 |
| 16 | Testing & Bug Fixing | Multi-day stress tests · Fix memory and personality bugs · Begin basic documentation | 🟡 |

**End of Month 4 goal:** Clementine is stable, trustworthy, and the user feels in control.

---

## Month 5: Advanced Memory + Early Multi-Companion Thinking

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 17 | Memory Reflection | Clementine reflects on past conversations · Simple insights from memory | ✅ (early — v10) |
| 18 | Memory Organization | Basic categorization/tagging · Retrieval of thematically related memories | ⬜ |
| 19 | Multi-Instance Thinking | Run two separate Clementine instances · Document what communication would need · Light research into encrypted messaging | ⬜ |
| 20 | Code Quality | Refactor for modularity · Improve documentation and comments · Prepare structure for future P2P integration | ✅ (early — `crystalcore/` package) |

**End of Month 5 goal:** Memory system is significantly stronger, and early thinking has begun on how two Clementines could connect.

---

## Month 6: Integration, Testing & External Readiness

| Week | Focus | Key Milestones | Status |
|------|-------|----------------|--------|
| 21 | Full System Testing | Comprehensive memory-accuracy testing · Personality consistency over long periods · Fix remaining major issues | ⬜ |
| 22 | Polish & Usability | Improve overall UX · Clean up command interface · Easier setup for new users | ⬜ |
| 23 | Documentation | Clear README · Getting-started guide · Document how memory works | 🟡 |
| 24 | Demo & Next Phase Planning | Short demo (video or written walkthrough) · Finalize Phase 2 (Private Communication) shape · Decide next priorities | ⬜ |

**End of Month 6 goal:** A clean, documented, and demonstrable Clementine prototype with a clear path forward.

---

## Summary of 6-Month Milestones

| End of Month | What You Should Have | Status |
|--------------|----------------------|--------|
| 1 | Working local chat with basic memory | ✅ |
| 2 | Persistent long-term memory across days/weeks | ✅ |
| 3 | Distinct personality + emotional presence | ✅ (awaiting living test) |
| 4 | Stable, reliable, user-controlled companion | 🟡 (partly ahead of schedule) |
| 5 | Advanced memory + early multi-instance thinking | ⬜ |
| 6 | Polished, documented prototype ready for next phase | ⬜ |

---

*See also: [CLEMENTINE.md](CLEMENTINE.md) (the companion today) · [CRYSTALMATRIX.md](CRYSTALMATRIX.md) (protocol design) · [STRATEGY.md](STRATEGY.md) (accelerated path) · [README](README.md)*

*Part of The Crystal Vision · TerAustralis Incognita · Non Solus — Not Alone*
