# Synthesis — X For You algorithm (open source + Under the Hood)

**Date of sitting:** 24 September 2026 (UTC)  
**Analyst:** Cursor cloud agent  
**Drawer:** `13_RESEARCH_SOURCES` · Canon: **no**  
**Peg posts:** Elon [2103238840072937532](https://x.com/elonmusk/status/2103238840072937532) · XOpenSource [2103234630342357089](https://x.com/XOpenSource/status/2103234630342357089)

---

## 0. Honest limits

| Limit | Implication |
| --- | --- |
| Repo is **For You** + labeling/VF, not whole X | Following, Search, Trends, Notifications, ads auction, reply-thread ranker are mostly out of scope |
| Production Phoenix checkpoints / training data not shipped | Published weights multiply **P(action)** you cannot audit live |
| Feature-switch YAML not in repo | Defaults in `param.rs` ≈ primary production; per-viewer overrides possible |
| Enforcement YAML is GrowthBook snapshot + **mock** thresholds | Published numbers can be deliberately false |
| Grox `.j2` prompts withheld | Semantic “why labeled” is dark |
| Under the Hood drops label-source provenance | Automated vs author warning vs human review not separable in report JSON |

Companion map: [`WITHHELD-MAP.md`](WITHHELD-MAP.md).

---

## 1. What the trigger posts actually say

| When | Who | Claim |
| --- | --- | --- |
| 24 Sep 2026 ~21:43 UTC | @elonmusk | “Easy way to see how the 𝕏 algorithm works” — quotes X Open Source |
| 24 Sep 2026 ~21:26 UTC | @XOpenSource | New, easier Under the Hood UI; JSON download still available → `x.com/i/jf/under_the_hood` |
| 19 Sep 2026 | @XOpenSource | UTH expanded: prior-month labels **plus** government-required / legal visibility limits |

UTH eligibility (typical, from public coverage): account ≥ 1 year; ≥ 10 posts in prior month. Report is **monthly aggregate**, not live per-post scores.

Receipts: [`raw/SOURCE-elon-2103238840072937532.txt`](raw/SOURCE-elon-2103238840072937532.txt) · [`raw/SOURCE-xopensource-uth-ui.txt`](raw/SOURCE-xopensource-uth-ui.txt) · [`raw/SOURCE-xopensource-legal-expand.txt`](raw/SOURCE-xopensource-legal-expand.txt).

---

## 2. Big picture — two systems

For You is **not** one score.

1. **Ranking** — order candidates by predicted engagement for *this viewer*  
2. **Visibility filtering** — ALLOW / INTERSTITIAL / DROP for *this viewer*

High score can still be dropped after ranking. Open-source home: [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) (Apache 2.0). Major expansion **13 Aug 2026** (weights, VF, Phoenix train code, SimClusters, UTH).

---

## 3. Request path (Home Mixer)

```
Query hydrate → Candidate sources → Hydrate → Pre-filters
  → Phoenix score → RankingScorer → VMRanker → Top-K
  → Visibility filter → Dedup → Blend ads / WTF / prompts
```

### 3.1 Candidate sources

| Source | Type | Role |
| --- | --- | --- |
| Thunder | In-network | Recent posts from follows (in-memory) |
| Phoenix retrieval | Out-of-network | Two-tower embeddings + ANN |
| SimClusters | Out-of-network | Cluster similarity |

Funnel (public analyses): ~500M daily posts → ~1.5k candidates → score → top ~50 selected / ~35 returned (config-dependent).

### 3.2 Pre-scoring filters (hard drops)

Duplicates; age **> 48h**; own posts; blocks/mutes; muted keywords; already seen/served; inaccessible subscriber posts; OON retweet/reply filter; SimClusters NSFW author filter for non-followers; new-user min engagement; etc. (`home-mixer/filters/`).

### 3.3 Scoring

Phoenix (Grok-derived transformer, **candidate isolation**) predicts multi-action probabilities. Then:

```
Final Score = Σ (weight_i × P(action_i | viewer, post))
```

Weights multiply **predicted probabilities**, not raw engagement counts. X README (14 Aug 2026): do **not** read “report weight / like weight = one report cancels N likes.”

### 3.4 Post-score adjustments

- **Author diversity** — successive posts from same author decay (e.g. decay 0.5, floor 0.25 in public reads)  
- **Out-of-network discount** — OON scaled; also replies/reposts for followers (on by default in analyzed commits)  
- **New-author / cold-start boost** — low-follower / low-impression originals lifted toward a target rank under conditions  
- **VMRanker** — DPP-style diversity reorder  

### 3.5 Visibility filtering (after order)

Rules in `visibility-filtering/`. Base rules for all viewers + **recommendations-only** drop set for OON (spam high-recall, etc.). First drop wins. Followers may still see what OON cannot.

### 3.6 Blending

Ads, Who to Follow, prompts interleaved; ads blender can reorder for adjacency.

---

## 4. Ranking weights (public defaults snapshot)

From public transcriptions of `home-mixer/params/param.rs` (synced toward production; treat as **snapshot**, re-verify file):

| Action | Weight | Note |
| --- | --- | --- |
| Share via copy link | **+20.0** | Strongest positive |
| Reply | +5.0 | **+15 boost → 20** for eligible mutual-follow originals (`BidirectionalFollowReplyWeightBoost`; was 20 then lowered — see `docs/BIDIRECTIONAL_BOOST_CHANGE.md`) |
| Quote / Share via DM | +5.0 | |
| Follow author | +4.0 | |
| Share (generic) | +2.0 | |
| Repost | +1.0 | |
| Like | +0.5 | Weak alone |
| Click / open link | +0.4 / +0.2 | Open link is **positive** — no coded “link penalty” in VF list beyond malicious URL |
| Video open / photo expand / etc. | small | Some heads at **0.0** (off) |
| Cont. dwell time | ~0.004 | |
| Not dwelled | −0.02 | |
| Block author | −31.2 | |
| Not interested | −43.2 | |
| Mute author | −58.8 | |
| Report | **−234.0** | Strongest negative |

Secondary writeups: [ppc.land weights table](https://ppc.land/x-gives-copy-link-shares-a-feed-weight-of-20-against-0-5-for-likes/), [Ryan Lenk](https://www.ryanlenk.com/blogs/articles/x-algorithm-real-ranking-weights).

---

## 5. Labeling path (drives VF / UTH)

Continuous, not only on request:

| Layer | Examples |
| --- | --- |
| Content understanding | `grox/`, media models, CLIP |
| Account models | `agatha/`, `bdsm/`, `user-cred-v2/` |
| Rules | `scarecrow/` + `botmaker/` (+ **partial** `botmaker-rules/`) |
| Enforcement | `abuse-enforcement-service/`, `safety-label-user-agg/` |

Post labels can roll up to account labels (e.g. NSFW density → account restriction with TTL). High PageRank / grey badge often **exempt** from automated paths.

---

## 6. Under the Hood — what it closes

| Closes | Does not close |
| --- | --- |
| “Were visibility-impacting labels on me/my posts last month?” | Phoenix per-viewer scores |
| “Was reach limited by legal / government demand?” (post–19 Sep) | Why Grok matched a policy (prompts dark) |
| Match label name → public VF effect strings | Label **source** provenance (issue #39) |
| | Live restriction status (historical month only) |

Jobs/serving: `under-the-hood/`. Label copy: `underTheHoodLabels.strato`.

---

## 7. Practical playbook (from published arithmetic)

Not advice to evade safety — structural implications of public weights/filters:

1. **Original posts** beat replies/reposts for OON (four independent penalties stack on replies).  
2. **Copy-link / conversation** >> likes.  
3. **Mutuals** matter (bidirectional reply boost).  
4. **48h** hard age cutoff for For You candidacy.  
5. **Author diversity** — spam many posts into one slate → later posts decay.  
6. **One post per conversation** survives `DedupConversationFilter`.  
7. Check **UTH** monthly if eligible — labels explain OON disappearance better than “shadowban” folklore.  
8. Engagement outside Home Timeline may not train the same way (code comments emphasize Home Timeline logging for ranking).

---

## 8. Key design decisions (repo)

1. Multi-action prediction (policy in weights, not a single “relevance”)  
2. Candidate isolation (cacheable, consistent scores)  
3. Hash embeddings (new posts representable immediately)  
4. Ranking ≠ visibility  
5. Composable candidate-pipeline framework  

---

## 9. Cross-links (this monorepo)

| Sitting / drawer | Relation |
| --- | --- |
| [`../energy-ai-electricity-2026/`](../energy-ai-electricity-2026/) | Same-day Musk/X media sitting; different topic (watts) |
| [`../sitting-2026-09-19/elon-musk-filings-2026-09-16/`](../sitting-2026-09-19/elon-musk-filings-2026-09-16/) | Musk control / SEC filings evidence |
| [`16_AI_SAFETY_RESEARCH`](../../16_AI_SAFETY_RESEARCH/INDEX.md) | Platform ranking ≠ agent safety vault — connection ≠ merge |
| [`00_MEMORY/RESEARCH-STATUS.md`](../../00_MEMORY/RESEARCH-STATUS.md) | Cross-domain baseline (does not absorb this sitting) |

---

## 10. Sources (primary)

- [xai-org/x-algorithm README](https://github.com/xai-org/x-algorithm/blob/main/README.md)  
- Code-backed external extract: [gist patricksavalle @ c65aa17](https://gist.github.com/patricksavalle/366cf0da247c8d4594a1f7f4467502f5)  
- [GitHub issue #39](https://github.com/xai-org/x-algorithm/issues/39) (UTH provenance)  
- TechCrunch / industry coverage of 13 Aug 2026 open-source + UTH launch (secondary)

Full URL index: [`extracts/SOURCE-INDEX.md`](extracts/SOURCE-INDEX.md).
