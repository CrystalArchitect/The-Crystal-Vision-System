<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  const findings = [
    { id: 'link-in-text-block', label: 'Footer links need a non-colour cue', affected: 57, total: 57, kind: 'Shared', detail: 'The same shared-footer issue reproduced on every audited route.' },
    { id: 'heading-order', label: 'Heading hierarchy needs a separate review', affected: 1, total: 57, kind: 'Route-specific', detail: 'This route-specific issue was isolated to /crystalcore-os.' }
  ];

  const routeRegister = [
    { route: 'All audited routes', coverage: '57 prerendered routes', score: '0.95–0.96', finding: 'Shared footer link distinction', status: 'Healthy' },
    { route: '/atlas-ten', coverage: 'Named focus route', score: '0.95–0.96', finding: 'Shared footer link distinction', status: 'Healthy' },
    { route: '/crystalcore-os', coverage: 'Named follow-up route', score: '0.95', finding: 'Shared footer link distinction · heading-order', status: 'Review' }
  ];

  let query = $state('');
  let filter = $state('all');
  let filteredRoutes = $derived(routeRegister.filter((item) => {
    const haystack = `${item.route} ${item.coverage} ${item.score} ${item.finding}`.toLowerCase();
    const matchesQuery = !query.trim() || haystack.includes(query.trim().toLowerCase());
    const matchesFilter = filter === 'all' || item.status.toLowerCase() === filter;
    return matchesQuery && matchesFilter;
  }));
</script>

<svelte:head>
  <title>Shared Footer Route Audit | TerAustralis Incognita</title>
  <meta name="description" content="Evidence-first route health and accessibility summary for the TerAustralis public surface." />
</svelte:head>

<div class="audit-page">
  <section class="audit-hero wrap">
    <div class="hero-copy">
      <p class="kicker"><span></span> Accessibility / route health</p>
      <h1>Shared footer<br /><em>route audit</em></h1>
      <p class="lede">A measured view of the production surface — where every route is accounted for, every shared pattern is visible, and the next fix is easy to find.</p>
      <div class="meta"><span>Audited 24 August 2026</span><i></i><span>Lighthouse + HTTP</span></div>
    </div>
    <div class="coverage-orbit" aria-label="100 percent HTTP 200 route coverage">
      <div class="orbit orbit-dashed"><span>ROUTE<br />COVERAGE</span></div>
      <div class="orbit orbit-inner"><strong>100%</strong><small>HTTP 200</small></div>
      <b class="ray ray-left"></b><b class="ray ray-right"></b>
    </div>
  </section>

  <section class="metrics wrap" aria-label="Audit summary">
    <div><span>Routes audited</span><strong>57</strong><small>Concrete prerendered routes</small></div>
    <div class="healthy"><span>Healthy responses</span><strong>57 / 57</strong><small>No HTTP route failures</small></div>
    <div class="healthy"><span>Footer coverage</span><strong>100%</strong><small>Shared markup present</small></div>
    <div class="warning"><span>Score range</span><strong>0.95–0.96</strong><small>Accessibility before patch</small></div>
  </section>

  <section class="finding-grid wrap" id="findings">
    <article class="panel">
      <div class="panel-head"><div><span class="eyebrow">Signal map</span><h2>What the audit found</h2></div><span>01 / 02</span></div>
      <p class="intro">One shared pattern explains the dominant warning. One route deserves its own structural pass.</p>
      <div class="finding-list">
        {#each findings as finding, index}
          <div class="finding">
            <b class:amber={index === 1}>{String(index + 1).padStart(2, '0')}</b>
            <div><div class="finding-title"><h3>{finding.label}</h3><mark class:amber={index === 1}>{finding.kind}</mark></div><p>{finding.detail}</p><div class="bar"><i class:amber={index === 1} style={`width: ${(finding.affected / finding.total) * 100}%`}></i></div></div>
            <strong>{finding.affected}<small>/{finding.total}</small></strong>
          </div>
        {/each}
      </div>
    </article>
    <article class="panel sequence">
      <div class="panel-head"><div><span class="eyebrow">Recommended sequence</span><h2>Fix the pattern,<br />then the outlier</h2></div><span>02 / 02</span></div>
      <div class="step"><b class="done">✓</b><div><span class="eyebrow">Step 01 / complete in draft</span><h3>Underline shared footer links</h3><p>Use a persistent non-colour cue and the canonical ivory token across all routes.</p></div></div>
      <div class="connector"></div>
      <div class="step"><b class="next">02</b><div><span class="eyebrow">Step 02 / follow-up</span><h3>Review /crystalcore-os</h3><p>Inspect heading order independently; the footer patch will not affect this finding.</p></div></div>
    </article>
  </section>

  <section class="register wrap" id="routes">
    <div class="register-head"><div><p class="kicker"><span></span> Route register</p><h2>Coverage at a glance</h2></div><small>57 routes in scope</small></div>
    <div class="toolbar"><label><span aria-hidden="true">⌕</span><input bind:value={query} placeholder="Filter routes or findings" aria-label="Filter routes or findings" /></label><div class="filters" role="group" aria-label="Filter by status"><button class:active={filter === 'all'} onclick={() => filter = 'all'}>All</button><button class:active={filter === 'healthy'} onclick={() => filter = 'healthy'}>Healthy</button><button class:active={filter === 'review'} onclick={() => filter = 'review'}>Review</button></div></div>
    <div class="table-shell"><table><thead><tr><th>Route / cohort</th><th>Coverage</th><th>Accessibility</th><th>Finding</th><th>Status</th></tr></thead><tbody>{#each filteredRoutes as item}<tr><td><strong>{item.route}</strong></td><td>{item.coverage}</td><td><mark>{item.score}</mark></td><td><span class="finding-chip">{item.finding}</span></td><td><span class:review={item.status === 'Review'} class="status"><i></i>{item.status}</span></td></tr>{/each}</tbody></table>{#if filteredRoutes.length === 0}<p class="empty">No routes match this filter.</p>{/if}</div>
    <p class="table-note">◈ The register shows named focus routes plus the full audited cohort. Every route returned HTTP 200.</p>
  </section>

  <section class="method wrap" id="methodology">
    <div><p class="kicker"><span></span> Audit notes</p><h2>Evidence first.<br /><em>Action second.</em></h2><p>This dashboard reflects the supplied route-audit report, not a live telemetry stream. It preserves the distinction between measured findings and recommended remediation.</p></div>
    <div class="method-grid"><div><span>01</span><h3>HTTP health</h3><p>57 of 57 concrete prerendered routes returned HTTP 200.</p></div><div><span>02</span><h3>Shared markup</h3><p>Every route included the shared footer component.</p></div><div><span>03</span><h3>Lighthouse</h3><p>Accessibility audits completed after a lower-concurrency retry.</p></div></div>
  </section>
</div>

<style>
  .audit-page { --audit-bg: var(--observatory-bg); --audit-surface: var(--observatory-surface); --audit-ink: var(--observatory-ink); --audit-muted: var(--observatory-muted); --audit-purple: var(--observatory-copper); --audit-green: var(--observatory-green); --audit-warning: var(--observatory-warning); min-height: 100vh; margin: 0; background: radial-gradient(circle at 75% 0%, rgba(170,145,201,.13), transparent 32rem), var(--audit-bg); color: var(--audit-ink); }
  .wrap { max-width: 1180px; margin: 0 auto; padding-left: 28px; padding-right: 28px; }
  .audit-hero { display: flex; align-items: center; justify-content: space-between; gap: 50px; min-height: 430px; padding-top: 80px; padding-bottom: 62px; border-bottom: 1px solid var(--observatory-line); }
  .hero-copy { max-width: 650px; }.kicker { display: flex; align-items: center; gap: 9px; margin: 0; color: var(--audit-purple); font-family: var(--observatory-font-mono); font-size: 10px; letter-spacing: .16em; text-transform: uppercase; }.kicker span { width: 25px; height: 1px; background: var(--audit-purple); }.hero-copy h1 { margin: 22px 0 16px; font-family: var(--observatory-font-display); font-size: clamp(55px, 7vw, 92px); font-weight: 400; line-height: .87; letter-spacing: -.07em; }.hero-copy h1 em, .method h2 em { color: var(--audit-purple); font-style: italic; }.lede { max-width: 590px; margin: 0; color: var(--audit-muted); font-family: var(--observatory-font-body); font-size: 14px; line-height: 1.7; }.meta { display: flex; align-items: center; gap: 12px; margin-top: 27px; color: var(--audit-muted); font-family: var(--observatory-font-mono); font-size: 10px; }.meta i { width: 1px; height: 12px; background: var(--observatory-line); }
  .coverage-orbit { position: relative; flex: 0 0 auto; width: 255px; height: 255px; border: 1px solid rgba(170,145,201,.2); border-radius: 50%; background: radial-gradient(circle, rgba(170,145,201,.12), transparent 60%); }.orbit { position: absolute; border: 1px solid rgba(170,145,201,.38); border-radius: 50%; }.orbit-dashed { inset: 0; border-style: dashed; border-color: rgba(170,145,201,.25); transform: rotate(18deg); }.orbit-dashed span { position: absolute; top: 14px; left: 50%; transform: translateX(-50%) rotate(-18deg); color: var(--audit-muted); font: 8px/1.4 var(--observatory-font-mono); letter-spacing: .14em; text-align: center; }.orbit-inner { inset: 53px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-color: rgba(170,145,201,.6); box-shadow: 0 0 35px rgba(170,145,201,.1); }.orbit-inner strong { color: var(--audit-purple); font: 400 35px var(--observatory-font-display); letter-spacing: -.06em; }.orbit-inner small { margin-top: 5px; color: var(--audit-muted); font: 8px var(--observatory-font-mono); letter-spacing: .14em; }.ray { position: absolute; top: 50%; width: 27px; height: 1px; background: var(--audit-purple); }.ray-left { left: -20px; }.ray-right { right: -20px; }
  .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding-top: 25px; padding-bottom: 42px; }.metrics > div { min-height: 135px; padding: 17px 18px; border: 1px solid var(--observatory-line); background: rgba(17,24,23,.68); }.metrics span { display: block; color: var(--audit-muted); font: 700 9px var(--observatory-font-mono); letter-spacing: .15em; text-transform: uppercase; }.metrics strong { display: block; margin-top: 25px; color: var(--audit-ink); font: 400 29px var(--observatory-font-display); letter-spacing: -.05em; }.metrics small { display: block; margin-top: 5px; color: var(--audit-muted); font: 10px var(--observatory-font-body); }.metrics .healthy strong { color: var(--audit-green); }.metrics .warning strong { color: var(--audit-warning); }
  .finding-grid { display: grid; grid-template-columns: 1.18fr .82fr; gap: 12px; }.panel { padding: 25px; border: 1px solid var(--observatory-line); background: rgba(17,24,23,.7); }.panel-head, .register-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; }.panel-head > span, .register-head > small { color: var(--audit-muted); font: 9px var(--observatory-font-mono); letter-spacing: .12em; }.eyebrow { color: var(--audit-muted); font: 700 9px var(--observatory-font-mono); letter-spacing: .15em; text-transform: uppercase; }.panel h2, .register h2 { margin: 8px 0 0; font: 400 27px/1 var(--observatory-font-display); letter-spacing: -.045em; }.intro { max-width: 470px; margin: 20px 0 25px; color: var(--audit-muted); font: 12px/1.6 var(--observatory-font-body); }.finding-list { display: grid; gap: 23px; }.finding { display: grid; grid-template-columns: 33px minmax(0,1fr) auto; align-items: start; gap: 13px; }.finding > b { display: grid; place-items: center; width: 28px; height: 28px; color: var(--audit-purple); background: rgba(170,145,201,.1); border: 1px solid rgba(170,145,201,.25); font: 10px var(--observatory-font-mono); }.finding > b.amber, .finding mark.amber { color: var(--audit-warning); border-color: rgba(181,165,210,.32); background: rgba(181,165,210,.08); }.finding-title { display: flex; align-items: center; flex-wrap: wrap; gap: 9px; }.finding h3, .step h3 { margin: 1px 0 0; font: 600 13px var(--observatory-font-body); }.finding mark, .table-shell mark { padding: 4px 7px; color: var(--audit-purple); border: 1px solid rgba(170,145,201,.25); background: rgba(170,145,201,.08); font: 8px var(--observatory-font-mono); letter-spacing: .08em; text-transform: uppercase; }.finding p, .step p { margin: 7px 0 10px; color: var(--audit-muted); font: 11px/1.5 var(--observatory-font-body); }.bar { height: 3px; background: rgba(232,224,207,.08); }.bar i { display: block; height: 100%; background: var(--audit-purple); box-shadow: 0 0 11px rgba(170,145,201,.6); }.bar i.amber { background: var(--audit-warning); box-shadow: none; }.finding > strong { color: var(--audit-ink); font: 400 25px var(--observatory-font-display); white-space: nowrap; }.finding > strong small { color: var(--audit-muted); font-size: 11px; }.sequence { min-height: 330px; }.step { display: grid; grid-template-columns: 28px 1fr; gap: 12px; margin-top: 31px; }.step > b { display: grid; place-items: center; width: 27px; height: 27px; border-radius: 50%; color: var(--audit-purple); border: 1px dashed rgba(170,145,201,.5); font: 9px var(--observatory-font-mono); }.step > b.done { color: var(--audit-green); border-style: solid; border-color: rgba(136,182,166,.4); }.connector { width: 1px; height: 30px; margin: -4px 0 -4px 13px; background: linear-gradient(var(--audit-green), var(--audit-purple)); opacity: .5; }
  .register { padding-top: 80px; padding-bottom: 74px; }.register h2 { font-size: 31px; }.register-head > small { margin-top: 25px; }.toolbar { display: flex; justify-content: space-between; gap: 18px; margin: 27px 0 12px; }.toolbar label { display: flex; align-items: center; gap: 8px; width: min(350px, 100%); border-bottom: 1px solid rgba(170,145,201,.38); color: var(--audit-muted); }.toolbar input { width: 100%; height: 35px; border: 0; outline: 0; background: transparent; color: var(--audit-ink); font: 11px var(--observatory-font-body); }.toolbar input::placeholder { color: #777880; }.filters { display: flex; gap: 2px; }.filters button { padding: 7px 11px; border: 1px solid var(--observatory-line); background: transparent; color: var(--audit-muted); font: 10px var(--observatory-font-body); cursor: pointer; }.filters button:hover, .filters button.active { color: var(--audit-ink); border-color: rgba(170,145,201,.42); background: rgba(170,145,201,.1); }.table-shell { overflow-x: auto; border: 1px solid var(--observatory-line); }.table-shell table { width: 100%; min-width: 700px; border-collapse: collapse; text-align: left; }.table-shell th { padding: 13px 15px; color: var(--audit-muted); background: rgba(232,224,207,.025); font: 700 9px var(--observatory-font-mono); letter-spacing: .12em; text-transform: uppercase; }.table-shell td { padding: 16px 15px; border-top: 1px solid var(--observatory-line); color: var(--audit-muted); font: 11px var(--observatory-font-body); }.table-shell td strong { color: var(--audit-ink); font-weight: 600; }.finding-chip { display: inline-block; max-width: 240px; padding: 4px 7px; border: 1px solid var(--observatory-line); color: var(--audit-muted); font: 8px/1.35 var(--observatory-font-mono); text-transform: uppercase; }.status { display: inline-flex; align-items: center; gap: 7px; color: var(--audit-green); font: 10px var(--observatory-font-body); }.status.review { color: var(--audit-warning); }.status i { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }.empty { padding: 28px; color: var(--audit-muted); text-align: center; }.table-note { margin: 13px 0 0; color: var(--audit-muted); font: 10px var(--observatory-font-body); }.method { display: grid; grid-template-columns: .9fr 1.1fr; gap: 8%; padding-top: 62px; padding-bottom: 78px; border-top: 1px solid var(--observatory-line); }.method h2 { margin: 16px 0; font: 400 clamp(40px, 4.4vw, 59px)/.92 var(--observatory-font-display); letter-spacing: -.06em; }.method > div:first-child > p:last-child { max-width: 360px; color: var(--audit-muted); font: 12px/1.65 var(--observatory-font-body); }.method-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; padding-top: 13px; }.method-grid > div { padding-top: 13px; border-top: 1px solid rgba(170,145,201,.35); }.method-grid span { color: var(--audit-purple); font: 10px var(--observatory-font-mono); }.method-grid h3 { margin: 22px 0 8px; font: 600 12px var(--observatory-font-body); }.method-grid p { margin: 0; color: var(--audit-muted); font: 10px/1.55 var(--observatory-font-body); }
  @media (max-width: 760px) { .audit-hero { display: block; padding-top: 55px; }.coverage-orbit { width: 190px; height: 190px; margin: 45px auto 0; }.orbit-inner { inset: 40px; }.orbit-inner strong { font-size: 29px; }.metrics { grid-template-columns: 1fr 1fr; gap: 8px; padding-top: 18px; padding-bottom: 30px; }.metrics > div { min-height: 123px; padding: 14px; }.metrics strong { margin-top: 19px; font-size: 25px; }.finding-grid, .method { grid-template-columns: 1fr; }.panel { padding: 19px; }.register { padding-top: 55px; padding-bottom: 52px; }.toolbar { display: grid; }.method { gap: 40px; padding-top: 49px; }.method-grid { gap: 14px; }.wrap { padding-left: 18px; padding-right: 18px; } }
  @media (max-width: 420px) { .metrics { grid-template-columns: 1fr; }.meta { flex-wrap: wrap; }.method-grid { grid-template-columns: 1fr; gap: 24px; }.method-grid h3 { margin-top: 12px; } }
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; } }
</style>
