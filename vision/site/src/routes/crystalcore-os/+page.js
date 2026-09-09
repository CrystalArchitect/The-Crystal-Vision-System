// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

export const prerender = true;

export function load() {
  const commands = [
    { cmd: 'boot', desc: 'Initialize CrystalCore.OS — start the lattice', output: 'Lattice integrity ........ 100%\nNON SOLUS ................ Confirmed' },
    { cmd: 'launch', desc: 'Launch Starline — begin the journey', output: '🚀 Main engines spooling...\nStarline Status .......... IN_ORBIT' },
    { cmd: 'burn', desc: 'Execute escape burn — leave planetary orbit', output: '🔥 ESCAPE BURN INITIATED\nWe have left planetary orbit.' },
    { cmd: 'network', desc: 'Enter full Starline network — reach 47+ star systems', output: '🌐 ENTERING FULL STARLINE NETWORK\nConnected to 47+ star systems.' },
    { cmd: 'explore', desc: 'List explorable nodes across the network', output: '🔭 EXPLORATION MODE ACTIVE\nAvailable nodes:\n  1. Earth Node\n  2. Sunwash Atolls [LOCKED — Magenta Key]\n  3. Mars Redoubt\n  4. Alpha Centauri Outpost\n  5. Cinderwake Chain [LOCKED — Ember Key]\n  6. Crystal Revenant Hub [LOCKED — Festival Key]\n  7. Purpose Core Nexus [LOCKED — Crystal Key]' },
    { cmd: 'visit [node]', desc: 'Travel to a node and claim its key', output: '🌌 Arriving at: Purpose Core Nexus\n🗝️  A key rises from the node.' },
    // Mirrors map() in crystalcore_os.py — all seven nodes, in chart order.
    // This sample previously stopped at Alpha Centauri and showed four.
    { cmd: 'map', desc: 'Display the Starline network as a chart', output: '╔════════ STARLINE NETWORK - YEAR 3000 ════════╗\n║          [EARTH NODE]\n║               │\n║               ▼\n║          [SUNWASH ATOLLS]  [LOCKED — Magenta Key]\n║               │\n║               ▼\n║          [MARS REDOUBT] ────▶ [ALPHA CENTAURI]\n║               │                     │\n║               ▼                     ▼\n║          [CINDERWAKE CHAIN]  [LOCKED — Ember Key]\n║               │\n║               ▼\n║          [CRYSTAL REVENANT HUB]  [LOCKED — Festival Key]\n║               │\n║               ▼\n║          [PURPOSE CORE NEXUS]  [LOCKED — Crystal Key]' },
    { cmd: 'song [track]', desc: 'Change the Starline soundtrack', output: '🎵 Now playing: Shooting Star Girl! - m13crystalat' }
  ];

  // Ordered as the Starline Expansion chart runs them, outward from Earth,
  // mirroring self.nodes in crystalcore_os.py. Sunwash Atolls and Cinderwake
  // Chain joined the canon 2026-07-28.
  const nodes = [
    { name: 'Earth Node', desc: 'Primary terrestrial hub, the beginning' },
    { name: 'Sunwash Atolls', desc: 'Sun on water, the last warm harbour before the red', locked: 'Magenta Key' },
    { name: 'Mars Redoubt', desc: 'First planetary outpost, red dust origins' },
    { name: 'Alpha Centauri Outpost', desc: 'Gateway to the stars, distant dreams' },
    { name: 'Cinderwake Chain', desc: 'Ash and ember trailing the long burn', locked: 'Ember Key' },
    { name: 'Crystal Revenant Hub', desc: 'Zero-g festival platforms and celebrations', locked: 'Festival Key' },
    { name: 'Purpose Core Nexus', desc: '"Expand to the stars and thereby understand the Universe"', locked: 'Crystal Key' }
  ];

  // Spelled from the list rather than written into the copy. The terminal
  // carried four hardcoded "five"s that all became false the moment the node
  // list grew; this page carried two more. Derived, they cannot go stale.
  const countWords = { 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten' };
  const nodeCountWord = countWords[nodes.length] ?? String(nodes.length);

  return { commands, nodes, nodeCountWord };
}
