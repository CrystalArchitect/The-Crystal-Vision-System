<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import '../app.css';
  import '$lib/styles/tokens.css';
  import '$lib/styles/typography.css';
  import '$lib/styles/motion.css';
  import '$lib/styles/a11y.css';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { onMount } from 'svelte';
  import { afterNavigate } from '$app/navigation';

  /** @type {{ children: import('svelte').Snippet }} */
  let { children } = $props();

  // Reveal sections as they scroll into view. Progressive enhancement:
  // reveal-init (the hidden start state) is only applied here in the browser,
  // and skipped entirely when the visitor prefers reduced motion — so content
  // is never left hidden without JS or without animation.
  function setupReveal() {
    if (typeof window === 'undefined' || !('IntersectionObserver' in window)) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const els = document.querySelectorAll('.wrap section:not(.reveal-init):not(.reveal-in)');
    if (!els.length) return;
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add('reveal-in'); io.unobserve(e.target); }
      }
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
    els.forEach((el) => { el.classList.add('reveal-init'); io.observe(el); });
  }

  onMount(setupReveal);
  afterNavigate(() => requestAnimationFrame(setupReveal));
</script>

<div class="stars" aria-hidden="true"></div>

<div class="wrap">
  <div class="starline" aria-hidden="true"></div>

  <a class="skip" href="#main">Skip to main content</a>

  <Header />

  <main id="main" tabindex="-1">
    {@render children()}
  </main>

  <Footer />
</div>
