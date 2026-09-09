<script>
  import Footer from '$lib/components/Footer.svelte';

  /** @type {{ data: { slug: string, title: string, description: string, html: string } }} */
  let { data } = $props();
</script>

<svelte:head>
  <title>{data.title} — TerAustralis Incognita</title>
  {#if data.description}
    <meta name="description" content={data.description} />
  {/if}
</svelte:head>

<section class="hero node" style="--node:var(--purple)">
  <div class="eyebrow"><a href="/docs">The Archive</a> · TerAustralis Incognita</div>
</section>

<section class="section node" style="--node:var(--blue)">
  <!-- Content is authored in-repo and trusted. -->
  <article class="markdown">
    {@html data.html}
  </article>

  <p class="backlink">
    <a class="btn btn-ghost" href="/docs">← Back to the Archive</a>
  </p>
</section>

<Footer showVoices showCode />

<style>
  .markdown {
    color: var(--ink, #e9e6ff);
    line-height: 1.7;
    font-size: 1.02rem;
  }

  .markdown :global(h1),
  .markdown :global(h2),
  .markdown :global(h3),
  .markdown :global(h4) {
    font-family: var(--font-display, Georgia, serif);
    line-height: 1.25;
    margin: 2rem 0 0.75rem;
    color: var(--ink, #fff);
    text-wrap: balance;
  }

  .markdown :global(h1) {
    font-size: clamp(1.9rem, 4vw, 2.6rem);
    margin-top: 0;
  }

  .markdown :global(h2) {
    font-size: clamp(1.4rem, 3vw, 1.8rem);
  }

  .markdown :global(h3) {
    font-size: 1.2rem;
  }

  .markdown :global(p),
  .markdown :global(ul),
  .markdown :global(ol),
  .markdown :global(blockquote),
  .markdown :global(table) {
    margin: 0 0 1.1rem;
  }

  .markdown :global(a) {
    color: var(--gold, #ffd479);
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .markdown :global(img) {
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }

  .markdown :global(blockquote) {
    border-left: 3px solid var(--purple, #9b8cff);
    padding: 0.25rem 0 0.25rem 1rem;
    color: var(--muted, #b9b4d8);
    font-style: italic;
  }

  .markdown :global(code) {
    font-family: var(--font-mono, ui-monospace, monospace);
    font-size: 0.9em;
    background: rgba(255, 255, 255, 0.08);
    padding: 0.15em 0.4em;
    border-radius: 6px;
  }

  .markdown :global(pre) {
    background: rgba(10, 8, 24, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    overflow-x: auto;
    margin: 0 0 1.1rem;
  }

  .markdown :global(pre code) {
    background: none;
    padding: 0;
  }

  .markdown :global(table) {
    width: 100%;
    border-collapse: collapse;
    display: block;
    overflow-x: auto;
  }

  .markdown :global(th),
  .markdown :global(td) {
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 0.5rem 0.75rem;
    text-align: left;
  }

  .markdown :global(th) {
    background: rgba(255, 255, 255, 0.06);
  }

  .markdown :global(hr) {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    margin: 2rem 0;
  }

  .backlink {
    margin-top: 2rem;
  }
</style>
