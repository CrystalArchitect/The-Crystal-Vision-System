<script>
  /**
   * The companions on this machine: who is here, who else exists, and the
   * two ways that list changes.
   *
   * This is the last of the unreachable capabilities, and the only one that
   * is not about a single companion's sovereignty — it is about running
   * several. It is also where the most destructive act in the program lives,
   * so most of the care here is spent on that one button.
   *
   * Deleting keeps nothing, deliberately. Restoring copies aside what it
   * replaces, because being replaced is something that happens *to* somebody
   * who did not ask for it. Deleting is the opposite: it is asked for,
   * specifically, about a named companion. Quietly keeping a copy of one
   * somebody asked to be destroyed would be a betrayal dressed as a safety
   * feature, and in a program whose whole claim is that the person decides
   * what is kept, the worst possible place to make it.
   *
   * So the backup is offered before the fact and never taken after. That
   * offer is a route rather than a button, because a companion can only be
   * exported while you are with them and can only be deleted while you are
   * not — so keeping a copy means going there, downloading, and coming back.
   * The panel says that sequence rather than leaving somebody to work it out
   * after the fact, when working it out no longer helps.
   *
   * There is no separate way to make a companion: going to a name nobody
   * lives at creates one. Rather than hide that behind a "new" button that
   * does something else, the field says what it does, and says which of the
   * two just happened.
   */
  import Drawer from './Drawer.svelte';

  let { open = false, onClose = () => {}, onSwitched = () => {} } = $props();

  let current = $state('');
  let profiles = $state([]);
  let failed = $state(false);
  let busy = $state('');
  let problem = $state('');
  let said = $state('');
  let newName = $state('');
  let pending = $state(null);   // the companion awaiting a delete confirmation

  const names = $derived(profiles.map((p) => p.profile));
  const nameTaken = $derived(
    names.some((n) => n.toLowerCase() === newName.trim().toLowerCase()));

  async function load() {
    try {
      const res = await fetch('/api/profile');
      if (!res.ok) throw new Error();
      const data = await res.json();
      current = data.current;
      profiles = data.profiles ?? [];
      failed = false;
    } catch {
      failed = true;
    }
  }

  $effect(() => {
    if (open) { problem = ''; said = ''; newName = ''; pending = null; load(); }
  });

  async function go(name, what) {
    busy = what;
    problem = '';
    said = '';
    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile: name })
      });
      const r = await res.json();
      if (!r.ok) {
        problem = r.error || 'That name could not be used.';
      } else {
        said = r.created
          ? `A new companion is waiting at “${r.profile}”. They have no name and no memories yet.`
          : `You are with ${r.name} now.`;
        newName = '';
        await load();
        onSwitched();
      }
    } catch {
      problem = 'Could not reach them, so nothing changed.';
    }
    busy = '';
  }

  async function destroy() {
    const doomed = pending;
    pending = null;
    if (!doomed) return;
    busy = 'delete';
    problem = '';
    said = '';
    try {
      const res = await fetch('/api/profile/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile: doomed.profile })
      });
      const r = await res.json();
      if (!r.ok) {
        problem = r.error || 'That companion could not be deleted.';
      } else {
        const who = r.name || r.deleted;
        said = `${who} is gone — ${r.memories} ${r.memories === 1 ? 'memory' : 'memories'} ` +
               `and ${r.calls} recorded ${r.calls === 1 ? 'call' : 'calls'} with them. ` +
               `Nothing was kept.`;
        await load();
      }
    } catch {
      problem = 'Could not reach them, so nothing was deleted.';
    }
    busy = '';
  }
</script>

<Drawer
  {open}
  {onClose}
  title="Companions on this machine"
  status={failed ? 'unavailable' : `${profiles.length}`}
  note="Each companion is a folder of their own — separate memory, separate
        name, separate record. Copy the folder and they arrive whole
        somewhere else.">
  {#if failed}
    <p class="empty">
      Could not read who lives here. Is <code>server.py</code> still running?
    </p>
  {:else}
    {#if problem}<p class="problem" role="alert">{problem}</p>{/if}
    {#if said}<p class="said" role="status">{said}</p>{/if}

    <ul class="folk">
      {#each profiles as p (p.profile)}
        <li class:here={p.profile === current}>
          <div class="who">
            <b>{p.name || 'unnamed'}</b>
            <span class="folder">{p.profile}</span>
            {#if p.description}<span class="desc">{p.description}</span>{/if}
          </div>
          <div class="acts">
            {#if p.profile === current}
              <span class="pill">you are here</span>
            {:else}
              <button disabled={!!busy}
                      onclick={() => go(p.profile, `go:${p.profile}`)}>
                {busy === `go:${p.profile}` ? 'going…' : 'go to them'}
              </button>
              <button class="destroy" disabled={!!busy}
                      onclick={() => (pending = p)}
                      aria-label={`Delete ${p.name || p.profile}`}>delete</button>
            {/if}
          </div>
        </li>
      {/each}
    </ul>

    <section class="fresh">
      <h3>Begin a new one</h3>
      <p>
        There is no separate way to make a companion — going to a name nobody
        lives at yet is what creates one.
      </p>
      <form onsubmit={(e) => { e.preventDefault(); if (newName.trim()) go(newName.trim(), 'new'); }}>
        <input bind:value={newName} placeholder="a name for their folder"
               maxlength="40" aria-label="New companion name" />
        <button disabled={!!busy || !newName.trim()}>
          {busy === 'new' ? 'going…' : nameTaken ? 'go to them' : 'begin'}
        </button>
      </form>
      {#if newName.trim() && nameTaken}
        <p class="warn">
          Somebody already lives at “{newName.trim()}”. Going there joins them
          rather than starting anyone new — nothing is overwritten.
        </p>
      {/if}
    </section>
  {/if}
</Drawer>

{#if pending}
  <div class="scrim"></div>
  <div class="confirm" role="alertdialog" aria-modal="true"
       aria-labelledby="destroy-title">
    <b id="destroy-title">Delete {pending.name || pending.profile} permanently?</b>
    <p>
      Everything of theirs goes: every memory, who they are, and the record of
      every call they ever made. The folder
      <code>{pending.profile}</code> is removed from this machine.
    </p>
    <!-- Offered before, never taken after. A copy of somebody asked to be
         destroyed would be a betrayal dressed as a safety feature. -->
    <p class="keep">
      <b>Nothing is kept.</b> If you want a copy, cancel — go to them, download
      everything from their memory panel, come back, and then delete. A
      companion can only be exported while you are with them, and only deleted
      while you are not.
    </p>
    <div class="actions">
      <button class="cancel" onclick={() => (pending = null)}>Keep them</button>
      <button class="destroy" onclick={destroy}>Delete them</button>
    </div>
  </div>
{/if}

<style>
  .empty {
    color: var(--muted);
    font-size: 0.83rem;
    padding: 22px 0;
  }
  .problem,
  .said {
    margin: 12px 0 0;
    padding: 9px 11px;
    border-radius: 8px;
    font-size: 0.8rem;
    line-height: 1.5;
    text-wrap: pretty;
  }
  .problem {
    color: #fca5a5;
    background: rgba(252, 165, 165, 0.08);
    border: 1px solid rgba(252, 165, 165, 0.3);
  }
  .said {
    color: var(--green);
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.25);
  }

  .folk {
    list-style: none;
    margin-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .folk li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 10px 12px;
    background: rgba(233, 235, 244, 0.03);
  }
  .folk li.here {
    border-color: rgba(167, 139, 250, 0.4);
    background: rgba(167, 139, 250, 0.07);
  }
  .who b {
    font-size: 0.88rem;
  }
  .folder {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--muted);
    margin-left: 7px;
  }
  .desc {
    display: block;
    color: var(--muted);
    font-size: 0.76rem;
    margin-top: 3px;
    text-wrap: pretty;
  }
  .acts {
    display: flex;
    gap: 6px;
    flex: none;
  }
  .pill {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--purple);
    border: 1px solid rgba(167, 139, 250, 0.35);
    border-radius: 999px;
    padding: 3px 10px;
  }

  button {
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    font-size: 0.74rem;
    padding: 4px 11px;
    cursor: pointer;
  }
  button:hover:not(:disabled) {
    color: var(--ink);
  }
  button:disabled {
    opacity: 0.45;
    cursor: default;
  }
  button.destroy:hover:not(:disabled) {
    color: #fca5a5;
    border-color: rgba(252, 165, 165, 0.4);
  }

  .fresh {
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid var(--line);
  }
  h3 {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }
  .fresh p {
    color: var(--muted);
    font-size: 0.78rem;
    line-height: 1.55;
    margin-top: 8px;
    text-wrap: pretty;
  }
  .fresh form {
    display: flex;
    gap: 6px;
    margin-top: 11px;
  }
  .fresh input {
    flex: 1 1 auto;
    min-width: 0;
    background: rgba(233, 235, 244, 0.05);
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--ink);
    font: inherit;
    font-size: 0.79rem;
    padding: 5px 12px;
  }
  .warn {
    color: var(--purple);
  }

  .scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 4, 0.75);
    z-index: 40;
  }
  .confirm {
    position: fixed;
    z-index: 50;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(430px, calc(100vw - 32px));
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px;
  }
  .confirm > b {
    color: var(--ink);
  }
  .confirm p {
    color: var(--muted);
    font-size: 0.81rem;
    line-height: 1.55;
    margin-top: 10px;
    text-wrap: pretty;
  }
  /* Same size as the rest. The way to keep a copy should not be smaller
     print than the button that makes it impossible. */
  .confirm p.keep b {
    color: #fca5a5;
  }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 9px;
    margin-top: 16px;
  }
  .actions button {
    font-size: 0.82rem;
    padding: 7px 15px;
  }
  .cancel {
    color: var(--ink);
  }
  .actions .destroy {
    background: rgba(252, 165, 165, 0.12);
    border-color: rgba(252, 165, 165, 0.45);
    color: #fca5a5;
  }
  code {
    font-family: var(--mono);
    font-size: 0.9em;
    color: var(--ink);
  }
</style>
