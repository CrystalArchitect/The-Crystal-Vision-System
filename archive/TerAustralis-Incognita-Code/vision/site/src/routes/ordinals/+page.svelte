<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->


<svelte:head>
  <title>The Ordinals Collection — TerAustralis Incognita</title>
  <meta
    name="description"
    content="Mythos art from TerAustralis Incognita, inscribed on-chain as Ordinals by @pacartcollect under a separate licence grant. The project issues no token."
  />
</svelte:head>

<article class="page node" style="--node:var(--gold)">
  <div class="eyebrow">Third-party work · licensed</div>
  <h1>The Ordinals Collection</h1>
  <p class="attribution">
    Inscribed and offered by <a href="https://x.com/pacartcollect" target="_blank" rel="noopener noreferrer">@pacartcollect</a>,
    under a written licence grant from the copyright holder.
  </p>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>Where to find it</h2>
    <dl class="collection-facts">
      <dt>Collection</dt>
      <dd>TerAustralis Incognita Mythos Art</dd>
      <dt>Chain</dt>
      <dd>BSV — inscribed as Ordinals, not on BTC</dd>
      <dt>Platform</dt>
      <dd>3dordi</dd>
      <dt>Credited to</dt>
      <dd>Crystal Arena-Turner — TerAustralis Incognita</dd>
    </dl>
    <p>
      <a
        class="btn btn-primary"
        href="https://3dordi.io/collection/cc35f9a95773d2f97328ccb33c582d1f853e7856c47397751a06a0e910da8086_0"
        target="_blank"
        rel="noopener noreferrer">View the collection on 3dordi →</a>
    </p>
    <p class="attribution">
      This is the one authorised collection. The artist credit follows the licence grant, which
      requires every inscription and listing to name Crystal Arena-Turner — it records who made the
      art, not who is selling it.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>What this is</h2>
    <p>
      Pac is inscribing the TerAustralis Incognita mythos art on-chain as Ordinals, working through
      the collection in stages. Each inscription is a copy of an artwork from the
      <a href="/gallery">gallery</a>, credited to the artist and carrying its provenance.
    </p>
    <p>
      This is <strong>Pac's project, not the project's project</strong>. It is independent work by
      someone who liked the art enough to put it somewhere permanent, and it is listed here because
      the work is real and the permission is real — not because the project is selling anything.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--blue)">
    <h2>What it is not</h2>
    <ul>
      <li>
        <strong>Not a project token.</strong> TerAustralis Incognita issues no token, runs no sale,
        and holds no coin. It never has.
      </li>
      <li>
        <strong>Not an investment.</strong> Nothing here is a financial product or financial advice.
        Buying an inscription buys a copy of an artwork and nothing else.
      </li>
      <li>
        <strong>Not membership.</strong> Holding an inscription confers no right in the project, its
        software, its mythos, its governance, or any decision made about them.
      </li>
      <li>
        <strong>Not an endorsement of any marketplace.</strong> Where the inscriptions are listed and
        what they cost is entirely Pac's business.
      </li>
    </ul>
  </section>

  <section class="chapter node" style="--node:var(--purple)">
    <h2>The licence</h2>
    <p>
      The mythos art is published under
      <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" rel="noopener noreferrer">CC BY-NC-ND 4.0</a>,
      which permits neither commercial use nor derivatives. Inscribing artwork and selling it is
      commercial use, so it needed permission the public licence does not give.
    </p>
    <p>
      That permission was granted in writing, to Pac specifically, and is published in full:
      <a
        href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/governance/ORDINALS-LICENCE-GRANT.md"
        target="_blank"
        rel="noopener noreferrer">ORDINALS-LICENCE-GRANT.md</a>. It is non-exclusive, revocable, and
      covers the art only — not the writing, the code, or the names.
    </p>
    <p>
      <strong>The public licence is unchanged.</strong> No one else gains a commercial or derivative
      right from that grant. If you want to do something similar, ask first.
    </p>
    <p>
      Two pieces are excluded because they bear a real person's photographic likeness and carry a
      truth label for it. They are not licensed for inscription or sale.
    </p>
  </section>

  <nav class="pagenav" aria-label="Continue">
    <a href="/gallery">See the gallery →</a>
    <a href="/join">Ways to take part →</a>
    <a href="/">← Home</a>
  </nav>
</article>


<style>
  .collection-facts {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 10px 22px;
    margin: 22px 0 26px;
  }
  .collection-facts dt {
    color: var(--muted);
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .collection-facts dd {
    margin: 0;
  }
  @media (max-width: 520px) {
    .collection-facts {
      grid-template-columns: 1fr;
      gap: 2px 0;
    }
    .collection-facts dd {
      margin-bottom: 14px;
    }
  }
</style>
