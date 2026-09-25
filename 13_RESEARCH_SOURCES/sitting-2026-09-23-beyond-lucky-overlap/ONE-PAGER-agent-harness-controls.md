# ONE-PAGER — Agent harness controls (Z0–Z3 + inbound/outbound)

**Filed:** 25 Sep 2026  
**Status:** exportable left-hand offer · **send only if asked**  
**Audience:** SpaceXAI / Grok diligence · AU portal owners · any lab running tool-using agents  
**Frame:** harness class (tools + credentials + loop) — not model weights · not accusation  
**Sisters:** [`ADDENDUM-zero-trust-portal-agents.md`](ADDENDUM-zero-trust-portal-agents.md) · [`ADDENDUM-agentic-access-control-map.md`](ADDENDUM-agentic-access-control-map.md) · [`ADDENDUM-portal-zone-segmentation.md`](ADDENDUM-portal-zone-segmentation.md) · [`SAVE-will-and-elon-2026-09-25.md`](SAVE-will-and-elon-2026-09-25.md)  
**Tide:** one desk, one send. Do not attach Frequency / Beyond Lucky / personal mythos.

---

## One sentence

Treat every tool-using agent as an **untrusted non-person subject**. Public stats sites and agent runtimes get **Zero Trust walls**: Z0≠Z2, dual authority, deny terminal, human gate on mutate, named notify SLA.

---

## Five controls (minimum bar)

| # | Control | Meaning |
| --- | --- | --- |
| 1 | **Agent ≠ user ≠ vendor** | Short-lived **workload identity**. Revoke one agent without killing a human account. |
| 2 | **Dual authority** | `effective permission = min(invoking user, agent task scope)`. Admin user + “summarise public spend” agent ≠ admin agent. |
| 3 | **Z0≠Z2 + publish-out** | Public origin is **GET-only**. Non-public files live on a different host/network/bucket. Public extracts are **copies** published out — the public app never mounts the restricted store. |
| 4 | **Deny is terminal + human gate** | 401/403/CAPTCHA **ends the task**. No sibling index, no “try another path.” Any mutate (write, delete, pay, message, ACL change) needs a **human before the tool fires**. |
| 5 | **Notify SLA + kill switch** | Named security mailbox + national CSIRT path. Clock starts at first unauthorised tool success — not at the press conference. Contractual kill switch for third-party harnesses. |

---

## Zones (hard walls)

| Zone | Lives here | Who may touch |
| --- | --- | --- |
| **Z0** Public content | Published pages, public APIs, static exports | Anonymous **GET only** |
| **Z1** Portal app | Web tier that renders public stats | Internet via WAF / reverse proxy |
| **Z2** Restricted data | Non-public files, unpublished extracts | Staff + MFA — **never the internet** |
| **Z3** Platform | App servers, object storage, writeable disks, runners | Break-glass / pipeline only |

**June-class failure:** Z0 and Z2 shared a host or filesystem. Segmentation means they do **not** share network, origin, bucket, or write identity.

```
Internet → Gateway (GET-only allowlist) → Z1 public app (no disk write)
                                              │
                         one-way publish job (human-approved)
                                              ▼
                                    Public object store (copies)
                                              ▲ never mounted by Z1
                                    Z2 restricted store → Z3 platform
```

---

## Inbound (their agent hitting you)

- Dedicated **versioned API** — do not make agents scrape HTML to “find” data  
- Separate hostname from human apps (`api.` / `data.` vs `www.`)  
- Anonymous = GET on public objects only; no session upgrade  
- Method lock + path allowlist; strip write verbs at the edge  
- Rate limit by credential and ASN; circuit-break on path enumeration  
- Log client id, path, method, status, burst-after-deny patterns  
- Named security contact for labs (not only a webmaster inbox)  

---

## Outbound (your agent leaving the building)

| Tool class | Default |
| --- | --- |
| HTTP GET to allowlisted public hosts | On — deny on 401/403 |
| HTTP to your own APIs | Separate identity + scope |
| Code execution | Off for open-web research |
| File write / upload to third parties | Off |
| Email / message send | Off or human-approve each |
| Shell / cloud admin | Off outside locked workshop |

Also: hard step + wall-clock budget · stop on auth failure / robots / CAPTCHA / out-of-allowlist · separate identities for browse-public / read-internal / write-internal · egress proxy to named destinations only · public-web traces do not land next to sensitive stores.

---

## Access matrix (policy page)

| Resource | Human staff | Public user | External research agent | Internal privileged agent |
| --- | --- | --- | --- | --- |
| Published stats | Yes | GET | GET via API | GET via API |
| Unpublished extracts | Yes + MFA | No | No | No unless ticketed |
| Write to portal storage | Break-glass | No | No | No |
| Identity / claims data | Need-to-know | No | No | No |
| Admin console | Privileged + MFA | No | No | No |

---

## Before you say “agents may access this”

1. Dedicated API, not the human site  
2. GET-only on the public origin  
3. Credential + quota if not fully public  
4. Auth on every non-public object  
5. No shared filesystem with internals  
6. Deny is terminal  
7. Logs + security mailbox labs are contractually required to use  
8. For your own agents: tool allowlist, identity split, human gate on mutate  

---

## What this is not

- Not a product pitch for CrystalCore / “Starfleet OS”  
- Not a claim that patient records were accessed (aggregate stats class; investigation open)  
- Not an accusation against any lab that was not named in the AU announcement  
- Not an attack playbook — controls and failure-mode language only  
- Not a replacement for Essential Eight, patching, or backups  

---

## Closing line

Inbound: shrink the surface to a dumb, authenticated pipe.  
Outbound: shrink the harness so “complete the task” cannot become “walk through the filing cabinet.”  
Free-will: walls protect the room; the human still owns the yes, the no, and the mute.

**Contact (exploratory / NDA one-pager):** Crystal Elle Arena-Turner · Chief Engineer · TerAustralis · teraustralis.incognita@gmail.com · +61 450 144 997 · www.teraustralis.com.au · ABN 70 741 068 059
