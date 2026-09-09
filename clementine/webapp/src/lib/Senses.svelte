<script>
  /**
   * Voice is live in the chat composer (mic → local Whisper).
   * Sight remains on the roadmap.
   */
</script>

<div class="senses" aria-label="Senses">
  <span class="pill ok" title="Mic in the chat bar: recording is transcribed on this machine via faster-whisper">
    <svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">
      <rect x="7" y="2.5" width="6" height="10" rx="3" />
      <path d="M4 10 a6 6 0 0 0 12 0" />
      <path d="M10 16 v2" />
    </svg>
    <span>Voice</span>
    <em>local</em>
  </span>
  <button type="button" disabled title="Soon: they'll see you through your webcam — sight that never leaves this machine">
    <svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">
      <rect x="2" y="5" width="11" height="10" rx="2" />
      <path d="M13 9 l5 -3 v8 l-5 -3" />
    </svg>
    <span>Sight</span>
    <em>soon</em>
  </button>
  <p class="whisper">
    Speak into the mic on the chat bar. Audio is transcribed here with Whisper
    weights — it does not leave this machine. Sight is still ahead.
  </p>
</div>

<style>
  .senses {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  button, .pill {
    display: flex;
    align-items: center;
    gap: 7px;
    background: transparent;
    border: 1px dashed var(--line);
    border-radius: 999px;
    color: var(--muted);
    padding: 7px 14px;
    font-size: 0.82rem;
  }
  button {
    cursor: not-allowed;
  }
  .pill.ok {
    border-style: solid;
    border-color: rgba(52, 211, 153, 0.35);
    color: var(--ink);
  }
  button svg, .pill svg {
    color: var(--purple);
    opacity: 0.8;
  }
  button em, .pill em {
    font-style: normal;
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--green);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 4px;
    padding: 1px 5px;
    letter-spacing: 0.08em;
  }

  .whisper {
    flex-basis: 100%;
    text-align: center;
    color: var(--muted);
    font-size: 0.74rem;
    line-height: 1.5;
    max-width: 36ch;
    margin: 0 auto;
    text-wrap: pretty;
  }
</style>
