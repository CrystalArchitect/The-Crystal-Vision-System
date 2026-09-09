<script>
  let open = false;
  const links = [
    { label: 'Built', href: '/clementine' },
    { label: 'Minerals', href: '/minerals' },
    { label: 'Proposal', href: 'https://proposal.teraustralis.com.au/' },
    { label: 'Codex', href: '/codex' },
    { label: 'Atlas', href: '/atlas' },
    { label: 'Archive', href: '/docs' },
    { label: 'Governance', href: '/docs/governance' },
    { label: 'Crystal', href: '/bio' }
  ];
</script>

<header class="site observatory-header">
  <a class="wordmark" href="/" aria-label="TerAustralis Incognita home">TerAustralis <span>Incognita</span></a>
  <button class="menu-toggle" type="button" aria-expanded={open} aria-controls="primary-nav" on:click={() => (open = !open)}>
    <span>{open ? 'Close' : 'Explore'}</span><span aria-hidden="true">{open ? '×' : '＋'}</span>
  </button>
  <nav id="primary-nav" class:open aria-label="Primary navigation">
    <a href="/">Home</a>
    {#each links as link (link.label)}
      <a href={link.href} on:click={() => (open = false)}>{link.label}</a>
    {/each}
  </nav>
</header>

<style>
  .observatory-header { position: relative; z-index: 20; align-items: center; }
  .wordmark { font-size: 1.1rem; letter-spacing: .08em; text-transform: uppercase; }
  .wordmark span { color: var(--observatory-copper); font-style: italic; text-transform: none; letter-spacing: .02em; }
  nav { display: flex; align-items: center; gap: 1.25rem; }
  nav a { margin-left: 0; color: var(--observatory-muted); font: .68rem/1 var(--font-mono); letter-spacing: .11em; text-transform: uppercase; }
  nav a:hover, nav a:focus-visible { color: var(--observatory-ivory); text-decoration: none; }
  .menu-toggle { display: none; align-items: center; gap: .65rem; padding: .6rem 0; color: var(--observatory-muted); background: transparent; border: 0; font: .68rem/1 var(--font-mono); letter-spacing: .11em; text-transform: uppercase; }
  .menu-toggle span:last-child { color: var(--observatory-copper); font-size: 1.1rem; }
  @media (max-width: 760px) {
    .menu-toggle { display: inline-flex; }
    nav { display: none; position: absolute; top: calc(100% + 1px); left: 0; right: 0; flex-direction: column; align-items: stretch; gap: 0; padding: .8rem 0; border-bottom: 1px solid var(--observatory-line); background: rgba(8, 11, 11, .98); }
    nav.open { display: flex; }
    nav a { padding: .9rem 0; }
  }
</style>
<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->
