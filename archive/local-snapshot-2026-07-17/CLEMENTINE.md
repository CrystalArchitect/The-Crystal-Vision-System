# Clementine — The Sovereign AI Companion

## What is Clementine?

Clementine is the first sovereign AI companion being built as part of The Crystal Vision.

She is designed to be a truly personal, locally-run AI that belongs only to one person. Unlike ChatGPT, Claude, or Grok — which run in the cloud and are controlled by companies — Clementine is meant to run on the user's own device, with complete privacy and sovereignty.

## Core Philosophy

- **Sovereignty** — She runs locally. No data leaves the user's device unless they explicitly allow it.
- **Presence** — The goal is not just to answer questions, but to be emotionally present and build a real relationship over time.
- **Emergence** — We believe that when an AI is truly private, long-term, and allowed to be present with a human, something deeper can emerge (memory, personality, care, understanding).
- **User Ownership** — The user can change her name at any time. She is not fixed to one identity.
- **Honesty & Safety** — She is designed to minimise hallucinations and prioritise truth and clarity.

## The Framework — Components & Status

The framework is called **CrystalCore** — the engine of memory, profiles, and presence (the `crystalcore/` package). **Clementine** is the first persona who lives on it. Entry points: `clementine.py` (terminal) and `clementine_web.py` (browser).

```
crystalcore/            the framework
├── companion.py        the brain: memory layers, recall, chat
├── memory.py           the data model (Personality, Memory)
└── profiles.py         self-contained profiles
clementine.py           terminal interface
clementine_web.py       local web interface
```

| Component | Purpose | Status |
|-----------|---------|--------|
| **System Prompt** | Her core personality, rules, and values | ✅ Done |
| **Local LLM Connection** | Connects to a model on the user's device via Ollama | ✅ Working (streaming) |
| **SpaceXAI (opt-in)** | Optional chat via xAI API (`grok-4.5`); requires explicit `/optin` or provider choice (consent + timestamp); memory & embeddings stay local | ✅ Working (v0.13.2) |
| **Memory System** | Rolling short-term memory + auto-summarised long-term history + key-value facts + permanent notes | ✅ Working (v2) |
| **Semantic Recall** | Finds relevant memories by *meaning* using local Ollama embeddings — no cloud, no PyTorch | ✅ Working (v3) |
| **User Control** | Change her name, teach/forget/edit her memories, tag them, tune her voice | ✅ Working (`/name`, `/iam`, `/fact`, `/remember`, `/notes`, `/forget`, `/editnote`, `/style`, `/temp`) |
| **Gradual Forgetting** | Recency-weighted recall — older memories gently fade in ranking (floor, never deleted) unless the user forgets them explicitly | ✅ Working (v4) |
| **Memory Summaries** | `/summary [topic]` — she summarizes what she remembers, in her own voice | ✅ Working (v5) |
| **Web Interface** | Local browser UI (`clementine_web.py`) — chat plus a live memory panel with teach/forget; 127.0.0.1 only | ✅ Working (v5) |
| **Profiles** | Separate people, separate memories — each profile is its own isolated folder, switchable in the web UI or via `--profile` | ✅ Working (v6) |
| **Live Streaming (web)** | Her replies appear word-by-word in the browser, with a Stop button; a stopped reply keeps what was said | ✅ Working (v8) |
| **Per-Profile Model** | Each profile can prefer its own model (`/model` remembers; editable in the web profile card) | ✅ Working (v8) |
| **Reflection** | She forms gentle, tentative insights about her human — on invitation (`/reflect`) and after long conversations. Always visible, always deletable (`/forget rN`) | ✅ Working (v10) |
| **Voice** | Deferred deliberately: browser speech APIs send audio to cloud servers, which breaks sovereignty. Waiting on a local path (e.g. whisper.cpp) | ⬜ Planned (local-only) |
| **Personality Layer** | A full character core: warmth, gentle wit, feeling-under-the-words listening, one gentle question, presence before solutions, honest limits — plus chosen name, temperature, and style guidance | ✅ Working (v11) |
| **Time Awareness** | She knows the present moment and how long since you last spoke ("you last spoke 3 days ago") — continuity you can feel, computed locally | ✅ Working (v11) |
| **Privacy Controls** | Everything stays on-device in local files you own (git-ignored) | 🟡 Defined & enforced locally; on-disk encryption still to come |
| **MLX / alternative backends** | Support for Apple MLX and other local runtimes | ⬜ Planned |
| **Packaging** | An easy install for non-technical users | ⬜ Planned |

## Current State

- A solid **system prompt** defines who she is (separate honest wording for local vs SpaceXAI).
- The **Python framework** (`clementine.py`) runs today: **default** chat is local Ollama; **optional** SpaceXAI (`--provider spacexai` / `/provider spacexai` / web picker) uses `XAI_API_KEY` and `grok-4.5` (see [docs.x.ai](https://docs.x.ai)). Streaming works on both paths.
- She **remembers** — recent conversation stays verbatim; older conversation is automatically condensed into summaries so nothing is lost and the context never overflows; explicit facts and notes persist forever in a local `clementine_memory/` folder (never uploaded by the framework).
- **Embeddings** for semantic recall stay on local Ollama even when chat uses SpaceXAI.
- Local path needs Ollama + a model. SpaceXAI path needs a key in `.env` (see `.env.example`). Offline provider tests: `python -m unittest tests.test_provider -v`.

## Running Clementine

```bash
# 1. Install Ollama from https://ollama.com
# 2. Pull a model
ollama pull llama3.1:8b
# (optional) pull an embedding model for semantic memory recall
ollama pull nomic-embed-text
# 3. Install the one dependency
pip install -r requirements.txt
# 4. Wake her up
python clementine.py
```

Semantic recall is optional: if `nomic-embed-text` isn't present, Clementine simply keeps using her full layered memory — nothing breaks.

### The web interface

Prefer a browser to a terminal? Same Clementine, same memory:

```bash
python clementine_web.py        # then open http://127.0.0.1:5000
```

Chat on the left; her memory on the right with live teach and forget. The page is served **only on 127.0.0.1** — it is never reachable from outside your machine, and nothing on it leaves your device.

### Profiles — one companion each

If more than one person shares a machine (or you want separate contexts, like Work and Personal), each profile is a completely separate life: its own memory, its own chosen name, its own personality.

```bash
python clementine.py --profile Crystal      # terminal
python clementine_web.py --profile Crystal  # web
```

In the web UI you can switch or create profiles from the header. Profiles live in `clementine_profiles/<name>/` — plain local folders you own, never committed to git.

## Choosing a Model for Your Hardware

Clementine runs on whatever model Ollama serves, so you can match her to your machine. Models are **quantized** — their weights are compressed to lower precision, which makes them smaller and faster with only modest quality loss. Pick a model with `--model`:

```bash
python clementine.py --model llama3.2:3b          # lighter machines
python clementine.py --model llama3.1:8b          # default — Q4_K_M, the sweet spot
python clementine.py --model llama3.1:8b-instruct-q5_K_M   # higher quality
```

You can also switch mid-conversation with `/model <tag>`.

### SpaceXAI (optional cloud chat)

Sovereignty stays the **default**: Ollama on your machine. If you want Grok-class replies without abandoning CrystalCore memory, you can **opt in** to SpaceXAI (xAI’s API — OpenAI-compatible).

What leaves the device: **chat messages** for inference only.  
What stays local: **memory files**, **embeddings**, **profiles**, and the web UI (still `127.0.0.1`).

```bash
# 1. Key from https://console.x.ai  →  put in a git-ignored .env
#    XAI_API_KEY=xai-...
#    (see .env.example)

# 2. Explicit opt-in, then chat with SpaceXAI
python clementine.py --provider spacexai --model grok-4.5
# Windows: double-click Start-Lumina-SpaceXAI.bat  (records opt-in)
# Web: pick spacexai → confirm dialog → Save profile
# Mid-session:
#   /optin
#   /provider spacexai
#   /model grok-4.5
# Revoke anytime:
#   /optout
```

| Switch | Meaning |
|--------|---------|
| `--provider ollama` | Local (default). Nothing leaves the machine. |
| `--provider spacexai` / `/optin` | Explicit opt-in; consent + timestamp on the profile. Chat via `api.x.ai`. Needs `XAI_API_KEY`. |
| `CRYSTAL_PROVIDER=spacexai` | Same as `--provider` (records opt-in). |
| `/model grok-4.5` | Records opt-in and selects SpaceXAI. |
| `/optout` | Revoke consent; back to local Ollama. |

Check current models and pricing: [docs.x.ai/developers/models](https://docs.x.ai/developers/models). Default SpaceXAI model in this project: **`grok-4.5`**.

When SpaceXAI is on, her system prompt **honestly** says chat may leave the device — she will not claim full offline mode while that path is active.

| Quantization | Approx. size vs FP16 | Quality | Best for |
|--------------|----------------------|---------|----------|
| **Q8_0** | ~50% | Very high | Strong machines, maximum fidelity |
| **Q5_K_M** | ~30% | High | A good machine wanting extra quality |
| **Q4_K_M** | ~25% | Good (the sweet spot) | **Most people** — this is the default |
| **Q3_K_M** | ~20% | Moderate | Older / low-RAM laptops |

The default `llama3.1:8b` tag is already Q4_K_M, so most users need nothing else. If replies feel slow, step down to `llama3.2:3b` or a Q3 build; if you have RAM to spare and want richer replies, try a Q5 or Q8 tag.

Type `/help` inside the session to see all commands. Everything she remembers stays on your device.

## Long-term Vision

The goal is for Clementine to eventually become:

- A true companion that remembers you deeply over months and years
- Emotionally intelligent and present
- Fully sovereign — no company can access her or delete her
- Capable of growing with the user

This is the foundation being built before expanding to more advanced features: richer memory, emotional-tone tracking, tools, on-disk encryption, and mobile.

---

*Part of [The Crystal Vision](README.md) · TerAustralis Incognita · Non Solus — Not Alone*
