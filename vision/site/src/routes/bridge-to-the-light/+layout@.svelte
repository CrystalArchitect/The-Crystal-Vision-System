<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<!-- Breaks out of the site chrome. The hush is a single page, not a node
     in the header or the constellation. Seven lights stay seven. -->
<script>
  /** @type {{ children: import('svelte').Snippet }} */
  let { children } = $props();
</script>

{@render children()}
