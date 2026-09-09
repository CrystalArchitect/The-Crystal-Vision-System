<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>

  /** @type {{ data: { tracks: any[] } }} */
  let { data } = $props();
</script>

<svelte:head>
  <title>The Music — TerAustralis Incognita</title>
  <meta
    name="description"
    content="The recordings of the TerAustralis Incognita mythos — preserved in the repository, catalogued with honest labels, and anchored to Bitcoin. Nineteen recordings; four canon works."
  />
</svelte:head>

<article class="page node" style="--node:var(--pink)">
  <div class="eyebrow">Preserved · catalogued · anchored</div>
  <h1>The Music</h1>
  <p class="attribution">
    Audio of the mythos — the canon works, and recordings that are not canon and are marked so.
    Generated with Suno; lyrics for the canon works are human-written and credited on their pages.
  </p>

  <section class="chapter node" style="--node:var(--pink)">
    <h2>Why the recordings live in the repository</h2>
    <p>
      Until 31 July 2026 the music was the only kind of work in this project held in exactly one
      place, by a third party — a lapsed subscription or a changed platform policy away from being
      lost. Now every recording the canon names is held in
      <a
        href="https://github.com/CrystalArchitect/TerAustralis-Incognita/tree/main/mythos/music"
        target="_blank"
        rel="noopener noreferrer">the public repository</a
      >, hashed file by file, and covered by the project's
      <a href="/provenance">Bitcoin-anchored manifest</a> — along with twelve recordings the canon does
      not name, kept for the same reason and labelled as exactly what they are.
    </p>
    <p>
      The canon names four works: the three ignition songs written across the sky in The First
      Remembering, and Wire Skull Memory, which its own page marks as standalone. Being preserved
      here is not what makes a work canon — a work enters the canon by being written into it, and
      that is the maintainer's decision, not a consequence of a file being backed up.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--blue)">
    <h2>The catalogue</h2>
    <p>
      One row per <em>recording</em>, not per song — Shooting Star Girl has two takes, generated
      nearly three months apart, and which take is the song is a question the catalogue leaves
      honestly open. Every length, timestamp and plan label below mirrors the
      <a
        href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/music/README.md"
        target="_blank"
        rel="noopener noreferrer">catalogue of record</a
      >, where each fact was read from the file's own ID3 tag.
    </p>
    <div class="tracktable-scroll">
      <table class="tracktable">
        <thead>
          <tr><th>Work</th><th>Canon status</th><th>Length</th><th>Generated</th><th>Plan when generated</th></tr>
        </thead>
        <tbody>
          {#each data.tracks as t (t.work + t.generated)}
            <tr class:removed={t.removed}>
              <td>
                {#if t.url}
                  <a href={t.url} target="_blank" rel="noopener noreferrer">{t.work}</a>
                {:else}
                  {t.work}
                {/if}
              </td>
              <td>{t.canon}</td>
              <td>{t.length}</td>
              <td>{t.generated}</td>
              <td>{t.plan}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <p class="attribution">
      Each linked title opens the audio file in the repository. The commercially-licensed
      recordings are also on
      <a href="https://suno.com/@m13crystalat" target="_blank" rel="noopener noreferrer">Suno</a>;
      the platform copies of the non-commercial ones were deleted by the maintainer on 8 August
      2026, so for those the repository copy is the only copy in existence — hashed, dated, and
      anchored.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>Rights, split by a date</h2>
    <p>
      Suno's free tier grants non-commercial use only; paid plans grant commercial rights. The same
      audio file carries different rights depending on the plan running when it was generated — so
      the catalogue records the plan for every row, and the dates are settled by Apple's own
      receipts: the Pro subscription began <strong>7 May 2026</strong> (the receipt reads
      &ldquo;Init.&nbsp;Subscription&rdquo; — a first charge, not a renewal) and ended
      <strong>6 June 2026</strong>.
    </p>
    <p>
      The subscription later resumed, and the renewal receipt of 8 August 2026 precedes the nine
      recordings generated that evening and the first minutes of the next day (UTC) in any
      Australian timezone. That splits the nineteen
      recordings cleanly: <strong>twelve carry commercial rights</strong> — three from the first Pro
      period (Wire Skull Memory, Fermi's Silent Line, Safari Chains) and the nine August
      recordings from the resumed plan — and <strong>seven are non-commercial</strong>: the two
      earliest recordings predate the first plan, and everything from July was generated after it
      ended. Nothing about preservation changes; what changes is what may be done with them.
    </p>
    <p>
      Beneath all of it sits a plainer fact the catalogue states outright: model-generated audio may
      attract no copyright at all, since copyright generally requires a human author. What cannot be
      copied by copying a file is the canon these songs belong to.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--silver)">
    <h2>One recording was removed</h2>
    <p>
      A recording titled <em>Look What You Made Me Do</em> was removed from the tree on
      31 July 2026, the day the maintainer listened and confirmed it relates to the 2017 song of the
      same name. This repository asserts a Creative Commons licence over its audio, and that grant is
      not the maintainer's to make over someone else's composition. The catalogue row and a dated
      truth label stay — a record that loses its own history is not a record — and git history was
      deliberately not rewritten.
    </p>
  </section>

  <nav class="pagenav" aria-label="Continue">
    <a href="/provenance">How the anchor works →</a>
    <a href="/gallery">See the gallery →</a>
    <a href="/">← Home</a>
  </nav>
</article>


<style>
  .tracktable-scroll {
    overflow-x: auto;
    margin: 22px 0;
  }
  .tracktable {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
  }
  .tracktable th {
    text-align: left;
    color: var(--muted);
    font-size: 0.8rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 8px 14px 8px 0;
    border-bottom: 1px solid color-mix(in srgb, var(--muted) 30%, transparent);
  }
  .tracktable td {
    padding: 9px 14px 9px 0;
    border-bottom: 1px solid color-mix(in srgb, var(--muted) 14%, transparent);
    vertical-align: top;
  }
  .tracktable tr.removed td {
    color: var(--muted);
    font-style: italic;
  }
</style>
