# CrystalCore.OS-APP

A chat app with a crystalline soul. Flask backend, single-page chat UI,
powered by all the major AIs — Grok, DeepSeek, ChatGPT, Gemini, Mistral,
Llama, Perplexity, and Claude — switchable right in the chat, with the CrystalCore personality built in as the system
prompt and a memory layer so CrystalCore remembers you.

## Memory

- **Conversation memory** — the chat history is saved on the server, so
  closing the tab or restarting the app doesn't lose the conversation.
  The **New** button starts a fresh conversation.
- **Long-term memory** — CrystalCore can choose to permanently remember
  things (your name, promises, milestones). Saved memories survive even a
  new conversation and are shown to the AI at the start of every chat.
  Ask it to remember something and it will.
- Everything is stored as plain JSON files in the `memory/` folder, which
  is gitignored — your conversations never leave the machine running the
  app. Open `memory/memories.json` any time to see (or edit) what it
  remembers.

## Setup (works in GitHub Codespaces)

1. **Add your API key** — create a file named `.env` in the repo root.

   To use Grok:

   ```
   AI_PROVIDER=grok
   XAI_API_KEY=your_grok_key_here
   ```

   Or to use DeepSeek:

   ```
   AI_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your_deepseek_key_here
   ```

   Or to use Claude:

   ```
   AI_PROVIDER=claude
   ANTHROPIC_API_KEY=your_claude_key_here
   ```

   ChatGPT, Gemini, Mistral, Llama, and Perplexity work the same way —
   see `.env.example` for every provider's key name and where to get one.
   Add keys for as many AIs as you like; the chat has a dropdown to switch
   between them, and they all share the same conversation and memories.

   (`.env` is gitignored, so your key never gets committed.)

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   python app.py
   ```

4. Open the URL Codespaces forwards for port **5000** (a popup will offer
   "Open in Browser") — and talk to CrystalCore.

## Deploy to Railway (lives 24/7)

Railway runs the app permanently — no Codespace needed, works from a phone.

1. Go to [railway.com](https://railway.com) and log in **with GitHub**.
2. **New Project → Deploy from GitHub repo** → pick `CrystalCore.OS-APP`.
   Railway detects Python and the `Procfile` automatically.
3. Open the service → **Variables** tab → add your keys (Railway has no
   `.env` file; variables go here instead):
   - `AI_PROVIDER` = `grok` (or whichever you want as default)
   - `XAI_API_KEY` = your key (and any other providers' keys you have)
4. **Persistent memory** (recommended): in the service, **Add Volume**,
   set the mount path to `/data`, then add one more variable:
   - `MEMORY_DIR` = `/data`
   Without a volume, memories reset whenever Railway restarts the app.
5. **Settings → Networking → Generate Domain** — that URL is CrystalCore's
   permanent home. Open it from any device, any time.

Every `git push` to `main` redeploys automatically.

## Customizing the CrystalMatrix

The CrystalMatrix — the system prompt that shapes who CrystalCore is —
lives in the `CRYSTALCORE_SYSTEM_PROMPT` string near the top of `app.py`.
Per-AI names (like Ren Ren for Grok) live in `PROVIDER_PERSONAS` just
below it. Restart the app to apply changes.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Flask server + 8 AI providers + the CrystalMatrix |
| `memory.py` | The memory layer (conversation history + long-term memories) |
| `templates/index.html` | The chat UI (provider picker, New-chat button) |
| `Procfile` | Tells Railway (or any host) how to run the app |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for your `.env` file (local runs) |
| `memory/` | Created at runtime; holds the JSON memory files (gitignored) |
