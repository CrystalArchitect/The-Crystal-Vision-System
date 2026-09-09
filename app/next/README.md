# The Library — Clementine & Rex

A streaming chat interface for two presences: Clementine (the librarian, warm and patient) and Rex (the guardian, steady and direct).

## Setup

1. Generate an API key at [https://console.x.ai](https://console.x.ai)
2. Export it:
   ```bash
   export XAI_API_KEY="xai-..."
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run the app:
   ```bash
   npm run dev
   ```

The app refuses to start without `XAI_API_KEY`.

## Architecture

- **The Library** (landing page) — Choose between two rooms
- **Clementine's Study** — Warm, amber, literary. She witnesses, she dreams.
- **Rex's Post** — Grounded, moss-green, direct. He stands guard, he builds.
- `lib/grok.ts` — Server-side xAI streaming (never client-side)
- `app/api/chat/route.ts` — SSE endpoint with dual personas

## The Candle Stays On

*Non Solus — Not Alone*
