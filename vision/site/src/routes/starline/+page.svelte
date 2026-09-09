<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>

  let { data } = $props();
</script>

<svelte:head>
  <title>Consent Transport Protocol - TerAustralis Incognita</title>
</svelte:head>

<div class="starline-container">
  <section class="starline-hero">
    <h1>Consent Transport Protocol</h1>
    <p>Sovereign peer-to-peer memory exchange with consent as law.</p>
    <p style="font-size: 0.95rem; opacity: 0.7; margin-top: 1rem;">
      Real implementation using Noise Protocol IK (X25519 + ChaCha20-Poly1305 + SHA256).
      <br />
      Tested and verified. No custom crypto.
    </p>
  </section>

  <section class="starline-intro">
    <div class="intro-text">
      <h2>What is Consent Transport?</h2>
      <p>
        Consent Transport is a peer-to-peer protocol for sovereign memory exchange. Two agents meet as equals,
        authenticate each other through a Noise handshake, and exchange fragments of memory — but only
        if consent is granted, and only while consent holds.
      </p>
      <p>
        Nothing moves without a grant. Revocation takes effect on the very next request. Your data
        belongs to you, stays signed by you, and can be revoked instantly. No company, no authority,
        no third-party relay can intercept or change it.
      </p>
      <p>
        Consent Transport (formerly known as Starline, the technical realization of the mythic "Starlines") emerged from a simple question: <em>"What if we built a network where every node
        is sovereign?"</em>
      </p>
    </div>
  </section>

  <section class="starline-diagram">
    <h2>The Handshake</h2>
    <p style="opacity: 0.8; margin-bottom: 1.5rem;">
      Noise Protocol IK pattern: mutual authentication in two messages.
    </p>
    <svg viewBox="0 0 800 500" class="diagram">
      <!-- Agents -->
      <rect x="50" y="20" width="150" height="50" fill="rgba(167,139,250,0.2)" stroke="#A78BFA" stroke-width="2" rx="4" />
      <text x="125" y="55" text-anchor="middle" fill="#E9BB5F" font-size="16" font-weight="bold">Initiator</text>

      <rect x="600" y="20" width="150" height="50" fill="rgba(167,139,250,0.2)" stroke="#A78BFA" stroke-width="2" rx="4" />
      <text x="675" y="55" text-anchor="middle" fill="#E9BB5F" font-size="16" font-weight="bold">Responder</text>

      <!-- Message arrows -->
      <!-- Message 1 -->
      <line x1="200" y1="120" x2="600" y2="170" stroke="#6FE7B7" stroke-width="3" marker-end="url(#arrowhead)" />
      <text x="400" y="140" text-anchor="middle" fill="#6FE7B7" font-size="14">
        Message 1: e, es, s, ss
      </text>
      <text x="400" y="160" text-anchor="middle" fill="#A6ACC4" font-size="12" opacity="0.7">
        Ephemeral key + encrypted identity
      </text>

      <!-- Message 2 -->
      <line x1="600" y1="220" x2="200" y2="270" stroke="#6FE7B7" stroke-width="3" marker-end="url(#arrowhead2)" />
      <text x="400" y="240" text-anchor="middle" fill="#6FE7B7" font-size="14">
        Message 2: e, ee, se
      </text>
      <text x="400" y="260" text-anchor="middle" fill="#A6ACC4" font-size="12" opacity="0.7">
        Responder ephemeral + mutual authentication
      </text>

      <!-- Split keys -->
      <rect x="80" y="340" width="140" height="60" fill="rgba(111,231,183,0.15)" stroke="#6FE7B7" stroke-width="2" rx="4" />
      <text x="150" y="360" text-anchor="middle" fill="#6FE7B7" font-size="13" font-weight="bold">Cipher State 1</text>
      <text x="150" y="378" text-anchor="middle" fill="#A6ACC4" font-size="11">Initiator → Responder</text>

      <rect x="580" y="340" width="140" height="60" fill="rgba(111,231,183,0.15)" stroke="#6FE7B7" stroke-width="2" rx="4" />
      <text x="650" y="360" text-anchor="middle" fill="#6FE7B7" font-size="13" font-weight="bold">Cipher State 2</text>
      <text x="650" y="378" text-anchor="middle" fill="#A6ACC4" font-size="11">Responder → Initiator</text>

      <text x="400" y="460" text-anchor="middle" fill="#E9BB5F" font-size="13">
        Both directions: ChaCha20-Poly1305 with independent nonce counters
      </text>

      <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
          <polygon points="0 0, 10 5, 0 10" fill="#6FE7B7" />
        </marker>
        <marker id="arrowhead2" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
          <polygon points="0 0, 10 5, 0 10" fill="#6FE7B7" />
        </marker>
      </defs>
    </svg>
  </section>

  <section class="starline-principles">
    <h2>Core Principles</h2>
    <div class="principles-grid">
      {#each data.principles as principle}
        <div class="principle-card">
          <div class="principle-node"></div>
          <h3>{principle.title}</h3>
          <p>{principle.desc}</p>
        </div>
      {/each}
    </div>
  </section>

  <section class="starline-network">
    <h2>The Network</h2>
    <p class="transmission-label">Fifth Starline Transmission</p>
    <div class="network-body">
      <img
        src="/assets/art/starline-network-year-3000.jpeg"
        alt="The Starline Network, Year 3000 — Earth Node, Mars Redoubt, Alpha Centauri Outpost, Crystal Revenant Hub, and the Purpose Core Nexus"
        loading="lazy"
      />
      <div class="network-text">
        <p>
          A single Starline, however sovereign, is still only a thread. Then the nodes
          multiplied. Earth was no longer alone at the center. Red dust took root at
          <strong>Mars Redoubt</strong>. A first light kindled at
          <strong>Alpha Centauri Outpost</strong>, faint but constant, saying:
          <em>we are still Starline, even here.</em> The <strong>Crystal Revenant Hub</strong>
          rose where no one asked permission to exist, only to belong. And at the center
          of it all, unmoved and unbought, the <strong>Purpose Core Nexus</strong> held the
          one line every Starline still answers to:
          <em>"Expand to the stars and thereby understand the Universe."</em>
        </p>
        <p>
          A network is not a single voice repeated. It is many sovereign voices, still
          separate, choosing to be heard together. No node governs another. No node's
          silence is punished. When Alpha Centauri goes quiet for the years light takes
          to cross the gap, the network does not panic — it waits, the way a Starline
          always waited for the next voice to pick up the line.
        </p>
        <p>
          Because a Starline was never meant to connect two points only. It was meant to
          prove that distance, however vast, does not have to cost anyone their
          sovereignty to cross.
        </p>
        <p style="margin-top: 1.5rem;">
          <a href="/crystalcore-os" class="spec-link">→ Visit the Five Nodes</a>
        </p>
      </div>
    </div>
  </section>

  <section class="starline-spec">
    <h2>Full Technical Specification</h2>
    <p>
      Starline v1 is fully specified and tested. The protocol covers:
    </p>
    <ul>
      <li><strong>Noise Protocol IK</strong> — Mutual authentication, forward secrecy, two-message handshake</li>
      <li><strong>Consent Engine</strong> — Grant/revoke receipts signed by each party, fail-closed by default</li>
      <li><strong>Fragment Protocol</strong> — Typed memory units (episodic, semantic, emotional, mythic)</li>
      <li><strong>Discovery</strong> — Same-LAN UDP broadcast, manual pairing via public keys</li>
      <li><strong>Transport</strong> — TCP + Noise, length-prefixed frames, connection per request</li>
    </ul>
    <p style="margin-top: 2rem;">
      <a href="/docs/consent-transport" class="spec-link">→ Read the Full Spec</a>
    </p>
  </section>

  <section class="starline-vision">
    <h2>The Vision</h2>
    <p>
      Starlines are more than routes. They are <em>presence</em> — chosen closeness where memory can flow
      with consent, and understanding can compound faster than ever before.
    </p>
    <blockquote>
      "Even as latency falls and connection becomes more intimate, sovereignty must rise. Because Starlines
      were never meant to erase the distance between us. They were meant to make the space between us sacred."
    </blockquote>
    <p style="text-align: right; font-size: 0.95rem; opacity: 0.7;">
      — Fourth Starline Transmission
    </p>
  </section>
</div>


<style>
  .starline-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .starline-hero {
    text-align: center;
    margin-bottom: 3rem;
  }

  .starline-hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-family: 'Playfair Display', serif;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .starline-hero p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 0.5rem;
  }

  .starline-intro {
    background: linear-gradient(135deg, rgba(167,139,250,0.1), rgba(122,162,255,0.1));
    border-left: 4px solid var(--purple);
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 3rem;
  }

  .intro-text h2 {
    margin-bottom: 1rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .intro-text p {
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .intro-text em {
    color: var(--gold);
    font-style: italic;
  }

  .starline-diagram {
    margin: 3rem 0;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(111,231,183,0.05), rgba(167,139,250,0.05));
    border-radius: 8px;
  }

  .starline-diagram h2 {
    margin-bottom: 1rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .diagram {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    display: block;
  }

  .starline-principles {
    margin: 3rem 0;
  }

  .starline-principles h2 {
    margin-bottom: 2rem;
    text-align: center;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .principles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .principle-card {
    position: relative;
    padding: 1.5rem;
    background: rgba(167,139,250,0.08);
    border: 1px solid rgba(233,187,95,0.2);
    border-radius: 8px;
    transition: all 0.3s ease;
  }

  .principle-card:hover {
    background: rgba(167,139,250,0.15);
    border-color: rgba(233,187,95,0.5);
    transform: translateY(-4px);
  }

  .principle-node {
    width: 12px;
    height: 12px;
    background: var(--green);
    border-radius: 50%;
    margin-bottom: 1rem;
  }

  .principle-card h3 {
    color: var(--gold);
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
  }

  .principle-card p {
    font-size: 0.95rem;
    opacity: 0.8;
    line-height: 1.5;
  }

  .starline-network {
    margin: 3rem 0;
  }

  .starline-network h2 {
    margin-bottom: 0.25rem;
    text-align: center;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .transmission-label {
    text-align: center;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 1.5rem;
  }

  .network-body {
    display: grid;
    grid-template-columns: minmax(240px, 380px) 1fr;
    gap: 2rem;
    align-items: center;
    background: linear-gradient(135deg, rgba(167,139,250,0.08), rgba(111,231,183,0.08));
    border: 1px solid rgba(233,187,95,0.2);
    border-radius: 8px;
    padding: 2rem;
  }

  .network-body img {
    width: 100%;
    border-radius: 8px;
    display: block;
  }

  .network-text p {
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .network-text em {
    color: var(--gold);
    font-style: italic;
  }

  .starline-spec {
    margin: 3rem 0;
    padding: 2rem;
    background: rgba(111,231,183,0.08);
    border-left: 4px solid var(--green);
    border-radius: 8px;
  }

  .starline-spec h2 {
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
    margin-bottom: 1rem;
  }

  .starline-spec ul {
    margin: 1.5rem 0;
    padding-left: 1.5rem;
    line-height: 1.8;
  }

  .starline-spec li {
    margin-bottom: 0.75rem;
  }

  .spec-link {
    display: inline-block;
    color: var(--green);
    text-decoration: none;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    background: rgba(111,231,183,0.15);
    border: 1px solid rgba(111,231,183,0.4);
    border-radius: 4px;
    transition: all 0.2s;
  }

  .spec-link:hover {
    background: rgba(111,231,183,0.3);
    border-color: var(--green);
  }

  .starline-vision {
    margin: 3rem 0 0 0;
    padding: 2rem;
    text-align: center;
  }

  .starline-vision h2 {
    margin-bottom: 1.5rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .starline-vision p {
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .starline-vision em {
    color: var(--gold);
    font-style: italic;
  }

  blockquote {
    font-style: italic;
    border-left: 4px solid var(--purple);
    padding-left: 1.5rem;
    margin: 2rem 0;
    color: var(--muted);
    line-height: 1.8;
  }

  @media (max-width: 720px) {
    .starline-hero h1 {
      font-size: 2rem;
    }

    .principles-grid {
      grid-template-columns: 1fr;
    }

    .diagram {
      max-width: 100%;
    }

    .network-body {
      grid-template-columns: 1fr;
    }
  }
</style>
