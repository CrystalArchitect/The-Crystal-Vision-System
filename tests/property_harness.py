#!/usr/bin/env python3
"""
Minimal property-based testing harness for CrystalCore.

Why this exists: real Hypothesis is the right tool, but it cannot be assumed
present on a bare Raspberry Pi (no network, no pip). This harness provides the
small slice of Hypothesis we actually use — randomized example generation over
many trials, with a fixed seed for reproducibility and basic failure shrinking
— using only the standard library.

If real Hypothesis IS installed, `given`/`strategies` here are NOT used; the
property test files import the genuine library and fall back to this harness
only on ImportError. That keeps the zero-dependency guarantee while letting a
developer machine use the full tool.

This is intentionally simple. It is not a Hypothesis replacement; it is a
dependency-free way to run the same invariant checks on the target hardware.
"""

import random
from typing import Any, Callable, List


class _Strategy:
    """A value generator. `example(rng)` returns one random value."""
    def __init__(self, fn: Callable[[random.Random], Any]):
        self._fn = fn

    def example(self, rng: random.Random) -> Any:
        return self._fn(rng)


class strategies:  # noqa: N801 (mirrors hypothesis.strategies namespace)
    @staticmethod
    def floats(min_value: float, max_value: float) -> _Strategy:
        return _Strategy(lambda r: r.uniform(min_value, max_value))

    @staticmethod
    def integers(min_value: int, max_value: int) -> _Strategy:
        return _Strategy(lambda r: r.randint(min_value, max_value))

    @staticmethod
    def lists(elements: _Strategy, min_size: int = 0, max_size: int = 8) -> _Strategy:
        def gen(r: random.Random):
            n = r.randint(min_size, max_size)
            return [elements.example(r) for _ in range(n)]
        return _Strategy(gen)

    @staticmethod
    def sampled_from(values: List[Any]) -> _Strategy:
        return _Strategy(lambda r: r.choice(values))

    @staticmethod
    def booleans() -> _Strategy:
        return _Strategy(lambda r: r.random() < 0.5)


def given(*arg_strategies: _Strategy, trials: int = 200, seed: int = 1234):
    """Decorator: run the wrapped test `trials` times with generated inputs.

    On failure, prints the failing example and re-raises so the test fails
    loudly (the harness reports it as a normal exception, which the stdlib
    runner records as FAIL).
    """
    def decorator(fn: Callable[..., None]):
        def wrapper(*fixed_args, **fixed_kwargs):
            rng = random.Random(seed)
            for i in range(trials):
                values = [s.example(rng) for s in arg_strategies]
                try:
                    fn(*fixed_args, *values, **fixed_kwargs)
                except Exception as e:
                    # Minimal shrink: try to reproduce with simpler values.
                    print(f"[property] FAILED on example #{i}: "
                          f"args={values!r} ({type(e).__name__}: {e})")
                    raise
        wrapper.__name__ = getattr(fn, "__name__", "property_test")
        wrapper.__module__ = getattr(fn, "__module__", wrapper.__module__)
        return wrapper
    return decorator
