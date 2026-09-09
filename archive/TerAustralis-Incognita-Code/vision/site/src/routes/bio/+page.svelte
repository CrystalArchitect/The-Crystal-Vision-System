<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { profile, socials, groups } from '$lib/data/bio.js';

  const published = groups.find((g) => g.id === 'published');
  const rest = groups.filter((g) => g.id !== 'published');

  function isExternal(href) {
    return href.startsWith('http://') || href.startsWith('https://');
  }
</script>

<svelte:head>
  <title>Crystal Arena Turner — TerAustralis Incognita</title>
  <meta
    name="description"
    content="Crystal Arena Turner — steward of TerAustralis Incognita. Family first. Vision first. Proof later."
  />
  <meta property="og:title" content="Crystal Arena Turner — TerAustralis Incognita" />
  <meta
    property="og:description"
    content="A mother with a systems mind. Steward of this archive. A person, not the map."
  />
  <link rel="me" href="https://x.com/M13CrystalAT" />
  <link rel="me" href="https://github.com/CrystalArchitect" />
</svelte:head>

<article class="page node bio-page" style="--node:var(--purple)">
  <div class="eyebrow">Steward · a person, not the map</div>

  <div class="bio-hero">
    <img
      class="bio-avatar"
      src="/bio/avatar.jpg"
      alt="Portrait of Crystal Arena Turner"
      width="256"
      height="256"
    />
    <p class="bio-kicker">{profile.kicker}</p>
    <h1>
      Crystal<br /><em>Arena Turner</em>
    </h1>
    <p class="bio-handle">{profile.handle}</p>
    <p class="attribution">{profile.bio}</p>
    <p class="bio-place">{profile.location}</p>
    <nav class="bio-socials" aria-label="Social profiles">
      {#each socials as social (social.id)}
        <a
          href={social.href}
          rel={social.me ? 'me noopener noreferrer' : 'noopener noreferrer'}
          target="_blank">{social.label}</a
        >
      {/each}
    </nav>
  </div>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>Published</h2>
    <a class="pull" href={profile.quote.href} target="_blank" rel="noopener noreferrer">
      <p>{profile.quote.text}</p>
      <span>{profile.quote.cite} ↗</span>
    </a>
    <div class="cards bio-cards">
      {#each published.links as link (link.href)}
        <a
          class="card"
          href={link.href}
          style="--st:{link.st}"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h3>{link.title}</h3>
          <p>{link.body}</p>
          <span class="status">{link.cta}</span>
        </a>
      {/each}
    </div>
  </section>

  {#each rest as group (group.id)}
    <section class="chapter node" style="--node:{group.node}">
      <h2>{group.label}</h2>
      <div class="cards bio-cards">
        {#each group.links as link (link.href)}
          <a
            class="card"
            href={link.href}
            style="--st:{link.st}"
            {...isExternal(link.href)
              ? { target: '_blank', rel: 'noopener noreferrer' }
              : {}}
          >
            <h3>{link.title}</h3>
            <p>{link.body}</p>
            <span class="status">{link.cta}</span>
          </a>
        {/each}
      </div>
    </section>
  {/each}

  <section class="chapter node" style="--node:var(--silver)">
    <h2>Boundary</h2>
    <p>
      This page is a door into work that already exists. It does not appoint, and it does not
      replace the observatory. Stars do not appoint. Recovery is a job.
    </p>
    <p class="bio-covenant">{profile.covenant}</p>
  </section>
</article>

<style>
  .bio-hero {
    max-width: 40rem;
  }
  .bio-avatar {
    display: block;
    width: 7.5rem;
    height: 7.5rem;
    object-fit: cover;
    object-position: top;
    border-radius: 999px;
    border: 1px solid var(--observatory-line-strong);
    background: var(--observatory-surface);
    margin: 8px 0 28px;
  }
  .bio-kicker {
    color: var(--observatory-copper);
    font: 0.72rem / 1 var(--font-mono);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0;
  }
  .bio-page h1 {
    background: none;
    -webkit-text-fill-color: var(--observatory-ivory);
    color: var(--observatory-ivory);
    font-size: clamp(2.4rem, 7vw, 4.2rem);
    line-height: 0.95;
    letter-spacing: -0.04em;
    margin: 0.6rem 0 0;
  }
  .bio-page h1 em {
    color: var(--observatory-copper);
    font-style: italic;
  }
  .bio-handle {
    color: var(--observatory-muted);
    font: 0.78rem / 1 var(--font-mono);
    letter-spacing: 0.12em;
    margin-top: 0.85rem;
  }
  .bio-place {
    color: var(--observatory-copper);
    font: 0.72rem / 1.4 var(--font-mono);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 1.2rem;
  }
  .bio-socials {
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem 1.4rem;
    margin-top: 1.6rem;
  }
  .bio-socials a {
    color: var(--observatory-ivory);
    font: 0.7rem / 1 var(--font-mono);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--observatory-copper);
    padding-bottom: 0.2rem;
  }
  .bio-socials a:hover {
    color: var(--observatory-copper);
    text-decoration: none;
  }
  .pull {
    display: block;
    margin-top: 1.4rem;
    padding: 1.4rem 0 1.4rem 1.3rem;
    border-left: 1px solid var(--observatory-copper);
    color: var(--observatory-ivory);
    max-width: 42rem;
  }
  .pull:hover {
    text-decoration: none;
    color: var(--observatory-ivory);
  }
  .pull p {
    font: italic 1.25rem / 1.35 var(--font-display);
    margin: 0;
    color: var(--observatory-ivory);
  }
  .pull span {
    display: block;
    margin-top: 0.9rem;
    color: var(--observatory-copper);
    font: 0.68rem / 1 var(--font-mono);
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }
  .bio-cards {
    grid-template-columns: 1fr;
    max-width: 40rem;
  }
  @media (min-width: 820px) {
    .bio-cards {
      grid-template-columns: 1fr 1fr;
      max-width: none;
    }
  }
  .bio-covenant {
    font: italic 1.15rem / 1.4 var(--font-display);
    color: var(--observatory-copper);
  }
</style>
