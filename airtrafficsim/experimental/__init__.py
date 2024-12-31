"""
Rewrite of airtrafficsim. See `./README.md` for more information.
"""

import logging

logger = logging.getLogger(__name__)

try:
    import polars as pl
except ImportError:
    pl = None  # type: ignore

if pl is not None:
    from types import ModuleType

    from polars import Expr

    from . import _polars_array_api

    @pl.api.register_expr_namespace("__array_namespace__")
    class ArrayAPI:
        """
        Polars isn't exactly an array library, but we would like to make it
        compatible with the array API as far as possible.

        See: https://github.com/pola-rs/polars/issues/2249

        Activate it by importing `airtrafficsim.experimental`.
        """

        # NOTE: a plain register_expr_namespace would work, but static typing
        # would not work and we would have to duplicate the API. See:
        #
        # - https://github.com/pola-rs/polars/issues/14475
        # - https://github.com/pola-rs/polars/issues/13899
        # - workaround: https://github.com/StefanBRas/polugins/blob/main/polugins/__init__.py

        def __init__(self, expr: Expr) -> None:
            self._expr = expr

        def __call__(self) -> ModuleType:
            """
            Return the `__array_namespace__` module.

            Unsupported functions:

            - `bitwise_left_shift`
            - `bitwise_right_shift`
            - `broadcast_arrays`
            - `broadcast_to`
            - `can_cast`
            - `complex128`
            - `complex64`
            - `conj`
            - `copysign`
            - `empty`
            - `empty_like`
            - `expand_dims`
            - `expm1`
            - `eye`
            - `finfo`
            - `from_dlpack`
            - `full`
            - `full_like`
            - `get_array_api_strict_flags`
            - `iinfo`
            - `imag`
            - `isdtype`
            - `linspace`
            - `matmul`
            - `matrix_transpose`
            - `meshgrid`
            - `moveaxis`
            - `newaxis`
            - `nextafter`
            - `ones_like`
            - `permute_dims`
            - `real`
            - `reset_array_api_strict_flags`
            - `result_type`
            - `roll`
            - `set_array_api_strict_flags`
            - `squeeze`
            - `tensordot`
            - `tile`
            - `tril`
            - `triu`
            - `trunc`
            - `unique_all`
            - `unstack`
            - `zeros_like`
            """
            return _polars_array_api

    # from functools import wraps
    # from typing import Any, Callable, TypeVar

    # M = TypeVar("M", bound=Callable[..., Any])
    # """Method to be registered"""

    # def register_expr_method(method: M) -> M:
    #     """
    #     Decorator to register a method as a `pl.Expr` method.
    #     """

    #     def inner(*args: Any, **kwargs: Any) -> M:
    #         class _AirTrafficSimOperations:
    #             __doc__ = method.__doc__

    #             def __init__(self, expr: pl.Expr) -> None:
    #                 self._expr = expr

    #             @wraps(method)
    #             def __call__(self, *args: Any, **kwargs: Any) -> Any:
    #                 return method(self._expr, *args, **kwargs)

    #         pl.api.register_expr_namespace(method.__name__)(
    #             _AirTrafficSimOperations
    #         )

    #         return method

    #     return inner()
