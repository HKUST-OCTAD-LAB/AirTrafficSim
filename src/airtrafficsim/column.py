from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from .units import UnitBase

if TYPE_CHECKING:
    from typing import Any

    import polars as pl


@dataclass
class Column:
    unit: UnitBase | None
    display_name: str | None = None
    symbol: str | None = None
    identifier: str | None = None
    """
    A unique identifier for retrieving the series in a dataframe (optional)
    """

    @property
    def label(self) -> str:
        if self.display_name and self.symbol:
            label = f"{self.display_name}, {self.symbol}"
        elif self.display_name:
            label = self.display_name
        elif self.symbol:
            label = f"{self.symbol}"
        else:
            raise ValueError("Either display_name or symbol must be provided.")
        if self.unit is not None:  # hide for dimensionless
            label += f" (${self.unit.to_siunitx()}$)"
        return label

    @overload
    def __call__(self, df: pl.DataFrame) -> pl.Series: ...

    @overload
    def __call__(self, df: Any) -> Any: ...

    def __call__(self, df: Any) -> Any:
        """Returns series in the dataframe."""
        return df[self.identifier]
