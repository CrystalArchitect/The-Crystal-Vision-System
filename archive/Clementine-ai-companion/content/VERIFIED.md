# Verified

*What this project enforces, checked by running it. Extracted 11 August 2026
from an internal working brief; the rest of that brief is deliberately not
here.*

`UNBUILT.md` records what is described but does not exist. This is its
complement: the claims that do hold, with the method that establishes them
and the date they were last run. Between the two there should be nowhere for
a claim to sit unexamined.

---

## Why this document is only half of something

It comes from a brief arguing a larger case about compute and sovereignty in
Australia. That brief separates its evidence into three kinds, and the
separation is the reason this file exists:

| | |
|---|---|
| **[V]** | *verified by execution.* Run on a machine, on a stated date, and the output read. Depends on nobody else's reporting. |
| **[S]** | *surveyed.* Corroborated across independent secondary sources and **not** primary-verified. |
| **[B]** | *bet.* Not evidence of anything. |

Only the **[V]** material is here. The surveyed half concerns grid capacity,
planning approvals and energy policy, and rests on sources that could not be
opened from the machine it was assembled on — so publishing it, in a
repository or anywhere else, would do the exact thing the brief warns
against. It stays in a working copy until somebody with unrestricted access
opens those sources.

The three markers were previously two, which put the strongest section under
the weaker label. Understating evidence is a smaller sin than overstating it,
and it is the same sin: the marker had stopped describing the thing it was
attached to.

---

## What is enforced

**[V]** Clementine is a working personal AI companion in which the control
boundary sits at the **runtime**, not at the policy or product layer. Every
line below was re-run on 11 August 2026 against `master` and the output read,
rather than carried forward from when it was first written.

- Model calls that would leave the machine are refused unless explicitly
  allowed; local calls proceed and are recorded. *(`allow_local` defaults
  true — the weaker and accurate statement, not the stricter and tidier one.)*
- Memory stays on the device. Embeddings are computed locally regardless of
  which model answers: configured against a vendor, the chat endpoint is the
  vendor's and the embedding endpoint is still `localhost:11434`.
- It fails closed, and fails at startup rather than at first use. Naming a
  remote provider without saying **where** it lives, or **which model** to ask
  for, is refused at construction. No vendor address and no model name is ever
  guessed on the human's behalf.
- Some material is refused to every model, local ones included, with no prompt
  offered — the person at the keyboard has no standing to consent on a
  custodian's behalf.
- Every call, allowed or refused, is written to an append-only, hash-chained
  log: a plain file on the person's own disk, openable in any text editor, and
  the verification is itself a script they can run.
- Neither a name nor pronouns are assigned. Either the human or the companion
  may choose, and the record says which of them did.
- **229 tests**, a number of them written by breaking the implementation first
  to confirm they would catch it.

---

## Which layer these claims describe

They are properties of the **runtime** — enforced in the process on the
machine, and true of every way of reaching it.

That distinction used to be load-bearing. The graphical interface reached
four of the runtime's fourteen capabilities: seeing stored memories, deleting
one, exporting them, restoring, and reading the consent record were available
over the local API and from a terminal, and not from the window a person
opens. An enforced property only a developer can exercise is still enforced,
and still more than a policy commitment — but it is not a finished product,
and saying so cost nothing an accurate argument needed.

**[V]** As of 11 August 2026 that gap is closed but for two conveniences:
**twelve of fourteen** are reachable from the window. Seeing what is held, deleting a memory,
leaving with everything, coming back from a file, reading the whole record,
and settling a name and pronouns are all things a person who never opens a
terminal can do.

The two that remain — `teach` and `reflect` — are conveniences already
reachable by talking to the companion, which is what the window is for.

That ratio is produced by `tests/test_reachability.py` rather than counted by
hand, because counting it by hand got it wrong twice: once low, and once high
when a substring match let one wired-up endpoint mark two others as reached.
A figure that lives in a document and is produced by an ad-hoc search drifts
by exactly that much.

---

## Not claimed here

This section is adapted rather than transplanted. The original names a
minerals-and-compute linkage that only makes sense beside the surveyed half,
and it stays there. What follows is what *this* document does not claim.

- **Nothing about grid capacity, planning, or energy policy.** That is the
  surveyed half, and it is not here precisely because it is not verified.
- **Not that the interface is finished.** Two capabilities have no interface,
  though both are reachable by talking. Deleting a companion now has one, and
  deliberately keeps nothing: a copy of somebody asked to be destroyed would
  be a betrayal dressed as a safety feature, so the backup is offered before
  the fact and never taken after.
- **Not that the audit log proves completeness, though it now proves more of
  it.** The hash chain catches an entry altered after writing, an entry cut
  from the middle, and reordering. It cannot catch entries removed from the
  *end*, because a truncated chain verifies perfectly and nothing inside a
  file can prove what is missing from the end of it.

  **[V]** Every export now carries a fingerprint of the record as it stood —
  the number of calls and the last one's hash, not the calls themselves — so
  a backup can later be asked whether the record still agrees with it. That
  closes the hole **as far back as the last backup and no further**. Calls
  made since are outside what any backup saw, so removing exactly those
  leaves no trace. Backing up more often shortens the unwitnessed gap; it
  never closes it. `tests/test_audit_witness.py` pins both the detection and
  the limit, so the limit cannot be quietly overstated later.

  This is deliberately not the usual fix. The usual fix is an anchor outside
  the machine, and publishing the head anywhere is a network call the human
  did not choose, leaking that they use this, how often, and when — the exact
  thing the gate exists to refuse. An anchor stored locally would be no
  better: whoever can truncate the log runs with the same privileges and can
  edit a sidecar file too. So the anchor is the person's own backup, which
  never leaves the machine and is held by them rather than by anybody else.
- **Not that any of this generalises.** That it scales from a personal
  companion to institutional infrastructure is a bet, and bets are not in this
  file.

---

## Keeping it true

Every claim above is checked by something that runs, so this page fails loudly
rather than ageing quietly:

| Claim | Held by |
|---|---|
| the gate, and protected material | `verify_consent.py` — 25 checks |
| refusals at construction | `tests/test_default_model.py` |
| either party may choose a name or pronouns | `tests/test_pronouns.py`, `tests/test_identity_surface.py` |
| memory handles keep meaning one memory | `tests/test_memory_identity.py` |
| what the audit chain does and does not catch | `tests/test_audit_visibility.py` |
| what a backup can and cannot witness | `tests/test_audit_witness.py` |
| deleting a companion keeps nothing | `tests/test_companions.py` |
| a damaged backup cannot empty a companion | `tests/test_import_safety.py` |
| the reachability ratio | `tests/test_reachability.py` |

If a number here disagrees with the suite, the suite is right and this page
is stale.
