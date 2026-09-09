# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Deprecated import alias — ``starline`` is now ``consent_transport``.

This project's peer-to-peer transport was renamed from "Starline" to
``consent_transport`` so the built layer carries a plain, literal name (the
mythic "Starlines" live on in ``mythos/``, not here). Importing ``starline``
still works — it re-exports ``consent_transport`` unchanged — but is
deprecated and will be removed in a future release.
"""
import importlib as _importlib
import sys as _sys
import warnings as _warnings

_warnings.warn(
    "starline has been renamed to consent_transport; "
    "this alias will be removed in a future release",
    DeprecationWarning,
    stacklevel=2,
)

from consent_transport import *  # noqa: F401,F403,E402
from consent_transport import __version__  # noqa: F401,E402

# Keep ``starline.<submodule>`` (and ``python -m starline.<submodule>``)
# resolving to the real package's modules for code written against the
# previous release.
for _sub in (
    "agent", "consent", "discovery", "fragment", "identity", "noise",
    "peers", "protocol", "run", "selftest", "transport",
):
    _sys.modules[f"{__name__}.{_sub}"] = _importlib.import_module(
        f"consent_transport.{_sub}"
    )

del _importlib, _sys, _warnings, _sub
