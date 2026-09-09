// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

// The real repository portfolio — rendered from the Archive's own
// ledgers: the repository map, the per-repo STATUS files, and the
// six-repo archaeology of 2026-07-24. Ledger, not legend: every state
// below is recorded, dated, and checkable in the Archive. No invented
// provenance, no simulated metrics.

/**
 * @typedef {Object} RepoEntry
 * @property {string} id
 * @property {string} name - repository name on GitHub
 * @property {string} role - what it is, one breath
 * @property {'active'|'dormant'|'frozen'} state
 * @property {string} stateNote - the dated, checkable state line
 * @property {string[]} holds - what actually lives there
 * @property {string} [link] - GitHub URL (omitted for private repos)
 * @property {boolean} [isPrivate]
 */

/** @type {RepoEntry[]} */
export const repositories = [
  {
    id: 'umbrella',
    name: 'TerAustralis-Incognita',
    role: 'The umbrella — canon, governance, mythos, research. The charter every other repository derives from.',
    state: 'active',
    stateNote: 'The most active repository in the portfolio (archaeology, 2026-07-24).',
    holds: [
      'The Constitution, ADRs, and the governance stack',
      'The mythos — canon texts and the art collection',
      'The CrystalCore.OS terminal (mythos as a playable command line)',
      'Seven Sisters research and prototypes'
    ],
    link: 'https://github.com/CrystalArchitect/TerAustralis-Incognita'
  },
  {
    id: 'code',
    name: 'TerAustralis-Incognita-Code',
    role: 'The software home — the engine, the vision app, and this website’s source.',
    state: 'active',
    stateNote: 'CI runs five suites on every push; all passing at last record (2026-07-24).',
    holds: [
      'Crystal Core engine — Clementine bridge, consent_transport, RDP',
      'Clementine, the local-first companion (terminal, API, web UI)',
      'This site'
    ],
    link: 'https://github.com/CrystalArchitect/TerAustralis-Incognita-Code'
  },
  {
    id: 'archive',
    name: 'CrystalCore.OS-the-Crystal-Architecture-Archive',
    role: 'The system ledger — the portfolio’s meta-record, all Markdown.',
    state: 'active',
    stateNote: 'Documents the other five; this page renders from its ledgers.',
    holds: [
      'The knowledge base — architecture, governance, glossary, corrections',
      'The fleet-wide STATUS ledger',
      'The repository archaeology (evidence-tiered, 2026-07-24)'
    ],
    link: 'https://github.com/CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive'
  },
  {
    id: 'origin',
    name: 'The-Crystal-Vision',
    role: 'The origin — where it began, and the oldest commits anywhere in the portfolio.',
    state: 'dormant',
    stateNote: 'First commit 2026-07-14; dormant since 2026-07-17 — preserved as history, not built upon.',
    holds: [
      'The first-generation codex site',
      'The crystalcore v0.13.4 Python package (recovered)',
      'The founding laptop’s final snapshot'
    ],
    link: 'https://github.com/CrystalArchitect/The-Crystal-Vision'
  },
  {
    id: 'protocol-pack',
    name: 'crystalcore',
    role: 'The frozen protocol pack — the Seven Sisters paths and the first protocol sketches, sealed as provenance.',
    state: 'frozen',
    stateNote: 'Every commit dated 2026-07-17; superseded by carried-forward copies in the umbrella and code repositories.',
    holds: [
      'Seven Sisters Songline documents (honoured as story)',
      'The earliest bridge and interface sketches',
      'BLUEPRINT v0.3 and the first architecture spec'
    ],
    link: 'https://github.com/CrystalArchitect/crystalcore'
  },
  {
    id: 'demo-shell',
    name: 'crystal-vision',
    role: 'The frozen demo shell — a single-page interface experiment from the founding week.',
    state: 'frozen',
    stateNote: 'Private repository; audited 2026-07-24 — functional static demo, kept as provenance.',
    holds: [
      'The static interface shell (one page, no build step)',
      'The Grok Build v0.4.0 manifest'
    ],
    isPrivate: true
  }
];

export const stateLabels = {
  active: 'Active',
  dormant: 'Dormant · preserved',
  frozen: 'Frozen · provenance'
};
