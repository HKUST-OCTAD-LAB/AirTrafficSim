from bisect import bisect_right
from typing import Annotated, Callable, TypeVar

_T = TypeVar("_T")
ArrayApiNamespace = Annotated[_T, "ArrayApiNamespace"]
"""See:

- https://github.com/data-apis/array-api/issues/229
- https://github.com/data-apis/array-api/discussions/863
- https://github.com/data-apis/array-api-typing"""


def array_namespace(value) -> ArrayApiNamespace:
    return getattr(value, "__array_namespace__", None)


def where(where, left, right: Callable, *, xp: ArrayApiNamespace | None):
    if xp is not None:
        return xp.where(where, left, right())
    if where:
        return left
    return right()


def linear_interp(
    x, xs, fs, left=None, right=None, *, xp: ArrayApiNamespace | None
):
    if xp is not None:
        return xp.interp(x, xs, fs, left, right)

    index = bisect_right(xs, x)
    if index == 0:
        return fs[0] if left is None else left
    if index >= len(xs):
        return fs[-1] if right is None else right

    x0 = xs[index - 1]
    x1 = xs[index]
    y0 = fs[index - 1]
    y1 = fs[index]
    if x1 == x0:
        return y0

    slope = (y1 - y0) / (x1 - x0)
    return y0 + slope * (x - x0)
