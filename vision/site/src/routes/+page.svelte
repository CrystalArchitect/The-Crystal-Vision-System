<script>
  import ObservatoryMap from '$lib/components/ObservatoryMap.svelte';
</script>

<svelte:head>
  <title>TerAustralis Incognita — Observed from the Edge</title>
  <meta name="description" content="TerAustralis Incognita is an evidence-first archive of built software, proposed Southern systems, and a clearly labelled mythic Codex." />
  <meta property="og:title" content="TerAustralis Incognita — Observed from the Edge" />
  <meta property="og:description" content="Built systems, Southern proposals, and a vision-layer atlas, held apart by an explicit interpretation boundary." />
</svelte:head>

<section class="observatory-hero" aria-labelledby="page-title">
  <div class="hero-copy">
    <p class="eyebrow">Southern Observatory · Field note 00</p>
    <h1 id="page-title">TerAustralis<br /><em>Incognita</em></h1>
    <p class="hero-kicker">Observed from the edge.</p>
    <p class="hero-intro">An evidence-first archive of what exists, what is being explored, and what we imagine. Enter by constellation; keep the boundary visible.</p>
    <a class="enter-link" href="#entry-map"><span>Enter the atlas</span><span aria-hidden="true">↓</span></a>
  </div>
  <div class="hero-note" aria-label="Project note">
    <span class="note-mark">◆</span>
    <p>The edge is where you see furthest.</p>
    <small>— a poetic proposition, not a scientific claim</small>
  </div>
</section>

<section class="map-section" id="entry-map" aria-labelledby="map-heading">
  <div class="section-intro">
    <p class="eyebrow">The first looking</p>
    <h2 id="map-heading">Choose a field of view.</h2>
    <p>Three doors, one map. The labels are part of the evidence architecture: <strong>Built</strong> is not Vision, and Vision is not proof. The quiet index also holds a ground claim: processing, not just ore.</p>
  </div>
  <ObservatoryMap />
</section>

<section class="boundary-band" aria-labelledby="boundary-heading">
  <div>
    <p class="eyebrow">Interpretation boundary</p>
    <h2 id="boundary-heading">The map does not make the claim.</h2>
  </div>
  <p>H2 remains an analytical encoder study. Australian HPS → crystal remains a research hypothesis. The Atlas is vision-layer mythic cartography. CrystalCore remains its demonstrated software scope.</p>
  <a href="/docs/governance">Read the governance record <span aria-hidden="true">↗</span></a>
</section>

<section class="observatory-index" aria-labelledby="index-heading">
  <div class="section-intro">
    <p class="eyebrow">A quiet index</p>
    <h2 id="index-heading">From the observatory.</h2>
  </div>
  <div class="index-grid">
    <a class="index-card" href="/clementine"><span class="index-number">01</span><strong>Working software</strong><span>Clementine, ConsentGate, and the CrystalCore lineage.</span></a>
    <a class="index-card" href="https://proposal.teraustralis.com.au/"><span class="index-number">02</span><strong>Southern systems proposal</strong><span>Documents under exploration. Berth not selected.</span></a>
    <a class="index-card" href="/atlas"><span class="index-number">03</span><strong>Celestial Atlas</strong><span>A natural-history / mythic record. Vision only.</span></a>
    <a class="index-card" href="/minerals"><span class="index-number">04</span><strong>Processing, not just ore</strong><span>Mine-to-magnet is a plant, not a shipping schedule. Built claim, not Vision.</span></a>
    <a class="index-card" href="/bio"><span class="index-number">05</span><strong>Crystal Arena Turner</strong><span>Steward of this archive. A person, not the map.</span></a>
    <a class="index-card" href="/brief"><span class="index-number">06</span><strong>Named Pathway Brief</strong><span>One page, one named Australian mineral, one path to launch. Built product, not Vision.</span></a>
    <a class="index-card" href="/earth-twin"><span class="index-number">07</span><strong>Earth twin</strong><span>Return fuel is CO₂ and ice. The rust is the factory floor — already here. Built claim, not Vision.</span></a>
    <a class="index-card" href="/the-licence"><span class="index-number">08</span><strong>The licence</strong><span>Australian talent hit criticality in the US. Civil nuclear power plants are still banned here.</span></a>
    <a class="index-card" href="/wavelength"><span class="index-number">09</span><strong>Wavelength</strong><span>Wavelength is an address. Telecom shares a strand; spectral combining shares an aperture. Built claim, not Vision.</span></a>
    <a class="index-card" href="/after-the-radar"><span class="index-number">10</span><strong>After the radar</strong><span>Australia’s industrial bargain with AUKUS — DARC to Aerotropolis hands. Strategic opinion, available surface.</span></a>
    <a class="index-card" href="/bci-aerotropolis"><span class="index-number">11</span><strong>BCI + robotics pathway</strong><span>Named Pathway Brief for Aerotropolis dual-rail BCI/robotics. Proposal beside Built neighbours.</span></a>
    <a
      class="index-card"
      href="https://crystalarchitect.github.io/teraustralis-incognita-canon-gallery/"
      target="_blank"
      rel="noopener noreferrer"
    ><span class="index-number">12</span><strong>Mythic Canon</strong><span>16-card set reveal — Origin, Ancients, Oathbearers. Vision only. Separate gallery.</span></a>
  </div>
</section>

<style>
  .observatory-hero { min-height: min(760px, calc(100vh - 100px)); display: grid; grid-template-columns: minmax(0, 1fr) minmax(220px, .42fr); align-items: end; gap: 4rem; padding: clamp(5rem, 15vh, 10rem) 0 6rem; position: relative; }
  .observatory-hero::after { content: ''; position: absolute; inset: 8% -18% 0 36%; background: radial-gradient(circle at 50% 48%, rgba(170, 145, 201, .13), transparent 38%), radial-gradient(circle at 35% 45%, rgba(112, 177, 171, .1), transparent 30%); pointer-events: none; z-index: -1; }
  .hero-copy, .hero-note { position: relative; z-index: 1; }
  .hero-copy { max-width: 760px; }
  h1 { font-size: clamp(4rem, 12vw, 9.5rem); line-height: .88; letter-spacing: -.06em; font-weight: 500; color: var(--observatory-ivory); }
  h1 em { color: var(--observatory-copper); font-style: italic; }
  .hero-kicker { color: var(--observatory-copper); font: .78rem/1 var(--font-mono); letter-spacing: .24em; text-transform: uppercase; margin-top: 2.2rem; }
  .hero-intro { max-width: 40ch; color: var(--observatory-muted); font-size: 1.08rem; line-height: 1.65; margin-top: 1.35rem; }
  .enter-link { display: inline-flex; align-items: center; gap: 2.2rem; margin-top: 2.6rem; padding: .8rem 0; color: var(--observatory-ivory); border-bottom: 1px solid var(--observatory-copper); font: .75rem/1 var(--font-mono); letter-spacing: .16em; text-transform: uppercase; }
  .enter-link:hover { color: var(--observatory-copper); text-decoration: none; }
  .hero-note { align-self: center; max-width: 18rem; padding: 1.5rem 0 1.5rem 1.4rem; border-left: 1px solid var(--observatory-copper); color: var(--observatory-ivory); }
  .hero-note .note-mark { display: block; color: var(--observatory-copper); font-size: 1.2rem; margin-bottom: 1.5rem; }
  .hero-note p { font: italic 1.35rem/1.25 var(--font-display); }
  .hero-note small { display: block; color: var(--observatory-muted); font: .68rem/1.45 var(--font-mono); margin-top: 1.2rem; }
  .map-section, .observatory-index { padding: 5.5rem 0; border-top: 1px solid var(--observatory-line); }
  .section-intro { max-width: 44rem; }
  h2 { color: var(--observatory-ivory); font: 500 clamp(2rem, 5vw, 4rem)/1.05 var(--font-display); letter-spacing: -.035em; }
  .section-intro > p:last-child { color: var(--observatory-muted); margin-top: 1rem; max-width: 44rem; }
  .section-intro strong { color: var(--observatory-ivory); font-weight: 500; }
  .boundary-band { display: grid; grid-template-columns: 1fr 1fr auto; gap: 3rem; align-items: end; padding: 3rem 0; border-top: 1px solid var(--observatory-line); border-bottom: 1px solid var(--observatory-line); }
  .boundary-band h2 { font-size: clamp(1.8rem, 3vw, 3rem); }
  .boundary-band > p { max-width: 34rem; color: var(--observatory-muted); font-size: .96rem; }
  .boundary-band > a { white-space: nowrap; color: var(--observatory-copper); font: .7rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
  .index-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--observatory-line); margin-top: 2.5rem; border: 1px solid var(--observatory-line); }
  .index-card { display: flex; flex-direction: column; min-height: 210px; padding: 1.6rem; background: rgba(14, 20, 21, .74); color: var(--observatory-ivory); }
  .index-card:hover { background: rgba(32, 43, 41, .86); text-decoration: none; }
  .index-number { color: var(--observatory-copper); font: .7rem/1 var(--font-mono); letter-spacing: .1em; }
  .index-card strong { margin-top: 3.5rem; font: 500 1.45rem/1.1 var(--font-display); }
  .index-card span:last-child { color: var(--observatory-muted); font-size: .86rem; line-height: 1.5; margin-top: .7rem; }
  @media (min-width: 1100px) {
    .index-grid { grid-template-columns: repeat(3, 1fr); }
  }
  @media (max-width: 760px) {
    .observatory-hero { min-height: auto; grid-template-columns: 1fr; gap: 3rem; padding-top: 5rem; }
    .hero-note { align-self: auto; max-width: 20rem; }
    .boundary-band { grid-template-columns: 1fr; gap: 1.25rem; }
    .index-grid { grid-template-columns: 1fr; }
    .index-card { min-height: 170px; }
    .index-card strong { margin-top: 2.2rem; }
  }
</style>
<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
