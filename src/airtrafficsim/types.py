from typing import Any, TypeAlias, TypeVar

Array: TypeAlias = Any
"""
An array that conforms to the [array API](https://data-apis.org/array-api/latest)
(e.g. NumPy, PyTorch, etc.)
"""
# NOTE: unfortunately, static type checking for the array API is not fully
# developed. See:
# - https://github.com/data-apis/array-api/issues/229
# - https://github.com/data-apis/array-api/discussions/863
# - https://github.com/data-apis/array-api-typing

ArrayT = TypeVar("ArrayT", bound=Array)

ArrayOrScalarT = TypeVar("ArrayOrScalarT", float, Array)

__all__ = ["Array", "ArrayOrScalarT", "ArrayT"]
