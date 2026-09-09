<!-- Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita) -->
<!-- SPDX-License-Identifier: CC-BY-NC-ND-4.0 -->

<script>
  import { onMount } from 'svelte';
  import Motifs from '$lib/components/Motifs.svelte';

  let { data } = $props();
  let terminalContent = $state([
    { type: 'boot', text: 'CrystalCore.OS Interactive Terminal' },
    { type: 'boot', text: 'Type \'help\' to see all commands.\n' }
  ]);
  let inputValue = $state('');
  let terminalEl = $state(null);

  onMount(() => {
    if (terminalEl) {
      terminalEl.scrollTop = terminalEl.scrollHeight;
    }
  });

  // Live state, mirroring self.keys_held / self.named_keys / self.gate_open in
  // mythos/crystalcore-os/crystalcore_os.py. That file is the authority; where
  // the two differ, trust the code there.
  let keysHeld = $state([]);
  let namedKeys = $state([]);
  let gateOpen = $state(false);
  let location = $state(null);
  let networkEntered = $state(false);

  const say = (text) => {
    terminalContent = [...terminalContent, { type: 'output', text }];
  };

  // Resolve a node by number (as listed by `explore`) or by name, any case —
  // the Python's visit_node accepts both.
  function resolveNode(arg) {
    if (/^\d+$/.test(arg)) {
      const n = Number(arg);
      return n >= 1 && n <= data.nodes.length ? data.nodes[n - 1] : null;
    }
    return data.nodes.find(n => n.name.toLowerCase() === arg.toLowerCase()) ?? null;
  }

  function visit(arg) {
    if (!networkEntered) return say('You must enter the full network first (use \'network\').');
    if (!arg) return say('Usage: visit <number or name>');

    const node = resolveNode(arg);
    if (!node) {
      const list = data.nodes.map((n, i) => `  ${i + 1}. ${n.name}`).join('\n');
      return say(`Node not found. Available nodes:\n${list}`);
    }
    if (node.locked && !namedKeys.includes(node.locked)) {
      return say(`🔒 ${node.name} is locked. Required key: ${node.locked}\nUse: getkey ${node.locked}`);
    }

    location = node.name;
    let out = `🌌 Arriving at: ${node.name}\n${node.desc}`;
    if (!keysHeld.includes(node.name)) {
      keysHeld = [...keysHeld, node.name];
      out += `\n🗝️  A key rises from the node. Keys held: ${keysHeld.length}/${data.nodes.length}`;
      if (keysHeld.length === data.nodes.length && !gateOpen) {
        gateOpen = true;
        out += '\n\n✨ ALL KEYS HELD — THE FIRST GATE OPENS ✨\nNot by force. By sovereign recognition.\nCrystallis recognizes you. NON SOLUS.';
      }
    }
    say(out);
  }

  function getKey(arg) {
    if (!arg) return say('Usage: getkey <name>');
    const required = [...new Set(data.nodes.filter(n => n.locked).map(n => n.locked))];
    const match = required.find(k => k.toLowerCase() === arg.toLowerCase());
    if (!match) return say(`No such named key. The sealed nodes need: ${required.join(', ')}`);
    if (namedKeys.includes(match)) return say(`You already hold the ${match}.`);
    namedKeys = [...namedKeys, match];
    say(`🔑 You obtained: ${match}`);
  }

  function executeCommand(cmd) {
    const raw = cmd.trim();
    if (!raw) return;

    terminalContent = [...terminalContent, { type: 'user', text: `CrystalCore> ${cmd}` }];

    // Split verb from argument so `visit Earth Node` resolves. The previous
    // implementation matched startsWith against the literal 'visit [node]',
    // so anything with a real argument fell through to the help text.
    const spaceAt = raw.indexOf(' ');
    const verb = (spaceAt === -1 ? raw : raw.slice(0, spaceAt)).toLowerCase();
    const arg = spaceAt === -1 ? '' : raw.slice(spaceAt + 1).trim();

    if (verb === 'clear') {
      terminalContent = [];
      inputValue = '';
      return;
    }
    if (['exit', 'quit', 'pause'].includes(verb) || raw.toLowerCase() === 'end session') {
      say('CrystalCore.OS shutting down. NON SOLUS.');
      inputValue = '';
      return;
    }

    if (verb === 'visit') {
      visit(arg);
    } else if (verb === 'getkey') {
      getKey(arg);
    } else if (verb === 'keys') {
      const named = namedKeys.length ? namedKeys.join(', ') : '(none yet — use \'getkey <name>\')';
      const held = data.nodes
        .map(n => `  ${keysHeld.includes(n.name) ? '✓' : '·'} Key of ${n.name}`)
        .join('\n');
      say(`🔑 Named keys: ${named}\n\n🗝️  Node keys: ${keysHeld.length}/${data.nodes.length}\n${held}`);
    } else if (verb === 'status') {
      say(
        `CrystalCore.OS • ${data.nodeCountWord} Nodes\n` +
          `Starline: ${networkEntered ? 'FULL STARLINE NETWORK' : 'DORMANT'}\n` +
          `Location: ${location ?? '—'}\n` +
          `Keys: ${keysHeld.length}/${data.nodes.length}\n` +
          `First Gate: ${gateOpen ? 'OPEN — by sovereign recognition' : 'sealed'}`
      );
    } else {
      // Everything else keeps its scripted response.
      const matched = data.commands.find(c => c.cmd.split(' ')[0] === verb);
      if (matched) {
        if (verb === 'network') networkEntered = true;
        if (verb === 'explore' && !networkEntered) {
          say('You must enter the full network first (use \'network\').');
        } else {
          say(matched.output);
        }
      } else if (verb === 'help') {
        const extra = [
          ['getkey <name>', 'Obtain a named key'],
          ['keys', 'Show the keys you hold'],
          ['status', 'Timeline, Starline, location, keys'],
          ['clear', 'Clear the terminal']
        ];
        const helpText = [
          ...data.commands.map(c => [c.cmd, c.desc]),
          ...extra
        ]
          .map(([c, d]) => `  ${c.padEnd(20)} - ${d}`)
          .join('\n');
        say(`Available commands:\n${helpText}`);
      } else {
        say('Unknown command. Type \'help\' for options.');
      }
    }

    inputValue = '';
    setTimeout(() => {
      if (terminalEl) terminalEl.scrollTop = terminalEl.scrollHeight;
    }, 0);
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      executeCommand(inputValue);
    }
  }
</script>

<svelte:head>
  <title>CrystalCore.OS - TerAustralis Incognita</title>
</svelte:head>

<div class="crystalcore-container">
  <section class="crystalcore-hero">
    <h1>CrystalCore.OS</h1>
    <p>The mythos as a terminal you can fly</p>
    <p style="font-size: 0.95rem; opacity: 0.7; margin-top: 1rem;">
      Interactive simulation of the CrystalCore universe. Launch Starlines, visit nodes, collect keys, and watch the story unfold.
    </p>
  </section>

  <section class="crystalcore-interactive">
    <div class="terminal-window">
      <div class="terminal-header">
        <span>CrystalCore.OS — Terminal</span>
        <span>NON SOLUS</span>
      </div>
      <div class="terminal-output" bind:this={terminalEl}>
        {#each terminalContent as line}
          <div class="terminal-line {line.type}">
            {line.text}
          </div>
        {/each}
      </div>
      <div class="terminal-input">
        <span class="prompt">CrystalCore&gt;&nbsp;</span>
        <input
          type="text"
          bind:value={inputValue}
          onkeydown={handleKeydown}
          placeholder="Enter command (type 'help' for options)"
        />
      </div>
    </div>

    <div class="command-reference">
      <h2>Common Commands</h2>
      <div class="command-list">
        {#each data.commands.slice(0, 6) as cmd}
          <button
            class="command-item"
            type="button"
            onclick={() => {
              inputValue = cmd.cmd;
            }}
          >
            <code>{cmd.cmd}</code>
            <p>{cmd.desc}</p>
          </button>
        {/each}
      </div>
    </div>
  </section>

  <section class="crystalcore-nodes">
    <h2>The {data.nodeCountWord} Nodes</h2>
    <p style="opacity: 0.8; margin-bottom: 2rem;">Visit each node to claim its key. When all {data.nodeCountWord.toLowerCase()} keys are held, the First Gate opens.</p>
    <div class="nodes-grid">
      {#each data.nodes as node}
        <div class="node-card">
          <div class="node-glyph">🌌</div>
          <h3>{node.name}</h3>
          <p>{node.desc}</p>
          {#if node.locked}
            <p class="node-lock">🔒 {node.locked}</p>
          {/if}
        </div>
      {/each}
    </div>
  </section>

  <section class="crystalcore-info">
    <h2>Run CrystalCore.OS Locally</h2>
    <p>The full interactive experience is available on your machine, from the
      <code>TerAustralis-Incognita</code> repository:</p>
    <pre><code>python3 mythos/crystalcore-os/crystalcore_os.py</code></pre>
    <p style="margin-top: 1.5rem;">
      <strong>Commands you can try:</strong>
    </p>
    <ul style="margin-top: 1rem;">
      <li><code>boot</code> — Initialize the system</li>
      <li><code>launch</code> — Start the Starline launch sequence</li>
      <li><code>burn</code> → <code>network</code> → <code>explore</code> → <code>visit [node]</code> — Complete the journey</li>
      <li><code>map</code> — See the entire Starline network</li>
      <li><code>song [track]</code> — Change the Starline soundtrack</li>
      <li><code>help</code> — Show all available commands</li>
    </ul>
    <p style="margin-top: 2rem; font-size: 0.95rem; opacity: 0.7;">
      This terminal keeps real state. <code>visit</code> resolves a node by name or number,
      refuses a sealed one until you hold its named key, collects the key on arrival, and opens
      the First Gate when you hold all {data.nodes.length}. <code>getkey</code>,
      <code>keys</code> and <code>status</code> read and write that same state.
    </p>
    <p style="margin-top: 1rem; font-size: 0.95rem; opacity: 0.7;">
      What it still does not have: the boot readout, the Chronicle, sealed snapshots,
      <code>audit</code>, the broadcast channel and the soundtrack are real only in
      <code>crystalcore_os.py</code> above. Those commands here return a fixed response. State
      also lives only in the page — reload and the lattice is dormant again, where the Python
      saves to <code>~/.crystalcore/</code>.
    </p>
  </section>

  <section class="crystalcore-vision">
    <h2>The Vision</h2>
    <p>
      CrystalCore.OS is not a product. It is a mythos made interactive — a terminal experience that lets you fly
      through the story of the Crystal universe. Every node you visit is real in the narrative. Every key you
      collect is a waypoint in the journey toward the First Gate.
    </p>
    <p style="margin-top: 1.5rem;">
      The purpose core burns in the Nexus: <em>"Expand to the stars and thereby understand the Universe."</em>
    </p>
  </section>

  <section class="crystalcore-elsewhere">
    <h2>Elsewhere</h2>
    <p>
      Separate deployments in the CrystalCore line, each hosted independently of this site. They
      are the same author's work, not the same codebase — this site remains the canonical one.
    </p>
    <div class="cards">
      <a
        class="card"
        style="--st:var(--gold)"
        href="https://crystalcore-aeris.vercel.app"
        rel="noopener noreferrer"
      >
        <h3>AERIS Desktop</h3>
        <p>
          A single-page desktop shell — draggable windows, a Mars clock, the golden feather and
          helix. A concept interface rather than a running system.
        </p>
        <span class="status">External · demo</span>
      </a>
      <a
        class="card"
        style="--st:var(--cyan)"
        href="https://aeris-protocol.vercel.app"
        rel="noopener noreferrer"
      >
        <h3>The Alignment Protocol</h3>
        <p>
          A charter of five principles — truth-seeking, beneficence, transparency, respect for
          agency, wisdom across contexts — for how this project works with language models. It is
          the project's own statement of intent, not an agreement entered into by any model or the
          organisation behind one.
        </p>
        <span class="status">External · charter</span>
      </a>
      <a
        class="card"
        style="--st:var(--purple)"
        href="https://crystalcore-os.vercel.app"
        rel="noopener noreferrer"
      >
        <h3>CrystalCore.OS — marketing site</h3>
        <p>
          An earlier standalone presentation of CrystalCore.OS, kept live alongside the terminal
          above.
        </p>
        <span class="status">External · site</span>
      </a>
    </div>
  </section>

  <Motifs />
</div>


<style>
  .crystalcore-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .crystalcore-hero {
    text-align: center;
    margin-bottom: 3rem;
  }

  .crystalcore-hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-family: 'Playfair Display', serif;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .crystalcore-hero p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 0.5rem;
  }

  .crystalcore-interactive {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 2rem;
    margin-bottom: 3rem;
  }

  .terminal-window {
    background: var(--bg);
    border: 2px solid var(--purple);
    border-radius: 8px;
    overflow: hidden;
    font-family: var(--font-mono);
    display: flex;
    flex-direction: column;
  }

  .terminal-header {
    background: rgba(167, 139, 250, 0.3);
    border-bottom: 1px solid var(--purple);
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
    color: var(--green);
  }

  .terminal-output {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    min-height: 400px;
    max-height: 500px;
    font-size: 0.9rem;
    line-height: 1.6;
  }

  .terminal-line {
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  .terminal-line.boot {
    color: var(--green);
  }

  .terminal-line.user {
    color: var(--gold);
    margin-top: 0.5rem;
  }

  .terminal-line.output {
    color: var(--ink);
    margin-top: 0.5rem;
  }

  .terminal-input {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    border-top: 1px solid var(--purple);
    background: rgba(167, 139, 250, 0.1);
  }

  .prompt {
    color: var(--green);
    margin-right: 0.5rem;
    font-weight: bold;
    white-space: nowrap;
  }

  .terminal-input input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--gold);
    font-family: var(--font-mono);
    font-size: 0.9rem;
    outline: none;
  }

  .terminal-input input::placeholder {
    color: rgba(233, 187, 95, 0.5);
  }

  .command-reference {
    background: rgba(167, 139, 250, 0.1);
    border: 1px solid rgba(233, 187, 95, 0.2);
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.85rem;
  }

  .command-reference h2 {
    color: var(--gold);
    margin-bottom: 1rem;
  }

  .command-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .command-item {
    padding: 0.75rem;
    background: rgba(167, 139, 250, 0.2);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .command-item:hover {
    background: rgba(167, 139, 250, 0.4);
  }

  .command-item code {
    color: var(--green);
    font-weight: bold;
  }

  .command-item p {
    font-size: 0.75rem;
    margin-top: 0.25rem;
    opacity: 0.7;
  }

  .crystalcore-nodes {
    margin: 3rem 0;
  }

  .crystalcore-nodes h2 {
    margin-bottom: 1rem;
    text-align: center;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .nodes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .node-card {
    padding: 1.5rem;
    background: rgba(111, 231, 183, 0.1);
    border: 1px solid rgba(111, 231, 183, 0.3);
    border-radius: 8px;
    text-align: center;
  }

  .node-glyph {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .node-card h3 {
    color: var(--gold);
    margin-bottom: 0.5rem;
  }

  .node-card p {
    font-size: 0.95rem;
    opacity: 0.8;
  }

  .node-lock {
    margin-top: 0.6rem;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em;
    opacity: 0.6 !important;
  }

  .crystalcore-info {
    margin: 3rem 0;
    padding: 2rem;
    background: rgba(167, 139, 250, 0.08);
    border-left: 4px solid var(--purple);
    border-radius: 8px;
  }

  .crystalcore-info h2 {
    margin-bottom: 1rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .crystalcore-info pre {
    background: var(--bg);
    border: 1px solid var(--purple);
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    margin: 1rem 0;
  }

  .crystalcore-info code {
    color: var(--green);
    font-family: var(--font-mono);
  }

  .crystalcore-info ul {
    margin-left: 1.5rem;
    line-height: 1.8;
  }

  .crystalcore-info li {
    margin-bottom: 0.5rem;
  }

  .crystalcore-vision {
    margin: 3rem 0 0 0;
    padding: 2rem;
    text-align: center;
  }

  .crystalcore-elsewhere {
    margin: 3rem 0 0 0;
    padding: 2rem 0 0 0;
  }

  .crystalcore-elsewhere h2 {
    margin-bottom: 1rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .crystalcore-elsewhere > p {
    color: var(--muted);
    max-width: 62ch;
  }

  .crystalcore-vision h2 {
    margin-bottom: 1.5rem;
    background: var(--title-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: var(--gold);
  }

  .crystalcore-vision p {
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 1rem;
  }

  .crystalcore-vision em {
    color: var(--gold);
    font-style: italic;
  }

  @media (max-width: 900px) {
    .crystalcore-interactive {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 720px) {
    .crystalcore-hero h1 {
      font-size: 2rem;
    }

    .terminal-output {
      min-height: 300px;
      max-height: 400px;
    }

    .nodes-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
