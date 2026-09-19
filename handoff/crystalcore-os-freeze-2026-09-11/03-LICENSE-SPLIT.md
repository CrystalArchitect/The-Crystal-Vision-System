# License split — proposal for Crystal stamp

**Current state:** CrystalCore.OS `LICENSE` is CC BY-NC-ND 4.0 on the whole tree. That license forbids commercial use and forbids distributing derivatives. A buyer cannot ship a product under it. That is the single largest discount on the $95k artifact number.

**Proposed split (not executed until Crystal stamps):**

| Layer | Path glob | Proposed license | Why |
|---|---|---|---|
| Runnable code | `index.html`, `backend/**`, companion `*.py`, protocol modules, tests | **Apache-2.0** | Buyers and contributors can use, modify, ship. Patent grant. Attribution kept. |
| Specifications that describe running code | `docs/architecture/*`, CONSENT-GATE-SPEC, WHAT-RUNS | **Apache-2.0** or CC BY 4.0 | Specs must move with the code |
| Mythos, Codex, songs, narrative terminal prose, vision essays | `mythos/**`, vision-layer markdown, art | **CC BY-NC-ND 4.0** | Story stays Crystal’s; no commercial remix without a deal |
| Company name, product name, SAT mark | names / ™ | **not licensed out** | Trademark, not copyright |

`crystalcore_os.py` is a hybrid: the *program* can be Apache-2.0; the *narrative strings* can stay ND if you extract them. Until extracted, mark the file `SPDX-License-Identifier: Apache-2.0 AND CC-BY-NC-ND-4.0` and put the split in NOTICE.

## What this does to value

- Keep ND on code → transaction range stays ~$35k–$80k (a buyer is licensing a reading copy).
- Split as above → transaction range can sit in the original $35k–$220k band without the license being the first objection.
- Exclusive commercial assignment of mythos + code → that is a **company** deal, not a product artifact sale. Price that separately.

## NOTICE block to add on stamp

```
CrystalCore.OS
Copyright 2026 Crystal Arena-Turner / TerAustralis Incognita

Code and executable specs: Apache-2.0 (see LICENSE-CODE)
Mythos and vision prose: CC BY-NC-ND 4.0 (see LICENSE-MYTHOS)
Names TerAustralis Incognita and CrystalCore.OS are unlicensed trademarks of the company.
MemClaw-inspired concepts: see docs/ATTRIBUTIONS.md (Apache-2.0 upstream).
```

## What not to do

- Do not put Apache-2.0 on the Codex or Gate-Opening narrative.
- Do not leave ND on `backend/` if the company intends to sell software.
- Do not claim “open source” while ND remains on the runnable tree. ND is source-available, not open source.
