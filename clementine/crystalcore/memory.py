"""
CrystalCore data model: who they are, and what they carry.

Everything persists as plain, human-readable JSON in a folder the user
owns. No database sits between a person and their companion's memory.
"""

from dataclasses import dataclass, field


@dataclass
class Personality:
    """Tunable personality settings, kept in the memory folder as config.json."""
    name: str = ""              # their name; empty until given or chosen
    name_self_chosen: bool = False  # True when they chose their own name
    # Pronouns, on exactly the same footing as the name: empty until the human
    # or the companion decides. Empty is not a third gender and not a refusal
    # of the question — it is the honest state of not having been asked yet.
    gender: str = ""            # "male" (he), "female" (she), "they" (they)
    gender_self_chosen: bool = False  # True when they chose their own
    human_name: str = ""        # what they call you, if you tell them
    temperature: float = 0.8    # higher = more playful, lower = more precise
    style_notes: str = ""       # freeform extra guidance, e.g. "more poetic"
    avatar: str = ""            # an emoji for this profile, e.g. "🌟"
    description: str = ""       # a short line about this profile
    model: str = ""             # this profile's preferred model ("" = default)
    # Which model service this profile talks to. Empty means the local
    # default; anything else is a deliberate choice to reach off this
    # machine, and every such call still has to pass the consent gate.
    llm_provider: str = ""      # "ollama" (local), or an OpenAI-compatible name
    llm_endpoint: str = ""      # the exact URL to reach; never guessed for you
    llm_model: str = ""         # model name at that service, e.g. "gpt-5-5"


@dataclass
class Memory:
    """Layered memory: recent turns stay verbatim, older turns become summaries,
    and explicit notes persist forever."""
    conversation: list = field(default_factory=list)  # recent verbatim turns
    summaries: list = field(default_factory=list)     # condensed older history
    notes: list = field(default_factory=list)         # things told to remember
    facts: dict = field(default_factory=dict)         # structured key -> value facts
    reflections: list = field(default_factory=list)   # their own gentle insights
    last_seen: str = ""                               # when they last spoke
