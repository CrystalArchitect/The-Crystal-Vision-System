<script>
  import { onMount } from 'svelte';

  let glow = true;
  let activeStar = null;
  let mounted = false;

  const constellations = [
    { id: 'I', name: 'First Sketch', x: 112, y: 166, note: 'seated figure sketching' },
    { id: 'II', name: 'Path of Footprints', x: 220, y: 252, note: 'winding trail' },
    { id: 'III', name: 'The Storm', x: 385, y: 205, ghost: true, note: 'empty circle · faint ghost' },
    { id: 'IV', name: 'Southern Edge', x: 320, y: 414, note: 'low arc · southern boundary' },
    { id: 'V', name: 'Groundkeeper', x: 685, y: 144, note: 'single bright star · faint staff' },
    { id: 'VI', name: 'The Rebuilt Chart', x: 530, y: 360, note: 'dense lattice · finer threads' },
    { id: 'VII', name: 'The Rocket', x: 615, y: 270, note: 'bright star · ascending trail' },
    { id: 'VIII', name: 'The Returning Gaze', x: 746, y: 350, note: 'arc of stars · watchful' },
    { id: 'IX', name: 'The Shared Fire', x: 548, y: 456, note: 'seven stars · shared flame' },
    { id: 'X', name: 'The Far Horizon', x: 760, y: 492, note: 'distant light · open way' }
  ];

  const trail = [
    [112, 166], [220, 252], [320, 414], [548, 456], [760, 492],
    [746, 350], [685, 144], [615, 270], [530, 360]
  ];

  onMount(() => {
    mounted = true;
  });

  function setActive(id) {
    activeStar = id;
  }
</script>

<svelte:head>
  <title>Atlas of The Ten — Southern Observatory</title>
  <meta name="description" content="A fictional Southern Observatory atlas plate for The Ten, presented as interpretive story-layer work." />
</svelte:head>

<article class="atlas-ten" class:glow-on={glow}>
  <header class="atlas-header">
    <div class="eyebrow">TerAustralis Incognita — Southern Pillar</div>
    <h1>Atlas of <em>The Ten</em></h1>
    <p class="dek">Charted right both ways — 1860–1872 — Path of Footprints, Storm, Groundkeeper</p>
    <p class="subdek">A fictional Southern Observatory plate, observed from the edge.</p>
  </header>

  <section class="boundary boundary-top" aria-label="Fictional story-layer notice">
    <strong>FICTIONAL STORY-LAYER WORK</strong>
    <p>This interactive atlas is an interpretive literary work. Its dates, chart marks, and star-lines are invented devices; it is not a sky survey, scientific observation, cultural record, or governance instrument.</p>
  </section>

  <section class="chart-shell" aria-labelledby="chart-title">
    <div class="chart-heading">
      <div>
        <div class="chart-label" id="chart-title">CHART T-10 · SOUTHERN PILLAR · FICTIONAL DATE 1860–1872</div>
        <div class="chart-caption">Hover or focus a position to read its story-layer annotation.</div>
      </div>
      <button class="glow-toggle" type="button" aria-pressed={glow} on:click={() => (glow = !glow)}>
        {glow ? 'GLOW ON' : 'GLOW OFF'}
      </button>
    </div>

    <div class="chart-frame">
      <svg class="star-chart" viewBox="0 0 860 540" role="img" aria-labelledby="chart-title chart-desc">
        <desc id="chart-desc">Ten fictional constellation positions connected by a thin Southern Observatory trail. The Storm is represented by an empty boundary circle.</desc>
        <defs>
          <linearGradient id="trail-gradient" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="var(--atlas-accent)" stop-opacity=".18" />
            <stop offset=".5" stop-color="var(--atlas-accent)" stop-opacity=".82" />
            <stop offset="1" stop-color="var(--atlas-accent)" stop-opacity=".25" />
          </linearGradient>
        </defs>
        <polyline class="trail-line" points={trail.map(([x, y]) => `${x},${y}`).join(' ')} />
        <circle class="storm-circle" cx="385" cy="205" r="42" />
        <text class="chart-note" x="385" y="275" text-anchor="middle">STORM · ABSENCE / BOUNDARY</text>
        {#each constellations as star}
          <g class:active={activeStar === star.id} class="star-group" on:mouseenter={() => setActive(star.id)} on:mouseleave={() => (activeStar = null)}>
            <circle class="hit-area" cx={star.x} cy={star.y} r="24" tabindex="0" role="button" aria-label={`${star.id}. ${star.name}`} on:focus={() => setActive(star.id)} on:blur={() => (activeStar = null)} />
            <circle class:ghost={star.ghost} class="star-point" cx={star.x} cy={star.y} r={star.ghost ? 0 : star.id === 'I' || star.id === 'V' ? 5 : 3.5} />
            <text class="roman" x={star.x} y={star.y + 22} text-anchor="middle">{star.id}</text>
            <text class="star-name" x={star.x} y={star.y - 16} text-anchor="middle">{star.name}</text>
          </g>
        {/each}
      </svg>
    </div>

    <div class="chart-footer">
      <span>1860–1872 · Terra → TerAustralis</span>
      <span>Faint ghost · mark boundary · pass with care</span>
      <span>Ground remembers · sky returns</span>
    </div>
  </section>

  <section class="position-index" aria-labelledby="index-title">
    <div class="section-label" id="index-title">TEN POSITIONS · STORY-LAYER INDEX</div>
    <div class="index-grid">
      {#each constellations as star}
        <button class:active={activeStar === star.id} type="button" class="index-item" on:click={() => setActive(star.id)}>
          <span class="index-id">{star.id}</span>
          <span class="index-name">{star.name}</span>
          <span class="index-note">{star.note}</span>
        </button>
      {/each}
    </div>
  </section>

  <section class="prose-layer" aria-labelledby="fragment-title">
    <div class="source-label" id="fragment-title">APOCRYPHON · FRAGMENT T-10 · FICTIONAL VELLUM TRANSCRIPTION</div>
    <div class="fragment-grid">
      <blockquote>
        <header>I. Path of Footprints</header>
        <p>Not a road, but the proof a road was taken. The ground holds the shape longer than the man remembers the step. Follow only when you mean to leave the same.</p>
      </blockquote>
      <blockquote>
        <header>VII. The Storm</header>
        <p>Called ghost because the fictional cartographers left it blank. An empty circle on the chart: a mark of uncertainty, not an instruction to enter.</p>
      </blockquote>
      <blockquote>
        <header>X. Groundkeeper</header>
        <p>Bright fixed star on the edge. Not to be followed, only imagined as a bearing. The figure belongs to this invented atlas and no historical tradition.</p>
      </blockquote>
    </div>
  </section>

  <section class="two-spellings" aria-labelledby="spelling-title">
    <div class="section-label" id="spelling-title">TWO SPELLINGS · ONE FICTIONAL SOUTH</div>
    <div class="spelling-grid">
      <div><span class="spelling-label">OLD MAP NAME</span><h2>Terra Australis Incognita</h2><p>A historical geographic phrase, presented here as literary context rather than a source of cultural or scientific authority.</p></div>
      <div><span class="spelling-label">LIVING PROJECT NAME</span><h2>TerAustralis Incognita</h2><p>The project’s invented story-layer identity. The spelling difference is a creative device, not a claim of continuity or inheritance.</p></div>
    </div>
  </section>

  <aside class="boundary boundary-bottom" aria-label="Publication boundary">
    <strong>PUBLICATION BOUNDARY</strong>
    <p>This page does not represent Aboriginal or Torres Strait Islander peoples, Country, ceremony, law, ancestors, or cultural knowledge. It claims no custodianship or authority. “Sovereignty,” “stewardship,” “covenant,” and “gap” remain authorial metaphors only.</p>
  </aside>

  <footer class="atlas-footer">Non Solus — Not Alone · Southern Observatory · No technical or governance claim</footer>
</article>

<style>
  .atlas-ten {
    --atlas-accent: var(--observatory-copper, #aa91c9);
    --atlas-ink: var(--observatory-ink, #f0eadb);
    --atlas-muted: var(--observatory-muted, #a8aaa0);
    --atlas-bg: var(--observatory-bg, #080b0b);
    --atlas-surface: var(--observatory-surface-deep, #0b1010);
    --atlas-line: var(--observatory-line, rgba(232, 224, 207, .16));
    --atlas-strong-line: var(--observatory-line-strong, rgba(232, 224, 207, .34));
    max-width: 900px;
    margin: 0 auto;
    padding: 48px 24px 72px;
    color: var(--atlas-ink);
    background: var(--atlas-bg);
    font-family: var(--observatory-font-body, system-ui, sans-serif);
  }

  .atlas-header { text-align: center; padding-top: 8px; }
  .eyebrow, .chart-label, .section-label, .source-label, .spelling-label, .atlas-footer, .footer-note { font-family: var(--observatory-font-mono, ui-monospace, monospace); text-transform: uppercase; letter-spacing: .18em; }
  .eyebrow { color: var(--atlas-muted); font-size: .68rem; }
  h1, h2, h3, blockquote header { font-family: var(--observatory-font-display, Georgia, serif); font-weight: 300; }
  h1 { margin: 18px 0 10px; font-size: clamp(3rem, 8vw, 5.25rem); line-height: .95; letter-spacing: -.03em; }
  h1 em { color: var(--atlas-accent); font-style: italic; }
  .dek { margin: 0 auto; max-width: 680px; color: var(--atlas-ink); font-family: var(--observatory-font-display, Georgia, serif); font-size: 1.1rem; line-height: 1.45; }
  .subdek { margin: 10px 0 0; color: var(--atlas-muted); font-size: .88rem; letter-spacing: .05em; }

  .boundary { border-top: 1px solid var(--atlas-strong-line); border-bottom: 1px solid var(--atlas-line); }
  .boundary-top { margin-top: 42px; padding: 17px 0 16px; }
  .boundary strong { display: block; color: var(--atlas-accent); font-family: var(--observatory-font-mono, ui-monospace, monospace); font-size: .68rem; letter-spacing: .18em; }
  .boundary p { margin: 8px 0 0; color: var(--atlas-muted); font-size: .83rem; line-height: 1.55; }

  .chart-shell { margin-top: 42px; border: 1px solid var(--atlas-line); background: var(--atlas-surface); }
  .chart-heading { display: flex; align-items: center; justify-content: space-between; gap: 20px; border-bottom: 1px solid var(--atlas-line); padding: 15px 18px; }
  .chart-label { color: var(--atlas-muted); font-size: .62rem; }
  .chart-caption { margin-top: 7px; color: var(--atlas-muted); font-size: .77rem; }
  .glow-toggle { appearance: none; border: 1px solid var(--atlas-accent); background: transparent; color: var(--atlas-accent); padding: 8px 11px; font-family: var(--observatory-font-mono, ui-monospace, monospace); font-size: .62rem; letter-spacing: .13em; cursor: pointer; }
  .glow-toggle:focus-visible, .index-item:focus-visible { outline: 2px solid var(--atlas-accent); outline-offset: 4px; }
  .chart-frame { padding: 12px; }
  .star-chart { display: block; width: 100%; max-height: 530px; background: radial-gradient(circle at 55% 42%, rgba(170,145,201,.07), transparent 46%); }
  .trail-line { fill: none; stroke: url(#trail-gradient); stroke-width: 1.5; stroke-dasharray: 2 6; }
  .storm-circle { fill: none; stroke: var(--atlas-muted); stroke-width: 1; stroke-dasharray: 4 6; opacity: .55; }
  .chart-note, .roman, .star-name { fill: var(--atlas-muted); font-family: var(--observatory-font-mono, ui-monospace, monospace); letter-spacing: .12em; }
  .chart-note { font-size: 8px; opacity: .7; }
  .roman { font-size: 9px; opacity: .7; }
  .star-name { font-size: 9px; opacity: 0; transition: opacity .2s ease; }
  .star-group.active .star-name, .star-group:focus-within .star-name { opacity: 1; fill: var(--atlas-ink); }
  .hit-area { fill: transparent; cursor: pointer; }
  .star-point { fill: var(--atlas-accent); filter: drop-shadow(0 0 4px var(--atlas-accent)); }
  .glow-on .star-point { filter: drop-shadow(0 0 11px var(--atlas-accent)); }
  .star-point.ghost { fill: none; }
  .chart-footer { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; border-top: 1px solid var(--atlas-line); padding: 13px 18px; color: var(--atlas-muted); font-family: var(--observatory-font-mono, ui-monospace, monospace); font-size: .62rem; letter-spacing: .06em; }

  .position-index, .prose-layer, .two-spellings { margin-top: 54px; }
  .section-label, .source-label { color: var(--atlas-accent); font-size: .65rem; }
  .index-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 36px; margin-top: 18px; border-top: 1px solid var(--atlas-line); }
  .index-item { display: grid; grid-template-columns: 28px 1fr; grid-template-rows: auto auto; column-gap: 9px; text-align: left; border: 0; border-bottom: 1px solid var(--atlas-line); background: transparent; color: var(--atlas-ink); padding: 13px 0; cursor: pointer; }
  .index-item.active .index-name, .index-item:hover .index-name { color: var(--atlas-accent); }
  .index-id { grid-row: span 2; color: var(--atlas-accent); font-family: var(--observatory-font-mono, ui-monospace, monospace); font-size: .72rem; }
  .index-name { font-family: var(--observatory-font-display, Georgia, serif); font-size: 1.1rem; line-height: 1.1; }
  .index-note { margin-top: 4px; color: var(--atlas-muted); font-size: .73rem; line-height: 1.35; }

  .fragment-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 26px; margin-top: 18px; border-top: 1px solid var(--atlas-line); }
  blockquote { margin: 0; padding-top: 17px; }
  blockquote header { color: var(--atlas-ink); font-size: 1.35rem; }
  blockquote p { margin-top: 10px; color: var(--atlas-muted); font-size: .85rem; line-height: 1.6; }

  .spelling-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 40px; margin-top: 18px; border-top: 1px solid var(--atlas-line); }
  .spelling-grid > div { padding-top: 17px; }
  .spelling-label { color: var(--atlas-muted); font-size: .6rem; }
  .spelling-grid h2 { margin: 9px 0; color: var(--atlas-accent); font-size: 1.55rem; }
  .spelling-grid p { margin: 0; color: var(--atlas-muted); font-size: .84rem; line-height: 1.55; }
  .boundary-bottom { margin-top: 54px; padding: 19px 0 18px; }
  .atlas-footer { margin-top: 28px; color: var(--atlas-muted); font-size: .62rem; text-align: center; }

  @media (max-width: 720px) {
    .atlas-ten { padding-left: 16px; padding-right: 16px; }
    .chart-heading { align-items: flex-start; flex-direction: column; }
    .glow-toggle { align-self: flex-start; }
    .chart-footer { flex-direction: column; }
    .index-grid, .fragment-grid, .spelling-grid { grid-template-columns: 1fr; gap: 0; }
    .fragment-grid > blockquote, .spelling-grid > div { border-bottom: 1px solid var(--atlas-line); padding-bottom: 19px; }
    .fragment-grid > blockquote + blockquote, .spelling-grid > div + div { padding-top: 19px; }
    .star-name { font-size: 8px; }
  }

  @media (prefers-reduced-motion: reduce) {
    .star-name { transition: none; }
  }
</style>

{#if mounted}{/if}
