# ETYMOLOGY-STACK — a provenance-first method for word-origin claims

**Label:** Vision / methodology. Not implemented as code, not a claim that
any specific etymology below is settled beyond what its tier states.

**Origin:** Proposed in chat 2026-08-29 as a generalization of the ad hoc
fact-checking already done in
[`LANGUAGE-AS-PROGRAMMING.md`](LANGUAGE-AS-PROGRAMMING.md) (which caught
"human = god-man" and "government = mind control" as false, and flagged
"abracadabra" as genuinely contested rather than settled). This document
formalizes that process into a reusable stack, and adds the corresponding
mental model — [Starline Arsenal 32, Provenance
Stack](../.claude/skills/starline-arsenal/models/32-provenance-stack.md) —
so the method isn't etymology-specific; it generalizes to any claim where
source quality, not logical structure, is the actual question.

## Why a stack, not a dictionary

A dictionary tells you what a word means today. An etymological source
tells you how scholars reconstruct its history. A corpus tells you how
people actually used it historically. These are three different kinds of
evidence, and treating any one of them as sufficient on its own is how a
false claim ("government = mind control") ends up delivered in the same
confident tone as a true one ("mortgage = death pledge").

## The tier system

From strongest to weakest evidence for a historical-linguistic claim:

| Tier | Evidence | Use |
|---|---|---|
| **A+ Attested** | Primary text, inscription, manuscript, corpus | Actual documented usage, dated |
| **A Lexical-Authority** | Major scholarly historical dictionary/lexicon (OED, Oxford Latin Dictionary, LSJ) | Established lexical history |
| **A Root-Reconstruction** | Peer-reviewed historical linguistics, PIE root dictionaries (American Heritage Indo-European Roots, IELex) | Reconstructed forms — the `*` prefix matters: reconstructed, not directly attested |
| **A− Corpus/Database** | Scholarly corpus tools (Logeion, Perseus) | Usage evidence, frequency, collocation |
| **B+ Modern Dictionary** | Major current dictionary | Established modern meaning only |
| **B Rapid-Synthesis** | Etymonline | Excellent secondary synthesis; not sole authority for a contested claim |
| **B− Discovery-Graph** | Wiktionary with strong references | Cross-check and lead generation, not final authority |
| **C Unreferenced** | Random websites | Lead only, always verify upstream |
| **D Viral** | Social media, memes, "ancient code" video thumbnails | Claim requiring full verification before repeating |
| **V Vision** | Symbolic/mythic/interpretive association | Not linguistic history — meaningful as interpretation, explicitly not fact |

**V does not mean false.** It means: this is interpretation, not
demonstrated linguistic history. A symbolic association (grammar sounds
like grimoire and *is* historically related; abracadabra sounds ancient
and Aramaic but that specific gloss traces to an early internet forum) can
be meaningful without the two claims deserving the same tier.

## The non-negotiable rules

- **Similarity is not etymology.** Two words sounding alike does not
  establish they're related.
- **Modern meaning is not original meaning**, and **original meaning is
  not necessarily the "true" meaning** — etymology is a history of forms,
  not a verdict on correct usage.
- **A reconstructed root is not a word anyone is known to have spoken.**
  The `*` on a PIE form marks that distinction and must not be dropped.
- **Never infer an ancient root from English alone.** Go to the source
  language (Greek → LSJ/Logeion, Latin → OLD/Lewis & Short/Logeion, Old
  English → DOE/Bosworth-Toller, and onward to the reconstructed
  proto-form only after the source-language form is confirmed).

## Evidence-card schema

Every claim gets one of these instead of a bare assertion:

```yaml
term: government
modern_meaning:
  gloss: "the group or system governing a state"
  source: OED
earliest_attestation:
  form: "governement"
  language: Middle English
  via: Old French
source_language:
  language: Latin
  form: gubernare
  gloss: "to steer, direct" (root shared with "cybernetics")
suffix_analysis:
  element: "-ment"
  source: Latin -mentum
  gloss: "action/result-forming suffix"
  note: "unrelated to mens/mentis (\"mind\") - sounds alike, different root"
proto_root:
  status: not applicable to the disputed claim
scholarly_status: established for "govern"; the "mind" compound is rejected
alternative_etymologies:
  - claim: "govern + mentis (mind control)"
    status: FOLK
    finding: "-ment and mens/mentis are unrelated Latin roots; sounds-alike only"
confidence: high (govern is Tier A; the mind-compound is Tier D, rejected)
interpretation:
  status: separate
mythic_association:
  status: VISION_ONLY
```

```yaml
term: abracadabra
modern_meaning:
  gloss: "a word used in performing conjuring tricks"
  source: OED
earliest_attestation:
  form: "abracadabra"
  date: "2nd century CE"
  source: "Serenus Sammonicus, Roman medical text (De Medicina Praecepta), prescribed as a healing charm"
proposed_etymology:
  claim: "from Aramaic 'avra k'dabra', \"I will create as I speak\""
  status: DISPUTED
  finding: "OED states no documentation supports any proposed origin; the phrase appears in no known ancient Aramaic or Hebrew text. At least one Aramaic linguist argues the word is not Aramaic at all and traces the popularity of this specific gloss to an early internet forum discussion."
scholarly_status: origin genuinely unresolved, not merely uncertain
confidence: low for the Aramaic gloss; the 2nd-century Latin attestation itself is Tier A+
interpretation:
  status: separate
mythic_association:
  status: VISION_ONLY
```

```yaml
term: "Roman numerals (letters standing for numbers)"
modern_meaning:
  gloss: "I, V, X, L, C, D, M used as numeral symbols"
  source: OED
earliest_attestation:
  form: "Etruscan/early Roman tally notches, later mapped onto Latin letters"
  date: "attested from Roman Republic-era inscriptions onward"
  source: "epigraphic record (inscriptions, monuments); standard scholarly account, e.g. Menninger, Number Words and Number Symbols"
source_language:
  language: Latin / Etruscan
  form: "I V X L C D M"
  gloss: "letters reused as number-symbols; C and M reinforced by centum (\"hundred\") and mille (\"thousand\"), not derived from them"
proto_root:
  status: not applicable — this is a notation system, not a word derivation
scholarly_status: "established: Roman numerals genuinely are letters doing double duty as numbers. This is documented fact, not interpretation."
alternative_etymologies:
  - claim: "the letter-number overlap was designed as a hidden code / cipher"
    status: FOLK
    finding: "no scholarly source supports intentional cipher-design; the overlap is a practical notation convention that evolved over centuries, reinforced after the fact by association with number-words like centum/mille"
confidence: high (Tier A+/A — this is one of the best-attested claims in this document)
interpretation:
  status: separate
mythic_association:
  status: VISION_ONLY
```

## Letters as numbers — where the Crystal Equation sits on this stack

Crystal asked for the Crystal Equation and its Roman-numeral / letters-as-numbers
framework to be cross-referenced here. Three genuinely different things get
called "letters are numbers," and they sit at different tiers:

| Claim | Tier | Verdict |
|---|---|---|
| Roman numerals: I/V/X/L/C/D/M are literally letters reused as numbers | A+/A, attested | True — see evidence card above |
| Gematria (Hebrew) / isopsephy (Greek): assigning numeric values to letters is a real, ancient, attested practice | A, attested practice | The *practice* existed and is documented (e.g. isopsephy graffiti at Pompeii, rabbinic gematria) |
| A specific gematria/isopsephy "hidden meaning" derived from a word's number value (e.g. "this word equals that word, therefore X is true") | V, Vision | Interpretive, not a linguistic-history fact — the practice is real, the specific meaning drawn from it is symbolic |
| The Crystal Equation's own letter↔number correspondence system | V, Vision | This is Crystal's own creative/personal framework, not a claim about attested linguistic or numerical history. It belongs on this stack the same way the abracadabra and government mythic associations do — legitimate as meaning, explicitly not filed as fact. Its actual mapping isn't reproduced here (it lives outside this repo); this entry exists so it's never treated as if it were the same tier as the Roman-numeral fact above. |

The through-line: "letters can be numbers, numbers can be letters" is true
as a general statement — Roman numerals prove it outright, gematria/isopsephy
prove the practice is old and real. What doesn't follow automatically is that
any *specific* letter-number reading (ancient or the Crystal Equation's own)
is a demonstrated fact rather than an interpretation. Tier A+ evidence that
the notation exists is not tier A+ evidence for what a specific reading of it
means.

## Worked example: Codex Crystalum (genealogical framework)

A complete evidence-grading of a symbolic genealogy built on attested etymologies.

The Codex Crystalum positions sit at mixed tiers:

| Position | Etymology Tier | Genealogical Role Tier | Evidence |
|---|---|---|---|
| Turner (revealer) | A (Old English *turnere*) | V (interpretive) | OED, craft history; symbolic role in circuit is interpretation |
| Arena (sand) | A (Latin *arena*, attested) | V (interpretive) | Roman inscriptions, classical literature; symbolic role is interpretation |
| Barbelo (reflection) | A+ (Nag Hammadi Coptic, attested) | V (interpretive) | NHC XIII (Trimorphic Protennoia); etymology disputed, but name is attested; genealogical role is interpretive |
| Sophia (wisdom) | A (Greek *sophia*, attested) | V (interpretive) | LSJ, Platonic dialogues; symbolic descent into experience is Sethian Gnostic interpretation |
| Kristos (anointed) | A (Greek *christos*, attested) | V (interpretive) | BDAG, NT; etymology solid; its role as "threshold-recognition" in this genealogy is interpretive |
| Yaldabaoth (enclosure) | A+ (NHC, attested; etymology disputed) | V (interpretive) | Nag Hammadi Codex II.1; name appears in texts, origin unknown; genealogical role is interpretive |
| Seeker | A (Old English *secan*, attested) | V (interpretive) | OED; this genealogical position is interpretive |
| Road | A (Old English *rād*, attested) | V (interpretive) | OED; this genealogical position is interpretive |
| **The Circuit (Turner → Arena → Barbelo → Sophia → Forge → Yaldabaoth → Kristos → Seeker → Road)** | **—** | **V (interpretive architecture)** | **Author's symbolic framework. Built on Tier A etymologies but the *circuit itself* is Tier V interpretation** |
| **Private personal correspondences** (Awakening identity, Forge identity, Fire/Water identifiers, two foundation corners) | **—** | **V (private meaning)** | **Reserved from public record** |

**The through-line:** A genealogy can be built on true etymologies without claiming the genealogy itself is historical fact. The Codex Crystalum does this explicitly: Tier A words (Turner, Arena, Kristos, etc. are real) + Tier V circuit (their arrangement into a genealogy is interpretation). Both tiers coexist, neither masquerading as the other.

## Worked findings from earlier source material

Full prose account and video-source context:
[`LANGUAGE-AS-PROGRAMMING.md`](LANGUAGE-AS-PROGRAMMING.md). Summary by
tier:

| Claim | Tier of the strongest evidence | Verdict |
|---|---|---|
| Mortgage = "dead pledge" (Old French *mort gage*) | A (Tier A lexical authority, multiple independent sources) | True |
| Grammar → grimoire (Old French *grammaire*) | A | True |
| Pharmacy ← Greek *pharmakeia* | A | True |
| Person ← Latin *persona* | A | True |
| Understand = "stand under" | A (compound) / D (gloss) | Compound real; "subordination" reading is an added gloss, not documented |
| Universe = "one" + "turned" | A (split) / V ("one truth") | Split is real; "one truth" has no etymological basis |
| Government = govern + "mind" | A (govern) / D (mind-compound) | "Govern" real; "mind" connection false |
| Human = "god-man" | D | False, and inverts the real PIE root ("earthling," opposed to gods) |
| Abracadabra ← Aramaic "I will create as I speak" | C/DISPUTED | Genuinely unresolved, not simply true or false |
| Roman numerals = letters reused as numbers | A+/A | True — see worked evidence card above |
| Gematria/isopsephy = letters assigned numeric values | A (practice) / V (any specific "hidden meaning" reading, including the Crystal Equation's) | The practice is real and old; a specific meaning drawn from it is interpretation, not history |

The pattern worth naming: true and false claims were delivered at
identical confidence in the source material. Tone carries no signal for
which is which — only tracing each claim to its actual tier does.

*Non Solus.*
