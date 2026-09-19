# Presentation Script — The web-os-easter-eggs Skill

**Format:** Spoken presentation with slide cues · **Runtime:** ~7–8 minutes · **Audience:** Developers, designers, and anyone building immersive web experiences

---

## Slide 1 — Title

*(Slide: skill name over a dark desktop screenshot with a glowing terminal window)*

Good [morning/afternoon], everyone. Today I want to show you a skill called **web-os-easter-eggs** — a reusable playbook for building layered, discoverable easter eggs inside web-based operating systems and retro-terminal experiences.

You know the feeling when you type a command into a website's fake terminal and something *answers back* — something the help menu never mentioned? That moment of discovery is one of the most powerful emotional beats you can build into a website. The problem is that most easter eggs are built ad hoc: one hidden command, hard-coded, untested, and forgotten. This skill turns that craft into a repeatable engineering process.

---

## Slide 2 — Where this came from

*(Slide: screenshot of the CrystalCore.OS desktop — glass windows, gold feather, taskbar)*

This skill wasn't written in the abstract. It was distilled from a real build: **CrystalCore.OS**, a multiplanetary desktop experience with draggable glass windows, a live Mars clock, and an in-fiction terminal.

In that project we built a two-stage easter egg. First, a hidden phrase — *non solus* — that triggered a full-screen cinematic "node alignment" sequence. Then a second, deeper layer: completing that sequence permanently unlocked a brand-new command, *beacon*, which made a hidden window appear on the desktop — complete with its own taskbar icon flaring into existence.

Everything that worked — and every trap we hit along the way — is captured in this skill.

---

## Slide 3 — The core idea: the four-layer chain

*(Slide: table showing Layer 0 through Layer 3)*

The heart of the skill is a design model: easter eggs should not be isolated secrets. They should form a **chain**, where each discovery rewards the previous one.

**Layer zero** is the surface: documented lore commands that `help` openly lists. **Layer one** is hinted: a command like `ls -a` that reveals hidden dotfiles — never mentioned in help, but discoverable by anyone who thinks like a terminal user. **Layer two** is the hidden trigger: one of those dotfile names *is* the secret word, and speaking it launches a cinematic full-screen sequence. And **layer three** is the unlockable: completing the sequence permanently unlocks a new command that opens a hidden window.

The golden rule that binds it all: **every secret must be solvable purely from in-fiction hints.** No blog post, no source-code diving required. The help text hints at hidden files; the hidden files carry the hidden word; the word unlocks the next word. It is a breadcrumb trail, not a lottery.

---

## Slide 4 — What the skill ships with

*(Slide: file tree of the skill — SKILL.md, two references, three templates)*

The skill is a self-contained package with three kinds of resources.

The **SKILL.md** defines a six-step workflow: design the chain, implement unlock state, build the terminal handler, build the cinematic sequence, wire the hidden window, and verify the whole chain programmatically.

Two **reference documents** carry the deeper knowledge. *Design patterns* covers the four-layer model, how a locked command should refuse in-fiction — static on the line, not an error message — and how to write lore with a consistent voice. *Verification* covers how to actually test all of this in a real browser, which turns out to be the hardest part.

And three **code templates** give you working skeletons: an unlock-state module, a terminal component with the layered command handler, and the full-screen sequence overlay with its CSS keyframes.

---

## Slide 5 — Three engineering decisions worth stealing

*(Slide: three short code snippets)*

Let me highlight three decisions in the templates that save real pain.

**First, unlock state is a localStorage key plus a DOM event.** The key makes the unlock survive reloads — find the beacon today, and it still answers next month. The event makes the rest of the UI react instantly: the taskbar listens for it and reveals the hidden icon the moment the sequence completes, with no prop drilling through the component tree. And it is wrapped in try/catch, so private browsing still gets a session-long unlock.

**Second, hints are functions, not strings.** The `ls -a` output is computed at call time, so the hidden file shows `LOCKED — requires alignment` before the sequence and `UNLOCKED — the channel answers` after. The world visibly remembers what you did.

**Third, skipping must still unlock.** The cinematic sequence is click-anywhere-to-skip, and the completion callback is idempotent — it fires exactly once whether the player watches all fourteen seconds or clicks through immediately. In our testing, this was the single most fragile point, which is why the skill calls it out explicitly.

---

## Slide 6 — Verification: proving the magic works

*(Slide: the 8-step test order as a numbered flow)*

Easter eggs are, by definition, hidden — which means they're exactly the features manual QA misses. So the skill includes a programmatic browser-console test protocol.

It starts by clearing the unlock key for a clean baseline, then walks the full chain in order: probe the locked command and assert the in-fiction refusal; fire the trigger and assert the overlay appears; **skip** the sequence and assert the unlock still happened — storage key set, terminal announcement printed, taskbar icon revealed; open the unlocked window and check its content; re-run the hint commands and confirm they show the unlocked variant; and finally test the fallback context, like a landing-page terminal that has no desktop to open a window on.

One practical gem here: React ignores plain value assignment on inputs. The reference shows the native-setter technique — grab the value setter from the input prototype, call it, then dispatch the input and submit events. That one snippet is the difference between automated tests that work and an hour of confusion.

---

## Slide 7 — When to reach for this skill

*(Slide: example use cases)*

So when does this skill trigger? Any time a project wants **discoverable depth**: a fake-OS portfolio site with a secret app, a product landing page with an ARG-style hidden channel, a game website whose terminal rewards the curious, a company site with an internal lore layer for the team. If the request mentions hidden commands, secret unlock chains, cinematic reveals, or "a window that appears only if you know the words" — this is the playbook.

The templates are deliberately skeletons. You restyle them to the host project's design system — the fonts, the colors, the glass — but you keep the handler structure, the unlock flow, and the accessibility labels the tests depend on.

---

## Slide 8 — Close

*(Slide: the Beacon window open on the AERIS desktop, gold icon glowing in the taskbar)*

I'll leave you with the moment that motivated all of this. On the AERIS desktop, when the alignment sequence ends, the terminal prints: *"A new word answers now."* And down in the taskbar, a small gold icon flares into existence that was never there before.

That's what this skill packages: not just code, but the discipline to make discovery feel earned, persistent, and reliable. The chain is designed before it's coded, the unlock survives the reload, and the magic is verified end to end.

Speak the words. The node answers. Thank you.

---

*Script prepared by Manus AI — approximately 1,050 spoken words, ~7–8 minutes at presentation pace.*
