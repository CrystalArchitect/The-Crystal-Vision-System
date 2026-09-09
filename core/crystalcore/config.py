# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Configuration loader for CrystalBridge — reads profiles/<name>/bridge_config.json.

Guest grants carry two independent consent axes:
  - visibility scope (private|shared) — which visibility classes a guest may touch
  - memory types (episodic|semantic|reflective) — which memory *layers* a guest may touch

The memory structure *is* the taxonomy (no per-entry type field):
  summaries → episodic, notes+facts → semantic, reflections → reflective,
  conversation → working (never guest-readable, and deliberately not grantable).

Empty scope or empty types is absence of consent, not legacy full access.
Unknown type names fail loud at load ("Told, or stopped.").
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = SRC_ROOT / "profiles"

#: The documented memory taxonomy (Clementine content/MEMORY.md): the layers
#: a grant may name.
MEMORY_TYPES = ("episodic", "semantic", "reflective")

#: The visibility classes a grant's scope may name (CONSENT-GATE-SPEC.md §
#: "Two classes at first, deliberately no more"). An unknown class is a
#: config error, the same as an unknown memory type — validated at load so
#: the operator is stopped, not a guest surprised.
VISIBILITY_CLASSES = ("private", "shared")


def _require_steward_persist(operation: str, path: Path) -> None:
    """Host trust lives under crystal-core/; this package runs from core/."""
    import sys

    sibling = Path(__file__).resolve().parent.parent / "crystal-core"
    s = str(sibling)
    if s not in sys.path:
        sys.path.insert(0, s)
    from host_trust.classify import require_steward_persist

    require_steward_persist(operation, path)


def write_json_atomic(path: Path, obj: object) -> None:
    """Replace `path` with JSON only after the new bytes are complete.

    A crash mid-write used to leave a half-written `bridge_config.json`
    — the grants file — and lose the previous one. Write beside it,
    fsync, then `os.replace`. New files are 0600 (hashes of guest
    secrets live here).

    Host trust refuses this write on shared/unknown hosts unless the
    path is job-scoped GitHub scratch. Grants are durable steward
    material.
    """
    path = Path(path)
    _require_steward_persist("token-mint", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, path)


@dataclass
class GuestGrant:
    approved: bool
    tools: list[str] = field(default_factory=list)
    # Scope: which memory visibility classes this guest may read, and which
    # single class its teachings land in (the first entry). Empty means none —
    # absence of scope is absence of consent, not legacy full access.
    read_scope: list[str] = field(default_factory=list)
    write_scope: list[str] = field(default_factory=list)
    # Types: which memory layers (MEMORY_TYPES) this guest may read from and
    # write into. Empty means none — a config written before this dimension
    # existed has not consented to it, and the gate refuses with a reason
    # that says exactly what to add. Fail-closed, like everything here.
    read_types: list[str] = field(default_factory=list)
    write_types: list[str] = field(default_factory=list)
    # Provenance: SHA-256 hex of this guest's minted secret. Empty means no
    # provenance is configured, and the gate refuses — mint one with
    # `python -m crystalcore.bridge --mint-token <guest>`.
    token_hash: str = ""


@dataclass
class BridgeConfig:
    profile: str
    human_name: str
    interactive_approval: bool
    guests: dict[str, GuestGrant]
    profile_dir: Path

    @property
    def audit_path(self) -> Path:
        return self.profile_dir / "audit.jsonl"

    @property
    def revocations_path(self) -> Path:
        return self.profile_dir / "revocations.jsonl"

    @property
    def pending_path(self) -> Path:
        return self.profile_dir / "pending.jsonl"

    def guest(self, name: str) -> GuestGrant | None:
        return self.guests.get((name or "").strip().lower())

    @classmethod
    def load(cls, profile: str = "default",
             profiles_dir: Path | None = None) -> "BridgeConfig":
        profile_dir = (profiles_dir or PROFILES_DIR) / profile
        config_path = profile_dir / "bridge_config.json"
        if not config_path.exists():
            raise FileNotFoundError(
                f"No bridge config at {config_path}. Copy "
                f"profiles/default/bridge_config.json to a new profile folder and "
                f"edit it, or pass --profile default."
            )
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        guests = {}
        for name, grant in raw.get("guests", {}).items():
            read_types = list(grant.get("read_types", []))
            write_types = list(grant.get("write_types", []))
            # An unknown type name is a config error, not a silent drop: a
            # grant naming a layer this gate does not govern must stop the
            # operator, loudly, before any guest is served. Told, or stopped.
            unknown = [t for t in read_types + write_types
                       if t not in MEMORY_TYPES]
            if unknown:
                raise SystemExit(
                    f"bridge_config.json: guest '{name}' names unknown memory "
                    f"type(s) {unknown} — valid types are {list(MEMORY_TYPES)}. "
                    "Fix the grant before starting the bridge."
                )
            read_scope = list(grant.get("read_scope", []))
            write_scope = list(grant.get("write_scope", []))
            # The visibility axis was validated for memory *types* but not for
            # visibility *classes*: a scope naming an ungoverned class loaded
            # as an arbitrary string, and `teach` passes write_scope[0]
            # straight into remember(visibility=...). Same rule as types —
            # unknown class stops startup.
            unknown_scope = [c for c in read_scope + write_scope
                             if c not in VISIBILITY_CLASSES]
            if unknown_scope:
                raise SystemExit(
                    f"bridge_config.json: guest '{name}' names unknown "
                    f"visibility class(es) {unknown_scope} — valid classes are "
                    f"{list(VISIBILITY_CLASSES)}. Fix the grant before starting "
                    "the bridge."
                )
            # And the spec's absolute (CONSENT-GATE-SPEC.md §Scope: "a guest is
            # never able to write private memories") is enforced here, not
            # merely documented: `private` in write_scope would make the very
            # class the human's own conversation defaults to writable by a
            # guest.
            if "private" in write_scope:
                raise SystemExit(
                    f"bridge_config.json: guest '{name}' has write_scope naming "
                    "'private' — a guest is never able to write private "
                    "memories. Use 'shared'."
                )
            guests[name.strip().lower()] = GuestGrant(
                approved=bool(grant.get("approved", False)),
                tools=list(grant.get("tools", [])),
                read_scope=read_scope,
                write_scope=write_scope,
                read_types=read_types,
                write_types=write_types,
                token_hash=str(grant.get("token_hash", "")),
            )
        return cls(
            profile=raw.get("profile", profile),
            human_name=raw.get("human_name", ""),
            interactive_approval=bool(raw.get("interactive_approval", False)),
            guests=guests,
            profile_dir=profile_dir,
        )
