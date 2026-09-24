# X For You algorithm — open-source + Under the Hood (research sitting)

**Sitting:** 24 Sep 2026  
**Trigger:** [@elonmusk](https://x.com/elonmusk/status/2103238840072937532) quoting [@XOpenSource](https://x.com/XOpenSource/status/2103234630342357089) on Under the Hood UI  
**Drawer:** `13_RESEARCH_SOURCES` (external platform research — compass, not a CVS component)  
**Canon:** **no**

**Verdict (one line):** X published the For You **skeleton** (pipeline, weights, filters, VF rules) and a user **label dump** (Under the Hood); the **judgment layer** (Grox prompts), **brain** (live Phoenix P + checkpoints), and **live dials** (feature switches / GrowthBook / mock thresholds) remain incomplete — map in [`WITHHELD-MAP.md`](WITHHELD-MAP.md).

---

## Start here

1. [`SYNTHESIS.md`](SYNTHESIS.md) — full algorithm analysis (architecture, weights, playbook, UTH)  
2. [`WITHHELD-MAP.md`](WITHHELD-MAP.md) — **published vs withheld vs falsified vs out-of-scope**  
3. [`RECEIPT-agent-sitting-2026-09-24.md`](RECEIPT-agent-sitting-2026-09-24.md) — how this sitting was built  
4. [`raw/`](raw/) — source receipts (posts, repo pointers)  
5. [`extracts/SOURCE-INDEX.md`](extracts/SOURCE-INDEX.md) — URL / claim index

---

## Official URLs (live as of sitting)

| Artifact | URL |
| --- | --- |
| Elon quote (UTH pointer) | https://x.com/elonmusk/status/2103238840072937532 |
| X Open Source — Under the Hood UI | https://x.com/XOpenSource/status/2103234630342357089 |
| X Open Source — legal filtering expansion | https://x.com/XOpenSource/status/2101103144004411696 |
| Under the Hood (user tool) | https://x.com/i/jf/under_the_hood |
| Open-source repo | https://github.com/xai-org/x-algorithm |
| Repo README | https://github.com/xai-org/x-algorithm/blob/main/README.md |
| Ranking weights file | https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs |
| RankingScorer | https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/ranking_scorer.rs |
| UTH labels copy | https://github.com/xai-org/x-algorithm/blob/main/under-the-hood/strato/lib/underTheHoodLabels.strato |
| UTH provenance gap (issue) | https://github.com/xai-org/x-algorithm/issues/39 |

---

## What this is (and is not)

| Is | Is not |
| --- | --- |
| Research extract of public X algorithm + transparency tooling | Canon / Crystal stamp |
| Map of incomplete / withheld surfaces | Advice to game spam/safety systems |
| Source-backed compass for platform literacy | Claim that every weight equals production for every viewer |
| Companion to energy × AI / ICANN sittings (same day) | Merge with Drawer 16 AI Safety repos |

**Honesty:** Weights and VF rule counts below are from public writeups checked against `xai-org/x-algorithm` (esp. analysis @ `c65aa17`, Aug 2026). Live feature-switch overlays can diverge. Prefer re-reading `param.rs` before acting on a number.

*Non Solus.*
