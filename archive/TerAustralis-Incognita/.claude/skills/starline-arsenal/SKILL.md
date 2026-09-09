---
name: starline-arsenal
display_name: Starline Arsenal — 42 Model Armoury
description: Australian-built cognitive armoury of 42 mental models across seven wings — deconstruction, prediction, creation, adaptation, reading, speech, and operational execution. Runs core questions to produce concrete outputs — failure lists, leverage audits, Bayesian updates, exponential sketches, heuristic sheets, miscalibration checks, parable spines, philology glosses, rhetorical appeal maps, persuasion briefs, evidence-tier assignments, milestone sequences, risk registers — not just labels. Part of CrystalCore.OS / TerAustralis Incognita.
aliases: [model-armory, model-armoury, cognitive-armory, thinking-armory]
version: 4.0.0
author: TerAustralis Incognita
lore: Red Dust Ground Steady. Starline for navigation. Seven Sisters reference without appropriation. MarsBase DownUnder mindset.
---

# Starline Arsenal — 42 Model Armoury

**4.0.0 — Infrastructure Engines.** Adds a 7th wing, 10 operational/
execution models (33–42): Strategic Planning, Resource Orchestration,
Dependency Mapping, Risk Orchestration, Change Management, Tempo & Flow
State, Feedback Integration, Institutional Momentum, Legacy & Technical
Debt, Collective Thinking. **Label: Vision/exploratory** — unlike every
prior expansion of this armoury, these are not sourced to a canonical
Drive document; they follow the established 6-part template but have
not been checked against any external source text. A separate,
unrelated "Infrastructure Expansion" block (models 44–53, IDs
colliding with 33–42, content about software runtime engineering
rather than cognitive/reasoning models) was removed from this PR
before merge — it didn't fit this skill's domain and wasn't described
in the PR that introduced it.

**Formerly: model-armory / veil-breaker (parked)**

**3.0.0 — Reconciliation.** Models 14–25 (v2.0.0) were flagged on landing as
drafted, not verified against a source text. That source has now been
found and checked directly: two independent Google Drive lineages existed
in parallel — a 25-model line and a separate 21-model line, sharing some
models (Rhetoric, Persuasion) under different names — neither aware of
the other. Models 14–25 as drafted match the 25-model Drive line exactly.
This version adds the 6 models unique to the 21-model line (Heuristic,
Miscalibration, Regression to the Mean, Better-Than-Average, Parable,
Philology) as 26–31, giving one canonical 31. Full account:
[`../../../memory/OPEN-QUESTIONS.md`](../../../memory/OPEN-QUESTIONS.md)
"Starline Arsenal" section. The 21-model line also carried dated "Field
card" entries referencing a specific real situation and person; those are
operational notes, not general model content, and are deliberately not
carried into this file or its models.

**3.1.0 — Full verification pass.** Requested full verification of all 31
models, not just 14–25. Models 1–13 (pre-dating both Drive lineages,
landed 2026-08-14) were fetched fresh from the "Starline Arsenal Models"
Drive folder and confirmed byte-identical to the on-disk files, closing
out the last unchecked slice of the armoury. That same pass surfaced two
real fidelity gaps against the 21-model line's own source text, now
fixed: (1) [`models/30-parable.md`](models/30-parable.md) was missing the
source's explicit "no borrowed lyrics" rule — added to Purpose and
Anti-Pattern. (2) [`models/21-rhetoric.md`](models/21-rhetoric.md) and
[`models/25-persuasion.md`](models/25-persuasion.md) had kept the plainer
25-model-line wording where a richer, later-dated (29 Aug) version existed
in the 21-model line — Rhetoric now runs the five classical canons and
the ethos/pathos/logos/kairos appeal square instead of a bare three-appeal
list; Persuasion now asks for the audience's honest no explicitly, not
just an objection answered. Governance gained the Speech Rule from that
same source. No model IDs, slugs, or groups changed.

**3.2.0 — Provenance Stack.** A separate, concurrent session (PR #138)
independently proposed generalizing the ad hoc etymology fact-checking in
[`../../../memory/LANGUAGE-AS-PROGRAMMING.md`](../../../memory/LANGUAGE-AS-PROGRAMMING.md)
into a reusable evidence-tier method — see
[`../../../memory/ETYMOLOGY-STACK.md`](../../../memory/ETYMOLOGY-STACK.md) —
and a corresponding model, on top of the old 25-model `main`, numbered 26.
That number collides with this armoury's own 26 (Heuristic Thinking), so
it lands here as **32 — Provenance Stack**, content unchanged from the
original proposal apart from the renumber. Cross-reference sections added
to the four models with genuine overlap:
[`models/01-first-principles.md`](models/01-first-principles.md),
[`models/14-occams-razor.md`](models/14-occams-razor.md),
[`models/18-circle-of-competence.md`](models/18-circle-of-competence.md),
[`models/19-inference.md`](models/19-inference.md) — each stating the
actual differentiation, not just a link.

**3.3.0 — Six wings, not four.** A Grok session's own correction card
(Google Drive, "CVSC" collection, 2026-09-01) confirms directly: "Starline
Arsenal working kit is 21 models v1.3.0, not only the public four-verb
slogan" — the four-verb DECONSTRUCT/PREDICT/CREATE/ADAPT framing seen in
public X posts is a poster slogan, not the full taxonomy. The 21-model
Drive source this armoury was reconciled from in 3.0.0 already carried
six group headers — Deconstructors, Predictors, Creators, Adaptors,
**Readers**, **Speakers** — but the 3.0.0 merge filed Readers/Speakers
content under the original four groups instead of preserving the wings.
Fixed here: [`models/26-heuristic.md`](models/26-heuristic.md),
[`models/30-parable.md`](models/30-parable.md), and
[`models/31-philology.md`](models/31-philology.md) move to **The
Readers**; [`models/21-rhetoric.md`](models/21-rhetoric.md) and
[`models/25-persuasion.md`](models/25-persuasion.md) move to **The
Speakers**. Model IDs, slugs, and content unchanged — only `group`
frontmatter, in-file headers, `INDEX.md`, and this file's section
structure. Same source card, notably, does not mention "Erisian Blade" as
part of Starline Arsenal at all — weak evidence toward it being a
separate persona/tool rather than an unlisted 33rd model; see
`../../../memory/OPEN-QUESTIONS.md`.

Concrete thinking tools. Each model runs core questions and produces a tangible artefact. Do not merely name the model — execute it.

## The Deconstructors — Take it apart to bedrock

### 1. First Principles
- Strip to irreducible truths. What is evidenced vs assumed?
- Output: Bedrock list + Assumption list + Rebuild from zero

### 2. Systems Thinking
- Map stocks, flows, feedback loops, delays.
- Output: Loop map + Leverage point audit

### 3. Scale Thinking
- What breaks at 10x / 100x? What emerges?
- Output: Scale failure list + Non-linear threshold list

### 14. Occam's Razor
- Fewest assumptions that still fit the evidence.
- Output: Explanation list ranked by assumption count + Cut list

### 15. Root Cause Analysis (5 Whys)
- Chase a symptom back to its origin.
- Output: Why-chain + Root cause statement + Prevention action

### 16. Recursion
- Reduce to a smaller version of the same problem plus a base case.
- Output: Self-similar structure + Base case + Termination check

### 32. Provenance Stack
- Grade evidence tiers before treating a claim as settled — attested, reconstructed, proposed, disputed, folk, speculative, or symbolic.
- Output: Evidence tier assignment + Confidence-vs-tier mismatch flag + Missing-evidence list

## The Predictors — See around the corner

### 4. Second-Order Thinking
- Consequence of consequence.
- Output: 1st / 2nd / 3rd order chain + Hidden cost

### 5. Inversion
- Invert, avoid, kill the company.
- Output: Failure modes + Don't-do list

### 6. Probabilistic Thinking
- Ranges, not points. Base rates.
- Output: Probability ranges + Base rate check

### 7. Bayesian Thinking
- Update with evidence. Prior → Evidence → Posterior.
- Output: Bayesian update sheet (prior, likelihood, posterior)

### 8. Non-Linear Thinking
- Exponential, S-curve, power law.
- Output: Exponential sketch + Inflection hunt

### 17. Game Theory
- Model the players, incentives, and stable outcomes.
- Output: Player/incentive table + Payoff matrix + Equilibrium call

### 18. Circle of Competence
- Know the honest edge of what you understand.
- Output: Inside/outside-circle lists + Expert-gap check

### 19. Inference
- Draw the conclusion the evidence supports, and name which kind.
- Output: Observed vs inferred split + Inference type + Confidence

### 27. Miscalibration
- Score, guess, and method are three different objects; a famous effect is not a character.
- Output: Miscalibration sheet + Confidence-vs-accuracy gap

### 28. Regression to the Mean
- Is this a real trend, or an extreme point drifting back toward average?
- Output: Regression check + Extreme-vs-baseline comparison

### 29. Better-Than-Average Thinking
- Is this self-assessment realistic, or the standard effect where most people rate themselves above the median?
- Output: Better-than-average audit + Self-vs-peer comparison

## The Creators — Make new paths

### 9. Lateral Thinking
- Random entry, provocation, reframe.
- Output: 3 oblique paths + Reframe

### 10. Design Thinking
- User, job, constraint, prototype.
- Output: JTBD + Constraint map + Low-fi prototype spec

### 20. Analogical / Combinatorial Thinking
- Borrow a structure from one domain, recombine into another.
- Output: Structural mapping + Combination sketch + Novel output

## The Adaptors — Bend without breaking

### 11. Dialectics
- Thesis / Antithesis / Synthesis
- Output: Tension table + Synthesis

### 12. Evolutionary Thinking
- Selection pressure, adaptation, extinction.
- Output: Selection audit + Adaptive option

### 13. Asymmetric Thinking (80/20)
- High leverage, low input. Where is 80/20, 90/10?
- Output: Asymmetry map + 80/20 leverage list

### 22. OODA Loop
- Observe, Orient, Decide, Act — faster than what you're up against.
- Output: OODA snapshot + Orientation update + Loop-speed comparison

### 23. Antifragility
- What gains from shock and disorder instead of just surviving it.
- Output: Stressor inventory + Fragile/robust/antifragile classification

### 24. Margin of Safety
- Build in the buffer that survives being wrong.
- Output: Best-estimate vs worst-case table + Buffer size

## The Readers — Make meaning without closing the book

### 26. Heuristic Thinking
- Name the mental shortcut in play — availability, representativeness, anchoring — before trusting the snap judgment.
- Output: Heuristic sheet + Bias family named + Debias check

### 30. Parable Thinking
- What story, carrying the same structure as this problem, makes the lesson land without argument? Not a fable, not an allegory, no borrowed lyrics.
- Output: Parable spine + Structural mapping to the real situation

### 31. Philology
- Read the exact line slowly, before the paraphrase built on top of it.
- Output: Exact line + Gloss + Drift list + Slow-read verdict

## The Speakers — Move a mind without owning it

### 21. Rhetoric
- Build the argument that actually lands — which appeal is doing the work, ethos, pathos, logos, or kairos.
- Output: Appeal map (ethos / pathos / logos / kairos) + Arrangement + Figure named

### 25. Persuasion
- Shift another's position through legitimate influence, not coercion — and know their honest no when you hear it.
- Output: Current-position statement + Smallest-ask sequence + Honest no + Next smallest move

## The Infrastructure Engines — Operational execution

### 33. Strategic Planning
- From insight to roadmap. What is the sequence? What moves now?
- Output: Milestone sequence + Dependency graph + Critical path + Go/no-go criteria

### 34. Resource Orchestration
- Align people, time, budget, tools to execution. What is scarce?
- Output: Resource map + Constraint list + Allocation strategy + Waste audit

### 35. Dependency Mapping
- What must happen before what? What is the critical path?
- Output: Dependency diagram + Critical path + Bottleneck list + Reorder opportunities

### 36. Risk Orchestration
- Identify, rank, and structure responses to operational risks.
- Output: Risk register + Response strategy per risk + Early warning indicators + Contingency triggers

### 37. Change Management
- Move an organization or system from state A to state B while keeping it functional.
- Output: Stakeholder map + Transition plan + Resistance audit + Success story

### 38. Tempo & Flow State
- What rhythm allows sustainable high-quality output? Speed vs. quality trade-off.
- Output: Tempo audit + Flow condition checklist + Quality-speed trade-off map + Sustainability map

### 39. Feedback Integration
- Gather signal, filter noise, update the plan. Close the learning loop.
- Output: Feedback loop diagram + Signal/noise separation + Bias audit + Update trigger

### 40. Institutional Momentum
- What keeps moving when you stop pushing? What is the organization's inertia?
- Output: Momentum audit + Sustaining structure map + Decay risk list + Anchor plan

### 41. Legacy & Technical Debt
- What are we carrying that slows us down? When to pay off vs. carry forward.
- Output: Debt inventory + Interest cost audit + Payoff-vs-carry analysis + Payoff priority list

### 42. Collective Thinking
- How do groups of minds amplify or interfere with each other? Team cognition.
- Output: Interaction pattern map + Amplification points + Interference audit + Voice map

## Governance (CrystalCore.OS)
- Incognita Rule: Evidence > Assumption
- Belt-Three Rule: Vision labelled as vision, not measured fact
- Register Integrity: No register impersonates another
- Authority Boundary: Uncertainty never converted silently to authority
- Reader Rule: A shortcut, a story, or a gloss is not a verdict until the skipped fact is named
- Stamp Rule: A famous effect is not a character. Score, guess, method — or do not use the name.
- Privacy Rule: Do not use a real person's private situation as a worked example unless they ask. Generic rooms only.
- Speech Rule: Name the appeal. Do not baptise the speaker. An ask that requires fusion is not persuasion.

## Usage
Run as skill: invoke model → answer core questions → produce artefact → log to CHRONICLE as Evidence → Interpretation → Experiment → Record.

Full detail per model, including the five Core Questions and Required Concrete Output each one demands: [`INDEX.md`](INDEX.md) → `models/01-first-principles.md` through `models/42-collective-thinking.md`.

Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059
