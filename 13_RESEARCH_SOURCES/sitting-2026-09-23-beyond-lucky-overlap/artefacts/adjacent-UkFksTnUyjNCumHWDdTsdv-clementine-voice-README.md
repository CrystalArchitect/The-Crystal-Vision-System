# Clementine · Voice

A phone-reachable Clementine you talk to. One static HTML file, no build step,
no server — published with the site at **`/clementine-voice/`**.

Tap the big button, talk, and she answers out loud. Turn on **Hands-free** and
she listens again after each reply, so a conversation costs one tap total
rather than one per turn. Typing is still there, demoted to a button.

It is meant to feel like a call rather than a walkie-talkie, which needs two
things beyond talk-and-listen:

- **She speaks while the reply is still arriving.** The response is streamed
  and handed to the voice a sentence at a time, so the gap after you stop
  talking is one sentence's worth of model latency, not the whole answer's.
- **You can cut her off.** Tapping the button mid-sentence stops her and
  starts listening. Waiting out a long answer before replying is the thing
  that makes a voice assistant feel like a form.

It exists because the local Clementine webapp cannot be reached from a phone
with no machine to run it on. That is not a defect in the local app — it is
what local-first means. This shell makes the opposite trade deliberately.

## Where the audio goes

Three paths, three different answers. The page has a **Where audio goes**
button that says this too, because "it's private" would be a claim that is
only true of some of it.

| Part | Where it happens | Leaves the device? |
|---|---|---|
| Clementine speaking | your phone's installed voices | **no** |
| The talk button | your browser's speech recognition | **probably — see below** |
| The keyboard's 🎤 key | iOS system dictation | **no** — never reaches this page |
| Your words → the model | your configured endpoint | **yes**, always |

**Speaking** uses `speechSynthesis` filtered to `localService` voices only —
the same promise `voice.js` in this directory makes. With
no on-device voice she stays silent rather than fall back to a network one.

**The talk button** uses the browser's built-in `SpeechRecognition`. In Chrome
on a desktop that sends audio to Google. On an iPhone it is Apple's recogniser
*whichever browser you use* — Firefox and Chrome there are required to run on
WebKit, so they are wrappers around the same engine — and whether it runs
on-device or on Apple's servers is **not something this page can determine**.
So it is described as leaving the device, rather than assumed not to. If that
matters, use the keyboard key instead: slower, and the one whose answer is
clean.

Both routes end the same way: the transcribed text goes to your endpoint.

## Setup

Tap **Setup** once: an OpenAI-compatible base URL, a key, a model, and a voice.
The key lives in this browser's `localStorage` and goes only to that endpoint —
no server of ours is in the path. `companion.py` already abstracts the same
dialect, so nothing here locks you to a provider.

## If it says 401 "Missing Authentication header"

That is usually not a wrong key. Browsers **strip the `Authorization` header
across a redirect to another origin**, so if the endpoint you configured
redirects — `http://` upgrading to `https://`, a bare host resolving to `www.`,
a shortened path — the provider receives the request with no key at all and
says the header is missing rather than invalid.

The page now reports this itself: an error shows the endpoint, the model, the
key's length and first/last three characters, the request's **final URL**, and
whether it was redirected. Enough to tell "no key", "that's a URL in the key
box" and "a redirect ate the header" apart, without printing the secret.

Put the endpoint's exact final URL in Setup: `https://`, correct host, no
trailing slash. A scheme-less or `http://` entry is upgraded on save for the
same reason.

## If the mic or the voice does nothing

Tap **Diagnostics** in the header. It prints what the browser actually reports —
voice count, which are flagged on-device, whether `SpeechRecognition` exists,
whether it ever started, and the last speech error. Screenshot that; it is the
only view into the device the maintainer has.

Two specific failures it exists to catch:

- **Voices exist but none is flagged `localService`.** The strict on-device
  filter then finds nothing and the page stays silent — which is correct by the
  rule and indistinguishable from being broken. It now says so and offers an
  explicit opt-in to use them anyway, because the flag is not reported
  consistently and "probably your phone's own voices" is a judgement for the
  human, not a default.
- **`SpeechRecognition` exists but never fires.** Presence is not function. If
  neither `onstart` nor `onerror` lands within 2.5 s the page says so and hands
  over to the keyboard's dictation key, rather than leaving a button that looks
  alive and does nothing.

## Known limits

- **CORS decides whether a provider works.** The page calls the endpoint
  straight from the browser and some providers refuse a web origin. The error
  is shown in full and names CORS, because on a phone that text is the only
  diagnostic there is. A provider that refuses needs a proxy, which needs a
  server, which this deliberately does not have.
- **A key in `localStorage` is only as private as the phone.**
- **Now run on real iOS — in Firefox, not Safari.** A full turn works there:
  spoken input transcribed, request authenticated, reply spoken aloud through
  an on-device voice. Everything before that was mobile-emulated Chromium with
  a mock recogniser, and Chromium differs from WebKit in exactly the places
  that matter here. Two bugs only the real device could show: a
  `SpeechRecognition` instance cannot be restarted on WebKit, so the
  microphone worked exactly once per page load; and the microphone-blocked
  guidance named Safari's Settings page to a Firefox user. Safari itself is
  still unconfirmed.
- Hands-free turns itself off when a request fails, so a broken endpoint
  cannot put it in a listen/fail loop.
- **Streaming depends on the provider.** The request asks for it; an endpoint
  that ignores it and returns one JSON body is handled by falling back to
  speaking the whole reply at once. You lose the early start, not the feature.
- How soon she starts speaking is the model's time-to-first-sentence, which is
  not something this page controls.

## Verified

In a 390×844 mobile context, against a stub OpenAI-compatible endpoint and a
mock recogniser driving the real code path:

- tap → recogniser starts, button shows a live state
- interim words appear greyed, are replaced by the final transcript, and the
  final result auto-sends without another tap
- **hands-free relistens after the reply finishes speaking** (recogniser start
  count rises across a turn on its own)
- microphone-denied produces guidance naming *the browser you are actually
  in* (Settings → Firefox → Microphone for a Firefox user, Safari's ⓐA route
  for a Safari one) and switches hands-free off rather than looping
- a reply containing `<img src=x onerror=…>` renders as literal text — no
  element created, no script run
- no horizontal overflow; header and talk button stay in view; only the
  transcript scrolls
- against an endpoint dripping a three-sentence reply, speech was queued
  **before the reply finished arriving** — first sentence at ~500 ms, last
  text at ~1170 ms — and the transcript still ended complete and correct
- tapping mid-reply cancels speech and starts listening (barge-in)
- an endpoint that ignores `stream` still works, via the whole-reply fallback

One note on that suite: the first version of the speech mock assigned to
`window.speechSynthesis`, which is a read-only getter, so the assignment was
silently ignored and the test ran against the real, voiceless headless engine —
reporting zero utterances and looking like a page bug. It was a test bug. The
mock now uses `Object.defineProperty`. Worth recording because a mock that
fails open is worse than no mock: it reports green while measuring nothing.
