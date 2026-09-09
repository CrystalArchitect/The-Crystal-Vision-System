<script>
  /**
   * Bringing a companion back from a file.
   *
   * Export without import is not half a feature, it is a broken promise: a
   * person could take a backup and never restore it, which is false
   * confidence rather than portability. This closes that.
   *
   * It is also the only control in this window that replaces everything at
   * once — identity and every memory, in one act. So the shape here is: read
   * the file, say plainly who is in it and who they would replace, and make
   * the way back visible rather than merely available.
   *
   * The file is read in the browser and parsed here. Nothing is uploaded
   * anywhere; the bundle only reaches the local server, on the same machine,
   * at the moment the person says yes.
   *
   * The server does the load-bearing work and did not always: it now refuses
   * a structurally damaged bundle before writing anything, and copies the
   * existing companion into replaced-<stamp>/ first. This component checks
   * the file too, because being told "that file is damaged" before agreeing
   * to anything is kinder than being told after, and it can say so without
   * the round trip. It does not rely on that check — the server's refusal is
   * the one that protects the memory.
   */
  import Drawer from './Drawer.svelte';

  let { open = false, onClose = () => {}, currentName = 'Clementine' } = $props();

  let file = $state(null);      // the parsed bundle, once a file is chosen
  let filename = $state('');
  let problem = $state('');
  let working = $state(false);
  let done = $state(null);      // {name, replaced_backup} after a restore
  let witness = $state(null);   // {ok, sentence} — what the file attests to

  const counts = $derived(summarise(file));

  // Opening starts over. The drawer only removes its DOM, so without this a
  // second visit still shows the last restore's "they are here" banner and
  // no file picker — the panel would work exactly once per page load, and
  // the person who most needs to restore twice is the one whose first
  // attempt was the wrong file.
  $effect(() => {
    if (open) {
      file = null;
      filename = '';
      problem = '';
      done = null;
      working = false;
      witness = null;
    }
  });

  /**
   * Ask the file what it remembers about the consent record, and check.
   *
   * The chain in audit.jsonl cannot notice entries removed from its own end
   * — a truncated chain verifies perfectly. A backup taken earlier can,
   * because it wrote down where the record stood at the time. This is that
   * check, and it is offered whether or not the person goes on to restore:
   * asking a backup whether the record still agrees with it is a reason to
   * open one on its own.
   *
   * What it cannot do is stated wherever the answer is shown. It witnesses
   * up to the moment the backup was taken and is silent about everything
   * after, so entries added since and then removed leave no trace here
   * either.
   */
  async function askTheWitness(bundle) {
    const w = bundle?.audit;
    if (!w?.head || !w?.count) {
      witness = { ok: null, sentence:
        'This backup was taken before any calls were recorded, or by a ' +
        'version that did not note them, so it has nothing to attest to.' };
      return;
    }
    try {
      const record = await (await fetch('/api/audit')).json();
      const hashes = (record.entries ?? []).map((e) => e.hash);
      const at = hashes.indexOf(w.head) + 1;
      if (at === 0) {
        witness = { ok: false, sentence:
          `The entry this backup witnessed is no longer in the record. It ` +
          `saw ${w.count} calls, and the last of them is gone.` };
      } else if (at !== w.count) {
        witness = { ok: false, sentence:
          `This backup saw that call as number ${w.count}; it is now number ` +
          `${at}. ${Math.abs(w.count - at)} entries have been ` +
          `${at < w.count ? 'removed from' : 'inserted into'} the record ` +
          `before it.` };
      } else {
        witness = { ok: true, sentence:
          `The record still agrees with this backup: the ${w.count} calls it ` +
          `witnessed are all present, in the same order.` };
      }
    } catch {
      witness = null;
    }
  }

  function summarise(bundle) {
    const m = bundle?.memory ?? {};
    return {
      name: bundle?.config?.name || 'an unnamed companion',
      notes: (m.notes ?? []).length,
      facts: Object.keys(m.facts ?? {}).length,
      reflections: (m.reflections ?? []).length,
      turns: (m.conversation ?? []).length,
      exported: bundle?.exported_at || ''
    };
  }

  /** The same shapes the server refuses, checked here to save a round trip
      and to say so before anything is agreed to — never instead of it. */
  function unusable(b) {
    if (!b || typeof b !== 'object') return 'That file is not a memory bundle.';
    if (b.format !== 'crystalcore-memory-bundle')
      return 'That file is not a Clementine memory bundle.';
    if (b.version !== 1)
      return `That bundle is version ${b.version}, and this version of the companion only understands 1.`;
    for (const key of ['config', 'memory']) {
      const v = b[key];
      if (v !== undefined && v !== null &&
          (typeof v !== 'object' || Array.isArray(v)))
        return `That file is damaged: its ${key} section is not an object.`;
    }
    const m = b.memory ?? {};
    for (const [field, ok] of [['notes', Array.isArray], ['reflections', Array.isArray],
                               ['conversation', Array.isArray], ['summaries', Array.isArray],
                               ['facts', (x) => typeof x === 'object' && !Array.isArray(x)]]) {
      if (field in m && !ok(m[field]))
        return `That file is damaged: ${field} is the wrong shape.`;
    }
    if (!b.config && !b.memory)
      return 'That bundle holds neither a companion nor a memory.';
    return '';
  }

  async function chose(event) {
    const chosen = event.target.files?.[0];
    file = null;
    problem = '';
    done = null;
    if (!chosen) return;
    filename = chosen.name;
    try {
      const parsed = JSON.parse(await chosen.text());
      const why = unusable(parsed);
      if (why) { problem = why; return; }
      file = parsed;
      askTheWitness(parsed);
    } catch {
      problem = 'That file could not be read as JSON. If it was downloaded, it may have arrived incomplete.';
    }
  }

  async function restore() {
    working = true;
    problem = '';
    try {
      const res = await fetch('/api/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(file)
      });
      const body = await res.json();
      if (!body.ok) {
        problem = body.error || 'The companion refused that file.';
      } else {
        done = body;
        file = null;
      }
    } catch {
      problem = 'Could not reach them, so nothing was changed.';
    }
    working = false;
  }
</script>

<Drawer
  {open}
  {onClose}
  title="Bring a companion back"
  note="Restoring replaces who is here now. What is replaced is copied aside
        first, so this can be undone.">
  {#if done}
    <div class="arrived" role="status">
      <b>{done.name || 'They'} is here.</b>
      <p>
        Their memory has been restored from <code>{filename}</code>.
      </p>
      {#if done.replaced_backup}
        <p>
          The companion who was here has not been thrown away. They are in
          <code>{done.replaced_backup}</code>, and importing the two files in
          that folder brings them back.
        </p>
      {:else}
        <p>There was no companion here before, so nothing was replaced.</p>
      {/if}
      <p class="quiet">
        The consent record was not touched. It belongs to this machine rather
        than to any one companion, so calls made before the restore are still
        listed — those calls did happen here.
      </p>
    </div>
  {:else}
    <p class="lead">
      Choose a file you exported earlier. It is read here on this machine and
      only sent to the companion running on it, at the moment you say yes.
    </p>

    <label class="pick">
      <input type="file" accept="application/json,.json" onchange={chose} />
      <span>Choose a backup file…</span>
    </label>
    {#if filename}<p class="chosen">{filename}</p>{/if}

    {#if problem}
      <p class="problem" role="alert">{problem}</p>
    {/if}

    {#if witness}
      <!-- Shown before the restore controls, because it is worth reading even
           if the person never restores: it is the only way to notice entries
           taken off the end of the record. -->
      <div class="witness" class:broken={witness.ok === false}
           class:fine={witness.ok === true} role="status">
        <h3>What this backup says about your consent record</h3>
        <p>{witness.sentence}</p>
        <p class="bound">
          A backup can only vouch for the record as it stood when the backup
          was taken. Calls made since are outside what it saw, so if any of
          those were removed, nothing here would show it. Take a backup more
          often and the unwitnessed gap gets shorter; it never closes.
        </p>
      </div>
    {/if}

    {#if file}
      <div class="preview">
        <h3>What is in this file</h3>
        <ul>
          <li><b>{counts.name}</b></li>
          <li>{counts.facts} facts, {counts.notes} notes, {counts.reflections} reflections</li>
          <li>{counts.turns} saved conversation turns</li>
          {#if counts.exported}<li>exported {counts.exported}</li>{/if}
        </ul>
      </div>

      <!-- Named on both sides. "Are you sure?" asks a person to agree to a
           category; naming who goes and who arrives asks them to agree to
           the actual thing, which is the only version they can catch a
           mistake in. -->
      <div class="swap">
        <p>
          Restoring this will replace <b>{currentName}</b>, who is here now,
          with <b>{counts.name}</b>.
        </p>
        <p class="quiet">
          {currentName} will be copied into a folder beside the memory first,
          and you will be told where. Nothing is thrown away.
        </p>
      </div>

      <button class="restore" disabled={working} onclick={restore}>
        {working ? 'Restoring…' : `Replace ${currentName} with ${counts.name}`}
      </button>
    {/if}
  {/if}
</Drawer>

<style>
  .lead,
  .chosen,
  .quiet {
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1.55;
    text-wrap: pretty;
  }
  .lead {
    margin-top: 14px;
  }
  .chosen {
    margin-top: 8px;
    font-family: var(--mono);
    font-size: 0.74rem;
  }

  .pick {
    display: inline-block;
    margin-top: 14px;
    cursor: pointer;
  }
  .pick input {
    position: absolute;
    width: 1px;
    height: 1px;
    opacity: 0;
  }
  .pick span {
    display: inline-block;
    border: 1px solid rgba(167, 139, 250, 0.4);
    border-radius: 999px;
    color: var(--purple);
    font-size: 0.79rem;
    padding: 6px 15px;
  }
  .pick:hover span,
  .pick input:focus-visible + span {
    background: rgba(167, 139, 250, 0.1);
  }

  .problem {
    margin-top: 14px;
    padding: 9px 11px;
    border-radius: 8px;
    color: #fca5a5;
    background: rgba(252, 165, 165, 0.08);
    border: 1px solid rgba(252, 165, 165, 0.3);
    font-size: 0.8rem;
    line-height: 1.5;
    text-wrap: pretty;
  }

  .witness {
    margin-top: 18px;
    padding: 11px 13px;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: rgba(233, 235, 244, 0.04);
  }
  .witness.fine {
    border-color: rgba(52, 211, 153, 0.25);
    background: rgba(52, 211, 153, 0.07);
  }
  .witness.broken {
    border-color: rgba(252, 165, 165, 0.35);
    background: rgba(252, 165, 165, 0.08);
  }
  .witness p {
    font-size: 0.81rem;
    line-height: 1.55;
    margin-top: 7px;
    text-wrap: pretty;
  }
  .witness.fine p {
    color: var(--green);
  }
  .witness.broken p {
    color: #fca5a5;
  }
  /* The limit is the same size as the finding. A backup that can only see
     part of the record should not be presented as though it saw all of it,
     and shrinking this line would be a way of saying so without saying so. */
  .witness p.bound,
  .witness.fine p.bound,
  .witness.broken p.bound {
    color: var(--muted);
  }

  .preview {
    margin-top: 20px;
    padding-top: 14px;
    border-top: 1px solid var(--line);
  }
  h3 {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }
  .preview ul {
    list-style: none;
    margin-top: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.84rem;
    line-height: 1.5;
  }
  .preview b {
    color: var(--purple);
  }

  .swap {
    margin-top: 18px;
    padding: 11px 13px;
    border-radius: 8px;
    background: rgba(233, 235, 244, 0.04);
    border: 1px solid var(--line);
  }
  .swap p {
    font-size: 0.84rem;
    line-height: 1.55;
    text-wrap: pretty;
  }
  .swap p.quiet {
    margin-top: 7px;
  }

  .restore {
    margin-top: 16px;
    width: 100%;
    border-radius: 999px;
    padding: 9px 15px;
    font-size: 0.84rem;
    cursor: pointer;
    background: rgba(252, 165, 165, 0.12);
    border: 1px solid rgba(252, 165, 165, 0.45);
    color: #fca5a5;
  }
  .restore:disabled {
    opacity: 0.5;
    cursor: default;
  }

  .arrived {
    margin-top: 16px;
    padding: 13px;
    border-radius: 8px;
    background: rgba(52, 211, 153, 0.07);
    border: 1px solid rgba(52, 211, 153, 0.25);
  }
  .arrived b {
    color: var(--green);
  }
  .arrived p {
    color: var(--muted);
    font-size: 0.81rem;
    line-height: 1.55;
    margin-top: 8px;
    text-wrap: pretty;
  }
  code {
    font-family: var(--mono);
    font-size: 0.9em;
    color: var(--ink);
    background: rgba(233, 235, 244, 0.07);
    border-radius: 3px;
    padding: 1px 4px;
    overflow-wrap: anywhere;
  }
</style>
