<script>
  /** Streaming chat with the local model via the Flask API. */
  let { name = 'Clementine', pagesPreview = false, onStateChange = () => {} } = $props();

  let messages = $state([]);
  let draft = $state('');
  let busy = $state(false);
  let logEl;
  let controller = null;

  function scrollLog() {
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  }

  function stop() {
    if (controller) controller.abort();
  }

  async function send(event) {
    event.preventDefault();
    const text = draft.trim();
    if (!text || busy) return;
    draft = '';
    messages.push({ who: 'you', text });
    const reply = $state({ who: 'companion', text: '' });
    messages.push(reply);
    busy = true;
    onStateChange('thinking');
    controller = new AbortController();
    setTimeout(scrollLog, 0);
    try {
      const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
        signal: controller.signal
      });
      if (!res.ok || !res.body) throw new Error('offline');
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let first = true;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (first) {
          first = false;
          onStateChange('speaking');
        }
        reply.text += dec.decode(value, { stream: true });
        scrollLog();
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        reply.text += reply.text ? ' — [stopped]' : '[stopped]';
      } else {
        reply.text =
          pagesPreview
            ? '[This is a static preview. Clone the repository and run python server.py — I have no brain on GitHub Pages.]'
            : '[I can\u2019t reach my local brain. Is server.py running, and is Ollama awake?]';
      }
    }
    busy = false;
    controller = null;
    onStateChange('idle');
  }

  function onKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      // CJK IME safety: don't submit mid-composition
      if (e.isComposing || e.keyCode === 229) return;
      e.preventDefault();
      send(e);
    }
  }
</script>

<section class="chat" aria-label="Conversation">
  <div class="log" bind:this={logEl}>
    {#if messages.length === 0}
      <div class="empty">
        <p class="prompt-line">{'>'} say something to wake them</p>
        <p class="hint">
          {#if pagesPreview}
            This GitHub Pages copy has no model. Clone the repo; the brain is local.
          {:else}
            They run entirely on this machine. Nothing you say leaves it.
          {/if}
        </p>
      </div>
    {/if}
    {#each messages as m, i (i)}
      <div class={`msg ${m.who}`}>
        {#if m.who === 'companion'}
          <span class="speaker">{name}</span>
        {/if}
        <p>{m.text}{#if m.who === 'companion' && busy && i === messages.length - 1}<span class="caret" aria-hidden="true"></span>{/if}</p>
      </div>
    {/each}
  </div>

  <form class="composer" onsubmit={send}>
    <textarea
      rows="1"
      placeholder="Say something…"
      bind:value={draft}
      onkeydown={onKeydown}
      aria-label="Your message"
    ></textarea>
    {#if busy}
      <button type="button" class="stop" onclick={stop}>Stop</button>
    {:else}
      <button type="submit" disabled={!draft.trim()}>Send</button>
    {/if}
  </form>
</section>

<style>
  .chat {
    display: flex;
    flex-direction: column;
    min-height: 0;
    flex: 1;
  }

  .log {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .empty {
    margin: auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .prompt-line {
    font-family: var(--mono);
    color: var(--green);
    font-size: 0.95rem;
  }
  .hint {
    color: var(--muted);
    font-size: 0.85rem;
  }

  .msg {
    max-width: 68ch;
    padding: 10px 14px;
    border-radius: 12px;
    line-height: 1.55;
    white-space: pre-wrap;
  }
  .msg.you {
    background: #141420;
    align-self: flex-end;
  }
  .msg.companion {
    background: var(--panel);
    border: 1px solid var(--line);
    align-self: flex-start;
  }
  .speaker {
    display: block;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--purple);
    margin-bottom: 4px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .caret {
    display: inline-block;
    width: 8px;
    height: 1em;
    margin-left: 2px;
    vertical-align: text-bottom;
    background: var(--green);
    animation: blink 0.9s steps(1) infinite;
  }
  @keyframes blink {
    50% { opacity: 0; }
  }

  .composer {
    display: flex;
    gap: 10px;
    padding: 14px 20px;
    border-top: 1px solid var(--line);
  }
  textarea {
    flex: 1;
    resize: none;
    background: #0d0d18;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 10px 12px;
    font-family: var(--sans);
    line-height: 1.4;
  }
  textarea:focus {
    outline: 2px solid var(--purple);
    outline-offset: -1px;
  }
  button {
    cursor: pointer;
    background: var(--purple);
    color: #050208;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 18px;
  }
  button:disabled {
    opacity: 0.45;
    cursor: default;
  }
  button.stop {
    background: transparent;
    color: var(--muted);
    border: 1px solid var(--line);
    font-weight: 400;
  }

  @media (prefers-reduced-motion: reduce) {
    .caret { animation: none; }
  }
</style>
