# CrystalCore.OS Admin API

FastAPI backend for the CrystalCore.OS admin panel prototype: JWT-authenticated
diagnostics, container listing, and container terminal log endpoints, backed
by SQLAlchemy (SQLite by default, swappable to Postgres/MySQL via
`DATABASE_URL`).

## Project layout

```
backend/
  app/
    core/       # settings, JWT, logging config, llm.py (llama.cpp wrapper)
    db/         # SQLAlchemy engine/session/base
    models/     # SQLAlchemy models
    schemas/    # Pydantic request/response models
    api/
      deps.py           # auth guard, db session dependency
      v1/router.py      # mounts routes under /api/v1
      v1/routes/         # auth.py, admin.py
    middleware/ # request-id + global error handling
    main.py     # app factory, startup seeding, /healthz
  models/       # downloaded GGUF weights (gitignored, see below)
  scripts/      # hash_password.py, cc_admin_client.py
  download_model.py  # fetches the GGUF weights from Hugging Face
  tests/        # pytest smoke tests
```

Nothing outside `app/api/v1/routes/*.py` needs to change to add a new
endpoint or swap the database -- that's the extensibility this structure
buys you over a single-file script.

## Running locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"   # -> JWT_SECRET_KEY
python3 scripts/hash_password.py "your-password-here"       # -> ADMIN_PASSWORD_HASH
# paste both into .env

python3 download_model.py   # fetches the GGUF weights for POST /generate (~2GB, one-time)

uvicorn app.main:app --host localhost --port 8080
```

In another terminal:

```bash
CC_ADMIN_USER=admin CC_ADMIN_PASSWORD=your-password-here \
  python3 scripts/cc_admin_client.py
```

Run tests: `pytest` (from `backend/`).

## Endpoints

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| POST | `/api/v1/admin/login` | - | Returns a JWT, expires per `ACCESS_TOKEN_EXPIRE_MINUTES` |
| GET | `/api/v1/admin/diagnostics` | Bearer JWT | Real host CPU/RAM/disk via `psutil` -- reports whatever machine the process runs on |
| GET | `/api/v1/admin/containers` | Bearer JWT | Reads from the `containers` table (seeded with `cc-container-01` on startup) |
| GET | `/api/v1/admin/containers/{id}/terminal` | Bearer JWT | **Log-replay only, see below** |
| POST | `/api/v1/admin/generate` | Bearer JWT | Local LLM completion, see below |
| GET | `/healthz` | - | Liveness check |

### The terminal endpoint does not execute commands

`GET /api/v1/admin/containers/{id}/terminal` returns canned/log-replay lines
from an in-memory store, not a live shell. Wiring it to a real container
runtime (`docker exec`, a PTY over a websocket, etc.) is a deliberate,
separate decision: it turns this from a diagnostics API into a remote code
execution surface. Before doing that, decide explicitly:

- who/what can reach this endpoint (network-level restriction, not just the
  JWT check),
- whether JWT-only auth is enough, or you want mTLS / a second factor /
  short-lived scoped tokens per container,
- audit logging of every command issued through it.

Happy to help design and build that once you've made those calls -- it's a
different, higher-stakes piece of work than the rest of this API.

### Local LLM (`POST /api/v1/admin/generate`)

Runs a small quantized model locally via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
-- no external API calls, no API key. Default model: [Qwen2.5-3B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF),
Q4_K_M quantization (~2GB on disk, runs comfortably in ~4-6GB RAM on CPU).

Setup (one-time): `python3 download_model.py` fetches the weights into
`models/` (gitignored -- weights don't belong in version control). Re-running
it is a no-op if the file's already there. Override the repo/file/destination
with `MODEL_REPO_ID` / `MODEL_FILENAME` / `MODEL_DIR`; `LLM_MODEL_PATH` in
`.env` must point at wherever that lands.

```bash
curl -X POST http://localhost:8080/api/v1/admin/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize what CrystalCore.OS is.", "max_tokens": 128}'
```

The model loads lazily on first request (not at server startup), and a
missing model file returns `503` rather than crashing the app. Requests are
serialized through a single model instance (`app/core/llm.py`) -- llama.cpp
contexts aren't safe for concurrent calls -- so this is fine for occasional
admin use, not a high-throughput inference server.

`llama-cpp-python` builds a C++ extension on install; if `pip install` fails,
you're missing a C/C++ toolchain (`build-essential` on Debian/Ubuntu, Xcode
CLI tools on macOS) or want one of its prebuilt wheel variants -- see its
README for CPU/GPU wheel options.

**CI note:** `.github/workflows/download-model.yml` runs `download_model.py`
on pushes that touch it, as a sanity check that the download step still
works. GitHub Actions runners are ephemeral -- this does **not** deploy the
model anywhere or update a running server; an actual deploy needs its own
step (bake the file into an image, or run `download_model.py` on the target
host) that reuses this same script.

## Deployment notes (concepts only -- not run from this session)

This session can't reach your local network, so nothing below has been
executed on your behalf; these are the standard steps for when you deploy
this yourself.

### Running the process

Use a production ASGI setup, not the bare `uvicorn` dev command:

```bash
pip install gunicorn
gunicorn app.main:app -k uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8080 --workers 2
```

Bind to `127.0.0.1`, not `0.0.0.0` -- keep it reachable only via the reverse
proxy below, not directly from the network.

### Nginx reverse proxy (HTTPS via your own cert / certbot)

```nginx
server {
    listen 443 ssl;
    server_name admin.yourdomain.example;

    ssl_certificate     /etc/letsencrypt/live/admin.yourdomain.example/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/admin.yourdomain.example/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Cloudflare Tunnel (no open inbound port)

```bash
cloudflared tunnel create cc-admin
cloudflared tunnel route dns cc-admin admin.yourdomain.example
```

`~/.cloudflared/config.yml`:

```yaml
tunnel: cc-admin
credentials-file: /root/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: admin.yourdomain.example
    service: http://127.0.0.1:8080
  - service: http_status:404
```

```bash
cloudflared tunnel run cc-admin
```

### Before you point either of these at the public internet

This API currently exposes real host CPU/RAM/disk metrics behind nothing but
a single JWT. Before making it internet-reachable, at minimum:

- restrict access at the network layer too (Cloudflare Access, an IP
  allowlist, or a VPN/tailnet) rather than relying on the JWT alone,
- rotate `JWT_SECRET_KEY` and the admin password out of `.env.example`
  defaults,
- turn on rate limiting on the login route,
- keep the terminal endpoint log-replay-only (see above) until you've
  deliberately designed real exec access.

None of this happens automatically -- it's a checklist for you to work
through, not something already configured here.
