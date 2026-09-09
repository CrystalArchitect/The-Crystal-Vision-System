<script>
  /**
   * The consent record, shown rather than vouched for.
   *
   * The window used to report that the chain verified and show none of what
   * it had checked, which is a request to be trusted — the one thing this
   * record exists so that nobody has to do. This is the other half: every
   * call the companion made, allowed or refused, where it went and why.
   *
   * On the word "intact", which is the easy thing to overstate. `verify()`
   * recomputes each entry's hash and checks it links to the one before, so
   * it catches an entry altered after the fact and an entry cut out of the
   * middle. It cannot catch entries removed from the *end*: a chain with its
   * tail cut off is a shorter chain that still verifies perfectly. That was
   * measured, not assumed, and it is why the wording below says every
   * remaining entry rather than every entry. Closing that gap needs an
   * anchor outside the file, which is a change to the record's format and
   * not this panel's to make.
   *
   * No message content is in here — the entries carry a character count, not
   * the characters — so showing the record reveals nothing the conversation
   * did not already.
   */
  import Drawer from './Drawer.svelte';

  let { open = false, onClose = () => {} } = $props();

  const SHOWN = 200;

  let entries = $state([]);
  let total = $state(0);
  let intact = $state(null);
  let problems = $state([]);
  let loading = $state(false);
  let failed = $state(false);
  let disabled = $state(false);

  async function load() {
    loading = true;
    failed = false;
    try {
      const res = await fetch(`/api/audit?limit=${SHOWN}`);
      if (!res.ok) throw new Error('unreachable');
      const data = await res.json();
      entries = (data.entries ?? []).slice().reverse(); // newest first
      total = data.total ?? entries.length;
      intact = data.intact;
      problems = data.problems ?? [];
      disabled = intact === null && entries.length === 0;
    } catch {
      failed = true;
    }
    loading = false;
  }

  $effect(() => {
    if (open) load();
  });

  function when(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return Number.isNaN(d.getTime())
      ? iso
      : d.toLocaleString(undefined, {
          day: 'numeric', month: 'short',
          hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
  }
</script>

<Drawer
  {open}
  {onClose}
  title="Every call they have made"
  status={loading ? 'reading…' : failed ? 'unavailable' : `${total} recorded`}
  note="This is the whole record, not a summary of it. It lives as
        audit.jsonl in the same folder as their memory, and you can read it
        there too.">
  {#if failed}
    <p class="empty">
      The record could not be read. Is <code>server.py</code> still running?
    </p>
  {:else if disabled}
    <p class="empty">Auditing is switched off for this session, so there is
      nothing to show.</p>
  {:else if !loading && total === 0}
    <p class="empty">
      They have not made a call yet. When they do — whether it is allowed or
      refused — it will be written here before anything else happens.
    </p>
  {:else}
    {#if intact === false}
      <div class="verdict broken" role="alert">
        <b>This record has been tampered with.</b>
        <ul>
          {#each problems as problem (problem)}<li>{problem}</li>{/each}
        </ul>
      </div>
    {:else if intact === true}
      <div class="verdict fine">
        Every entry still here is unaltered and in the order it was written.
        <span class="caveat">
          A hash chain cannot notice entries deleted from the end, so this
          says nothing about whether the record is complete.
        </span>
      </div>
    {/if}

    {#if total > entries.length}
      <p class="trimmed">
        Showing the most recent {entries.length} of {total}. The rest are in
        the file.
      </p>
    {/if}

    <ul class="entries">
      {#each entries as entry (entry.hash)}
        <li class:refused={entry.outcome === 'refused'}
            class:away={entry.destination && entry.destination !== 'local'}>
          <div class="line">
            <span class="outcome">{entry.outcome}</span>
            <span class="service">{entry.service}</span>
            <span class="dest">
              {entry.destination === 'local'
                ? 'on this machine'
                : `to ${entry.destination}`}
            </span>
            <span class="at">{when(entry.at)}</span>
          </div>
          <div class="why">
            {entry.reason}{#if entry.model} · {entry.model}{/if}{#if entry.chars} · {entry.chars} characters{/if}{#if entry.source} · {entry.source}{/if}
          </div>
        </li>
      {/each}
    </ul>
  {/if}
</Drawer>

<style>
  .empty {
    color: var(--muted);
    font-size: 0.83rem;
    line-height: 1.6;
    padding: 22px 0;
    text-wrap: pretty;
  }

  .verdict {
    margin: 12px 0 4px;
    padding: 9px 11px;
    border-radius: 8px;
    font-size: 0.78rem;
    line-height: 1.5;
    text-wrap: pretty;
  }
  .verdict.fine {
    color: var(--green);
    background: rgba(52, 211, 153, 0.07);
    border: 1px solid rgba(52, 211, 153, 0.22);
  }
  .verdict.broken {
    color: #fca5a5;
    background: rgba(252, 165, 165, 0.08);
    border: 1px solid rgba(252, 165, 165, 0.35);
  }
  .verdict.broken ul {
    margin: 6px 0 0 16px;
  }
  /* The limit is part of the claim, not a disclaimer under it. */
  .caveat {
    display: block;
    margin-top: 5px;
    color: var(--muted);
  }
  .trimmed {
    color: var(--muted);
    font-size: 0.75rem;
    margin: 10px 0 0;
  }

  .entries {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 12px;
  }
  .entries li {
    border: 1px solid var(--line);
    border-left: 2px solid rgba(52, 211, 153, 0.5);
    border-radius: 7px;
    padding: 7px 10px;
    background: rgba(233, 235, 244, 0.03);
  }
  /* A call that left the machine, and a call that was stopped, are the two
     things somebody opens this panel to find. They should be findable by
     glance rather than by reading every row. */
  .entries li.away {
    border-left-color: var(--purple);
  }
  .entries li.refused {
    border-left-color: #fca5a5;
  }

  .line {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 7px;
    font-size: 0.8rem;
  }
  .outcome {
    font-family: var(--mono);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--green);
  }
  li.refused .outcome {
    color: #fca5a5;
  }
  .service {
    color: var(--ink);
  }
  .dest {
    color: var(--muted);
  }
  li.away .dest {
    color: var(--purple);
  }
  .at {
    margin-left: auto;
    color: var(--muted);
    font-size: 0.72rem;
    font-family: var(--mono);
  }
  .why {
    color: var(--muted);
    font-size: 0.73rem;
    margin-top: 3px;
    line-height: 1.45;
    text-wrap: pretty;
  }
</style>
