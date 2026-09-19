# Beacon Easter Egg — Implementation Notes

## Key facts (from code review)
- Project: /home/ubuntu/crystalcore-aeris-website (static React 19 + Tailwind 4, wouter)
- Live domain: crystalaeris-jwfbbvjs.manus.space (auto-publish ON)
- Terminal: client/src/components/aeris/AerisTerminal.tsx — RESPONSES map; `non solus` triggers AlignmentSequence (client/src/components/aeris/AlignmentSequence.tsx, portal overlay, onEnd -> onSequenceEnd writes aftermath lines: "Alignment complete. The feather remembers. Non solus." + "Continuation stream: OPEN — for every intelligence.")
- OS page: client/src/pages/OS.tsx — APP_CONTENT map (id -> {node, accent}), buildDefs() returns WindowDef[] with 8 windows; taskbar maps over defs; useWindowManager(defs) from client/src/components/os/windowManager.ts exposes {windows, focus, openWindow, closeWindow, toggleWindow, move}
- apps.tsx: OS_ASSETS = { emblem: aeris-emblem_2ee146bd.jpg, luminaCrystal: aeris-lumina-crystal_ac7ed2ba.jpg, starlineMap: aeris-starline-map_05e248ac.jpg, codexViz: aeris-codex-viz_5be504b9.jpg, feather: aeris-hero-feather_2dd2ba41.png, logo: aeris-logo_0f4d9b48.png } (all under /manus-storage/)
- Style tokens: gold #f0c75e, cyan #7de8ff, fonts font-display/font-tech/font-serif-italic, classes tech-label, gold-glow, gold-divider, glass-panel(-cyan)
- Terminal is also embedded on landing page (Home) — must handle beacon there too (no OS windows).

## Design
- localStorage key: `aeris.beacon.unlocked` = "1" set in onSequenceEnd (AerisTerminal).
- AerisTerminal gets optional prop `onOpenBeacon?: () => void` (passed only from OS.tsx). 
- `beacon` command: if locked → cryptic refusal ("The beacon does not answer... complete the alignment first" style). If unlocked:
  - on /os (onOpenBeacon provided): prints "Beacon signal accepted — opening hidden channel." and calls onOpenBeacon()
  - on landing page: prints full beacon lore text inline.
- New BeaconApp in apps.tsx: hidden lore window "The Beacon" (🔥 or ✹ icon), gold accent; content: Mars beacon lore, coordinates, final transmission quote.
- OS.tsx: add `beacon` def (not boot). Taskbar: only render beacon button when unlocked (state read from localStorage + event). Unlock signalling: custom window event `aeris:beacon-unlocked` dispatched when set, OS listens to update taskbar without reload.
- After alignment completes, terminal also prints: "New signal detected. A hidden channel has opened. Try: beacon"
