"""
ICAO International Standard Atmosphere.

Assumptions:

- air is dry, calorically perfect, perfect gas ($p = \\rho R T$).
- atmosphere is in hydrostatic equilibrium ($\\frac{dp}{dz} = -\\rho g$).
"""

from typing import Annotated

from ..quantity import (
    Density,
    GeopotentialAltitude,
    StaticPressure,
    StaticTemperature,
    TemperatureGradient,
)

H_BELOW_TROP: Annotated[float, GeopotentialAltitude("m")] = 11000.0
"""
The tropopause is the separation between the troposphere and the stratosphere.
In ISA, its geopotential altitude is constant.
"""
BETA_BELOW_TROP: Annotated[float, TemperatureGradient("K m⁻¹")] = -0.0065

T_0: Annotated[float, StaticTemperature("K")] = 288.15
P_0: Annotated[float, StaticPressure("Pa")] = 101325.0
RHO_0: Annotated[float, Density("kg m⁻³")] = 1.225

T_11: Annotated[float, StaticTemperature("K")] = 216.65
P_11: Annotated[float, StaticPressure("Pa")] = 22632.06
