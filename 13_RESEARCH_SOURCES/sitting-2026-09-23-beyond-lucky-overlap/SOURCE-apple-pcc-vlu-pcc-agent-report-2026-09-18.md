# Source note — Apple Intelligence Report · PCC VLU / pcc-agent (architecture receipt)

**Filed:** 24 Sep 2026 (Crystal paste — reverse-engineering *writeup* of a transparency JSON)  
**Sibling (different report):** [`SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md`](SOURCE-apple-pcc-accessibility-reader-analytics-2026-09-24.md) — that one had **populated `modelRequests`** (Accessibility Reader).  
**This report:** `modelRequests: []` · all action in `privateCloudComputeRequests` · **Vision-Language Understanding (VLU)** via `pcc-agent`.  
**Hold:** JSON truncated at end · attestation crypto **not** fully decoded here · **no** agent-built attestation RE decoder / cert-chain cracker.

## Plain English

This is another **Apple Intelligence Report** — Apple’s audit receipt for Private Cloud Compute.  
Unlike the Reader extract (readable prompts + answers), this file’s **on-device model list is empty**. What you see is only the **cloud side**: which PCC agent pipeline ran, which nodes attested, which encrypted ML assets were named.

**Inference id:** `com.apple.fm.service.vlu.v1` → **Vision–Language Understanding** (image/scene understanding on PCC — Art / Book / Animal / Pet / Landmark asset names).  
**Pipeline:** `pcc-agent` (not the Accessibility Reader client from the other report).

## Time window (UTC)

| requestId (short) | ≈ UTC |
| --- | --- |
| A60B1F1A-… | 2026-09-18 02:01 |
| E6D4A12E-… | 2026-09-18 09:34 |
| A13C1EDB-… | 2026-09-18 20:13 (two entries) |
| 2734BA41-… | 2026-09-18 21:38 |
| 2371F78D-… | 2026-09-18 22:24–22:25 (four entries) |

**Span:** ~20 h 23 min on **18 Sep 2026**.  
Crystal’s paste notes **9 entries / 5 unique requestIds** (retries or proxy fan-out).

## Architecture (high-level — sitting)

| Piece | Meaning |
| --- | --- |
| Empty `modelRequests` | No on-device readable prompt/response block in *this* export |
| `privateCloudComputeRequests` | Cloud attestation + routing receipt |
| `pipelineKind: pcc-agent` | Agent service handling the job |
| `nodes` / `Validated` | Nodes that passed Apple attestation |
| `proxiedBy` | Client → proxy → worker path |
| `attestationBundle` | Protobuf + X.509 chain + secure-config metadata (rack/cell, policy) |
| `assets` | Named encrypted CipherML / safety assets for VLU |

**Visible secure-config themes (from paste):** `customer` vs `customerProxy` · rack / cell routing hints · `com.apple.privateCloudCompute.pccAgent` / worker · Apple Secure Boot / Data Center Attestation roots.

**Named assets (ids only):** PCC safety overrides · `encryptedVluArt` · `encryptedVluBook` · `encryptedVluAnimal` · `encryptedVluPet` · `encryptedVluLandmark`.

## Inferred flow (architecture only)

Device VLU ask → (optional proxy) → attested compute node(s) → load CipherML VLU assets → `vlu.v1` inference → execution log finalized → written into transparency report.

## Sitting relevance

| Lane | Fit |
| --- | --- |
| Zero Trust / PCC | Live shape of Apple’s attest → encrypt → stateless node story — neighbour to [`ADDENDUM-zero-trust-portal-agents.md`](ADDENDUM-zero-trust-portal-agents.md) |
| Two reports, two desks | **Reader** = text clean/summary with readable `modelRequests` · **This** = vision/agent PCC with empty `modelRequests` |
| Phone hygiene | Shows *which class* of AI ran (VLU) without dumping your photos into this sitting |
| What we will **not** do | Full protobuf RE · cert-chain verification tooling · attestation “complete decoder” PoC |

## Caveats (from Crystal’s analyst paste)

- Truncated JSON / incomplete last bundle  
- Protobuf field names inferred  
- Cert chains not verified in-sitting  
- Rack/cell strings are **location metadata Apple embeds for attestation**, not an invitation to map physical attacks  

## Confidence

High that this is a PCC **VLU / pcc-agent** transparency slice distinct from Accessibility Reader. Medium on exact user gesture that triggered VLU (Photos, Camera, Visual Look Up, etc. — not stated in paste).
