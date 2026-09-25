# Receipt — agent sitting 2026-09-24 (X algorithm)

**Filed:** 24 Sep 2026  
**Agent:** Cursor cloud agent  
**User request chain:** (1) full analysis of X algorithm from Elon post → (2) go deeper on incomplete/withheld → (3) add all to research  

---

## Method

| Step | What |
| --- | --- |
| Trigger post | X API `get_posts_by_id` on `2103238840072937532` (Elon) + quoted `2103234630342357089` (XOpenSource) + prior `2101103144004411696` (legal UTH expand) |
| Repo docs | Fetched GitHub README / RankingScorer / issue pages for `xai-org/x-algorithm` |
| Secondary | Web search: TechCrunch (Aug 2026 open-source), weight writeups (ppc.land, Ryan Lenk), [gist analysis @ c65aa17](https://gist.github.com/patricksavalle/366cf0da247c8d4594a1f7f4467502f5) |
| Limits | Some domains rejected by network allowlist (raw.githubusercontent.com, techcrunch.com, tech-ish.com); content recovered via GitHub HTML fetch / search snippets / gist |

## Outputs filed

| File | Role |
| --- | --- |
| [`README.md`](README.md) | Sitting entry |
| [`SYNTHESIS.md`](SYNTHESIS.md) | Full algorithm analysis |
| [`WITHHELD-MAP.md`](WITHHELD-MAP.md) | Incomplete / withheld map |
| [`raw/*.txt`](raw/) | Post receipts |
| [`extracts/SOURCE-INDEX.md`](extracts/SOURCE-INDEX.md) | URL index |

## Addendum 2026-09-25 (“Go”)

| Step | What |
| --- | --- |
| Sparse clone | `git clone --filter=blob:none --sparse` of `xai-org/x-algorithm` @ `bf7db1b` → `under-the-hood/strato/lib/underTheHoodLabels.strato` |
| Filed | [`CHECKLIST-UTH-LABELS.md`](CHECKLIST-UTH-LABELS.md) + verbatim extract [`extracts/SOURCE-underTheHoodLabels.strato`](extracts/SOURCE-underTheHoodLabels.strato) |

## Not done

- No full vendor of `xai-org/x-algorithm` into this monorepo (extract only)  
- No live Under the Hood JSON from a Crystal account (no credentials)  
- No Canon stamp  

*Non Solus.*
