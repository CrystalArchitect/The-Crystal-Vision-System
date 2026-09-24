# Source — Adam Lyttle: NDIS provider PII still leaking (4 years after report)

**URL:** https://x.com/adamlyttleapps/status/2102958488658104365  
**Author:** [@adamlyttleapps](https://x.com/adamlyttleapps) (Adam Lyttle)  
**Posted:** 24 Sep 2026 · ~03:09 UTC  
**Checked:** 24 Sep 2026 (X API + page title)  
**Quotes:** [@AlboMP](https://x.com/AlboMP/status/2102891827536032037) (PM OpenAI / Medicare portal announce video)

## What he says (summary — no repro)

Australia has a massive cyber security problem. He found vulnerabilities on **NDIS service provider** websites that expose **PII** (patients, employees, suppliers — names, addresses, etc.). He reports notifying the provider (Feb / Mar / Jun **2022**), **ASD/ACSC**, and **cyber.gov.au**, following procedure. He checked again **today**: the leak path is **still live** (~**4 years** later). Publicly available to anyone. He has seen many cases; calls this the most egregious.

## Why it sits here

Same **day** as the OpenAI research-agent / Medicare **stats** portal announce and our national-security / protect-people desks. Different mechanism (misconfigured provider web app vs agent harness + weak Z0/Z2), same **failure class**:

| This post | Our sitting frame |
| --- | --- |
| PII on the open web for years | Protect people — systems & protocols, not vibes |
| Notify / ACSC path did not close the hole | Notify clock + enforce remediation, not mailbox theatre |
| Quotes Albo’s AI-agent announce | National security = walls that work on **all** gov-adjacent surfaces |
| Provider sites next to care data | Z0≠Z2 / publish-out / least agency — not only “AI agents” |

**Do not** file exploit steps, sample URLs that dump PII, or “how to look.” Cite the report as **evidence of posture failure**, not a tutorial.

## Metrics at check (API)

~31k impressions · ~403 likes · ~60 reposts · ~44 replies · quotes Albo video post.

## Sitting use

- Peg twin to [`SOURCE-youtube-albanese-openai-medicare-portal.md`](SOURCE-youtube-albanese-openai-medicare-portal.md): AI-agent fail **and** boring misconfig fail — both national-security class for people in the system.  
- Optional QT / reply desk: protect-people + free-will (consent to leave a broken surface) — **no** dunk that names live leak paths.  
- Aligns with [`POSITION-national-security-agent-portals.md`](POSITION-national-security-agent-portals.md) + [`POSITION-systems-protocols-protect-people.md`](POSITION-systems-protocols-protect-people.md).

## Confidence

High on what Lyttle **claims** publicly. Medium on the underlying vuln until ACSC / provider confirm — we treat as **reporter allegation + longevity claim**, not forensic proof.
