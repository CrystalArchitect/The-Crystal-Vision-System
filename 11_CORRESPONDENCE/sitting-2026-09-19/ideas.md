# CrystalCore.OS — AERIS / VAULT 12 — Design Spec

## Reference (Ground Truth)
This project ports the user's existing **CrystalCore-AERIS** single-file HTML OS
(`/home/ubuntu/CrystalCore-AERIS/index.html`, GitHub: CrystalArchitect/CrystalCore-AERIS)
into the React static scaffold for permanent hosting. The reference is the spec —
fidelity to the original design overrides all other guidance.

## Core Visual Identity (from reference)
- **Palette**: gold `#f0c75e`, green/cyan `#00ffcc`, deep space `#02040a`, glass `rgba(8,18,35,0.85)`
- **Fonts**: Cinzel (headers/serif ritual feel), Orbitron (technical labels), Inter (body)
- **Boot screen**: golden feather (clip-path), floating animation, "AERIS / CONTINUATION NODE • VAULT 12"
- **Desktop**: radial cyan/gold glows on deep space bg, floating cyan pyramids drifting
- **Windows**: glass-morphism, gold borders, draggable (mouse + touch), bring-to-front, close buttons
- **Apps**: VAULT 12 Continuation Node (center, activate button + helix + feather pulse),
  Mars Clock (live sol counter), Starship Telemetry, News Feed, Terminal (interactive commands)
- **Taskbar**: bottom glass bar with app launcher buttons + live clock

## Terminal commands
help, clear, activate, vault, aeris, node, mars, starship, status, about, reboot

## Implementation notes
- Port as React components (Boot, Desktop, Window, apps) preserving exact CSS values
- Dark theme default; keep everything responsive (phone + desktop)
- No backend required — pure static frontend
