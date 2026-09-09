<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<!--
  The Crystal motifs, drawn in pure inline SVG (no external assets):
  the Seed of Life (sacred geometry) and the vortex wheel (the 1-2-4-8-7-5
  doubling cycle + the 3-6-9 triangle). Both are Vision-layer symbols — the
  caption keeps them honest.
-->
<section class="motifs" aria-labelledby="motifs-title">
  <h2 id="motifs-title">The Motifs</h2>

  <div class="motif-grid">
    <figure>
      <svg viewBox="0 0 200 200" role="img" aria-label="Seed of Life — seven overlapping circles" class="spin">
        <g fill="none" stroke="var(--gold)" stroke-width="1.2">
          <circle cx="100" cy="100" r="60" opacity="0.25" />
          <circle cx="100" cy="100" r="30" />
          <circle cx="130" cy="100" r="30" />
          <circle cx="115" cy="125.98" r="30" />
          <circle cx="85"  cy="125.98" r="30" />
          <circle cx="70"  cy="100" r="30" />
          <circle cx="85"  cy="74.02" r="30" />
          <circle cx="115" cy="74.02" r="30" />
        </g>
      </svg>
      <figcaption>Seed of Life — seven circles, seven paths</figcaption>
    </figure>

    <figure>
      <svg viewBox="0 0 200 200" role="img" aria-label="Vortex wheel — the 1 2 4 8 7 5 doubling cycle and the 3 6 9 triangle">
        <circle cx="100" cy="100" r="70" fill="none" stroke="var(--purple)" stroke-width="1" opacity="0.3" />
        <!-- doubling cycle 1 -> 2 -> 4 -> 8 -> 7 -> 5 -> 1 -->
        <path d="M145,46.4 L168.9,87.8 L123.9,165.8 L55,46.4 L31,87.8 L76.1,165.8 Z"
              fill="none" stroke="var(--gold)" stroke-width="1.6" stroke-linejoin="round" />
        <!-- the 3 - 6 - 9 triangle -->
        <path d="M160.6,135 L39.4,135 L100,30 Z"
              fill="none" stroke="var(--green)" stroke-width="1.4" stroke-linejoin="round" opacity="0.9" />
        <g class="nums" font-size="11" text-anchor="middle" dominant-baseline="middle" fill="var(--ink)">
          <text x="145"   y="42">1</text>
          <text x="176"   y="88">2</text>
          <text x="168"   y="135">3</text>
          <text x="124"   y="174">4</text>
          <text x="76.1"  y="174">5</text>
          <text x="32"    y="135">6</text>
          <text x="23"    y="88">7</text>
          <text x="55"    y="42">8</text>
          <text x="100"   y="24">9</text>
        </g>
      </svg>
      <figcaption>The vortex wheel — <span class="mono">1·2·4·8·7·5</span>, and <span class="mono">3·6·9</span></figcaption>
    </figure>
  </div>

  <p class="note">
    Both are <strong>symbols</strong>, not measurements. The wheel is real
    arithmetic — digital roots mod&nbsp;9, so doubling truly cycles 1‑2‑4‑8‑7‑5 —
    but "vortex mathematics" as a theory of the universe is numerology, not
    physics. Draw with them; don't cite them.
  </p>
</section>

<style>
  .motifs {
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 1.5rem 1rem;
    text-align: center;
  }
  .motifs h2 {
    font-family: var(--font-display);
    font-weight: 600;
    margin-bottom: 2rem;
  }
  .motif-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
    align-items: flex-start;
  }
  figure {
    margin: 0;
    flex: 1 1 240px;
    max-width: 320px;
  }
  svg {
    width: 100%;
    height: auto;
    max-width: 260px;
    filter: drop-shadow(0 0 14px rgba(167, 139, 250, 0.18));
  }
  figcaption {
    margin-top: 0.85rem;
    font-size: 0.9rem;
    opacity: 0.75;
  }
  .mono {
    font-family: var(--font-mono);
    color: var(--gold);
  }
  .note {
    max-width: 620px;
    margin: 2.25rem auto 0;
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.7;
  }
  .spin {
    animation: turn 90s linear infinite;
    transform-origin: 50% 50%;
  }
  @keyframes turn {
    to { transform: rotate(360deg); }
  }
  @media (prefers-reduced-motion: reduce) {
    .spin { animation: none; }
  }
</style>
