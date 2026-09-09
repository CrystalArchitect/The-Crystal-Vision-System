<script>
  import { atlasPlates } from '$lib/atlas';

  let activeIndex = $state(0);
  let dreamMode = $state('resting');
  let reducedMotion = $state(false);
  let checklist = $state({
    opening: true,
    sequence: true,
    directSelection: false,
    edgeStates: false,
    keyboard: false,
    boundary: true
  });
  let events = $state([
    { time: 'initial', message: 'Runner initialized at index 0 · First Sketch' }
  ]);

  const activePlate = $derived(atlasPlates[activeIndex]);
  const firstPlate = $derived(activeIndex === 0);
  const lastPlate = $derived(activeIndex === atlasPlates.length - 1);
  const passed = $derived(Object.values(checklist).filter(Boolean).length);

  function log(message) {
    events = [{ time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), message }, ...events].slice(0, 8);
  }

  function selectPlate(index) {
    activeIndex = Math.max(0, Math.min(index, atlasPlates.length - 1));
    log(`select(${index}) → index ${activeIndex} · ${atlasPlates[activeIndex].plate}`);
    checklist.directSelection = true;
  }

  function previousPlate() {
    if (firstPlate) {
      log('previous() blocked at lower boundary · index remains 0');
      checklist.edgeStates = true;
      return;
    }
    activeIndex -= 1;
    log(`previous() → index ${activeIndex} · ${activePlate.plate}`);
  }

  function nextPlate() {
    if (lastPlate) {
      log(`next() blocked at upper boundary · index remains ${activeIndex}`);
      checklist.edgeStates = true;
      return;
    }
    activeIndex += 1;
    log(`next() → index ${activeIndex} · ${activePlate.plate}`);
  }

  function toggleCheck(key) {
    checklist[key] = !checklist[key];
  }
</script>

<svelte:head>
  <title>Atlas Test Runner — TerAustralis Incognita</title>
  <meta name="description" content="Interactive QA preview for the Celestial Atlas dream-circle and plate navigator state machine." />
</svelte:head>

<div class="runner-shell">
  <header class="runner-header">
    <div>
      <p class="eyebrow">QA instrument · PR #101</p>
      <h1>Atlas state runner<span>dream-circle / plate navigator</span></h1>
    </div>
    <div class="header-meta"><span class="status-dot"></span><span>LOCAL PREVIEW</span><small>/atlas/test-runner</small></div>
  </header>

  <main>
    <section class="control-bar" aria-labelledby="controls-title">
      <div>
        <p class="eyebrow">01 · Test controls</p>
        <h2 id="controls-title">Change the state. Watch the boundary.</h2>
      </div>
      <div class="controls">
        <label>Dream-circle mode
          <select bind:value={dreamMode}>
            <option value="resting">Resting</option>
            <option value="focused">Focused</option>
            <option value="transitioning">Transitioning</option>
          </select>
        </label>
        <label class="toggle"><input type="checkbox" bind:checked={reducedMotion} /> Reduced motion</label>
        <button type="button" class="reset" onclick={() => { activeIndex = 0; dreamMode = 'resting'; reducedMotion = false; log('runner reset → index 0 · resting'); }}>Reset runner</button>
      </div>
    </section>

    <section class="instrument-grid">
      <div class="circle-instrument" class:focused={dreamMode === 'focused'} class:transitioning={dreamMode === 'transitioning'} class:reduced={reducedMotion} aria-label={`Dream-circle ${dreamMode} state`}>
        <div class="crosshair"></div>
        <div class="ring ring-outer"></div><div class="ring ring-inner"></div>
        <img src="/assets/art/celestial-atlas-night-from-the-edge.jpeg" alt="Night from the Edge preview" />
        <div class="circle-label"><span>THE SOUTHERN</span><strong>INVISIBLE ATLAS</strong><small>{dreamMode.toUpperCase()} · {reducedMotion ? 'MOTION OFF' : 'MOTION ON'}</small></div>
      </div>
      <div class="instrument-readout">
        <p class="eyebrow">Dream-circle readout</p>
        <div class="readout-line"><span>Mode</span><strong>{dreamMode}</strong></div>
        <div class="readout-line"><span>Animation</span><strong>{reducedMotion ? 'disabled' : 'available'}</strong></div>
        <div class="readout-line"><span>Visual boundary</span><strong>purple ring / no telemetry</strong></div>
        <p class="readout-note">The circle is tested as a visual threshold. It must remain atmospheric, not scientific, and must never be the only carrier of meaning.</p>
        <div class="pass-badge"><span>{checklist.opening ? 'PASS' : 'OPEN'}</span><small>opening composition</small></div>
      </div>
    </section>

    <section class="navigator-panel" aria-labelledby="navigator-title">
      <div class="panel-heading"><div><p class="eyebrow">02 · State machine</p><h2 id="navigator-title">{activePlate.plate} <em>{activePlate.title}</em></h2></div><div class="counter">INDEX <strong>{activeIndex}</strong> / {atlasPlates.length - 1}</div></div>
      <nav class="plate-nav" aria-label="Test plate navigator">
        {#each atlasPlates as plate, index}
          <button class:active={index === activeIndex} type="button" aria-current={index === activeIndex ? 'page' : undefined} aria-label={`Select ${plate.plate} ${plate.title}`} onclick={() => selectPlate(index)}>
            <span>{plate.plate}</span><small>{plate.sequence}</small>
          </button>
        {/each}
      </nav>
      <div class="state-detail">
        <div class="plate-thumb"><img src={`/assets/art/${activePlate.filename}`} alt={`${activePlate.plate} ${activePlate.title}`} /><span class="vision-seal">VISION</span></div>
        <div class="state-copy"><p class="eyebrow">Current state · {activeIndex + 1} / {atlasPlates.length}</p><h3>{activePlate.title}</h3><p>{activePlate.interpretation}</p><small>{activePlate.boundary}</small></div>
        <div class="movement"><button type="button" onclick={previousPlate} disabled={firstPlate}>← Previous</button><button type="button" onclick={nextPlate} disabled={lastPlate}>Next →</button></div>
      </div>
    </section>

    <section class="lower-grid">
      <div class="qa-panel"><div class="panel-heading"><div><p class="eyebrow">03 · Acceptance matrix</p><h2>Runner coverage</h2></div><div class="coverage"><strong>{passed}</strong><span>/ {Object.keys(checklist).length} pass</span></div></div>
        {#each [
          ['opening', 'Dream-circle opening is visible and bounded'],
          ['sequence', 'Navigator exposes all 11 ordered entries'],
          ['directSelection', 'Direct selection updates all detail fields'],
          ['edgeStates', 'Previous / Next edges block invalid states'],
          ['keyboard', 'Keyboard focus and activation verified'],
          ['boundary', 'Vision boundary remains visible in every state']
        ] as item}
          <label class="check-row"><input type="checkbox" checked={checklist[item[0]]} onchange={() => toggleCheck(item[0])} /><span class:checked={checklist[item[0]]}>{item[1]}</span><b>{checklist[item[0]] ? 'PASS' : 'OPEN'}</b></label>
        {/each}
      </div>
      <div class="event-panel"><p class="eyebrow">04 · Transition log</p><h2>Event trace</h2><div class="event-list">{#each events as event}<div class="event"><time>{event.time}</time><span>{event.message}</span></div>{/each}</div><button class="clear" type="button" onclick={() => (events = [])}>Clear trace</button></div>
    </section>
  </main>

  <footer class="runner-footer"><span>Source surface: `/atlas`</span><span>Evidence boundary: unchanged</span><span>Build target: Playwright-ready</span></footer>
</div>

<style>
  :global(body) { background: #080b0d; }
  .runner-shell { max-width: 1380px; margin: 0 auto; padding: 2rem 0 4rem; color: var(--observatory-ivory); }
  .runner-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; padding-bottom: 2.4rem; border-bottom: 1px solid var(--observatory-line); }
  .eyebrow { color: var(--observatory-copper); font: .66rem/1.3 var(--font-mono); letter-spacing: .18em; text-transform: uppercase; }
  h1 { margin-top: .8rem; font: 500 clamp(2.8rem, 6vw, 6.4rem)/.88 var(--font-display); letter-spacing: -.06em; }
  h1 span { display: block; color: var(--observatory-copper); font-size: .45em; font-style: italic; margin-top: .3em; }
  h2 { margin-top: .65rem; font: 500 clamp(1.8rem, 3vw, 3.1rem)/.95 var(--font-display); letter-spacing: -.04em; }
  h3 { margin-top: .6rem; font: italic 500 clamp(2rem, 3.2vw, 3.8rem)/.95 var(--font-display); }
  .header-meta { display: flex; align-items: center; gap: .55rem; color: var(--observatory-muted); font: .62rem var(--font-mono); letter-spacing: .1em; text-transform: uppercase; }
  .header-meta small { color: var(--observatory-sand); letter-spacing: .02em; text-transform: none; }
  .status-dot { width: .45rem; height: .45rem; border-radius: 50%; background: var(--observatory-copper); box-shadow: 0 0 14px rgba(170,145,201,.8); }
  .control-bar,.panel-heading { display: flex; justify-content: space-between; align-items: end; gap: 2rem; }
  .control-bar { padding: 3rem 0 2rem; }
  .controls { display: flex; align-items: end; gap: 1.3rem; flex-wrap: wrap; }
  .controls label { display: grid; gap: .45rem; color: var(--observatory-muted); font: .62rem var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
  select,.reset,.clear { padding: .7rem .8rem; border: 1px solid var(--observatory-line-strong); background: #0b1013; color: var(--observatory-ivory); font: .68rem var(--font-mono); }
  select:focus-visible,.reset:focus-visible,.clear:focus-visible,input:focus-visible,button:focus-visible { outline: 2px solid var(--observatory-copper); outline-offset: 3px; }
  .toggle { display: flex !important; align-items: center; grid-template-columns: auto auto !important; gap: .45rem !important; padding-bottom: .75rem; }
  .toggle input,.check-row input { accent-color: var(--observatory-copper); }
  .reset,.clear { color: var(--observatory-copper); cursor: pointer; }
  .instrument-grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(250px, .65fr); gap: 3rem; align-items: center; min-height: 460px; border-top: 1px solid var(--observatory-line); border-bottom: 1px solid var(--observatory-line); }
  .circle-instrument { position: relative; width: min(100%, 720px); aspect-ratio: 1.4; display: grid; place-items: center; isolation: isolate; }
  .circle-instrument img { width: 72%; aspect-ratio: 1; object-fit: cover; clip-path: circle(48%); opacity: .72; filter: saturate(.7) contrast(1.05); transition: opacity .35s ease, filter .35s ease; }
  .ring { position: absolute; border: 1px solid var(--observatory-copper); border-radius: 50%; transition: transform .35s ease, opacity .35s ease, box-shadow .35s ease; }
  .ring-outer { width: 82%; aspect-ratio: 1; opacity: .3; box-shadow: 0 0 70px rgba(170,145,201,.14); }
  .ring-inner { width: 56%; aspect-ratio: 1; opacity: .7; }
  .crosshair { position: absolute; width: 90%; height: 1px; background: linear-gradient(90deg, transparent, var(--observatory-copper), transparent); opacity: .4; }
  .circle-label { position: absolute; right: 4%; bottom: 9%; display: grid; gap: .3rem; color: var(--observatory-ivory); font: .65rem var(--font-mono); letter-spacing: .12em; text-align: right; }
  .circle-label strong { color: var(--observatory-copper); font-weight: 400; }
  .circle-label small { color: var(--observatory-muted); font-size: .55rem; }
  .circle-instrument.focused .ring-inner { transform: scale(1.1); opacity: 1; box-shadow: 0 0 35px rgba(170,145,201,.35); }
  .circle-instrument.focused img { opacity: .9; filter: saturate(.85) contrast(1.1); }
  .circle-instrument.transitioning .ring-outer { transform: rotate(8deg) scale(1.03); opacity: .65; }
  .circle-instrument.transitioning .ring-inner { transform: rotate(-10deg) scale(.95); }
  .circle-instrument.reduced .ring,.circle-instrument.reduced img { transition: none; }
  .instrument-readout { padding: 1.4rem 0; border-left: 1px solid var(--observatory-line); padding-left: 2rem; }
  .readout-line { display: flex; justify-content: space-between; gap: 1rem; padding: .85rem 0; border-bottom: 1px solid var(--observatory-line); color: var(--observatory-muted); font: .68rem var(--font-mono); }
  .readout-line strong { color: var(--observatory-copper); font-weight: 400; text-align: right; }
  .readout-note { margin-top: 1.4rem; color: var(--observatory-muted); font-size: .85rem; line-height: 1.6; }
  .pass-badge { display: flex; align-items: center; gap: .8rem; margin-top: 2rem; color: var(--observatory-muted); font: .62rem var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
  .pass-badge span { padding: .42rem .55rem; border: 1px solid var(--observatory-copper); color: var(--observatory-copper); }
  .navigator-panel,.lower-grid { padding-top: 4.5rem; }
  .counter,.coverage { color: var(--observatory-muted); font: .62rem var(--font-mono); letter-spacing: .12em; text-transform: uppercase; }
  .counter strong,.coverage strong { color: var(--observatory-copper); font-size: 1.3rem; font-weight: 400; }
  .panel-heading em { color: var(--observatory-copper); font-style: italic; }
  .plate-nav { display: flex; overflow-x: auto; margin-top: 2rem; border-top: 1px solid var(--observatory-line); border-bottom: 1px solid var(--observatory-line); }
  .plate-nav button { min-width: 90px; flex: 0 0 auto; padding: 1rem .8rem; border: 0; border-right: 1px solid var(--observatory-line); background: transparent; color: var(--observatory-muted); text-align: left; cursor: pointer; }
  .plate-nav button:first-child { border-left: 1px solid var(--observatory-line); }
  .plate-nav button span { display: block; color: inherit; font: .8rem var(--font-mono); letter-spacing: .08em; }
  .plate-nav button small { display: block; margin-top: .5rem; color: inherit; font: .55rem var(--font-mono); letter-spacing: .06em; white-space: nowrap; }
  .plate-nav button.active,.plate-nav button:hover { color: var(--observatory-copper); background: rgba(170,145,201,.08); }
  .state-detail { display: grid; grid-template-columns: minmax(260px, 1.2fr) minmax(220px, .8fr) auto; gap: 2rem; align-items: center; padding-top: 2.5rem; }
  .plate-thumb { position: relative; border: 1px solid var(--observatory-line-strong); background: #071019; }
  .plate-thumb img { display: block; width: 100%; aspect-ratio: 1.4; object-fit: contain; }
  .vision-seal { position: absolute; top: 1rem; right: 1rem; padding: .42rem .5rem; border: 1px solid var(--observatory-copper); background: rgba(8,11,11,.78); color: var(--observatory-copper); font: .58rem var(--font-mono); letter-spacing: .12em; }
  .state-copy p:not(.eyebrow) { margin-top: 1.25rem; color: var(--observatory-ivory); font: 1rem/1.5 var(--font-display); }
  .state-copy small { display: block; margin-top: 1rem; color: var(--observatory-muted); font-size: .76rem; line-height: 1.5; }
  .movement { display: flex; flex-direction: column; gap: .6rem; }
  .movement button,.clear { padding: .65rem .7rem; border: 1px solid var(--observatory-line-strong); background: transparent; color: var(--observatory-copper); font: .62rem var(--font-mono); cursor: pointer; white-space: nowrap; }
  .movement button:disabled { color: var(--observatory-muted); opacity: .4; cursor: not-allowed; }
  .lower-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 3rem; }
  .qa-panel,.event-panel { border-top: 1px solid var(--observatory-line); }
  .check-row { display: grid; grid-template-columns: auto 1fr auto; gap: .8rem; align-items: center; padding: .9rem 0; border-bottom: 1px solid var(--observatory-line); color: var(--observatory-muted); font-size: .82rem; cursor: pointer; }
  .check-row span.checked { color: var(--observatory-ivory); }
  .check-row b { color: var(--observatory-copper); font: .58rem var(--font-mono); font-weight: 400; letter-spacing: .1em; }
  .event-list { margin-top: 1.4rem; border-top: 1px solid var(--observatory-line); }
  .event { display: grid; grid-template-columns: 5rem 1fr; gap: .8rem; padding: .85rem 0; border-bottom: 1px solid var(--observatory-line); color: var(--observatory-ivory); font: .75rem/1.4 var(--font-mono); }
  .event time { color: var(--observatory-copper); }
  .clear { margin-top: 1.2rem; }
  .runner-footer { display: flex; justify-content: space-between; gap: 1rem; margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--observatory-line); color: var(--observatory-muted); font: .58rem var(--font-mono); letter-spacing: .09em; text-transform: uppercase; }
  @media (max-width: 820px) { .runner-header,.control-bar,.panel-heading { display: block; } .header-meta { margin-top: 1.5rem; } .controls { margin-top: 1.5rem; } .instrument-grid,.lower-grid { grid-template-columns: 1fr; } .instrument-readout { padding-left: 0; border-left: 0; border-top: 1px solid var(--observatory-line); } .state-detail { grid-template-columns: 1fr 1fr; } .movement { grid-column: 1 / -1; flex-direction: row; } .runner-footer { display: grid; } }
  @media (max-width: 520px) { .runner-shell { padding-top: 1rem; } h1 { font-size: 3.5rem; } .circle-instrument { min-height: 300px; } .state-detail { grid-template-columns: 1fr; } .movement { grid-column: auto; } .movement button { flex: 1; } }
</style>
