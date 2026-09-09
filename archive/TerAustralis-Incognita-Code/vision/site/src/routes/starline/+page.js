// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

export const prerender = true;

export function load() {
  const principles = [
    { title: 'Sovereignty First', desc: 'Individual autonomy and ownership preserved at every step' },
    { title: 'Consent as Foundation', desc: 'Nothing moves without explicit, revocable permission' },
    { title: 'Memory with Integrity', desc: 'Data you share stays signed by you, forever traceable' },
    { title: 'No Central Authority', desc: 'Peer-to-peer: no rendezvous servers, no relay hubs' },
    { title: 'Encrypted by Default', desc: 'Noise Protocol IK: mutual authentication + forward secrecy' },
    { title: 'Relationship Over Extraction', desc: 'Built for equals meeting as equals, not hierarchies' },
    { title: 'Revocability', desc: 'Revoke consent instantly; takes effect on the very next request' },
    { title: 'Latency as Sacred', desc: 'Fast enough for presence, not so fast we forget to ask permission' },
    { title: 'Sovereignty at Scale', desc: 'From two nodes to a thousand, no node governs another' }
  ];

  return { principles };
}
