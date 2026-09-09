<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import Starfield from '$lib/crystalcore/Starfield.svelte';
  import Terminal from '$lib/crystalcore/Terminal.svelte';
  import { USER } from '$lib/crystalcore/stack.js';

  let flying = $state(false);
  let uptime = $state('00:00');

  $effect(() => {
    const t0 = Date.now();
    const id = setInterval(() => {
      const s = Math.floor((Date.now() - t0) / 1000);
      uptime = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
    }, 1000);
    return () => clearInterval(id);
  });

  // any key or click lands the flight — only listening while actually flying
  $effect(() => {
    if (!flying) return;
    function landKey(e) {
      e.preventDefault();
      flying = false;
    }
    function landClick() {
      flying = false;
    }
    // Deferred by one task: `fly` itself runs from a keydown on the
    // terminal input, which bubbles to window right after this effect
    // runs. Attaching synchronously would let that same keydown catch
    // its own listener and land in the tick it took off. A fresh task
    // guarantees these only see key/click events that happen after.
    const timer = setTimeout(() => {
      window.addEventListener('keydown', landKey);
      window.addEventListener('click', landClick);
    }, 0);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('keydown', landKey);
      window.removeEventListener('click', landClick);
    };
  });
</script>

<svelte:head>
  <title>CrystalCore.OS — TerAustralis Incognita</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link
    href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=IBM+Plex+Mono:wght@300;400;500&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="crystalcore">
  <Starfield {flying} />
  <div class="vignette"></div>

  <span class="bracket br-tl"></span>
  <span class="bracket br-tr"></span>
  <span class="bracket br-bl"></span>
  <span class="bracket br-br"></span>

  <div class="wordmark">CrystalCore<i>.OS</i></div>
  <div class="readout">
    <div>arc <b>196°–300°</b></div>
    <div>gnd <b>#06070E</b></div>
    <div>usr <b>{USER}</b></div>
    <div>up <b>{uptime}</b></div>
  </div>

  {#if flying}
    <div class="flightcard">
      <p>Mark which lines are dreamed, and which are surveyed.</p>
      <small>press any key to return</small>
    </div>
  {/if}

  <Terminal {flying} onfly={() => (flying = true)} />
</div>

<style>
  :global(html, body) {
    height: 100%;
  }

  .crystalcore {
    position: fixed;
    inset: 0;
    overflow: hidden;
    background: var(--cc-ground);
    color: var(--cc-ink);
    font-family: var(--cc-mono);
    font-size: 14px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;

    --cc-ground: #06070e;
    --cc-cyan: #3cdce5; /* 196° — surveyed */
    --cc-sky: #55a4eb;
    --cc-blue: #4771da;
    --cc-indigo: #6641db;
    --cc-violet: #8443e8;
    --cc-magenta: #c977ec; /* 300° — dreamed */
    --cc-gold: #efd383; /* the Rule, and nothing else */

    --cc-ink: #a2b0dc;
    --cc-ink-dim: #5c6a9b;
    --cc-ink-faint: #333d63;

    --cc-rule: rgba(102, 65, 219, 0.26);
    --cc-mono: 'IBM Plex Mono', ui-monospace, monospace;
    --cc-display: 'Bodoni Moda', Georgia, serif;
  }

  .vignette {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    background: radial-gradient(ellipse 120% 80% at 50% 45%, transparent 40%, rgba(6, 7, 14, 0.82) 100%);
  }

  .bracket {
    position: fixed;
    width: 34px;
    height: 34px;
    z-index: 4;
    pointer-events: none;
    opacity: 0.5;
  }
  .bracket::before,
  .bracket::after {
    content: '';
    position: absolute;
    background: var(--cc-indigo);
  }
  .bracket::before {
    width: 100%;
    height: 1px;
  }
  .bracket::after {
    width: 1px;
    height: 100%;
  }
  .br-tl {
    top: 20px;
    left: 20px;
  }
  .br-tl::before,
  .br-tl::after {
    top: 0;
    left: 0;
  }
  .br-tr {
    top: 20px;
    right: 20px;
  }
  .br-tr::before,
  .br-tr::after {
    top: 0;
    right: 0;
  }
  .br-bl {
    bottom: 20px;
    left: 20px;
  }
  .br-bl::before,
  .br-bl::after {
    bottom: 0;
    left: 0;
  }
  .br-br {
    bottom: 20px;
    right: 20px;
  }
  .br-br::before,
  .br-br::after {
    bottom: 0;
    right: 0;
  }

  .readout {
    position: fixed;
    top: 26px;
    right: 34px;
    z-index: 5;
    text-align: right;
    font-size: 10px;
    letter-spacing: 0.13em;
    color: var(--cc-ink-faint);
    text-transform: uppercase;
    line-height: 1.9;
    pointer-events: none;
  }
  .readout :global(b) {
    color: var(--cc-ink-dim);
    font-weight: 400;
  }

  .wordmark {
    position: fixed;
    top: 22px;
    left: 36px;
    z-index: 5;
    pointer-events: none;
    font-family: var(--cc-display);
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 0.05em;
    color: var(--cc-ink-dim);
  }
  .wordmark :global(i) {
    font-style: normal;
    color: var(--cc-violet);
  }

  .flightcard {
    position: fixed;
    inset: 0;
    z-index: 6;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    pointer-events: none;
  }
  .flightcard p {
    font-family: var(--cc-display);
    font-size: clamp(20px, 4.4vw, 38px);
    color: var(--cc-ink);
    line-height: 1.35;
    max-width: 16ch;
    text-shadow: 0 0 34px rgba(132, 67, 232, 0.55);
  }
  .flightcard small {
    display: block;
    margin-top: 20px;
    font-family: var(--cc-mono);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--cc-ink-faint);
  }

  @media (max-width: 640px) {
    .crystalcore {
      font-size: 13px;
    }
    .readout {
      top: 22px;
      right: 24px;
      font-size: 9px;
      line-height: 1.75;
    }
    .wordmark {
      left: 24px;
      font-size: 13px;
    }
    .bracket {
      width: 22px;
      height: 22px;
      top: 14px;
      left: 14px;
    }
    .br-tr {
      right: 14px;
      left: auto;
    }
    .br-bl {
      bottom: 14px;
      top: auto;
    }
    .br-br {
      bottom: 14px;
      right: 14px;
      top: auto;
      left: auto;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .crystalcore :global(*) {
      animation: none !important;
      transition: none !important;
    }
  }
</style>
