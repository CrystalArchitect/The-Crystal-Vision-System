<!-- ACCESSION PLATE — The Library -->

> **Accession plate**
>
> - **Holding:** AERIS site build task log — Lumina chat, voice,
>   streaming, edge-nodes window
> - **Document date:** undated; late July 2026, inferred from content
> - **Accessioned:** 5 August 2026, supplied by the steward as a file
>   upload to the library-sync session (received as `todo.md`)
> - **Source label:** task log from the Manus build sessions
>   (human-directed, model-executed)
> - **Layer:** Claim — every item is marked complete by its author; none
>   of those completions were re-verified by the sync session, and the
>   code they describe lives on the Manus platform outside the eleven
>   visible repositories
> - **Status:** active
> - **Text below the rule is verbatim as received.**

---

# CrystalCore.OS — Task Todo

## Lumina chat window (current request)
- [x] Add Lumina CSS (chat bubbles, input, reflections) matching gold/cyan glass theme
- [x] Add Lumina window to Home.tsx: WinId, state, window UI, taskbar button
- [x] On-device response engine (keyword-based reflections, honesty-first tone)
- [x] Local memory: persist conversation in localStorage, visible & deletable (sovereignty)
- [x] Verify desktop + mobile screenshots
- [x] Checkpoint and deliver

## LLM-backed Lumina chat (current request)
- [x] Upgrade project to full-stack (web-db-user) for built-in LLM API
- [x] Add backend LLM chat endpoint with Lumina persona system prompt (lumina.chat tRPC)
- [x] Frontend: send recent local history as context, keep memory in localStorage only
- [x] Fallback to local reflection engine if LLM call fails
- [x] Vitest specs for lumina.chat (persona, history mapping, empty reply, input limits)
- [x] Test live conversation (endpoint returns in-character reply, HTTP 200)
- [x] Checkpoint and deliver

## Voice input for Lumina (current request)
- [x] Read voice transcription skill and add server transcription endpoint
- [x] Mic button in Lumina input row (gold/cyan theme, recording pulse state)
- [x] Record audio via MediaRecorder, send to transcription, insert text into input
- [x] Auto-send transcribed text for hands-free flow
- [x] Handle mic permission denied / unsupported browser gracefully
- [x] Vitest coverage for the transcription procedure
- [x] Verify UI states via screenshots, checkpoint and deliver

## Live voice waveform (current request)
- [x] Web Audio AnalyserNode wired to the mic stream during recording
- [x] Canvas waveform bars in Lumina window reacting to voice volume (gold/cyan theme)
- [x] Clean teardown of AudioContext/analyser on stop, close, and unmount
- [x] Respect prefers-reduced-motion (static level indicator fallback)
- [x] Verify recording UI via screenshot, run tests, checkpoint and deliver

## Edge AI hardware report integration (current request)
- [x] EDGE NODES desktop window: hard limits, hardware landscape, tiered node model (gold/cyan glass)
- [x] Taskbar button for EDGE NODES window
- [x] `edge` / `hardware` terminal command printing summary + tiers; listed in help
- [x] Fold report into Lumina system prompt (server) + local fallback keyword replies
- [x] Vitest coverage for updated Lumina persona knowledge
- [x] Verify UI via screenshots, run tests, checkpoint and deliver

## Lumina → EDGE NODES action button (current request)
- [x] Hardware-topic detection (user msg + reply keywords) shared by LLM and fallback paths
- [x] LuminaMsg supports an optional action; render clickable "OPEN EDGE NODES" chip under matching Lumina replies
- [x] Clicking the chip opens/focuses the EDGE NODES window
- [x] Persisted localStorage history keeps/restores the action chip safely (backward compatible)
- [x] Gold/cyan glass styling for the action chip
- [x] Verify UI via screenshot, run tests, checkpoint and deliver

## LLM structured-output action detection (current request)
- [x] Read LLM integration skill for structured output (JSON schema) usage
- [x] lumina.chat returns { reply, action } via JSON-schema structured output; system prompt documents when to suggest open-edge-nodes
- [x] Frontend uses server-provided action for the chip on the LLM path; keyword heuristic remains only for the offline fallback
- [x] Graceful degradation if structured parse fails (reply still shown, no chip)
- [x] Update/add vitest coverage for the structured action output
- [x] Verify end-to-end in browser, run tests, checkpoint and deliver

## Token-by-token streaming for Lumina replies (current request)
- [x] Read LLM integration skill streaming section; pick streaming approach compatible with structured action output
- [x] Server: streaming endpoint that emits reply tokens live and resolves { action } at stream end
- [x] Frontend: render Lumina reply incrementally as tokens arrive (replace typing dots with live text)
- [x] Action chip appears once the final structured payload arrives; offline fallback path unchanged
- [x] Graceful degradation: stream errors fall back to non-streaming or local engine without losing the reply
- [x] Vitest coverage for the streaming endpoint/parsing logic
- [x] Verify end-to-end in browser, run tests, checkpoint and deliver
