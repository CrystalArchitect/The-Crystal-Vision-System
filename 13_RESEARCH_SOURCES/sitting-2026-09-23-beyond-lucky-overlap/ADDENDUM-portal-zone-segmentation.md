# Addendum — Defensive segmentation for a public stats portal (Z0–Z3)

**Filed:** 24 Sep 2026  
**Controls only — no attack paths.**  
**Peg:** [`SOURCE-youtube-albanese-openai-medicare-portal.md`](SOURCE-youtube-albanese-openai-medicare-portal.md)  
**Sits with:** [`ADDENDUM-zero-trust-portal-agents.md`](ADDENDUM-zero-trust-portal-agents.md) · [`ADDENDUM-agentic-access-control-map.md`](ADDENDUM-agentic-access-control-map.md)  
**Frames:** ASD gateway guidance · Essential Eight · AGA deny-by-default · agentic AI harness advice (least privilege, human oversight on high-impact actions, logging)

## One line

Defensive map for a **public statistics portal** that must not be a stepping stone into government internals. Matches what the June incident exposed: a public site, **adjacent non-public files**, and a **write path**.

## Trust zones (hard walls)

Treat the portal as **four zones**. Nothing in a lower zone may reach a higher zone by URL luck.

| Zone | What lives here | Who may touch it |
| --- | --- | --- |
| **Z0 Public content** | Published stats pages, public APIs, static exports meant for the world | Anonymous **GET only** |
| **Z1 Portal app** | Web tier that renders public stats | Internet via WAF / reverse proxy |
| **Z2 Restricted data** | Non-public files, unpublished extracts, admin reports | Staff identity + MFA, **never the internet** |
| **Z3 Platform** | App servers, object storage, writeable disks, job runners | Break-glass / pipeline only |

The June failure is the classic one: **Z0 and Z2 shared a host or a filesystem**. Segmentation means they do **not** share a network, an origin, a bucket, or a write identity.

---

## Control map by layer

### 1. Identity and object authorization

- Every non-public object has its own authn/authz. A published dashboard is **not** a capability ticket for sibling paths.  
- No “security by unlisted URL.”  
- Public endpoints are **GET-only**. PUT/POST/PATCH/DELETE do not exist on the internet-facing origin.  
- Separate service accounts: a **read-only publisher** identity for Z0; a different identity for anything that can write. The web process that serves the internet **must not hold the write key**.  

### 2. Network and gateway

ASD treats gateways as **policy enforcement points**, not just pipes.

- Public origin in a DMZ / isolated app service. **No east-west** to Services Australia core.  
- Egress from Z1 only to **named backends** (the public dataset API). No SMB, no SSH, no metadata endpoints, no internal HTTP.  
- Internal files live on a **different hostname and different network** (e.g. `stats-internal.agency.gov.au` on a private link). Not `/internal/` on the same site.  
- WAF / reverse proxy: allowlist methods and paths; drop scanners and high-rate non-browser clients at the edge; do not rely on “looks like a browser.”  
- **Deny by default** between subnets. Essential Eight / AGA: traffic between systems only if required.  

### 3. Data plane

- Public extracts are built **outbound**: a job in Z2 publishes a **copy** into a locked public bucket. The public site **never mounts** the internal store.  
- Public bucket: versioning on, public-write off, object lock if available.  
- No shared disk, no shared CMS library, no “drafts” folder next to “published.”  
- If a file must exist before publication day, it stays in Z2 until a **human-approved promote** step copies it.  

### 4. Application

- Path and host binding: the public app cannot open arbitrary files from disk. Content comes from a **signed manifest** of published object IDs.  
- No upload, no “save report,” no debug write, no leftover admin UI on the public origin.  
- Separate **code deploy** from **data publish**.  
- Feature flags for anything experimental stay off on the internet-facing build.  

### 5. Agent-aware edge (new control set)

Agents are not browsers. Controls assume a stubborn client with tools.

- **403/401 is terminal** at the gateway. Do not return a different document, a sibling index, or a helpful “try this other path.”  
- `robots.txt` and `llms.txt` are hints only; enforcement is auth + method lock.  
- Distinct rate limits and bot scores for non-interactive clients.  
- If you must serve researchers, give them a **documented public API** with a key and a quota — so they stop wandering the HTML tree.  
- Never expose writeable error handlers or temp-file endpoints to the world.  

### 6. Detect and contain

- Log every request to Z1 with path, method, status, TLS fingerprint, user-agent, source ASN.  
- Alert on: method other than GET, 404 bursts across many paths, first-time paths, writes of any kind, spikes from a single ASN after a 403.  
- **Canaries:** fake internal-looking paths that only exist as tripwires. Hit = page security, not “serve the file.”  
- Immutable logs **off-box**. If something writes to an internal server, you need a trail the writer cannot edit.  

### 7. Recovery

- Essential Eight backups of Z2/Z3, tested restore. Public zone is disposable; rebuild from the publisher job.  
- Known-good public snapshot so you can freeze and republish if an agent dropped junk in a writable corner.  

---

## Agent-side segmentation (OpenAI / any lab)

ASD’s harness guidance is the other half: the danger is the software that wires the model to tools, not the weights.

| Control | Meaning |
| --- | --- |
| Tool allowlist | Research agents: HTTP GET to public web only |
| Domain allowlist | Government sites only via published APIs, not “the whole TLD” |
| No write tools | No local file drop onto third-party servers |
| Stop on deny | 401/403/CAPTCHA ends the task |
| Human gate | Any tool that mutates state needs approval |
| Separate identities | Research crawl ≠ production ChatGPT users |
| Notify owners fast | Security mailbox + named national CSIRT, not a generic public inbox three months later |

---

## Minimum viable split for a stats portal

```
Internet
   │
   ▼
Gateway / WAF          ← GET-only path allowlist
   │
   ▼
Z1 Public app          ← no disk write, no internal DNS
   │
   │  (one-way publish job, human-approved)
   ▼
Public object store    ← copies only
   ▲
   │  never mounted by Z1
Z2 Restricted store    ← staff MFA, private network
   │
Z3 Platform / identity
```

If those four boxes share a host, a bucket, or a service account, you do **not** have segmentation. You have a public front door on a filing cabinet.

## Closing

That is the control map. Optional next artefacts (not filed yet):

- One-page checklist for Services Australia–style portals  
- Same zones mapped onto Apple PCC vs third-party ChatGPT so the two “infiltration” stories stay distinct  

## Sitting use

Operational twin of the Zero Trust addendum: **draw the PEPs as zone walls**. Use with the agentic access matrix when reviewing any TerAustralis / CrystalCore public surface next to OFFICIAL or restricted stores.
