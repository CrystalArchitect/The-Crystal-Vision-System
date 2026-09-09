# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CrystalCore.mind — the mind.

Layered memory, semantic recall, profiles, personality, and a local-model
connection: everything a sovereign, locally-run companion needs, with
nothing leaving the device.

The mind is nameless. A persona name is a runtime property — given by the
human or chosen by the companion, held in `Personality.name`, and empty
until then. Front-of-house branding (Clementine) belongs to the interface
that speaks for this mind, never to the mind itself.
"""

from .companion import BASE_PROMPT, CrystalCore
from .memory import Memory, Personality
from .profiles import (PROFILES_DIR, delete_profile, list_profiles,
                       profile_dir, profile_meta)

# The companion class under a role name, for callers who prefer it.
Companion = CrystalCore

__version__ = "0.8.0"

# System identity, for anything that introspects this package rather than
# just importing from it (a boot/status display, a health check).
SYSTEM_VERSION = f"CrystalCore.OS {__version__}"
MEMORY_SCHEMA_VERSION = "1"
SYSTEM_MANIFEST = {
    "system": "CrystalCore.OS",
    "version": SYSTEM_VERSION,
    # Design lineage, not a dependency: this package shares no import with
    # core/crystal-core (the bridge) in either direction today.
    # "Bridge-compatible" names the intent, not a wired connection.
    "architecture": "bridge-compatible (intent)",
    "memory_schema": MEMORY_SCHEMA_VERSION,
    # The mind carries no persona name. Whatever the companion is called
    # lives in Personality.name — set at runtime, or left empty.
    "runtime": "crystalcore.mind",
    "authority": "companion_only",
}

__all__ = [
    "CrystalCore", "Companion", "Personality", "Memory", "BASE_PROMPT",
    "PROFILES_DIR", "profile_dir", "list_profiles", "profile_meta",
    "delete_profile", "__version__",
    "SYSTEM_VERSION", "MEMORY_SCHEMA_VERSION", "SYSTEM_MANIFEST",
]
