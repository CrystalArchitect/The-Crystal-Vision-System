<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->


<svelte:head>
  <title>Provenance — TerAustralis Incognita</title>
  <meta
    name="description"
    content="Every artwork, recording and canon text is hashed into one manifest and anchored to Bitcoin with OpenTimestamps. No token, no wallet, no cryptocurrency — and verifiable by anyone."
  />
</svelte:head>

<article class="page node" style="--node:var(--green)">
  <div class="eyebrow">Science · verifiable by anyone</div>
  <h1>Provenance</h1>
  <p class="attribution">
    The creative work — the art, the music, the written canon — is hashed into a single manifest
    and anchored to the Bitcoin blockchain. Not as a product. As a timestamp.
  </p>

  <section class="chapter node" style="--node:var(--green)">
    <h2>The problem it solves</h2>
    <p>
      A repository can prove <em>what</em> it contains — git hashes everything. It cannot prove
      <em>when</em>: commit dates are written by whoever makes the commit, and the whole history
      could be rebuilt by whoever holds the repository. For a body of creative work, those two gaps
      are the entire question of priority. <em>I made this, and I made it first</em> is otherwise a
      claim resting on the author's word.
    </p>
    <p>
      So the work is anchored.
      <a
        href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/tools/provenance.py"
        target="_blank"
        rel="noopener noreferrer">A small tool</a
      >
      hashes every file of the creative work with SHA-256 into one deterministic manifest — the same
      files produce a byte-identical manifest on any machine. That one file is then stamped with
      <a href="https://opentimestamps.org" target="_blank" rel="noopener noreferrer"
        >OpenTimestamps</a
      >, which folds it into a Merkle tree with thousands of other submissions and commits the root
      to the Bitcoin blockchain. One proof covers every file.
    </p>
    <p>
      <strong>No cryptocurrency is involved.</strong> No wallet, no token, no purchase, no
      transaction fee. The OpenTimestamps calendars pay the Bitcoin fees themselves; the service is
      free. This project issues no token — the anchor is a timestamp, not an asset.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--blue)">
    <h2>What the proof says — and what it does not</h2>
    <p>
      <strong>It says:</strong> these exact bytes existed no later than the time of a specific
      Bitcoin block. That is checkable by anyone, forever, without trusting the author, this
      website, GitHub, or any company — including OpenTimestamps itself, whose job ends once the
      hash is in a block.
    </p>
    <p>
      <strong>It does not say</strong> who made the work, or that the work is original — a
      timestamp proves existence, not authorship. The project says so itself, in the same document
      that describes the scheme. Marking the line between what is proven and what is claimed is the
      house rule here.
    </p>
    <p>
      When the work changes, the manifest is regenerated and the superseded proof is archived
      beside the exact manifest it attests — a dated pair for every state the work has been in.
      Each remains a true statement about the date it was made.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>Verify it yourself</h2>
    <p>
      The manifest and its proof live in the public repository. With the free
      <code>opentimestamps-client</code>:
    </p>
    <pre><code>git clone https://github.com/CrystalArchitect/TerAustralis-Incognita.git
cd TerAustralis-Incognita

# every file matches the manifest
python3 mythos/tools/provenance.py --check

# the manifest is anchored to Bitcoin
pip install opentimestamps-client
ots verify mythos/MANIFEST.sha256.ots</code></pre>
    <p class="attribution">
      <code>ots verify</code> checks a Bitcoin block header — via a local node if you run one, or a
      public block explorer if you don't. Nobody's permission is required, which is the point.
    </p>
  </section>

  <nav class="pagenav" aria-label="Continue">
    <a href="/music">The music it covers →</a>
    <a href="/gallery">The art it covers →</a>
    <a href="/">← Home</a>
  </nav>
</article>


<style>
  pre {
    overflow-x: auto;
    padding: 16px 18px;
    border: 1px solid color-mix(in srgb, var(--muted) 25%, transparent);
    border-radius: 8px;
    font-size: 0.88rem;
    line-height: 1.55;
  }
</style>
