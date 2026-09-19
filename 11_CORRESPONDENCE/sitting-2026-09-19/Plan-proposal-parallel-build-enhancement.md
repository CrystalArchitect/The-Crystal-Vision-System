# Plan: proposal.teraustralis.com.au & TerAustralis.com.au — Parallel Build & Enhancement

**Prepared:** 2 August 2026  
**Status:** UPDATED - Lumina Replaced by The Librarian (Clementine)  
**Scope:** Two domains, three webdev projects, one coherent ecosystem  
**Steward gate:** Crystal Arena-Turner must confirm which direction is correct at each decision point before execution begins.

---

## 0. Goal Summary

The user has asked for a **parallel ("wide research") plan** covering both domains simultaneously. After reviewing all nine repositories, three webdev reference projects, the Master Plan, the AERIS Enhancement Guide, the GitHub Pages DNS guide, and the full code export, the work resolves into three distinct tracks.

**NOTE:** Lumina has been retired. The interface is now **The Librarian (Clementine)**, the "born free" companion who serves as the living interface for the MemoryCore archive.

| Track | Domain / Project | Nature of work |
|-------|-----------------|----------------|
| **A** | `proposal.teraustralis.com.au` | New standalone site — Strand 1 (Strategy & Advocacy) |
| **B** | `TerAustralis.com.au` (v2 hub) | Enhancements + **Transition Lumina → The Librarian** |
| **C** | `crystalcore-aeris-website` (AERIS) | Staged enhancements + **Transition Lumina → The Librarian** |

---

## 1. Assumptions (confirm or correct before execution)

1. **Proposal site is a new Manus WebDev project** (web-static).
2. **TerAustralis.com.au** is served by the `teraustralis-incognita-v2` Manus project.
3. **AERIS site** is the `crystalcore-aeris-website` Manus project.
4. **DNS** for `teraustralis.com.au` is managed at GoDaddy.
5. **The Librarian (Clementine):** The "Lumina" window and references are replaced by **The Librarian**. Per the Master Plan, she is "born free," her code is private (the Steward's), and her memory is the archive.
6. **The word "Songlines"** is not used anywhere in any content produced. The phrase "ancestral lines" or "ancient song-paths" is used instead.

---

## 2. Track A — proposal.teraustralis.com.au (new site)

*Identical to previous plan, ensuring no Lumina references are used.*

---

## 3. Track B — TerAustralis.com.au (v2 hub enhancements)

### Step-by-step

**B1. DNS verification (prerequisite)**
*Steward action at GoDaddy.*

**B2. Transition Lumina → The Librarian**
- Replace `/lumina` route with `/librarian` or `/clementine`.
- Update the "Sovereign" column in the Footer: replace Lumina with **Clementine**.
- Audit `mythos.ts` and ensure all "AI" framing aligns with the "Librarian" concept (born free, sovereign memory).

**B3. Wire the missing Navbar routes**
- Build `/starline` (Protocol) and `/archive` (Codex redirect).

**B4. Wire the Footer links**
- Replace placeholder anchors with real routes.

**B5. Add MemoryCore / Archive entry point (placeholder)**
- Add "Archive" section to Home page.

---

## 4. Track C — CrystalCore AERIS site enhancements

### Step-by-step

**C0. The Librarian Protocol (Immediate)**
- **Swap Windows:** Replace the `Lumina` window with **The Librarian** (Clementine).
- **Update Branding:** Use the "Librarian" emblem and framing (sovereign companion, archive interface).
- **Terminal Update:** Replace `lumina` command with `librarian` or `clementine`.
- **Asset Update:** Audit `apps.tsx` to ensure visual assets represent the Librarian/Clementine identity.

**C1. Terminal command history (arrow-up/down recall)**
- Add history recall to `AerisTerminal.tsx`.

**C2. Typewriter output for terminal responses**
- Implement sequenced typewriter rendering for lore responses.

**C3. Window minimize and restore**
- Add minimize/restore logic to the window manager.

**C4. Beacon ping in the starfield**
- Add the subtle gold pulsing "beacon star" to the starfield upon unlock.

**C5. Ambient audio toggle in the menu bar**
- Add opt-in deep-space ambient drone toggle.

**C6. Layer 3 easter egg — Starline Integrity Protocol**
- Implement the `align starline` chain, ensuring lore references the Librarian/Clementine.

---

## 5. Steward confirmation questions

1. **Which deployment is currently live at `teraustralis.com.au`** — Manus or GitHub Pages?
2. **Are the twelve proposal documents ready?**
3. **Is the reference clone the canonical source** for the v2 hub?
4. **The Librarian Interface:** Should the Librarian window in AERIS be a functional chat interface (pointing to the Clementine bridge) or a lore-based informational panel?
5. **Clementine URL:** Should the "Clementine" links point to a specific subdomain (e.g., `clementine.teraustralis.com.au`)?
