# Celestial Portal Social Orbit API stubs

FastAPI stubs and Pydantic data models for the cross-platform Social Orbit and Entertainment Studio roadmap.

## Run locally

From this directory:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
uvicorn app.main:app --reload --port 8010
```

Health check:

```bash
curl http://127.0.0.1:8010/health
```

OpenAPI:

```text
http://127.0.0.1:8010/docs
```

## Included

- Shared models for workspaces, connector accounts, provider capabilities, content assets, variants, consent grants, publication jobs, approvals, analytics snapshots, and audit events.
- Provider capability matrix for YouTube, Instagram, TikTok, X, LinkedIn, Facebook, Reddit, Discord, Telegram, and Slack.
- Connector-neutral `SocialConnector` interface.
- Safe `StubConnector` implementations that never contact a real provider.
- Deny-by-default consent decision service.
- In-memory connector, consent, publication, variant, and hash-chained audit storage.
- Connector lifecycle routes.
- Publication job creation, approval, and execution routes.
- Idempotency key field on publication jobs.
- Explicit blocked result when a provider publish operation is still a stub.

## Important limitations

This package intentionally does not store OAuth secrets, call provider APIs, publish content, process webhooks, or run a durable queue. Replace the in-memory store, stub OAuth URLs, and `publish()` methods before production use.

Production replacements should include:

1. Encrypted secret storage and refresh-token rotation.
2. Signed OAuth state and callback verification.
3. Durable Postgres models and migrations.
4. Redis or equivalent job queue with idempotency enforcement.
5. Provider-specific adapters and capability tests.
6. Webhook signature validation or a documented polling fallback.
7. Per-workspace authorization and role checks.
8. Provider rate-limit and circuit-breaker handling.
9. Durable audit storage with an external integrity boundary.
10. Media preflight and object-storage integration.
