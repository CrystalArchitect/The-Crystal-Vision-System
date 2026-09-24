# 07_CELESTIAL_PORTAL

**Canon:** **no**  
**Updated:** 2026-09-18  
**Drive:** [folder 07](https://drive.google.com/drive/folders/11iytHl9SQtFW6ECQMAeaanJhM0nO7_n6)

## What this drawer is

Pointer + handoff trail for Celestial Portal. **Not** a merge of CrystalCore into TerAustralis. **Not** the ASUS install.

| Pile | What | Status |
| --- | --- | --- |
| **A — original-export** | Dream’s AI Studio zip | **PARTIAL** — full zip still on Crystal’s phone / needed in Drive 07 as `original-export.zip` |
| **B — gemini-overlay** | CrystalCore-on-Portal from Gemini on phone | In Drive tar + handoff `GET-THESE` |
| **Plan** | Crystal + Dream Google Doc | [Dream and Crystal - Celestial Portal Build](https://docs.google.com/document/d/11TZt0tPstx4NhrkRQv38FoT2Ue2l-K3mCmwE8cub-O4/edit) |

## In this repo

- Handoff pack: [`../handoff/celestial-portal/`](../handoff/celestial-portal/) (`README.md`, `GET-THESE.md`)
- Working-index id: `CVS-PORTAL-A`
- Living Portal API: [`../backend/`](../backend/)
- Stack surface (Siri → Portal → CrystalCore.OS → TAI): [`../00_MASTER_INDEX/STACK-SURFACE.md`](../00_MASTER_INDEX/STACK-SURFACE.md)
- iOS App Intent (Siri entry): [`../apps/ios/CelestialPortal/Sources/Intents/`](../apps/ios/CelestialPortal/Sources/Intents/)
- Vision sandbox (narrative Portal boot only — not product): [`../10_ORIGINAL_CREATIVE/ahs-lemuria/`](../10_ORIGINAL_CREATIVE/ahs-lemuria/) · `CVS-AHS-LEMURIA`

## Still missing (from handoff)

Original zip A must include (Gemini did **not** create these): `src/main.tsx`, `src/App.tsx`, other original `src/components/*`, `vite.config.ts`, voice/live/orb UI. Skip `.env`.

## Do not

- Treat B as A  
- Treat phone paths as the ASUS disk  
- Commit secrets  
- Rebuild from chat dumps  

AI Studio app (reference): https://ai.studio/apps/9feb2193-fb99-430c-bfd0-299f7ef2f084
