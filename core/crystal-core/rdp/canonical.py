# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""RDP-JCS Profile v1 — deterministic canonical JSON for the record chain.

The point of canonicalization is simple: the *same* event must always produce
the *same* bytes, on any machine, in any language, so that a hash over those
bytes means something. Two parties who disagree on the bytes disagree on the
hash, and the chain stops proving anything.

This is a JSON Canonicalization Scheme (RFC 8785 / JCS) with one deliberate
profile applied to numbers — the "decimal-6" profile:

  * Every JSON number is treated as a fixed-point decimal and quantized to
    exactly 6 fractional digits, rounding halves *away from zero*.
  * Numbers are rendered unquoted, always with all 6 fractional digits
    (``1`` -> ``1.000000``, ``0.5`` -> ``0.500000``).
  * ``NaN``, the infinities, and any magnitude greater than 2**53 - 1 are
    rejected — they have no unambiguous decimal-6 form and no place in a record
    that has to survive a round-trip through other languages' JSON parsers.

Object keys are sorted (by Unicode code point), arrays keep their order, strings
use standard JSON escaping, and there is no insignificant whitespace.

Note on scope: this profile is defined *by this module and its selftest*. There
is no external frozen conformance suite to match — the RDP handoff described one
that never actually existed. So the rules here are the specification, and
``rdp/selftest.py`` is their ground truth. Where JCS itself is precise (string
escaping, member ordering) we follow it; the number handling is our profile.

    from rdp.canonical import canonical_serialize, sha256_hex
    canonical_serialize({"b": 1, "a": 0.5})   # -> '{"a":0.500000,"b":1.000000}'
"""

from __future__ import annotations

import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# The largest integer a IEEE-754 double can hold exactly. Values beyond this
# cannot be relied on to survive a trip through a JSON parser that decodes
# numbers to floats, so the profile refuses them rather than record a value it
# cannot guarantee another reader will reproduce.
MAX_MAGNITUDE = 2 ** 53 - 1

# Quantum for the decimal-6 profile: six fractional digits.
_SIX_PLACES = Decimal("0.000000")


def _to_decimal(x: object) -> Decimal:
    """Coerce a supported numeric input to an exact Decimal.

    floats are converted via ``str`` so we capture the value the human wrote
    ("0.1"), not the binary approximation a double actually stores.
    """
    if isinstance(x, bool):  # bool is an int subclass — never a number here
        raise TypeError("bool is not a number in canonical JSON")
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    if isinstance(x, float):
        return Decimal(str(x))
    if isinstance(x, str):
        return Decimal(x)
    raise TypeError(f"not a number: {type(x).__name__}")


def quantize6(x: object) -> Decimal:
    """Quantize *x* to 6 fractional digits, halves away from zero.

    Rejects NaN, +/-Infinity, and any magnitude greater than 2**53 - 1 with
    ``ValueError``. ``decimal.ROUND_HALF_UP`` rounds ties away from zero, which
    is exactly the profile's rule.
    """
    try:
        d = _to_decimal(x)
    except InvalidOperation as exc:  # e.g. Decimal("nonsense")
        raise ValueError(f"not a valid number: {x!r}") from exc
    if d.is_nan() or d.is_infinite():
        raise ValueError("NaN and Infinity are not representable")
    if abs(d) > MAX_MAGNITUDE:
        raise ValueError(f"magnitude exceeds 2**53-1: {d}")
    return d.quantize(_SIX_PLACES, rounding=ROUND_HALF_UP)


def render_number(x: object) -> str:
    """Render a number in canonical decimal-6 form, e.g. ``-0`` -> ``0.000000``."""
    d = quantize6(x)
    if d == 0:  # collapse a negative zero to the single canonical zero
        return "0.000000"
    return str(d)


def canonical_serialize(obj: object) -> str:
    """Serialize *obj* to its canonical JSON string (no trailing newline)."""
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, Decimal)):
        return render_number(obj)
    if isinstance(obj, str):
        # json.dumps gives RFC-8785-compatible escaping: minimal escapes,
        # lowercase \uXXXX for control characters, UTF-8 passed through.
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(canonical_serialize(v) for v in obj) + "]"
    if isinstance(obj, dict):
        for k in obj:
            if not isinstance(k, str):
                raise TypeError(f"object keys must be strings, got {type(k).__name__}")
        items = sorted(obj.keys())
        return "{" + ",".join(
            json.dumps(k, ensure_ascii=False) + ":" + canonical_serialize(obj[k])
            for k in items
        ) + "}"
    raise TypeError(f"not JSON-serializable in this profile: {type(obj).__name__}")


def canonical_bytes(obj: object) -> bytes:
    """Canonical JSON of *obj* encoded as UTF-8 — the bytes that get hashed."""
    return canonical_serialize(obj).encode("utf-8")


def sha256_hex(data: object) -> str:
    """SHA-256 hex digest of a str (UTF-8), bytes, or a JSON-able object.

    A str or bytes is hashed directly; anything else is canonicalized first.
    """
    if isinstance(data, str):
        raw = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        raw = bytes(data)
    else:
        raw = canonical_bytes(data)
    return hashlib.sha256(raw).hexdigest()
