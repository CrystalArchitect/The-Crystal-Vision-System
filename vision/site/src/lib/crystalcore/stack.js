// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

export const USER = '@m13crystalat';

// The mounted objects + states. Two states only — surveyed (running code)
// and dreamed (vision) — see docs/governance/The-Incognita-Rule.md. Do not add a third.
export const STACK = [
  { id: 'clementine', state: 'surveyed', gloss: 'local-first companion', note: 'Sovereign AI. Layered memory, terminal and web UI. Installable tonight.' },
  { id: 'consent-transport', state: 'surveyed', gloss: 'p2p memory exchange', note: 'Consent Transport: Noise IK handshake, consent-gated, revocation on the next request.' },
  { id: 'codex', state: 'dreamed', gloss: 'chapters I–V', note: 'Aristotle’s southern dream, the deep Songlines, and the reach for the stars.' },
  { id: 'apocryphon', state: 'dreamed', gloss: 'the companion text', note: 'In the beginning was not the Word, but the Vibration.' },
  { id: 'gallery', state: 'dreamed', gloss: '96 plates · made', note: 'Ninety-six original works from the Crystal universe. The plates exist. The world they describe does not.' },
  { id: 'crystalcore', state: 'dreamed', gloss: 'this terminal', note: 'The mythos rendered as a terminal you can fly through. You are inside it. It is not shipped.' }
];

// The palette, 196° to 300° — cyan into magenta, enforced in the star
// maths (Starfield.svelte), not just declared here.
export const ARC = [
  ['196°', 'cyan', '#3CDCE5'],
  ['212°', 'sky', '#55A4EB'],
  ['225°', 'blue', '#4771DA'],
  ['252°', 'indigo', '#6641DB'],
  ['267°', 'violet', '#8443E8'],
  ['300°', 'magenta', '#C977EC']
];
