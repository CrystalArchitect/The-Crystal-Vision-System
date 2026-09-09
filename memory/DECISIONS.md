# DECISIONS

Summaries only. The ADR file is the record. Status column in
[`docs/adr/README.md`](../docs/adr/README.md) is authoritative.

**How an ADR becomes Accepted:** maintainer merges the PR that carries it
([`Decision-Records.md`](../docs/governance/Decision-Records.md)). Until
then it is Proposed. Do not treat a draft ADR as law.

**Write-back:** when a new ADR is merged, add a row here and point at the
file. Do not rewrite Accepted ADRs. A reversed decision gets a new ADR.

**Sourced:** 2026-08-28 from the ADR index on
`bdddf0cdf4c2e47f7d517aaf9edbf1a9ba928b08`.

| ADR | Title (from the index) | Status | Memory note |
|---|---|---|---|
| [0001](../docs/adr/ADR-0001.md) | Adopt the CrystalCore OS v1.0 repository architecture | Accepted | Layout: docs / mythos / research / archive. Historical implementer named in the ADR stays as written. |
| [0002](../docs/adr/ADR-0002.md) | Content areas: the mythos stays a top-level peer of docs and src | Accepted | License-area split, not a nesting under `docs/`. |
| [0003](../docs/adr/ADR-0003.md) | Move code into src/ as a uniform shift; keep runtime-coupled files with their code | Accepted | Describes a tree that is **not in this git** (see README status note). |
| [0004](../docs/adr/ADR-0004.md) | Lock the CrystalCore naming taxonomy; ban future CrystalCore-* runtime names | Accepted | Framework / Protocol / CrystalBridge / OS. Collision with the mythos terminal is documented, not silently resolved. |
| [0005](../docs/adr/ADR-0005.md) | AI Orchestrator — consolidate the naming; ship the concept as documentation first | Accepted | Recommend, then a human decides. No autonomous dispatch runtime. |
| [0006](../docs/adr/ADR-0006.md) | Licensing strategy — keep the dual license, record the IP principles, flag trademark as unfinished | Accepted — §1 superseded by ADR-0008 | IP principles in later sections still stand per the index/CHANGELOG. |
| [0007](../docs/adr/ADR-0007.md) | Correct the project name to "TerAustralis Incognita"; rename mythos/teraaustralis/ | Accepted | One *a*. Constitution §1 amended via §8. Historical ADRs 0001/0002 left unedited. |
| [0008](../docs/adr/ADR-0008.md) | Supersede ADR-0006 §1 — adopt CC BY-NC-ND 4.0 for code; reconcile the fallout | Accepted | Code license direction confirmed by the maintainer. |
| [0009](../docs/adr/ADR-0009.md) | Reconcile the licensing chaos — CC BY-NC-ND governs today; packages/ is an in-progress target | Accepted — target question resolved by ADR-0010 | Do not reopen the four-license model without a new ADR. |
| [0010](../docs/adr/ADR-0010.md) | Uniform CC BY-NC-ND 4.0 for the whole repository; differentiated per-package licensing not adopted | Accepted | Terminus of the 2026-07-23 license sequence. |
| [0011](../docs/adr/ADR-0011.md) | Adopt the three-project boundary model — umbrella, Crystal Core, Crystal Vision | Accepted | This git is the umbrella (no main app code). Decided-NOT: no renames, no moves, no new repos in that ADR. |
| [0012](../docs/adr/ADR-0012.md) | Site visual-token layer now; domain restructure deferred behind triggers | **Proposed** | Not law until merged. Palette unchanged; nested layouts / new routes deferred. |
| [0013](../docs/adr/ADR-0013.md) | Extend uniform CC BY-NC-ND 4.0 across the whole portfolio; retire Apache-2.0 and the unlicensed repositories | Accepted | Portfolio-wide, not only this umbrella. |
| [0014](../docs/adr/ADR-0014.md) | Grok Build takes the Repository Engineer seat; Claude retained as history | Accepted (PR #116) | This memory protocol does **not** undo this ADR. Claude returning later needs a new ADR. |
| [0015](../docs/adr/ADR-0015.md) | Stop growing the constellation — no new GitHub repository without an ADR | Accepted (PR #118) | Nineteen repos measured 2026-08-20. Agents do not create repositories. Sandbox is not a repository. |
| [0016](../docs/adr/ADR-0016.md) | Recognize samuelsalmon3/SourceCode as an external peer, not a CrystalCore module | **Proposed** | Neighbor recorded; engines not fused. Becomes Accepted on merge of its PR. |

## Seat and repo-count (load-bearing)

- **Grok Build** = Repository Engineer. **Creative Grok** = separate seat.
  A Grok App Builder sandbox is not a CrystalCore.OS product and is not
  the estate ([ADR-0014](../docs/adr/ADR-0014.md)).
- Next work lands in an existing living repo ([ADR-0015](../docs/adr/ADR-0015.md)
  landing table). Splitting `-Code` into core/vision still requires
  Migration-Plan Stage 3 criteria **and** ADR-0015.

## Not decided here

Starline taxonomy (three meanings) has **no ADR yet**. See
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md). Do not mint component names that
use **Songline**.

## Direct maintainer decisions recorded in memory (not ADRs)

These did not go through the ADR process
([`Decision-Records.md`](../docs/governance/Decision-Records.md)) — they
are recorded here because the maintainer gave them directly, in session,
as durable rulings for this memory protocol to carry. Say so plainly: a
decision recorded here is **current, dated, Crystal-authored** — never
represent it as a rediscovered older repository source, and never let it
imply an ADR exists when it doesn't.

**2026-09-05** — Roadmap #7 (Small Council) mechanism selection: **Option D, Prototype Demonstration.** · After confirming that the verification mechanisms previously assumed (Standards Australia, then ASA public consultation) do not exist or have closed, decision made to pursue a real engineering demonstration instead: co-develop a prototype component sourced end-to-end through the Iluka → ANSTO/AR3 → Liquid Instruments sourcing narrative (one-pager framing; not an existing partnership). This replaces the need for external verification with proof-of-concept working hardware. Phase 2 outreach begins with technical pitch to companies. Timeline shifts to 3–4 months for the full item. Record: [`specs/small-council-mechanism-options.md`](../specs/small-council-mechanism-options.md), [`memory/projects/90-Day-Roadmap/CURRENT.md`](projects/90-Day-Roadmap/CURRENT.md).

**2026-08-28** — CMX / Ovaro / Continuum external boundary · Recorded by
Crystal Arena-Turner directly, resolving the "no on-disk citation" gap
[`collaboration/EXTERNAL-RELATIONSHIPS.md`](collaboration/EXTERNAL-RELATIONSHIPS.md)
had flagged in PR #123 · **Authority: current explicit Crystal-authored
repository decision, not a rediscovered historical citation.**

> Ovaro is CMX's agency/shopfront relationship. Continuum is CMX's
> separate product. TerAustralis / SAT / CrystalCore remain Crystal's
> work. Collaboration or architectural similarity does not imply merger,
> ownership, licence, identity, or authority. Readability or access does
> not imply permission. Silence does not imply permission. The
> plain-language "authority ≠ capability" acknowledgement remains limited
> to its written scope and credit, and does **not** grant SAT internals,
> Operator Frame internals, DUR, token/revocation mechanics, lattice
> internals, or private specification material.

Memory note: [`collaboration/EXTERNAL-RELATIONSHIPS.md`](collaboration/EXTERNAL-RELATIONSHIPS.md)
now cites this entry as its repository authority for the Ovaro/Continuum/CMX
boundary specifically. It does **not** newly authorize anything about SAT,
Operator Frame, DUR, or lattice internals — those stay protected/out of
scope with no on-disk specification, per [`PRIVACY.md`](PRIVACY.md).
