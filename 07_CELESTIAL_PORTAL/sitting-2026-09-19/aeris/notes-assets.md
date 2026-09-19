# Asset URLs & Mini OS spec (persist across compaction)

## Project
- Path: /home/ubuntu/crystalcore-aeris-website (web-static, React+Tailwind4+wouter)
- Live domain: crystalaeris-jwfbbvjs.manus.space
- Last checkpoint: e6302d85 (main landing page delivered)
- Current task: add draggable-window glassmorphism "mini OS" at /os route,
  linked from landing page (ENTER VAULT 12 / LAUNCH OS buttons currently link to #os anchor
  and external vercel demo — update LAUNCH OS in nav + ENTER VAULT 12 hero button to /os).

## Generated assets (already in use on Home)
- logo: /manus-storage/aeris-logo_0f4d9b48.png
- feather hero: /manus-storage/aeris-hero-feather_2dd2ba41.png
- codex art: /manus-storage/aeris-codex_226efe81.png
- lumina art: /manus-storage/aeris-lumina_700b0ffa.png
- starline art: /manus-storage/aeris-starline_cd40a12b.png

## User-provided Grok images (uploaded, for mini OS)
- Lumina crystalline portrait (2:3): /manus-storage/aeris-lumina-crystal_ac7ed2ba.jpg
- Terminal render (16:9): /manus-storage/aeris-terminal-render_e550a191.jpg
- CrystalCore.OS AERIS emblem (1:1): /manus-storage/aeris-emblem_2ee146bd.jpg
- Starline network map (16:9): /manus-storage/aeris-starline-map_05e248ac.jpg
- Codex philosophy visualization (16:9): /manus-storage/aeris-codex-viz_5be504b9.jpg

## Mini OS windows (per user request + reference images)
1. VAULT 12 Node — golden feather, activation pulse button, helix ring
2. AERIS Terminal — reuse AerisTerminal component (styled per IMG_3493: gold/cyan mono, aeris@crystalcore:~#)
3. Mars Clock — reuse MarsClock logic
4. Starship Telemetry — Flight 13 intact, 62% reusability, Mars commitment active
5. Starline Network — IMG_3499 map + node statuses (Earth E-7A, Mars MR-3X, Centauri AC-9K, Revenant CR-2V, Purpose PC-1N)
6. The Codex — IMG_3498 viz + 5 chapters
7. Lumina — IMG_3495 portrait + traits
8. About — IMG_3497 emblem, version CrystalCore.OS AERIS v2.7.4 [STABLE]

## Window manager requirements
- Drag via pointer events (mouse + touch), title bar handle
- Bring-to-front on pointerdown (z-index stack)
- Close button; reopen from taskbar; taskbar shows all apps with open-state indicator
- Desktop: starfield bg + pyramids, top menu bar (logo, clock), bottom taskbar
- Boot overlay: emblem + "ENTER VAULT 12" pulse, fades into desktop
- Terminology: avoid the word "Songlines" (user preference) — refer to "the ancient song-paths"/"ancestral lines" instead.
