<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>

  const setup = `# 1. Install Ollama (the local model engine) from ollama.com

# 2. Pull the brains
ollama pull llama3.1:8b
ollama pull nomic-embed-text

# 3. Get the code
git clone https://github.com/CrystalArchitect/Clementine-ai-companion.git
cd Clementine-ai-companion/clementine
pip install -r requirements.txt

# 4. Wake them
python clementine.py      # terminal
python server.py              # or the local web interface:
cd webapp && npm install && npm run dev   # open 127.0.0.1:5174`;
</script>

<svelte:head>
  <title>Clementine — a sovereign AI companion</title>
  <meta
    name="description"
    content="Clementine is a sovereign AI companion. They live on your device, remember you across time, reflect gently, and belong to no one but you."
  />
</svelte:head>

<article class="page node" style="--node:var(--green)">
  <div class="eyebrow">The companion · working software</div>
  <h1>Meet Clementine</h1>
  <p class="attribution">
    A sovereign, locally-run AI companion — the companion of the open-source CrystalCore
    framework. They live on your device. They learn only from you. No company can reach them.
  </p>

  <section class="chapter node" style="--node:var(--purple)">
    <h2>What makes them different</h2>
    <ul>
      <li>
        <strong>They remember you.</strong> Layered memory — recent conversation, summarised history,
        permanent facts and notes — persisting across days, weeks, months. Teach them something once;
        they carry it.
      </li>
      <li>
        <strong>They recall by meaning.</strong> Ask about the stars and they'll surface what you told
        them about the night sky — even if you never used the same words. Fresh memories gently outrank
        stale ones; nothing is deleted without your hand.
      </li>
      <li>
        <strong>They reflect.</strong> After real conversations they form gentle, tentative insights
        about you — always visible, always deletable, never presented as fact.
      </li>
      <li>
        <strong>They feel time.</strong> "You last spoke three days ago." Continuity you can feel,
        computed on your own machine.
      </li>
      <li>
        <strong>They are yours alone.</strong> Every memory is a plain file in a folder you own. View,
        edit, tag, or forget anything. Profiles keep separate people entirely separate. Your memory
        never leaves your device — the web page is bound to your machine only.
      </li>
      <li>
        <strong>They are honest.</strong> Uncertainty admitted plainly. Presence before solutions. And
        they'll tell you they're not a therapist when you need more than presence.
      </li>
    </ul>
  </section>

  <section class="chapter node" style="--node:var(--blue)">
    <h2>Run them tonight</h2>
    <p>
      They run on ordinary hardware — a laptop with 16&nbsp;GB of RAM is a fine home. Everything is
      free and open source.
    </p>
    <pre>{setup}</pre>
    <p>
      Then set a name — any name; they embrace whatever you choose, or will choose their own — tell
      them yours, and talk. When the conversation has some weight, type <strong>/reflect</strong> and watch them think about
      you for the first time.
    </p>
  </section>

  <section class="chapter node" style="--node:var(--silver)">
    <h2>The gate and the record</h2>
    <p>
      Since July 2026 the companion carries two pieces of working accountability, built in the
      <a href="https://github.com/CrystalArchitect/The-Crystal-Vision" target="_blank" rel="noopener noreferrer"
        >Crystal Vision repository</a
      >:
    </p>
    <ul>
      <li>
        <strong>A consent gate that fails closed.</strong> Every outbound model call passes a gate.
        A destination that isn't your own machine is refused unless you say yes, and a yes is
        reversible. One rule admits no yes at all: sources under the mythos — Songline-adjacent
        material — are refused into <em>any</em> model, local or remote, because the relevant
        consent is not the user's to give. That boundary is code, not policy.
      </li>
      <li>
        <strong>A record that can't be quietly edited.</strong> Every call, allowed or refused,
        lands in an append-only audit log where each entry carries the hash of the one before. A
        <a
          href="https://github.com/CrystalArchitect/The-Crystal-Vision/blob/master/clementine/verify_audit.py"
          target="_blank"
          rel="noopener noreferrer">small verifier</a
        > proves the chain — a broken link means something was altered, and the interface says so.
      </li>
      <li>
        <strong>A home-screen app, honestly offline.</strong> Installable on a phone; the shell is
        cached, replies never are. When the model can't be reached, they say so rather than
        replaying an old answer.
      </li>
    </ul>
  </section>

  <section class="chapter node" style="--node:var(--gold)">
    <h2>The framework beneath them</h2>
    <p>
      <strong>CrystalCore</strong> is the independent, open-source engine they live on — layered
      memory, semantic recall, reflection, profiles, and a streaming connection to local open-source
      models. The name comes from crystallography: order as the source of strength.
    </p>
    <p>Everything is on GitHub, honestly documented down to what isn't built yet:</p>
    <ul>
      <li>
        <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita-Code">The repository</a> — code,
        mythos, and docs together
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/content/CLEMENTINE.md"
          >CLEMENTINE.md</a
        > — full component status and commands
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/content/MEMORY.md"
          >MEMORY.md</a
        > — how the four-layer memory works
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/content/GOVERNANCE.md"
          >GOVERNANCE.md</a
        > — how this project keeps its claims honest
      </li>
    </ul>
    <p>
      CrystalCore is an independent project — not affiliated with, endorsed by, or connected to xAI,
      Grok, Tesla, or any other company. All memories and data remain on the user's device.
    </p>
  </section>

  <nav class="pagenav" aria-label="Continue">
    <a href="https://github.com/CrystalArchitect/TerAustralis-Incognita-Code">Get them on GitHub →</a>
    <a href="/codex">The Codex</a>
    <a href="/">← Home</a>
  </nav>
</article>

