# Node Network Beneath Water — Technical Infrastructure & Data Flows

*The deep structural layer: how consent, memory, and trust flow through CrystalCore's infrastructure.*

---

## I. Core Principle: Sovereignty Through Architecture

Every governance rule is **enforced in the database, not the UI.** The steward does not trust clients. The database trusts only a single SHA-256 hash.

---

## II. Trust Root: The Steward Key

**One cryptographic hash.**
- **Location:** `mc_config.value` where `key = 'steward_key_hash'` (Supabase `mc_config` table)
- **Format:** SHA-256 hash of the steward's key (never stored plain-text anywhere)
- **Rotation:** Update the hash in mc_config; old key becomes inert immediately
- **Access:** Server-side only; never embedded in any client, repo, or environment file
- **Enforcement:** PostgreSQL SECURITY DEFINER functions check the hash before executing any write

**Flow:**
```
Client submits entry + plain-text steward key
     ↓
Supabase RPC `mc_submit_entry` (SECURITY DEFINER)
     ↓
Function computes SHA-256(key), compares to stored hash
     ↓
If match: entry is written; if fail: rollback
```

---

## III. Table Schema: `mc_entries` (The Vault)

**Core columns:**
- `id` (uuid): Primary key, immutable at creation
- `receipt_id` (text): SHA-256 hash of entry (immutable, unique)
- `created_at` (timestamptz): Immutable timestamp
- `type` (enum): work | lyric | document | decision | correction | citation | conversation | family_history | oral_tradition
- `title` (text): Entry name
- `content_body` (text): The actual content
- `source_url` (text): Where it came from (if external)
- `source_label` (text): Human-readable source name
- `file_url` (text): Link to associated file/artifact
- `tags` (text[]): Array of labels (e.g. ["urgent", "draft", "verified"])
- `domain` (enum): Music | Art | Codex & Mythos | Proposal & Strategy | Software & Protocols | Decisions & Corrections | External Index | Indigenous & Oral Knowledge | Family & Genealogy
- `subdomain` (text): Optional finer category
- `era` (text): Time period (e.g. "2026-Q3", "pre-launch")
- `language` (text): ISO 639-1 code (default 'en')
- `contributor_handle` (text): Who submitted (default 'CrystalArchitect')

**Provenance (never null, always visible):**
- `provenance_source` (enum): human | model | verified_external
- `tier` (enum): fact | claim | canon
- `status` (enum): active | disputed | corrected | removed
- `status_reason` (text): Why status changed; mandatory for any status change

**Governance:**
- `consent_ref` (text): For consent-gated domains (Indigenous & Oral Knowledge, Family & Genealogy), this must be non-empty; database rejects NULL submissions to these domains
- `parent_entry_id` (uuid FK): For corrections/amendments, link to original; forms a revision chain
- `related_entry_ids` (uuid[]): Cross-reference array for semantic links

**Metadata:**
- `synthesis_notes` (jsonb): AI-generated cross-references, proposals, or notes (always tagged with provenance_source='model')

**Indexing:**
- `fts` (tsvector, generated): Full-text search index using websearch syntax
- GIN index on fts
- Unique index on receipt_id
- Unique index on (id, created_at)

---

## IV. Table Schema: `mc_config` (Private Steward Table)

**Only one row ever needed:**
```sql
key='steward_key_hash', value='<SHA-256 of current steward key>'
```

**Row-Level Security:**
- RLS policy denies all access except through SECURITY DEFINER functions
- No direct client reads
- No direct client writes

---

## V. Security Definer Functions (The Enforcement Layer)

### Function: `mc_submit_entry(steward_key TEXT, entry_data JSONB) → SETOF mc_entries`

**Signature:** SECURITY DEFINER, LANGUAGE plpgsql

**Pre-flight checks:**
1. Hash the `steward_key` parameter: `computed_hash := extensions.digest(steward_key::bytea, 'sha256')`
2. Query `mc_config` for stored hash (uses RLS-bypassing query inside SECURITY DEFINER)
3. Compare: `computed_hash != stored_hash` → RAISE EXCEPTION 'Invalid steward key'

**Consent gate enforcement:**
4. Extract `domain` from `entry_data`
5. If domain IN ('Indigenous & Oral Knowledge', 'Family & Genealogy'):
   - Check `entry_data->'consent_ref'` IS NOT NULL
   - If NULL or empty: RAISE EXCEPTION 'Consent required for this domain'

**Entry creation:**
6. Generate `receipt_id := encode(digest(entry_data::text || NOW()::text, 'sha256'), 'hex')`
7. Generate `id := gen_random_uuid()`
8. Set `created_at := NOW()` (immutable)
9. Set `status := 'active'` (default)
10. Set `status_reason := 'created'`
11. INSERT into mc_entries; RETURN inserted row

---

### Function: `mc_set_status(steward_key TEXT, entry_id UUID, new_status TEXT, reason TEXT) → mc_entries`

**Signature:** SECURITY DEFINER, LANGUAGE plpgsql

**Pre-flight checks:**
1. Hash and verify steward_key (same as above)
2. Validate `new_status` is in enum (active | disputed | corrected | removed)

**Immutability enforcement:**
3. Fetch the entry by `id`; lock with FOR UPDATE
4. Verify these fields never change: id, receipt_id, created_at, type, title (originally), domain
5. If any of these are being modified: RAISE EXCEPTION 'Immutable field modification attempted'

**Tombstone rule (on removal):**
6. If `new_status = 'removed'`:
   - NULL the `content_body`
   - Preserve all metadata (id, receipt_id, timestamps, domain, consent_ref, etc.)
   - Set `status_reason := reason` (mandatory; reject if NULL)

**Correction linkage:**
7. If `new_status = 'corrected'` and `parent_entry_id` is provided:
   - Create a child revision linking via `parent_entry_id`
   - Both original and correction remain visible; lineage is transparent

**Status update:**
8. SET status := new_status, status_reason := reason
9. RETURN updated row

---

## VI. Row-Level Security (RLS)

### mc_entries table:
**Policy: public_select_all**
- `FOR SELECT` to authenticated users and anon users
- PERMISSIVE (allow)
- Using: `true` (read all rows)

**Policy: no_direct_insert / no_direct_update / no_direct_delete**
- `FOR INSERT/UPDATE/DELETE` to all roles
- RESTRICTIVE (deny)
- Using: `false` (reject all direct writes)
- **Reason:** All writes go through SECURITY DEFINER RPCs, never direct SQL

### mc_config table:
**Policy: admin_only**
- `FOR SELECT/INSERT/UPDATE/DELETE` to a custom "admin" role
- PERMISSIVE
- Using: `role = 'admin'` (or `current_setting('request.jwt.claims'->>'role') = 'admin'`)

**Policy: deny_all_others**
- `FOR ALL` to authenticated and anon users
- RESTRICTIVE
- Using: `false`

---

## VII. API Endpoint Contract (MemoryCore Public JSON API)

### GET `/api/entries` (Public Read)
**Query parameters:**
- `domain` (optional): filter by domain name
- `type` (optional): filter by entry type
- `tier` (optional): filter by tier (fact | claim | canon)
- `status` (optional): filter by status (active | disputed | corrected | removed)
- `q` (optional): full-text search using websearch syntax
- `limit` (optional, default 25, max 100)
- `offset` (optional, default 0)

**Response:**
```json
{
  "entries": [
    {
      "id": "uuid",
      "receipt_id": "sha256hex",
      "type": "work",
      "title": "...",
      "content_preview": "first 200 chars",
      "domain": "Music",
      "created_at": "iso8601",
      "provenance": {
        "source": "human",
        "tier": "fact",
        "status": "active"
      },
      "consent_ref": null
    }
  ],
  "total": 1523,
  "next_offset": 25
}
```

### GET `/api/entries/:id` (Public Read Full Entry)
**Response:**
```json
{
  "id": "uuid",
  "receipt_id": "sha256hex",
  "type": "work",
  "title": "...",
  "content_body": "full content",
  "domain": "Music",
  "subdomain": "Starline Transmissions",
  "created_at": "iso8601",
  "era": "2026-Q3",
  "tags": ["verified", "canon"],
  "provenance": {
    "source": "human",
    "tier": "fact",
    "status": "active",
    "status_reason": "created"
  },
  "parent_entry_id": null,
  "related_entry_ids": ["uuid", "uuid"],
  "synthesis_notes": {
    "proposed_by": "Clementine",
    "timestamp": "iso8601"
  },
  "citations": [
    {
      "format": "APA",
      "text": "Arena-Turner, C. (2026). ..."
    },
    {
      "format": "MLA",
      "text": "Arena-Turner, Crystal. \"...\" MemoryCore. 2026."
    },
    {
      "format": "Chicago",
      "text": "Arena-Turner, Crystal. \"...\" MemoryCore, accessed Sept 2026."
    },
    {
      "format": "raw_json",
      "text": "{\"id\": \"...\", \"receipt_id\": \"...\", ...}"
    }
  ]
}
```

### POST `/api/entries` (Steward-Gated Write)
**Request body:**
```json
{
  "steward_key": "plain-text key (ONLY OVER HTTPS)",
  "entry": {
    "type": "work",
    "title": "...",
    "content_body": "...",
    "domain": "Music",
    "tier": "canon",
    "provenance_source": "human",
    "consent_ref": null,
    "tags": ["verified"],
    "source_url": null,
    "file_url": null
  }
}
```

**Response:**
```json
{
  "success": true,
  "entry": { ... full entry object ... },
  "receipt_id": "sha256hex"
}
```

**Error responses:**
```json
{
  "success": false,
  "error": "Invalid steward key"
}
```

```json
{
  "success": false,
  "error": "Consent required for Indigenous & Oral Knowledge domain"
}
```

### POST `/api/entries/:id/status` (Steward-Gated Status Change)
**Request body:**
```json
{
  "steward_key": "...",
  "new_status": "disputed",
  "reason": "Timeline inconsistency flagged by reviewer"
}
```

**Response:**
```json
{
  "success": true,
  "entry": { ... updated entry ... }
}
```

---

## VIII. MCP Endpoint (AI Agent Access)

**Tools exposed to Claude, Grok, and other models:**

### `search_entries(query: string, domain?: string, limit?: int) → Entry[]`
- Full-text search on `fts` column
- Returns public-readable metadata + content
- Always includes provenance labels

### `get_entry(entry_id: UUID) → Entry`
- Fetch single entry by id
- Includes full history if `parent_entry_id` chain exists

### `list_domain(domain: string, tier?: string, limit?: int) → Entry[]`
- List all entries in a domain (or subdomain)
- Filter by tier if provided
- Sorted by created_at DESC

**Note:** All MCP responses are read-only and carry full provenance. Any AI proposals enter via `mc_submit_entry`, labelled `provenance_source='model'`, queued for steward review.

---

## IX. Consent Gating: Technical Enforcement

**For entries in `Indigenous & Oral Knowledge` or `Family & Genealogy`:**

1. Database schema marks these domains as ENUM values
2. Application code (front-end, API) surfaces the consent requirement to the user before submission
3. User provides `consent_ref` (a URI, document hash, or identifier of the consent)
4. Before `mc_submit_entry` runs:
   - Function calls `mc_check_consent(domain TEXT, consent_ref TEXT) → boolean`
   - Query: `SELECT (domain NOT IN ('Indigenous & Oral Knowledge', 'Family & Genealogy') OR consent_ref IS NOT NULL AND consent_ref != '') AS consent_ok`
   - If FALSE: RAISE EXCEPTION
5. Consent reference is stored immutably with the entry; audit trail is permanent

**Living person safeguard (Family & Genealogy):**
- Application logic (not database) cross-checks entries against a living-person registry
- Any new entry naming a living person triggers a consent-confirmation workflow
- Documented consent is stored as `consent_ref`
- Entries without valid consent_ref are rejected by the function

---

## X. Revision Chain (Amendment & Correction Flow)

**Scenario:** An entry is found to contain incorrect information.

1. Steward creates a NEW entry with:
   - `type: 'correction'`
   - `parent_entry_id: <id of original>`
   - `content_body: <correct information or explanation>`
   - `status: 'active'`
2. Original entry status is changed to `'corrected'` with reason "Corrected by entry <new_id>"
3. Both entries remain visible; full chain is traversable via `parent_entry_id`
4. Front-end renders both: original (marked as corrected, with link) and correction side-by-side

**Immutability guarantee:** Original entry's id, receipt_id, created_at, and type never change. Only status and status_reason are updated.

---

## XI. Bitcoin Anchoring & OpenTimestamps

**Weekly workflow:**

1. **Manifest generation:** Export all entries as JSON
   ```json
   {
     "exported_at": "2026-09-10T00:00:00Z",
     "total_entries": 42,
     "entries": [
       {
         "id": "uuid",
         "receipt_id": "sha256hex",
         "created_at": "iso8601",
         "type": "work",
         "domain": "Music",
         "title": "...",
         "receipt_timestamp": "iso8601"
       }
     ]
   }
   ```

2. **Manifest hash:** Compute SHA-256 of the JSON payload
   ```
   manifest_hash = sha256(json_string)
   ```

3. **Bitcoin timestamp:** Submit manifest_hash to OpenTimestamps
   - OpenTimestamps merkle-includes the hash into Bitcoin
   - Returns proof: a path of hashes + Bitcoin block height + proof certificate

4. **Proof storage:** Store the OpenTimestamps proof as an entry in MemoryCore itself
   ```json
   {
     "type": "document",
     "domain": "Decisions & Corrections",
     "title": "Bitcoin Anchor — Week of 2026-09-10",
     "content_body": "<OpenTimestamps proof certificate>",
     "provenance_source": "verified_external",
     "tier": "fact",
     "tags": ["bitcoin_anchor", "permanent"]
   }
   ```

**Result:** Every entry is indirectly secured by the Bitcoin blockchain via the manifest hash. Immutability is cryptographically verifiable: if anyone modifies an entry, the manifest hash changes, the proof breaks, and the tampering is obvious.

---

## XII. Data Isolation & Account Separation

**One Steward, One Key, One Vault:**
- Single Supabase project holds all entries
- Single steward key controls all writes
- No per-user accounts or API key hierarchies (keeps trust model simple)

**Multi-AI access (read-only by default):**
- MCP endpoint exposes read tools to any AI system
- Write proposals always require human (steward) approval
- Grok, Claude, future models all read the same vault; none can unilaterally modify it

**No vendor lock-in:**
- Data in Supabase is fully portable (standard PostgreSQL)
- Manifest can be exported to any archive or blockchain at any time
- Front-end can be replaced without touching the vault

---

## XIII. Deployment Checklist (For Each Build)

- [ ] Create Supabase project (owner's account, ap-southeast-2 region)
- [ ] Apply migration `0001_memorycore_v1.sql` (creates tables, indexes, RLS, SECURITY DEFINER functions)
- [ ] Generate fresh steward key (strong random, never committed)
- [ ] Compute SHA-256(steward_key) and INSERT into mc_config
- [ ] Verify RLS policies are active: `SELECT schemaname, tablename, policyname FROM pg_policies WHERE tablename IN ('mc_entries', 'mc_config')`
- [ ] Test SECURITY DEFINER function: `SELECT mc_check_consent('Music', NULL)` (should return true)
- [ ] Restore founding entries from backup JSON (preserving original ids, receipt_ids, created_at timestamps)
- [ ] Create publishable (public) API key in Supabase (read-only key)
- [ ] Embed public key in front-end (publishable key is public-by-design; steward key is never embedded)
- [ ] Deploy front-end (Manus build) with connection to Supabase URL + publishable key
- [ ] Point memory.teraustralis.com.au DNS at front-end
- [ ] Verify public read works: `curl https://memory.teraustralis.com.au/api/entries?limit=1`
- [ ] Verify steward write RPC works (test with correct key, verify rejection with wrong key)
- [ ] Deploy MCP endpoint (Node.js or Python service calling the same Supabase RPC and API)
- [ ] Deploy Clementine v1 with engine adapter (Grok API / OpenRouter / local)
- [ ] Set up weekly manifest export → OpenTimestamps workflow

---

## XIV. Threat Model & Mitigations

| Threat | Mitigation |
|--------|-----------|
| Client-side key injection | Steward key never embedded; only sent over HTTPS POST to RPC; never logged |
| Mass data corruption via bad client | Database rejects non-SECURITY DEFINER writes; client cannot bypass |
| Steward key leakage | Only hash stored server-side; rotation via mc_config hash update; no key recovery |
| Unauthorized AI modification | All model writes labelled `provenance_source='model'`; human must approve via steward gate |
| Deletion without trace | Tombstone rule: removal clears content but keeps row with reason; immutable receipt_id |
| Living person privacy breach | Application logic checks living-person registry; database enforces consent_ref for Family & Genealogy; consent is stored immutably |
| Frontend tampering | RLS + SECURITY DEFINER prevent direct writes; all truth lives in Postgres, not the UI |
| Backend compromise (Supabase) | Data portability: can migrate to any PostgreSQL, re-anchor via OpenTimestamps, deploy new front-end |

---

## XV. Health Checks & Monitoring

**Regular audits:**
1. Verify all entries have non-NULL (source, tier, status) — invariant violated = data corruption alert
2. Count entries by domain; alert if consent-gated domains have NULL consent_ref
3. Verify all receipt_ids are unique SHA-256 hexstrings
4. Check for orphaned parent_entry_id references (FK integrity)
5. Audit status_reason for every status != 'active' (reason required)
6. Monthly Bitcoin anchor verification: re-download OpenTimestamps proof, verify against manifest hash

**Logging (external to Supabase):**
- Every call to mc_submit_entry or mc_set_status should log: timestamp, steward_key_hash (first 8 chars for debugging), entry_id, operation, result
- NO full key or entry content in logs
- Logs stored on owner's infrastructure, not Supabase

