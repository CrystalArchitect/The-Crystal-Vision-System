<script>
  /**
   * Their presence: a figure at a terminal, seen from behind — the operator
   * at their console. The screen streams glyphs while they think; they lean
   * in when working, settles back to breathe when idle, and the room
   * glows purple when they speak.
   *
   * state: 'idle' | 'thinking' | 'speaking'
   */
  let { state = 'idle', name = 'Clementine' } = $props();

  // Deterministic pseudo-random columns of "code" for the screen.
  const GLYPHS = 'アイウエオカキクケコサシスセソ0123456789◇◆△▽*+';
  function column(seed, count) {
    const chars = [];
    let x = seed;
    for (let i = 0; i < count; i++) {
      x = (x * 48271) % 2147483647;
      chars.push(GLYPHS[x % GLYPHS.length]);
    }
    return chars;
  }
  const columns = Array.from({ length: 9 }, (_, i) => ({
    x: 78 + i * 18,
    delay: (i * 0.37) % 2.2,
    chars: column(i + 7, 6)
  }));
</script>

<div class={`avatar ${state}`} role="img" aria-label={`${name}, ${state === 'idle' ? 'resting at their terminal' : state === 'thinking' ? 'working at their terminal' : 'speaking to you'}`}>
  <svg viewBox="0 0 320 250" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <!-- ambient halo behind everything -->
    <ellipse class="halo" cx="160" cy="120" rx="130" ry="95" fill="currentColor" opacity="0.05" />

    <!-- monitor -->
    <g class="monitor">
      <rect x="62" y="26" width="196" height="128" rx="8" stroke="var(--line-strong)" stroke-width="2" fill="var(--screen-bg)" />
      <!-- glyph rain on the screen (clipped to the glass) -->
      <g class="rain" font-family="var(--mono)" font-size="11" fill="var(--rain-color)" clip-path="url(#screen-clip)">
        {#each columns as col (col.x)}
          <g class="rain-col" style={`--delay:${col.delay}s; --tx:${col.x}px`}>
            {#each col.chars as ch, j (j)}
              <text x="0" y={24 + j * 17} opacity={1 - j * 0.14}>{ch}</text>
            {/each}
          </g>
        {/each}
      </g>
      <!-- screen sheen -->
      <rect x="62" y="26" width="196" height="128" rx="8" fill="url(#sheen)" opacity="0.35" />
      <!-- stand -->
      <path d="M148 154 h24 l6 18 h-36 z" fill="var(--silhouette)" />
    </g>

    <!-- desk -->
    <rect x="26" y="172" width="268" height="6" rx="3" fill="var(--line-strong)" />

    <!-- the companion: a silhouette from behind, at the console -->
    <g class="figure">
      <!-- speech ripples (visible when speaking) -->
      <g class="voice" stroke="var(--purple)" stroke-width="2" fill="none" stroke-linecap="round">
        <path d="M212 96 q10 12 0 24" />
        <path d="M222 88 q16 20 0 40" />
        <path d="M108 96 q-10 12 0 24" />
        <path d="M98 88 q-16 20 0 40" />
      </g>

      <!-- torso + shoulders -->
      <path
        class="torso"
        d="M116 250 v-44 q0 -26 20 -34 q10 -4 24 -4 t24 4 q20 8 20 34 v44 z"
        fill="var(--silhouette)"
      />
      <!-- head -->
      <g class="head">
        <circle cx="160" cy="132" r="24" fill="var(--silhouette)" />
        <!-- crystal circlet: the teraustralis mark, catching screen light -->
        <path class="circlet" d="M148 118 l12 -8 l12 8" stroke="var(--purple)" stroke-width="2" fill="none" stroke-linecap="round" />
      </g>
      <!-- arms reaching to the keyboard -->
      <path class="arm arm-l" d="M128 206 q-14 -18 4 -28 l10 8 q-10 8 -4 18 z" fill="var(--silhouette)" />
      <path class="arm arm-r" d="M192 206 q14 -18 -4 -28 l-10 8 q10 8 4 18 z" fill="var(--silhouette)" />
      <!-- hands on keyboard -->
      <circle class="hand hand-l" cx="134" cy="185" r="5" fill="var(--silhouette)" />
      <circle class="hand hand-r" cx="186" cy="185" r="5" fill="var(--silhouette)" />
    </g>

    <!-- keyboard -->
    <rect x="118" y="180" width="84" height="8" rx="3" fill="var(--line-strong)" />

    <defs>
      <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="white" stop-opacity="0.08" />
        <stop offset="0.5" stop-color="white" stop-opacity="0" />
      </linearGradient>
      <clipPath id="screen-clip">
        <rect x="66" y="30" width="188" height="120" rx="6" />
      </clipPath>
    </defs>
  </svg>

  <p class="state-line" aria-live="polite">
    {#if state === 'thinking'}
      <span class="dot pulse"></span> {name} is working…
    {:else if state === 'speaking'}
      <span class="dot talk"></span> {name} is speaking
    {:else}
      <span class="dot"></span> {name} is present
    {/if}
  </p>
</div>

<style>
  .avatar {
    --silhouette: #12121f;
    --line-strong: rgba(233, 235, 244, 0.22);
    --screen-bg: #020208;
    --rain-color: var(--green);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    color: var(--purple);
  }

  svg {
    width: 100%;
    max-width: 300px;
    height: auto;
    overflow: visible;
  }

  /* ---------- breathing (always) ---------- */
  .figure {
    transform-origin: 160px 200px;
    animation: breathe 5s ease-in-out infinite;
  }
  @keyframes breathe {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
  }

  /* ---------- glyph rain ---------- */
  .rain-col {
    transform: translate(var(--tx, 0), 0);
    animation: rainfall 2.6s linear infinite;
    animation-delay: var(--delay);
  }
  @keyframes rainfall {
    from { transform: translate(var(--tx, 0), 0); opacity: 0.9; }
    to { transform: translate(var(--tx, 0), 110px); opacity: 0; }
  }
  .rain { opacity: 0.45; }
  .idle .rain-col { animation-duration: 4.5s; }

  /* ---------- thinking: they lean in and type ---------- */
  .thinking .rain { opacity: 0.95; }
  .thinking .rain-col { animation-duration: 1.1s; }
  .thinking .figure { animation: lean-in 1.6s ease-in-out infinite; }
  @keyframes lean-in {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-1px) scale(1.008); }
  }
  .thinking .head {
    transform-origin: 160px 140px;
    animation: consider 3.4s ease-in-out infinite;
  }
  @keyframes consider {
    0%, 100% { transform: rotate(0deg); }
    30% { transform: rotate(-3deg); }
    70% { transform: rotate(2.5deg); }
  }
  .thinking .hand-l { animation: type-l 0.34s ease-in-out infinite; }
  .thinking .hand-r { animation: type-r 0.34s ease-in-out infinite 0.17s; }
  @keyframes type-l { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
  @keyframes type-r { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
  .thinking .halo { opacity: 0.1; animation: halo-pulse 1.6s ease-in-out infinite; }
  @keyframes halo-pulse {
    0%, 100% { opacity: 0.06; }
    50% { opacity: 0.14; }
  }
  .thinking .circlet { filter: drop-shadow(0 0 4px var(--purple)); }

  /* ---------- speaking: ripples, purple room ---------- */
  .voice { opacity: 0; }
  .speaking .voice { opacity: 1; }
  .speaking .voice path { animation: ripple 1.4s ease-out infinite; }
  .speaking .voice path:nth-child(2),
  .speaking .voice path:nth-child(4) { animation-delay: 0.35s; }
  @keyframes ripple {
    0% { opacity: 0; transform: scale(0.92); }
    40% { opacity: 0.9; }
    100% { opacity: 0; transform: scale(1.06); }
  }
  .speaking .voice path { transform-origin: 160px 110px; }
  .speaking .halo { opacity: 0.16; }
  .speaking .rain { opacity: 0.6; }
  .speaking .rain-col { animation-duration: 2s; }
  .speaking .head { animation: nod 2.2s ease-in-out infinite; transform-origin: 160px 140px; }
  @keyframes nod {
    0%, 100% { transform: rotate(0deg) translateY(0); }
    50% { transform: rotate(1.5deg) translateY(1px); }
  }

  /* ---------- state line ---------- */
  .state-line {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    display: inline-block;
  }
  .dot.pulse { animation: dot-pulse 0.9s ease-in-out infinite; }
  .dot.talk { background: var(--purple); animation: dot-pulse 1.4s ease-in-out infinite; }
  @keyframes dot-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  @media (prefers-reduced-motion: reduce) {
    .figure, .head, .hand-l, .hand-r, .rain-col, .halo, .voice path, .dot {
      animation: none !important;
    }
  }
</style>
