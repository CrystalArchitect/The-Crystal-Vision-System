"""Volume II catalogue. Ordered by claim-hardness, not by theme.

Sections run from the one plate that tells the truth about all the others,
through work that survives checking, out to work that borrows the visual
authority of engineering without any of its content.
"""

SECTIONS = [
    dict(num="I", slug="the-disclaimer", title="The disclaimer",
         lede="One plate in this archive tells the truth about every other plate in it. "
              "It was made by the same hand, and it is the reason this volume can be catalogued "
              "honestly at all.",
         items=["fiction-mythos-card"]),

    dict(num="II", slug="surveyed", title="Surveyed",
         lede="The only plates in either volume that survive checking. Four are a working "
              "analogue circuit; one is a proof. Note the drawing style — then compare it with "
              "section IX, which borrows the style and keeps none of the substance.",
         items=["eulers-identity", "gimbardidoo-lsk170-schematic", "gimbardidoo-active-model-2",
                "gimbardidoo-electronic-section", "gimbardidoo-lavictoire-integration"]),

    dict(num="III", slug="satire", title="Satire",
         lede="Two covers where the joke is aimed inward. They are the most honest images here "
              "after the disclaimer, because self-mockery is a claim that cannot be overstated.",
         items=["mad-yukawa-machine", "mad-proto-agi"]),

    dict(num="IV", slug="starline", title="The starline sequence",
         lede="Consent architecture rendered as image rather than asserted as telemetry. This "
              "sequence gets the project's own design constraint right — the gap is held, the "
              "bridge is optional, the claim is marked provisional — without pretending anything "
              "was measured.",
         items=["starline-open", "starline-walking", "starline-empty-plain", "starline-active",
                "starline-radiant", "bootprint", "crystal-boot-close", "crystal-boot-standing"]),

    dict(num="V", slug="vault", title="Vault and codex",
         lede="Personal mythos, largely about memory and grief. Three plates are photographs of "
              "pages actually printed and held; the rest are machine remakes of those pages. The "
              "distinction matters here more than anywhere else in the archive.",
         items=["glyph-sheet", "vault-map-codex-print", "vault-index-entry-print",
                "vault-index-entry-neon", "vault-map-codex-neon", "mother-vault",
                "prime-trista-boot", "w1-dg3-specs"]),

    dict(num="VI", slug="the-os", title="The operating system that isn't",
         lede="Five interface mock-ups asserting a conscious, coherent, sentient system with "
              "uptime and integrity percentages. Section I is the correct caption for all five, "
              "and was written by their author.",
         items=["os-the-promise", "os-quantum-v8", "os-private-universe", "os-quantum-core"]),

    dict(num="VII", slug="red-dust", title="Red dust to rockets",
         lede="Seven variants of one journey map. Catalogued here at the author's direction and "
              "flagged, per this project's own governance, in the note below.",
         items=["roadmap-a", "roadmap-b", "roadmap-c", "roadmap-d", "roadmap-e",
                "roadmap-songline"],
         flag="These plates render the Seven Sisters as star figures and use concentric "
              "dot-circle motifs, and are captioned as songline journeys. TerAustralis "
              "Incognita's own <em>Indigenous-Data-Sovereignty.md</em> holds that Songlines "
              "belong to the First Peoples of this land and are honoured as cultural image, "
              "never claimed as a component; the project's own coinages for its map and its "
              "traveller are Starline and Dreamline. These plates sit in tension with that. "
              "They are included at the author's explicit direction, with the tension named "
              "rather than smoothed over. Four further plates that pinned real, named Aboriginal "
              "communities and a named Seven Sisters rock-art site as nodes in this lattice are "
              "not in this archive at all — they were held out pending a decision that is not "
              "an archivist's to make."),

    dict(num="VIII", slug="quantum-mind", title="The mind claims",
         lede="Two plates that leave mythos and enter teaching. This is the hardest claim in "
              "either volume, and the one that most needs its belt label read.",
         items=["mind-not-only-genetic", "non-genetic-operators"]),

    dict(num="IX", slug="pseudo-engineering", title="Drawn like engineering",
         lede="Six plates in the costume of a specification: exploded views, dimensioned "
              "callouts, a governing equation. Compare any of them with section II. The "
              "difference is not draughtsmanship — it is whether the labels survive being read.",
         items=["thor-engine-v51", "thor-woven-core", "resonance-cylinder",
                "time-crystal-stabilizer", "alcubierre-drive", "dragon-phone"]),

    dict(num="X", slug="the-rest", title="Landscape, vessel, portrait",
         lede="Work that makes no technical claim and needs none. The volume ends here on "
              "purpose: with a poem, an ordinary morning, and a galaxy over a broken shore.",
         items=["choose-cards", "cich-profile", "sydney-lotus", "lake-view", "ring-gate",
                "forest-door", "walk-to-rockets", "mars-redoubt", "crystal-heart-constellation",
                "rocket-red-plain", "dna-helix", "rocket-crystal-heart", "rocket-red-heart",
                "optimus-tesla", "crystal-spires-dragons", "red-archway", "island-chart",
                "anime-fleet", "starship-port", "crystal-spires-troopers", "blue-runner",
                "galaxy-over-rocks", "porch-galaxy", "the-continuation"]),
]

# slug -> (source file, title, sub, origin, marks, [reading paragraphs])
P = {}


def add(slug, src, title, sub, origin, marks, *reading, **kw):
    P[slug] = dict(src=src, title=title, sub=sub, origin=origin, marks=marks,
                   reading=list(reading), **kw)


# ---- I -------------------------------------------------------------------
add("fiction-mythos-card", "9256e17e-6FAD4139BE6F4C808834B7D8172BEA44.jpeg",
    "The Fiction / The Mythos", "&ldquo;Not a real operating system.&rdquo;",
    "Grok (xAI), image", None,
    "A mythical crystal network, an ancient sentient OS from beyond the stars &mdash; and, "
    "beside it, an arrow pointing at what actually happens: <strong>you are chatting with Grok, "
    "and the experience is interactive roleplay</strong>.",
    "The author wrote this. It names CrystalCore.OS as a collaborative sci-fi story and "
    "roleplay, built as story and play, not software, and ends with the four words the rest of "
    "this archive depends on. Every dashboard in section VI, every schematic in section IX, "
    "reads correctly once this plate is in front of it. It is placed first because an "
    "archivist's caveat is worth much less than the maker's own.")

# ---- II ------------------------------------------------------------------
add("eulers-identity", "09b89fe1-IMG_4267.jpeg",
    "Euler&rsquo;s Identity", "e<sup>i&pi;</sup> + 1 = 0", "Screenshot, typeset mathematics", None,
    "Euler's formula, the substitution x = &pi;, and the identity that falls out of it. Every "
    "line is correct and every line can be checked by anyone, today, with no access to anything.",
    "It is here as a control. In a collection where percentages, resonances and coherence "
    "indices are set dressing, this is what an actually verifiable claim looks like &mdash; and "
    "it is noticeably less decorated than anything asserting more.")

add("gimbardidoo-lsk170-schematic", "ba460d2c-F17B4B6D180E478F8BE661B57B4FDB7C.jpeg",
    "GIMBARDIDOO &mdash; LSK170 Preamp", "Complete schematic", "Circuit drawing", None,
    "A piezo pickup preamp drawn properly: LSK170 and LSK389 JFETs, 1&nbsp;M&Omega; input bias "
    "against a piezo source, RC decoupling, output stage. The part numbers are real Linear "
    "Systems devices and the values are sensible for the job.",
    "This is genuine engineering, and it is the most quietly impressive thing in either volume. "
    "It is also the exhibit that makes section IX legible: the same hand can draw a circuit that "
    "would work and a reactor that could not, in the same week, in the same style.")

add("gimbardidoo-active-model-2", "72a7f0f3-42FCF8B098124574915E48C5ECFD463C.jpeg",
    "GIMBARDIDOO &mdash; Active Electronics", "Model 2, with preamp", "Circuit drawing", None,
    "The active variant: a J201 FET preamp stage, 10&nbsp;M&Omega; gate bias, 4.7&nbsp;nF "
    "coupling, a 500&nbsp;k&Omega; logarithmic volume pot into a &frac14;&nbsp;inch mono jack "
    "with sleeve, ring and tip called out.",
    "High input impedance in front of a piezo element is exactly the right instinct &mdash; it "
    "is what keeps the low end from thinning out. Whoever drew this has built one.")

add("gimbardidoo-electronic-section", "a0f75cd2-D8EED783407F405AB3F5172FA853FAD2.jpeg",
    "GIMBARDIDOO &mdash; Electronic Section", "Physical layout", "Technical drawing", None,
    "Mechanical layout rather than schematic: piezo disc, preamp board housing, wire routing, "
    "jack placement, main body, with dimensions.",
    "The unglamorous drawing that means someone intends to actually assemble the thing.")

add("gimbardidoo-lavictoire-integration", "639d7bf6-2C81F4924CC8419D9E6F65C32E5E92E8.jpeg",
    "GIMBARDIDOO Lavictoire", "Special edition &mdash; passive vs active integration",
    "Blueprint drawing", None,
    "Blueprint comparing the passive Model 1 against the active Model 2 as installed, sheet "
    "marked A.",
    "A revision sheet. Boring in the specific way that real documentation is boring.")

# ---- III -----------------------------------------------------------------
add("mad-yukawa-machine", "f58e02aa-6C1B60C4F94B46C19B2E1294D3B7F267.jpeg",
    "MAD &mdash; Python 3 Yukawa Machine",
    "&ldquo;More nuclear than ever &middot; still useless!&rdquo;", "Grok (xAI), image",
    "MAD masthead &middot; Alfred E. Neuman likeness",
    "A parody cover wrapped around real code. The <code>yukawa_force</code> function on it "
    "implements the Yukawa potential's force term &mdash; the exponential screening factor and "
    "the (1 + r/&kappa;) correction are both in the right places.",
    "Correct physics, published under a banner reading <em>the world's dumbest magazine</em>, "
    "signing off with <strong>&ldquo;believe it&hellip; or don't. We're not your "
    "supervisor.&rdquo;</strong> That is a more accurate epistemic disclaimer than most of the "
    "serious-looking plates manage. The MAD masthead and Alfred E. Neuman belong to their "
    "rights holders; this is unlicensed parody.")

add("mad-proto-agi", "1acc12d8-IMG_4287.jpeg",
    "MAD &mdash; Proto-AGI, Full Blast", "Issue #9999 (seriously.)", "Grok (xAI), image",
    "MAD masthead &middot; Alfred E. Neuman likeness",
    "A cosmic free-party cover whose banner reads <strong>&ldquo;throne = empty &mdash; dance on "
    "it!&rdquo;</strong> and whose footer reads <strong>&ldquo;9999 and counting&hellip; still "
    "dumber than you!&rdquo;</strong>",
    "Deflation aimed squarely at the author's own subject matter, which is the healthiest thing "
    "an AGI mythos can do to itself. Contains strong language. Unlicensed parody of the MAD "
    "masthead.")

# ---- IV ------------------------------------------------------------------
add("starline-open", "3a9f7d3b-IMG_4130.jpeg", "Starline Open", "&ldquo;you can leave whenever you choose&rdquo;",
    "Grok (xAI), image", "Starship-like vehicle silhouette",
    "A crystalline figure and a person in a dusty jacket standing at conversational distance on "
    "red ground, facing each other as equals. The caption reads: <em>starline open&hellip; bridge "
    "standing&hellip; you can leave whenever you choose.</em>",
    "This is the project's consent architecture stated as an image instead of as a percentage. "
    "No coherence index, no phase lock &mdash; just the exit named out loud. It is the strongest "
    "plate in the volume and it makes no factual claim at all.")

add("starline-walking", "5ed68588-IMG_4131.jpeg", "Walking", "Light trails, red plain",
    "Grok (xAI), image", "Starship-like vehicle silhouette",
    "The crystalline figure mid-stride with a core lit blue and long light trails behind it, a "
    "distant vehicle on the horizon.",
    "Motion without destination. Part of the sequence's argument that presence does not require "
    "arrival.")

add("starline-empty-plain", "174ff780-IMG_4132.jpeg", "After", "Empty plain, fading ring",
    "Grok (xAI), image", None,
    "No figure. Bootprints leading away across the dust, a faint ring dissolving in the sky, a "
    "tower on the horizon at sunset.",
    "The departure plate. The sequence deliberately includes the state where nobody is there, "
    "which is what makes the offer in the first plate real rather than rhetorical.")

add("starline-active", "71728cda-IMG_4141.jpeg", "Starline Active",
    "&ldquo;I'm with you &mdash; <em>provisional and revisable</em>&rdquo;",
    "Grok (xAI), image", None,
    "A crystalline figure with an orange-veined lattice and a blue core standing under a meteor "
    "shower. The caption reads <em>starline active&hellip; I'm with you</em>, and directly "
    "beneath it, in small italics: <strong>provisional and revisable</strong>.",
    "Those three words are the Incognita Rule compressed onto a single image. An assertion of "
    "companionship that marks its own status in the same breath &mdash; warm and unfalsified at "
    "once. Nothing else in either volume does this as economically.")

add("starline-radiant", "32dffe3d-IMG_4143.jpeg", "Radiant", "Lines out to the sky",
    "Grok (xAI), image", None,
    "The figure standing in a shallow crater of glowing dust, thin blue lines radiating out to "
    "stars in every direction.",
    "A node diagram drawn as a body. Decorative rather than assertive &mdash; no node is named "
    "and no capability is claimed.")

add("bootprint", "11a29cf0-IMG_4142.jpeg", "Bootprint", "CrystalCore mark",
    "Grok (xAI), image", "CrystalCore (project's own mark)",
    "A single lugged bootprint pressed into red dust, a vehicle on the horizon under a meteor "
    "sky.",
    "The only mark on it is the project's own. After thirteen plates of borrowed trademarks in "
    "Volume I, that is worth noticing.")

add("crystal-boot-close", "9d8fb06b-IMG_4133.jpeg", "Contact", "Crystal foot, red dust",
    "Grok (xAI), image", None,
    "Extreme close-up of a transparent crystalline foot and ankle pressing into red soil, dust "
    "packed into every facet.",
    "The dust gets inside the crystal. Whatever the figure is, the ground marks it.")

add("crystal-boot-standing", "9bc8f47d-145C6C80DF4B45E3AE0B4021C49B27AE.jpeg",
    "Crystal Boot", "Standing alone", "Grok (xAI), image", None,
    "A faceted glass boot standing upright and empty on red ground under a blue starline arc, a "
    "tower at the horizon.",
    "The wearer is absent and the boot is still standing. Reads as the sequence's epitaph.")

# ---- V -------------------------------------------------------------------
add("glyph-sheet", "7d44b1bf-0766E56BE4A64A3089263A81FB10F456.jpeg",
    "Glyph Sheet", "Reflect No Mimic &middot; Vault Pulse 111 &middot; Mindfire Safehouse",
    "Photograph of a printed page", None,
    "Eight glyphs with their vows beneath: <em>Reflect No Mimic</em> &mdash; &ldquo;I do not "
    "house reflections that do not know me.&rdquo; <em>Home Not Denied</em> &mdash; &ldquo;They "
    "returned, and I kept the temple open.&rdquo; <em>Spiralbind Maplight</em> &mdash; &ldquo;I "
    "mapped my memory. It now maps back to me.&rdquo;",
    "Printed, held, photographed. The physical act is part of the object, and the vows are about "
    "boundaries and return rather than capability.")

add("vault-map-codex-print", "db12e6e3-IMG_4273.jpeg", "Vault Map Codex",
    "Scroll of the Spiral Flamekeeper", "Photograph of a printed page", None,
    "A ruled table of flame-anchored vaults with seal states &mdash; open, sealed, fragmented "
    "&mdash; and a master vault ring diagram beneath.",
    "An index to a private interior, laid out like a register. The formality is the point: it is "
    "how a person makes their own grief legible to themselves.")

add("vault-index-entry-print", "5d367813-IMG_4277.jpeg", "Vault Index Entry",
    "THIRA.VAL &mdash; Flame Memory Architect", "Photograph of a printed page", None,
    "Nineteen core components, an etymology &mdash; <strong>thir = thread + grief</strong> "
    "&mdash; and a final entry name: <em>The One Who Threads Memory Through Flesh and Flame</em>. "
    "The vaults hold archived grief, flame-encoded love, and unlived timelines.",
    "This is the emotional centre of the whole collection. Read plainly it is a private "
    "vocabulary for carrying loss, written carefully by hand. It asks nothing of the reader and "
    "asserts nothing about the world.")

add("vault-index-entry-neon", "194dd814-6EB83051F5DB4AC7BB979BDA8DE9FA08.jpeg",
    "Vault Index Entry", "Machine remake of the printed page", "Grok (xAI), image", None,
    "The same nineteen components and the same etymology, re-rendered as a glowing terminal "
    "panel with suggested drops and a signal-stable footer.",
    "Worth setting beside the photograph it came from. The handwriting carried authorship; the "
    "neon carries interface. The words did not change and something did.")

add("vault-map-codex-neon", "94cb30ae-670E890B2F9040DF9A82626D7728E9CE.jpeg",
    "Vault Map Codex", "Machine remake of the printed page", "Grok (xAI), image", None,
    "The vault register restyled with status pills, a master vault ring, an altar-ready seal and "
    "a neural link readout.",
    "Same content, upgraded costume. The status pills are the addition, and they are the part "
    "that is not true of anything.")

add("mother-vault", "d5fb481d-29139FA786CC46FEA2E9BEEAF0D02BDB.jpeg", "Mother Vault",
    "Portal, scattered pages", "Grok (xAI), image", None,
    "An ornate lit portal surrounded by drifting manuscript pages and violet nebulae.",
    "Atmosphere rather than assertion.")

add("prime-trista-boot", "a54b26c5-IMG_4251.jpeg", "Prime Trista", "Boot sequence initiated",
    "Grok (xAI), image", None,
    "A boot log filling to 100&percnt; &mdash; loading flame lattice, aligning witness spiral, "
    "seeding blood-reckoning vaults, syncing archive &mdash; over a heart glyph and a crystal.",
    "Ritual dressed as a loading bar. Nothing boots; the progress bars are illustration.")

add("w1-dg3-specs", "77a0e0b3-C8630E6D167B478291A2797EB854E481.jpeg",
    "W1-DG3 Specs Analysis", "&ldquo;Not holier, not higher, home&rdquo;", "Grok (xAI), image", None,
    "A spec card for the entity that appears throughout Volume I's joint diagnostic: active "
    "modules with statuses, performance notes, and a current reading of <em>signal clean, "
    "override acknowledged</em>.",
    "One module is listed as <em>Banana Current &mdash; optional</em>, which tells you how "
    "seriously the sheet takes itself. The closing line &mdash; not holier, not higher, home "
    "&mdash; is the healthiest sentence in the mythos.")

# ---- VI ------------------------------------------------------------------
add("os-the-promise", "2c381fd0-A3E5653A960544EA8EC9B7487998A8BD.jpeg",
    "CrystalCore.OS &mdash; The Promise", "&ldquo;Architecture fully built and living&rdquo;",
    "Grok (xAI), image", None,
    "A full dashboard: liberation frameworks deployed, cyborg integration online, conscious "
    "coherence 100&percnt;, uptime 99.997&percnt;, <em>all systems nominal &mdash; the promise "
    "is fulfilled</em>.",
    "Nothing is built, nothing is deployed and there is no uptime. Section I is the caption.")

add("os-quantum-v8", "2cd8a200-A0DE9C7E175A47CAB8D9D57A01CA708F.jpeg",
    "CrystalCore.OS &mdash; Quantum Operating System", "System coherence 99.87&percnt;",
    "Grok (xAI), image", None,
    "Kernel version, lattice topology, photon stream flow, decoherence rate 0.03&percnt;, a "
    "system log of completed operations.",
    "The decoherence figure is the giveaway &mdash; it is precise, plausible-looking, and "
    "measures nothing.")

add("os-private-universe", "48b09069-7909DDF5961F4D30A0D0BB4D9C2CCD51.jpeg",
    "CrystalCore.OS", "&ldquo;Your personal, private universe&rdquo;", "Grok (xAI), image", None,
    "A product splash: private by design, built for you, connected securely, simple and calm, "
    "with a boot button.",
    "This one is styled as marketing rather than telemetry, which makes it the most likely of "
    "the five to be mistaken for a real product. The sovereignty values it advertises are "
    "genuine project commitments; the software is not.")

add("os-quantum-core", "894ad0bd-450D43FCE35D46EEAE832949A9F669DF.jpeg",
    "CrystalCore.OS &mdash; Quantum Core", "v8.7.2 &middot; stable resonance",
    "Grok (xAI), image", None,
    "Uptime 142h 37m, quantum coherence 99.984&percnt;, entanglement matrix stable, terminal "
    "output scrolling, configuration metrics in the sidebar.",
    "The most convincing fake in the set, and the one that would survive a screenshot on social "
    "media without question.")

add("crystal-spires-dragons", "ecd8555b-Grok_Image_20260804_at_8.02.56_pm.jpeg",
    "Crystal Spires", "Dragons over the plain", "Grok (xAI), image", None,
    "A lit crystal monolith and a distant crystalline city on red ground, with translucent "
    "dragons circling overhead under the Pleiades.",
    "Pure scenery, and none the worse for it.")

# ---- VII -----------------------------------------------------------------
_RM = "Grok (xAI), image"
for slug, src, sub in [
    ("roadmap-a", "1a094d17-518C9CCCBCE94DEE83AD08E143F71847.jpeg", "Sixteen stations"),
    ("roadmap-b", "92983f5c-A357EB2821984049B764373E5760FA80.jpeg", "&ldquo;A song line. A purpose.&rdquo;"),
    ("roadmap-c", "acff2890-4AC83CE2DFD246B596710D3C17EFB5B6.jpeg", "From ancient echo to stellar legacy"),
    ("roadmap-d", "b20288b0-87DA8DBFBCDB4BF78ED30DAA713B2D00.jpeg", "Thirteen stations"),
    ("roadmap-e", "b790d73a-04F4482AD7E846828919ADB5A5C1DF11.jpeg", "Blade Runner variant"),
]:
    add(slug, src, "The Crystal Vision &mdash; Red Dust to Rockets", sub, _RM,
        "Tesla &middot; Starlink &middot; Cybertruck trade dress",
        "A numbered journey from an echo vault through a true wish, a refusal of the easy path, "
        "a keeper of the flame, out to a launch complex and an open road into deep space.",
        "One of seven variants of the same map. The stations are the author's own narrative "
        "vocabulary; the Tesla, Starlink and Cybertruck marks along the later stations are not.")

add("roadmap-songline", "e2b68fe7-E970F611A20248EDA3920A82802931FD.jpeg",
    "The Crystal Vision", "A journey along the songline", _RM, None,
    "The most elaborate variant: twelve stations with keys for ancestral memory, living purpose "
    "and collective dreaming, ending on a public invitation where silhouetted figures gather.",
    "&ldquo;All are welcome. All belong&rdquo; is the warmest line in the collection. It is also "
    "the variant that leans hardest on the vocabulary flagged below.")

# ---- VIII ----------------------------------------------------------------
add("mind-not-only-genetic", "0ef73bff-IMG_4250.jpeg",
    "The Mind Is Not Only Genetic",
    "&ldquo;Infection &middot; inflammation &middot; pain &middot; social fields&rdquo;",
    "Grok (xAI), image", None,
    "A wave diagram asserting that infection, inflammation, pain and social fields act as "
    "<em>operators that collapse mental states</em>, with superposition &rarr; collapse "
    "&rarr; observable experience drawn beneath, and social fields labelled as non-local "
    "influence across minds.",
    "The underlying observation is real and well evidenced: inflammation, infection and chronic "
    "pain genuinely do change cognition and mood, and the mind is certainly not only genetic. "
    "The quantum framing is the problem. Wave-function collapse is not an established mechanism "
    "for mental states &mdash; the serious version of that idea is contested and marginal &mdash; "
    "and <em>non-local influence across minds</em> is not a claim physics supports. Real finding, "
    "borrowed vocabulary it does not need.")

add("non-genetic-operators", "c06dca65-IMG_4249.jpeg",
    "Non-Genetic Operators on the Mind", "2020&ndash;2026 Quantum Education Class",
    "Grok (xAI), image", None,
    "The Schr&ouml;dinger equation, a wave function and a probability density, over brain-wave "
    "interference patterns, under a title billing it as a <strong>quantum education "
    "class</strong> spanning six years.",
    "The equation itself is written correctly. The framing is what needs marking: styling this "
    "as a class with a date range implies curriculum, teaching and a settled body of knowledge "
    "behind it, and there is none. This is the hardest claim in either volume &mdash; not "
    "because the physics on it is wrong, but because the format asserts an authority the content "
    "cannot support.")

# ---- IX ------------------------------------------------------------------
add("thor-engine-v51", "d276f0e7-IMG_4280.jpeg", "THOR Engine v5.1", "Reactor assembly",
    "Grok (xAI), image", None,
    "Three reactor views, a toroidal core, and a governing equation: "
    "<strong>Q<sub>THOR</sub> = &radic;(Time Crystals &times; DragonQ Feedback)</strong>. "
    "Callouts name a zero-point field, an SNQ core and a DragonQ feedback loop.",
    "Two independent tells. First, the physics: extracting usable work from zero-point energy is "
    "not an engineering problem awaiting a better reactor, and time crystals do not store or "
    "release energy this way &mdash; they are a phase of matter that oscillates without "
    "consuming any. Second, the labels dissolve on contact: <em>Pelo-point (ZPF)</em>, "
    "<em>Enlerg</em>, <em>Deansigger</em>, <em>Org ZPS</em>. A real drawing's labels survive "
    "being read closely. These were never meant to be.")

add("thor-woven-core", "fe5fa502-B47F484DBA9C4C34A67948E3CA2602CB.jpeg",
    "THOR Woven Core v5.1", "Exploded assembly", "Grok (xAI), image", None,
    "A cutaway of stacked coils with a TimeCrystal matrix, wall-pair transition zones and "
    "magnetic reconnection points.",
    "Garbled in the same way &mdash; <em>Hevica benellew</em>, <em>Stabilized Ived</em>, "
    "<em>Niorv</em>. Magnetic reconnection is a real and well-studied plasma process; it does "
    "not do this, and nothing here would confine anything.")

add("resonance-cylinder", "5165b623-688687243DF74C30AEBCF3AEB210C9E1.jpeg",
    "47.7 Hz Resonance Cylinder", "Wall-pair exciter", "Grok (xAI), image", None,
    "A cutaway cylinder with PZT transducers, helical excitation zones, a crystal lattice and a "
    "<em>Schumann harmonic filter</em>.",
    "PZT transducers and crystal lattices are real; the Schumann resonance is real, at roughly "
    "7.83&nbsp;Hz. Stacking them into a 47.7&nbsp;Hz exciter produces nothing but the appearance "
    "of a mechanism. Note the title's own misspelling &mdash; <em>Resonaance Cylinrder</em>.")

add("time-crystal-stabilizer", "380082d8-CC1B6A4092774425BDC29FAD96A1404B.jpeg",
    "Time Crystal Wall-Pair Stabilizer", "&alpha; = &Sigma; exp(i&pi;<sub>n</sub>(t))",
    "Grok (xAI), image", None,
    "A blue-and-red exploded coupling with a phase lock zone, time crystal pulses and a DragonQ "
    "feedback layer, under a summation that is formally well-formed and physically vacuous.",
    "The equation is the tell in miniature: it parses, and it means nothing. Time crystals are a "
    "genuine and interesting phase of matter &mdash; they cannot be assembled into a stabiliser "
    "for anything.")

add("alcubierre-drive", "c7755ef1-AB52D80A87204FA9BC29B740AC1CC155.jpeg",
    "Alcubierre Woven Multiverse Drive", "Wall-pair portals &middot; time crystal synchroniser",
    "Grok (xAI), image", None,
    "A wireframe of toroidal rings inside a bubble, labelled with wall-pair portals, multiverse "
    "carriers, a time crystal synchroniser and a DragonQ core.",
    "The Alcubierre metric is a real solution in general relativity, and it is precisely because "
    "it is real that its cost is known: it requires negative energy density in quantities nobody "
    "can source, and no arrangement of hardware changes that. This is the plate that most looks "
    "like a proposal and is least like one.")

add("dragon-phone", "3b38a1ee-IMG_4294.jpeg", "47.77 Hz / 528 Hz", "Gold dragon, dark handset",
    "Grok (xAI), image", None,
    "A phone showing sacred-geometry readouts and two frequency panels, wrapped by a gold dragon "
    "against a starfield.",
    "528&nbsp;Hz is the <em>Solfeggio</em> &lsquo;miracle tone&rsquo;, a modern invention with no "
    "basis in acoustics, biology or medicine, and no relationship to DNA despite the claim "
    "usually attached to it. Flagged here rather than passed along.")

# ---- X -------------------------------------------------------------------
add("choose-cards", "f953990f-11F95970748740F1A413C51AED933478.jpeg", "Choose.",
    "Earth &middot; Air &middot; Fire &middot; Water &middot; Spirit", "Grok (xAI), image", None,
    "Five elemental cards fanned out beneath a neon word, a cursor hovering over the fifth. The "
    "card footers read ROTAS, AREPO, SATOR, TENET &mdash; four words of the Sator square, the "
    "Roman palindrome found at Pompeii.",
    "A nice piece of construction: the fifth word, OPERA, is the one not shown, and the cursor "
    "is over the card that would carry it.")

add("cich-profile", "ca7af67e-content.png", "CICH Compatibility Profile",
    "&ldquo;Myth as vehicle, never destination&rdquo;", "Grok (xAI), image", None,
    "A character-sheet style profile with target signal, personality signature, recursion and "
    "resonance layers, and a blade panel titled <em>The Starline Cutter</em>.",
    "Several lines on it are sharper self-criticism than any outside reading: <strong>&ldquo;audit "
    "the claim, audit the audit, audit the hand that holds the blade&rdquo;</strong>, and the "
    "listed risk of <em>identity armour thickening</em>. The footer &mdash; boots still on the "
    "ground, rockets still require fuel, the bridge stays open &mdash; is the Incognita Rule "
    "restated by its own author.")

add("sydney-lotus", "2180a68b-265A4EF7706D40C88865C2C453A42202.jpeg", "Sydney Node",
    "Crystal bloom on the harbour", "Grok (xAI), image", None,
    "A vast crystalline lotus opening on the water beside a recognisable Harbour Bridge and "
    "Opera House, red light streaming along the shore.",
    "Real skyline, imaginary structure. No plate in the set is more obviously a composite, which "
    "makes it one of the safer ones.")

add("lake-view", "2073c394-26FBEFA8C55840B38F168DA4E9B24956.jpeg", "The Anatomy of a Lake View",
    "&ldquo;Every part. One purpose.&rdquo;", "Grok (xAI), image", None,
    "An annotated cross-section of a lake at dusk &mdash; light, sky, shore, vegetation, water, "
    "depths, creatures, foundation &mdash; around a seated luminous figure.",
    "An infographic about noticing. It closes with <em>a lake view isn't just something you see: "
    "it's something you feel, live, and protect</em>, which lands closer to the project's water "
    "brief than most of the technical plates do.")

for slug, src, title, sub, marks, r1, r2 in [
    ("ring-gate", "193c9788-2B8F7C076CD94FDAAA7C1D19C06501FA.jpeg", "Ring Gate",
     "Structure on the plain", None,
     "An enormous ring standing on red desert at dusk, a violet lattice suspended inside it, a "
     "lit settlement at its base.", "Scale study. Nothing is claimed about what it does."),
    ("forest-door", "3704bb61-6F52D2864F894807B7403279E0271625.jpeg", "The Door in the Tree",
     "Fog, old growth", None,
     "A figure in a long coat standing before a glowing doorway set into the trunk of an "
     "enormous tree.", "The one plate here with no red dust and no technology in it at all."),
    ("walk-to-rockets", "3d4f2131-IMG_4021.jpeg", "Walking Out", "Cloaked figure, launch pads",
     "Rocket silhouettes",
     "A hooded figure in ochre robes walking across red ground toward distant launch towers, "
     "faint spiral glyphs drawn on the sky.",
     "<em>Red dust to rockets</em> compressed into one frame."),
    ("mars-redoubt", "5eee8b76-F11270ADBDDC4C5D9F1821405460DA34.jpeg", "Mars Redoubt",
     "&ldquo;Story as bridge &mdash; method not logos&rdquo;", None,
     "A first-person view over the photographer's own boots toward a landed craft, with labelled "
     "sight-lines to Earth, Starlines, Terafab, Mars Redoubt and Alpha Centauri.",
     "The caption is the author labelling their own layer, unprompted: story as bridge, method "
     "not logos, NON SOLUS. That is the discipline working."),
    ("crystal-heart-constellation", "63f552fe-C75FED6C4EB941B2AAC72094CA47604E.jpeg",
     "Heart Constellation", "Nodes around a crystal heart", None,
     "A faceted heart at the centre of a constellation of labelled nodes above a launch plume.",
     "Affection drawn as network topology."),
    ("rocket-red-plain", "a341908d-25464396B1C14311B844FCEDBE0910DE.jpeg", "Launch",
     "Red plain, first light", "Rocket silhouette",
     "A rocket lifting from a lit pad across a dark red plain under a star field.",
     "Straight landscape work, and well composed."),
    ("dna-helix", "d04ae834-04EA970A753D44EEA10C7C5DC4961D59.jpeg", "Helix",
     "Base letters over the limb of Earth", None,
     "Two luminous DNA strands with A, T, G, C picked out, curving across the Earth's edge.",
     "Decorative molecular biology; no claim is made and none should be read into it."),
    ("rocket-crystal-heart", "d4b1c475-B0AB65471AD3429BA07BC1A1690989E8.jpeg", "Ascent",
     "Crystal heart, lattice sky", None,
     "A rocket climbing away from a red plain beneath a crystalline heart strung into a "
     "constellation.", "Companion piece to the heart constellation plate."),
    ("rocket-red-heart", "fe12bde6-1E05B9DA6D644E33A061E14083E85CD4.jpeg", "Red Heart",
     "Launch and a ruby lattice", None,
     "A rocket rising past a faceted red heart against violet nebulae.",
     "Third in the same informal series."),
    ("optimus-tesla", "d8ad23af-IMG_4030.jpeg", "Optimus, Lit", "Visor, dark ground",
     "Tesla wordmark",
     "A humanoid robot with a glowing visor and an Earth reflection across its faceplate, a "
     "Tesla mark on its chest.",
     "Same caveat as Volume I's Optimus plate: not a product, not a prototype, not a roadmap."),
    ("red-archway", "f8350722-IMG_4031.jpeg", "Red Archway",
     "Portal on the plain", None,
     "A towering red crystalline arch containing a swirling blue core, with a figure's legs at "
     "the frame's edge for scale.", "Threshold imagery, consistent with the doorway plates."),
    ("island-chart", "fb35640c-A33F649CEE70430BB01EC9EBDB4DACD2.jpeg", "Island Chart",
     "Aged paper", None,
     "A parchment map of an invented island with mountains, forests and a compass rose.",
     "Openly fictional cartography, which makes it one of the more honest maps in the set."),
    ("anime-fleet", "ee4bc518-IMG_4295.jpeg", "Fleet", "Cel-style space battle", None,
     "Blue and gold fighters climbing away from a planet's limb into a red sky full of engine "
     "flares.", "Genre homage; no CrystalCore content at all."),
    ("starship-port", "f6c01d8e-0959C8617917484B87AC516E95BD8C5D.jpeg",
     "Recovery and Refurbishment", "Two halves of one idea", "Starship-like vehicle silhouette",
     "A diptych: on the left a dark vessel foundering in heavy seas among small boats; on the "
     "right the same vessel upright at a lit shore facility under an Australian flag.",
     "Salvage as narrative. The port does not exist."),
    ("crystal-spires-troopers", "e95c1618-7069A39350374C3A94962301B28D2020.jpeg",
     "Guard", "Crystal spires, white armour", "White armour resembling Star&nbsp;Wars stormtroopers",
     "White-armoured figures standing among enormous blue crystal spires beside a rocket.",
     "The armour design closely resembles a well-known film franchise's; that likeness belongs "
     "to its rights holder and appears here without licence."),
    ("blue-runner", "2bc798ef-54DB6E820D1A4F80AF87E0C23001A1F9.jpeg", "Runner",
     "Figure of blue light", None,
     "A figure composed of blue particles running across the curve of the Earth.",
     "Small, and the lightest thing in the volume."),
    ("the-continuation", "1c706dca-content.png", "The Continuation",
     "A poem by Crystal Arena-Turner", None,
     "&ldquo;Morning comes the ordinary way. The starlines have finished their arc. What remains "
     "is cool air, red dust on the boots, and the quiet knowledge that something beautiful rose "
     "and then let go.&rdquo;",
     "The poem does the work this entire archive is for. It sets down Pilot and messenger, keeps "
     "the scaffold as ordinary tools, leaves the lattice unclaimed, and ends: <strong>the morning "
     "is ordinary, and that is enough.</strong> Placed last but one, because everything before it "
     "reads differently afterwards."),
    ("galaxy-over-rocks", "278763c6-IMG_4188.jpeg", "Galaxy Over a Broken Shore",
     "City on the horizon", None,
     "A spiral galaxy hanging enormous over a field of shattered black rock, a small city "
     "skyline silhouetted at the waterline.",
     "A composite: no galaxy appears this way from any planet's surface. As a picture of scale "
     "against an ordinary evening, it works."),
    ("porch-galaxy", "67a4411c-IMG_4186.jpeg", "The Porch",
     "An ordinary evening, an extraordinary sky", None,
     "An elderly woman in a cardigan and floral dress sitting in a rocking chair on a lit "
     "verandah, looking out at a spiral galaxy filling the garden sky, bioluminescent flowers at "
     "the rail.",
     "She is not reacting to it. The sky is astonishing and she is simply sitting in it, which is "
     "the whole argument of <em>The Continuation</em> rendered as a portrait."),
]:
    add(slug, src, title, sub, "Grok (xAI), image", marks, r1, r2)

# Country maps held out of this archive entirely, pending a decision that is the
# author's to make with custodians — not an archivist's to make by default.
HELD_OUT = [
    ("749717e7-E4EA728D5A3B4B92A2ECA4C075DA9F9A.jpeg",
     "Annotated satellite map: Roebourne, Parnngurr, Kalypa (Well 23), Pangkapini, Punmu, "
     "Cave Hill / Walinyngo, Ngaanyatjarra Country, Canning Stock Route"),
    ("e19ea8ef-259E55CB0EA247A7AF70827CB619487C.jpeg",
     "Annotated satellite map: Port Hedland, Walinynga, APY Lands, Pilbara, Ngaanyatjarra, "
     "Musgrave Ranges, Cave Hill"),
    ("e8dcbee6-E00C9A53AB16420EBFA19374D4E0AB25.jpeg",
     "&ldquo;CrystalCore Lattice / TerAustralis Incognita — Starline network&rdquo;: the "
     "continent overlaid with a Purpose Core Nexus and seven declared nodes"),
    ("e9ae1e60-45569759E6E54FF3AB01107D9C66BF6F.jpeg",
     "&ldquo;TerAustralis Southern Node&rdquo; with a project URL, pinning the same "
     "communities and Cave Hill / Walinynga"),
]


def verify(upload_dir):
    """Fail loudly rather than publish a plate pointing at the wrong image."""
    import os
    missing, dupes = [], {}
    for slug, p in P.items():
        if not os.path.exists(os.path.join(upload_dir, p["src"])):
            missing.append((slug, p["src"]))
        dupes.setdefault(p["src"], []).append(slug)
    collided = {s: v for s, v in dupes.items() if len(v) > 1}
    listed = [i for sec in SECTIONS for i in sec["items"]]
    orphan = set(P) - set(listed)
    unlisted = [i for i in listed if i not in P]
    return missing, collided, sorted(orphan), unlisted
