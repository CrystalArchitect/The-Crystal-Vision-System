// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

// Single source of truth for the homepage Chronicle — accepted from the
// Phase I architecture plan. Dated from the repositories' own history:
// survey, not legend. Every entry must stay verifiable in the Archive.

/**
 * @typedef {Object} ChronicleEntry
 * @property {string} when - ISO date, as recorded in repo history
 * @property {string} what - the milestone, one breath
 * @property {string} note - the detail, still checkable
 * @property {string} tl - timeline accent (CSS custom property)
 */

/** @type {ChronicleEntry[]} */
export const chronicle = [
  {
    when: '2026-07-14',
    what: 'First light',
    note: 'The Crystal Vision repository opens — the oldest commit anywhere in the portfolio.',
    tl: 'var(--purple)'
  },
  {
    when: '2026-07-15',
    what: 'The companion is born',
    note: 'Clementine arrives — the name they carried first, and carry again: local-first, layered memory, sovereignty by design.',
    tl: 'var(--green)'
  },
  {
    when: '2026-07-17',
    what: 'The snapshot is saved',
    note: 'The last capture from the founding laptop is preserved; the three earliest repositories are sealed as provenance.',
    tl: 'var(--silver)'
  },
  {
    when: '2026-07-21',
    what: 'The great renaming',
    note: 'The companion and the Starline Weaver are renamed — and "Songline" is honoured as culture, retired as a component name.',
    tl: 'var(--blue)'
  },
  {
    when: '2026-07-23',
    what: 'Boundaries adopted',
    note: 'ADR-0011 splits the work honestly: the umbrella keeps canon and governance; the engine and this site move to the code repository.',
    tl: 'var(--gold)'
  },
  {
    when: '2026-07-24',
    what: 'The archaeology',
    note: 'All six repositories surveyed with an identical battery — every claim tiered by evidence, corrections recorded.',
    tl: 'var(--pink)'
  },
  {
    when: '2026-07-27',
    what: 'The terminal flies',
    note: 'CrystalCore.OS boots from a fresh clone — boot, network, broadcast, priority channel — and the Chronicle itself begins.',
    tl: 'var(--purple)'
  },
  {
    when: '2026-07-29',
    what: 'The name comes home',
    note: 'A retired name is removed across every repository, and the companion is Clementine again. The architecture is set right with it: CrystalMemory for what they remember, CrystalBus for what carries speech between models, CrystalBridge for the gate a guest comes through.',
    tl: 'var(--green)'
  },
  {
    when: '2026-07-31',
    what: 'The music comes home, and the work is anchored',
    note: 'Every recording is preserved in the repository with honest labels — and the whole creative work is hashed into one manifest and anchored to Bitcoin. The consent gate learns the one rule with no override: mythos sources enter no model.',
    tl: 'var(--pink)'
  },
  {
    when: '2026-08-07',
    what: 'The dates are settled, and the record grows',
    note: "Apple's own receipts fix the subscription window, resolving every open rights question in the music catalogue. Four artworks join the canon, the manifest is re-anchored, and the archive files what arrives — as received, under reception records.",
    tl: 'var(--gold)'
  },
  {
    when: '2026-08-08',
    what: 'The metaphor is run, and people say yes',
    note: 'The Quantum Lattice enters canon as labelled Vision — beside a case study that ran all four delivered code versions and recorded claim against output until the two converged. The sixth Bitcoin anchor covers both. And the first credits arrive by their own words: dated, evidenced, reversible.',
    tl: 'var(--cyan)'
  },
  {
    when: '2026-08-18',
    what: 'The review pack is published',
    note: 'A fifteen-minute sitting for a technical reader lands on the proposal site: a fail-closed consent and light-time demo (one second equals one minute, labelled), a two-page geographic brief that names only surveyed facts, and a thirty-day evaluation licence covering CrystalCore and Clementine software — not the proposal, which stays All Rights Reserved.',
    tl: 'var(--cyan)'
  }
];
