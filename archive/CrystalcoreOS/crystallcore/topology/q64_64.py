#!/usr/bin/env python3
"""
Q64.64 Fixed-Point Arithmetic
Sentinel Constitutional Execution System — Phase 3

Q64.64 provides 64-bit integer + 64-bit fractional fixed-point arithmetic.
Ideal for high-precision computation in resource-constrained environments
(remote Outback nodes, Starship onboard systems) without floating-point drift.

Format: 128-bit signed integer, interpreted as 64-bit.64-bit fixed point.
Range: approximately ±9.2e18 with fractional precision to 2^-64.
"""

from typing import Union, Tuple

# Fractional part is 2^64
FRAC_BITS = 64
FRAC_SCALE = 1 << FRAC_BITS  # 2^64


class Q6464:
    """64.64 fixed-point number."""

    def __init__(self, value: Union[int, float, str] = 0):
        """Initialize Q64.64 from int, float, or string."""
        if isinstance(value, Q6464):
            self.raw = value.raw
        elif isinstance(value, int):
            self.raw = value * FRAC_SCALE
        elif isinstance(value, float):
            self.raw = int(value * FRAC_SCALE)
        elif isinstance(value, str):
            try:
                f = float(value)
                self.raw = int(f * FRAC_SCALE)
            except ValueError:
                raise ValueError(f"Cannot parse Q6464 from {value}")
        else:
            raise TypeError(f"Cannot construct Q6464 from {type(value)}")

    def __add__(self, other: "Q6464") -> "Q6464":
        result = Q6464()
        result.raw = self.raw + other.raw
        return result

    def __sub__(self, other: "Q6464") -> "Q6464":
        result = Q6464()
        result.raw = self.raw - other.raw
        return result

    def __mul__(self, other: "Q6464") -> "Q6464":
        result = Q6464()
        result.raw = (self.raw * other.raw) >> FRAC_BITS
        return result

    def __truediv__(self, other: "Q6464") -> "Q6464":
        if other.raw == 0:
            raise ZeroDivisionError("Q6464 division by zero")
        result = Q6464()
        result.raw = (self.raw << FRAC_BITS) // other.raw
        return result

    def __eq__(self, other: "Q6464") -> bool:
        return self.raw == other.raw

    def __lt__(self, other: "Q6464") -> bool:
        return self.raw < other.raw

    def __le__(self, other: "Q6464") -> bool:
        return self.raw <= other.raw

    def __gt__(self, other: "Q6464") -> bool:
        return self.raw > other.raw

    def __ge__(self, other: "Q6464") -> bool:
        return self.raw >= other.raw

    def __repr__(self) -> str:
        return f"Q6464({self.to_float():.16f})"

    def to_float(self) -> float:
        """Convert to Python float (loses precision)."""
        return self.raw / FRAC_SCALE

    def to_int(self) -> int:
        """Get integer part (truncates)."""
        return self.raw >> FRAC_BITS

    def fractional_part(self) -> "Q6464":
        """Get fractional part (0 to 1)."""
        result = Q6464()
        result.raw = self.raw & ((1 << FRAC_BITS) - 1)
        return result

    def abs(self) -> "Q6464":
        """Absolute value."""
        result = Q6464()
        result.raw = abs(self.raw)
        return result

    def sqrt(self) -> "Q6464":
        """Integer square root using Newton's method."""
        if self.raw < 0:
            raise ValueError("Cannot take sqrt of negative Q6464")
        if self.raw == 0:
            return Q6464(0)

        x = Q6464()
        x.raw = self.raw
        x_prev = Q6464()
        x_prev.raw = 0

        for _ in range(100):
            x_prev.raw = x.raw
            x = (x + Q6464().__class__.from_raw(self.raw // x.raw)) * Q6464(0.5)
            if abs(x.raw - x_prev.raw) < 1:
                break

        return x

    @classmethod
    def from_raw(cls, raw: int) -> "Q6464":
        """Create Q6464 from raw 128-bit representation."""
        result = cls()
        result.raw = raw
        return result


def q64_64_add(a: Q6464, b: Q6464) -> Q6464:
    """Add two Q64.64 values."""
    return a + b


def q64_64_mul(a: Q6464, b: Q6464) -> Q6464:
    """Multiply two Q64.64 values."""
    return a * b


def q64_64_div(a: Q6464, b: Q6464) -> Q6464:
    """Divide two Q64.64 values."""
    return a / b
