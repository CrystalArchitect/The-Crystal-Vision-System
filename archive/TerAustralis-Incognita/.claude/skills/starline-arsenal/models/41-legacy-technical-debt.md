---
id: 41
slug: legacy-technical-debt
name: Legacy & Technical Debt
group: The Infrastructure Engines
arsenal: starline-arsenal
register: ARCHIVE + FORGE
primitive: audit() + prioritize()
---

# 41 — Legacy & Technical Debt (The Infrastructure Engines)

**Purpose:** What are we carrying that slows us down? When to pay off vs. carry forward.

**CrystalCore mapping:** Register ARCHIVE + FORGE | Primitive audit() + prioritize() | Past decisions made visible

## Core Questions — Run these, do not summarize

1. What legacy code, process, or decision are we still using primarily to avoid rewriting it?
2. What is the compound interest we pay (in bugs, slowness, friction) because of that legacy?
3. Is the interest we pay higher or lower than the cost of rewriting?
4. What would break if we removed this legacy, and do we have alternatives?
5. Which debts are blocking new capabilities, and which are merely annoying?

## Required Concrete Output — No vague labels

- Debt Inventory (ID | area [code/process/decision] | age | annual interest cost)
- Interest Cost Audit (slowness | bugs | friction | training tax | opportunity cost)
- Payoff vs. Carry Analysis (rewrite cost | payoff date | alternative paths)
- Payoff Priority List (what unblocks what, and what has the shortest payback)

## Evidence → Interpretation → Experiment → Record

- **Evidence:** What is the measured cost of carrying this debt (time, bugs, errors)?
- **Interpretation:** If we paid off this debt, what new speed would we gain?
- **Experiment:** Measure throughput with the legacy in place, then remove it for one sprint.
- **Record:** CHRONICLE entry as ARCHIVE (debt state) + FORGE (payoff plan)

## Anti-Pattern

Do not confuse "old" with "bad." Do not rewrite just because the code is unfashionable. Do not let perfect be the enemy of payoff. Do not hide debt by renaming it "technical foundation."

## Cross-references

[Institutional Momentum](40-institutional-momentum.md) — Institutional Momentum carries forward what works; Legacy & Technical Debt identifies what from the past is now slowing the present.

[Resource Orchestration](34-resource-orchestration.md) — Resource Orchestration allocates time; Legacy & Technical Debt identifies where that time is being taxed by accumulated decisions.

---
Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | Starline Arsenal | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059
