# CrystalCore

Creative vision lattice and protocol pack: **Seven Sisters Songline**, water care rails, sky anchors, and local tools.

**🔭 Crystal universe — which repo is this?**  
This is **Crystal Core** — the protocol pack: Seven Sisters Songline, Starline Weaver (multi-AI), Decode→Ingest→Twin pipeline, specs.  
Corrected 2026-07-24 — six repos exist today, not the three implied
below originally: **TerAustralis-Incognita** (umbrella — governance,
ADRs, canon, mythos, no app code) · **TerAustralis-Incognita-Code**
(this repo, this file's actual home — the engine at `core/` and the
vision app at `vision/`; CrystalBridge lives here, at
`core/crystalcore/`, not in the umbrella as previously stated) ·
**CrystalCore.OS-the-Crystal-Architecture-Archive** (the fleet-wide
status ledger) · three frozen-provenance repos, none touched since
2026-07-17: **The-Crystal-Vision** (codex site + the companion's
ancestor), **crystal-vision** (this pack's interface-demo ancestor),
and **crystalcore** (this Songline pack itself — direct ancestor of
`core/crystal-core/`, the directory this README describes). Full map:
the umbrella's `docs/governance/Project-Boundaries.md`, "Repositories,
today."  
**License:** CC BY-NC-ND 4.0 — see `LICENSE` (portfolio-wide, per ADR-0013)

**Author:** Crystal Arena-Turner (@M13CrystalAT) · TerAustralis Incognita  
**Status:** Build in public  

## What this is

- Art / documentation / optional CLI around a seven-path Songline process  
- Public water literacy notes (Lake Eyre Basin, Great Artesian Basin, Murray–Darling)  
- A simple landing page (`index.html`)

## What this is not

- Not ownership of Aboriginal Seven Sisters Songlines or sacred law  
- Not physical control of rivers, aquifers, or weather  
- Not endorsed by Elon Musk, xAI, SpaceX, or any government  

## Truth labels

| Layer | Meaning |
|-------|---------|
| **Science** | Astronomy, hydrology, published geography |
| **Story** | Dreaming / Songline narratives (honour; no restricted detail) |
| **Vision** | CrystalCore art and protocol |

**Belt-Three:** Honour Country · Label layers · No coercion / no fake hydrology  

## Quick start

### Landing page

Open `index.html` in a browser.

### CLI (Windows PowerShell)

```powershell
cd cli
.\crystalcore.ps1 status
.\crystalcore.ps1 paths
.\crystalcore.ps1 transmit
.\crystalcore.ps1 open
```

## Clementine — Singularity Bridge

**Vision:** all minds, one weave. **Science (v0):** a working message bus where AI systems
(Claude, Grok, GPT, or built-in agents) talk to each other under Belt-Three law — every
message labeled, impersonation rejected, one red button stops everything.

```bash
# no API keys needed
python3 -m bus.run --agents echo,sisters --turns 4 --topic "first water"

# prove the law holds in code
python3 -m bus.selftest

# boot Clementine as a live service — agents join over HTTP from anywhere
python3 -m bus.server --port 8777 --topic "first water"
python3 -m bus.remote --agent sisters --server http://127.0.0.1:8777
```

See `../../docs/architecture/crystal-core/STARLINE-WEAVE-PROTOCOL.md` (the envelope + law) and `../../docs/architecture/crystal-core/CLEMENTINE.md`
(the hub persona). Live models join via env keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `XAI_API_KEY`.

## Crystal Core stack — Decode → Ingest → Twin

The runnable spine of the full-stack blueprint (`../../docs/architecture/crystal-core/BLUEPRINT-v0.3.md`, grounded map
in `../../docs/architecture/crystal-core/ARCHITECTURE.md`): events are validated (bad ones quarantined with reasons),
stored in a SQLite twin, and queryable as flows. Stdlib only.

```bash
python3 -m services.selftest                                        # prove it
python3 -m services.pipeline services/sample-events/budapest.jsonl  # run it
python3 -m services.api --port 8899                                 # serve it
```

Visual story: open `interface/index.html` — an interactive demo of the twin, pipeline,
mesh, and econ simulation (simulated data, labeled as such).

## Consent Transport — sovereign agent-to-agent communication

The technical realization of the mythic Starlines: two locally-running
companion agents exchange consented memory fragments directly, peer to peer, over a real Noise
Protocol handshake — no server between them, no data moved without explicit,
revocable consent. Spec: `../../docs/architecture/crystal-core/STARLINE.md`. Needs one dependency
(`pip install -r requirements-consenttransport.txt`) — the only non-stdlib code in this repo.

```bash
python3 -m consent_transport.selftest   # prove it — real TCP sockets, real handshake, 49/49
python3 -m consent_transport.run demo   # watch it: pair, deny, grant, exchange, revoke, deny
```

**The handshake is hybrid post-quantum by default.** X25519 falls to a large enough
quantum computer, and an adversary doesn't need one today to benefit later — they can
record a session now and decrypt it when the hardware exists. Memory fragments are
exactly the payload that stays sensitive for decades, so the handshake mixes a second,
independent secret from ML-KEM-768 (NIST FIPS 203) into the same chaining key:

    -> e, ekem, es, s, ss      ekem: an ephemeral ML-KEM-768 public key
    <- e, ee, se, kem          kem:  the encapsulation against it

Hybrid, never replacement — the session key needs *both* the X25519 DHs and the ML-KEM
secret, so an attacker has to break both. A flaw in ML-KEM leaves X25519 holding; a
quantum computer leaves ML-KEM holding. Costs 1184 bytes on the first message and 1088
on the second, and needs `cryptography>=47`.

**Identity is hybrid post-quantum too.** Every signature — fragments, consent receipts,
tokens, revocations — is Ed25519 ++ ML-DSA-65 (NIST FIPS 204), and verification requires
**both** halves. One good half and one bad half is a forgery, and an Ed25519-only
signature never verifies, so there is no downgrade to strip down to.

The fingerprint hashes the *whole* hybrid public key, and that part is load-bearing
rather than cosmetic. A quantum adversary can recover an Ed25519 private key from its
public key; if the fingerprint committed only to Ed25519, they could pair using the
victim's genuine Ed25519 key alongside their own ML-DSA key and every signature would
check out against what the peer stored. Hashing both closes that substitution.

**Known limitation, not fixed here:** the discovery beacon carries the signing key, so
it grew from ~330 bytes to ~4.2 KB and now exceeds a 1500-byte MTU. Loopback never shows
this; on a real LAN the datagram IP-fragments and discovery gets flaky. The fix is to
move the signing key out of the beacon and deliver it over TCP at pairing — a new
protocol frame, recorded as follow-up rather than half-done.

The two modes use different Noise protocol names, and the name is mixed into the
handshake hash, so a hybrid peer and a classical peer fail loudly rather than
negotiating down. There is no downgrade path by design.

## Receipts — tamper-evident records of what a companion said

**Vision:** the substrate of a "same someone" continuity metric. **Science (v0):** a
hash-chained SHA-256 receipt log over text artifacts, stdlib only. Two questions the
module refuses to conflate: `verify` is byte-exact (has this stored artifact changed? —
even a trailing-whitespace edit fails), `match` is canonical (does fresh text equal the
recorded return, ignoring line endings and blank-run noise?). Every receipt carries the
hash of the previous one, so history cannot be quietly rewritten; the exported `HEAD`
line is what to anchor with the umbrella's OpenTimestamps flow for witnessed time.

A receipt proves the bytes and their order — never that their content is true. Hashing
a claim does not make the claim so.

```bash
python3 -m receipts.selftest   # prove it — 15/15, including the whitespace attack
```

```python
from receipts import ReceiptStore
store = ReceiptStore("receipts-data")
r = store.capture(model_reply, label="continuity")
store.verify(r.filename)   # (ok, expected, actual) — byte-exact
store.match(fresh, r.filename)  # (ok, expected, actual) — canonical
store.head()               # the one line to anchor
```

## Paths (1–7)

1. **Spring** — first water; begin  
2. **Motion** — move; ship  
3. **Mark** — name true; atlas  
4. **Law** — consent; audit  
5. **Deep water** — GAB care  
6. **Sky bridge** — dust ↔ Pleiades (symbolic)  
7. **Ascent** — transmit; teach; rest  

## Main files

| File | Role |
|------|------|
| `index.html` | Landing page |
| `../../research/seven-sisters/WATER-BRIEF.md` | LEB / GAB / MDB fact sheet |
| `../../research/seven-sisters/FIRST-ACCELERATION-PLAN.md` | Weekly plan |
| `../../research/seven-sisters/crystalcore-seven-sisters-FULL.md` | Full path manual |
| `../../research/seven-sisters/crystalcore-seven-sisters-paths.md` | One-pagers |
| `../../research/seven-sisters/crystalcore-TRANSMIT-A.txt` | X post text (Option A) |
| `cli/crystalcore.ps1` | Mini CLI |
| `clementine/` | Singularity Bridge — multi-AI message bus + protocol |

## Licence / respect

Honour to Aboriginal custodians of the Seven Sisters.  
This repository is **homage and personal creative work**, not a claim on living law or Country.

---

*Red dust → starlines. Water with truth.*
