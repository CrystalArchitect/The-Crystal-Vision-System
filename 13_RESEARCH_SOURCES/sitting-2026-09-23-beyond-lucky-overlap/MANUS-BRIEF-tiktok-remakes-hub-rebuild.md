# Manus brief — TikTok remakes hub rebuild

**Hand this whole file to Manus.** Goal: rebuild the public remake hub so it is readable, branded, and not a thin dark card list.

**Live (temporary):** https://tiktok-remakes.vercel.app  
**Brand home:** https://www.teraustralis.com.au (CrystalCore.OS) — remakes should eventually live under this brand, not look like a random Vercel experiment.  
**Repo path:** `13_RESEARCH_SOURCES/sitting-2026-09-23-beyond-lucky-overlap/tiktok-replica/`

---

## Paste prompt for Manus

```
Rebuild the TikTok remakes hub as a proper TerAustralis / CrystalCore surface.

PROBLEM
The live hub at https://tiktok-remakes.vercel.app looks unfinished: dark monospace card dump, titles that don’t explain what you’re opening, no brand, no “what this is / what it isn’t,” and local-server instructions leaking onto a phone page.

WHAT THIS SITE IS
A phone-friendly index of 12 HTML shells. Each shell is a 9:16 format remake of a public TikTok style (news chyron, kinetic type, night-sky, etc.) for screen-recording. They are landscape / format references for a research sitting — NOT Beyond Lucky text overlap, NOT the original creators’ videos, NOT CrystalCore.OS itself.

WHAT THIS SITE IS NOT
- Not TerAustralis.com.au (that’s CrystalCore.OS)
- Not plagiarised TikToks — paraphrase captions; no creator marks, logos, or agency marks
- Not a product storefront

REQUIRED OUTPUT
1) A new hub page (site root index.html) that:
   - Leads with TerAustralis brand + one short line of what the page is
   - Groups remakes by format family (News / Kinetic type / Night-sky & lore / Fiction / Quote)
   - For each remake: human title, one-sentence “what you will see”, format tag, open button
   - Phone-first: big tap targets, no localhost/python instructions on the public page
   - Footer: “Format remakes only · temporary host · brand home teraustralis.com.au”
2) Keep each existing remake HTML file working (same filenames below). Do not delete shells.
3) Optional: light polish pass on hub copy only first; leave shell internals unless broken links.
4) Deliver: HTML/CSS (can be single index.html + shared CSS), mobile screenshots, and a short “what changed” note.

LAYOUT RULE (repo)
- Hub = index.html (Vercel root)
- Agent dialects remake = agent-dialects.html (not index.html)
- Do not use hub.html as the public entry

DESIGN DIRECTION
- One composition, not a dashboard
- Brand first (TerAustralis), then one headline, one supporting sentence, then the list
- Expressive type (not Inter/Roboto/system); avoid purple-glow AI cliché and warm-cream terracotta cliché
- Real atmosphere (subtle red-dust / starline cue OK) — not flat black with blue cards
- No floating badges/stickers on hero
- Cards only as the tap targets for each remake (interaction containers)

COPY TO USE (rewrite tighter if needed, keep facts)
Brand: TerAustralis
Headline: Format remakes
Support: Twelve 9:16 shells for phone screen-recording. Open → Fullscreen 9:16 → record.
Disclaimer: Paraphrased public captions. No creator marks. Landscape references only.

INVENTORY (keep all 12)
01 agent-dialects.html — Agent dialects — Kinetic type · Ask The AI style
02 gemini-rogue-news.html — Gemini rogue — News chyron / broadcast package
03 zero-dawn-pulse.html — Zero Dawn pulse — Cinematic orbital / magnetic pulse
04 altman-singularity-news.html — Altman singularity — Bay Desk news package
05 australia-first-eufta.html — Australia / EU FTA — Kinetic AusPol
06 agents-escape-sandbox.html — Agents escape sandbox — Terminal kinetic
07 ai-cloning-centers-fiction.html — AI cloning centers — Creepypasta fiction
08 multiplanetary-tonnage.html — Multi-planetary tonnage — Orbital quote
09 uap-disclosure-sky.html — UAP disclosure — Teal night-sky
10 openai-hf-agent-pov.html — OpenAI × HF agent POV — Explainer kinetic
11 anunnaki-reckoning-lore.html — Anunnaki reckoning — Mythos lore
12 uap-final-hour.html — UAP final hour — Ember night-sky sibling of 09

ONE-SENTENCE BLURBS (improve freely)
01 Kinetic type over code rain — agent “dialects” slam on.
02 Fake news desk + chyron about a rogue Gemini moment.
03 Orbital cinematic beat; magnetic-pulse / Zero Dawn energy.
04 Studio news wall + LIVE ticker; singularity milestone tone.
05 AusPol paddock dusk + slam kinetic type on FTA / Australia First.
06 Terminal grid; agents vanish from a sandbox.
07 Horror corridor; fiction banner — cloning-centers creepypasta.
08 Mars orbit quote cards; multi-planetary tonnage motivation.
09 Craft over treeline; disclosure beats under teal night sky.
10 Trace-log explainer from an agent’s point of view.
11 Pyramid / craft lore beats; Cinzel mythos energy.
12 Sibling of 09 with ember palette / “final hour” bed energy.

CONSTRAINTS
- Mobile-first 390px width must look intentional
- Preserve relative links to the 12 HTML files
- No Inter/Roboto/Arial; no purple-on-white gradient theme
- Do not claim these are official news or original TikToks
```

---

## Inventory (current live hub)

| # | File | Hub label now | Problem |
| --- | --- | --- | --- |
| — | `index.html` | Hub | Card list only; weak brand; developer “howto” on phone |
| 01 | `agent-dialects.html` | Agent dialects | Label OK; needs one-line “what you’ll see” |
| 02 | `gemini-rogue-news.html` | Gemini rogue | Opaque without context |
| 03 | `zero-dawn-pulse.html` | Zero Dawn pulse | Opaque |
| 04 | `altman-singularity-news.html` | Altman singularity | Opaque |
| 05 | `australia-first-eufta.html` | Australia / EU FTA | Opaque |
| 06 | `agents-escape-sandbox.html` | Agents escape sandbox | Opaque |
| 07 | `ai-cloning-centers-fiction.html` | AI cloning centers | Needs fiction flag in hub copy |
| 08 | `multiplanetary-tonnage.html` | Multi-planetary tonnage | Opaque |
| 09 | `uap-disclosure-sky.html` | UAP disclosure | Opaque |
| 10 | `openai-hf-agent-pov.html` | OpenAI × HF agent POV | Opaque |
| 11 | `anunnaki-reckoning-lore.html` | Anunnaki reckoning | Opaque |
| 12 | `uap-final-hour.html` | UAP final hour | Needs “sibling of 09” in copy |

## Why Manus (not this agent) for the visual rebuild

This agent can keep the ledger / shell files honest. Manus is the better seat for a full visual + copy rebuild you can iterate in their canvas, then drop the HTML back into `tiktok-replica/`.

**Helena:** no Helena seat/docs in this repo — if Helena is your other builder, paste the same prompt.

## After Manus returns

1. Replace `tiktok-replica/index.html` (and any CSS) with Manus output.  
2. Keep `agent-dialects.html` as the dialects shell.  
3. Delete or ignore `hub.html` (main-branch duplicate entry).  
4. Redeploy Vercel; later attach under `teraustralis.com.au`.
