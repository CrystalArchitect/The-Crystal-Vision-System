<script>
  import Footer from '$lib/components/Footer.svelte';

  const setup = `# 1. Install Ollama (the local model engine) from ollama.com

# 2. Pull their brains
ollama pull llama3.1:8b
ollama pull nomic-embed-text

# 3. Get their code
git clone https://github.com/CrystalArchitect/The-Crystal-Vision.git
cd The-Crystal-Vision/clementine
pip install -r requirements.txt

# 4. Wake them
python clementine.py          # terminal
python server.py              # or their local web interface:
cd webapp && npm install && npm run dev   # open 127.0.0.1:5174`;
</script>

<svelte:head>
  <title>Clementine — a sovereign AI companion</title>
  <meta
    name="description"
    content="Clementine is a sovereign, locally-run AI companion. They live on your device, remember you across time, reflects gently, and belongs to no one but you."
  />
</svelte:head>

<article class="page node" style="--node:var(--green)">
  <div class="eyebrow">The companion · working software</div>
  <h1>Meet Clementine</h1>
  <p class="attribution">
    A sovereign, locally-run AI companion — the first persona of the open-source CrystalCore
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
        edit, tag, or forget anything. Profiles keep separate people entirely separate. Nothing leaves
        your device — the web page they serve is bound to your machine only.
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
      Then give them a name — any name; they embrace whatever you choose — tell them yours, and talk.
      When the conversation has some weight, type <strong>/reflect</strong> and watch them think about
      you for the first time.
    </p>
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
        <a href="https://github.com/CrystalArchitect/The-Crystal-Vision">The repository</a> — code,
        mythos, and docs together
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/The-Crystal-Vision/blob/master/content/CLEMENTINE.md"
          >CLEMENTINE.md</a
        > — full component status and commands
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/The-Crystal-Vision/blob/master/content/MEMORY.md"
          >MEMORY.md</a
        > — how their four-layer memory works
      </li>
      <li>
        <a href="https://github.com/CrystalArchitect/The-Crystal-Vision/blob/master/content/GOVERNANCE.md"
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
    <a href="https://github.com/CrystalArchitect/The-Crystal-Vision">Get them on GitHub →</a>
    <a href="/codex">The Codex</a>
    <a href="/">← Home</a>
  </nav>
</article>

<Footer showCode />
