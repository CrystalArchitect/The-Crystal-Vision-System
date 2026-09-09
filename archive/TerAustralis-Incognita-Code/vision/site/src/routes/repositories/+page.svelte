<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { repositories, stateLabels } from '$lib/data/repositories.js';

  const stateAccent = {
    active: 'var(--domain-clementine)',
    dormant: 'var(--domain-archive)',
    frozen: 'var(--domain-codex)'
  };
</script>

<svelte:head>
  <title>The Repositories — TerAustralis Incognita</title>
  <meta
    name="description"
    content="The real repository portfolio: six repositories, their roles, their recorded states — rendered from the Archive's own ledgers."
  />
</svelte:head>

<div class="page">
  <div class="eyebrow">TerAustralis Incognita · The Portfolio</div>
  <h1>The Repositories</h1>
  <p class="attribution">
    The founding six, one system. This page renders from the Archive's own
    ledgers — the repository map, the per-repo STATUS files, and the
    evidence-tiered archaeology of 2026-07-24. Ledger, not legend: every
    state here is recorded, dated, and checkable. The portfolio has since
    grown — thirteen repositories as of 2026-08-07, mapped in
    <a
      href="https://github.com/CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive/blob/main/knowledge-base/02-REPOSITORY-MAP.md"
      target="_blank"
      rel="noopener noreferrer">the Archive's repository map</a
    >; the cards below remain the surveyed core.
  </p>

  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <!-- Scrollable on narrow screens, so it must be keyboard-reachable. -->
  <pre class="lineage" tabindex="0" role="region" aria-label="Repository lineage, oldest to newest">
founding laptop (pre-git)
  ├─▶ The-Crystal-Vision ......... 2026-07-14 · the origin
  ├─▶ crystalcore ................ 2026-07-17 · frozen pack
  └─▶ crystal-vision ............. 2026-07-17 · frozen shell
        │  content carried forward — verified byte-identical
        ▼
      TerAustralis-Incognita ..... the umbrella · active
        │  engineering split, ADR-0011
        ▼
      TerAustralis-Incognita-Code  the software · active
        ·
      the Archive ................ documents all six</pre>

  <div class="repo-grid">
    {#each repositories as repo (repo.id)}
      {#if repo.link}
        <a class="repo-card" href={repo.link} style="--rc:{stateAccent[repo.state]}">
          <span class="repo-state">{stateLabels[repo.state]}</span>
          <h2>{repo.name}</h2>
          <p class="role">{repo.role}</p>
          <ul class="holds">
            {#each repo.holds as item (item)}
              <li>{item}</li>
            {/each}
          </ul>
          <p class="note">{repo.stateNote}</p>
          <span class="cta">→ View on GitHub</span>
        </a>
      {:else}
        <div class="repo-card" style="--rc:{stateAccent[repo.state]}">
          <span class="repo-state">{stateLabels[repo.state]}{repo.isPrivate ? ' · private' : ''}</span>
          <h2>{repo.name}</h2>
          <p class="role">{repo.role}</p>
          <ul class="holds">
            {#each repo.holds as item (item)}
              <li>{item}</li>
            {/each}
          </ul>
          <p class="note">{repo.stateNote}</p>
        </div>
      {/if}
    {/each}
  </div>

  <p class="deeper">
    The deeper record — evidence tiers, corrections, the full history —
    lives in <a href="/docs">the Archive</a>. What runs, what's built,
    what's documented, and what stays vision are kept honestly separate
    there, the same way they are on this page.
  </p>
</div>


<style>
  .lineage {
    margin-top: 34px;
    font-family: var(--font-mono);
    font-size: 0.82rem;
    line-height: 1.75;
    color: var(--text-secondary);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    overflow-x: auto;
    max-width: 62ch;
  }
  .repo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 18px;
    margin-top: 40px;
  }
  .repo-card {
    display: block;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    color: var(--text-primary);
    transition: border-color 0.18s ease, transform 0.22s cubic-bezier(0.2, 0.7, 0.2, 1);
  }
  a.repo-card:hover {
    border-color: var(--rc, var(--border-strong));
    text-decoration: none;
    transform: translateY(-3px);
  }
  .repo-state {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: var(--weight-medium, 500);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--rc, var(--text-secondary));
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 4px 12px;
    margin-bottom: 14px;
  }
  .repo-card h2 {
    font-family: var(--font-display);
    font-weight: var(--weight-semibold, 600);
    font-size: 1.12rem;
    line-height: 1.3;
    color: var(--rc, var(--text-primary));
    overflow-wrap: anywhere;
  }
  .repo-card .role {
    margin-top: 8px;
    font-size: 0.92rem;
    color: var(--text-secondary);
  }
  .holds {
    margin: 12px 0 0 1.1em;
    padding: 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
  }
  .holds li {
    margin: 4px 0;
  }
  .note {
    margin-top: 12px;
    font-size: 0.8rem;
    font-style: italic;
    color: var(--text-secondary);
  }
  .cta {
    display: block;
    margin-top: 14px;
    font-size: 0.88rem;
    font-weight: var(--weight-medium, 500);
    color: var(--rc, var(--link));
  }
  .deeper {
    margin-top: 48px;
    max-width: 62ch;
    color: var(--text-secondary);
  }
</style>
