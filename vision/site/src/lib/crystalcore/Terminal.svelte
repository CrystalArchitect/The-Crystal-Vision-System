<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { untrack } from 'svelte';
  import { STACK, ARC, USER } from './stack.js';

  let { flying = false, onfly = () => {} } = $props();

  let scrollEl = $state(null);
  let fieldEl = $state(null);
  let lines = $state([]);
  let fieldValue = $state('');

  let history = [];
  let hpos = -1;

  function esc(s) {
    return String(s).replace(/[<>&]/g, '');
  }

  function pushLine(html, cls) {
    lines.push({ html, cls: cls || '' });
  }
  function gap() {
    pushLine('&nbsp;');
  }

  function pad(s, n) {
    s = String(s);
    return s + new Array(Math.max(1, n - s.length + 1)).join('·');
  }
  function tag(state) {
    return state === 'surveyed'
      ? '<span class="cy">[ surveyed ]</span>'
      : '<span class="mg">[ dreamed  ]</span>';
  }

  function buildBoot() {
    const boot = [
      ['<span class="dim">CRYSTALCORE.OS</span>  <span class="faint">v0.1.0</span>', 90],
      ['<span class="faint">ground #06070E · arc 196°–300° · no white</span>', 90],
      ['&nbsp;', 140]
    ];
    STACK.forEach((o) => {
      boot.push([tag(o.state) + '  <span class="dim">' + pad(o.id, 15) + '</span> <span class="faint">' + o.gloss + '</span>', 110]);
    });
    boot.push(['&nbsp;', 200]);
    boot.push(['<div class="notice">crystalcore.os is a <span class="mg">dreamed</span> line.<br>you are standing inside something unbuilt.<br><span class="dim">the incognita rule holds. nothing here is shipped.</span></div>', 340]);
    boot.push(['&nbsp;', 120]);
    boot.push(['<span class="dim">welcome, <span class="vi">' + USER + '</span></span>', 90]);
    boot.push(['<span class="faint">type `help` · `fly` to move · `rule` for the rule</span>', 0]);
    return boot;
  }

  function boot(reduced, i) {
    const BOOT = buildBoot();
    function step(idx) {
      if (idx >= BOOT.length) {
        fieldEl?.focus();
        return;
      }
      pushLine(BOOT[idx][0]);
      const wait = reduced ? 0 : BOOT[idx][1];
      if (wait === 0 && idx < BOOT.length - 1) return step(idx + 1);
      setTimeout(() => step(idx + 1), wait);
    }
    step(i || 0);
  }

  const CMD = {
    help() {
      gap();
      pushLine('<span class="dim">ls</span>          <span class="faint">the stack, with states</span>');
      pushLine('<span class="dim">open &lt;name&gt;</span> <span class="faint">read one object</span>');
      pushLine('<span class="dim">rule</span>        <span class="faint">the incognita rule</span>');
      pushLine('<span class="dim">arc</span>         <span class="faint">the palette, 196° to 300°</span>');
      pushLine('<span class="dim">fly</span>         <span class="faint">move through it</span>');
      pushLine('<span class="dim">whoami</span>      <span class="faint">who is at the keys</span>');
      pushLine('<span class="dim">clear</span>       <span class="faint">wipe the buffer</span>');
      pushLine('<span class="dim">reboot</span>      <span class="faint">run the boot log again</span>');
      gap();
    },
    ls() {
      gap();
      STACK.forEach((o) => {
        pushLine(tag(o.state) + '  <span class="dim">' + pad(o.id, 15) + '</span> <span class="faint">' + o.gloss + '</span>');
      });
      gap();
      const s = STACK.filter((o) => o.state === 'surveyed').length;
      pushLine('<span class="faint">' + s + ' surveyed · ' + (STACK.length - s) + ' dreamed</span>');
      gap();
    },
    open(arg) {
      if (!arg) {
        pushLine('<span class="mg">open what?</span> <span class="faint">try `ls` for names</span>');
        return;
      }
      const o = STACK.filter((x) => x.id === arg)[0];
      if (!o) {
        pushLine('<span class="mg">no object named `' + esc(arg) + '`.</span> <span class="faint">`ls` lists what is mounted.</span>');
        return;
      }
      gap();
      pushLine(tag(o.state) + '  <span class="' + (o.state === 'surveyed' ? 'cy' : 'mg') + '">' + o.id + '</span>');
      pushLine('<span class="dim">' + o.note + '</span>');
      if (o.state === 'dreamed') {
        pushLine('<span class="faint">this is a dreamed line. it is not running anywhere.</span>');
      } else {
        pushLine('<span class="faint">this one is running code.</span>');
      }
      gap();
    },
    rule() {
      pushLine('<div class="ruleblock">Mark which lines are dreamed,<br>and which are surveyed.</div>');
      pushLine('<span class="faint">The-Incognita-Rule.md · TerAustralis Incognita</span>');
      gap();
    },
    arc() {
      gap();
      ARC.forEach((c) => {
        pushLine('<span class="sw" style="background:' + c[2] + '"></span><span class="dim">' + pad(c[1], 10) + '</span> <span class="faint">' + c[0] + '  ' + c[2] + '</span>');
      });
      gap();
      pushLine('<span class="faint">one continuous sweep, cyan into magenta. nothing outside the arc.</span>');
      pushLine('<span class="gd">gold #EFD383</span> <span class="faint">is held back for the rule alone.</span>');
      gap();
    },
    whoami() {
      pushLine('<span class="vi">' + USER + '</span> <span class="faint">· at the keys, inside a dreamed line</span>');
    },
    clear() {
      lines = [];
    },
    reboot() {
      lines = [];
      boot(reducedMotion());
    },
    fly() {
      onfly();
      pushLine('<span class="faint">flying · press any key to return</span>');
    }
  };
  CMD.status = CMD.ls;

  function reducedMotion() {
    return typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function run(raw) {
    const line = raw.trim();
    pushLine('<span class="echo">&rsaquo; <b>' + esc(line) + '</b></span>');
    if (!line) return;
    history.unshift(line);
    hpos = -1;

    const parts = line.toLowerCase().split(/\s+/);
    const fn = CMD[parts[0]];
    if (fn) fn(parts[1]);
    else pushLine('<span class="mg">`' + esc(parts[0]) + '` is not a command here.</span> <span class="faint">`help` lists what is.</span>');
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      run(fieldValue);
      fieldValue = '';
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (hpos < history.length - 1) fieldValue = history[++hpos];
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (hpos > 0) fieldValue = history[--hpos];
      else {
        hpos = -1;
        fieldValue = '';
      }
    }
  }

  $effect(() => {
    lines.length; // track
    if (scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
  });

  $effect(() => {
    // Runs once on mount. untrack() is load-bearing here: without it,
    // reading fieldEl to call .focus() makes this effect depend on
    // fieldEl, and re-focusing the bound element re-triggers the same
    // effect — an infinite loop (Svelte's effect_update_depth_exceeded).
    untrack(() => {
      boot(reducedMotion());
      fieldEl?.focus();
    });
  });

  $effect(() => {
    function refocus() {
      if (!flying) fieldEl?.focus();
    }
    document.addEventListener('click', refocus);
    return () => document.removeEventListener('click', refocus);
  });

  // landing (flying true -> false) prints its own line and reclaims focus,
  // same as the reference implementation's land() — not left to the
  // passive click-refocus listener above, which only covers click, not key.
  let wasFlying = false;
  $effect(() => {
    const justLanded = wasFlying && !flying;
    wasFlying = flying;
    if (justLanded) {
      untrack(() => {
        pushLine('<span class="faint">landed.</span>');
        fieldEl?.focus();
      });
    }
  });
</script>

<!-- section, not main: the page landmark lives in the root layout -->
<section class="shell" class:flying aria-label="CrystalCore terminal">
  <div class="scroll" bind:this={scrollEl}>
    {#each lines as line}
      <div class="ln {line.cls}">{@html line.html}</div>
    {/each}
  </div>
  <div class="prompt">
    <span class="sigil">&rsaquo;</span>
    <input
      class="field"
      bind:this={fieldEl}
      bind:value={fieldValue}
      onkeydown={handleKeydown}
      autocomplete="off"
      autocapitalize="off"
      spellcheck="false"
      placeholder="type `help`"
      aria-label="CrystalCore.OS command line"
    />
  </div>
</section>

<style>
  .shell {
    position: relative;
    z-index: 3;
    height: 100%;
    max-width: 860px;
    margin: 0 auto;
    padding: 74px 26px 22px;
    display: flex;
    flex-direction: column;
  }
  .shell.flying {
    opacity: 0.14;
    transition: opacity 0.5s ease;
  }

  .scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: var(--cc-rule) transparent;
    padding-right: 6px;
  }
  .scroll::-webkit-scrollbar {
    width: 3px;
  }
  .scroll::-webkit-scrollbar-thumb {
    background: var(--cc-rule);
  }

  .ln {
    white-space: pre-wrap;
    word-break: break-word;
    min-height: 1.65em;
  }
  :global(.dim) {
    color: var(--cc-ink-dim);
  }
  :global(.faint) {
    color: var(--cc-ink-faint);
  }
  :global(.cy) {
    color: var(--cc-cyan);
  }
  :global(.mg) {
    color: var(--cc-magenta);
  }
  :global(.vi) {
    color: var(--cc-violet);
  }
  :global(.sk) {
    color: var(--cc-sky);
  }
  :global(.gd) {
    color: var(--cc-gold);
  }

  :global(.echo) {
    color: var(--cc-ink-dim);
  }
  :global(.echo b) {
    color: var(--cc-cyan);
    font-weight: 400;
  }

  :global(.notice) {
    border-left: 1px solid var(--cc-magenta);
    padding: 2px 0 2px 14px;
    margin: 14px 0;
    color: var(--cc-ink);
    display: block;
  }

  :global(.ruleblock) {
    border-left: 1px solid var(--cc-gold);
    padding: 4px 0 4px 14px;
    margin: 14px 0;
    font-family: var(--cc-display);
    font-size: 19px;
    line-height: 1.45;
    color: var(--cc-gold);
    display: block;
  }

  :global(.sw) {
    display: inline-block;
    width: 26px;
    height: 9px;
    vertical-align: middle;
    margin-right: 9px;
  }

  .prompt {
    display: flex;
    align-items: baseline;
    gap: 9px;
    border-top: 1px solid var(--cc-rule);
    margin-top: 12px;
    padding-top: 12px;
  }
  .sigil {
    color: var(--cc-violet);
    flex: none;
  }
  .field {
    flex: 1;
    background: transparent;
    border: 0;
    outline: 0;
    font-family: var(--cc-mono);
    font-size: 14px;
    color: var(--cc-cyan);
    caret-color: var(--cc-cyan);
  }
  .field::placeholder {
    color: var(--cc-ink-faint);
  }
  .shell:focus-within .prompt {
    border-top-color: var(--cc-violet);
  }

  @media (max-width: 640px) {
    .shell {
      padding: 66px 18px 16px;
    }
    :global(.ruleblock) {
      font-size: 17px;
    }
  }
</style>
