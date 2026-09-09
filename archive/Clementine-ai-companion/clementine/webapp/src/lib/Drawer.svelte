<script>
  /**
   * The shell the side panels share: scrim, panel, header, scrolling body,
   * footer note.
   *
   * Extracted when the second one arrived rather than the fifth. The panels
   * differ in what they show and in nothing else, and two copies of a scrim
   * drift apart in small ways that read as carelessness — a border on one
   * side, a different close button, a body that scrolls where the other does
   * not.
   */
  let {
    open = false,
    title = '',
    note = '',
    status = '',
    onClose = () => {},
    children
  } = $props();
</script>

{#if open}
  <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
  <div class="scrim" onclick={onClose}></div>
  <aside class="drawer" aria-label={title}>
    <header>
      <div>
        <b>{title}</b>
        {#if status}<span class="status">{status}</span>{/if}
      </div>
      <button class="close" onclick={onClose} aria-label="Close">✕</button>
    </header>

    <div class="body">{@render children()}</div>

    {#if note}<footer>{note}</footer>{/if}
  </aside>
{/if}

<style>
  .scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 4, 0.6);
    z-index: 20;
  }
  .drawer {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: min(460px, 100vw);
    background: var(--panel);
    border-left: 1px solid var(--line);
    z-index: 30;
    display: flex;
    flex-direction: column;
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    border-bottom: 1px solid var(--line);
  }
  header b {
    color: var(--purple);
  }
  .status {
    color: var(--muted);
    font-size: 0.78rem;
    margin-left: 8px;
  }
  .close {
    background: transparent;
    border: 0;
    color: var(--muted);
    font-size: 1rem;
    cursor: pointer;
    padding: 4px 6px;
  }
  .body {
    flex: 1;
    overflow-y: auto;
    padding: 6px 18px 18px;
  }
  footer {
    padding: 10px 18px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 0.74rem;
    line-height: 1.5;
    text-wrap: pretty;
  }
  @media (max-width: 760px) {
    .drawer {
      width: 100vw;
    }
  }
</style>
