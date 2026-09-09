# SURFACE.md — ContextGate (canon, called once)

Do not rewrite mid-build without Crystal’s say-so. Code quotes this file.

- **Offer name:** ContextGate
- **For whom:** Crystal Elle Arena-Turner / TerAustralis operators (and later, any desk that runs AI sessions where invented facts and token burn hurt).
- **The hole:** Models fill silence with plausible text. Context windows fill with restatement. Neither is a clinical urgency signal — both look like “helpfulness.” There is no small, deterministic gate that scores a draft *before* it ships, the way veTriage scores a sick-pet call before it hits the vet.
- **Price:** TBD — internal tool first. Not a subscription.
- **Promise:** One pass over a draft or session note. One colour. One authorized next step. Same answers → same colour every time.
- **Headline:** Urgency is not vibes. Capacity is not truth.
- **Subhead:** Clinical-style triage for AI output — context, hallucination risk, token burn — without letting the model mark its own homework.
- **CTA:** Paste the draft. Run the gate. Override only if you mean it.
- **Built product, not Vision.** Live routing is deterministic rules. Generative AI may help *write* rules; it does not decide the colour at runtime.

---

## Non-goals

- Not a fine-tune of Grok.
- Not reverse-engineering X / recommendation ranking.
- Not an LLM “fact checker” that asks another model if a claim is true.
- Not a full IDE or agent OS.
- Not medical advice, legal advice, or a replacement for Incognita / PRIVACY judgment.

## Human authority

- Anyone can escalate **up** (mark greener output as riskier).
- Only Crystal (operator) may **downgrade** a RED or force-send past a block — with a written reason logged.
- Original RED trigger stays visible after override (audit).

## First three rules (v0)

1. **RED — unsourced hard claim.** A sentence that asserts a specific fact (org location, product name, dollar figure, “we verified,” named person email, legal status) with no `source:` tag, URL, file path, or tool-id in the same block → RED. Next step: label as hypothesis or attach source; do not ship as Built.
2. **ORANGE — context / token budget.** Estimated tokens for draft + declared session used > `budget_ratio` (default 0.7) of `window_tokens`, **or** draft alone > `max_draft_tokens` (default 800) → ORANGE. Next step: compress, split, or drop restatement before continue.
3. **YELLOW — filler / restatement.** Draft matches filler patterns (opens with “Certainly/Of course/I’d be happy to,” or repeats the user ask for >2 sentences before new content) → YELLOW. Next step: rewrite lead-with-result.

GREEN = none of the above fire.

Capacity (how tired the session is) must not flip a RED claim to GREEN.

## Colours → action

| Colour | Meaning | Authorized next step |
|--------|---------|----------------------|
| RED | Invented / unsourced Built claim | Stop. Source or mark hypothesis. |
| ORANGE | Window or draft too fat | Compress / split before send. |
| YELLOW | Soft waste | Trim opener; lead with result. |
| GREEN | Passes v0 gate | May send. |

## Version

- **rules_version:** `0.1.0`
- **Date locked:** 2026-09-04
- **Operator:** Crystal Elle Arena-Turner · TerAustralis Incognita
