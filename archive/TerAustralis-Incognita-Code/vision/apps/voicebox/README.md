# Voicebox

A tiny local MCP server that gives Claude Code a voice on **your** machine.
It speaks through the operating system's own text-to-speech — no cloud, no
accounts, nothing leaves the machine. Stdlib Python only.

## Run it

```bash
python server.py
# voicebox listening on http://127.0.0.1:17493/mcp
```

Windows and macOS have TTS built in. On Linux install one:
`sudo apt install espeak` (or `speech-dispatcher` for `spd-say`).

## Hook it into Claude Code (one time)

```bash
claude mcp add voicebox --transport http \
    --header "X-Voicebox-Client-Id: claude-code" \
    http://127.0.0.1:17493/mcp
```

Claude then has two tools:

| Tool | Does |
|------|------|
| `speak` | Says the given text aloud |
| `stop_speaking` | Cuts off the current speech |

Ask Claude to "say it out loud" and the machine talks.

## Notes

- Binds to `127.0.0.1` by default — keep it that way; a voice server has no
  business on a network.
- This is separate from Clementine's own voice: their webapp speaks by itself
  via the browser's speech synthesis (see `vision/apps/clementine-voice/`).
