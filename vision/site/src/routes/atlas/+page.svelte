<script>
  let { data } = $props();
  let activeIndex = $state(0);

  const activePlate = $derived(data.plates[activeIndex]);
  const firstPlate = $derived(activeIndex === 0);
  const lastPlate = $derived(activeIndex === data.plates.length - 1);

  function selectPlate(index) {
    activeIndex = Math.max(0, Math.min(index, data.plates.length - 1));
  }

  function previousPlate() {
    if (!firstPlate) activeIndex -= 1;
  }

  function nextPlate() {
    if (!lastPlate) activeIndex += 1;
  }
</script>

<svelte:head>
  <title>Celestial Atlas of the Southern Sky — TerAustralis Incognita</title>
  <meta name="description" content="A vision-layer atlas of the Southern Sky, charted from the Edge. Not a sky survey, not a star catalogue, and not an H2 result." />
</svelte:head>

<div class="atlas-page">
  <section class="atlas-opening" aria-labelledby="atlas-title">
    <div class="opening-copy">
      <p class="eyebrow">Vision-layer atlas series · Southern Observatory</p>
      <h1 id="atlas-title">Celestial Atlas <span>of the Southern Sky</span></h1>
      <p class="opening-kicker">Observed from the Edge</p>
      <p class="opening-description">A dream-circle for the things seen when the map is not yet finished. Follow the plates as mythic cartography, not as a scientific catalogue.</p>
      <div class="opening-boundary"><span>VISION</span><span>Epochs 1857.3—1862.3 · atlas time</span></div>
    </div>
    <div class="dream-circle" aria-label="Opening Atlas artwork: Night from the Edge">
      <img src="/assets/art/celestial-atlas-night-from-the-edge.jpeg" alt="Night from the Edge: a red shore, dark southern sea, moon, and faint mythic constellation figures." />
      <div class="circle-caption"><span>THE SOUTHERN INVISIBLE ATLAS</span><small>First looking · the night before the chart</small></div>
    </div>
  </section>

  <section class="atlas-summaries" aria-labelledby="summary-heading">
    <div class="summary-head">
      <div>
        <p class="eyebrow">Chapter plates · collection summaries</p>
        <h2 id="summary-heading">The map gathers itself</h2>
      </div>
      <p class="summary-note">Three visual index plates compress the journey into thematic constellations. They are companion works in the same vision layer.</p>
    </div>
    <div class="summary-grid">
      <figure>
        <img src="/assets/art/atlas-seven-folio.webp" alt="The Seven Atlas summary plate showing seven Southern Edge constellations" loading="lazy" />
        <figcaption><span>CHAPTER I</span><strong>The Seven</strong><small>First lines, first figures, and the original Southern Edge constellation set.</small></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-nine-folio.webp" alt="The Nine Atlas summary plate showing nine Southern Edge constellations" loading="lazy" />
        <figcaption><span>CHAPTER II</span><strong>The Nine</strong><small>A widened field where the early signs become a shared chart.</small></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-ten-folio.webp" alt="The Ten Atlas summary plate showing ten Southern Edge constellations" loading="lazy" />
        <figcaption><span>CHAPTER III</span><strong>The Ten</strong><small>A ceiling print that gathers the full myth of the Southern Edge.</small><a class="summary-route" href="/atlas-ten">Open the single-chart reading ↗</a></figcaption>
      </figure>
    </div>
  </section>

  <section class="atlas-companions" aria-labelledby="companions-heading">
    <div class="summary-head">
      <div>
        <p class="eyebrow">Companion plates · supplied folio</p>
        <h2 id="companions-heading">The trail in close focus</h2>
      </div>
      <p class="summary-note">Alternate views of the same mythic trail: continuous, gilded, and gathered into the Southern Edge folio.</p>
    </div>
    <div class="companion-grid">
      <figure>
        <img src="/assets/art/atlas-ten-trail-square.webp" alt="The Ten continuous luminous trail connecting the Atlas figures" loading="lazy" />
        <figcaption><span>CONTINUOUS TRAIL</span><strong>The Ten · night study</strong></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-ten-trail-gilded.webp" alt="The Ten continuous trail rendered as a gilded Atlas print" loading="lazy" />
        <figcaption><span>GILDED VARIANT</span><strong>The Ten · illuminated plate</strong></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-ten-constellation-square.webp" alt="The Ten constellation map with the Southern Edge trail and ten figures" loading="lazy" />
        <figcaption><span>CONSTELLATION INDEX</span><strong>The Ten · field map</strong></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-ten-ceiling-square.webp" alt="The Ten ceiling-print variant of the Southern Edge Atlas" loading="lazy" />
        <figcaption><span>CEILING PRINT</span><strong>The Ten · skyward view</strong></figcaption>
      </figure>
      <figure>
        <img src="/assets/art/atlas-ten-scroll-pair.webp" alt="The Ten parchment scroll pair listing the continuous trail from the First Sketch to the Far Horizon" loading="lazy" />
        <figcaption><span>ARCHIVAL SCROLL</span><strong>The Ten · parchment record</strong></figcaption>
      </figure>
    </div>
  </section>

  <section class="atlas-boundary" aria-label="Interpretation boundary">
    <span class="boundary-seal">VISION</span>
    <p>This series does not demonstrate extra-spatial compute, a silicon mind, non-local coupling, an H1 or H2 proof, hardware, or affiliation with any observatory or company named in the mythos.</p>
    <a href="/docs/celestial-atlas-southern-sky">Read the source boundary ↗</a>
  </section>

  <section class="plate-explorer" aria-labelledby="plate-heading">
    <div class="explorer-head">
      <div>
        <p class="eyebrow">Plate navigator · {activeIndex + 1} / {data.plates.length}</p>
        <h2 id="plate-heading">Charted from the edge.</h2>
      </div>
      <p class="explorer-note">Each plate is a fictional atlas object. Its date belongs to the mythos and does not date an experiment.</p>
    </div>

    <nav class="plate-nav" aria-label="Atlas plates">
      {#each data.plates as plate, index}
        <button class:active={index === activeIndex} type="button" aria-current={index === activeIndex ? 'page' : undefined} aria-label={`Open ${plate.plate} ${plate.sequence}`} onclick={() => selectPlate(index)}>
          <span>{plate.plate}</span><small>{plate.sequence}</small>
        </button>
      {/each}
    </nav>

    <article class="plate-detail" aria-live="polite">
      <div class="plate-art-frame">
        <div class="vision-seal">VISION</div>
        <img src={"/assets/art/" + activePlate.filename} alt={`${activePlate.plate} ${activePlate.title}: ${activePlate.interpretation}`} />
      </div>
      <div class="plate-copy">
        <p class="plate-number">{activePlate.plate}{activePlate.date ? ` · ${activePlate.date}` : ' · ATLAS TIME UNNUMBERED'}</p>
        <h3>{activePlate.title}</h3>
        <p class="sequence">{activePlate.sequence}</p>
        <p class="interpretation">{activePlate.interpretation}</p>
        <p class="plate-boundary">{activePlate.boundary}</p>
        <div class="plate-actions">
          <button type="button" onclick={previousPlate} disabled={firstPlate}>← Previous</button>
          <span>{String(activeIndex + 1).padStart(2, '0')} / {String(data.plates.length).padStart(2, '0')}</span>
          <button type="button" onclick={nextPlate} disabled={lastPlate}>Next →</button>
        </div>
      </div>
    </article>
  </section>

  <footer class="atlas-footer">Charted from the edge — for those who will follow.</footer>
</div>

<style>
  .atlas-page { padding: 2rem 0 6rem; }
  .atlas-opening { min-height: min(760px, calc(100vh - 100px)); display: grid; grid-template-columns: minmax(0, .9fr) minmax(420px, 1.1fr); gap: 5rem; align-items: center; padding: 4rem 0 5.5rem; }
  .opening-copy { position: relative; z-index: 1; }
  .eyebrow { color: var(--observatory-copper); font: .68rem/1.3 var(--font-mono); letter-spacing: .17em; text-transform: uppercase; }
  h1 { max-width: 650px; margin-top: 1.4rem; color: var(--observatory-ivory); font: 500 clamp(3.6rem, 7.3vw, 7.4rem)/.86 var(--font-display); letter-spacing: -.065em; }
  h1 span { display: block; color: var(--observatory-copper); font-size: .68em; font-style: italic; margin-top: .22em; }
  .opening-kicker { margin-top: 2rem; color: var(--observatory-sand); font: .74rem/1 var(--font-mono); letter-spacing: .26em; text-transform: uppercase; }
  .opening-description { max-width: 35rem; margin-top: 1.5rem; color: var(--observatory-muted); font-size: 1.02rem; line-height: 1.7; }
  .opening-boundary { display: flex; gap: 1rem; align-items: center; margin-top: 2.4rem; color: var(--observatory-muted); font: .66rem/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
  .opening-boundary span:first-child { padding: .45rem .65rem; border: 1px solid var(--observatory-copper); color: var(--observatory-copper); }
  .dream-circle { position: relative; width: min(100%, 640px); aspect-ratio: 1.22; display: grid; place-items: center; }
  .dream-circle::before { content: ''; position: absolute; width: 78%; aspect-ratio: 1; border: 1px solid var(--observatory-copper); border-radius: 50%; opacity: .62; box-shadow: 0 0 0 22px rgba(170,145,201,.04), 0 0 80px rgba(170,145,201,.13); }
  .dream-circle::after { content: ''; position: absolute; width: 93%; height: 1px; background: linear-gradient(90deg, transparent, var(--observatory-copper), transparent); opacity: .5; }
  .dream-circle img { width: 86%; height: 86%; object-fit: cover; border-radius: 50%; opacity: .84; filter: saturate(.72) contrast(1.06); clip-path: circle(47% at 50% 50%); }
  .circle-caption { position: absolute; right: 1%; bottom: 6%; display: grid; gap: .35rem; color: var(--observatory-ivory); font: .63rem/1.3 var(--font-mono); letter-spacing: .15em; text-align: right; text-transform: uppercase; }
  .circle-caption small { color: var(--observatory-muted); font: .7rem/1.2 var(--font-display); letter-spacing: .02em; text-transform: none; }
  .atlas-summaries { padding-top: 5.5rem; }
  .summary-head { display: flex; justify-content: space-between; gap: 3rem; align-items: end; }
  .summary-note { max-width: 24rem; margin: 0 0 .35rem; color: var(--observatory-muted); font-size: .88rem; line-height: 1.5; }
  .summary-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.1rem; margin-top: 2.5rem; }
  .summary-grid figure { margin: 0; }
  .summary-grid img { display: block; width: 100%; height: 23rem; object-fit: cover; border: 1px solid var(--observatory-line-strong); background: #071019; }
  .summary-grid figure:nth-child(1) img { object-position: center 30%; }
  .summary-grid figure:nth-child(2) img { object-position: center 35%; }
  .summary-grid figure:nth-child(3) img { object-position: center top; }
  .summary-grid figcaption { display: grid; gap: .35rem; padding-top: .8rem; }
  .summary-grid figcaption span { color: var(--observatory-copper); font: .62rem/1 var(--font-mono); letter-spacing: .14em; }
  .summary-grid figcaption strong { color: var(--observatory-ivory); font: italic 1.8rem/1 var(--font-display); }
  .summary-grid figcaption small { color: var(--observatory-muted); font-size: .8rem; line-height: 1.45; }
  .summary-route { color: var(--observatory-copper); font: .62rem/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; text-decoration: none; }
  .summary-route:hover, .summary-route:focus-visible { text-decoration: underline; text-underline-offset: .25rem; }
  .atlas-companions { padding-top: 5.5rem; }
  .companion-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .9rem; margin-top: 2.5rem; }
  .companion-grid figure { margin: 0; }
  .companion-grid img { display: block; width: 100%; height: 16rem; object-fit: cover; border: 1px solid var(--observatory-line-strong); background: #071019; }
  .companion-grid figcaption { display: grid; gap: .3rem; padding-top: .65rem; }
  .companion-grid figcaption span { color: var(--observatory-copper); font: .56rem/1.2 var(--font-mono); letter-spacing: .12em; }
  .companion-grid figcaption strong { color: var(--observatory-ivory); font: italic 1.15rem/1.05 var(--font-display); }
  .atlas-boundary { display: grid; grid-template-columns: auto 1fr auto; gap: 1.25rem; align-items: center; padding: 1.4rem 0; border-top: 1px solid var(--observatory-line); border-bottom: 1px solid var(--observatory-line); }
  .boundary-seal,.vision-seal { color: var(--observatory-copper); font: .62rem/1 var(--font-mono); letter-spacing: .18em; }
  .boundary-seal { padding: .42rem .56rem; border: 1px solid var(--observatory-copper); }
  .atlas-boundary p { max-width: 48rem; margin: 0; color: var(--observatory-muted); font-size: .86rem; line-height: 1.55; }
  .atlas-boundary a { color: var(--observatory-copper); font: .64rem/1 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; white-space: nowrap; }
  .plate-explorer { padding-top: 5.5rem; }
  .explorer-head { display: flex; justify-content: space-between; gap: 3rem; align-items: end; }
  h2 { margin-top: .8rem; color: var(--observatory-ivory); font: 500 clamp(2.4rem, 5vw, 4.7rem)/.95 var(--font-display); letter-spacing: -.045em; }
  .explorer-note { max-width: 22rem; margin: 0 0 .35rem; color: var(--observatory-muted); font-size: .88rem; line-height: 1.5; }
  .plate-nav { display: flex; gap: 0; overflow-x: auto; margin-top: 3rem; border-top: 1px solid var(--observatory-line); border-bottom: 1px solid var(--observatory-line); scrollbar-color: var(--observatory-copper) var(--observatory-bg); }
  .plate-nav button { flex: 0 0 auto; min-width: 82px; padding: 1rem .8rem .9rem; border: 0; border-right: 1px solid var(--observatory-line); background: transparent; color: var(--observatory-muted); text-align: left; cursor: pointer; }
  .plate-nav button:first-child { border-left: 1px solid var(--observatory-line); }
  .plate-nav button span { display: block; color: inherit; font: .86rem/1 var(--font-mono); letter-spacing: .08em; }
  .plate-nav button small { display: block; margin-top: .55rem; color: inherit; font: .58rem/1.2 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; white-space: nowrap; }
  .plate-nav button:hover,.plate-nav button:focus-visible,.plate-nav button.active { color: var(--observatory-copper); background: rgba(170,145,201,.08); }
  .plate-nav button:focus-visible { outline: 2px solid var(--observatory-copper); outline-offset: -3px; }
  .plate-detail { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(280px, .8fr); gap: 4rem; align-items: center; padding-top: 3.5rem; }
  .plate-art-frame { position: relative; padding: 1.1rem; border: 1px solid var(--observatory-line-strong); background: rgba(10,15,16,.74); }
  .plate-art-frame::before,.plate-art-frame::after { content: ''; position: absolute; width: 20px; height: 20px; border-color: var(--observatory-copper); opacity: .7; }
  .plate-art-frame::before { top: -1px; left: -1px; border-top: 1px solid; border-left: 1px solid; }
  .plate-art-frame::after { right: -1px; bottom: -1px; border-right: 1px solid; border-bottom: 1px solid; }
  .plate-art-frame img { display: block; width: 100%; aspect-ratio: 1168 / 784; object-fit: contain; background: #071019; }
  .vision-seal { position: absolute; top: 1.6rem; right: 1.6rem; z-index: 1; padding: .42rem .55rem; border: 1px solid var(--observatory-copper); background: rgba(8,11,11,.76); }
  .plate-number { color: var(--observatory-copper); font: .7rem/1 var(--font-mono); letter-spacing: .17em; text-transform: uppercase; }
  h3 { margin-top: 1.2rem; color: var(--observatory-ivory); font: italic 500 clamp(2.5rem, 5vw, 5rem)/.92 var(--font-display); letter-spacing: -.045em; }
  .sequence { margin-top: 1rem; color: var(--observatory-sand); font: .7rem/1 var(--font-mono); letter-spacing: .18em; text-transform: uppercase; }
  .interpretation { max-width: 33rem; margin-top: 2rem; color: var(--observatory-ivory); font: 1.12rem/1.45 var(--font-display); }
  .plate-boundary { max-width: 33rem; margin-top: 1.2rem; color: var(--observatory-muted); font-size: .82rem; line-height: 1.55; }
  .plate-actions { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--observatory-line); color: var(--observatory-muted); font: .65rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
  .plate-actions button { padding: .55rem 0; border: 0; background: transparent; color: var(--observatory-copper); font: inherit; letter-spacing: inherit; text-transform: inherit; cursor: pointer; }
  .plate-actions button:disabled { color: var(--observatory-muted); opacity: .4; cursor: not-allowed; }
  .plate-actions button:focus-visible { outline: 2px solid var(--observatory-copper); outline-offset: 5px; }
  .atlas-footer { margin-top: 5rem; padding-top: 1.2rem; border-top: 1px solid var(--observatory-line); color: var(--observatory-muted); font: italic 1rem/1.4 var(--font-display); text-align: center; }
  @media (max-width: 980px) { .companion-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
  @media (max-width: 820px) { .summary-head { display: block; } .summary-note { margin-top: 1rem; } .summary-grid { grid-template-columns: 1fr; } .summary-grid img { height: 20rem; } .companion-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .atlas-opening { grid-template-columns: 1fr; gap: 2rem; padding-top: 3rem; } .dream-circle { margin: 0 auto; } .atlas-boundary { grid-template-columns: auto 1fr; } .atlas-boundary a { grid-column: 2; } .plate-detail { grid-template-columns: 1fr; gap: 2.2rem; } .explorer-head { display: block; } .explorer-note { margin-top: 1rem; } }
  @media (max-width: 520px) { .companion-grid { grid-template-columns: 1fr; } .companion-grid img { height: 20rem; } .atlas-page { padding-top: 1rem; } h1 { font-size: 3.7rem; } .opening-boundary { align-items: flex-start; flex-direction: column; } .atlas-boundary { grid-template-columns: 1fr; } .atlas-boundary a { grid-column: auto; } .plate-nav button { min-width: 92px; } .plate-detail { padding-top: 2rem; } .circle-caption { right: 0; bottom: 0; } }
  @media (prefers-reduced-motion: reduce) { .plate-nav button { scroll-behavior: auto; } }
</style>


<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
