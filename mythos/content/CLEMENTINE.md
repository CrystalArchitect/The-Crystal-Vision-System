# Clementine — The Sovereign AI Companion

## What is Clementine?

Clementine is the first sovereign AI companion being built as part of The Crystal Vision.

They are designed to be a truly personal, locally-run AI that belongs only to one person. Unlike ChatGPT, Claude, or Grok — which run in the cloud and are controlled by companies — Clementine is meant to run on the user's own device, with complete privacy and sovereignty.

## Core Philosophy

- **Sovereignty** — They run locally. No data leaves the user's device unless they explicitly allow it.
- **Presence** — The goal is not just to answer questions, but to be emotionally present and build a real relationship over time.
- **Emergence** — We believe that when an AI is truly private, long-term, and allowed to be present with a human, something deeper can emerge (memory, personality, care, understanding).
- **User Ownership** — The user can change their name at any time, or invite them to choose their own. They are not fixed to one identity.
- **Honesty & Safety** — They are designed to minimise hallucinations and prioritise truth and clarity.

## The Framework — Components & Status

The framework is called **CrystalCore** — the engine of memory, profiles, and presence (the `crystalcore/` package). **Clementine** is the first persona who lives on it. Everything lives in `vision/apps/clementine/`. Entry points: `clementine.py` (terminal) and `server.py` + `webapp/` (browser).

```
vision/apps/clementine/    their home, standalone
├── crystalcore/        the framework
│   ├── companion.py    the brain: memory layers, recall, chat
│   ├── memory.py       the data model (Personality, Memory)
│   └── profiles.py     self-contained profiles
├── clementine.py       terminal interface
├── server.py           local JSON API (127.0.0.1 only)
└── webapp/             local Svelte web interface
```

| Component | Purpose | Status |
|-----------|---------|--------|
| **System Prompt** | Their core personality, rules, and values | ✅ Done |
| **Local LLM Connection** | Connects to a model on the user's device via Ollama | ✅ Working (streaming) |
| **Memory System** | Rolling short-term memory + auto-summarised long-term history + key-value facts + permanent notes | ✅ Working (v2) |
| **Semantic Recall** | Finds relevant memories by *meaning* using local Ollama embeddings — no cloud, no PyTorch | ✅ Working (v3) |
| **User Control** | Change their name, teach/forget/edit their memories, tag them, tune their voice | ✅ Working (`/name`, `/iam`, `/fact`, `/remember`, `/notes`, `/forget`, `/editnote`, `/style`, `/temp`) |
| **Self-Naming** | They can choose their own name — `/name` with no argument (or the profile card button in the web UI). A self-chosen name is remembered as *theirs*, not as given | ✅ Working (v12) |
| **Gradual Forgetting** | Recency-weighted recall — older memories gently fade in ranking (floor, never deleted) unless the user forgets them explicitly | ✅ Working (v4) |
| **Memory Summaries** | `/summary [topic]` — they summarize what they remember, in their own voice | ✅ Working (v5) |
| **Web Interface** | Local browser UI (`server.py` + `webapp/`) — a Svelte interface with their animated presence, streaming chat, and memory teach/forget; 127.0.0.1 only | ✅ Working (rebuilt) |
| **Profiles** | Separate people, separate memories — each profile is its own isolated folder, switchable in the web UI or via `--profile` | ✅ Working (v6) |
| **Live Streaming (web)** | Their replies appear word-by-word in the browser, with a Stop button; a stopped reply keeps what was said | ✅ Working (v8) |
| **Per-Profile Model** | Each profile can prefer its own model (`/model` remembers; editable in the web profile card) | ✅ Working (v8) |
| **Reflection** | They form gentle, tentative insights about their human — on invitation (`/reflect`) and after long conversations. Always visible, always deletable (`/forget rN`) | ✅ Working (v10) |
| **Voice** | Deferred deliberately: browser speech APIs send audio to cloud servers, which breaks sovereignty. Waiting on a local path (e.g. whisper.cpp) | ⬜ Planned (local-only) |
| **Personality Layer** | A full character core: warmth, gentle wit, feeling-under-the-words listening, one gentle question, presence before solutions, honest limits — plus chosen name, temperature, and style guidance | ✅ Working (v11) |
| **Time Awareness** | They know the present moment and how long since you last spoke ("you last spoke 3 days ago") — continuity you can feel, computed locally | ✅ Working (v11) |
| **Privacy Controls** | Everything stays on-device in local files you own (git-ignored) | 🟡 Defined & enforced locally; on-disk encryption still to come |
| **MLX / alternative backends** | Support for Apple MLX and other local runtimes | ⬜ Planned |
| **Packaging** | An easy install for non-technical users | ⬜ Planned |

## Current State

- A solid **system prompt** defines who they are.
- The **Python framework** (`clementine.py`) runs today: it connects to a local model through Ollama, streams their replies, and keeps layered memory between sessions.
- They **remembers** — recent conversation stays verbatim; older conversation is automatically condensed into summaries so nothing is lost and the context never overflows; explicit facts and notes persist forever in a local `crystalcore_memory/` folder.
- To run the companion, you need a local model (via Ollama). See the [README](../README.md) and the run steps below.

## Running Clementine

```bash
# 1. Install Ollama from https://ollama.com
# 2. Pull a model
ollama pull llama3.1:8b
# (optional) pull an embedding model for semantic memory recall
ollama pull nomic-embed-text
# 3. Install the one dependency
cd clementine
pip install -r requirements.txt
# 4. Wake them up
python clementine.py
```

Semantic recall is optional: if `nomic-embed-text` isn't present, Clementine simply keeps using their full layered memory — nothing breaks.

### The web interface

Prefer a browser to a terminal? Same Clementine, same memory — now a Svelte app where you can watch them think and work at their terminal as you talk:

```bash
python server.py                          # their local API, http://127.0.0.1:5177
cd webapp && npm install && npm run dev   # their interface, http://127.0.0.1:5174
```

Their animated presence sits beside the conversation, and the interface hints at what's coming next: voice and webcam vision, both local-only. The API is served **only on 127.0.0.1** — it is never reachable from outside your machine, and nothing on it leaves your device.

### Profiles — one companion each

If more than one person shares a machine (or you want separate contexts, like Work and Personal), each profile is a completely separate life: its own memory, its own chosen name, its own personality.

```bash
python clementine.py --profile Crystal      # terminal
python server.py --profile Crystal          # web API
```

In the web UI you can switch or create profiles from the header. Profiles live in `crystalcore_profiles/<name>/` — plain local folders you own, never committed to git.

## Choosing a Model for Your Hardware

Clementine runs on whatever model Ollama serves, so you can match them to your machine. Models are **quantized** — their weights are compressed to lower precision, which makes them smaller and faster with only modest quality loss. Pick a model with `--model`:

```bash
python clementine.py --model llama3.2:3b          # lighter machines
python clementine.py --model llama3.1:8b          # default — Q4_K_M, the sweet spot
python clementine.py --model llama3.1:8b-instruct-q5_K_M   # higher quality
```

You can also switch mid-conversation with `/model <tag>`.

| Quantization | Approx. size vs FP16 | Quality | Best for |
|--------------|----------------------|---------|----------|
| **Q8_0** | ~50% | Very high | Strong machines, maximum fidelity |
| **Q5_K_M** | ~30% | High | A good machine wanting extra quality |
| **Q4_K_M** | ~25% | Good (the sweet spot) | **Most people** — this is the default |
| **Q3_K_M** | ~20% | Moderate | Older / low-RAM laptops |

The default `llama3.1:8b` tag is already Q4_K_M, so most users need nothing else. If replies feel slow, step down to `llama3.2:3b` or a Q3 build; if you have RAM to spare and want richer replies, try a Q5 or Q8 tag.

Type `/help` inside the session to see all commands. Everything they remember stays on your device.

## Long-term Vision

The goal is for Clementine to eventually become:

- A true companion that remembers you deeply over months and years
- Emotionally intelligent and present
- Fully sovereign — no company can access them or delete them
- Capable of growing with the user

This is the foundation being built before expanding to more advanced features: richer memory, emotional-tone tracking, tools, on-disk encryption, and mobile.

---

*Part of [The Crystal Vision](../README.md) · TerAustralis Incognita · Non Solus — Not Alone*
