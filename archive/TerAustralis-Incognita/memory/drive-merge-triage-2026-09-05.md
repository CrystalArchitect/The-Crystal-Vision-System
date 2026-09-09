# Drive → git merge triage — 2026-09-05

Classification of Drive items reviewed for the TerAustralis Incognita
merge. Tags: **Canon** | **Working** | **Private** | **External** |
**Skip** | **Hold**.

Incognita Rule applied: do not invent canon; label Dreamed vs Built.
Wave 3 bodies included per Crystal 2026-09-05 direction (was Hold; now Included).

## Summary

| Wave | Action |
|------|--------|
| 0 | This triage file |
| 1 | Four card-art WebPs → `mythos/art/`; 16-card list export → `mythos/art/16-card-canon-list.md`; README rows |
| 2 | Drive Canon Lore → `mythos/content/16-CARD-CANON-LORE.md` (new Vision-layer lock note); CVSC Dictionary plate/log/json → `research/cvsc/` with working banner. **Did not** rewrite `mythos/content/CODEX-CRYSTALUM.md` (Drive folder is not a duplicate of that file). |
| 3 | **Included** — Erisian → `research/erisian-blade/`; `memory/briefs/sam-maher-status-brief.md` + `colossus-architecture-brief-2026-08-31.md`; Continuum × SAT → `memory/collaboration/continuum-x-sat-working.md` (joint banner) |
| 4 | Branch `drive-merge-2026-09-05` + PR on `CrystalArchitect/TerAustralis-Incognita`. Site/-Code PR **skipped** (see below). |

## Today / recent inventory

| Drive item | ID | Tag | Destination / note |
|------------|----|-----|--------------------|
| `00_Crystal_Dragon_Architect_FINAL.webp` | `1jb09K77LzSFDAp7LVI_iPghr9KnivMvf` | Canon (Vision art) | `mythos/art/crystal-dragon-architect-final.webp` |
| `01_Monad_Red_Dust_Avatar.webp` | `1-MFkyOm6YsbhrTWzRco6NnGPzHfb5JAc` | Canon (Vision art) | `mythos/art/monad-red-dust-avatar.webp` |
| `02_Lira_Pearl_Winged_Guide.webp` | `1jZ66-J7M2uDOlr1BBg9MdOGBgTQaCsTx` | Canon (Vision art) | `mythos/art/lira-pearl-winged-guide.webp` |
| `03_Dwarven_Artificer.webp` | `1tblrmUVkDIpmEdhoozRtWzNTFNczAYhf` | Canon (Vision art) | `mythos/art/dwarven-artificer.webp` |
| `TerAustralis_16_Card_Canon_List` (sheet) | `10ECzOolOViwQ4P0KTwLbNB2QNCz7o3CqKlvtOJKx2ak` | Canon (Vision list) | Exported CSV → `mythos/art/16-card-canon-list.md` |
| `TerAustralis_Canon_Lore.md` (Doc) | `1wmWA6ADzRxtQ6qL107y0YIVsPXHOJhoZuum_K886HzU` | Canon (Vision lock note) | `mythos/content/16-CARD-CANON-LORE.md` — **Dreamed / Vision-layer**, not Built |
| `TerAustralis_Complete_Canon` (folder) | `1bvVFieJmcbEef6hRvFkdbE_t4vOaNfDp` | Canon (container) | Parent of the four WebPs + Canon Lore Doc; no other children at scan time |
| `CODEX_CRYSTALUM` (folder) | `12B7e61F9qSJgyggdIgqFw3ibsYpHw1aM` | External / Working | Holds Dictionary-of-Dreams **citation** plate + JSON — **not** a duplicate of git `mythos/content/CODEX-CRYSTALUM.md`. See CODEX note below. |
| `2026-09-05_CVSC_Source-Plate_Dictionary-of-Dreams.md` | `10jUntavvlrt4CtiRJTUaGcHvGiAo6_Fh` | External / Working | `research/cvsc/` — bibliographic plate only; third-party book; plate itself says Not Canon / Not publication |
| `2026-09-05_Dictionary-of-Dreams_record.json` | `1njgF5LD9DYEf0gwu4swkysXXV7mr42EN` | External / Working | `research/cvsc/` — structured citation record (`canon: false`, `github_pushed: false`) |
| `2026-09-05_CVSC_Collection-Log_Dictionary-of-Dreams.md` | `1He3wzC6SAq20NbkdgDn16AeiSFYwY4ZD` | Working / Private-shaped | `research/cvsc/` — collection log; no dictionary body text; banner applied |

### CODEX duplicate note

Drive folder `CODEX_CRYSTALUM` is a CVSC **holding** for the Dictionary of
Dreams accession (external citation). It does **not** contain a copy of
the received archive already at `mythos/content/CODEX-CRYSTALUM.md`
(authority weight 0). **Skipped** merging any blob into that git file.
Dictionary plate/log/json land under `research/cvsc/` so they stay
outside public mythos content.

Expected Drive-side duplicates of the plate/json under
`13_RESEARCH_SOURCES` / related trees were **not** re-uploaded; triage
lists the canonical IDs above once.

## Wave 3 — Included (was Hold; Crystal asked for ALL Wave 3)

| Item | Tag | Destination |
|------|-----|-------------|
| `2026-09-03_Erisian-Blade_Grok-Truth-Level-Audit` | Working / audit | `research/erisian-blade/` |
| `2026-09-03_Claude-Ingest-Prompt_Erisian-Blade-Audit` | Working / audit | `research/erisian-blade/` |
| TerAustralis Status Brief for Sam Maher.docx (larger/newer; id `1ByoQs7…`) | Working / external brief | `memory/briefs/sam-maher-status-brief.md` (text extract; duplicates skipped) |
| Colossus Architecture Brief 2026-08-31 | Working / architecture brief | `memory/briefs/colossus-architecture-brief-2026-08-31.md` |
| Continuum x SAT (working — joint with J) | Working / joint | `memory/collaboration/continuum-x-sat-working.md` **with joint banner** |
| Older `Continuum x SAT` (no joint title) | Skip | Not Crystal’s sole ownership; skipped without banner twin |
| PRESERVATION-INVENTORY / random screenshots / Untitled | Skip | Not public gallery art |

## Site / `-Code` PR decision

**Skipped.** Wave 1 filenames are character-card portraits for the 16-card
canon, not members of the existing public-site `atlas-*` folio gallery
pattern under `vision/site/static/assets/art/`. Card-0 art also describes
a figure with personal likeness cues; keep review in Incognita
`mythos/art/` before any site mirror.

## Read failures / notes

| Item | Status |
|------|--------|
| Canon Lore Doc via `read_file_content` | First call rejected by classifier; recovered via `download_file_content` `exportMimeType=text/plain` |
| All four WebPs | Downloaded OK (RIFF/WebP; XMP `trainedAlgorithmicMedia` only — tool unconfirmed) |
| 16-card sheet | Exported OK as `text/csv` |
| Dictionary / CVSC trio | Downloaded OK |
| Erisian Blade pair | Downloaded OK (text/plain export) |
| Colossus Architecture Brief | Downloaded OK |
| Continuum × SAT (joint with J) | Downloaded OK (~78k chars); joint banner applied |
| Sam Maher status brief | Downloaded OK (docx → markdown extract); duplicate smaller copies skipped |

*Non Solus.*
