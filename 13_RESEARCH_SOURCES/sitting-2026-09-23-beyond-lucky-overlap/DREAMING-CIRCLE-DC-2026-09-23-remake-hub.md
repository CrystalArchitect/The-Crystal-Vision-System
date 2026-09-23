# Dreaming Circle — DC-2026-09-23-remake-hub

**Canon:** **no**  
**Domain:** ops  
**Consent:** yes (sitting work; public URLs)  
**Pool:** remake-hub deploy / 404 episode (23 Sep 2026)  
**Field sheet:** [`DREAMING-CIRCLES-FIELD-SHEET.md`](DREAMING-CIRCLES-FIELD-SHEET.md)

---

## 1. Record (trees already paid)

| Node | Action | Outcome | Score |
| --- | --- | --- | --- |
| n1 | Open `tiktok-remakes.vercel.app/` | 404 NOT_FOUND (syd1) | 0 |
| n2 | Open `…/index` | 308 → `/` → 404 (cleanUrls loop) | 0 |
| n3 | Open `…/hub` | 200 on some hosts | 1 |
| n4 | Open `crystal-tiktok-remakes.vercel.app/` | 200 hub | 2 |
| n5 | `vercel.json` cleanUrls true | root maps index→`/index` not `/` | 0 |
| n6 | `cleanUrls: false` + rewrite `/`→`/index.html` | temp deploy `/` = 200 | 2 |
| n7 | Point docs/phone to crystal host | usable phone URL | 2 |

Tree id: `T-remake-hub-404`

---

## 2. Pool

- Only ops nodes above  
- No mythos  
- Consent: public deploy debug for TerAustralis remake hub  

---

## 3. Dream (policies — offline)

**P0 (current / what we landed):**  
Prefer `crystal-tiktok-remakes.vercel.app`. Keep `cleanUrls: false` + `/`→`/index.html`. Tell humans the old hostname 404s.

**P1:**  
Always verify `/` with `curl -sI` after every Vercel deploy before sending a phone URL. If `/` ≠ 200, do not publish the link.

**P2:**  
Single canonical project name only; delete or redirect dead `tiktok-remakes` hostname so two URLs cannot diverge.

**P3:**  
Ship hub as `hub.html` at a clean path and put a tiny root `index.html` that only meta-refreshes to `/hub.html` (avoid cleanUrls index remap entirely).

**Score on this pool:** P1 wins for *next* deploys (cheap, prevents repeat 404 on phone). P0 stays live now. P2 nice later. P3 compost unless cleanUrls bites again.

---

## 4. Receipt (four lines)

1. Remake hub `/` 404’d because cleanUrls remapped `index.html` → `/index`.  
2. Working phone host today: `crystal-tiktok-remakes.vercel.app`.  
3. Learning: never hand a phone URL without a 200 on `/`.  
4. Policy candidate P1 — Gate pending Crystal.

---

## 5. Gate

- [ ] **stamp** P1 as deploy checklist policy v1  
- [ ] **refuse** — keep ad-hoc only  
- [ ] **compost** — receipt only  

Crystal: ________  date: ________

---

## Fixed / may improve

| Fixed | May improve |
| --- | --- |
| Vendor weights | Which URL we publish |
| Human publishes | Post-deploy `/` check |
| No weight fine-tune | Host naming hygiene |

*Thought over history. This circle is a receipt, not a masthead.*
