# Documentation

The documentation tree of the CrystalCore OS repository architecture. Each
area answers one kind of question; nothing in here is executable code, and
nothing in here claims to be more built than it is (see
[`governance/The-Incognita-Rule.md`](governance/The-Incognita-Rule.md)).

| Area | Question it answers |
|------|---------------------|
| [`vision/`](vision/) | Why does this project exist, and where is it going? |
| [`architecture/`](architecture/) | How is the system designed — components, relationships, data flow? |
| [`governance/`](governance/) | How are decisions made — review rules, standards, the Constitution? |
| [`ai/`](ai/AI-Architecture.md) | Which AI tools contribute, and how do they fit together? |
| [`agents/`](agents/) | Operating instructions for each AI agent working in this repo |
| [`guides/`](guides/) | How do I do a specific task — commit, push, connect a guest AI? |
| [`adr/`](adr/) | Architecture Decision Records — why the big calls were made |
| [`reviews/`](reviews/) | Point-in-time architectural surveys — dated snapshots, not living docs |

Component-level specs that used to live beside the code are under
[`architecture/crystal-core/`](architecture/crystal-core/); the Lattice
design sketch is under [`architecture/lattice/`](architecture/lattice/).

## Canonical knowledge base

Seven cross-linked documents describe the architecture **exactly as it
exists** — verified implementation, designed decisions, and open questions
(reconstructed 2026-07-24 from this repo's ADRs, Migration-Plan, and git
history; every claim labeled Science ✅ / Vision 🔮 / Drift ⚠️ / Unknown):

| File | What it covers |
|------|----------------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Belt-Three model, three-project boundary, six-repository constellation |
| [`REPOSITORIES.md`](REPOSITORIES.md) | Six-repo inventory (3 living + 3 frozen) — roles, links, CI/CD state |
| [`GOVERNANCE.md`](GOVERNANCE.md) | ADR trail (0001–0011), locked names, the Incognita Rule, amendment process |
| [`TECHNICAL-FINDINGS.md`](TECHNICAL-FINDINGS.md) | 2026-07-23 audit findings, component state matrix, test coverage |
| [`IP-LICENSING.md`](IP-LICENSING.md) | License trail (CC BY-NC-ND 4.0), naming debts resolved & outstanding |
| [`OPEN-DECISIONS.md`](OPEN-DECISIONS.md) | Stage 3–4 decision gates, Tier 1–3 recommendations |
| [`TIMELINE.md`](TIMELINE.md) | Chronological narrative with provenance SHAs and branch names |

**Relationship to the Archive repo's knowledge base (added 2026-07-24).**
A second, independently-built set covering overlapping ground also
exists: `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`
(13 documents, a Statement/Evidence/Historical-Notes/Cross-References
template, built the same day from much of the same underlying
evidence — ADRs, Migration-Plan, git history). Both were produced by
independent, uncoordinated sessions, the same pattern this project has
hit before (the licensing chaos of ADR-0006→0010; the Crystal Runtime
episode). Per a fresh, independent git-archaeology pass across all six
repositories (`REPO-ARCHAEOLOGY-2026-07-24.md`, committed to the
Archive repo), no single repository is canonical for everything — but
for the specific role both these documents sets play, its verdict is
direct: *"System ledger / meta-record → `CrystalCore.OS-the-Crystal-
Architecture-Archive`... documents the other five; no unique
application content."* That is this repository's own prior decision
too (recorded in the Archive repo's own `knowledge-base/00-INDEX.md`).
**When the two sets disagree, the Archive repo's `knowledge-base/`
governs.** This `docs/` set is preserved as-is — not deleted, not
marked deprecated — as a parallel, independently-produced reference;
worth reconciling into the Archive's structure in a future pass rather
than maintaining two knowledge bases indefinitely. See the Archive
repo's `knowledge-base/11-CORRECTIONS.md` for the full account.

## Root-level reference documents

Nine standalone docs live directly under `docs/`, not inside one of the
areas above — not indexed here until this pass (flagged missing by the
2026-07-23 architecture survey, corrected 2026-07-24):

| File | What it covers |
|------|-----------------|
| [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) | Third-party sources and IP that informed CrystalCore OS's design |
| [`DBT_WAREHOUSE_INTEGRATION.md`](DBT_WAREHOUSE_INTEGRATION.md) | The emotion-detection dbt data warehouse pipeline |
| [`HUGGINGFACE_INTEGRATION.md`](HUGGINGFACE_INTEGRATION.md) | DistilBERT/GoEmotions fine-tuning integration |
| [`ADVANCED_UNCERTAINTY_METHODS.md`](ADVANCED_UNCERTAINTY_METHODS.md) | Uncertainty-quantification strategies for active learning |
| [`EMOTIONAL_INTELLIGENCE_BLUEPRINT.md`](EMOTIONAL_INTELLIGENCE_BLUEPRINT.md) | The emotional-intelligence / affective-computing design |
| [`RESTRUCTURING_COMPLETE.md`](RESTRUCTURING_COMPLETE.md) | Superseded — packages/-era restructuring summary; kept for provenance |
| [`FIRST_RELEASE.md`](FIRST_RELEASE.md) | Superseded — packages/-era PyPI release guide; kept for provenance |
| [`PUBLISHING.md`](PUBLISHING.md) | Superseded — packages/-era publishing workflow; kept for provenance |
| [`COMMERCIAL_LICENSING_GUIDE.md`](COMMERCIAL_LICENSING_GUIDE.md) | Superseded — per-package licensing tiers reverted by ADR-0010; kept for provenance |

Start points: new to the project → the root [`README.md`](../README.md);
contributing → [`CONTRIBUTING.md`](../CONTRIBUTING.md) and
[`governance/Review-Process.md`](governance/Review-Process.md); working as an
AI agent → the root [`AGENTS.md`](../AGENTS.md) and your file in
[`agents/`](agents/).
