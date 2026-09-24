# Withheld / missing map — X algorithm transparency

**Sitting:** 2026-09-24  
**Subject:** What `xai-org/x-algorithm` + Under the Hood do **not** fully expose  
**Canon:** no  
**Companion:** [`SYNTHESIS.md`](SYNTHESIS.md)

---

## Transparency stack

```
┌─────────────────────────────────────────────────────────────┐
│  A. PUBLISHED & AUDITABLE                                   │
│     Ranking formula, filters, VF rules, weight defaults,    │
│     UserCred formula, UTH aggregation code                  │
├─────────────────────────────────────────────────────────────┤
│  B. PUBLISHED BUT UNTRUSTWORTHY / SNAPSHOT                  │
│     Enforcement YAML (GrowthBook mirror), mock thresholds   │
├─────────────────────────────────────────────────────────────┤
│  C. REFERENCED BUT ABSENT                                   │
│     Grox .j2 prompts, some botmaker rules, model checkpoints│
├─────────────────────────────────────────────────────────────┤
│  D. EXISTS IN PROD, NOT IN REPO                             │
│     Feature switches, reply ranking, Following/Search/…,    │
│     ads auction, training data, allowlist contents          │
├─────────────────────────────────────────────────────────────┤
│  E. PARTIAL USER VIEW (Under the Hood)                      │
│     Labels + legal limits; no scores / source provenance    │
└─────────────────────────────────────────────────────────────┘
```

Repo scope = **For You** ranking + visibility filtering + related labeling — not “all of X.”

---

## Tier A — Officially withheld (README admits)

| Missing | Stated reason | Why it matters |
| --- | --- | --- |
| **Grox LLM prompts** (`.j2`) | Anti-gaming | Semantic policy for spam / hate / violence / illegal / adult / PTOS / coordinated spam / reply scoring |
| **Some botmaker rules** | Anti-gaming | Event → label paths scarecrow never fully publishes |

### Known missing prompt templates

Imported by `grox/flows/*/prompts.py`; **zero** `.j2` in repo (comment: excluded per README). Includes:

- `spam_policy.j2`
- `hate_or_abuse_policy.j2`
- `violent_speech_policy.j2`
- `illegal_and_regulated_behaviors_policy.j2`
- `adult_content_policy.j2`
- `safety_ptos.j2`
- `coordinated_spam_system.j2`
- `reply_scoring_system.j2`
- (~14 total referenced)

**Also dark in same family:** `grox/prompts/` module; PostSafetyDeluxe / `TweetBoolMetadata` fact lists tied to withheld prompts (annotator flags without published meanings).

**Effect:** You can see *that* a label exists and *what VF does with it*. You cannot see *how* the LLM decided the post matched.

---

## Tier B — Published but falsified or stale

| Item | What’s wrong | Impact |
| --- | --- | --- |
| Enforcement thresholds | e.g. `follower_count >= 12.34` marked *“mock value to reduce gaming”* (`enforcement_user.yaml` / `enforcement_post.yaml`) | Real high-follower bypass floor unknown |
| GrowthBook enforcement YAML | Dated `# mirrored from GrowthBook… last sync …` | Live edits via `PUT/PATCH /api/config` without repo commit |
| `param.rs` defaults | Cron-synced “primary production” | Per-viewer feature switches can override |

Shape of enforcement is public; **live numbers** are not.

---

## Tier C — Wired in code; config/data not shipped

### C1. Per-viewer / per-author feature switches

- Recipient: `user_id`, country, language, client app, roles, datacenter, account age, phone status  
- Config e.g. `rust_home_mixer.yml` — **not in repo**  
- Every `param!` can resolve differently per person  
- `AuthorRulesEvaluator` keys off **author** ID (generic; cold-start uses it)

### C2. Phoenix production model

- No production checkpoints, training data, or real embeddings in public tree  
- `phoenix/reference` = synthetic stand-in  
- **Published:** `Score = Σ w × P`  
- **Missing:** live `P`  

Largest gap for “why did *my* post die for *this* audience?”

### C3. Feedback-loop / learned bias

Model trains on logged feed behavior. Temporary suppression can reshape future engagement → lasting downranking with **no rule left in repo**. Code cannot prove or disprove intentional steering via this path.

### C4. Manual / privileged channels (internal audit, not public)

| Channel | Role |
| --- | --- |
| User/post allowlist | Skip enforcement; named actor + reason; ≤90-day TTL |
| `POST /api/action` | Manual/debug enforcement intake |
| GrowthBook replace/patch | Change rules without Git |
| Admin labels (`NsfwAdmin`, etc.) | Human-stamped |
| Guano notes | Internal notes |
| Kafka `AdminActionEvent` | Internal audit trail |

### C5. Credibility bypass (logic public, floors mocked)

Before violation checks, skip when:

- High follower count (**real floor mocked**)  
- `cred.is_high` or UserCred ≥ **50**

Compounds with post→account rollup exemptions for high PageRank / grey badge; botmaker `IsHighPageRankUser` / verified primitives.

---

## Tier D — Entire surfaces outside this repo

| Surface | Status |
| --- | --- |
| Following timeline | Out of scope |
| Search / Explore / Trends | Out of scope |
| Notifications ranking | Out of scope |
| **Reply / conversation ranking under a post** | Separate service — where `RiskyHighVizReply` / `LowQualityReply` + reply-scoring prompt bite |
| Ads auction / bid logic | Blender interleaves; auction opaque |
| Who to Follow model | Positions known; model opaque |
| Community Notes | Separate |
| DMs / Spaces / Grok product chatbot | Separate |
| Full deploy/infra | Often omitted (`xai_service_runner`, Kafka wiring, …) |

---

## Tier E — Under the Hood gaps

| Present | Missing |
| --- | --- |
| Monthly label counts | **Label source** (automated vs author warning vs report vs human) — [issue #39](https://github.com/xai-org/x-algorithm/issues/39) |
| Legal / government withholding (expanded Sep 2026) | Per-viewer Phoenix scores |
| Static about/effect text per label | Live restriction status (historical month only) |
| Eligibility gates | Why *you* weren’t retrieved for a specific viewer |
| | Exact botmaker `rule_id` / agent |
| | Brand-safety aggs (schema fields exist; marked unused/empty) |

Upstream provenance variants exist (`BotmakerAction` / `ToolAction` / `GrokAnnotationAction`) but are **dropped** before report JSON. README claim that you can see whether labels were “manually applied” is only **partially** true.

Community PRs (e.g. tracking [#45](https://github.com/xai-org/x-algorithm/issues/45)) proposed richer UTH / expiry / credibility fixes; not treated as shipped here.

---

## Side-by-side auditability

| Question | Auditable from public code? |
| --- | --- |
| How is a For You score combined? | Yes — weights + formula |
| What pre-filters / VF drop rules exist? | Mostly yes (~54 VF rules in analyzed commits) |
| Why did Grok call this spam/hate? | **No** — prompts withheld |
| Exact live enforcement thresholds? | **No** — mocked / GrowthBook |
| Did my weights match production for me? | **No** — feature switches |
| What P(like)/P(report) did Phoenix assign? | **No** — model private |
| Am I allowlisted / admin-labeled? | Only if it surfaces as a UTH label |
| Why replies under big accounts die? | Partial — For You filters public; reply ranker + prompt private |
| Government country withhold? | Improving via UTH; still coarse |

---

## Largest unauditable surfaces (ranked)

1. Grox policy prompts  
2. Live Phoenix probabilities  
3. Feature-switch YAML  
4. GrowthBook + mock thresholds  
5. Reply/conversation ranking service  
6. Manual allowlist / admin actions  
7. UTH without provenance  

---

## Bottom line

X published the **skeleton** (pipeline, arithmetic, filter lists, VF registry) and a user-facing **label dump**.

Withheld: **judgment layer** (prompts), **brain** (trained model + data), **live dials** (feature switches / GrowthBook), adjacent **products** (Following, Search, reply ranker, ads auction).

Strong transparency on *structure*; weak transparency on *why a specific post was labeled or scored*.

---

## Primary evidence pointers

| Claim class | Where |
| --- | --- |
| Official “what’s not in this repo” | [README](https://github.com/xai-org/x-algorithm/blob/main/README.md) § What’s not in this repo? |
| Mock thresholds / allowlist / GrowthBook | `abuse-enforcement-service/service-lib/rules/*.yaml` |
| Prompt exclusion comment | `grox/flows/*/prompts.py` (imports `.j2` that do not exist) |
| UTH schema without source | `under-the-hood/thrift/uth_serving.thrift` · issue #39 |
| Code-backed external map | [gist @ c65aa17](https://gist.github.com/patricksavalle/366cf0da247c8d4594a1f7f4467502f5) |
