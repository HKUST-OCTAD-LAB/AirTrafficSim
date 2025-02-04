from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, overload

from .annotations import Quantity, Units

if TYPE_CHECKING:
    from typing import Any

    import polars as pl
    from typing_extensions import Self


def into_latex(unit: Units) -> str:
    raise NotImplementedError


@dataclass
class Column(Generic[Units]):
    quantity: Quantity[Units]
    display_name: str | None = None
    symbol: str | None = None
    identifier: str | None = None
    """
    A unique identifier for retrieving the series in a dataframe (optional)
    """

    @classmethod
    def from_quantity(cls, quantity: Quantity[Units]) -> Self:
        if (doc := quantity.__doc__) is not None:
            display_name = doc.split("\n")[0].split(",")[0]
            print(display_name)
        return cls(quantity)

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
        if self.quantity.unit is not None:  # hide for dimensionless
            label += f" (${self.quantity.unit}$)"
        return label

    @overload
    def __call__(self, df: pl.DataFrame) -> pl.Series: ...

    @overload
    def __call__(self, df: Any) -> Any: ...

    def __call__(self, df: Any) -> Any:
        """Returns series in the dataframe."""
        return df[self.identifier]
