# Celestial Portal — Local-First Hybrid Architecture Brief (Engineering)

**Author:** CrystalCore (systems architect)  
**Date:** 2026-09-16 (Australia/Sydney)  
**Audience:** Engineering  
**Status:** Design brief for build — **not** a claim that hybrid/offline is live  
**Domain law:** Celestial Portal ≠ CrystalCore. CrystalVision umbrella material is not Canon/GitHub by default.

---

## 0. Epistemic status (read first)

| Claim | Status | Evidence |
| --- | --- | --- |
| Hybrid online Gemini + offline local LLM intent | **CLAIMED / designed** | Drive: “Dream and Crystal - Celestial Portal Build” |
| Memory must belong to Portal, not Gemini | **LOCKED requirement** | Same Build doc + later CrystalCore/SAT hardening turns |
| Working copy at `C:\Users\Crystal\CelestialPortal` | **CLAIMED, unverified here** | Overlay manifest; this machine has not seen that path |
| Gemini–Dream overlay (better-sqlite3, crystalcore/*, phases A–E) | **CLAIMED overlay (Pile B)** | `2026-09-01_CVSC_Source_Gemini-Dream-overlay-manifest.md` |
| Overlay verified on ASUS hardware | **NOT verified** | Manifest: no ASUS terminal receipts; weak PASS rules |
| Online model is Gemini 3.7 Flash | **CONFLICT** | Intent says 3.7; overlay dump used `gemini-2.5-flash` |
| `/api/tts` is real audio TTS | **FALSE in overlay** | Calls `generateContent` with speech-instruction prompt |
| `celestial_portal_telemetry.json` = live node metrics | **Do not treat as live** | Reports 32 GB RAM vs target hardware 16 GB; mythic audit stream |
| Vercel Celestial Portal project | **None found** | TerAustralis Incognita Vercel team: empty project list |
| Public GitHub portal repo (from this machine) | **UNKNOWN** | `gh` not authenticated on box |
| Drive Architecture / Application folders | **Empty** | Listed 2026-09-16 |
| UI snapshots | **VERIFIED artifacts** | `index-snapshot.html` (“Bridge to the Light”), React artifact HTML dumps |

**Hard rule for Engineering:** nothing ships as “Built / surveyed / offline-capable” without machine receipts on Crystal’s ASUS (or a designated CI host). Chat PASS ≠ verification.

---

## 1. Product intent (one paragraph)

Celestial Portal is a **local-first companion / SAT study surface** that keeps a **private persistent memory** on-device. While online it may use **Gemini (Flash-class)** plus the existing voice path. While offline it must still open, talk, remember, search, and speak using **local LLM + local STT/TTS**, without losing memory when the model provider changes.

---

## 2. Target hardware (constraint, not optional)

- ASUS Vivobook Studio  
- Intel Core i9-13900H  
- 16 GB RAM  
- NVIDIA GeForce RTX 4050 Laptop (6 GB VRAM)  
- Windows 64-bit, ~157 GB free at last note  

All model / runtime choices must fit this envelope. Do not assume desktop 24–32 GB class.

---

## 3. Locked architecture (Phase 0–3 spine)

```
                 CELESTIAL PORTAL (UI)
                          │
                   AI ROUTER (mode)
                    /            \
               ONLINE            OFFLINE
                  │                 │
         GeminiProvider      LocalProvider
         (Flash-class)       (Ollama / llama.cpp)
                  │                 │
                  └────────┬────────┘
                           │
              CrystalCore envelope + SAT layer
              (governance, provenance, epistemic type)
                           │
                    LOCAL MEMORY
                 (SQLite + FTS5 + files)
```

### Invariants (must not be broken)

1. **Memory ownership:** SQLite/files are the source of truth; providers are replaceable.  
2. **Consent / keys:** Gemini API keys stay server-side (loopback gateway). No browser-held provider keys. No `Access-Control-Allow-Origin: *` for the local gateway. Bind to loopback only.  
3. **Epistemic typing:** ingested items carry immutable types after write (`evidence` | `vision` | `unverified_claim` | user statement vs system evidence). Promotion across belts is explicit, never silent.  
4. **SAT placement:** SAT sits **between memory retrieval and generation** — affect / gap modeling does not rewrite Canon or invent authority.  
5. **CrystalCore envelope:** every generation request carries provenance + governance_version; Method > Logos; Story as Bridge never Loop; external fact ≠ system capability.  
6. **Incognita / honesty:** do not label unbuilt offline paths as Built. Overlay contradictions stay in the ledger until re-verified.  
7. **Hard stop:** Phase 0–3 is not “done” until the verification checklist passes on the real machine.

### Non-goals (Phase 0–3)

- Replacing Gemini while online  
- Full offline voice (STT/TTS) — Phase 4+  
- Merging CrystalVision archive into Portal Canon  
- Treating telemetry JSON or mythic enclave metrics as product truth  
- Shipping CrystalCore.OS terminal work inside this repo (separate cut)

---

## 4. Recommended target tree (Phases 0–3)

```
celestial-portal/
  package.json                 # ESM; name: celestial-portal (not react-example)
  .env                         # server-only secrets; never commit
  .gitignore                   # .env, *.db, backups/, node_modules/
  server.js                    # loopback HTTP gateway
  lib/
    db.js                      # SQLite + FTS5 + CHECK constraints + rebuild
    ai-providers.js            # GeminiProvider | LocalProvider
    crystalcore.js             # envelope, invariants, governance_version
    sat.js                     # SAT boundary (no Canon rewrite)
  public/                      # static UI (path-containment!)
    app.js                     # talks only to local gateway
  scripts/
    backup-immutable.js        # Phase 0: copy-on-write / dated snapshot
    verify-phase0-3.js         # gate script
    test-crystalcore-invariants.js
  data/                        # local only
    portal.db
    documents/
  docs/
    ENGINEERING-BRIEF.md       # this brief
    OVERLAY-CONTRADICTIONS.md  # from Gemini–Dream manifest
```

### Provider contract (minimal)

```ts
interface ChatRequest {
  messages: { role: 'user' | 'assistant' | 'system'; content: string }[];
  mode: 'online' | 'offline' | 'auto';
  // browser must NOT send arbitrary localModel names that escalate privilege
}

interface ChatResponse {
  text: string;
  provider: 'gemini' | 'local';
  model: string;
  envelope: {
    governance_version: string;
    provenance: object;
    epistemic: object;
    sat?: object;
  };
}
```

### Memory schema (minimal — expand carefully)

- `messages` — conversation turns with timestamps, session_id, role  
- `memories` — durable facts/preferences/events with **epistemic_type**, **source/origin**, **governance_version**, created_at; epistemic_type immutable post-insert (trigger)  
- `documents` — local files metadata + path  
- `memories_fts` — FTS5 **external-content** table (fix known content= vs external bug from design thread)  
- On migrate: idempotent; rebuild FTS after schema change  

---

## 5. Phased delivery plan

### Phase 0 — Immutable backup
- Snapshot current Portal tree to dated read-only-ish backup (permissions + checksum ledger).  
- **Accept:** backup exists; modifying working tree does not alter backup bytes.

### Phase 1 — Loopback Node gateway
- `server.js` on `127.0.0.1` only; static path containment; body size limits on `/api/chat` and `/api/migrate`.  
- **Accept:** non-loopback connect fails; `../` static escape fails; oversized body rejected.

### Phase 2 — Local SQLite memory
- `lib/db.js` with FTS5 external content + rebuild; migrate idempotent.  
- **Accept:** insert memory → search hits; restart process → memory persists; epistemic_type change after insert fails.

### Phase 3 — Provider abstraction + online Gemini path
- `GeminiProvider` via server env key; frontend only hits gateway.  
- CrystalCore envelope + SAT stub wired on every chat.  
- **Accept:** chat online works; response includes envelope; swapping provider config does not wipe DB.

### Phase 4 — Local LLM (after 0–3 gate)
- Ollama (or llama.cpp) on device; benchmark on **this** hardware before locking primary model.  
- Candidates to **benchmark, not pre-lock:** Qwen2.5 7B-class Q4/Q5, Gemma / Mistral / Llama quantized fits for 6 GB VRAM + 16 GB RAM.  
- **Accept:** offline chat works with Wi-Fi off; tokens/sec + peak RAM/VRAM logged.

### Phase 5 — Offline voice
- Local STT + TTS chosen after LLM path stable. Do not install Whisper/Piper “just in case” before Phase 4 receipts.  
- **Accept:** mic → local STT → local LLM → local TTS with network disabled.

### Phase 6 — Security hardening pass
- Key never in browser; no injectedApiKey left in process beyond request scope if avoidable; export/delete memory; audit log of provider calls (local).

---

## 6. Known overlay contradictions (fix before trusting Pile B)

From `2026-09-01_CVSC_Source_Gemini-Dream-overlay-manifest.md`:

1. package rename `react-example` → `celestial-portal` + better-sqlite3 (Pile A ≠ Pile B).  
2. Phase D claimed `server.ts` untouched while listing it EDITED.  
3. Model ID mismatch (2.5 vs 3.7 intent).  
4. Fake TTS endpoint.  
5. Tests treating HTTP 500 as PASS.  
6. API key held in process memory + env fallback.  

**Engineering action:** treat Pile B as a **hypothesis patch set**. Re-audit the real tree on the ASUS before merging any overlay files.

---

## 7. Acceptance checklist (ship gate for “hybrid Phase 0–3”)

- [ ] Real repo path identified and backed up (Phase 0 receipt)  
- [ ] Gateway loopback-only + path containment + body limits  
- [ ] SQLite persists across restart; FTS search works; epistemic immutability holds  
- [ ] Online Gemini chat via gateway only  
- [ ] Envelope + governance_version on every response  
- [ ] Adversarial invariant tests pass on machine (not only in chat)  
- [ ] No claim of offline LLM/voice until Phase 4–5 receipts  
- [ ] README states Built vs Dreamed clearly (Incognita Rule)

---

## 8. Blockers / asks for Crystal

1. **Canonical working copy:** confirm path (`C:\Users\Crystal\CelestialPortal` or other) and whether GitHub remote exists.  
2. **GitHub access for Engineering / this bot** so the tree can be audited without relying on Drive HTML dumps.  
3. **Decision:** keep Google AI Studio export (Pile A) as upstream, or declare the ASUS folder canonical.  
4. **Model policy:** stay on Gemini Flash-class online; do not hard-lock offline model until benchmarks.

---

## 9. Source inventory (for this brief)

- Drive Build / design conversation: `https://docs.google.com/document/d/11TZt0tPstx4NhrkRQv38FoT2Ue2l-K3mCmwE8cub-O4/edit`  
- Overlay manifest: Drive `1H7qGnVhBUSJO8vvhlfJ6QP8JyxFum4qb`  
- UI: Drive folder `1BLB6LNQJ6-nMh4QmGoBuxNDyurzRS7zB`  
- Project memory note: possible link to observatory (`/`, `/bio`, `/atlas`) — **not proven**  
- Telemetry JSON: Drive `1qub0sWPVpacWj_DrBCIczOaZAjjfN01Z` — **non-authoritative**  
- Handoff archive: `celestial-portal-handoff.tar.gz` (small; extract on build machine)  
- Crystal Vision law: CrystalVision ≠ CrystalCore; Celestial Portal is its own domain  

---

## 10. Handoff note to Engineering

Build **Phases 0–3 only** first. Prefer a clean gateway + SQLite + provider interface over absorbing the entire Dream chat’s generated file dumps. Reconcile overlay contradictions with a file-by-file audit on the ASUS. Do not publish, do not claim offline-complete, do not merge Vision archive into product memory without Crystal’s explicit yes.
