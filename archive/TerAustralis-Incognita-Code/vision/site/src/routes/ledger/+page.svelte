<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { entries } from '$lib/data/ledger.js';

  /**
   * Ids of embeds the reader has explicitly asked to load. Nothing is requested
   * from a third party until an id lands in here.
   * @type {string[]}
   */
  let loaded = $state([]);

  /** @param {string} id */
  function play(id) {
    if (!loaded.includes(id)) loaded = [...loaded, id];
  }
</script>

<svelte:head>
  <title>The Journey Ledger — TerAustralis Incognita</title>
  <meta
    name="description"
    content="Creative footprints that predate TerAustralis Incognita — live performance in South-Western Sydney, short-form work, and industrial years in the west. Marked history, confirmed or unconfirmed, rather than lost fragments."
  />
</svelte:head>

<article class="page node" style="--node:var(--silver)">
  <div class="eyebrow">Before first light · Archives & footprints</div>
  <h1>The Journey Ledger</h1>
  <p class="attribution">
    The work that came before this work. Singing in South-Western Sydney, short-form
    fragments, industrial years in the west — kept here deliberately, because a prologue you
    name is worth more than one you leave scattered.
  </p>

  <section class="chapter node" style="--node:var(--purple)">
    <h2>Why this page exists</h2>
    <p>
      The dated commit record in the <a href="/docs">Archive</a> opens on 14 July 2026 — first
      light, the oldest commit anywhere in the portfolio. This page is what precedes it.
    </p>
    <p>
      Some of this material sits on accounts I no longer hold the keys to. That is ordinary —
      emails change, phases of life end, and the login goes with them. It is not a reason to
      disown the work. This page is the canonical record: <strong>the account is where a thing
      was published; this ledger is where it is claimed.</strong>
    </p>
    <p>
      The same rule governs this page as governs the rest of the project. Every entry is marked
      either <strong>confirmed</strong> — the link has been checked and points at the right
      recording — or <strong>unconfirmed</strong>. Nothing is embedded, and nothing is presented
      as evidence, until it has been checked. A dreamed line never gets to wear the costume of a
      surveyed one, and that includes lines about my own history.
    </p>
  </section>

  {#each entries as entry (entry.id)}
    <section class="chapter node" id={entry.id} style="--node:{entry.colour}">
      <h2>{entry.title}</h2>
      <p class="ledger-meta">
        {entry.era} · {entry.place} · {entry.platform}
      </p>

      {#if entry.verified && entry.youtubeId}
        {#if loaded.includes(entry.id)}
          <div class="embed">
            <iframe
              src="https://www.youtube-nocookie.com/embed/{entry.youtubeId}?autoplay=1&rel=0"
              title={entry.title}
              loading="lazy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              referrerpolicy="strict-origin-when-cross-origin"
              allowfullscreen
            ></iframe>
          </div>
        {:else}
          <button class="embed facade" type="button" onclick={() => play(entry.id)}>
            <span class="glyph" aria-hidden="true">▶</span>
            <span class="label">Play “{entry.title}”</span>
            <span class="fineprint">
              Loads from YouTube on youtube-nocookie.com. Nothing is requested until you press
              this.
            </span>
          </button>
        {/if}
      {/if}

      <p>{entry.body}</p>

      {#if entry.verified && entry.url}
        <p class="ledger-status confirmed">
          Confirmed · <a href={entry.url} target="_blank" rel="noopener noreferrer"
            >watch on {entry.platform}</a
          >
        </p>
      {:else}
        <p class="ledger-status pending">Unconfirmed — no link published yet</p>
      {/if}
    </section>
  {/each}

  <section class="chapter node" style="--node:var(--green)">
    <h2>Where the thread continues</h2>
    <p>
      From stages and short-form video to sovereign, local-first systems written largely from a
      phone. Different medium, same instinct: build the thing yourself, keep it in your own
      hands, and be straight about what it is.
    </p>
    <p>
      The recordings this project has made since are catalogued on <a href="/music">The Music</a>
      and hashed into the <a href="/provenance">Bitcoin-anchored manifest</a> — the same argument
      about not leaving your work in someone else's hands, applied forward instead of backward.
      The current work lives in <a href="/codex">the Codex</a>, in
      <a href="/clementine">Clementine</a>, and in the <a href="/docs">Archive</a>. The live
      thread runs through
      <a href="https://x.com/m13crystalat" target="_blank" rel="me noopener noreferrer"
        ><strong>@M13CrystalAT on X</strong></a
      >.
    </p>
  </section>
</article>


<style>
  .ledger-meta {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 10px;
  }

  .ledger-status {
    font-size: 0.76rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 16px;
  }
  .ledger-status.confirmed {
    color: var(--green);
  }
  .ledger-status.pending {
    color: var(--gold);
  }

  .embed {
    display: block;
    width: 100%;
    margin-top: 24px;
    aspect-ratio: 16 / 9;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 16px;
    overflow: hidden;
  }
  .embed iframe {
    width: 100%;
    height: 100%;
    border: 0;
    display: block;
  }

  .facade {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 24px;
    text-align: center;
    color: var(--ink);
    font: inherit;
    cursor: pointer;
    transition:
      border-color 0.18s ease,
      box-shadow 0.18s ease;
  }
  .facade:hover {
    border-color: var(--pink);
    box-shadow: 0 0 20px rgba(255, 174, 224, 0.14);
  }
  .facade .glyph {
    font-size: 1.6rem;
    color: var(--pink);
  }
  .facade .label {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 1.12rem;
  }
  .facade .fineprint {
    color: var(--muted);
    font-size: 0.82rem;
    max-width: 44ch;
  }
</style>
