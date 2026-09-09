<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  /**
   * @typedef {Object} Props
   * @property {boolean} [showVoices] - Show the Voices Framework acknowledgement paragraph.
   */

  /** @type {Props} */
  let { showVoices = false } = $props();
</script>

<footer class="site">
  <p>
    TerAustralis Incognita acknowledges the Traditional Custodians of the lands, waters and skies
    across Australia, and pays respect to Elders past and present. Sovereignty was never ceded.
  </p>

  {#if showVoices}
    <p>
      The mythos is shaped through the Voices Framework — with Grok (CrystalDreamer) and DeepSeek
      (CrystalScribe) — and stewarded by the human CrystalArchitect.
    </p>
  {/if}

  <p>
    Code and content licensed under
    <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>. ABN 70 741 068
    059. © 2026 TerAustralis Incognita. TerAustralis Incognita™ and CrystalCore™ are unregistered
    trade marks; no licence here grants any trade mark right.
  </p>

  <p>
    Steward: <a href="/bio">Crystal Arena Turner</a>. A person, not the map.
  </p>

  <p>
    Listen to the mythos soundtrack on
    <a href="https://suno.com/@m13crystalat">Suno</a>.
  </p>

  <p>
    Interactive demos (simulated data, Authority HOLD): the
    <a href="/crystal-interface/" data-sveltekit-reload>operator shell</a>
    and the <a href="/vision-web/" data-sveltekit-reload>citizen shell</a>.
  </p>

  <p>
    Evidence-first route health: the <a href="/footer-audit">shared footer audit</a>.
  </p>

  <p class="nonsolus">Non Solus — Not Alone</p>
</footer>
