# Host Trust — Design Spec

Status: **wired for `consent_transport` persist, CrystalBridge grants,
companion `memory.json` (atomic replace), audit/ask/revocation append,
StarlineAgent home mkdir, and PeerStore atomic replace.** Fragments
stay RAM. Job-scoped temp only on GitHub-hosted shared jobs. 2026-08-25.

This document adds a missing trust boundary: **where code is running**.
ConsentGate already fail-closes on *who* is asking and *what* they may
touch. It did not classify the *host*. Shared vendor pools are therefore
invisible to the architecture, which is the hole this spec names.

It does **not** unshare a pooled sandbox. It does not replace a vendor
allocator. It does not mint a seventh OS. A classifier that cannot empty
the pool still refuses to treat the pool as Layer 0.

## Why this was written

The steward named a class of problem: execution on a **shared cloud
sandbox** (the vendor pool they call HADES — SpaceX/xAI shared
sandboxes). Capacity, tenancy, and session refusal on that pool are the
vendor's. CrystalCore cannot move that machine.

What the framework *can* do is stop pretending that pool is a sovereign
computer. Peers are already untrusted until grant
(`consent_transport`). Hosts were not. This spec puts hosts in the same
fail-closed family as provenance: **unverifiable or shared origin
refuses steward persist.**

HADES is a **steward name for a SHARED pool**. It is not a `HostClass`
value, not a module, and not a southern berth.

## Classes

| Class | Meaning | Steward persist |
|---|---|---|
| `local` | Machine the steward controls | allowed |
| `delegated` | Named runner the steward controls (e.g. self-hosted Actions) | allowed |
| `shared` | Vendor multi-tenant pool (GitHub-hosted CI, HADES-class sandboxes) | **refuse** |
| `unknown` | Origin not established | **refuse** |

Default with no signal is `unknown`, not `local`. Same law as
provenance: absence of evidence is not home.

## What refuses on `shared` / `unknown`

Durable steward material:

- identity mint
- consent-save
- token-mint
- fragment-persist
- private memory write
- peer-save
- audit-append

**Exception — job-scoped scratch only.** Writes under
`tempfile.gettempdir()` (or `$TMPDIR` / `$TEMP`) are allowed **only**
when the host is `shared` **and** `GITHUB_ACTIONS=true`. GitHub-hosted
VMs die with the job. That is not a home.

`unknown` refuses even `/tmp`. Persistent vendor pools (HADES-class)
often mount `/tmp` on the same disk as the workspace. A path named tmp
is not a different lifetime there.

**Hatch.** `CRYSTAL_HOST_ALLOW_EPHEMERAL=1` allows any path. It is an
explicit override, not a default, and it does not reclassify the host.

Public, reproducible, non-secret work may still run on `shared` (site
build, Lighthouse against a local build artifact, syntax, this
classifier's own tests). That does not make the host trusted.

## Classifier (implemented)

`core/crystal-core/host_trust/`

- Steward override: `CRYSTAL_HOST_CLASS=local|delegated|shared|unknown`
- If unset and `GITHUB_ACTIONS=true`:
  - `RUNNER_ENVIRONMENT=self-hosted` → `delegated`
  - otherwise → `shared`
- Else → `unknown`
- A value of `hades` / `HADES` is **not** a class; it classifies
  `unknown` (fail-closed), so a vendor nickname cannot mint a home.

Prove: `cd core/crystal-core && python3 -m host_trust.selftest`

## Wired (2026-08-25)

`require_steward_persist(operation, path)` is the choke. On
`shared` / `unknown` it raises `PermissionError` unless:

- the host is `shared` and `GITHUB_ACTIONS=true` and the path is under
  the process temp dir (job-scoped scratch), or
- the hatch is set.

Called from:

- `consent_transport.identity.Identity.save` — `identity-mint`
- `consent_transport.consent._write_json_atomic` — `consent-save`
  (covers `ConsentEngine.save` and `TokenStore.save`)
- `consent_transport.peers.PeerStore.save` — `peer-save`
  (`starline_peers.json`; fsync + `os.replace`, 0600. A crash mid-write
  no longer destroys the address book.)
- `crystalcore.config.write_json_atomic` — `token-mint`
  (covers `--mint-token` / grants file)
- `crystalcore.mind.companion.CrystalCore.save` — `memory-private-write`
  (`memory.json` then `config.json`; fsync + `os.replace`, 0600. A crash
  mid-write no longer destroys the previous store.)
- `crystalcore.audit._append_private` — `audit-append` (guest pending +
  audit jsonl). Guest gate already treats `OSError` as ask-record refuse.
- `crystalcore.revocation.append_revocation` — `audit-append`
- `consent_transport.asklog._append_private` — `audit-append`. Peer
  knock log still proceeds on `OSError` (including this refuse):
  telemetry, not consent.
- `consent_transport.agent.StarlineAgent.__init__` — `identity-mint`
  on `starline_identity.json` **before** `state_dir.mkdir`. An empty
  directory on a pooled box is still a home.

`add_local_fragment` does not call the choke and does not write. Fragments
are RAM. There is no `starline_fragments.json`. Durable backing, if any,
is companion `memory.json` (`memory-private-write`).

GitHub-hosted CI stays green because those suites write under the
process temp dir **and** set `GITHUB_ACTIONS`. A durable path
(`/usr/...`, cwd, `$HOME`) on a pooled box is the thing that must fail.
An `unknown` host (this class of vendor sandbox, a desk that has not
declared itself) refuses `/tmp` too.

This is not a sixth ConsentGate door. Provenance is still *who*. Host
trust is *where*. The five guest doors do not move.

## Still open

- `fragment-persist` stays named in `STEWARD_PERSIST`. There is still no
  writer. RAM is pinned: `add_local_fragment` creates no disk file. Do
  not invent `starline_fragments.json` so the name has a body.
- A self-hosted runner is a **path**, not a plug. Default CI stays
  GitHub-hosted. See [`docs/deployment/STEWARD-RUNNER.md`](deployment/STEWARD-RUNNER.md).

Do not detect a vendor hostname as a `HostClass`. That couples the
framework to one allocator. Unknown already refuses.

## Mapping

- ConsentGate provenance = *who*. Host trust = *where*.
- Southern Cross architecture Layer 0 (Ground) = `local` / `delegated`
  only. SHARED is not Ground.
- Layer 2 (`consent_transport`) stays the wire. Do not rename it HADES
  and do not stand up a second protocol.
- Vision/mythos (Atlas, Starlines geometry) must not claim this
  classifier as a celestial lock.
- Songline stays outside the system. Public `/starline` copy uses
  Starline.

## Explicitly does not contain

- A boot sequence that “replaces HADES”
- A claim that this Grok/chat session is local
- A claim that the vendor pool is now unshared
- Songline mapping
- H2, materials, or proposal-berth changes
- A switch of default CI onto a box the maintainer does not have
