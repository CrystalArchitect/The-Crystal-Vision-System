# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CrystalCore profiles: separate people, separate memories.

Each profile is a self-contained folder — its own memory, chosen name,
avatar, and personality. No central registry: a profile folder can be
copied to another machine and the companion arrives whole.
"""

import json
import shutil
from pathlib import Path

# As with the memory folder: an existing profiles folder holds real people's
# separate histories, so a legacy one keeps being used where it is found
# rather than being silently abandoned for an empty new one.
DEFAULT_PROFILES_DIR = Path("crystalcore_profiles")
LEGACY_PROFILES_DIR = Path("lumina_profiles")

PROFILES_DIR = (
    LEGACY_PROFILES_DIR
    if not DEFAULT_PROFILES_DIR.exists() and LEGACY_PROFILES_DIR.exists()
    else DEFAULT_PROFILES_DIR
)


def profile_dir(name: str) -> str:
    """Each profile is its own folder: separate memory, name, personality.
    Complete isolation between the people who share a machine."""
    safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
    if not safe:
        raise ValueError("Profile name must contain letters or digits.")
    return str(PROFILES_DIR / safe)


def list_profiles() -> list:
    if not PROFILES_DIR.exists():
        return []
    return sorted(p.name for p in PROFILES_DIR.iterdir() if p.is_dir())


def profile_meta(name: str) -> dict:
    """Read a profile's avatar/description/companion-name from its own
    config.json — every profile is self-contained, no central registry."""
    config = Path(profile_dir(name)) / "config.json"
    meta = {"profile": name, "avatar": "", "description": "",
            "name": "", "model": ""}
    if config.exists():
        try:
            data = json.loads(config.read_text())
            meta["avatar"] = data.get("avatar", "")
            meta["description"] = data.get("description", "")
            meta["name"] = data.get("name", "")
            meta["model"] = data.get("model", "")
        except (json.JSONDecodeError, OSError):
            pass
    return meta


def delete_profile(name: str) -> bool:
    """Remove a profile folder entirely — the user's right, irreversible."""
    target = Path(profile_dir(name))
    if target.exists() and target.parent == PROFILES_DIR:
        shutil.rmtree(target)
        return True
    return False
