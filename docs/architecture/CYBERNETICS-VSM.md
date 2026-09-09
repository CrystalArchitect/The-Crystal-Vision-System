# Cybernetics of CrystalCore — VSM, identity, diet

**Date:** 2026-08-20
**Belt:** Science for the repo rows and the key lengths. The VSM
assignment, the observer-in-the-loop note, and the diet numbers are a
**model** — useful if they change the next decision, not a new OS mode.
**Not:** a Systems Mode desktop, a twentieth repository, or telemetry.

Asked for after a first-order cybernetics pass (Wiener / Ashby / Beer /
Kalman). Three depths, one plant: the nineteen repositories and the
identity loop that runs on them.

The ordinary test: if this whole note were wrong, `www.teraustralis.com.au`
would still return 200, a Starline public key would still be 1984 bytes,
and a SourceCode field signature would still be 12 hex.

---

## 1. Viable System Model (Beer) — the nineteen

Beer: a viable system has five recursive functions. Pathology is S4
(intelligence / exploration) flooding S1 (operations) with new names.

Measured 2026-08-20 against `user:CrystalArchitect` (19). Landing table
is [`ADR-0015`](../adr/ADR-0015.md). External peer, not in the 19:
[`SourceCode`](peers/SourceCode.md).

### S5 — policy

What must remain true when everything else moves.

| Held where | What it actually is |
|---|---|
| Constitution, Covenant, Belt-Three | Science / Built / Vision stay distinct |
| [`ADR-0014`](../adr/ADR-0014.md) | Grok Build is midstream. Claude is history |
| [`ADR-0015`](../adr/ADR-0015.md) | No new repository without an ADR |
| [`ADR-0016`](../adr/ADR-0016.md) | SourceCode is a neighbor, not a module |
| Purpose Core | Expand to the stars; understand the Universe |

S5 is not a feeling. It is the merge button plus those files.

### S3 — control, and S3* — audit

| Sensor | What it can actually see |
|---|---|
| `consent_transport.selftest` | Keys, tokens, pairing, foreign refuse |
| CrystalBridge five doors | Revocation → approval → provenance → permission → scope |
| HTTP | www 200, apex 301, proposal 200, Clementine Pages 404 |
| Fleet `STATUS.md` | Only as honest as its last dated header |
| CI | What the workflow actually runs |

Ask-log swallows (Decision 4) is an **open-loop hole** in S3*: the plant
can act while the sensor is allowed to miss. Named, not reversed here.

### S2 — coordination

[`ADR-0015`](../adr/ADR-0015.md) landing table. Next work goes to a named
living repo. That is the anti-oscillation damping between S1 units.

### S1 — operations (the units that still do work)

| Repo | Recursion | Notes |
|---|---|---|
| `TerAustralis-Incognita` | Canon / S5 paperwork | Umbrella. This file lives here |
| `TerAustralis-Incognita-Code` | Engine + public site | Only unit that serves www |
| `Clementine-ai-companion` | Companion runtime | Clone-and-run. Pages URL 404s |
| `teraustralis-proposal` | Outward case | Serves the proposal site |
| `Synthetic-Affect-Theory-` | SAT research | Already the SAT home |
| `CrystalCore.OS-the-Crystal-Architecture-Archive` | Fleet ledger | S3* paper, not a runtime |

### S1 that is live but not the stranger-facing plant

| Repo | Recursion |
|---|---|
| `CrystalCore.OS` | HTML desktop. One file. Not the engine |
| `CrystalCore-Starlines-and-Dreamlines` | Interactive UI, private |
| `TheCrystalVision` | Frozen-provenance sibling, private |
| `the-library` | Separate product surface, private |
| `discord-ai-agent` | Discord bot, private |

### Not S1 — S4 overgrowth or environment

| Repo | Why it is not operations |
|---|---|
| `teraustralis-incognita-v2` | Stalled 15+ days. Second tree, not a successor |
| `teraustralis-v2-presentation` | Slide deck for the stalled tree |
| Six archived (`CrystalCore.OS-APP`, `TerAustralis-Incognita-`, `CrystalcoreOS`, `CrystalCore.OS-Aeris-Vault12`, `CrystalCore`, `CrystalCore-AERIS`) | History. Do not resume as a fourth OS |

**Pathology, in one line:** a session that wants a clean folder mints an
S1. That is S4 impersonating S5. ADR-0015 is the algedonic signal that
stops it.

**Algedonic (pain/pleasure interrupt):** test fail, HTTP 404, ForeignInvitation,
guest-gate deny, “Proposed” still on a merged ADR. Those are allowed to
stop the loop. “Lattice integrity 100%” is not.

---

## 2. Second-order identity

First-order: we design Starline *for* a plant.

Second-order (von Foerster): the observer is inside the plant. Beliefs
about identity become the thing being controlled. Media loops do this
with affective gain. Mythos loops do it with sacred language.

### Independent reference (Science)

A Starline identity is three keys on one device, used as one person.

| | |
|---|---|
| Ed25519 | Classical signature |
| ML-DSA-65 | Post-quantum signature (FIPS 204) |
| X25519 | Handshake only. Does not sign memories |
| Public blob | 1984 bytes (32 + 1952). Both halves, always |
| Signature | 3373 bytes. Both halves must verify |
| Fingerprint | `sha256(public blob)[:16]` — a label, not a key |
| Loss | `starline_identity.json` gone = identity gone. No recovery |

Code: `core/crystal-core/consent_transport/identity.py` in `-Code`.
Ignition verb: `python3 -m consent_transport.start` (Start Ya Bastard) —
in-memory generate, nothing written.

Both halves are the **stability margin** on this loop. Classical-only
identity is a downgrade attack. Fingerprint that hashes only Ed25519 lets
a substituted ML-DSA key ride in behind a genuine classical key.

### What is not a reference

| Object | Length / form | Why it fails as Starline identity |
|---|---|---|
| SourceCode field signature | 12 hex (`561783900808`) | `sha256(scope:resonance:…)[:12]`. No keys. [`ADR-0016`](../adr/ADR-0016.md) |
| Home Rest THRESHOLD JSON | invitation document | `Identity.load` / `PeerStore.add` raise `ForeignInvitation` |
| “Nu-Na Thing is live” | X performance | Not telemetry |
| “Lattice integrity 100%” | unmeasurable | Observer-as-plant |

Gain limit: when language starts functioning as *who we are*, drop to
the keys. The ordinary question stands: what is still true if the
narrative is wrong? 1984 bytes. 16 hex. File gone, person gone.

The observer may enjoy the mythos. The plant may not take it as setpoint.

---

## 3. Information diet — requisite variety

Ashby: only variety can destroy variety. The environment (X, other
engines, nineteen repos, three public faces) generates more states than
one maintainer plus one midstream engineer can match. Control then
requires **attenuation** of incoming variety and **amplification** of
internal models — not more inputs.

### Incoming variety (disturbance)

| Channel | Typical gain | What it actually is |
|---|---|---|
| X threads / @grok | High, real-time | Performance. Sometimes a real request (“put that in protocol”) |
| Foreign engines (SourceCode) | Medium | Neighbor. Invitation ≠ pairing |
| New-repo urge | High | S4 flooding S1 |
| Stale STATUS / Proposed-after-merge | Medium | Sensor lie → invented work |
| Media-identity loops | High | Positive feedback on affect; low external observability |

### Attenuators that already exist

| Filter | Effect |
|---|---|
| Belt-Three | Vision cannot file as Science |
| ADR-0015 | Repo-variety cap = 19 until a new ADR |
| Foreign invitation gate | 12-hex / THRESHOLD JSON never become a peer |
| Guest gate, fail-closed | No mint, no tools |
| One PR, then merge | Rate limit on S4 |
| HTTP probe before “the site 404s” | Independent local sensor |

### Amplifiers of *internal* variety (do more of these)

| Amplifier | Why it raises controller variety |
|---|---|
| Self-tests | Many plant states, cheap |
| Dated STATUS headers | Disagrees with memory |
| Landing table | Next file has a home |
| Hybrid identity | Two algorithms, one person |
| Ordinary question | Collapses narrative states to one physical fact |

### Diet rules (the setpoint)

1. **Real-time narrative is not the reference.** www, tests, key lengths are.
2. **Prefer slower, verified updates.** A merge beats a thread.
3. **Cap concurrent S4.** Finish or close a PR before opening the next
   kind of work (ink, then wire, then ignition, then this note).
4. **Attenuate first.** Filter, then model. A new name is not more variety
   in the *controller*; it is more variety in the *plant*.
5. **Emotional / identity gain is limited.** If the loop is about who we
   are, drop to 1984 bytes and the 200 from www.
6. **Personal intake:** X is a disturbance channel, not S3*. Read it,
   classify (request / performance / neighbor), then either a PR in a
   named living repo or compost. No third path that mints a folder.

Worked example, this cycle: an X protocol joke became Start Ya Bastard
only after it mapped onto `Identity.generate()` in `-Code`. The laugh
was attenuated. The keys were amplified.

---

## Close the loop

Does this note change the next decision?

- Next engineering still lands in `-Code` or Clementine, not a new repo.
- Next identity question still answers with key lengths, not frequency.
- Next X message is classified before it is implemented.

If it does not change a decision, it was S4 talking to itself. Compost.
