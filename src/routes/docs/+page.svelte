<script>
  import Footer from '$lib/components/Footer.svelte';

  /** @type {{ data: { docs: { slug: string, title: string, description: string }[] } }} */
  let { data } = $props();

  const nodeColors = [
    'var(--purple)',
    'var(--blue)',
    'var(--gold)',
    'var(--green)',
    'var(--pink)',
    'var(--silver)'
  ];
</script>

<svelte:head>
  <title>The Archive — TerAustralis Incognita</title>
  <meta
    name="description"
    content="The living archive of TerAustralis Incognita — the Codex, the Apocryphon, architecture, governance, and every document that shapes the vision."
  />
</svelte:head>

<section class="hero node" style="--node:var(--gold)">
  <div class="eyebrow">TerAustralis Incognita · The Archive</div>
  <h1>The Archive</h1>
  <p class="lede">
    Every document that shapes the vision, rendered live from the source. Read the mythos, the
    architecture, and the working method — straight from the repository.
  </p>
</section>

<section class="section node" style="--node:var(--blue)">
  {#each data.docs as doc, i (doc.slug)}
    <a class="codexlink" href={`/docs/${doc.slug}`} style={`--tc:${nodeColors[i % nodeColors.length]}`}>
      <strong>{doc.title}</strong>
      {#if doc.description}
        <span>{doc.description}</span>
      {/if}
      <span>→ Read {doc.title}</span>
    </a>
  {/each}
</section>

<Footer showVoices showCode />
