"""
ICAO International Standard Atmosphere.

Assumptions:

- air is dry, calorically perfect, perfect gas ($p = \\rho R T$).
- atmosphere is in hydrostatic equilibrium ($\\frac{dp}{dz} = -\\rho g$).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Annotated

    from .. import units as u
    from ..quantity import (
        Density,
        GeopotentialAltitude,
        SpeedOfSound,
        StaticPressure,
        StaticTemperature,
        TemperatureGradient,
    )

H_BELOW_TROP: Annotated[float, GeopotentialAltitude(u.METER)] = 11000.0
"""
The tropopause is the separation between the troposphere and the stratosphere.
In ISA, its geopotential altitude is constant.
"""
BETA_BELOW_TROP: Annotated[
    float, TemperatureGradient(u.KELVIN * u.METER**-1)
] = -0.0065

T_0: Annotated[float, StaticTemperature(u.KELVIN)] = 288.15
P_0: Annotated[float, StaticPressure(u.PASCAL)] = 101325.0
RHO_0: Annotated[float, Density(u.KGM3)] = 1.225
A_0: Annotated[float, SpeedOfSound(u.MPS)] = 340.294


T_11: Annotated[float, StaticTemperature(u.KELVIN)] = 216.65
P_11: Annotated[float, StaticPressure(u.PASCAL)] = 22632.06
