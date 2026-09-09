<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  // Seven lights, seven real doors — the node data is the single source
  // of truth in $lib/data/constellation.js; this component stays purely
  // presentational.
  import {
    constellationNodes as nodes,
    constellationLines as lines
  } from '$lib/data/constellation.js';
</script>

<div class="constellation">
  <!-- No role="img" here: the map contains real links, and an image
       role would mark them presentational (axe: nested-interactive). -->
  <svg viewBox="0 0 800 400" aria-labelledby="constellation-title">
    <title id="constellation-title">
      The TerAustralis constellation — seven nodes, each a page of this site
    </title>
    {#each lines as [a, b], i (i)}
      <line
        x1={nodes[a].x} y1={nodes[a].y}
        x2={nodes[b].x} y2={nodes[b].y}
        class="thread"
      />
    {/each}
    {#each nodes as n, i (n.href)}
      <a href={n.href} aria-label="{n.label} — {n.sub}">
        <circle
          class="halo" cx={n.x} cy={n.y} r={n.r * 2.6}
          style="--c:{n.color}; --delay:{i * 1.1}s"
        />
        <circle
          class="star" cx={n.x} cy={n.y} r={n.r}
          style="--c:{n.color}; --delay:{i * 1.1}s"
        />
        <text
          class="label"
          x={n.x} y={n.y + n.r * 2.6 + 18}
          text-anchor="middle"
        >{n.label}</text>
        <text
          class="sublabel"
          x={n.x} y={n.y + n.r * 2.6 + 36}
          text-anchor="middle"
        >{n.sub}</text>
      </a>
    {/each}
  </svg>
</div>

<style>
  .constellation {
    margin-top: 38px;
  }
  svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }
  .thread {
    stroke: var(--border, var(--line));
    stroke-width: 1;
  }
  .halo {
    fill: var(--c, var(--gold));
    opacity: 0.1;
  }
  .star {
    fill: var(--c, var(--gold));
    opacity: 0.9;
  }
  .label {
    fill: var(--text-primary, var(--ink));
    font-family: var(--font-display);
    font-size: var(--text-body, 17px);
    font-weight: var(--weight-semibold, 600);
  }
  .sublabel {
    fill: var(--muted);
    font-family: var(--font-body);
    font-size: 12.5px;
    letter-spacing: 0.06em;
  }
  a {
    cursor: pointer;
  }
  a:hover .star,
  a:focus-visible .star {
    opacity: 1;
  }
  a:hover .halo,
  a:focus-visible .halo {
    opacity: 0.28;
  }
  a:hover .label {
    fill: var(--c, var(--gold));
  }
  a:focus-visible {
    outline: var(--focus-ring, 2px solid var(--blue));
    outline-offset: 4px;
    border-radius: 4px;
  }
  /* restrained constellation motion: a slow, staggered breath per star —
     and perfect stillness for anyone who asks for it */
  @media (prefers-reduced-motion: no-preference) {
    .halo {
      animation: breathe 6.5s ease-in-out infinite;
      animation-delay: var(--delay, 0s);
    }
    .star {
      animation: glimmer 6.5s ease-in-out infinite;
      animation-delay: var(--delay, 0s);
    }
  }
  @keyframes breathe {
    0%, 100% { opacity: 0.08; }
    50% { opacity: 0.2; }
  }
  @keyframes glimmer {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
  }
  @media (max-width: 720px) {
    .label { font-size: 21px; }
    .sublabel { font-size: 15px; }
  }
</style>
