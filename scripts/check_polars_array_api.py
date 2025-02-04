"""Quick script to find equivalent Array API methods in polars."""

import inspect
from logging import getLogger
from typing import Any

import array_api_strict
import polars as pl

import airtrafficsim._polars_array_api as polars_array_api

logger = getLogger(__name__)


def get_signature(x: Any) -> Any:
    try:
        return inspect.signature(x)
    except TypeError:
        return ""


def main() -> None:
    for array_api_attr in dir(array_api_strict):
        if array_api_attr.startswith("_"):
            continue
        try:
            pl_array_api_attr = getattr(polars_array_api, array_api_attr)
        except AttributeError:
            logger.error(f"missing {array_api_attr}")
            if array_api_attr in dir(pl.Expr):
                logger.info("-- found exact match")
            continue

        array_api_sig = get_signature(getattr(array_api_strict, array_api_attr))
        pl_array_api_sig = get_signature(pl_array_api_attr)
        debug = (
            f"{array_api_attr}{array_api_sig}\n"
            f"{pl_array_api_attr}{pl_array_api_sig}"
        )
        print(debug)


if __name__ == "__main__":
    main()
