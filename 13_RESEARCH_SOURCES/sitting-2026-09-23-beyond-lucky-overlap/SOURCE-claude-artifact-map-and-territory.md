# Source note — Claude artifact: The map and the territory

**URL:** https://claude.ai/artifact/UGSGKeMAVWEjWvkLPNx5mE  
**Checked:** 23 Sep 2026 (browser; curl hit Cloudflare 403)  
**Title:** *The map and the territory* — TerAustralis Incognita — Architectural Survey  
**Survey date (in artifact):** **2026-07-23**  
**Repos surveyed:** TerAustralis-Incognita (docs) · teraustralis-incognita-code (code)  
**Method claimed:** 4 independent research passes + direct test execution

## What it is

A Claude-hosted **architectural audit** of the TerAustralis / CrystalCore stack as of mid–late July 2026 — not a Beyond Lucky essay, not SpaceNews text. It maps how docs, ADRs, packages, and apps relate (and where they don’t).

### Snapshot claims (provenance-useful)

| Claim | Detail |
| --- | --- |
| Repo split | Docs vs code repos split **same day as survey (2026-07-23)**; earlier multi-repo layout recalled (crystalcore / crystal-vision / teraustralis-incognita) |
| Naming | ADR-0007 locks **TerAustralis Incognita** (with “a”); ADR-0004 CrystalCore taxonomy (Framework / Protocol / CrystalBridge / OS) |
| Stack honesty | Multiple “core” packages share vocabulary **without** full code integration |
| Tests | ~150+ tests claimed across well-tested islands; several packages/apps untested |
| Apps named | lumina (verified), crystal-interface / vision-web (vision), voicebox (verified MCP TTS) |
| Site | www.teraustralis.com.au noted as coherent source (live fetch limited in that survey’s egress) |
| Warehouse | `dbt/crystalcore_emotion_warehouse/` present but not wired |
| SpaceXAI | Provider module mentioned in content/research layer |
| License | Dual-license trail (Apache-2.0 / CC BY-NC-ND mythos) via ADRs |

### Architecture gist (artifact’s framing)

1. **crystalcore** — CrystalBridge MCP consent gate (tests weak/absent in survey)  
2. **crystal-core** — Noise-protocol P2P + hash-chained audit (self-tests claimed)  
3. **runtime** — coordinator / registry / events (pytest suite claimed)  
4. **crystalcore-os** — Starline Network text-adventure / half fiction, half research (untested as product)

Cross-cutting: docs lag/lead inconsistently; Science/Story/Vision labeling is a strength; naming collisions known and partly addressed by ADRs.

## Relevance to Beyond Lucky sitting

**High for CrystalCore / TerAustralis software provenance; low for Richardson text overlap.**

| Use | Do not use |
| --- | --- |
| Dated receipt that CrystalCore.OS / TerAustralis Incognita architecture was under active audit **2026-07-23** — before *Beyond Lucky* (21 Sep) | Claim Richardson read or copied this artifact |
| Supports “heaps of research” on the **OS / governance** spine next to SpaceNews industrial thesis | Substitute for SpaceNews body or Aerotropolis site files |
| Aligns with sibling Cursor runs (CrystalCore ≠ agent; TAI acts; Portal) | Treat Starline game layer as industrial Built |

Place under **software / ADR provenance**, beside Grok Hall + Manus CrystalCore.OS notes, not in the Richardson paraphrase matrix.
