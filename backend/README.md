# Celestial Portal Backend

Voice-first governance system with immutable audit trails. Three-layer architecture:

- **MemoryCore Vault** (PostgreSQL): Canonical decision authority with SHA-256 receipt chains
- **Celestial Portal** (FastAPI): Steward approval workflows and decision canonicalization
- **CrystalBus** (MCP): Read-only access for UK portfolio CI/CD integration

## Architecture

```
Device Apps (iOS, Windows)
    ↓
    ← Biometric Auth (Face ID, Windows Hello)
    ↓
Portal REST API (8000)
    ↓
    ← Voice Chat (Whisper STT → Llama 3 8B → Piper TTS)
    ↓
MemoryCore Vault (PostgreSQL)
    ↓
    ← SHA-256 Immutable Receipt Chain
    ↓
CrystalBus MCP (→ UK Portfolio CI/CD)
```

## Components

### MemoryCore Vault (`vault/`)
PostgreSQL database with:
- `decisions` table: Administrative decisions (ADM-001, ADM-002, etc.)
- `audit_events` table: Immutable SHA-256 event chain
- `stewards` table: Approved personnel with biometric enrollment status
- `enforcement_log` table: Decision enforcement in CI/CD pipelines

**Schema**: `vault/schema.sql` — includes all table definitions with immutable hash fields.

### Celestial Portal (`portal/`)
FastAPI service with endpoints:

```
POST   /v1/admin/stamp                    Canonicalize decision (steward approval)
GET    /v1/decisions/{decision_code}      Fetch active decision by code
GET    /v1/audit-chain/{decision_id}      Fetch immutable audit chain
POST   /v1/decisions/{decision_id}/revoke Revoke decision (steward-only)
GET    /health                            Service health check
```

**Key flow**:
1. Steward authenticates via biometric (device-local)
2. Steward approves decision via voice or UI
3. Portal computes SHA-256 receipt and stores in Vault
4. Decision immutably recorded with previous_hash chain-of-custody
5. Audit event recorded with separate hash chain

### CrystalBus MCP (`bus/`)
Model Context Protocol server exposing:

```
crystal_get_decision(decision_code)           → Decision with receipt hash
crystal_get_decision_payload(decision_code)   → Just payload (for enforcement)
crystal_get_audit_chain(decision_id)          → Audit events with hash chain
crystal_verify_audit_chain(events)            → Boolean: verify hash integrity
```

Used by UK portfolio repositories to fetch decisions for CI/CD enforcement.

## Running Locally

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 16+ client tools (optional, for debugging)

### Quick Start

```bash
# Start all services
cd infrastructure/docker
docker-compose up -d

# Wait for services to be healthy (30-60 seconds)
docker-compose ps
```

Services will be available at:
- Portal API: `http://localhost:8000`
- LLM (Ollama): `http://localhost:11434`
- Whisper STT: `http://localhost:8001`
- PostgreSQL: `localhost:5432`
- Redis Cache: `localhost:6379`

### Manual Setup (for development)

```bash
# 1. Start PostgreSQL
docker run --rm -d \
  --name crystal_vault_db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=crystal_vision \
  -p 5432:5432 \
  postgres:16-alpine

# 2. Initialize schema
psql -h localhost -U postgres -d crystal_vision < backend/vault/schema.sql

# 3. Install Portal dependencies
cd backend/portal
pip install -r requirements.txt

# 4. Run Portal
python main.py
```

## API Examples

### Create Decision (Steward)

```bash
curl -X POST http://localhost:8000/v1/admin/stamp \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "decision_code": "ADM-001",
      "title": "Code Linting Standards",
      "description": "All PRs must pass eslint and Black formatter",
      "decision_type": "linting_standard",
      "payload": {
        "linters": ["eslint", "black"],
        "severity": "hard_block",
        "exemptions": []
      }
    },
    "steward": {
      "steward_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Alice",
      "email": "alice@example.com",
      "can_approve_decisions": true
    }
  }'
```

Response:
```json
{
  "decision_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "decision_code": "ADM-001",
  "title": "Code Linting Standards",
  "status": "active",
  "event_hash": "a1b2c3d4e5f6...",
  "created_at": "2026-09-17T10:00:00Z",
  "approved_by": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Fetch Decision (CI/CD)

```bash
curl http://localhost:8000/v1/decisions/ADM-001
```

Response:
```json
{
  "decision_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "decision_code": "ADM-001",
  "title": "Code Linting Standards",
  "status": "active",
  "event_hash": "a1b2c3d4e5f6...",
  "created_at": "2026-09-17T10:00:00Z",
  "approved_by": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Fetch Audit Chain

```bash
curl http://localhost:8000/v1/audit-chain/f47ac10b-58cc-4372-a567-0e02b2c3d479
```

Response:
```json
[
  {
    "event_id": "e1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c",
    "event_category": "decision_approved",
    "actor_steward_id": "550e8400-e29b-41d4-a716-446655440000",
    "outcome": "success",
    "event_hash": "b2c3d4e5f6...",
    "previous_event_hash": null,
    "created_at": "2026-09-17T10:00:00Z"
  }
]
```

## Voice Chat Integration

### Whisper STT (Device-Local)
Runs locally on each device for privacy. Transcribes speech to text.

```bash
# Send audio to Portal (which proxies to Whisper)
curl -X POST http://localhost:8001/transcribe \
  -F "audio=@approval.wav"
```

### Llama 3 8B (Central LLM)
Runs at `http://localhost:11434`. Portal routes transcribed text here.

```bash
# Query LLM
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama2",
    "prompt": "Is this a valid administrative decision approval?"
  }'
```

### Piper TTS (Device-Local)
Installed on device alongside Whisper. Converts text to speech.

## Database Debugging

```bash
# Connect to vault
psql -h localhost -U postgres -d crystal_vision

# List decisions
SELECT decision_code, status, event_hash, created_at FROM vault.decisions;

# View audit chain for decision
SELECT event_category, outcome, event_hash, created_at 
FROM vault.audit_events 
WHERE decision_id = '<decision_id>'
ORDER BY created_at ASC;

# Verify audit chain integrity
SELECT 
  event_id,
  event_hash,
  previous_event_hash,
  (previous_event_hash = LAG(event_hash) OVER (ORDER BY created_at)) AS chain_valid
FROM vault.audit_events
WHERE decision_id = '<decision_id>'
ORDER BY created_at;
```

## Environment Variables

```env
# Portal
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/crystal_vision
PORTAL_HOST=0.0.0.0
PORTAL_PORT=8000

# LLM
OLLAMA_HOST=http://localhost:11434

# Whisper
WHISPER_ENDPOINT=http://localhost:8001

# Voice (on device)
DEVICE_VOICE_MODEL=piper  # or espeak
```

## Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Full Workflow
```bash
# 1. Get active decision
curl http://localhost:8000/v1/decisions/ADM-001

# 2. Get audit chain
curl http://localhost:8000/v1/audit-chain/<decision_id>

# 3. Revoke decision
curl -X POST http://localhost:8000/v1/decisions/<decision_id>/revoke \
  -H "Content-Type: application/json" \
  -d '{"steward_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

## Production Considerations

- [ ] Enable SSL/TLS for all services
- [ ] Set strong PostgreSQL password
- [ ] Configure rate limiting on API endpoints
- [ ] Enable audit logging for all database operations
- [ ] Set up monitoring/alerting for hash chain integrity
- [ ] Implement steward MFA (beyond biometric)
- [ ] Backup Vault database daily
- [ ] Rotate encryption keys quarterly

## Troubleshooting

**Portal can't connect to database**:
```bash
docker-compose logs vault_db
docker exec crystal_vault_db psql -U postgres -d crystal_vision -c "SELECT 1"
```

**Audit chain broken**:
Check if event timestamps are monotonic:
```sql
SELECT event_id, created_at, created_at - LAG(created_at) OVER (ORDER BY created_at) AS time_delta
FROM vault.audit_events
WHERE decision_id = '<decision_id>'
ORDER BY created_at;
```

**LLM not responding**:
```bash
docker exec crystal_llm ollama pull llama2:7b
curl http://localhost:11434/api/tags
```

## Next Steps

1. Build iOS app (Swift + React Native) with Face ID approval
2. Build Windows app (Electron + WinUI) with Windows Hello
3. Integrate with UK portfolio repositories via CrystalBus
4. Deploy on production infrastructure (Kubernetes or Docker Swarm)
5. Implement steward onboarding workflow
