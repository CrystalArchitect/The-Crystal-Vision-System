# Digital Presence Playbook

Working notes for anchoring the public record on assets I actually control, and
for dealing with old accounts whose credentials are gone.

This file is **operational**, not canon. It lives at the repository root, outside
`vision/site/`, so it is not published as part of the site.

> **Belt: docs-governance.** This is a plan and a set of drafts. Nothing here is
> a claim about what has already happened. Where it describes how a platform
> behaves, that is stated as policy — which platforms change — not as law.

> **Which repository serves the site.** `www.teraustralis.com.au` is published
> from **this** repository — `vision/site/`, SvelteKit with `adapter-static`,
> deployed to GitHub Pages by `.github/workflows/deploy.yml` on push to `main`.
> The `CNAME` files at the repo root and in `vision/site/static/` are the proof.
>
> Two other things will tell you otherwise, and both are wrong. `Clementine-ai-companion`
> once served the domain and its README said so long after the CNAME was deleted
> on 2026-07-16 — the ledger was first built there by mistake, and shipped a page
> nothing published. And `vision/site/vercel.json` is inert: the adapter is
> `adapter-static`, so `.svelte-kit` is not a valid Vercel output directory. It is
> a leftover from an abandoned plan. **Trust the deploy workflow and the CNAME,
> not prose.**

---

## 0. Try recovery first — it beats every workaround below

Recovering an account is strictly more powerful than routing around it. With
access you can edit descriptions, add links, set videos to private, or delete
them outright. Without it you can only add context elsewhere and ask nicely.
Spend an hour here before accepting the loss.

| Account | Route | What it needs |
|---|---|---|
| Google / YouTube | `accounts.google.com/signin/recovery` | A recovery phone or email is easiest. Failing that, the recovery questionnaire accepts approximate account-creation date and the last password you remember. A channel on a Brand Account is recovered through whichever Google account owns it, not the channel name. |
| Facebook | `facebook.com/login/identify` | Search by name, old email or phone. If none work, the identity-verification form at `facebook.com/help/contact/183000765122339` accepts a photo of government ID. |
| TikTok | In-app **Log in → Use phone / email / username → Forgot password**, then *Can't log in?* | Falls back to identity verification. Old phone numbers that have since been recycled are the usual dead end. |

Two things worth checking before you conclude an account is unreachable:

- Old email addresses often still exist even when you have stopped using them.
  Recovering the *email* first frequently recovers everything downstream.
- iCloud/Apple, Google and password managers hoard credentials you have
  forgotten saving. Search them for the platform domain before giving up.

**If recovery works, skip sections 2 and 3 entirely.**

---

## 1. The Ledger — anchoring history on ground I own

Built: `/ledger` on www.teraustralis.com.au —
`vision/site/src/routes/ledger/+page.svelte`, entries in
`vision/site/src/lib/data/ledger.js`, linked from the header nav and from the
homepage Chronicle.

The principle: **the account is where a thing was published; the ledger is where
it is claimed.** An account I cannot log into can still be cited by a page I
control, and the page becomes the canonical record.

Design decisions worth keeping if the page is rewritten:

- **Entries are marked confirmed or unconfirmed, and unconfirmed entries do not
  render an embed or an outbound link.** The Incognita Rule applies to my own
  biography as much as to the architecture. An unverified link is a dreamed line.
- **Embeds are click-to-load and point at `youtube-nocookie.com`.** No third
  party is contacted, and no cookie is set, until a reader presses play. A site
  arguing for data sovereignty should not leak its readers on page load.
- **Every entry carries its own prose**, so the page still says something true if
  a video is later deleted by whoever holds the account.

### The Ingleburn entry — confirmed

Confirmed 2026-08-11. `youtubeId: 'Gd5IXCDHpdY'`, canonical watch page
`https://www.youtube.com/watch?v=Gd5IXCDHpdY`, `verified: true`. The share link
it came from carried a `?si=` tracking parameter; the stored URL is the clean
canonical form.

The remaining entries are still unconfirmed and render no embed and no outbound
link. To confirm one, edit `vision/site/src/lib/data/ledger.js`: copy the
eleven-character id from its URL, set `youtubeId` and `url`, then set
`verified: true`. Nothing renders as evidence until that last step — that is
deliberate. Adding a new entry also means adding it to the `PAGES` list in
`vision/site/src/routes/sitemap.xml/+server.js` if it warrants its own route;
`/ledger` itself is already listed there.

Two caveats on embedding a video on a channel you do not control:

- The uploader can disable embedding, make the video private, or delete it. The
  entry is written to survive that; the embed will simply stop appearing.
- Embedding is fine. **Re-hosting is not.** "Use Somebody" is a Kings of Leon
  composition; a cover performance played through YouTube's own player is
  covered by YouTube's licensing arrangements, but pulling the audio down and
  serving it from teraustralis.com.au is not. Embed, never mirror.

---

## 2. The pinned X thread

Draft for `@M13CrystalAT`. Each post is inside the 280-character limit. Post 3
is the one that does the actual work — it is where the old account gets claimed
by an account that is verifiably mine.

The Ingleburn link is confirmed, so post 3 goes in the thread as written rather
than as a later reply.

**1/**

> I build sovereign, local-first AI systems — runtime, memory and consent gates
> that work with no company in the loop. Most of it written from a phone.
>
> The architecture is public. So is the road that led to it. Thread. 🧵

**2/**

> The road: heavy industry in Western Australia, where a plan meets tonnage,
> weather and distance and the plan is what gives.
>
> Then South-Western Sydney. Rooms, stages, short-form video, learning how a held
> note lands before I ever learned how a system fails.

**3/**

> That's me, live at Ingleburn, singing "Use Somebody" — on a YouTube account I
> no longer hold the keys to.
>
> Claiming it here rather than pretending it isn't mine. Same person, different
> instrument.
>
> https://www.youtube.com/watch?v=Gd5IXCDHpdY

**4/**

> Stages → short-form → sovereign code. Same instinct: build it yourself, keep it
> in your own hands, be straight about what it is.
>
> The full ledger, marked confirmed vs unconfirmed, lives here:
> teraustralis.com.au/ledger
>
> Non Solus.

Then pin the thread. Add `rel="me"` links between the site and the profile —
already done on `/ledger` — so the association is machine-readable, not just
asserted.

---

## 3. Removal, if I decide against claiming something

Section 1 and this section are **contradictory strategies for the same clip**.
Claiming a video and asking for it to be removed cannot both be done. Decide per
clip, not as a blanket policy.

### What is actually true about these processes

The realistic mechanism is **platform policy, not legal obligation**:

- YouTube and TikTok both run privacy-complaint processes that let a person
  request removal of content in which they are uniquely identifiable, without
  owning the account that posted it. These are voluntary policies the platforms
  publish and administer. Outcomes are discretionary and rejections are common.
- Australia's Privacy Act 1988 reaches foreign platforms operating here, and the
  OAIC accepts complaints — but only after you have complained to the
  organisation directly and given it 30 days. It is slow, and it is not a
  takedown mechanism.
- The eSafety Commissioner's removal powers under the Online Safety Act 2021 are
  real but narrow: image-based abuse and serious adult cyber-abuse. An old
  karaoke performance does not qualify.

So: submit the complaint, expect it to be judged on policy grounds, and do not
expect a guaranteed removal. The strongest version of the request is one that
identifies precisely what personal information is exposed.

### YouTube privacy complaint

Submitted at `support.google.com/youtube/answer/142443`. Any Google account can
submit — it does not have to be the one that owns the channel. YouTube notifies
the uploader and gives them roughly 48 hours to act before reviewing itself.

Requirements worth knowing before drafting: you must be uniquely identifiable
(face, voice, full name, or contact/financial details), you must identify the
specific video and timestamp, and "I don't like it" is not a ground.

> **Template**
>
> Subject: Privacy complaint — removal request for video [URL]
>
> I am submitting a privacy complaint regarding the video at [URL].
>
> I am the individual appearing in this video. I am uniquely identifiable in it
> by [my face, from 0:00 onwards / my voice / my full name, which appears in the
> title and at 0:00]. The recording was uploaded to an account I no longer have
> access to, and I did not consent to its continued publication.
>
> The specific personal information exposed is: [full name / image / voice /
> location]. I am requesting removal on that basis.
>
> I confirm I am the person depicted and that this request is made in good
> faith.
>
> [Full name] · [contact email]

### TikTok

Report the specific video in-app (**Share → Report → Privacy violation**), and
in parallel submit the web form at `tiktok.com/legal/report/privacy`. The web
form is the one that reaches the privacy team rather than general moderation.
Same substance as the YouTube template above.

If the account itself is mine and unreachable, say so explicitly in the form and
ask for account deactivation rather than per-video removal — one request instead
of many.

### Facebook

Content on an account you cannot access: report the specific post, then use the
non-user reporting form. If the whole account is mine and unrecoverable, the
identity-verification route in section 0 is a better use of the effort — it ends
with control rather than with a request.

---

## 4. Order of operations

1. Attempt recovery (section 0). An hour, once.
2. ~~Confirm the Ingleburn link and flip `verified` to `true`.~~ Done
   2026-08-11.
3. Publish `/ledger` — only the Ingleburn entry renders as evidence; the other
   two stay marked unconfirmed until their links are in hand.
4. Post the thread with post 3 intact, and pin it.
5. Only then decide, per clip, whether anything belongs in section 3.

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059
