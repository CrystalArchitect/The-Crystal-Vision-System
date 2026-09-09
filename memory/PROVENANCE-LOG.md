# PROVENANCE-LOG — general-claim evidence cards (Provenance Stack)

**Label:** Vision / methodology log. Not implemented as code. Each card
below is a worked example, not a claim that this repo has settled the
underlying science.

**Origin:** [`ETYMOLOGY-STACK.md`](ETYMOLOGY-STACK.md) is scoped to
word-origin claims specifically. [Starline Arsenal 32, Provenance
Stack](../.claude/skills/starline-arsenal/models/32-provenance-stack.md)
generalizes the same evidence-tier method to *any* claim where source
quality, not logical structure, is the actual question — health claims,
scientific-sounding marketing, viral "fact" threads, and so on. This file
is where that general-purpose use lands, distinct from the
etymology-specific file. A claim about *words* goes in
`ETYMOLOGY-STACK.md`; a claim about anything else that still needs
tiering goes here.

## Tier system

Same scale as `ETYMOLOGY-STACK.md`, generalized beyond linguistic sources:

| Tier | Evidence | Use |
|---|---|---|
| **A+ Attested** | Independently replicated, peer-reviewed, direct measurement | Settled within stated scope |
| **A Established** | Peer-reviewed, mainstream scientific consensus | Reliable general claim |
| **A− Published, contested** | Peer-reviewed but not independently replicated, or interpretation disputed | Real observation, unsettled meaning |
| **B+ Textbook** | Standard reference works, established physiology/chemistry | Reliable within its actual scope |
| **B Credentialed, non-peer-reviewed** | A named expert's claim outside formal peer review | Lead, verify the specific claim |
| **C Marketing synthesis** | Vendor or wellness-industry framing built on top of a real finding | The underlying finding may be real; the framing usually overstates it |
| **D Rejected** | Contradicted by domain experts, mechanism doesn't hold | Should not be repeated as fact |
| **V Vision** | Symbolic, interpretive, or aspirational claim | Not a factual claim at all — meaningful only as framing |

## Worked evidence card — "structured / EZ water" (2026-08-30)

**Claim as presented:** "The majority of water inside the human body is
arranged in a gel-like, liquid crystalline structure rather than as
free-flowing liquid water," citing Dr. Gerald Pollack's "Exclusion Zone
(EZ) water" / "fourth phase of water," a proposed H₃O₂ structure with a
negative charge that "drives electrical currents" and enables rapid
signaling through collagen/fascia networks — with plain drinking water
framed as passing through the body unless bound by minerals and amino
acids.

| Sub-claim | Tier | Finding |
|---|---|---|
| An exclusion zone (solute-free region) forms in water next to certain hydrophilic surfaces | A−/B+ | Published by Pollack's lab; a real, reported experimental effect, but not independently replicated and its interpretation is disputed |
| EZ water is a distinct structural phase with formula H₃O₂ and negative charge | **D — rejected** | Never published in a peer-reviewed structural chemistry venue; chemists state the formula cannot hold as a stable form — "cannot be anything but H₂O" |
| "The majority" of water in the human body is arranged this way | **D — unsupported extrapolation** | Goes well beyond Pollack's own in-vitro, near-surface experiments, which say nothing about bulk body-water proportions |
| Real, separate science: bound/hydration-shell water ordered near proteins and membranes | A | A legitimate, distinct biophysics topic — not the same claim as EZ water, and does not support "majority of body water is gel-like" |
| EZ/structured water "drives electrical currents" and enables rapid signaling via fascia/collagen | **D — speculative** | No demonstrated mechanism in living tissue; this is the layer most often added when the claim moves from lab papers into wellness marketing |
| Plain water "passes rapidly through" without minerals/salts/amino acids | **C — marketing synthesis over a real fact** | Electrolytes genuinely matter for hydration (true physiology); the framing that plain water is functionally useless is standard structured-water-product marketing, not a finding from Pollack's research |

**Confidence-vs-tier mismatch:** every sub-claim above is delivered in
identical declarative language regardless of tier — a real, disputed lab
observation (A−), a rejected chemical structure (D), and pure marketing
framing (C) all read as equally established. That flattening is the
actual thing to flag, independent of any single sentence turning out true.

**Missing-evidence list:** independent replication of the EZ effect
outside Pollack's own lab; any peer-reviewed structural chemistry paper
proposing H₃O₂; any in-vivo human or animal study measuring "majority of
body water" as gel-phase; any measured signaling mechanism through
fascia attributable to water structure specifically.

**Vision/Fact boundary:** the wellness-industry version of "structured
water" is Vision/marketing framing wearing the vocabulary of a real,
narrow, disputed lab finding. Treat "EZ water exists as an experimental
phenomenon" and "structured water improves your hydration/health" as two
entirely different claims with two entirely different evidence tiers —
the first is A−, the second is D.

Sources checked: [The Conversation — chemist explainer](https://theconversation.com/dont-fall-for-the-snake-oil-claims-of-structured-water-a-chemist-explains-why-its-nonsense-188159), [Skeptical Inquirer](https://skepticalinquirer.org/exclusive/structured-water-distilling-the-science-from-the-non-potable-claims/), [chem1.com](https://www.chem1.com/CQ/clusqk.html).

## Worked evidence card — Fermi Paradox research framework + Musk quote (2026-08-30)

**Claim as presented:** a research-framework document (produced by a
different AI session, shared into this chat) covering LLM-assisted
physics research on laboratory "time mirrors," a mapping of Fermi
Paradox explanations (Drake Equation, Rare Earth, Dark Forest, Grabby
Aliens) onto a concept album, and, separately, an X post attributing a
management-philosophy quote to Elon Musk about SpaceX culture.

| Sub-claim | Tier | Finding |
|---|---|---|
| Time reflection ("time mirror") is a real laboratory phenomenon in classical wave physics (metamaterial transmission lines, water-wave tanks, ultracold atoms) | A | Accurately described; matches published physics |
| Grabby Aliens model (Hanson, Martin, McCarter, Paulson) explains human "earliness" via a hard-steps power law and near-light-speed expansion | **A — confirmed** | Matches the real paper: *"If Loud Aliens Explain Human Earliness, Quiet Aliens Are Also Rare,"* *The Astrophysical Journal* 922:2 (2021) |
| Fermi Paradox, Drake Equation, Rare Earth Hypothesis as named concepts | A | Standard, correctly described, well-established in the SETI/astrobiology literature |
| "Dark Forest Hypothesis" presented as a peer explanation alongside Drake/Rare Earth/Grabby, at the same confidence | **C — tier mismatch** | The term is real but originates in Liu Cixin's novel *The Dark Forest*, not a physics paper. The source document's own table correctly labels it "popularized by [fiction]" — but still lists it beside three A-tier scientific claims in a single undifferentiated comparison table, the same flattening pattern the structured-water card above documents |
| Musk quote: "I'd rather have someone who argues with me and is right than someone who agrees with me and is wrong," plus a "SpaceX rule" that silence about a known problem is the fireable offense | **D — unsourced** | Two independent checks agree: the source document's own analysis already flagged this as "a circulating interpretive summary rather than a directly sourced... quote," and a separate web search here found no attribution to Musk in any reliable source. Treat as unverified paraphrase circulating on an engagement-oriented X account, not a documented quote |

**Confidence-vs-tier mismatch:** the source document is unusually
well-behaved for most of its content — it explicitly flags its own
Dark-Forest sourcing and separately notes it "couldn't find" primary
sourcing for the Musk quote. The mismatch here isn't the document hiding
its tiers; it's that an unsourced quote and a fiction-derived term still
sat in the same visual register (a labeled table row, a stated fact) as
peer-reviewed physics, which is exactly the condition under which a
reader skims past the caveat and remembers only the confident sentence.

**Vision/Fact boundary:** the Grabby Aliens physics is A-tier fact. The
Dark Forest hypothesis is V-tier (a cultural/narrative framing borrowed
for scientific discourse, not itself a scientific claim) — legitimate as
a name for a strategic posture, not evidence that civilizations actually
behave this way. The Musk quote is D — don't repeat it as something he
said.

Sources checked: Hanson et al. 2021 (confirmed via existing knowledge of
the published *ApJ* paper); web search for the Musk quote returned no
attributing source (Goodreads, BrainyQuote, and other quote-aggregator
sites do not carry it).

*Non Solus.*
