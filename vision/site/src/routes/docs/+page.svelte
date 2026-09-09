<script>
  /** @type {{ data: { docs: { slug: string, title: string, description: string }[] } }} */
  let { data } = $props();

  const groups = [
    {
      label: 'Built / implemented',
      note: 'Working surfaces and recorded methods.',
      tone: 'var(--observatory-built)',
      slugs: ['clementine', 'consent-transport', 'governance', 'provenance']
    },
    {
      label: 'Partial / in development',
      note: 'Technical and strategic work still being developed or evaluated.',
      tone: 'var(--observatory-experiment)',
      slugs: [
        'architecture',
        'blueprint-v0.3',
        'milestones',
        'quantum-lattice-case-study',
        'strategy',
        'silicon-brain-brief',
        'after-the-radar',
        'named-pathway-brief-bci-robotics-aerotropolis'
      ]
    },
    {
      label: 'Vision / design',
      note: 'Interpretive, narrative, and proposed material. Read the status seal on each document.',
      tone: 'var(--observatory-vision)',
      slugs: []
    }
  ];

  /** @param {{ slugs: string[] }} group */
  function groupedDocs(group) {
    if (group.slugs.length) return data.docs.filter((doc) => group.slugs.includes(doc.slug));
    const assigned = groups.flatMap((item) => item.slugs);
    return data.docs.filter((doc) => !assigned.includes(doc.slug));
  }
</script>

<svelte:head>
  <title>The Archive — TerAustralis Incognita</title>
  <meta name="description" content="The living archive of TerAustralis Incognita, grouped by demonstrated work, development, and vision-layer material." />
</svelte:head>

<section class="archive-hero">
  <p class="eyebrow">TerAustralis Incognita · source index</p>
  <h1>The Archive</h1>
  <p class="lede">A field guide to the documents that shape the project. The archive is grouped for discovery; the source documents retain their authoritative wording.</p>
  <p class="verified">LAST VERIFIED · CURRENT REPOSITORY CHECKOUT</p>
</section>

{#each groups as group}
  <section class="archive-group" aria-labelledby={`group-${group.label}`}>
    <div class="group-heading" style={`--group-tone:${group.tone}`}>
      <p class="eyebrow">Index / {String(groups.indexOf(group) + 1).padStart(2, '0')}</p>
      <h2 id={`group-${group.label}`}>{group.label}</h2>
      <p>{group.note}</p>
    </div>
    <div class="archive-grid">
      {#each groupedDocs(group) as doc (doc.slug)}
        <a class="archive-card" href={`/docs/${doc.slug}`} style={`--group-tone:${group.tone}`}>
          <span class="archive-status">{group.label.split(' / ')[0].toUpperCase()}</span>
          <strong>{doc.title}</strong>
          {#if doc.description}<span>{doc.description}</span>{/if}
          <span class="archive-cta">Open document <span aria-hidden="true">↗</span></span>
        </a>
      {/each}
    </div>
  </section>
{/each}

<style>
  .archive-hero { padding: 7rem 0 5rem; max-width: 52rem; }
  h1, h2 { color: #f5f0e6; font-family: var(--font-display); font-weight: 500; letter-spacing: -.04em; }
  h1 { font-size: clamp(3.5rem, 9vw, 7rem); line-height: .9; }
  h2 { font-size: clamp(1.8rem, 4vw, 3rem); line-height: 1; }
  .lede { max-width: 48ch; margin-top: 1.4rem; color: var(--observatory-muted); font-size: 1.05rem; }
  .verified { margin-top: 2rem; color: var(--observatory-copper); font: .67rem/1 var(--font-mono); letter-spacing: .13em; }
  .archive-group { padding: 3.5rem 0 4.5rem; border-top: 1px solid var(--observatory-line); }
  .group-heading { border-left: 2px solid var(--group-tone); padding-left: 1rem; }
  .group-heading .eyebrow { color: var(--group-tone); margin-bottom: .65rem; }
  .group-heading > p:last-child { margin-top: .7rem; color: var(--observatory-muted); }
  .archive-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1px; margin-top: 2rem; background: var(--observatory-line); border: 1px solid var(--observatory-line); }
  .archive-card { display: flex; flex-direction: column; min-height: 190px; padding: 1.35rem; background: var(--observatory-surface-deep); color: #f5f0e6; }
  .archive-card:hover { background: var(--observatory-surface); text-decoration: none; }
  .archive-status { color: var(--group-tone); font: .64rem/1 var(--font-mono); letter-spacing: .13em; }
  .archive-card strong { margin-top: 2.8rem; font: 500 1.4rem/1.15 var(--font-display); color: #f7f3ea; }
  .archive-card > span:nth-child(3) { color: var(--observatory-muted); font-size: .84rem; line-height: 1.45; margin-top: .65rem; }
  .archive-cta { color: var(--group-tone); font: .68rem/1 var(--font-mono); letter-spacing: .1em; margin-top: auto; padding-top: 1.2rem; text-transform: uppercase; }
  @media (max-width: 700px) { .archive-hero { padding: 5rem 0 3.5rem; } .archive-grid { grid-template-columns: 1fr; } }
</style>
<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
