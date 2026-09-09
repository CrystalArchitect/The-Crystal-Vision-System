"""
CrystalCore — the sovereign companion framework.

CrystalCore is the engine: layered memory, semantic recall, profiles,
personality, and a local-model connection — everything a sovereign,
locally-run companion needs, with nothing leaving the device.

Clementine is the first persona who lives on it (and the default one
shipped here). Your human may rename her; the framework doesn't mind.
"""

from .version import __version__
from .companion import BASE_PROMPT, MAX_MEMORIES, Clementine
from .expose import (
    companion_dump,
    full_expose,
    node_dump,
    package_surface,
    web_routes_catalog,
)
from .memory import Memory, Personality
from .node import (
    DreamtimeField,
    EthicsCore,
    EthicsDelta,
    IncognitaNode,
    RedDustPacket,
    SovereignEthicsHash,
    SovereignIntent,
    StarlineVector,
    TransmutedResult,
    local_node,
)
from .ollama import (
    CHAT_URL,
    DEFAULT_EMBED_MODEL,
    EMBED_URL,
    OllamaClient,
    user_facing_ollama_error,
)
from .profiles import (PROFILES_DIR, delete_profile, list_profiles,
                       profile_dir, profile_meta)

# The framework name for the companion class, for those who prefer it.
Companion = Clementine


__all__ = [
    # Companion / memory
    "Clementine", "Companion", "Personality", "Memory", "BASE_PROMPT",
    "MAX_MEMORIES",
    # Profiles
    "PROFILES_DIR", "profile_dir", "list_profiles", "profile_meta",
    "delete_profile",
    # Node / ethics stubs
    "IncognitaNode", "EthicsCore", "SovereignEthicsHash", "SovereignIntent",
    "EthicsDelta", "DreamtimeField", "RedDustPacket", "StarlineVector",
    "TransmutedResult", "local_node",
    # Ollama
    "OllamaClient", "DEFAULT_EMBED_MODEL", "CHAT_URL", "EMBED_URL",
    "user_facing_ollama_error",
    # Full transparency
    "full_expose", "companion_dump", "node_dump", "package_surface",
    "web_routes_catalog",
    "__version__",
]
