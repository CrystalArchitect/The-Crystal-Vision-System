<script>
  const doors = [
    {
      label: 'BUILT',
      title: 'What exists.',
      detail: 'Clementine · CrystalCore · ConsentGate · Starline',
      href: '/clementine',
      color: 'var(--observatory-green)',
      x: 148,
      y: 246
    },
    {
      label: 'PROPOSAL',
      title: 'What we are exploring.',
      detail: 'Southern systems · geography · recovery · future infrastructure',
      href: 'https://proposal.teraustralis.com.au/',
      color: 'var(--observatory-copper)',
      x: 400,
      y: 126
    },
    {
      label: 'CODEX',
      title: 'What we imagine.',
      detail: 'Celestial Atlas · chronicle · mythos · story maps',
      href: '/codex',
      color: 'var(--observatory-violet)',
      x: 652,
      y: 246
    }
  ];
</script>

<div class="map-shell">
  <div class="map-caption"><span>MYTHIC CARTOGRAPHY</span><span>NOT A SCIENTIFIC CATALOGUE</span></div>
  <svg viewBox="0 0 800 350" role="group" aria-labelledby="map-title map-desc">
    <title id="map-title">The Southern Observatory entry map</title>
    <desc id="map-desc">A symbolic constellation connects three destinations: Built, Proposal, and Codex.</desc>
    <defs>
      <filter id="soft-glow" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="4" result="blur" />
        <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
      </filter>
    </defs>
    <path class="orbit" d="M74 236 C190 24 612 18 726 236" />
    <path class="orbit orbit-secondary" d="M98 277 C258 90 548 92 702 277" />
    <path class="thread" d="M148 246 L400 126 L652 246" />
    <path class="thread thread-faint" d="M148 246 Q400 310 652 246" />
    {#each doors as door, index (door.label)}
      <a href={door.href} class="door" style={`--door-color:${door.color};--door-delay:${index * 1.2}s`} aria-label={`${door.label}: ${door.title}`}>
        <circle class="halo" cx={door.x} cy={door.y} r="28" />
        <circle class="star" cx={door.x} cy={door.y} r="7" />
        <circle class="pin" cx={door.x} cy={door.y} r="13" />
        <text class="door-label" x={door.x} y={door.y + 50} text-anchor="middle">{door.label}</text>
        <text class="door-title" x={door.x} y={door.y + 70} text-anchor="middle">{door.title}</text>
      </a>
    {/each}
    <text class="coordinate" x="80" y="326">SOUTHERN EDGE · 00—03</text>
    <text class="coordinate" x="720" y="326" text-anchor="end">OBSERVED FROM THE EDGE</text>
  </svg>
</div>

<style>
  .map-shell { margin-top: 48px; padding: 18px 0 0; border-top: 1px solid var(--observatory-line); }
  .map-caption { display: flex; justify-content: space-between; gap: 1rem; color: var(--observatory-muted); font: 0.66rem/1.4 var(--font-mono); letter-spacing: 0.14em; }
  svg { display: block; width: 100%; height: auto; overflow: visible; margin-top: 16px; }
  .orbit { fill: none; stroke: var(--observatory-line-strong); stroke-width: 1; stroke-dasharray: 1 8; }
  .orbit-secondary { opacity: .5; stroke-dasharray: 1 11; }
  .thread { fill: none; stroke: color-mix(in srgb, var(--observatory-ivory) 32%, transparent); stroke-width: 1.2; stroke-dasharray: 2 7; }
  .thread-faint { opacity: .4; }
  .halo { fill: var(--door-color); opacity: .1; filter: url(#soft-glow); transform-origin: center; }
  .star { fill: var(--door-color); filter: url(#soft-glow); }
  .pin { fill: none; stroke: var(--door-color); opacity: .42; stroke-width: 1; }
  .door { cursor: pointer; outline: none; }
  .door-label { fill: var(--door-color); font: 600 16px/1 var(--font-mono); letter-spacing: .14em; }
  .door-title { fill: var(--observatory-ivory); font: 400 15px/1 var(--font-display); }
  .coordinate { fill: var(--observatory-muted); font: 10px/1 var(--font-mono); letter-spacing: .12em; opacity: .75; }
  .door:hover .halo, .door:focus-visible .halo { opacity: .3; }
  .door:hover .pin, .door:focus-visible .pin { opacity: 1; stroke-width: 1.5; }
  .door:hover .door-title, .door:focus-visible .door-title { fill: var(--door-color); }
  .door:focus-visible { outline: 2px solid var(--door-color); outline-offset: 8px; }
  @media (prefers-reduced-motion: no-preference) {
    .halo { animation: map-breathe 7s ease-in-out infinite; animation-delay: var(--door-delay); }
  }
  @keyframes map-breathe { 0%, 100% { opacity: .08; } 50% { opacity: .22; } }
  @media (max-width: 680px) {
    .map-caption { flex-direction: column; gap: .35rem; }
    .door-label { font-size: 18px; }
    .door-title { font-size: 16px; }
    .coordinate { font-size: 8px; }
  }
  @media (prefers-reduced-motion: reduce) { .halo { animation: none; } }
</style>
<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
