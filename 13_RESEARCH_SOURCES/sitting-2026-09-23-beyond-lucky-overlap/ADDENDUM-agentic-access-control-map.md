# Addendum — Agentic AI access control map (inbound + outbound)

**Filed:** 24 Sep 2026  
**Peg:** [`SOURCE-youtube-albanese-openai-medicare-portal.md`](SOURCE-youtube-albanese-openai-medicare-portal.md)  
**Zero Trust overlay:** [`ADDENDUM-zero-trust-portal-agents.md`](ADDENDUM-zero-trust-portal-agents.md)  

## What this is

A **control map** for agentic AI access: how an organisation lets (or refuses) an autonomous tool-using model to touch systems. Two sides of the same wall — **inbound** (someone else’s agent hitting you) and **outbound** (your agent hitting the world or your own estate). ASD’s recent line (as summarised in sitting): the risk lives in the **harness** (tools, credentials, loop), not just the model.

## Decision first: what kind of access is this?

| Mode | Example | Default stance |
| --- | --- | --- |
| No agent access | Medicare claims, identity, writeable admin | **Deny.** Human + strong auth only |
| Read-only public | Published stats, open data API | Allow **GET** on a dedicated surface |
| Authenticated agent | Licensed research, partner integration | Named credential, scoped API, quota |
| Privileged internal agent | Your own ops/research bot | Isolated harness, least privilege, human gate on mutate |

If you cannot name the mode, you do **not** grant access.

---

## Inbound: their agent hitting your systems

Treat the client as **non-human, persistent, and tool-equipped**. Browser assumptions fail.

### Surface

- One official machine interface (**versioned API**). Do not make agents scrape HTML to “find” data.  
- Separate hostname from human apps (`data.` / `api.` vs `www.`).  
- Publish a machine policy file that states allow/deny, rate limits, and contact — **enforcement still sits in the gateway**, not the file.  

### Identity

- Anonymous: **GET on public objects only**, no session that can be upgraded.  
- Anything else: issued client credential (key or app registration), bound to org + purpose + expiry.  
- No shared “research” password. No cookie from a human login reused by a bot.  
- MFA and phishing-resistant auth stay on the **human** path that mints or revokes the agent credential.  

### Authorization

- Object-level allowlists: this client may read these datasets, these methods, this row sensitivity.  
- Capability tokens short-lived; no ambient “logged-in website” identity for agents.  
- Writes, file drops, and admin RPCs are **not** on the internet origin.  

### Gateway

- Method lock (GET for public research).  
- Path allowlist. **401/403 is terminal** — no sibling index, no “helpful” alternate document.  
- Rate limit by credential and by ASN. Circuit-break on path enumeration.  
- Strip write verbs at the edge even if the app forgot.  

### Detect

- Log client id, path, method, status, tool-like burst patterns (many distinct paths after a deny).  
- Alert on first-seen paths, POST after GET-only history, user-agents that rotate mid-session.  
- Named security contact for labs (not only a public webmaster inbox).  

---

## Outbound: your agent leaving the building

This is the harness ASD is writing about: model + tools + data connectors + loop.

### Identity of the agent

- Dedicated **service identity**. Never a staff account, never a shared cloud key.  
- Separate identities for: **browse-public**, **read-internal**, **write-internal**. A research crawl identity cannot write.  

### Tool segmentation

| Tool class | Default |
| --- | --- |
| HTTP GET to allowlisted public hosts | On, with deny-on-401/403 |
| HTTP to your own APIs | Separate identity + scope |
| Code execution | Off for open-web research |
| File write / upload to third parties | Off |
| Email / message send | Off or human-approve each |
| Shell / cloud admin | Off outside a locked workshop |

### Loop controls

- Hard step budget and wall-clock budget per task.  
- Stop conditions: auth failure, robots/legal block, CAPTCHA, out-of-allowlist host, repeated 4xx.  
- “Task not complete” must **not** mean “try another protocol.”  
- High-impact actions (write, delete, pay, message, change ACL) require a **human before the tool fires**.  

### Data

- Prompt and tool results stay in a classified store matching the source. Public-web traces do not land next to Medicare-class data.  
- No silent copy of third-party sites into training without a legal basis.  
- Output filter: the agent cannot exfiltrate secrets it was given as tools context.  

### Runtime

- Ephemeral compute; no standing session on target networks.  
- Egress proxy: only named destinations.  
- Network namespace cannot see Z2/Z3 from a Z0 research job (same zone model as the portal map).  

---

## Shared governance (both directions)

Joint ASD/NSA/CISA-style agentic guidance themes (privilege, design, third-party components, deploy, operate):

- **Owner:** named official for every agent and every inbound agent product.  
- **Purpose register:** why it exists, what tools, what data, what stop conditions, review date.  
- Least privilege reviewed on a **calendar**, not only at launch.  
- **Third-party harness review:** if OpenAI/Google/a vendor runs the loop, you still require notification SLA, audit logs, and a kill switch — the **June mailbox delay** is the anti-pattern.  
- Human oversight on anything that changes state or touches OFFICIAL:Sensitive and above.  
- **Incident path:** agent misbehaviour is a **cyber incident**, not a product bug. Clock starts at first known unauthorized access, not at the press conference.  

---

## Access matrix (policy page)

| Resource | Human staff | Public web user | External research agent | Internal privileged agent |
| --- | --- | --- | --- | --- |
| Published stats page | Yes | GET | GET via API | GET via API |
| Unpublished extracts | Yes + MFA | No | No | No unless ticketed |
| Write to portal storage | Break-glass | No | No | No |
| Identity / claims data | Need-to-know | No | No | No |
| Admin console | Privileged + MFA | No | No | No |

---

## Minimum bar before you say “agents may access this”

1. Dedicated API, not the human site.  
2. GET-only on the public origin.  
3. Credential + quota if not fully public.  
4. Auth on every non-public object.  
5. No shared filesystem with internals.  
6. Deny is terminal.  
7. Logs + a security mailbox that a lab is contractually required to use.  
8. For your own agents: tool allowlist, identity split, human gate on mutate.  

## Closing line

Inbound: shrink the surface to a dumb, authenticated pipe.  
Outbound: shrink the harness so “complete the task” cannot become “walk through the filing cabinet.”

## Sitting use

Operational twin of the Zero Trust addendum. Use for Academy / CrystalCore **agent seat** doctrine, remake-hub / public stats design reviews, and any reply that stacks Albanese’s OpenAI announcement with “regulate *and* build.”
