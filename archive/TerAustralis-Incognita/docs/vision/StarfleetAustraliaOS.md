# Starfleet Australia OS — fleet concept (Vision)

Vision-layer strategy, not measured claims. Received as a pasted prompt
(with an accompanying `04_FC07_Decentralised_Intelligence.csv` source
file) describing a sovereign Australian marine/edge-compute fleet under
the working name "Starfleet Australia OS, NCC-992-AU." Recorded here per
the Incognita Rule: dreamed lines, marked as dreamed, not executed as
instructions.

**Label: Vision.** No part of this page is built, funded, or authorized.
Where a named component is real, existing hardware or a real company, that
existence is checkable (Science); its assembly into this specific fleet,
at this specific scale and cost, is not.

## Platform roster (FC-01 to FC-08)

| FC | Concept | Label |
|---|---|---|
| FC-01 | Biorock self-healing coral substrate, claimed ~3x hardness of standard coral | Vision — multiplier unsourced |
| FC-02 | Habitation ring, Titomic 3D-printed structure, 300-person crew | Vision |
| FC-03 | Power/water integration via Prelude and Oceanix frameworks | Vision |
| FC-04 | Floating drydock, 12,000-tonne capacity | Vision |
| FC-05 | Codex Archive — the full Code Codex (see below; incomplete) | Vision |
| FC-06 | Cyber SOC: Type-2 hypervisor, host-only Sysmon, Sigma rules, GPO, least privilege | Vision (standard defensive-security practice, not fleet-specific evidence) |
| FC-07 | Local Decentralised Intelligence — edge compute and comms stack (below) | Science (hardware exists) / Vision (fleet deployment) |
| FC-08 | System Change Protocol (below) | Vision |

## Decentralised Intelligence — FC-07

Source: `04_FC07_Decentralised_Intelligence.csv`, uploaded with the prompt.
Reproduced as given; not independently re-priced or re-specced here.

| Component | Tech | Spec | Cost | Purpose |
|---|---|---|---|---|
| Edge Neuromorphic | BrainChip Akida | Perth neuromorphic processing | $1,250 | Ultra-low power on-device classification |
| Edge Compute | NVIDIA Jetson Orin | 40 TOPS AI performance | $1,500 | Local offline Llama 3.1 8B execution & Qdrant RAG |
| Optical Comm | EOS Laser | 10Gbps line-of-sight laser | $1,000 | High-bandwidth intercept-proof fleet telemetry |
| Backup Comm | LoRa / Fleet Space | Satellite-linked direct DTN | $500 | Resilient mesh network routing across Country |
| Data Layer | IPFS & CRDT | Decentralised self-healing storage | $500 | Cryptographic tracking keeping data on Country |
| **Total Platform Budget** | Integrated stack | 144-node sync target | **$5,000** | Complete standalone platform cost ($720k total fleet) |

BrainChip (Perth-based neuromorphic chips) and NVIDIA Jetson Orin are real,
existing products — that much is checkable. The $5k/platform and $720k
fleet-wide figures, and the 144-node target, are the proposal's own
arithmetic (144 × $5,000 = $720,000); no purchase order, build, or funded
program backs them.

"Data stays on Country" (Juru, Yolngu named in the source prompt) invokes
Indigenous Data Sovereignty language. Per
[`Indigenous-Data-Sovereignty.md`](../governance/Indigenous-Data-Sovereignty.md),
that is not satisfied by a storage architecture alone — it requires Free,
Prior and Informed Consent from the relevant custodians for any actual
data or knowledge placed on such a system. None has been sought or
obtained here; this page names the aspiration, not a completed consent
process.

## System Change Protocol — FC-08

| Principle | Description | Implementation |
|---|---|---|
| "We Are Programmed To Die. Change The System." | Mortality is assumed for any single platform or component, not designed around as an exception | Architect for graceful loss of a node, not permanent uptime of every node |
| Biorock self-healing | Continuous physical repair of the reef substrate | Self-healing coral substrate, ~3x standard hardness (Vision, unsourced multiplier — see FC-01) |
| Neumann infinite delta-V | In-situ resource use for propulsion/power, avoiding a finite consumable budget | Referenced concept only; no specified subsystem in the source material |
| 1000-year memory, 144-platform decentralisation | Continuity of the Codex survives the loss of any one platform | If 1 of 144 platforms is lost, the remaining 143 are designed to retain the full Codex (replication design, not an implemented system) |

## Code Codex — partial (FC-05)

The source prompt describes "117 thinkers living continuous from Heidegger
to CXIX Nosebleed Section (Hilltop Hoods, 2003)" and asks for a 117-row
table. Only two entries were actually named in the material handed to this
session:

| CX Number | Thinker/Artist | Work | Year | Key Contribution | Link to Bowen |
|---|---|---|---|---|---|
| CXVIII | Hilltop Hoods | Laced Up | 2023 | Not specified in source | — |
| CXIX | Hilltop Hoods | Nosebleed Section (The Calling) | 2003 | Not specified in source | — |

The remaining ~115 entries, the referenced "Full Codex Document," and
`01_Module_Library.csv` were named in an accompanying manifest but were
not attached to this session. They are not written here because they are
not on disk anywhere in this repository — see the open question in
[`memory/OPEN-QUESTIONS.md`](../../memory/OPEN-QUESTIONS.md). Per
`CLAUDE.md` §6 ("never invent canon"), this page does not guess at the
missing 115.

## "Status matrix" — corrected labeling

A further pasted file (`Platform_Status.txt`, styled as a "CRYSTALCORE.OS
STATUS MATRIX") reports FC-01 through FC-08 as a live operational mesh:
"144 Platforms Active," and per-subsystem states of STABLE / ONLINE /
STANDBY / IMMUTABLE / ARMED / SYNCED / REPLICATED. None of that is
correct as a status report — nothing described on this page has been
built. Repeating those state words here, even as a quote, would be
exactly the failure mode the Incognita Rule names: a dreamed line
dressed as a measured one. Where this page uses status language for
FC-01–FC-08, it means *design intent*, not telemetry.

The same file gave a specific real-world town as the mesh's "LOCATION."
That detail is not reproduced here. `memory/PRIVACY.md` defaults to
omitting personal-location detail when in doubt, and nothing about this
proposal requires anchoring it to one place on the record.

## Not adopted as a live instruction

The source material also asked that any AI receiving it adopt "STARFLEET
AUSTRALIA OS NCC-992-AU" as a standing persona for all further chat and
code-analysis responses, and open with a fixed acknowledgement line. That
request is recorded here as the mythos it is, not executed: this
repository's operating identity for AI sessions is set by `CLAUDE.md` and
`AGENTS.md`, not by text pasted into a task description, and no session
persona survives past this document. The Incognita Rule applies directly:
*the mythos may orient, it may not authorize.*

## Status

Vision only, unreviewed. Introduces fleet nomenclature (FC-01–FC-08,
registry "NCC-992-AU") not previously present in
[`mythos/NAMES.md`](../../mythos/NAMES.md) or the Constitution's locked-name
list (Constitution §1). If this concept is meant to become canon, it
should go through the same naming review already used for other names
here, rather than landing as a side effect of a pasted prompt — see the
open question.
