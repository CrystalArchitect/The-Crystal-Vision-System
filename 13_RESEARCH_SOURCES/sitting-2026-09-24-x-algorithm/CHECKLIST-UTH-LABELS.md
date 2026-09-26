# Checklist — Under the Hood labels → reach impact

**Sitting:** 2026-09-24 (addendum 2026-09-25)  
**Canon:** no  
**Source of truth for copy:** [`extracts/SOURCE-underTheHoodLabels.strato`](extracts/SOURCE-underTheHoodLabels.strato) (from `xai-org/x-algorithm` sparse clone at sitting)  
**Companion:** [`WITHHELD-MAP.md`](WITHHELD-MAP.md) · [`SYNTHESIS.md`](SYNTHESIS.md)

Use this when you open [Under the Hood](https://x.com/i/jf/under_the_hood) or download the JSON. It maps each **published** label name to X’s own about/effect text, plus severity and “dark judgment” notes.

---

## 0. How to run this checklist on your report

1. Open UTH (or JSON). Confirm eligibility: account age ≥ 1 year, ≥ 10 eligible posts in the report month.
2. Note `postCount` / period.
3. For each entry in `postLabels[]` and `accountLabels[]`, copy `label` into the tables below.
4. Read **Effect class** first (what it does to reach), then **About** (why X says it fired).
5. Remember gaps:
   - **No provenance** — “automated or user report” often means either; author self-warnings can look like automation ([issue #39](https://github.com/xai-org/x-algorithm/issues/39)).
   - **No Phoenix score** — labels ≠ “ranked low.”
   - **Grox prompts dark** — if the about text says “automated systems,” the actual spam/hate/adult criteria live in withheld `.j2` prompts ([`WITHHELD-MAP.md`](WITHHELD-MAP.md) Tier A).

### Severity key

| Class | Meaning |
| --- | --- |
| **HARD** | Not shown on X (or pending deletion / worldwide withhold) |
| **OON** | Hidden from recommendations to non-followers (followers may still see) |
| **VIS** | Interstitial / content warning / age gate — still exists, restricted presentation |
| **PROFILE** | Discoverability limited (e.g. FOSNR → mostly profile) |
| **LEGAL** | Country or worldwide legal/copyright withhold |

---

## 1. Post labels (18)

| Label | Class | Effect (verbatim summary from strato) | About (short) | Dark note |
| --- | --- | --- | --- | --- |
| `SPAM` | HARD | Post is not shown on X | Authenticity policy; automated **or** user report | Prompt criteria withheld |
| `PDNA` | HARD | Not shown while pending further review | ToS; automated | |
| `BOUNCE` | HARD | Not shown while pending deletion by author | ToS; automated **or** report | |
| `SPAM_HIGH_RECALL` | OON | Hidden from recommendations to non-followers | “May contain spam”; automated | Classic “followers OK / For You dead” signature |
| `MALICIOUS_URL` | OON | Hidden from recommendations to non-followers | Likely malicious link; automated | |
| `DO_NOT_AMPLIFY` | OON | Same (legacy; being replaced by `MALICIOUS_URL`) | Historical malicious-link path | Treat as legacy OON |
| `NSFW_HIGH_RECALL` | OON+age | Hidden from OON + underage / no-age / logged-out | May be adult content; automated | |
| `NSFW_TEXT` | OON+age | Hidden from OON + age/logged-out gates | Explicit language; automated | |
| `NSFW_HIGH_PRECISION` | VIS+OON+age | Content warning + OON hide + age gates; India: local-law restricted presentation | Likely adult; automated **or** report | **May be author content warning** — provenance missing |
| `NSFW_CARD_IMAGE` | VIS+OON+age | Warning + OON + age gates | Adult policy; automated | |
| `NSFW_ADMIN` | VIS+OON+age | Warning + OON + age gates | Author has `NsfwAdmin` (report-driven account stamp) | Human/report path at account level |
| `GORE_AND_VIOLENCE_HIGH_PRECISION` | VIS+OON+age | Warning + OON + age gates | Violent content; automated **or** report | |
| `FOSNR_ABUSE` | PROFILE | Discoverability → author profile; public limited-visibility label | Abuse/harassment; **user report** | |
| `FOSNR_HATEFUL_CONDUCT` | PROFILE | Same | Hateful conduct; automation **or** report | Prompt dark if automated |
| `FOSNR_VIOLENT_SPEECH` | PROFILE | Same | Violent content; **user report** | |
| `FOSNR_CIVIC_INTEGRITY` | PROFILE | Same | Civic integrity; **user report** | |
| `FOSNR_ABUSE_INSULTS` | OON+label | Hidden from OON; public limited-visibility label | Abuse/harassment; automation **or** report | |
| `FOR_EMERGENCY_USE_ONLY` | VIS+Home | Notice; not shown in Home timeline | Emergency incident-response | Rare / ops |

Alias: `NSFW_ADMIN_STAMPED` → `NSFW_ADMIN`.

---

## 2. Account labels (12)

Account labels typically hide **all** posts from OON recommendations (unless noted).

| Label | Class | Effect (short) | About (short) | Dark note |
| --- | --- | --- | --- | --- |
| `ReadOnly` | HARD-ish + OON | Read-only until violating post removed; posts hidden from OON | ToS requires post removal | |
| `Compromised` | OON | Posts hidden from OON; password reset required | Compromised; automated **or** report | |
| `SpamHighRecall` | OON | Posts hidden from OON | Likely to post spam; automated | Often rollup from post spam labels |
| `NsfwHighRecall` | OON | Posts hidden from OON | May post adult content; automated | |
| `NsfwHighPrecision` | OON | Posts hidden from OON | Likely adult content; automated | May interact with self-labeled posts — ambiguous |
| `NsfwAvatarImage` | OON | Posts hidden from OON | Adult policy (avatar); automated | |
| `NsfwBannerImage` | OON | Posts hidden from OON | Adult policy (banner); automated | |
| `NsfwNearPerfect` | OON | Posts hidden from OON | Adult policy; automated | |
| `NsfwAdmin` | VIS+OON+age | Warnings + OON + age gates on posts | Report: primarily adult/violent poster | Explicit **human/report** stamp |
| `ImpersonationHighPrecision` | OON | Posts hidden from OON | Authenticity; automated | |
| `AbusiveHighRecall` | OON + challenge | Posts hidden from OON; security challenge | Authenticity / automated abuse | |
| `DoNotAmplify` | OON | Posts hidden from OON pending further review | Likely ToS violation; automated | |

---

## 3. Legal / copyright takedowns (UTH expanded Sep 2026)

These appear as withhold labels (country codes filled into `{countries}`).

### Post takedowns

| Key pattern | Class | Effect |
| --- | --- | --- |
| `LegalRequest(COUNTRY)` | LEGAL | Not shown in listed countries |
| `BystanderReport(COUNTRY)` | LEGAL | Not shown in listed countries (third-party local-law report) |
| `UnspecifiedReason(COUNTRY)` | LEGAL | Legacy country withhold |
| `LegalRequest(xx)` / `UnspecifiedReason(xx)` | HARD | Not shown on X (worldwide) |
| `UnspecifiedReason(xy)` / `Dmca` | HARD | Not shown (copyright) |
| `is_dmca` | OON+media | Hidden from OON; where seen, media unavailable |

### Account takedowns

Same `LegalRequest` / `BystanderReport` / `UnspecifiedReason` patterns → account’s posts withheld in those countries (or worldwide for `xx`).

---

## 4. Interpretation cheatsheet

| If you see… | Likely reach picture |
| --- | --- |
| Only `SPAM_HIGH_RECALL` / `SpamHighRecall` / `MALICIOUS_URL` / `DoNotAmplify` | Followers may still see you; **For You / OON discovery crushed** |
| `SPAM` / `PDNA` / `BOUNCE` / worldwide legal | Near-total non-distribution |
| FOSNR_* | Post lives mainly on **profile**; limited discoverability |
| NSFW_* with interstitial | Still on platform; warnings + OON/age limits |
| `NsfwAdmin` / `NSFW_ADMIN` | Report-driven adult/violent account treatment |
| Empty post+account labels | UTH does **not** explain soft ranking death — check weights/playbook in SYNTHESIS, not labels |

### Rollup reminder

Post labels can aggregate into account labels (`safety-label-user-agg`). A few NSFW/spam posts → account-level OON suppression with TTL. High PageRank / grey badge often **exempt** from automated enforcement paths ([`WITHHELD-MAP.md`](WITHHELD-MAP.md) Tier C5).

---

## 5. JSON field map (serving shape)

From `underTheHoodReport.User.strato` build path (public):

| Field | Meaning |
| --- | --- |
| `period` | Report month window (UTC) |
| `postCount` | Eligible posts in month |
| `postLabels[].label` | Canonical post label name |
| `postLabels[].about` / `.effect` | Static strings from this catalog |
| `postLabels[].posts` / `.percentageOfPosts` | How many posts carried the label |
| `accountLabels[].label` | Canonical account label |
| `accountLabels[].days` / `.percentageOfDays` | Days label was active in period |
| `generatedAt` | Report build time |

**Absent:** `source` / `rule_id` / `actor` / Phoenix scores / brandSafety (schema exists, unused).

---

## 6. Worksheet (print / paste)

```
Account: _______________   Month: _______________   postCount: ____

Post labels found:
[ ] _______________  posts: ____  class: HARD/OON/VIS/PROFILE/LEGAL
[ ] _______________  posts: ____  class: …
Notes (self-warning? report?): _________________________________

Account labels found:
[ ] _______________  days: ____  class: …
[ ] _______________  days: ____  class: …

Legal/takedown:
[ ] _______________  countries: _______________

Empty report? → ranking/weights path, not label path.
```

---

## Honesty

- Catalog is the **allowlist of labels UTH will explain** — not every internal safety label that may exist upstream.
- Effect strings are X’s public copy; live VF rule names in `visibility-filtering/rules/registry.rs` are the enforcement mechanism.
- This checklist does **not** teach evasion of spam/safety systems.

*Non Solus.*
