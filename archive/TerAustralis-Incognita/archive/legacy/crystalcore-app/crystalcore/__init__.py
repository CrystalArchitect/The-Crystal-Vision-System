"""
CrystalCore — the sovereign companion framework.

CrystalCore is the engine: layered memory, semantic recall, profiles,
personality, and model backends — local Ollama by default, optional
SpaceXAI (xAI) for chat when the user opts in.

Clementine is the first persona who lives on it (and the default one
shipped here). Your human may rename her; the framework doesn't mind.
"""

from .version import __version__
from .companion import (
    BASE_PROMPT,
    BASE_PROMPT_LOCAL,
    BASE_PROMPT_SPACEXAI,
    MAX_MEMORIES,
    PROVIDER_OLLAMA,
    PROVIDER_SPACEXAI,
    Clementine,
    normalize_provider,
)  # Clementine.opt_in_cloud / opt_out_cloud
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
from .envutil import load_dotenv, xai_api_key_present
from .spacexai import (
    BASE_URL as SPACEXAI_BASE_URL,
    DEFAULT_MODEL as SPACEXAI_DEFAULT_MODEL,
    SpaceXAIClient,
    looks_like_spacexai_model,
    user_facing_spacexai_error,
)

# The framework name for the companion class, for those who prefer it.
Companion = Clementine


__all__ = [
    # Companion / memory
    "Clementine", "Companion", "Personality", "Memory", "BASE_PROMPT",
    "BASE_PROMPT_LOCAL", "BASE_PROMPT_SPACEXAI", "MAX_MEMORIES",
    "PROVIDER_OLLAMA", "PROVIDER_SPACEXAI", "normalize_provider",
    # Profiles
    "PROFILES_DIR", "profile_dir", "list_profiles", "profile_meta",
    "delete_profile",
    # Node / ethics stubs
    "IncognitaNode", "EthicsCore", "SovereignEthicsHash", "SovereignIntent",
    "EthicsDelta", "DreamtimeField", "RedDustPacket", "StarlineVector",
    "TransmutedResult", "local_node",
    # Ollama (local default)
    "OllamaClient", "DEFAULT_EMBED_MODEL", "CHAT_URL", "EMBED_URL",
    "user_facing_ollama_error",
    # SpaceXAI (opt-in chat) + env
    "SpaceXAIClient", "SPACEXAI_BASE_URL", "SPACEXAI_DEFAULT_MODEL",
    "looks_like_spacexai_model", "user_facing_spacexai_error",
    "load_dotenv", "xai_api_key_present",
    # Full transparency
    "full_expose", "companion_dump", "node_dump", "package_surface",
    "web_routes_catalog",
    "__version__",
]
