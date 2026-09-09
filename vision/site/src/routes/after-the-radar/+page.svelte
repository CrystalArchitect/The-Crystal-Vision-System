<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { getDoc, renderMarkdown } from '$lib/docs.js';
  const doc = getDoc('after-the-radar');
  if (!doc) throw new Error('Missing after-the-radar document');
  const html = renderMarkdown(doc.raw);
</script>

<svelte:head>
  <title>{doc.title} — TerAustralis Incognita</title>
  {#if doc.description}
    <meta name="description" content={doc.description} />
  {/if}
  <meta property="og:title" content="{doc.title} — TerAustralis Incognita" />
</svelte:head>

<article class="page node" style="--node:var(--blue)">
  <div class="eyebrow">Publish · SpaceNews opinion · available surface</div>
  <div class="markdown">
    {@html html}
  </div>
  <p class="attribution">
    Also filed in <a href="/docs/after-the-radar">The Archive</a>. Built claim boundary: strategic opinion, not a funded programme.
  </p>
</article>

<style>
  .markdown {
    color: var(--ink);
    -webkit-text-fill-color: var(--ink);
    line-height: 1.7;
    font-size: 1.02rem;
  }
  .markdown :global(h1),
  .markdown :global(h2),
  .markdown :global(h3),
  .markdown :global(h4) {
    font-family: var(--font-display);
    line-height: 1.25;
    margin: 2rem 0 0.75rem;
    color: var(--ink);
    -webkit-text-fill-color: var(--ink);
    background: none;
    text-shadow: none;
    text-wrap: balance;
  }
  .markdown :global(h1) {
    font-size: clamp(2rem, 5vw, 3rem);
    margin-top: 0;
  }
  .markdown :global(h2) {
    font-size: clamp(1.4rem, 3vw, 1.9rem);
  }
  .markdown :global(p),
  .markdown :global(ul),
  .markdown :global(ol),
  .markdown :global(blockquote),
  .markdown :global(table) {
    margin: 0 0 1.1rem;
  }
  .markdown :global(a) {
    color: var(--gold);
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .markdown :global(blockquote) {
    border-left: 3px solid var(--blue);
    padding: 0.25rem 0 0.25rem 1rem;
    color: var(--muted);
    font-style: italic;
  }
  .attribution {
    margin-top: 2.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--line);
  }
</style>
