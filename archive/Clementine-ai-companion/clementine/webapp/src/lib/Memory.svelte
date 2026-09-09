<script>
  /**
   * What they hold about you, and the ability to take any of it back.
   *
   * This is the first surface in this window that can destroy something. The
   * server's `forget` is immediate and permanent — there is no undo, no bin,
   * no second chance — so the work here is mostly about not deleting the
   * wrong thing.
   *
   * The hazard these guards were built for has since been closed at the
   * format level, and this note says so rather than implying they are still
   * load-bearing. Handles used to be positions in a list — n1, n2, n3 — so
   * deleting n2 renumbered everything after it and a list fetched a moment
   * ago could already describe different memories than the server did.
   * Confirming against a stale list permanently destroyed a memory nobody
   * chose. Notes and reflections now carry identifiers that keep meaning the
   * same memory, so `forget` removes what was named or nothing at all.
   *
   * The three guards stay, downgraded from necessary to cheap:
   *
   *   1. The confirmation names the memory in full, so the person is agreeing
   *      to specific words rather than to a row in a list. This was never
   *      really about the handle, and is the one that still earns its place.
   *   2. Immediately before deleting, the list is re-read and the handle
   *      checked to still mean the same words. Now catches a memory already
   *      forgotten in another tab, rather than a catastrophe.
   *   3. After deleting, the server's report of what it removed is compared
   *      against what was agreed to, and any disagreement is stated loudly.
   *      With stable handles this should be unreachable, which is the best
   *      reason to leave it in: if it ever fires, something is wrong that
   *      nobody predicted, and the person is told rather than not.
   *
   * Removing them would save a request and lose the ability to notice being
   * wrong. That is a poor trade on the one screen here that destroys things.
   */
  import Drawer from './Drawer.svelte';

  let { open = false, onClose = () => {}, onRestore = () => {} } = $props();

  let facts = $state([]);
  let notes = $state([]);
  let reflections = $state([]);
  let loading = $state(false);
  let failed = $state(false);
  let pending = $state(null); // the memory awaiting confirmation
  let working = $state(false);
  let warning = $state('');
  let said = $state('');

  const total = $derived(facts.length + notes.length + reflections.length);

  async function read() {
    const res = await fetch('/api/memories');
    if (!res.ok) throw new Error('unreachable');
    return await res.json();
  }

  async function load() {
    loading = true;
    failed = false;
    try {
      const data = await read();
      facts = data.facts ?? [];
      notes = data.notes ?? [];
      reflections = data.reflections ?? [];
    } catch {
      failed = true;
    }
    loading = false;
  }

  $effect(() => {
    if (open) load();
  });

  /**
   * Does `handle` still mean these exact words on the server?
   *
   * Every handle is now stable — a fact's key, or a note or reflection's
   * identifier — so finding it is enough to know the right memory is in
   * hand. The text is still compared because a handle proves which memory
   * and not what it currently says: a note reworded elsewhere since the
   * panel was opened would otherwise be deleted on the strength of words it
   * no longer holds, and the person deserves to re-read it first.
   */
  function stillMeans(fresh, item) {
    const group = fresh[item.kind === 'fact' ? 'facts'
      : item.kind === 'note' ? 'notes' : 'reflections'] ?? [];
    const found = group.find((m) => m.handle === item.handle);
    if (!found) return false;
    return item.kind === 'fact' ? found.handle === item.handle
      : found.text === item.text;
  }

  /** The server reports what it removed; check it is what was agreed. */
  function removedWhatWasAgreed(forgotten, item) {
    const said = String(forgotten || '');
    return item.kind === 'fact'
      ? said.includes(item.handle)
      : said.includes(item.text);
  }

  function ask(kind, memory) {
    warning = '';
    said = '';
    pending = { kind, handle: memory.handle, text: memory.text };
  }

  async function forget() {
    const item = pending;
    pending = null;
    if (!item) return;
    working = true;
    warning = '';
    said = '';

    try {
      // Guard 2 — re-read and re-check before destroying anything.
      const fresh = await read();
      if (!stillMeans(fresh, item)) {
        warning =
          'That memory shifted position before it could be forgotten, so ' +
          'nothing was deleted. The list below has been refreshed — check ' +
          'it and try again.';
        await load();
        working = false;
        return;
      }

      const res = await fetch('/api/forget', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ handle: item.handle })
      });
      const data = await res.json();

      if (!data.ok) {
        warning = 'Nothing matched that handle, so nothing was forgotten.';
      } else if (!removedWhatWasAgreed(data.forgotten, item)) {
        // Guard 3 — the wrong thing went. Say exactly what, because a person
        // told what they lost can write it back, and one told nothing cannot.
        warning =
          `You agreed to forget “${item.text}”, but the server removed ` +
          `${data.forgotten} instead. This should not happen. If that was ` +
          `not what you meant to lose, add it again now, while you can still ` +
          `read it here.`;
      } else {
        said = `Forgotten: ${data.forgotten}`;
      }
    } catch {
      warning = 'Could not reach them, so nothing was forgotten.';
    }

    await load();
    working = false;
  }
</script>

<Drawer
  {open}
  {onClose}
  title="What they remember"
  status={loading ? 'reading…' : failed ? 'unavailable' : `${total} in all`}
  note="Their memory is a folder on this machine. Forgetting is immediate
        and cannot be undone.">
  {#if warning}
    <p class="warning" role="alert">{warning}</p>
  {/if}
  {#if said}
    <p class="said" role="status">{said}</p>
  {/if}

  {#if failed}
    <p class="empty">
      Their memory could not be read. Is <code>server.py</code> still
      running?
    </p>
  {:else if !loading && total === 0}
    <p class="empty">
      They hold nothing about you yet. What you tell them to remember
      will appear here, and you can take any of it back.
    </p>
  {:else}
    {#each [['Told to them', 'fact', facts], ['Noticed', 'note', notes], ['Concluded on their own', 'reflection', reflections]] as [label, kind, items] (kind)}
      {#if items.length}
        <h3>{label}</h3>
        <ul>
          {#each items as memory (memory.handle + memory.text)}
            <li>
              <div class="text">
                {memory.text}
                {#if memory.tags?.length}
                  <span class="tags">
                    {#each memory.tags as tag (tag)}<em>#{tag}</em>{/each}
                  </span>
                {/if}
              </div>
              <button
                class="forget"
                disabled={working}
                onclick={() => ask(kind, memory)}
                aria-label={`Forget: ${memory.text}`}>forget</button>
            </li>
          {/each}
        </ul>
      {/if}
    {/each}
  {/if}

  <!--
    Export sits here rather than behind a third button in the header. Taking
    your memory with you is a thing you do *to* the memory, and a person
    looking for it will look where the memory is.

    A plain link, not a fetch: the server already sets the filename in
    Content-Disposition, so an anchor gets the right name, streams straight
    to disk, and works if the JavaScript ever does not.
  -->
  <section class="leaving">
    <h3>Take it with you</h3>
    <p>
      One file with everything in it: what they remember, what they have
      concluded, your conversations word for word, and who they are — their
      name, their pronouns, how you asked them to speak. Enough to put this
      companion back together somewhere else.
    </p>
    <p class="plain">
      It is unencrypted JSON you can open in any text editor, which is the
      point — nothing about you should need our software to be readable. It
      also means the file protects nothing by itself. Everything the consent
      gate refuses to send anywhere is in it, so once it leaves that folder
      it is only as private as wherever you put it.
    </p>
    <p class="plain">
      It also notes where your consent record stood — how many calls, and the
      last one's fingerprint, not the calls themselves. That lets this file
      later tell you whether anything has been taken off the end of that
      record, which the record cannot tell you about itself. It can only
      vouch for what it saw, so a more recent backup witnesses more.
    </p>
    <a class="download" href="/api/export" download>Download everything</a>
    <!-- Restoring is offered from here because this is where a person thinks
         about backups, but it is a button rather than part of the section:
         it replaces everyone here rather than adding to them, and should not
         sit one careless click away from "download". -->
    <p class="back">
      Going the other way —
      <button class="asLink" onclick={onRestore}>restore from a file</button>
      — replaces whoever is here now, so it asks first and keeps a copy.
    </p>
  </section>
</Drawer>

{#if pending}
  <div class="scrim confirming"></div>
  <div class="confirm" role="alertdialog" aria-modal="true"
       aria-labelledby="confirm-title">
    <b id="confirm-title">Forget this permanently?</b>
    <blockquote>{pending.text}</blockquote>
    <p>This cannot be undone. There is no copy and no bin to recover it from.</p>
    <div class="actions">
      <button class="cancel" onclick={() => (pending = null)}>Keep it</button>
      <button class="destroy" onclick={forget}>Forget it</button>
    </div>
  </div>
{/if}

<style>
  /* The panel shell — scrim, header, scrolling body, footer — lives in
     Drawer.svelte. What remains here is only what is particular to showing
     memories and to destroying one. */
  .scrim.confirming {
    position: fixed;
    inset: 0;
    z-index: 40;
    background: rgba(0, 0, 4, 0.75);
  }
  h3 {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin: 18px 0 8px;
  }
  ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  li {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    background: rgba(233, 235, 244, 0.04);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 9px 11px;
  }
  .text {
    font-size: 0.85rem;
    line-height: 1.45;
    text-wrap: pretty;
  }
  .tags {
    display: block;
    margin-top: 4px;
  }
  .tags em {
    font-style: normal;
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--purple);
    margin-right: 6px;
  }
  .forget {
    flex: none;
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    font-size: 0.72rem;
    padding: 3px 10px;
    cursor: pointer;
  }
  .forget:hover:not(:disabled) {
    color: #fca5a5;
    border-color: rgba(252, 165, 165, 0.4);
  }
  .forget:disabled {
    opacity: 0.4;
    cursor: default;
  }

  .empty {
    color: var(--muted);
    font-size: 0.83rem;
    line-height: 1.6;
    padding: 22px 0;
    text-wrap: pretty;
  }

  .leaving {
    margin-top: 26px;
    padding-top: 16px;
    border-top: 1px solid var(--line);
  }
  .leaving p {
    color: var(--muted);
    font-size: 0.79rem;
    line-height: 1.55;
    margin-top: 7px;
    text-wrap: pretty;
  }
  /* The caveat is the same size as the offer. Shrinking it would be a way of
     saying it without saying it. */
  .leaving p.plain {
    color: var(--muted);
  }
  .download {
    display: inline-block;
    margin-top: 13px;
    border: 1px solid rgba(167, 139, 250, 0.4);
    border-radius: 999px;
    color: var(--purple);
    text-decoration: none;
    font-size: 0.79rem;
    padding: 6px 15px;
  }
  .download:hover {
    background: rgba(167, 139, 250, 0.1);
  }
  .back {
    margin-top: 14px;
  }
  .asLink {
    background: none;
    border: 0;
    padding: 0;
    font: inherit;
    color: var(--purple);
    cursor: pointer;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .warning,
  .said {
    /* No horizontal margin: these used to sit outside the scrolling body and
       needed to match its inset by hand. They are inside it now, and 18px of
       their own would sit on top of the 18px it already provides. */
    margin: 12px 0 0;
    padding: 9px 11px;
    border-radius: 8px;
    font-size: 0.8rem;
    line-height: 1.5;
    text-wrap: pretty;
  }
  .warning {
    color: #fca5a5;
    background: rgba(252, 165, 165, 0.08);
    border: 1px solid rgba(252, 165, 165, 0.3);
  }
  .said {
    color: var(--green);
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.25);
  }

  .confirm {
    position: fixed;
    z-index: 50;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(400px, calc(100vw - 32px));
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px;
  }
  .confirm b {
    color: var(--ink);
  }
  blockquote {
    margin: 11px 0;
    padding: 9px 12px;
    border-left: 2px solid var(--purple);
    background: rgba(233, 235, 244, 0.04);
    font-size: 0.86rem;
    line-height: 1.5;
    text-wrap: pretty;
  }
  .confirm p {
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1.5;
  }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 9px;
    margin-top: 16px;
  }
  .actions button {
    border-radius: 999px;
    padding: 7px 15px;
    font-size: 0.82rem;
    cursor: pointer;
    border: 1px solid var(--line);
  }
  .cancel {
    background: transparent;
    color: var(--ink);
  }
  .destroy {
    background: rgba(252, 165, 165, 0.12);
    border-color: rgba(252, 165, 165, 0.45);
    color: #fca5a5;
  }

</style>
