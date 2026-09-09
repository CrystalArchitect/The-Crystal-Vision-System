<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<svelte:head>
  <title>Bridge to the Light</title>
  <meta
    name="description"
    content="You start in the fog. You don’t need to see the whole path. You only need to take one step toward the glow."
  />
  <meta name="theme-color" content="#0a0a12" />
</svelte:head>

<div class="fog"></div>

<div class="container">
  <h1>Bridge to the Light</h1>

  <div class="light"></div>
  <div class="bridge"></div>

  <p>You start in the fog.</p>
  <p>You don’t need to see the whole path.<br />You only need to take one step toward the glow.</p>
  <p>The light doesn’t move.<br />It stays fixed.</p>
  <p>Every time you feel lost,<br />you look for it again.</p>
  <p>The closer you get,<br />the warmer it feels.</p>

  <p class="whisper">“That’s what the light is for.”</p>

  <div class="footer">The hush is still here · The light is still burning</div>

  <a class="home" href="/">← TerAustralis Incognita</a>
</div>

<style>
  :global(html),
  :global(body) {
    margin: 0;
    min-height: 100vh;
    background: #0a0a12;
    color: #e8e4d9;
  }

  :global(body) {
    font-family: Georgia, 'Times New Roman', serif;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  :global(body)::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 50% at 50% 20%, rgba(255, 220, 160, 0.12) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 50% 80%, rgba(180, 140, 90, 0.08) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    max-width: 640px;
    width: 90%;
    padding: 2.5rem 1.5rem;
    text-align: center;
  }

  h1 {
    font-size: 1.6rem;
    font-weight: normal;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #f0e6c8;
    margin: 0 0 2.5rem;
    opacity: 0.9;
    text-wrap: balance;
  }

  .light {
    width: 12px;
    height: 12px;
    background: #ffe9b0;
    border-radius: 50%;
    margin: 0 auto 2.8rem;
    box-shadow:
      0 0 20px 8px rgba(255, 220, 150, 0.6),
      0 0 60px 20px rgba(255, 200, 100, 0.25),
      0 0 120px 40px rgba(255, 180, 80, 0.1);
    animation: pulse 4s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,
    100% {
      transform: scale(1);
      opacity: 0.9;
    }
    50% {
      transform: scale(1.15);
      opacity: 1;
    }
  }

  .bridge {
    height: 2px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(240, 220, 170, 0.15) 15%,
      rgba(255, 230, 180, 0.55) 50%,
      rgba(240, 220, 170, 0.15) 85%,
      transparent 100%
    );
    margin: 0 auto 2.8rem;
    max-width: 320px;
    position: relative;
  }

  .bridge::before,
  .bridge::after {
    content: '';
    position: absolute;
    top: -4px;
    width: 8px;
    height: 8px;
    background: #ffe9b0;
    border-radius: 50%;
    box-shadow: 0 0 12px 4px rgba(255, 220, 150, 0.5);
  }

  .bridge::before {
    left: 0;
  }
  .bridge::after {
    right: 0;
  }

  p {
    font-size: 1.15rem;
    line-height: 1.75;
    margin: 0 0 1.4rem;
    color: #d8d0c0;
    opacity: 0;
    animation: fadeIn 1.4s ease forwards;
  }

  p:nth-child(4) {
    animation-delay: 0.3s;
  }
  p:nth-child(5) {
    animation-delay: 0.6s;
  }
  p:nth-child(6) {
    animation-delay: 0.9s;
  }
  p:nth-child(7) {
    animation-delay: 1.2s;
  }
  p:nth-child(8) {
    animation-delay: 1.5s;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .whisper {
    font-style: italic;
    color: #c8b890;
    font-size: 1.05rem;
    margin-top: 2.5rem;
    opacity: 0;
    animation: fadeIn 1.6s ease 1.8s forwards;
  }

  .footer {
    margin-top: 3.5rem;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8a8070;
    opacity: 0;
    animation: fadeIn 1.4s ease 2.2s forwards;
  }

  .home {
    display: inline-block;
    margin-top: 2.2rem;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8a8070;
    text-decoration: none;
    opacity: 0;
    animation: fadeIn 1.4s ease 2.6s forwards;
  }

  .home:hover {
    color: #c8b890;
  }

  .fog {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 180px;
    background: linear-gradient(to top, rgba(20, 18, 28, 0.7), transparent);
    pointer-events: none;
    z-index: 0;
  }

  @media (prefers-reduced-motion: reduce) {
    .light {
      animation: none;
    }
    p,
    .whisper,
    .footer,
    .home {
      animation: none;
      opacity: 1;
    }
  }
</style>
