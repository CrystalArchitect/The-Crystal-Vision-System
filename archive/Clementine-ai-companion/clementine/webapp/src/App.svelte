<script>
  import Avatar from './lib/Avatar.svelte';
  import Chat from './lib/Chat.svelte';
  import Companions from './lib/Companions.svelte';
  import Identity from './lib/Identity.svelte';
  import Memory from './lib/Memory.svelte';
  import Record from './lib/Record.svelte';
  import Restore from './lib/Restore.svelte';
  import Senses from './lib/Senses.svelte';

  // One button and one drawer, deliberately. The window has had no structure
  // at all until now, and the first thing added should be the smallest thing
  // that reaches the memory — not a navigation system built for surfaces
  // that do not exist yet.
  let memoryOpen = $state(false);
  let recordOpen = $state(false);
  let restoreOpen = $state(false);
  let identityOpen = $state(false);
  let folkOpen = $state(false);

  let presence = $state('idle'); // idle | thinking | speaking
  let name = $state('Clementine');
  let model = $state('');
  let profile = $state('');
  let online = $state(null); // null=checking, true, false

  // Where the model actually is. Asked, never assumed — this used to be
  // hardcoded as "local · 127.0.0.1", which would have kept saying so from a
  // server on the other side of the world.
  let destination = $state(null); // null=unknown, 'local', or a hostname
  let auditCount = $state(null);
  let auditIntact = $state(null);
  const pagesPreview =
    typeof location !== 'undefined' && location.hostname.endsWith('github.io');


  async function loadStatus() {
    try {
      const res = await fetch('/api/status');
      if (!res.ok) throw new Error();
      const data = await res.json();
      name = data.name || 'Clementine';
      model = data.model || '';
      profile = data.profile || '';
      online = true;
    } catch {
      online = false;
    }
    try {
      const h = await fetch('/api/health').then((r) => r.json());
      destination = h.destination ?? null;
      auditCount = h.audit_entries ?? null;
    } catch {
      destination = null;
    }
    try {
      const a = await fetch('/api/audit?limit=1').then((r) => r.json());
      auditIntact = a.intact;
    } catch {
      auditIntact = null;
    }
  }
  loadStatus();
</script>

<header>
  <div class="who">
    <b>{name}</b>
    <span class="sub">sovereign companion</span>
  </div>
  <div class="status" role="status">
    {#if pagesPreview}
      <span class="chip down" title="GitHub Pages is static. The brain is python server.py on your machine.">face only · brain not here</span>
    {:else if online === true}
      <span class="chip ok">{model}{profile && profile !== 'default' ? ` · ${profile}` : ''}</span>
    {:else if online === false}
      <span class="chip down" title="Start it with: python server.py">brain offline</span>
      <button class="retry" onclick={loadStatus}>retry</button>
    {:else}
      <span class="chip">waking…</span>
    {/if}
    {#if !pagesPreview}
    {#if destination === 'local'}
      <span class="chip ok" title="The model runs on this same machine.">on this machine</span>
    {:else if destination}
      <span class="chip away" title="The model runs elsewhere. Requests need your consent and are logged.">
        via {destination}
      </span>
    {:else}
      <span class="chip" title="Could not determine where the model runs.">location unknown</span>
    {/if}
    {/if}
    {#if auditIntact === false}
      <span class="chip down" title="An entry was altered or removed after being written.">record broken</span>
    {/if}
    <button
      class="memory"
      onclick={() => (memoryOpen = true)}
      title="See everything they hold about you, and take any of it back">
      memory
    </button>
    <button
      class="memory"
      onclick={() => (identityOpen = true)}
      title="Their name and pronouns — chosen by you, or by them">
      who
    </button>
    <button
      class="memory"
      onclick={() => (folkOpen = true)}
      title="Every companion on this machine — go to one, begin one, or delete one">
      companions
    </button>
    <button
      class="memory"
      onclick={() => (recordOpen = true)}
      title="Read every call they have made, allowed or refused">
      record
    </button>
  </div>
</header>

<Memory
  open={memoryOpen}
  onClose={() => (memoryOpen = false)}
  onRestore={() => { memoryOpen = false; restoreOpen = true; }} />
<Record open={recordOpen} onClose={() => (recordOpen = false)} />
<!-- Switching replaces the companion the whole window is describing, so
     everything is re-read rather than any one field patched. -->
<Companions
  open={folkOpen}
  onClose={() => (folkOpen = false)}
  onSwitched={loadStatus} />
<Identity
  open={identityOpen}
  onClose={() => (identityOpen = false)}
  onChanged={loadStatus} />
<!-- After a restore the header is describing whoever was here before, so the
     whole status is re-read rather than patching the name in place. -->
<Restore
  open={restoreOpen}
  currentName={name}
  onClose={() => { restoreOpen = false; loadStatus(); }} />

<main>
  <aside class="presence">
    <Avatar state={presence} {name} />
    <Senses />
  </aside>
  <Chat {name} pagesPreview={pagesPreview} onStateChange={(s) => (presence = s)} />
</main>

<footer>
  {#if pagesPreview}
    This is their face, published as a static preview. The brain is
    <code>python server.py</code> after you clone
    <a href="https://github.com/CrystalArchitect/Clementine-ai-companion">the repository</a>.
    Nothing you type here reaches a model. Non solus.
  {:else if destination === 'local'}
    The model runs on this machine, so nothing you say here leaves it.
  {:else if destination}
    The model runs on <b>{destination}</b> — a machine you control. Your words
    travel there and no further.
  {:else}
    Where the model runs could not be determined, so nothing is claimed about it.
  {/if}
  {#if !pagesPreview}
  Their memory lives in a folder you own{#if auditCount}, and every call they
  make is appended to <code>audit.jsonl</code> beside it — {auditCount} so far.
  It is plain text: open it yourself and read every line. Reading it in this
  window is not built yet{/if}. Non solus.
  {/if}

</footer>

<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 14px 20px;
    border-bottom: 1px solid var(--line);
  }
  .who b {
    color: var(--purple);
    font-size: 1.05rem;
  }
  .who .sub {
    color: var(--muted);
    font-size: 0.85rem;
    margin-left: 8px;
  }
  .status {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .chip {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--muted);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 3px 10px;
  }
  .chip.ok {
    color: var(--green);
    border-color: rgba(52, 211, 153, 0.3);
  }
  .chip.down {
    color: #f0a5a5;
    border-color: rgba(240, 165, 165, 0.3);
  }
  /* The model is somewhere other than this machine — not wrong, but worth
     seeing at a glance rather than discovering later. */
  .chip.away {
    color: var(--purple);
    border-color: rgba(167, 139, 250, 0.35);
  }
  .retry {
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    font-size: 0.72rem;
    padding: 3px 10px;
    cursor: pointer;
  }
  /* Shaped like the chips beside it rather than announced as a new region.
     It reaches something that already existed and was simply unreachable. */
  .memory {
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--purple);
    font-size: 0.72rem;
    padding: 3px 11px;
    cursor: pointer;
  }
  .memory:hover {
    border-color: rgba(167, 139, 250, 0.45);
  }

  main {
    flex: 1;
    display: flex;
    min-height: 0;
  }

  .presence {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    width: 340px;
    flex-shrink: 0;
    padding: 24px;
    border-right: 1px solid var(--line);
  }

  footer {
    padding: 10px 20px;
    color: var(--muted);
    font-size: 0.78rem;
    border-top: 1px solid var(--line);
  }
  /* A filename the person is being told to go and open should look like one,
     rather than inheriting the browser's default serif-ish monospace against
     a dark background. */
  footer code {
    font-family: var(--mono);
    font-size: 0.95em;
    color: var(--ink);
    background: rgba(233, 235, 244, 0.07);
    border-radius: 3px;
    padding: 1px 4px;
  }

  @media (max-width: 760px) {
    main {
      flex-direction: column;
      overflow-y: auto;
    }
    .presence {
      width: 100%;
      border-right: none;
      border-bottom: 1px solid var(--line);
      padding: 16px;
    }
  }
</style>
