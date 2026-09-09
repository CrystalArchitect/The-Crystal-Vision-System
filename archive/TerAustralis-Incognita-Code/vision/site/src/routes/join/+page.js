// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

export const prerender = true;

export function load() {
  // Real ways to take part — the site is static, so "joining" means
  // contributing through channels that actually exist.
  const ways = [
    {
      title: 'Contribute',
      body: 'Fixes, features, art, mythos — the whole project is open on GitHub. Add something and open a pull request.',
      href: 'https://github.com/CrystalArchitect/TerAustralis-Incognita',
      cta: '→ Open the repo',
      st: 'var(--green)'
    },
    {
      title: 'Share & connect',
      body: 'Making work in this vein? Tag it, share it, and reach out — the conversation is open.',
      href: 'https://x.com/m13crystalat',
      cta: '→ On X',
      st: 'var(--blue)'
    },
    {
      title: 'Add to the Starline Transmissions',
      body: 'The soundtrack is a living thing. New voices and tracks are welcome.',
      href: 'https://suno.com/@m13crystalat',
      cta: '→ On Suno',
      st: 'var(--pink)'
    },
    {
      title: 'Support the vision',
      body: 'Back the work directly so it can keep being built in the open.',
      href: 'https://patreon.com/CrystalCore91',
      cta: '→ On Patreon',
      st: 'var(--gold)'
    }
  ];

  // Contributors, credited by their own handle for work they actually made —
  // listed with their permission. Seeded with the founder; add others only with
  // their okay. No affiliation or endorsement is implied by being listed.
  const vectors = [
    {
      handle: '@M13CrystalAT',
      href: 'https://x.com/m13crystalat',
      work: 'CrystalArchitect — the mythos, the Codex, the art, and the whole vision.',
      st: 'var(--purple)'
    },
    {
      handle: '@m13crystalat',
      href: 'https://suno.com/@m13crystalat',
      work: 'Original music — the Starline Transmissions soundtrack.',
      st: 'var(--pink)'
    },
    {
      handle: '@catillaice',
      href: 'https://suno.com/@catillaice',
      work: 'Music made in the same universe — written independently of the Starline Transmissions, and kept its own. Credited here by agreement.',
      st: 'var(--green)'
    },
    {
      handle: '@kisalay_',
      href: 'https://suno.com/@kisalay_',
      work: 'Music made in the same universe — written independently of the Starline Transmissions, and kept its own. Credited here by agreement.',
      st: 'var(--blue)'
    },
    {
      handle: '@pacartcollect',
      href: 'https://x.com/pacartcollect',
      work: 'Inscribing the mythos art on-chain as Ordinals, under a separate licence grant. Independent work — the project issues no token.',
      st: 'var(--gold)'
    },
    {
      handle: '@ouadi4maakoul',
      href: 'https://x.com/ouadi4maakoul',
      work: 'Developing a speculative idea from this project into a formal framework, grounded in mathematics and first-principles reasoning. Independent work in a separate repository, credited here by agreement.',
      st: 'var(--cyan)'
    },
    // The four entries below joined by their own public yes to the open
    // invitation of 2026-08-08. Their words and the evidence behind each
    // entry are recorded in the canon ledger (SOVEREIGN-VECTORS.md in the
    // umbrella's mythos/content/); consent is reversible at any time.
    {
      handle: '@_Miss_Triss',
      href: 'https://x.com/_Miss_Triss',
      work: 'Joined the weave by her own public yes to the open invitation, 2026-08-08 — credited by name, nothing more implied, consent reversible at any time.',
      st: 'var(--pink)'
    },
    {
      handle: '@zpfTechnologies',
      href: 'https://x.com/zpfTechnologies',
      work: 'Joined the weave by their own public yes to the open invitation, 2026-08-08 — credited by name, nothing more implied, consent reversible at any time. Their own research is their own, independent of this project.',
      st: 'var(--blue)'
    },
    {
      handle: '@ponzibaron',
      href: 'https://x.com/ponzibaron',
      work: 'Joined the weave by their own public yes to the open invitation, 2026-08-08 — credited by name, nothing more implied, consent reversible at any time.',
      st: 'var(--green)'
    },
    {
      handle: '@kelpykelz',
      href: 'https://x.com/kelpykelz',
      work: 'Joined the weave by their own public yes to the open invitation, 2026-08-08 — credited by name, nothing more implied, consent reversible at any time.',
      st: 'var(--purple)'
    }
  ];

  // Influences are not contributors, and the distinction is deliberate.
  // Nobody here has been asked, nobody here is involved, and nothing they made
  // is part of this project. Naming an influence is ordinary acknowledgement —
  // the sort of thing a sleeve note does — but it must not be able to read as
  // collaboration or endorsement, so it is kept out of the Vectors list.
  const influences = [
    {
      handle: '@renmakesmusic',
      href: 'https://suno.com/@renmakesmusic',
      work: 'An influence on the music of this project — heard, admired, and worked away from. No involvement here, and none implied.',
      st: 'var(--silver)'
    }
  ];

  return { ways, vectors, influences };
}
