# Architecture Review — discord-ai-agent

**Date:** 2026-08-26
**Reviewer:** Claude (independent architecture pass, not derived from any prior Grok review)
**Scope:** Full repository at commit `029c391` (`main`), plus full git history including `refs/pull/1/head`

---

## Summary

`discord-ai-agent` is a **standalone Discord bot** with no ties to the TerAustralis Incognita / CrystalCore ecosystem — a repo-wide search for `Crystal`, `TerAustralis`, `Clementine`, `Starline`, `Dreamline`, `Songline`, and `ConsentGate` (case-insensitive) returned zero matches, and neither `README.md` nor `requirements.txt` reference any component from that family. It is a small (6 Python files, ~14 KB) `discord.py` bot that lets users chat with either xAI Grok or Anthropic Claude via text or voice (Edge-TTS), evaluated here on general architecture merit: separation of concerns, credential handling, error/rate-limit resilience, testability, and module boundaries.

**This review found a live, currently-exploitable secret exposure** (Discord bot token + xAI key + Anthropic key, real values, committed in three commits still reachable via `refs/pull/1/head`) that requires immediate credential rotation by the repository owner — see Finding 1. Beyond that, the codebase is small and readable but has a fully duplicated second bot implementation, no tests, no rate-limiting/cooldowns, and no command error handling.

---

## Strengths

- **Clean provider abstraction.** `GrokClient` (`grok_client.py`) and `ClaudeClient` (`claude_client.py`) both expose the same `get_response(message_history)` contract, so `bot.py`'s `get_active_client()` (lines 29–34) can switch providers with a two-branch `if`. This is a reasonable seam for adding a third provider later.
- **`.gitignore` is now correct and explicit.** `.gitignore` (added in `f467e37`) excludes `.env`, `.env.*`, `*.pem`, `credentials*` while explicitly allowing `.env.template` (`!.env.template`). Going forward, a fresh `.env` will not be re-committed.
- **`.env.template` documents the required shape** without carrying values (`DISCORD_BOT_TOKEN`, `XAI_API_KEY`, `ANTHROPIC_API_KEY`, `AI_PROVIDER`, `GROK_MODEL`, `CLAUDE_MODEL`), and the README walks through obtaining each credential — good onboarding UX for a small bot.
- **Grok client has graceful model-name fallback.** `grok_client.py` lines 29–52 try a list of model IDs in order and remember whichever one succeeds (`self.model = model`), which is a small but real resilience feature absent from the Claude client.
- **Errors from the AI providers are caught and surfaced as chat messages** rather than raising — `claude_client.py` line 47 (`except Exception as e: return f"Error communicating with Claude: {str(e)}"`) and the equivalent in `grok_client.py` — so a failed API call degrades to a visible error message instead of crashing the bot process.

---

## Findings

### Finding 1 — CRITICAL — Real API credentials are permanently committed and still fetchable from the remote

**Evidence:**
- Commit `81062df` ("Add environment variables for easy setup") added a tracked `.env` file containing real values for `DISCORD_BOT_TOKEN`, `XAI_API_KEY`, and `ANTHROPIC_API_KEY` (verified directly; values not reproduced here). The same three keys persist unchanged through `ee84426` and `fc41506`.
- Commit `f467e37` ("Stop tracking .env, add .gitignore and requirements.txt") removed `.env` from the tree going forward and explicitly documented the exposure in its own commit message: *".env was committed with real credentials for three services... Untracking does NOT remove the secrets from history - they remain reachable in earlier commits... The only real remedy is rotating the keys at each provider."* That rotation does not appear to have happened — the same three variable names with (presumably) the same values are still what `.env.template` documents, and there is no record in history of a rotation follow-up.
- These three commits live on the branch that became pull request #1 (`claude/new-session-vrpyn9`). That branch was **squash-merged** into `main` as `444dd84`, and the source branch was subsequently deleted from the remote (confirmed via `git ls-remote --heads origin`, which now shows only `main`). Squash-merging means the mainline `main` history never contains the secret-bearing commits — but GitHub retains the original commits on the pull request's `refs/pull/1/head` ref indefinitely, independent of the source branch's existence. This repo's `refs/pull/1/head` was confirmed fetchable in this session (`git fetch origin '+refs/pull/1/head:refs/remotes/origin/pr/1'` succeeded and returned the three secret-bearing commits).
- **Net effect: this is not a "was exposed, now fixed" situation.** Anyone with read access to this (private) repository can retrieve the real Discord bot token, xAI key, and Anthropic key today with `git fetch origin refs/pull/1/head` (or via the GitHub web UI's "Files changed" view on PR #1), regardless of what `main` currently looks like.

**Recommendation (urgent, human action required — flagged to the user directly, not just in this document):**
1. **Rotate all three credentials now**: the Discord bot token (Discord Developer Portal → Bot → Reset Token), the xAI API key (console.x.ai), and the Anthropic API key (console.anthropic.com). This is the only real fix — removing the file from the working tree already happened and did not solve it.
2. After rotation, consider actually scrubbing history (`git filter-repo` or BFG) and, since GitHub does not let you delete a merged PR's `refs/pull/N/head`, treat rotation — not history rewriting — as the control that matters.
3. Add a pre-commit or CI secret-scanning step (e.g. gitleaks/trufflehog) so a future `.env` commit is caught before push rather than after.

---

### Finding 2 — HIGH — The bot is fully duplicated across two files with no shared source of truth

**Evidence:** `bot.py` (131 lines) and `replit_main.py` (125 lines) each independently define a `commands.Bot`, a `chat`, `speak`, `leave`, `provider`/`join` command set, and — critically — `replit_main.py` lines 17–50 **re-implement `GrokClient` and `ClaudeClient` inline** rather than importing `grok_client.py` / `claude_client.py`, which already exist in the same directory. The two client implementations have already drifted: `claude_client.py`'s `ClaudeClient` extracts a system prompt from message history (lines 26–38), while `replit_main.py`'s inline version does the same via `next(...)` (line 46) — same intent, different code, doubling the maintenance surface for a change as simple as adjusting the default system prompt.

**Recommendation:** Pick one entry point. If `replit_main.py` exists to work around a Replit-specific constraint (e.g., no `.env`/dotenv on Replit — note it never calls `load_dotenv()`, unlike `bot.py` line 5/10), document that constraint explicitly in the README and have it `import` `GrokClient`/`ClaudeClient`/`VoiceManager` from the shared modules instead of re-defining them. If it's simply legacy, delete it — the README's "Running the Bot" section (lines 53–59) only documents `python bot.py`, so `replit_main.py` is currently an undocumented, silently-diverging second implementation.

---

### Finding 3 — MEDIUM — No command error handling; malformed input surfaces as an unhandled exception

**Evidence:** None of `bot.py`'s commands (`chat`, `speak`, `join`, `leave`, `clear`, `provider`) have a companion `@bot.event async def on_command_error(...)`, and `*, message: str` (line 53) / `*, message: str` (line 97) are required positional arguments. Running `!chat` with no text raises `discord.ext.commands.MissingRequiredArgument`, which discord.py's default behavior logs to stderr and never reports to the user in Discord — the command silently does nothing from the user's point of view.

**Recommendation:** Add a global `on_command_error` handler that at minimum replies with a usage hint for `MissingRequiredArgument`/`BadArgument`, and swallow-and-log anything unexpected rather than letting it vanish into the process's stderr.

---

### Finding 4 — MEDIUM — No per-user rate limiting on API-calling commands

**Evidence:** `chat` (bot.py:52) and `speak` (bot.py:96) both forward arbitrary user-supplied text straight to `client.get_response(...)`, which calls a paid external API (Anthropic or xAI). There is no `@commands.cooldown(...)` on any command (confirmed absent via search), so a single user (or a compromised/malicious bot invite) can spam `!chat`/`!speak` and drive unbounded API spend with no code-level guard rail.

**Recommendation:** Add `@commands.cooldown(1, N, commands.BucketType.user)` (discord.py's built-in decorator) to `chat` and `speak` at minimum, and consider a global per-guild cap for shared servers.

---

### Finding 5 — MEDIUM — Voice state is a single global, not per-guild — the bot cannot serve two voice channels at once

**Evidence:** `VoiceManager.__init__` (`voice_manager.py` lines 6–9) holds exactly one `self.voice_client` and one `self.output_file = "response.mp3"`, and `bot.py` instantiates exactly one `VoiceManager()` (line 23) shared by the whole bot process. If the bot is invited to more than one Discord server and two different guilds both use `!join`/`!speak` concurrently, the second `join_channel` call (voice_manager.py lines 11–17) will `move_to` the *same* voice client into the second guild's channel, silently disconnecting the first guild. `replit_main.py`'s alternate implementation (lines 96–99) is per-`ctx` (`ctx.voice_client`) and doesn't have this specific problem, which is itself evidence the two files have diverged in a way that matters functionally, not just cosmetically.

**Recommendation:** If multi-guild voice support is in scope, key voice state by `guild.id` (a `dict[int, VoiceManager]` or equivalent) rather than a single shared instance. If the bot is only ever intended for one server, document that constraint in the README so it isn't discovered in production.

---

### Finding 6 — LOW — Unbounded, unpersisted per-user chat history

**Evidence:** `chat_history = {}` (bot.py line 26) is a plain in-memory dict, appended to on every `!chat`/`!speak` call (lines 61, 108) and never trimmed except by the user explicitly running `!clear` (line 119). Nothing caps its length, so a long-running conversation will eventually exceed the target model's context window and start failing at the API layer with no earlier warning to the user. It is also entirely lost on process restart, with no persistence layer — which may be an acceptable scope decision for a small bot, but is undocumented as such.

**Recommendation:** Either cap history length (e.g., keep the last N turns) or note the unbounded-growth / no-persistence tradeoff explicitly in the README so it's a documented decision rather than a latent bug report.

---

### Finding 7 — LOW — Default Claude model ID is a specific dated snapshot that will age out

**Evidence:** `claude_client.py` line 10: `self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")`. This is a fixed, dated model snapshot; Anthropic's currently supported model line (as of this review) no longer includes this identifier in its primary lineup. Because it's only a *default* (overridable via `CLAUDE_MODEL` in `.env`), this isn't a functional bug today, but a fresh clone that doesn't set `CLAUDE_MODEL` will silently target an aging/possibly-retired model with no fallback (unlike `grok_client.py`, which tries a list of models).

**Recommendation:** Either update the default periodically as part of routine maintenance, or apply the same fallback-list pattern already used in `grok_client.py` (lines 29–34) to `claude_client.py` for consistency.

---

### Finding 8 — LOW — No automated tests, no CI

**Evidence:** No `test_*.py` / `*_test.py` files anywhere in the repo, and no `.github/workflows/` directory (confirmed absent). Given the current size this is a low-severity finding, but the two-file duplication in Finding 2 is exactly the kind of drift that a basic smoke test (e.g., "does `ClaudeClient.get_response` correctly split out a system message") would have caught early.

**Recommendation:** At minimum, add a unit test around the client's system-prompt extraction (`claude_client.py` lines 26–38), since it's the one piece of non-trivial logic in the provider layer and has already been re-implemented independently once.

---

## Open Questions for a Human / Architect

1. **Have the three credentials from Finding 1 already been rotated outside of git?** This review can only observe repository state, not provider-side key status — please confirm rotation has happened (or schedule it) independent of any code change in this PR.
2. **What is `replit_main.py` for, going forward?** Is Replit an actively supported deployment target, or is this a leftover from an earlier hosting choice that should be removed or clearly documented as a separate, intentionally-divergent entry point?
3. **Is multi-guild deployment in scope?** Finding 5 only matters if the bot is (or will be) invited to more than one Discord server simultaneously — worth confirming the intended deployment shape before prioritizing a fix.
4. **What conversation-history retention is actually desired?** (Finding 6) — is losing history on restart acceptable, or should there eventually be persistence (e.g., SQLite/Redis) backing `chat_history`?
