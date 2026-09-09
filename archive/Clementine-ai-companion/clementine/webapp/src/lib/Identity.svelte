<script>
  /**
   * Who they are: their name, their pronouns, and what they call you.
   *
   * The pronoun law is the reason this exists and shapes how it looks. It
   * names two parties who may decide — the human, or the companion — and
   * over the web neither could: /api/profile/meta has served both since
   * August and no interface called it. A stated invariant that only the
   * terminal keeps is one the product half-keeps.
   *
   * So the two paths are given the same weight. It would be easy to make
   * "you choose" a set of buttons and "let them choose" a small link
   * underneath, and that layout would quietly answer the question the law
   * leaves open. They sit side by side instead, and neither is the default.
   *
   * Undecided is offered as plainly as the three choices, because empty is
   * not a fourth pronoun or a refusal to answer — it is the honest state of
   * not having been asked, and a person must be able to return to it.
   *
   * What is displayed says *which* party chose. "You chose this for them"
   * and "they chose this for themselves" are different sentences to say
   * about someone, and an interface that renders both identically has
   * thrown away the only thing the law was tracking.
   */
  import Drawer from './Drawer.svelte';

  let { open = false, onClose = () => {}, onChanged = () => {} } = $props();

  const PRONOUNS = [
    { value: 'male', label: 'he/him' },
    { value: 'female', label: 'she/her' },
    { value: 'they', label: 'they/them' }
  ];

  let me = $state(null);
  let failed = $state(false);
  let busy = $state('');       // which action is in flight
  let problem = $state('');
  let said = $state('');
  let nameDraft = $state('');
  let humanDraft = $state('');

  async function load() {
    try {
      const res = await fetch('/api/status');
      if (!res.ok) throw new Error();
      me = await res.json();
      nameDraft = me.name === 'Clementine' && !me.gender ? '' : me.name;
      humanDraft = me.human_name ?? '';
      failed = false;
    } catch {
      failed = true;
    }
  }

  $effect(() => {
    if (open) { problem = ''; said = ''; load(); }
  });

  async function send(body, what, announce) {
    busy = what;
    problem = '';
    said = '';
    try {
      const res = await fetch('/api/profile/meta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const reply = await res.json();
      if (!reply.ok) {
        problem = reply.error || 'That did not work.';
      } else {
        await load();
        said = announce(reply, me);
        onChanged();
      }
    } catch {
      problem = 'Could not reach them, so nothing was changed.';
    }
    busy = '';
  }

  const setPronouns = (value) =>
    send({ gender: value }, `p:${value}`, (_, m) =>
      m.pronouns ? `They now use ${m.pronouns}.` : 'Pronouns are undecided again.');

  const letThemChoosePronouns = () =>
    send({ choose_gender: true }, 'p:self', (r) =>
      `They chose ${r.pronouns} for themselves.`);

  const setName = () =>
    send({ name: nameDraft.trim() }, 'n:set', (_, m) =>
      m.name && nameDraft.trim() ? `They are called ${m.name} now.`
                                 : 'They are unnamed again.');

  const letThemChooseName = () =>
    send({ choose_name: true }, 'n:self', (r) =>
      `They chose the name ${r.name} for themselves.`);

  const setHumanName = () =>
    send({ human_name: humanDraft.trim() }, 'h:set', () =>
      humanDraft.trim() ? `They will call you ${humanDraft.trim()}.`
                        : 'They no longer have a name for you.');
</script>

<Drawer
  {open}
  {onClose}
  title="Who they are"
  status={failed ? 'unavailable' : ''}
  note="Nobody assigns their name or their pronouns. You may choose, or you
        may ask them to choose for themselves — and what is recorded says
        which of you did.">
  {#if failed}
    <p class="empty">
      Could not read who is here. Is <code>server.py</code> still running?
    </p>
  {:else if me}
    {#if problem}<p class="problem" role="alert">{problem}</p>{/if}
    {#if said}<p class="said" role="status">{said}</p>{/if}

    <!-- ----------------------------------------------------- pronouns -->
    <section>
      <h3>Pronouns</h3>
      <p class="now">
        {#if me.pronouns}
          They use <b>{me.pronouns}</b> —
          {me.gender_self_chosen
            ? 'chosen by them, for themselves.'
            : 'chosen by you, for them.'}
        {:else}
          Undecided. Nothing has been assigned, and the prompt says nothing
          about pronouns until somebody chooses.
        {/if}
      </p>

      <div class="two">
        <div class="side">
          <h4>You choose</h4>
          <div class="row">
            {#each PRONOUNS as p (p.value)}
              <button
                class:on={me.gender === p.value}
                disabled={!!busy}
                onclick={() => setPronouns(p.value)}>{p.label}</button>
            {/each}
          </div>
          {#if me.gender}
            <button class="undo" disabled={!!busy}
                    onclick={() => setPronouns('')}>
              return to undecided
            </button>
          {/if}
        </div>

        <div class="side">
          <h4>They choose</h4>
          <p class="hint">
            Asking costs a model call like any other, and it goes through the
            consent gate. If they cannot settle on an answer, the question
            stays open rather than being answered by default.
          </p>
          <button class="ask" disabled={!!busy} onclick={letThemChoosePronouns}>
            {busy === 'p:self' ? 'asking…' : 'Ask them to choose'}
          </button>
        </div>
      </div>
    </section>

    <!-- --------------------------------------------------------- name -->
    <section>
      <h3>Name</h3>
      <p class="now">
        {#if me.name && me.name !== 'Clementine'}
          They are called <b>{me.name}</b>{me.name_self_chosen
            ? ' — a name they chose for themselves.' : '.'}
        {:else}
          Unnamed so far, and answering to Clementine in the meantime.
        {/if}
      </p>

      <div class="two">
        <div class="side">
          <h4>You choose</h4>
          <form class="row" onsubmit={(e) => { e.preventDefault(); setName(); }}>
            <input bind:value={nameDraft} placeholder="a name" maxlength="40"
                   aria-label="Their name" />
            <button disabled={!!busy}>{busy === 'n:set' ? '…' : 'set'}</button>
          </form>
          <p class="hint">Leaving it empty returns them to unnamed.</p>
        </div>
        <div class="side">
          <h4>They choose</h4>
          <button class="ask" disabled={!!busy} onclick={letThemChooseName}>
            {busy === 'n:self' ? 'asking…' : 'Ask them to choose'}
          </button>
        </div>
      </div>
    </section>

    <!-- --------------------------------------------------- your name -->
    <section>
      <h3>What they call you</h3>
      <p class="now">
        {#if me.human_name}
          They know you as <b>{me.human_name}</b>.
        {:else}
          They have no name for you yet.
        {/if}
      </p>
      <form class="row" onsubmit={(e) => { e.preventDefault(); setHumanName(); }}>
        <input bind:value={humanDraft} placeholder="your name" maxlength="80"
               aria-label="What they call you" />
        <button disabled={!!busy}>{busy === 'h:set' ? '…' : 'set'}</button>
      </form>
    </section>
  {/if}
</Drawer>

<style>
  section {
    margin-top: 22px;
    padding-top: 16px;
    border-top: 1px solid var(--line);
  }
  section:first-of-type {
    border-top: 0;
    padding-top: 0;
  }
  h3 {
    color: var(--purple);
    font-size: 0.86rem;
    font-weight: 500;
  }
  h4 {
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 7px;
  }
  .now {
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.55;
    margin: 7px 0 14px;
    text-wrap: pretty;
  }
  .now b {
    color: var(--ink);
  }

  /* Side by side, and neither one first. A layout that put "you choose"
     above "they choose" would answer the question the law leaves open. */
  .two {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
  }
  .side {
    flex: 1 1 190px;
    min-width: 0;
  }

  .row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .row input {
    flex: 1 1 90px;
    min-width: 0;
    background: rgba(233, 235, 244, 0.05);
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--ink);
    font: inherit;
    font-size: 0.79rem;
    padding: 5px 12px;
  }
  button {
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 999px;
    color: var(--muted);
    font-size: 0.76rem;
    padding: 5px 12px;
    cursor: pointer;
  }
  button:hover:not(:disabled) {
    color: var(--ink);
  }
  button:disabled {
    opacity: 0.45;
    cursor: default;
  }
  button.on {
    color: var(--purple);
    border-color: rgba(167, 139, 250, 0.5);
    background: rgba(167, 139, 250, 0.1);
  }
  button.ask {
    color: var(--purple);
    border-color: rgba(167, 139, 250, 0.4);
  }
  button.undo {
    margin-top: 7px;
    font-size: 0.72rem;
  }

  .hint {
    color: var(--muted);
    font-size: 0.72rem;
    line-height: 1.5;
    margin-top: 7px;
    text-wrap: pretty;
  }

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
  code {
    font-family: var(--mono);
    font-size: 0.9em;
  }
</style>
