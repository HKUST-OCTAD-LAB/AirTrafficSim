"""Miscellaneous utility functions (stdlib only).

Do not import any other modules from this package here.
"""

from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from typing import Callable, Concatenate, Generic, ParamSpec, TypeVar

logger = getLogger(__name__)


P = ParamSpec("P")
S = TypeVar("S")


def hook(func: Callable[P, S]) -> Hook[P, S]:
    """Wraps a function in a `Hook` object, making it interceptable.

    Decorating a function with `@hook` allows its behavior to be observed,
    extended, or even completely replaced by downstream code.

    Example usage:
    ```py
    @hook
    def foo(state, t):
        ... # pure jax/torch/numpy code...
    ```
    For example, to time the function:
    ```py
    import time

    def timing_interceptor(original_fn, *args, **kwargs):
        start = time.perf_counter()
        result = original_fn(*args, **kwargs)
        end = time.perf_counter()
        print(f"{original_fn.__name__} took {end - start:.4f}s")
        return result

    foo.intercept(timing_interceptor)
    ```
    """
    return Hook(handler=func)


@dataclass(slots=True)
class Hook(Generic[P, S]):
    """A callable that implements the middleware pattern."""

    handler: Callable[P, S]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> S:
        return self.handler(*args, **kwargs)

    def intercept(
        self, interceptor: Callable[Concatenate[Callable[P, S], P], S]
    ) -> Hook[P, S]:
        original_handler = self.handler
        self.handler = lambda *args, **kwargs: interceptor(
            original_handler, *args, **kwargs
        )
        return self

    def debug(self) -> Hook[P, S]:
        """Log the function arguments and result."""

        def debug_interceptor(
            original_fn: Callable[P, S], /, *args: P.args, **kwargs: P.kwargs
        ) -> S:
            result = original_fn(*args, **kwargs)
            all_args = ", ".join(
                list(map(repr, args))
                + [f"{k}={v!r}" for k, v in kwargs.items()]
            )
            logger.debug(f"{original_fn.__name__}({all_args}) -> {result!r}")
            return result

        return self.intercept(debug_interceptor)
