# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Host trust — classify where code is running. Not a seventh OS.

See docs/HOST-TRUST.md. Steward persist refuses on SHARED and UNKNOWN.
Job-scoped temp is allowed only on GitHub-hosted shared jobs.
HADES is a vendor pool name, not a class here.
"""

from .classify import (
    HostClass,
    classify,
    is_ephemeral_path,
    refuse_steward_persist,
    require_steward_persist,
)

__all__ = [
    "HostClass",
    "classify",
    "is_ephemeral_path",
    "refuse_steward_persist",
    "require_steward_persist",
]
