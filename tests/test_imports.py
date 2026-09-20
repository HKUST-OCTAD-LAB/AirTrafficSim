import importlib
import pkgutil

import pytest

import airtrafficsim

MODULES = [
    m.name
    for m in pkgutil.walk_packages(
        airtrafficsim.__path__, f"{airtrafficsim.__name__}."
    )
]


@pytest.mark.parametrize("module", MODULES)
def test_import(module: str) -> None:
    """
    Names imported under `TYPE_CHECKING` but used at runtime pass mypy and only
    fail on import.
    """
    importlib.import_module(module)
