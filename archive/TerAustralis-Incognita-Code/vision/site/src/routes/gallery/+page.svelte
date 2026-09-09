<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { onMount } from 'svelte';

  let { data } = $props();
  let selectedImage = $state(null);

  onMount(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') selectedImage = null;
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  });

  function nextImage() {
    if (!selectedImage) return;
    const idx = data.images.findIndex(img => img.filename === selectedImage.filename);
    if (idx < data.images.length - 1) {
      selectedImage = data.images[idx + 1];
    }
  }

  function prevImage() {
    if (!selectedImage) return;
    const idx = data.images.findIndex(img => img.filename === selectedImage.filename);
    if (idx > 0) {
      selectedImage = data.images[idx - 1];
    }
  }
</script>

<svelte:head>
  <title>Art Gallery - TerAustralis Incognita</title>
</svelte:head>

<div class="gallery-container">
  <section class="gallery-hero">
    <h1>Mythos Art</h1>
    <p>Visual canon of the TerAustralis Incognita universe. {data.images.length}+ pieces from the Crystal universe.</p>
    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.7;">
      Content licensed CC BY-NC-ND 4.0. Where a real person's likeness appears, it is Vision-layer storytelling and AI-generated fan art only.
    </div>
  </section>

  <div class="gallery-grid">
    {#each data.images as image}
      <button class="gallery-item" onclick={() => (selectedImage = image)} type="button">
        {#if image.type === 'video'}
          <!-- preload="metadata" renders the first frame, so no poster file is needed -->
          <video src={image.url} muted playsinline preload="metadata"></video>
          <span class="media-badge" aria-hidden="true">▶</span>
        {:else}
          <img
            src={image.url}
            alt={image.description}
            loading="lazy"
          />
        {/if}
        <div class="gallery-overlay">
          <p>{image.description}</p>
        </div>
      </button>
    {/each}
  </div>
</div>


{#if selectedImage}
  <div class="lightbox-modal" onclick={() => (selectedImage = null)} role="dialog" aria-modal="true" tabindex="-1">
    <div class="lightbox-content" onclick={e => e.stopPropagation()} role="none">
      <button class="lightbox-close" onclick={() => (selectedImage = null)}>×</button>
      <button class="lightbox-prev" onclick={prevImage}>←</button>
      {#if selectedImage.type === 'video'}
        <!-- svelte-ignore a11y_media_has_caption -->
        <video src={selectedImage.url} controls autoplay loop muted playsinline></video>
      {:else}
        <img src={selectedImage.url} alt={selectedImage.description} />
      {/if}
      <button class="lightbox-next" onclick={nextImage}>→</button>
      <p class="lightbox-description">{selectedImage.description}</p>
    </div>
  </div>
{/if}

<style>
  .gallery-container {
    padding: 2rem 1rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  .gallery-hero {
    text-align: center;
    margin-bottom: 3rem;
  }

  .gallery-hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-family: 'Playfair Display', serif;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .gallery-hero p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 1rem;
  }

  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .gallery-item {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    cursor: pointer;
    aspect-ratio: 1;
    background: linear-gradient(135deg, rgba(167, 139, 250, 0.1), rgba(122, 162, 255, 0.1));
    border: 1px solid rgba(233, 187, 95, 0.2);
    transition: all 0.3s ease;
    padding: 0;
    font: inherit;
  }

  .gallery-item:hover {
    transform: scale(1.02);
    border-color: rgba(233, 187, 95, 0.6);
    box-shadow: 0 0 20px rgba(233, 187, 95, 0.3);
  }

  .gallery-item img,
  .gallery-item video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: opacity 0.3s ease;
  }

  .media-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 2;
    display: grid;
    place-items: center;
    width: 30px;
    height: 30px;
    padding-left: 2px;
    border-radius: 50%;
    border: 1px solid var(--line);
    background: rgba(0, 0, 0, 0.6);
    color: var(--ink);
    font-size: 0.7rem;
    pointer-events: none;
  }

  .gallery-item:hover img,
  .gallery-item:hover video {
    opacity: 0.7;
  }

  .gallery-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .gallery-item:hover .gallery-overlay {
    opacity: 1;
  }

  .gallery-overlay p {
    color: var(--gold);
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.4;
  }

  .lightbox-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .lightbox-content {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 90vw;
    max-height: 90vh;
  }

  .lightbox-content img,
  .lightbox-content video {
    max-width: 100%;
    max-height: 70vh;
    object-fit: contain;
    border-radius: 8px;
  }

  .lightbox-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: var(--gold);
    font-size: 2rem;
    cursor: pointer;
    z-index: 10;
    transition: color 0.2s;
  }

  .lightbox-close:hover {
    color: var(--ink);
  }

  .lightbox-prev,
  .lightbox-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(167, 139, 250, 0.3);
    border: 1px solid rgba(233, 187, 95, 0.4);
    color: var(--gold);
    font-size: 2rem;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: all 0.2s;
  }

  .lightbox-prev:hover,
  .lightbox-next:hover {
    background: rgba(167, 139, 250, 0.6);
    border-color: var(--gold);
  }

  .lightbox-prev {
    left: 1rem;
  }

  .lightbox-next {
    right: 1rem;
  }

  .lightbox-description {
    position: absolute;
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    background: rgba(0, 0, 0, 0.9);
    color: var(--gold);
    padding: 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    line-height: 1.5;
    max-width: 600px;
  }

  @media (max-width: 720px) {
    .gallery-grid {
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }

    .gallery-hero h1 {
      font-size: 2rem;
    }

    .lightbox-prev,
    .lightbox-next {
      font-size: 1.5rem;
      padding: 0.25rem 0.75rem;
    }
  }
</style>
