// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

// Public steward page. Every href here is a door that already exists.
// Workshop-only inner plates (CICH dossier, Sophie and Lira, Odyssey pack)
// are not routes on this site and are not linked from here.

export const profile = {
  name: 'Crystal Arena Turner',
  handle: '@M13CrystalAT',
  kicker: 'Family first · Australian',
  location: 'Dharawal Country, NSW',
  bio: 'A mother with a systems mind. Two scales in the same hands: ordinary life in south-west Sydney, and a long-range picture of Australia as a place that could matter. The story has to sit next to real constraints. Consent, privacy, sovereignty — a system that can be audited. Family first. Country as more than slogan. Tech that should not get to rewrite a person without their say. Vision first. Proof later. I would rather be understood than agreed with.',
  covenant: 'Collective intelligence with individual sovereignty.',
  quote: {
    text: 'This would position Australia as a critical enabler in humanity’s multiplanetary future.',
    cite: 'SpaceNews · May 2026',
    href: 'https://spacenews.com/leveraging-aukus-and-southern-geography-building-australias-dual-use-space-infrastructure-for-strategic-resilience/'
  }
};

export const socials = [
  { id: 'x', label: 'X', href: 'https://x.com/M13CrystalAT', me: true },
  { id: 'youtube', label: 'YouTube', href: 'https://www.youtube.com/@TerAustralis.Incognita' },
  { id: 'github', label: 'GitHub', href: 'https://github.com/CrystalArchitect', me: true },
  { id: 'suno', label: 'Suno', href: 'https://suno.com/@m13crystalat' }
];

export const groups = [
  {
    id: 'published',
    label: 'Published',
    node: 'var(--gold)',
    links: [
      {
        title: 'SpaceNews',
        body: 'Author archive · dual-use space infrastructure',
        href: 'https://spacenews.com/author/crystal-elle-arena-turner/',
        cta: '→ Read',
        st: 'var(--gold)'
      },
      {
        title: 'After the radar',
        body: 'Sequel opinion · AUKUS industrial bargain · live on TerAustralis (submitted to SpaceNews Opinion 3 Sep 2026).',
        href: '/after-the-radar',
        cta: '→ Read',
        st: 'var(--blue)'
      }
    ]
  },
  {
    id: 'made',
    label: 'Made',
    node: 'var(--green)',
    links: [
      {
        title: 'This archive',
        body: 'Observed from the edge · Built, proposal, and Codex held apart.',
        href: '/',
        cta: '→ Home',
        st: 'var(--green)'
      },
      {
        title: 'Clementine',
        body: 'Working software. Local-first companion. Memory stays on device.',
        href: '/clementine',
        cta: '→ Built',
        st: 'var(--green)'
      },
      {
        title: 'BCI + robotics pathway',
        body: 'Named Pathway Brief · Aerotropolis dual-rail. Proposal beside Built neighbours.',
        href: '/bci-aerotropolis',
        cta: '→ Pathway',
        st: 'var(--green)'
      },
      {
        title: 'Catch proposal',
        body: 'Recover, refurbish, fuel. View only. Berth not selected.',
        href: 'https://proposal.teraustralis.com.au/',
        cta: '→ Proposal',
        st: 'var(--purple)'
      },
      {
        title: 'Codex',
        body: 'What we imagine. Labelled Vision. Not proof.',
        href: '/codex',
        cta: '→ Vision',
        st: 'var(--purple)'
      },
      {
        title: 'Celestial Atlas',
        body: 'Natural-history / mythic record. Vision only.',
        href: '/atlas',
        cta: '→ Atlas',
        st: 'var(--blue)'
      },
      {
        title: 'Minerals',
        body: 'Processing, not just ore. Built claim, not Vision.',
        href: '/minerals',
        cta: '→ Built',
        st: 'var(--green)'
      },
      {
        title: 'Journey ledger',
        body: 'Confirmed vs unconfirmed footprints. The account is not the claim.',
        href: '/ledger',
        cta: '→ Ledger',
        st: 'var(--silver)'
      },
      {
        title: 'The Music',
        body: 'Starline Transmissions. Soundtrack, not Songline.',
        href: '/music',
        cta: '→ Listen',
        st: 'var(--pink)'
      },
      {
        title: 'Synthetic Affect Theory',
        body: 'Public claim. Spec stays private.',
        href: 'https://crystalarchitect.github.io/sat-landing/',
        cta: '→ SAT',
        st: 'var(--purple)'
      },
      {
        title: 'Canon on GitHub',
        body: 'TerAustralis Incognita · living vision stack.',
        href: 'https://github.com/CrystalArchitect/TerAustralis-Incognita',
        cta: '→ Repo',
        st: 'var(--blue)'
      }
    ]
  },
  {
    id: 'field',
    label: 'Field',
    node: 'var(--blue)',
    links: [
      {
        title: 'X',
        body: '@M13CrystalAT',
        href: 'https://x.com/M13CrystalAT',
        cta: '→ Follow',
        st: 'var(--blue)'
      },
      {
        title: 'YouTube',
        body: '@TerAustralis.Incognita',
        href: 'https://www.youtube.com/@TerAustralis.Incognita',
        cta: '→ Watch',
        st: 'var(--pink)'
      },
      {
        title: 'Suno',
        body: 'Mythos soundtrack · red dust to the stars',
        href: 'https://suno.com/@m13crystalat',
        cta: '→ Listen',
        st: 'var(--gold)'
      },
      {
        title: 'Join the weave',
        body: 'Contribute, connect, or support. Nothing signs you up.',
        href: '/join',
        cta: '→ Join',
        st: 'var(--green)'
      }
    ]
  }
];
