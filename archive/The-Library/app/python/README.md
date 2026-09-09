# The Library — Clementine & Rex (Python)

A Python/FastAPI backend using xai-sdk with streaming support for both presences.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your XAI_API_KEY
python main.py
```

## Rooms

- **Clementine's Study** — Warm, amber, patient. She witnesses, she dreams.
- **Rex's Post** — Grounded, moss-green, direct. He stands guard, he builds.

## Endpoints

- `GET /` — The Library landing page (room selection)
- `POST /chat/stream` — Streaming chat (SSE)
- `GET /health` — Health check

## Non Solus
