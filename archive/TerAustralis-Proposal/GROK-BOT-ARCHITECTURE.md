# Grok Bot Content Studio — Architecture Design Doc

**Status:** Design only. No code, no scrapers, no posting integrations built or run.
**Scope note:** The "4,200 bots" framing in the source post is marketing hyperbole, not
a real headcount — a working system needs a handful of *worker pools* (each pool is one
model/prompt config run N-wide in parallel), not 4,200 independently-provisioned agents.
This doc describes the pattern at a scale that's actually buildable.

---

## 1. Design goals

- Turn a continuous stream of raw signal (trending topics, formats, competitor posts)
  into a small number of *publish-ready* drafts per day, without a human doing the
  scanning/drafting/triage by hand.
- Keep a human as the actual publisher. No stage in this design auto-posts to a public
  platform — the last stage hands the owner a short, ranked list.
- Make every stage's failure mode cheap: a bad draft dies at Stage 4 or 5, not after
  it's live.

## 2. Compliance boundary (read first)

Any real build of Stage 1 needs to respect the terms of service of whatever it reads —
most platforms restrict or ban automated scraping outside their official API, and rate
limits are enforced server-side, not by good intentions. Treat this as a hard constraint
on implementation, not a detail to defer:

- Use official APIs (X API, YouTube Data API, Reddit API, etc.) with your own
  credentials and their published rate limits — not headless-browser scraping at volume.
- Auto-*posting* is a materially different, higher-risk action than auto-*drafting*.
  This design stops at drafts; wiring Stage 6's output straight into a posting API is a
  separate decision with its own platform-policy review, not an assumed next step.
- Content that imitates a real account, or is optimized purely to "spread" rather than
  to be accurate/useful, risks tripping platform inauthentic-behavior policies regardless
  of how the content was produced.

## 3. Pipeline stages

```
[Stage 1: Signal Intake] → [Stage 2: Pattern Miner] → [Stage 3: Draft Pool]
        → [Stage 4: Asset Pool] → [Stage 5: Scorer] → [Stage 6: Gate] → [Studio Lead]
```

### Stage 1 — Signal Intake
- **Job:** Pull recent posts/videos/threads from a fixed list of sources via official
  APIs, on a polling interval (minutes, not seconds — seconds-level polling is both
  unnecessary and the fastest way to hit rate limits).
- **Output:** Normalized records `{source, author, text, media, engagement_stats,
  fetched_at}` written to a queue/table.
- **Failure mode:** A dead source just produces fewer records; nothing downstream
  breaks.

### Stage 2 — Pattern Miner
- **Job:** Over a rolling window of Stage 1 records, identify which *formats* and
  *hooks* are currently outperforming baseline for this niche (e.g. by engagement
  velocity, not raw count — a 2-hour-old post with fast growth matters more than a
  2-day-old post with a big raw number).
- **Output:** A short list of `{pattern, evidence_examples, confidence}` — this is
  analysis, not content.
- **Model role:** One LLM call per window, not one per post — this is where "4,200
  bots" collapses to "one job that reads a batch."

### Stage 3 — Draft Pool
- **Job:** For each pattern from Stage 2, generate a small number of draft variants
  (e.g. 3–5) in the target formats — thread, script, carousel copy, reply.
- **Output:** Draft objects `{pattern_ref, format, body, variant_id}`.
- **Model role:** This is the one stage that benefits from real parallelism — N
  independent draft-generation calls, one per variant, run concurrently. This is the
  closest thing to "many workers" in the whole pipeline, and even here N is small
  (tens, not thousands) because Stage 5 has to be able to actually evaluate the output.

### Stage 4 — Asset Pool
- **Job:** For drafts that need visuals (thumbnail, carousel slides, clip crop),
  generate candidate images/crops.
- **Output:** `{draft_ref, asset_url, variant_id}`.
- **Note:** Image generation is the most expensive stage per unit — gate this on drafts
  that already survived an early cheap pass, not on every raw variant from Stage 3.

### Stage 5 — Scorer
- **Job:** Score every surviving draft+asset pair against explicit, written criteria —
  not vibes. Suggested rubric:
  | Criterion | What it checks |
  |---|---|
  | On-brand | Matches the account's established voice/topics |
  | Factual | Claims in the draft are checkable against Stage 1 source material |
  | Risk | Flags anything defamatory, impersonating, or making unverifiable claims about real people/orgs |
  | Novelty | Isn't a near-duplicate of something already posted this week |
  | Format fit | Matches what Stage 2 identified as currently working |
- **Output:** Ranked list with per-criterion scores, not just a single number — the
  human reviewing Stage 6's output needs to see *why*, not just a rank.

### Stage 6 — Gate
- **Job:** Hard-cut anything that fails the Risk or Factual criteria outright,
  regardless of how well it scores elsewhere. Everything else passes through ranked.
- **Output:** The day's shortlist (illustratively 3–7 items, matching the source post's
  own number) with scores and source evidence attached.

### Studio Lead (human)
- Reviews the shortlist, edits or approves, publishes manually (or via a platform's
  *official* scheduling tool, which is a deliberate choice distinct from Stage 6
  auto-posting).

## 4. What's deliberately NOT in this design

- **No auto-posting.** Stage 6 produces a shortlist, not a publish action.
- **No cross-platform coordinated posting.** Each platform has different automation
  policies; a system that posts the same content pattern across many accounts/platforms
  in a coordinated way is the specific shape platforms' inauthentic-behavior detection
  looks for, independent of content quality.
- **No fixed bot count.** "4,200" is not an engineering number — worker-pool size
  (Stage 3/4's N) should be tuned to what Stage 5 can meaningfully evaluate, and to your
  actual API rate limits, not to a marketing figure.

## 5. Minimum buildable slice

If you want a working v0 rather than just this doc, the smallest version that's still
useful:

1. Stage 1 for one source (e.g. X API search on a fixed query list).
2. Stage 2 as a single scheduled LLM call over the last hour's records.
3. Stage 3 producing 3 draft variants per surviving pattern.
4. Skip Stage 4 (no image gen) for v0.
5. Stage 5/6 collapsed into one scoring+gating call.
6. Output: a daily email/doc with the shortlist. No auto-post.

That's a buildable system in an afternoon, using one API credential and one LLM
account — worth confirming that's actually what you want before scaling it up.
