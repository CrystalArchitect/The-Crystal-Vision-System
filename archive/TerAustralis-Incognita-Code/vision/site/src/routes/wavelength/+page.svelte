<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<svelte:head>
  <title>Wavelength — TerAustralis Incognita</title>
  <meta
    name="description"
    content="Wavelength is an address. Telecom shares a strand; spectral combining shares an aperture. Coherent combining locks phase. Civilian optics core — Built claim, not Vision."
  />
  <meta property="og:title" content="Wavelength — TerAustralis Incognita" />
  <meta
    property="og:description"
    content="Colour vs phase. Both outrun a single fibre. Neither is a software patch."
  />
</svelte:head>

<article class="page node" style="--node:var(--green)">
  <div class="eyebrow">Optics · civilian core</div>
  <h1>Wavelength</h1>
  <p class="attribution">
    Built claim, not Vision. This page holds the civilian optics of spectral and coherent beam
    combining — wavelength as address, phase as lock. It is not a build sheet, not a weapons
    brief, and not a product page.
  </p>

  <section class="chapter node" style="--node:var(--green)">
    <h2>Wavelength is an address</h2>
    <p>
      Dense wavelength-division multiplexing (DWDM) uses many colours to share one fibre strand.
      Spectral beam combining (SBC) runs the same wavelength-to-angle physics in reverse: many
      channels into one free-space aperture. Address the spectrum; share the aperture.
    </p>
    <p>
      Wavelength is an address. Telecom uses it to share a strand. SBC uses it to share an
      aperture. Coherent beam combining (CBC) addresses with phase instead.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>Colour vs phase</h2>
    <p>
      <strong>SBC:</strong> different wavelengths, no phase lock. Beam quality can stay near one
      emitter. Losing a channel drops power; the far-field shape holds.
    </p>
    <p>
      <strong>CBC:</strong> same wavelength, active phase lock. Fields add as one wave. Power can
      scale with channel count; far-field peak can scale harder still if the aperture is used well —
      brightness scaling, not watt stacking. Filled aperture vs tiled aperture is an architecture
      choice, not a slogan.
    </p>
    <p>
      Both outrun a single fibre. Neither is a software patch.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--blue)">
    <h2>The tax is physical</h2>
    <p>
      SBC pays linewidth into divergence and M², thermal drift of centre wavelength, and heat on
      the combiner. CBC pays the phase servo and path match. The hard CBC tax is stimulated
      Brillouin scattering versus coherence: power wants a fat spectrum; interference wants a thin
      one. Coating absorption, substrate lensing, gain bandwidth — not a cloud API.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--silver)">
    <h2>Where the civilian core lives</h2>
    <p>
      Industrial cutting and welding past single-fibre nonlinear ceilings. Research ytterbium near
      1&nbsp;µm and thulium near 2&nbsp;µm. Pulsed CBC for LiDAR-class systems appears in the open
      literature. Defence high-energy laser programmes use the same combining <em>class</em> —
      that is a public fact. This page only holds the civilian optics core above.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>How to hold the chrome</h2>
    <p>
      Promo that dresses local-first constraints as a published defence node, or that says “bury
      fibre → future nodes,” skips multilayer dielectric gratings, thermal lensing, and M² under
      heat. Steal the constraint story — local-first, legacy iron, warm/cold weight split. Drop
      fake bylines and demonstrated dual-use product claims without public evidence.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>What this page does not say</h2>
    <ul>
      <li>
        <strong>It does not provide a weapons recipe.</strong> No HEL design, no build sheet, no
        step-by-step combining procedure.
      </li>
      <li>
        <strong>It does not endorse a product</strong> or invent affiliation with any vendor,
        lab, or programme beyond naming the public combining class.
      </li>
      <li>
        <strong>It does not claim a TerAustralis plant or berth</strong> for optics. Hold and
        Built claim only — not a deployment schedule.
      </li>
    </ul>
  </section>

  <section class="chapter node" style="--node:var(--green)">
    <h2>Record</h2>
    <ul>
      <li>
        DWDM as the telecom inverse analogy — many wavelengths share a strand; SBC shares an
        aperture with the same wavelength-to-angle physics run in reverse.
      </li>
      <li>
        Spectral combining families in the open literature: grating / volume Bragg / dichroic
        cascades — principle classes, not a shopping list.
      </li>
      <li>
        Coherent combining architectures in the open literature: filled vs tiled aperture; phase
        lock as the non-optional tax; SBS vs coherence as the power/coherence tension.
      </li>
      <li>
        Industrial multi-kW fibre systems and research CBC results are public; classified HEL
        recipes are not this page’s Record.
      </li>
    </ul>
    <p class="attribution" style="margin-top:1.5rem">
      Civilian core only. See also Analyst optics holds (SBC / CBC / AZUWAI) — not republished
      here as a build sheet.
    </p>
  </section>
</article>
