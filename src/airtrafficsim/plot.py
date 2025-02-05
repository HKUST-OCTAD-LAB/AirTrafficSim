"""
Lightweight matplotlib utils.

When developing on a remote host, you may want to view interactive plots
in a web browser. Tunnel port 8988 and use `WEB=1 python3 scripts/{}.py`
to enable the webagg backend.

Requires extras:

- `plot`
- `polars` for additional plots
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import matplotlib as mpl
import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from typing import Callable, Literal

    import polars as pl
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from .column import Column


class CMapCycler:
    def __init__(self, cmap_name: str = "tab10"):
        cmap = mpl.colormaps[cmap_name]
        self.colors: tuple[tuple[float, float, float]] = cmap.colors  # type: ignore
        self.N = cmap.N

    def __getitem__(self, i: int) -> tuple[float, float, float]:
        return self.colors[i % self.N]


C = CMapCycler()
"""Default color cycle"""


def init_style(
    dark: bool = False, fast: bool = True, use_tex: bool = True
) -> None:
    if fast:
        plt.style.use("fast")
    if dark:
        plt.style.use("dark_background")

    rc_params: dict[str, Any] = {
        "axes.axisbelow": True,  # make gridlines appear below plot
    }
    if use_tex:
        rc_params.update(
            {
                "text.usetex": use_tex,
                "text.latex.preamble": (
                    r"\usepackage{amsmath}"  # for \text
                    r"\usepackage{amssymb}"  # for real
                    r"\usepackage{siunitx}"
                    r"\usepackage{gensymb}"  # for \degree
                ),
                "font.family": "serif",
                "font.serif": "cm",
            }
        )
    plt.rcParams.update(rc_params)
    if os.getenv("WEB"):
        mpl.use("webagg")


def new_figure(*args: Any, **kwargs: Any) -> Figure:
    init_style()
    if "figsize" not in kwargs:
        kwargs["figsize"] = (16 * 0.5, 9 * 0.5)
    fig = plt.figure(*args, **kwargs)
    fig.set_layout_engine("tight")
    return fig


def setup_xy(
    ax: Axes,
    x: Column,
    y: Column,
    title: (
        Callable[[Column, Column], str] | Literal["default"] | str | None
    ) = None,
) -> None:
    """
    :param title: a function that computes the title from x and y,
        a fixed string, or explicitly None.
    """
    ax.set_xlabel(x.label)
    ax.set_ylabel(y.label)
    if title is not None:
        if callable(title):
            title_ = title(x, y)
        elif title == "default":
            title_ = f"Plot of {y.display_name} against {x.display_name}"
        else:
            title_ = title
        ax.set_title(title_)


#
# the following are highly opinionated and are used to reduce code duplication,
# not to provide a general-purpose API.
#


def add_linear_trendline(
    ax: Axes,
    x: pl.Series,
    y: pl.Series,
    *,
    x_symbol: str = "x",
    y_symbol: str = "y",
    with_legend: bool = True,
    **kwargs: Any,
) -> None:
    """
    Note: legend is NOT added, call `ax.legend()` manually.
    """
    from scipy.stats import linregress

    import numpy as np

    slope, intercept, r, _p, _se = linregress(x, y)

    intercept_sign = "+" if intercept >= 0 else ""
    label = (
        "Linear Trendline\n"
        f"${y_symbol} = {slope:.4f}{x_symbol}{intercept_sign}{intercept:.4f}$\n"
        f"$R^2 = {r**2:.4f}$"
    )

    x_range = np.linspace(x.min(), x.max(), 100)  # type: ignore
    y_trend = slope * x_range + intercept
    if with_legend:
        kwargs["label"] = label
    ax.plot(x_range, y_trend, **kwargs)


def basic_scatter(
    df: pl.DataFrame,
    x: Column,
    y: Column,
    *,
    with_line: bool = False,
) -> Figure:
    fig = new_figure()
    ax = fig.subplots()
    setup_xy(ax, x, y)
    if with_line:
        ax.plot(x(df), y(df))
    ax.scatter(x(df), y(df), marker="+")
    return fig
