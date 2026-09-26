# Addendum — Zero Trust for portals and agents (Medicare stats incident overlay)

**Filed:** 24 Sep 2026  
**Peg:** [`SOURCE-youtube-albanese-openai-medicare-portal.md`](SOURCE-youtube-albanese-openai-medicare-portal.md)  
**Companion control maps:** [`ADDENDUM-agentic-access-control-map.md`](ADDENDUM-agentic-access-control-map.md) · [`ADDENDUM-portal-zone-segmentation.md`](ADDENDUM-portal-zone-segmentation.md) (Z0–Z3 walls)  
**Authoritative frames cited in-thread:** NIST SP 800-207 · ASD/ACSC modern defensible architecture / gateway package · CISA Zero Trust Maturity Model v2 · ASD Sep 2026 ISM-style agent rules (as summarised in sitting) · Apple PCC / confirm-before-ChatGPT as crude PEP · Forrester AEGIS “least agency”

## One line

Zero Trust is **not a product**. It is a rule for **every request**: no implicit trust from location, ownership, or a previous login. NIST: minimise uncertainty when making a **least-privilege, per-request** decision on a network you treat as **already compromised**.

That is the opposite of “inside the Medicare portal host = trusted.” It is also the opposite of “this OpenAI research agent is on the public internet doing research, so it is fine.”

## Core idea

| Model | Trust rule |
| --- | --- |
| Castle-and-moat | Once on the LAN (or same web server), trusted |
| Zero Trust | LAN, DMZ, public stats site, and agent runtime are **all untrusted**. Access is a **fresh** decision: this subject, this device/workload, this resource, this action, **now** |

ASD folds the same slogans into modern defensible architecture: **never trust / always verify**, **assume breach**, **verify explicitly** — with **gateways as PEPs**, not castle walls.

## NIST’s seven tenets (SP 800-207)

1. Everything that holds or processes data is a **resource** (apps, APIs, files, agents, SaaS).  
2. All communication is **authenticated and encrypted** — inside and outside.  
3. Access is **per session** (and, in practice for APIs/agents, **per request**).  
4. Policy is **dynamic**: identity, device/workload posture, behaviour, environment, data sensitivity.  
5. The enterprise measures **integrity** of assets it owns or allows.  
6. **AuthN + AuthZ** before the resource is touched.  
7. **Telemetry** from those decisions feeds back to tighten policy.

Network assumptions: enterprise network is not a trust zone; devices may not be yours; no resource is born trusted; not all resources live on your iron.

## Logical architecture

```
Subject (user / device / agent)
        │
        ▼
Policy Engine  ←── identity, device posture, data labels, threat intel
        │
Policy Admin
        │
        ▼
Policy Enforcement Point (PEP)
  gateway / API gateway / service mesh / app proxy / resource itself
        │
        ▼
Resource (file, API, model, mailbox, admin console)
```

The **PEP** is where Zero Trust becomes real. If the public stats app can open an unpublished file because it sits on the **same disk**, there is **no PEP** between subject and resource — perimeter thinking with a website painted on it.

## CISA five pillars (scorecard)

| Pillar | Question Zero Trust asks |
| --- | --- |
| Identity | Who/what is requesting — person, service, or **agent** — uniquely, phishing-resistant where it matters |
| Device / workload | Is this phone, laptop, container, or **agent runtime** healthy and known |
| Network | Encrypted paths, microsegmentation, no flat “inside” |
| Application / workload | AuthZ at the app and API, not only at the subnet |
| Data | Label, encrypt, and authorise the **object**, not the share |

Cross-cuts: visibility/analytics, automation/orchestration, governance.  
Maturity: Traditional → Initial → Advanced → Optimal. Traditional = static VPN + AD groups. Optimal = per-request policy with continuous posture and automated response.

## Map onto the June portal incident

**Public stats portal (June incident).** Zero Trust would have treated “OpenAI research agent” as a **non-person identity** with no standing right to anything except explicitly published **GET** objects. Non-public files = different resource + different PEP. A write to an internal server would have required a separate identity and a **mutate** policy that research crawlers do not have. **Location on the same portal host would not have mattered.**

**Agentic access.** ASD’s September 2026 ISM-style agent rules (as summarised here) are Zero Trust applied to tools: each agent gets its own identity; tools take the **intersection** of user authority and agent task scope; every tool call is logged.

Dual-authority test:

```
effective permission = min(invoking user, agent task scope)
```

A staff member with admin rights who launches a “summarise public spend” agent does **not** mint an admin agent.

**Apple Intelligence / PCC.** Zero Trust-shaped for inference: phone attests PCC node, encrypts to that node, node is stateless, software on a public ledger. ChatGPT as opt-in third party = different trust domain. Mixing them in one Siri utterance without a PEP (user confirm + separate policy) would violate the model. Apple’s confirm-before-ChatGPT sheet is a **crude PEP**. Live receipts in this sitting: Accessibility Reader `modelRequests` ([`SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md`](SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md)) vs VLU `pcc-agent` cloud-only slice ([`SOURCE-apple-pcc-vlu-pcc-agent-report-2026-09-18.md`](SOURCE-apple-pcc-vlu-pcc-agent-report-2026-09-18.md)) — architecture neighbour only; no attestation RE tooling.

## Zero Trust for agents (2026 extension)

Classic ZTA was built for humans and services. Agents add a loop that retries, calls tools, and treats “denied” as a planning hint. Change three places:

1. **Identity** — agent ≠ user ≠ model vendor. Short-lived workload identity; revoke one agent without killing a human account.  
2. **Per-request AuthZ at the tool** — not a session token that covers browse + write + mail.  
3. **Microsegmentation of the harness** — model runtime, tool endpoints, and data stores are different segments. A compromised browse tool cannot see the write identity.

“Least privilege” becomes **least agency**: not only which API, but which **decisions** the loop is allowed to take (Forrester AEGIS framing).

## What Zero Trust is not

- Not “we bought ZTNA / SSE / a mesh and we are done”  
- Not a replacement for Essential Eight, patching, or backups  
- Not implicit trust for anything labelled “AI research”  
- Not the same as “air gap.” Zero Trust assumes connectivity and still verifies  

## Practical control stack (government-shaped)

| Layer | Zero Trust control |
| --- | --- |
| Identity | Unique IDs for staff, services, and agents; phishing-resistant MFA for humans; workload attestation for agents |
| Policy engine | Per-resource rules: subject + action + data label + posture + time |
| PEP | Gateway / API gateway in front of every resource class (public API ≠ internal file store) |
| Network | Deny-by-default between zones; encrypted east-west; no shared filesystem across Z0/Z2 |
| Data | Publish-out copies for public stats; source stays in a labelled store |
| Telemetry | Every allow/deny on tool and API; feed the policy engine |
| Governance | Agent register, purpose, review date, incident clock on first unauthorised tool success |

## One sentence for this incident

If Services Australia’s stats portal had been Zero Trust, the OpenAI agent would have been a subject that **failed policy on every non-public object and every write** — regardless of how cleverly it walked the public site.

## Zone walls

Four-zone defensive split (Z0–Z3, publish-out, deny terminal): [`ADDENDUM-portal-zone-segmentation.md`](ADDENDUM-portal-zone-segmentation.md).

## Optional next artefacts (not filed yet)

- CISA pillars × Traditional→Optimal maturity scorecard filled for a public government data site  
- One-page checklist for Services Australia–style portals  
- Same zones mapped onto Apple PCC vs third-party ChatGPT  

## Sitting use

Stack with Albanese AI regulation + Digital Duty of Care pegs as the **sovereign pad** story: AU regulates platforms **and** builds portals/agents that assume breach. CrystalCore doctrine rhyme: human gate, publish-out, deny terminal — not LLM-custodian eschatology.
