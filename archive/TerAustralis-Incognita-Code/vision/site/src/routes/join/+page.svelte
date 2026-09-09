<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>

  let { data } = $props();
</script>

<svelte:head>
  <title>Join the Weave — TerAustralis Incognita</title>
</svelte:head>

<section class="section node" style="--node:var(--green)">
  <h2>Join the Weave</h2>
  <p>
    In the mythos, everyone who aligns with the Lattice is a <strong>Sovereign Vector</strong> —
    a node in the weave that answers from its own note, never governed by another. In plain terms:
    this is an open project, and you're welcome to add to it. The weave grows by real people making
    real work — art, music, code, writing — and keeping it their own.
  </p>
  <p style="font-size:.95rem;opacity:.75;margin-top:14px">
    "Sovereign Vector" is Vision-layer language; joining is a real, ordinary thing — contribute,
    connect, or support, through the channels below. Nothing here signs you up for anything, and
    nothing moves without your say.
  </p>
</section>

<section class="section node" style="--node:var(--blue)">
  <h2>Ways to take part</h2>
  <div class="cards">
    {#each data.ways as way (way.href)}
      <a class="card" href={way.href} style="--st:{way.st}" target="_blank" rel="noopener noreferrer">
        <h3>{way.title}</h3>
        <p>{way.body}</p>
        <span class="status">{way.cta}</span>
      </a>
    {/each}
  </div>
</section>

<section class="section node" style="--node:var(--gold)">
  <h2>Sovereign Vectors</h2>
  <p>
    The people whose work is woven in — credited by their own handle, for what they actually made.
    Listed with permission; being here implies no affiliation or endorsement, only credit.
  </p>
  <blockquote style="border-left:2px solid var(--gold);padding-left:20px;margin:18px 0;font-style:italic;opacity:.9">
    <p>
      "I'm running an open public-build project called CrystalCore.OS. It's a collaborative list
      and story where I invite people whose posts or work I respect and give them proper public
      credit by including their name. Everything stays fully theirs, consent is reversible at any
      time, and there is no money, work, or control involved."
    </p>
    <p style="font-style:normal;font-size:.9rem;opacity:.75">
      — the open invitation these credits answer, posted 2026-08-08. Each entry's dated yes and
      its evidence are recorded in the
      <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/content/SOVEREIGN-VECTORS.md"
         target="_blank" rel="noopener noreferrer">canon credit ledger</a>.
    </p>
  </blockquote>
  <div class="cards">
    {#each data.vectors as v (v.handle)}
      <a class="card" href={v.href} style="--st:{v.st}" target="_blank" rel="noopener noreferrer">
        <h3>{v.handle}</h3>
        <p>{v.work}</p>
      </a>
    {/each}
  </div>
  <p style="font-size:.95rem;opacity:.75;margin-top:22px">
    Want your name here? Add something to the weave and say so — you're credited by the handle you
    choose, for the work you made, and only if you want to be listed.
  </p>
</section>

<section class="section node" style="--node:var(--silver)">
  <h2>Influences</h2>
  <p>
    Work that shaped this one from a distance. Named in acknowledgement, not association — nobody
    listed here has been asked, none of them is involved in this project, and nothing they made is
    part of it. A sleeve note, not a credit.
  </p>
  <div class="cards">
    {#each data.influences as inf (inf.handle)}
      <a class="card" href={inf.href} style="--st:{inf.st}" target="_blank" rel="noopener noreferrer">
        <h3>{inf.handle}</h3>
        <p>{inf.work}</p>
      </a>
    {/each}
  </div>
</section>

