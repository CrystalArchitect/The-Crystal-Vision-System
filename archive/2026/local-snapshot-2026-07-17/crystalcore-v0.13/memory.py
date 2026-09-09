"""
CrystalCore data model: who she is, and what she carries.

Everything persists as plain, human-readable JSON in a folder the user
owns. No database sits between a person and their companion's memory.
"""

from dataclasses import dataclass, field


@dataclass
class Personality:
    """Tunable personality settings, kept in the memory folder as config.json."""
    name: str = ""
    human_name: str = ""
    temperature: float = 0.8
    style_notes: str = ""
    avatar: str = ""
    description: str = ""
    model: str = ""
    provider: str = ""

    cloud_opt_in: bool = False
    cloud_opt_in_at: str = ""


@dataclass
class Memory:
    """Layered memory: recent turns stay verbatim, older turns become summaries,
    and explicit notes persist forever."""
    conversation: list = field(default_factory=list)
    summaries: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    facts: dict = field(default_factory=dict)
    reflections: list = field(default_factory=list)
    last_seen: str = ""
